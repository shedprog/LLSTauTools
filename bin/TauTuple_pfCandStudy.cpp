#include <string>
#include <iostream>
#include <fstream>
#include <cmath>
#include <vector>
#include <sstream>
#include <cmath>
#include <iomanip>

#include "TFile.h"
#include "TH1.h"
#include "TH2.h"
#include "TH3.h"
#include "TGraph.h"
#include "TTree.h"
#include "TROOT.h"
#include "TLorentzVector.h"
#include "TVector3.h"
#include "TH1F.h"
#include "TH1D.h"
#include "TChain.h"
#include "TMath.h"
#include "Math/VectorUtil.h"
#include "TRandom.h"
#include "TMath.h"

#include "FileTools.h"
#include "TauTuple.h"
#include "GenLepton.h"
#include "Functions.h"
#include "program_main.h"


struct Arguments {
    run::Argument<std::string> output{"output", "Full path to output file."};
    run::Argument<std::string> input_dir{"input-dir", "Full path to input dir."};
    run::Argument<int> n_files{"n-files", "Number of files to process.", -1};
};

namespace analysis {

class PfCandStudy {

public:
    using Tau = tau_tuple::Tau;
    using TauTuple = tau_tuple::TauTuple;
    using LorentzVectorXYZ = ROOT::Math::LorentzVector<ROOT::Math::PxPyPzE4D<double>>;

    PfCandStudy(const Arguments& args) :
      input_files(FindInputFiles(std::vector<std::string>{args.input_dir()},"^.*\\.root$","","")),
      outputfile(args.output())
    {
      if(args.n_files()>0) input_files.resize(args.n_files());
      std::cout << "Number of files to process: " << input_files.size() << std::endl;
      tauTuple = std::make_shared<TauTuple>("taus", input_files);

      n_entries = tauTuple->GetEntries();
      std::cout << "Number of entries: " << n_entries << std::endl;
    }

    void Run()
    {
      double up_lim = 200;
      double match_dR = 0.1;

      // Lost Track to stau match
      TH2D *h2_lostTrack_stau = new TH2D("h2_lostTrack_stau","lostTrack match to stau within dR",200,0,up_lim, 200, 0, 1.5);
      TH2D *h2_lostTrack_pion = new TH2D("h2_lostTrack_pion","lostTrack match to pion within dR",200,0,up_lim, 200, 0, 1.5);

      // pfCand
      TH2D *h2_pfCand_stau = new TH2D("h2_pfCand_stau","pfCand match to stau within dR",200,0,up_lim, 200, 0, 1.5);
      TH2D *h2_pfCand_pion = new TH2D("h2_pfCand_pion","pfCand match to pion within dR",200,0,up_lim, 200, 0, 1.5);

      // isoTrack
      TH2D *h2_isoTrack_stau = new TH2D("h2_isoTrack_stau","isoTrack match to stau within dR",200,0,up_lim, 200, 0, 1.5);
      TH2D *h2_isoTrack_pion = new TH2D("h2_isoTrack_pion","isoTrack match to pion within dR",200,0,up_lim, 200, 0, 1.5);

      for(size_t current_entry = 0; current_entry < n_entries; ++current_entry)
      {
        if(current_entry % 10000 == 0) std::cout << "Events processed: " << current_entry << " ("
                                                 << (int) ((double)current_entry/n_entries*100)
                                                 << "%)" << std::endl;
        tauTuple->GetEntry(current_entry);
        const auto& tau = tauTuple->data();

        if(tau.genLepton_kind==5 && tau.genLepton_vis_pt>=10.0) // to take only hadronic Taus
        { 
          auto genLeptons = reco_tau::gen_truth::GenLepton::fromRootTuple<std::vector>(
                            tau.genLepton_lastMotherIndex,
                            tau.genParticle_pdgId,
                            tau.genParticle_mother,
                            tau.genParticle_charge,
                            tau.genParticle_isFirstCopy,
                            tau.genParticle_isLastCopy,
                            tau.genParticle_pt,
                            tau.genParticle_eta,
                            tau.genParticle_phi,
                            tau.genParticle_mass,
                            tau.genParticle_vtx_x,
                            tau.genParticle_vtx_y,
                            tau.genParticle_vtx_z);

          const std::vector<reco_tau::gen_truth::GenParticle>& all_gen_particles = genLeptons.allParticles();
          int genTauDecayMode = gen_dm_encode(genLeptons.nChargedHadrons(), genLeptons.nNeutralHadrons());

          double disp{-9};
          LorentzVectorXYZ gentau_vis = genLeptons.visibleP4();
          ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double>> stau_p4;

          for(auto genparticle_: all_gen_particles)
          {
            if(std::abs(genparticle_.pdgId) == 15 && genparticle_.isLastCopy)
              disp = genparticle_.vertex.r();
              // disp = genparticle_.vertex.rho();
            if(std::abs(genparticle_.pdgId) == 1000015 && genparticle_.isLastCopy)
              stau_p4 = genparticle_.p4;
          }

          assert(disp != -9);
          assert(stau_p4.X() != 0.0);

          double dR_gentau_stau = ROOT::Math::VectorUtil::DeltaR(gentau_vis, stau_p4);

          // Fitting and Filling matched lostTracks/pfCand/isoTrack
          auto lazyGenMatch = [&](const std::string& prefix, TH2D* h_stua, TH2D* h_pion) -> void {
            for(int i=0; i < tauTuple->get<std::vector<float>>(prefix+"_pt").size(); i++)
            {
              if(tauTuple->get<std::vector<float>>(prefix+"_pt")[i] < 3.0) continue;
              float eta = tauTuple->get<std::vector<float>>(prefix+"_eta")[i];
              float phi = tauTuple->get<std::vector<float>>(prefix+"_phi")[i];

              if( TMath::Sqrt( TMath::Power(eta-stau_p4.eta(),2) + TMath::Power(phi-stau_p4.phi(),2) ) < match_dR )
                h_stua->Fill(disp, dR_gentau_stau);

              for(size_t gen_idx = 0; gen_idx < tau.genParticle_pdgId.size(); ++gen_idx)
              {
                float eta_gen = tau.genParticle_eta[gen_idx];
                float phi_gen = tau.genParticle_phi[gen_idx];
                if( TMath::Sqrt( TMath::Power(eta-eta_gen,2) + TMath::Power(phi-phi_gen,2) ) < match_dR )
                  h_pion->Fill(disp, dR_gentau_stau);
              }
            }
          };

          lazyGenMatch("lostTrack", h2_lostTrack_stau, h2_lostTrack_pion);
          lazyGenMatch("pfCand", h2_pfCand_stau, h2_pfCand_pion);
          lazyGenMatch("isoTrack", h2_isoTrack_stau, h2_isoTrack_pion);
        }
      }
      TFile *outputFile = new TFile(outputfile.c_str(),"RECREATE");
      h2_lostTrack_stau->Write();
      h2_lostTrack_pion->Write();
      h2_pfCand_stau->Write();
      h2_pfCand_pion->Write();
      h2_isoTrack_stau->Write();
      h2_isoTrack_pion->Write();
      outputFile->Close();
    }


  private:
    std::vector<std::string> input_files;
    std::string outputfile;
    std::shared_ptr<TauTuple> tauTuple;
    size_t n_entries;

};

};

PROGRAM_MAIN(analysis::PfCandStudy, Arguments)