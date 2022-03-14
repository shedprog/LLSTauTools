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
      double match_pt_rel = 0.1; // 20% by the relative pt (for pi0 and pi+-)
      double pfCand_MinPt = 1.0; // GeV consider only with bigger pt

      // // Lost Track to stau match
      // TH2D *h2_lostTrack_stau = new TH2D("h2_lostTrack_stau","lostTrack match to stau within dR",200,0,up_lim, 200, 0, 1.5);
      // TH2D *h2_lostTrack_pion = new TH2D("h2_lostTrack_pion","lostTrack match to pion within dR",200,0,up_lim, 200, 0, 1.5);
      // // pfCand
      // TH2D *h2_pfCand_stau = new TH2D("h2_pfCand_stau","pfCand match to stau within dR",200,0,up_lim, 200, 0, 1.5);
      // TH2D *h2_pfCand_pion = new TH2D("h2_pfCand_pion","pfCand match to pion within dR",200,0,up_lim, 200, 0, 1.5);
      // // isoTrack
      // TH2D *h2_isoTrack_stau = new TH2D("h2_isoTrack_stau","isoTrack match to stau within dR",200,0,up_lim, 200, 0, 1.5);
      // TH2D *h2_isoTrack_pion = new TH2D("h2_isoTrack_pion","isoTrack match to pion within dR",200,0,up_lim, 200, 0, 1.5);

      // // dR between the object and stau/pion
      // // Lost Track to stau match
      // TH2D *h2_dR_lostTrack_stau = new TH2D("h2_dR_lostTrack_stau","dR between lostTrack and stau within",200,0,up_lim, 200, 0, 1.5);
      // TH2D *h2_dR_lostTrack_pion = new TH2D("h2_dR_lostTrack_pion","dR between lostTrack and pion within",200,0,up_lim, 200, 0, 1.5);
      // // pfCand
      // TH2D *h2_dR_pfCand_stau = new TH2D("h2_dR_pfCand_stau","dR between pfCand and stau within",200,0,up_lim, 200, 0, 1.5);
      // TH2D *h2_dR_pfCand_pion = new TH2D("h2_dR_pfCand_pion","dR between pfCand and pion within",200,0,up_lim, 200, 0, 1.5);
      // // isoTrack
      // TH2D *h2_dR_isoTrack_stau = new TH2D("h2_dR_isoTrack_stau","dR between isoTrack and stau within",200,0,up_lim, 200, 0, 1.5);
      // TH2D *h2_dR_isoTrack_pion = new TH2D("h2_dR_isoTrack_pion","dR between isoTrack and pion within",200,0,up_lim, 200, 0, 1.5);

      // Numerical estimate of cand match
      TH1D *h1_Tau_h_all = new TH1D("h1_Tau_h_all","All hadronic taus delta_vtx",2000,0,up_lim);
      TH1D *h1_Tau_h_jet = new TH1D("h1_Tau_h_jet","All hadronic taus with jet delta_vtx",2000,0,up_lim);
      TH1D *h1_Tau_h_reco = new TH1D("h1_Tau_h_reco","Reco hadronic taus delta_vtx",2000,0,up_lim);
      // match of the stau (at least one match)
      TH1D *h1_stau_pfCand = new TH1D("h1_pfCand_stau","pfCand matches stau within dR",2000,0,up_lim);
      TH1D *h1_stau_lostTrack = new TH1D("h1_lostTrack_stau","lostTrack matches stau within dR",2000,0,up_lim);
      TH1D *h1_stau_isoTrack = new TH1D("h1_isoTrack_stau","pfCand matches stau within dR",2000,0,up_lim);
      // match of the pion (at least one match)
      TH1D *h1_pion_pfCand = new TH1D("h1_pfCand_pion","pfCand matches pion within dR",2000,0,up_lim);
      TH1D *h1_pion_lostTrack = new TH1D("h1_lostTrack_pion","lostTrack matches pion within dR",2000,0,up_lim);
      TH1D *h1_pion_isoTrack = new TH1D("h1_isoTrack_pion","pfCand matches pion within dR",2000,0,up_lim);
      // match of the pion0 (at least one match)
      TH1D *h1_pion0_pfCand = new TH1D("h1_pfCand_pion0","pfCand matches pion0 within dR",2000,0,up_lim);

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
          // ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double>> stau_p4;

          for(auto genparticle_: all_gen_particles)
          {
            if(std::abs(genparticle_.pdgId) == 15 && genparticle_.isLastCopy){
              disp = genparticle_.vertex.rho(); //disp = genparticle_.vertex.r();
            }

            // if(std::abs(genparticle_.pdgId) == 1000015 && genparticle_.isLastCopy) {
            //   stau_p4 = genparticle_.p4;
            // }
          }

          if(disp == -9) {
            std::cout << "No Tau is found!" << std::endl;
            continue;
          }

          // if(stau_p4.X() == 0.0) {
          //   std::cout << "No SusyTau is found!" << std::endl;
          //   continue;
          // }

          h1_Tau_h_all->Fill(disp);
          if(tau.tau_decayMode >= 0) h1_Tau_h_reco->Fill(disp);

          if(tau.jet_index<0) continue; // if there is no seeding jet
          h1_Tau_h_jet->Fill(disp);

          // double dR_gentau_stau = ROOT::Math::VectorUtil::DeltaR(gentau_vis, stau_p4);

          // Fitting and Filling matched lostTracks/pfCand/isoTrack
          // auto lazyGenMatch = [&](const std::string& prefix, TH2D* h_stua, TH2D* h_pion, bool threshold, bool staumatch) -> bool {

          //   bool gen_match = false;

          //   float best_dRstau = std::numeric_limits<float>::max();
          //   float best_dRpion = std::numeric_limits<float>::max();

          //   for(int i=0; i < tauTuple->get<std::vector<float>>(prefix+"_pt").size(); i++)
          //   {
          //     if(tauTuple->get<std::vector<float>>(prefix+"_pt")[i] < 3.0) continue;
          //     if(TMath::Abs(tauTuple->get<std::vector<int>>(prefix+"_charge")[i]) != 1) continue;

          //     float eta = tauTuple->get<std::vector<float>>(prefix+"_eta")[i];
          //     float phi = tauTuple->get<std::vector<float>>(prefix+"_phi")[i];

          //     float dRstau = TMath::Sqrt( TMath::Power(eta-stau_p4.eta(),2) + TMath::Power(phi-stau_p4.phi(),2) );
          //     best_dRstau = std::min(dRstau, best_dRstau);

          //     for(size_t gen_idx = 0; gen_idx < tau.genParticle_pdgId.size(); ++gen_idx)
          //     {
          //       if(TMath::Abs(tau.genParticle_pdgId[gen_idx]) != 211) continue;
          //       float eta_gen = tau.genParticle_eta[gen_idx];
          //       float phi_gen = tau.genParticle_phi[gen_idx];

          //       float dRpion = TMath::Sqrt( TMath::Power(eta-eta_gen,2) + TMath::Power(phi-phi_gen,2) );
          //       best_dRpion = std::min(dRpion, best_dRpion);
          //     }
          //   }

          //   if(best_dRpion < std::numeric_limits<float>::max()){
          //     if(!staumatch && best_dRpion < tight_dR) gen_match=true;
          //     if(threshold &&  best_dRpion < match_dR) h_pion->Fill(disp, dR_gentau_stau);
          //     else if(!threshold) h_pion->Fill(disp, best_dRpion);
          //   }

          //   if(best_dRstau < std::numeric_limits<float>::max()){
          //     if(staumatch && best_dRstau < tight_dR) gen_match=true;
          //     if(threshold && best_dRstau < match_dR) h_stua->Fill(disp, dR_gentau_stau);
          //     else if(!threshold) h_stua->Fill(disp, best_dRstau);
          //   }
            
          //   return gen_match;
          // };

          // auto lostTrack_match = lazyGenMatch("lostTrack", h2_lostTrack_stau, h2_lostTrack_pion, true, true);
          // auto pfCand_match = lazyGenMatch("pfCand", h2_pfCand_stau, h2_pfCand_pion, true, true);
          // auto isoTrack_match = lazyGenMatch("isoTrack", h2_isoTrack_stau, h2_isoTrack_pion, true, true);

          // if(lostTrack_match) h1_stau_lostTrack->Fill(disp);
          // if(pfCand_match) h1_stau_pfCand->Fill(disp);
          // if(isoTrack_match) h1_stau_isoTrack->Fill(disp);

          // lostTrack_match = lazyGenMatch("lostTrack", h2_dR_lostTrack_stau, h2_dR_lostTrack_pion, false, false);
          // pfCand_match = lazyGenMatch("pfCand", h2_dR_pfCand_stau, h2_dR_pfCand_pion, false, false);
          // isoTrack_match = lazyGenMatch("isoTrack", h2_dR_isoTrack_stau, h2_dR_isoTrack_pion, false, false);

          // if(lostTrack_match) h1_pion_lostTrack->Fill(disp);
          // if(pfCand_match) h1_pion_pfCand->Fill(disp);
          // if(isoTrack_match) h1_pion_isoTrack->Fill(disp);

          // Efficiency histograms only:
          auto MatchToPfCand = [&](const std::string& prefix,
                                   const ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double>> matchedVec, 
                                   const float dR,
                                   const bool fixType,
                                   const int pfType) -> bool
          {

            for(int i=0; i < tauTuple->get<std::vector<float>>(prefix+"_pt").size(); i++)
            {
              float pt = tauTuple->get<std::vector<float>>(prefix+"_pt")[i];
              if( pt < pfCand_MinPt) continue; // skip low energetic pfCands
              // if(TMath::Abs(tauTuple->get<std::vector<int>>(prefix+"_charge")[i]) != 1) continue; // skip neutral pfCands

              float eta = tauTuple->get<std::vector<float>>(prefix+"_eta")[i];
              float phi = tauTuple->get<std::vector<float>>(prefix+"_phi")[i];
              
              // match vector to the object
              float dR_current = TMath::Sqrt( TMath::Power(eta-matchedVec.eta(),2) + TMath::Power(phi-matchedVec.phi(),2) );
              float pt_rel = std::abs( (pt-matchedVec.pt())/matchedVec.pt() );

              if( dR_current < dR && pt_rel < pfCand_MinPt ) {
                if(fixType) {
                  if(tauTuple->get<std::vector<Int_t>>(prefix+"_particleType")[i] == pfType) 
                    return true;
                } else true;
              } 
            }

            return false;
          };
          
          // match stau to the object
          // if(MatchToPfCand("lostTrack", stau_p4, match_dR)) h1_stau_lostTrack->Fill(disp);
          // if(MatchToPfCand("pfCand", stau_p4, match_dR))    h1_stau_pfCand->Fill(disp);
          // if(MatchToPfCand("isoTrack", stau_p4, match_dR))  h1_stau_isoTrack->Fill(disp);

          // // match pion to the object
          bool lostTrack_match_pion = false;
          bool pfCand_match_pion = false;
          bool pfCand_match_pion0 = false;
          bool isoTrack_match_pion = false;

          for(size_t gen_idx = 0; gen_idx < tau.genParticle_pdgId.size(); ++gen_idx)
          {
            int pdgId = TMath::Abs(tau.genParticle_pdgId[gen_idx]);
            if( !( pdgId == 211 || pdgId == 111) || tau.genParticle_pt[gen_idx] < 1.0) continue;
            float eta_gen = tau.genParticle_eta[gen_idx];
            float phi_gen = tau.genParticle_phi[gen_idx];

            ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double>> pion_p4
              (
                tau.genParticle_pt[gen_idx], tau.genParticle_eta[gen_idx],
                tau.genParticle_phi[gen_idx], tau.genParticle_mass[gen_idx]       
              );

            if(pdgId == 211){
              if(MatchToPfCand("lostTrack", pion_p4, match_dR, true, 1)) lostTrack_match_pion = true;
              if(MatchToPfCand("pfCand", pion_p4, match_dR, true, 1)) pfCand_match_pion = true;
              if(MatchToPfCand("isoTrack", pion_p4, match_dR, false, 1)) isoTrack_match_pion = true;
            } else if(pdgId == 111) {
              if(MatchToPfCand("pfCand", pion_p4, match_dR, true, 5)) pfCand_match_pion0 = true;
            }
          }

          if(lostTrack_match_pion) h1_pion_lostTrack->Fill(disp);
          if(pfCand_match_pion) h1_pion_pfCand->Fill(disp);
          if(isoTrack_match_pion) h1_pion_isoTrack->Fill(disp);
          if(pfCand_match_pion0) h1_pion0_pfCand->Fill(disp);

        }
      }
      TFile *outputFile = new TFile(outputfile.c_str(),"RECREATE");
      // h2_lostTrack_stau->Write();
      // h2_lostTrack_pion->Write();
      // h2_pfCand_stau->Write();
      // h2_pfCand_pion->Write();
      // h2_isoTrack_stau->Write();
      // h2_isoTrack_pion->Write();
      // h2_dR_lostTrack_stau->Write();
      // h2_dR_lostTrack_pion->Write();
      // h2_dR_pfCand_stau->Write();
      // h2_dR_pfCand_pion->Write();
      // h2_dR_isoTrack_stau->Write();
      // h2_dR_isoTrack_pion->Write();
      
      h1_Tau_h_all->Write();
      h1_Tau_h_jet->Write();
      h1_Tau_h_reco->Write();

      h1_stau_pfCand->Write();
      h1_stau_lostTrack->Write();
      h1_stau_isoTrack->Write();

      h1_pion_pfCand->Write();
      h1_pion_lostTrack->Write();
      h1_pion_isoTrack->Write();

      h1_pion0_pfCand->Write();

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
