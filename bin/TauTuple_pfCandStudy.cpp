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

namespace setup {
  
  // Lxy
  static const double lxy_min = 0.0, lxy_max = 100; //cm
  
  // matching
  static const double genLepton_jet_dR = 0.4;
  static const double genLepton_hpstau_dR = 0.4;
  static const double genLepton_jet_relPt = 0.2; // 20%
  static const double genParticle_pfCand_dR = 0.2;
  static const double genParticle_pfCand_relPt = 0.3; // 30%

  // selection
  static const double gen_vz_max = 100.0; //cm
  // static const double pfCand_pt_min = 1.0; // > 1 GeV
  static const double genLepton_minPt = 10.0; // 10GeV

  static const bool requre_stau = true;
}

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
      // match of the stau (at least one match)
      TH1D *h1_stau_pfCand    = new TH1D("h1_pfCand_stau","pfCand matches stau (Lxy)", 500, setup::lxy_min, setup::lxy_max);
      TH1D *h1_stau_lostTrack = new TH1D("h1_lostTrack_stau","lostTrack matches stau (Lxy)", 500, setup::lxy_min, setup::lxy_max);
      TH1D *h1_stau_isoTrack  = new TH1D("h1_isoTrack_stau","pfCand matches stau (Lxy)", 500, setup::lxy_min, setup::lxy_max);
      
      // Electron from tau matching
      TH1D *h1_tau_e_all  = new TH1D("h1_tau_e_all","All electron from tau taus (Lxy)", 500, setup::lxy_min, setup::lxy_max);
      TH1D *h1_tau_e_jet  = new TH1D("h1_tau_e_jet","All electron from tau with jet (Lxy)", 500, setup::lxy_min, setup::lxy_max);
      TH1D *h1_tau_e_reco = new TH1D("h1_tau_e_reco","Reco hadronic taus (from electron) (Lxy)", 500, setup::lxy_min, setup::lxy_max);
      // match of the electron (at least one match)
      TH1D *h1_ele_pfCand    = new TH1D("h1_ele_pfCand","pfCand ele matches electron (Lxy)", 500, setup::lxy_min, setup::lxy_max);
      TH1D *h1_ele_pfCand_pi = new TH1D("h1_ele_pfCand_pi","pfCand pi matches electron (Lxy)", 500, setup::lxy_min, setup::lxy_max);
      TH1D *h1_ele_pfCand_any = new TH1D("h1_ele_pfCand_any","pfCand (any) matches electron (Lxy)", 500, setup::lxy_min, setup::lxy_max);
      TH1D *h1_ele_lostTrack = new TH1D("h1_ele_lostTrack","lostTrack matches electron (Lxy)", 500, setup::lxy_min, setup::lxy_max);
      TH1D *h1_ele_isoTrack  = new TH1D("h1_ele_isoTrack","isoTrack matches electron (Lxy)", 500, setup::lxy_min, setup::lxy_max);

      // Muon from tau matching
      TH1D *h1_tau_mu_all  = new TH1D("h1_tau_mu_all","All muon from tau (Lxy)", 500, setup::lxy_min, setup::lxy_max);
      TH1D *h1_tau_mu_jet  = new TH1D("h1_tau_mu_jet","All muon from tau with jet (Lxy)", 500, setup::lxy_min, setup::lxy_max);
      TH1D *h1_tau_mu_reco = new TH1D("h1_tau_mu_reco","Reco hadronic taus (from muon) (Lxy)", 500, setup::lxy_min, setup::lxy_max);
      // match of the muon (at least one match)
      TH1D *h1_mu_pfCand    = new TH1D("h1_mu_pfCand","pfCand mu matches muon (Lxy)", 500, setup::lxy_min, setup::lxy_max);
      TH1D *h1_mu_pfCand_pi = new TH1D("h1_mu_pfCand_pi","pfCand pi matches muon (Lxy)", 500, setup::lxy_min, setup::lxy_max);
      TH1D *h1_mu_pfCand_any = new TH1D("h1_mu_pfCand_any","pfCand (any) matches muon (Lxy)", 500, setup::lxy_min, setup::lxy_max);
      TH1D *h1_mu_lostTrack = new TH1D("h1_mu_lostTrack","lostTrack matches muon (Lxy)", 500, setup::lxy_min, setup::lxy_max);
      TH1D *h1_mu_isoTrack  = new TH1D("h1_mu_isoTrack","isoTrack matches muon (Lxy)", 500, setup::lxy_min, setup::lxy_max);

      // Hadronuc tau matching
      TH1D *h1_tau_h_all  = new TH1D("h1_tau_h_all","All hadronic taus (Lxy)", 500, setup::lxy_min, setup::lxy_max);
      TH1D *h1_tau_h_jet  = new TH1D("h1_tau_h_jet","All hadronic taus with jet (Lxy)", 500, setup::lxy_min, setup::lxy_max);
      TH1D *h1_tau_h_reco = new TH1D("h1_tau_h_reco","Reco hadronic taus (Lxy)", 500, setup::lxy_min, setup::lxy_max);
      // match of the pion+- (at least one match)
      TH1D *h1_tau_h_pfCand_pi = new TH1D("h1_tau_h_pfCand_pi","pfCand pi matches pion (Lxy)", 500, setup::lxy_min, setup::lxy_max);
      TH1D *h1_tau_h_pfCand_any = new TH1D("h1_tau_h_pfCand_any","pfCand any matches pion (Lxy)", 500, setup::lxy_min, setup::lxy_max);
      TH1D *h1_tau_h_lostTrack = new TH1D("h1_tau_h_lostTrack","lostTrack matches pion (Lxy)", 500, setup::lxy_min, setup::lxy_max);
      TH1D *h1_tau_h_isoTrack  = new TH1D("h1_tau_h_isoTrack","isoTrack matches pion (Lxy)", 500, setup::lxy_min, setup::lxy_max);

      size_t bar_chunk = n_entries/100;
      for(size_t current_entry = 0; current_entry < n_entries; ++current_entry)
      {
        if(current_entry % bar_chunk == 0)
          std::cout << "Events processed: " << current_entry << " ("
                    << (int) ((double)current_entry/n_entries*100)
                    << "%)" << std::endl;

        tauTuple->GetEntry(current_entry);
        const auto& tau = tauTuple->data();

        if(tau.genLepton_vis_pt>=setup::genLepton_minPt && (tau.genLepton_kind==3 || tau.genLepton_kind==4 || tau.genLepton_kind==5))
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
          LorentzVectorXYZ gentau_vis = genLeptons.visibleP4();

          double disp{-999}, disp_z{-999};
          ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double>> stau_p4;
	
          for(auto genparticle_: all_gen_particles)
          {
            if(std::abs(genparticle_.pdgId) == 15 && genparticle_.isLastCopy){
              disp = genparticle_.vertex.rho();
              disp_z = genparticle_.vertex.z();
            }

            if(setup::requre_stau && std::abs(genparticle_.pdgId) == 1000015 && genparticle_.isLastCopy){
              stau_p4 = genparticle_.p4;
            }

          }

          if (TMath::Abs(disp_z) > setup::gen_vz_max)
            continue;
          
          if(disp == -999) {
            std::cout << "Warrning: no tau is found (will skip event)." << std::endl;
            continue;
          }

          if(setup::requre_stau && stau_p4.X() == 0.0) {
            std::cout << "Warrning: no susy-tau is found (will skip event)." << std::endl;
            continue;
          }

          if(tau.genLepton_kind==3) h1_tau_e_all->Fill(disp);  
          if(tau.genLepton_kind==4) h1_tau_mu_all->Fill(disp);
          if(tau.genLepton_kind==5) h1_tau_h_all->Fill(disp);  

          if(tau.jet_index<0) continue; // if there is no seeding jet

          // calculate dR between jet and genLepton
          ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double>> jet_p4
              (
                tau.jet_pt,
                tau.jet_eta,
                tau.jet_phi,
                tau.jet_mass       
              );
          if(ROOT::Math::VectorUtil::DeltaR(jet_p4, gentau_vis) > setup::genLepton_jet_dR ) continue; // if there is no seeding jet
          
          if(tau.genLepton_kind==3) h1_tau_e_jet->Fill(disp);  
          if(tau.genLepton_kind==4) h1_tau_mu_jet->Fill(disp);  
          if(tau.genLepton_kind==5) h1_tau_h_jet->Fill(disp);  

          // function to match vector to collection (collection name in prefix)
          auto matchToPfCand = [&](const std::string& prefix,
                                   const ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double>> matchedVec, 
                                   const std::set<int> pf_types) -> bool
          {
            for(int i=0; i < tauTuple->get<std::vector<float>>(prefix+"_pt").size(); i++)
            {
              float pt = tauTuple->get<std::vector<float>>(prefix+"_pt")[i];
              
              // if( pt < setup::pfCand_pt_min) continue; // skip low energetic pfCands
              if(!pf_types.empty()) {
                if(!pf_types.count(tauTuple->get<std::vector<Int_t>>(prefix+"_particleType")[i]))
                  continue;
              }

              float eta = tauTuple->get<std::vector<float>>(prefix+"_eta")[i];
              float phi = tauTuple->get<std::vector<float>>(prefix+"_phi")[i];

              // match vector to the object
              float dR_current = TMath::Sqrt( TMath::Power(eta-matchedVec.eta(),2) + TMath::Power(MyDeltaPhi<Float_t>(phi,matchedVec.phi()),2) );
              float pt_rel = std::abs( (pt-matchedVec.pt())/matchedVec.pt() );
              
              if( dR_current < setup::genParticle_pfCand_dR && pt_rel < setup::genParticle_pfCand_relPt ) return true; // if any pfcand satisfy
            }
            return false;
          };
          
          // function returns one of the found leptons in the order of the set
          auto getGenP4 = [&](const auto& GenPartCollection, const std::set<int> pdgIds) -> ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double>> 
          { 
            for(auto particle: GenPartCollection)
              if(pdgIds.count(TMath::Abs(particle->pdgId))) return particle->p4;

            std::stringstream ss;
            ss << "Error: pdgId ( ";
            for(auto pdgId: pdgIds) ss << pdgId << " ";
            ss << ") is not found in the collection: ";
            for(auto particle: GenPartCollection) ss << TMath::Abs(particle->pdgId) << " ";
            genLeptons.PrintDecay(std::cout);
            throw std::runtime_error(ss.str());
          };


          if(tau.genLepton_kind==3) // electronic tau
          {
            auto finalStateFromDecay = genLeptons.finalStateFromDecay();
            auto gen_part_p4 = getGenP4(finalStateFromDecay, {11});            
            if(matchToPfCand("lostTrack", gen_part_p4, {})) h1_ele_lostTrack->Fill(disp);
            if(matchToPfCand("pfCand", gen_part_p4, {1})) h1_ele_pfCand_pi->Fill(disp);
            if(matchToPfCand("pfCand", gen_part_p4, {2})) h1_ele_pfCand->Fill(disp);
            if(matchToPfCand("pfCand", gen_part_p4, {})) h1_ele_pfCand_any->Fill(disp);
            if(matchToPfCand("isoTrack", gen_part_p4, {})) h1_ele_isoTrack->Fill(disp);
          }
          if(tau.genLepton_kind==4) // muonic tau
          {
            auto finalStateFromDecay = genLeptons.finalStateFromDecay();
            auto gen_part_p4 = getGenP4(finalStateFromDecay, {13});
            if(matchToPfCand("lostTrack", gen_part_p4, {})) h1_mu_lostTrack->Fill(disp);
            if(matchToPfCand("pfCand", gen_part_p4, {2})) h1_mu_pfCand_pi->Fill(disp);
            if(matchToPfCand("pfCand", gen_part_p4, {3})) h1_mu_pfCand->Fill(disp);
            if(matchToPfCand("pfCand", gen_part_p4, {}))  h1_mu_pfCand_any->Fill(disp);
            if(matchToPfCand("isoTrack", gen_part_p4, {})) h1_mu_isoTrack->Fill(disp);
          }
          if(tau.genLepton_kind==5) // hadronic tau
          {
            auto finalStateFromDecay = genLeptons.finalStateFromDecay();
            auto gen_part_p4 = getGenP4(finalStateFromDecay, {211, 321});
            if(matchToPfCand("lostTrack", gen_part_p4, {})) h1_tau_h_lostTrack->Fill(disp);
            if(matchToPfCand("pfCand", gen_part_p4, {1})) h1_tau_h_pfCand_pi->Fill(disp);
            if(matchToPfCand("pfCand", gen_part_p4, {})) h1_tau_h_pfCand_any->Fill(disp);
            if(matchToPfCand("isoTrack", gen_part_p4, {})) h1_tau_h_isoTrack->Fill(disp);
          }

          // Match STau to pfCand
          if(setup::requre_stau)
          {
            if(matchToPfCand("lostTrack", stau_p4, {})) h1_stau_lostTrack->Fill(disp);
            if(matchToPfCand("pfCand", stau_p4, {})) h1_stau_pfCand->Fill(disp);
            if(matchToPfCand("isoTrack", stau_p4, {})) h1_stau_isoTrack->Fill(disp);
          }

          // Match Tau Lepton
          if(tau.tau_decayMode >= 0){
            ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double>> tau_p4
                (
                  tau.tau_pt,
                  tau.tau_eta,
                  tau.tau_phi,
                  tau.tau_mass       
                );
            if( ROOT::Math::VectorUtil::DeltaR(tau_p4, gentau_vis) > setup::genLepton_hpstau_dR ) continue; // if there is no mathced tau
            float pt_rel = std::abs( (tau.tau_pt-gentau_vis.pt())/gentau_vis.pt() );
            if(pt_rel > setup::genLepton_jet_relPt) continue;
          } else continue;
          
          if(tau.genLepton_kind==3) h1_tau_e_reco->Fill(disp);  
          if(tau.genLepton_kind==4) h1_tau_mu_reco->Fill(disp);  
          if(tau.genLepton_kind==5) h1_tau_h_reco->Fill(disp);  

        }
      }



      TFile *outputFile = new TFile(outputfile.c_str(),"RECREATE");

      h1_stau_pfCand->Write();
      h1_stau_lostTrack->Write();
      h1_stau_isoTrack->Write();
      h1_tau_e_all->Write();
      h1_tau_e_jet->Write();
      h1_tau_e_reco->Write();
      h1_ele_pfCand->Write();
      h1_ele_pfCand_pi->Write();
      h1_ele_lostTrack->Write();
      h1_ele_isoTrack->Write();
      h1_tau_mu_all->Write();
      h1_tau_mu_jet->Write();
      h1_tau_mu_reco->Write();
      h1_mu_pfCand->Write();
      h1_mu_pfCand_pi->Write();
      h1_mu_lostTrack->Write();
      h1_mu_isoTrack->Write();
      h1_tau_h_all->Write();
      h1_tau_h_jet->Write();
      h1_tau_h_reco->Write();
      h1_tau_h_pfCand_pi->Write();
      h1_tau_h_lostTrack->Write();
      h1_tau_h_isoTrack->Write();
      h1_ele_pfCand_any->Write();
      h1_mu_pfCand_any->Write();
      h1_tau_h_pfCand_any->Write();

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
