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

      // Numerical estimate of cand match
      TH1D *h1_tau_chHad = new TH1D("h1_tau_chHad","Hadronic tau nChargedHadrons",20,0,20);
      TH1D *h1_tau_nHad = new TH1D("h1_tau_nHad","Hadronic tau nCNeutralHadrons",20,0,20);

      TH1D *h1_tau_mass_3pr = new TH1D("h1_tau_mass_3pr","Hadronic tau mass",100, 0.0, 2.3);
      TH1D *h1_tau_mass_1pr = new TH1D("h1_tau_mass_1pr","Hadronic tau mass",100, 0.0, 2.3);
      TH1D *h1_tau_mass_1pr1p0 = new TH1D("h1_tau_mass_1pr1p0","Hadronic tau mass",100, 0.0, 2.3);
      TH1D *h1_tau_mass_1prNp0 = new TH1D("h1_tau_mass_1prNp0","Hadronic tau mass",100, 0.0, 2.3);

      for(size_t current_entry = 0; current_entry < n_entries; ++current_entry)
      {
        if(current_entry % 10000 == 0) std::cout << "Events processed: " << current_entry << " ("
                                                 << (int) ((double)current_entry/n_entries*100)
                                                 << "%)" << std::endl;
        tauTuple->GetEntry(current_entry);
        const auto& tau = tauTuple->data();

        // if(tau.genLepton_kind==5 && tau.genLepton_vis_pt>=1.0) // to take only hadronic Taus
        if(tau.genLepton_kind==5) // to take only hadronic Taus
        { 
          auto genLeptons = reco_tau::gen_truth::GenLepton::fromRootTuple<std::vector>(
                            true,
                            tau.genLepton_lastMotherIndex,
                            tau.genParticle_pdgId,
                            tau.genParticle_status,
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

          int nCharge = genLeptons.nChargedHadrons();
          int nNeutral = genLeptons.nNeutralHadrons();

          h1_tau_chHad->Fill(nCharge);
          h1_tau_nHad->Fill(nNeutral);

          LorentzVectorXYZ genTaup4 = genLeptons.visibleP4();
          float mass = genTaup4.mass();

          if(nCharge==3) h1_tau_mass_3pr->Fill(mass);
          if(nCharge==1 && nNeutral==0) h1_tau_mass_1pr->Fill(mass);
          if(nCharge==1 && nNeutral==1) h1_tau_mass_1pr1p0->Fill(mass);
          if(nCharge==1 && nNeutral>1) h1_tau_mass_1prNp0->Fill(mass);

          // h1_tau_mass->Fill(genTaup4.mass());

        }
      }
      TFile *outputFile = new TFile(outputfile.c_str(),"RECREATE");

      h1_tau_chHad->Write();
      h1_tau_nHad->Write();
      h1_tau_mass_3pr->Write();
      h1_tau_mass_1pr->Write();
      h1_tau_mass_1pr1p0->Write();
      h1_tau_mass_1prNp0->Write();

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
