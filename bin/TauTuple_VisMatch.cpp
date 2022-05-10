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
      double match_dR = 0.1;
      double pfCand_MinPt = 1.0; // GeV consider only with bigger pt


      for(size_t current_entry = 0; current_entry < n_entries; ++current_entry)
      {
        if(current_entry % 10000 == 0) std::cout << "Events processed: " << current_entry << " ("
                                                 << (int) ((double)current_entry/n_entries*100)
                                                 << "%)" << std::endl;
        tauTuple->GetEntry(current_entry);
        const auto& tau = tauTuple->data();

        if(tau.genLepton_kind==5 && tau.genLepton_vis_pt>=10.0) // to take only hadronic Taus
        { 
          auto genLeptons = reco_tau::gen_truth::GenLepton::fromRootTuple
                            <std::vector<Int_t>, std::vector<Long64_t>, std::vector<Float_t>>
                            (
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

          // debug
          // genLeptons.PrintDecay(std::cout);
          // std::cout << "--------------------------------------\n";
          // std::cin.ignore();
          
          // if(genTauDecayMode == 1) continue;

          double disp{-9};
          LorentzVectorXYZ gentau_vis = genLeptons.visibleP4();
          ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double>> stau_p4;

          for(auto genparticle_: all_gen_particles)
          {
            if(std::abs(genparticle_.pdgId) == 15 && genparticle_.isLastCopy){
              disp = genparticle_.vertex.rho(); //disp = genparticle_.vertex.r();
            }

            if(std::abs(genparticle_.pdgId) == 1000015 && genparticle_.isLastCopy) {
              stau_p4 = genparticle_.p4;
            }
          }

          if(disp == -9) {
            std::cout << "No Tau is found!" << std::endl;
            continue;
          }

          if(stau_p4.X() == 0.0) {
            std::cout << "No SusyTau is found!" << std::endl;
            continue;
          }

          if(tau.jet_index<0) continue; // if there is no seeding jet

          // Efficiency histograms only:
          auto MatchToPfCand = [&](const std::string& prefix,
                                   const ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double>> matchedVec
                                   ) -> int
          {

            for(int i=0; i < tauTuple->get<std::vector<float>>(prefix+"_pt").size(); i++)
            {
              float pt = tauTuple->get<std::vector<float>>(prefix+"_pt")[i];
              if( pt < pfCand_MinPt) continue; // skip low energetic pfCands

              float eta = tauTuple->get<std::vector<float>>(prefix+"_eta")[i];
              float phi = tauTuple->get<std::vector<float>>(prefix+"_phi")[i];
              
              // match vector to the object
              float dR_current = TMath::Sqrt( TMath::Power(eta-matchedVec.eta(),2) + TMath::Power(phi-matchedVec.phi(),2) );

              if( dR_current < match_dR ) return i; // return index of pfCand
            }
            return -1;
          };
          

          int track_i  = MatchToPfCand("pfCand", stau_p4);

          if(track_i >= 0) {
            std::cout << "#####################################################################################################################################################\n";
            genLeptons.PrintDecay(std::cout);
            std::cout << "--------------------------------------\n";
            for(auto p: all_gen_particles)
            {
              std::cout << "pdgId=" << p.pdgId << " pt=" << p.p4.pt() << " eta=" << p.p4.eta() << " phi=" << p.p4.phi()
                        << " E=" << p.p4.energy() << " m=" << p.p4.mass()
                        << " vx=" << p.vertex.x() << " vy=" << p.vertex.y() << " vz=" << p.vertex.z() << " vrho=" << p.vertex.rho()
                        << " vr=" << p.vertex.r() << " q=" << p.charge
                        << std::endl;
            }
            std::cout << "--------------------------------------\n";
            std::cout << "PfCand:\n";
            std::cout << "pt: " << tau.pfCand_pt[track_i] << " eta: " << tau.pfCand_eta[track_i] << " phi: " << tau.pfCand_phi[track_i] << " mass: " << tau.pfCand_mass[track_i]
                      << " charge: " << tau.pfCand_charge[track_i]
                      << " vtx: " << tau.pfCand_vertex_x[track_i] << " " << tau.pfCand_vertex_y[track_i] << " " << tau.pfCand_vertex_z[track_i] << " " << tau.pfCand_vertex_t[track_i] << " "
                      << " nHits: " << tau.pfCand_nHits[track_i]
                      << " particleType: " << tau.pfCand_particleType[track_i]
                      // << " nPixelHits: " << tau.pfCand_nPixelHits[track_i]
                      // << " nPixelLayers: " << tau.pfCand_nPixelLayers[track_i]
                      // << " nStripLayers: " << tau.pfCand_nStripLayers[track_i]
                      << " Tau Signal: " << tau.pfCand_tauSignal[track_i]
                      << " ECAL/HCAL energy: " << tau.pfCand_caloFraction[track_i]  << " " << tau.pfCand_hcalFraction[track_i]
                      << std::endl;

            
            std::cin.ignore();
          }

        }
      }
    }


  private:
    std::vector<std::string> input_files;
    std::string outputfile;
    std::shared_ptr<TauTuple> tauTuple;
    size_t n_entries;

};

};

PROGRAM_MAIN(analysis::PfCandStudy, Arguments)