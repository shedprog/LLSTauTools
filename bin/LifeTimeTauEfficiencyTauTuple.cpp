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

#include "FileTools.h"
#include "TauTuple.h"
#include "GenLepton.h"

using Tau = tau_tuple::Tau;
using TauTuple = tau_tuple::TauTuple;

constexpr int sourceParticlePdgId = 1000015; // susy particle
// constexpr int sourceParticlePdgId = 24;

const std::map<unsigned int, unsigned int> dm_encode = { // dm finder encode
    {0, 1},                 // oneProng 0Pi0
    {1, 2}, {2, 2}, {3, 2}, // oneProng Pi0s
    {10,3},                 // 3Prong 0Pi0
    {11,4}, {12,4},         // 3Prong Pi0s
    {5, 0}, {6, 0},         // 2Prong Decays (Other)
};

const int gen_dm_encode (unsigned int nCharged, unsigned int nNutral) // gen encode
{
  switch (nCharged) {
       case 1:
          if(nNutral==0) return 1;  // oneProng 0Pi0
          else return 2;            // oneProng Pi0s
          break;
       case 3:
          if(nNutral==0) return 3;    // 3Prong 0Pi0
          else return 4;              // 3Prong Pi0s
          break;
       case 2:
          return 0; // 2Prong Decays (Other)
          break;
       case 5:
          return 0; // rare 5 prongs (Other)
          break;
       case 4:
          return 0; // rare 5 prongs (Other)
          break;
  }
  std::cout << "nCharged: " << nCharged << " nNutral: " << nNutral << std::endl;
  throw std::runtime_error("Error! Decay mode does not exists!");
  return 0;
}

bool dR_calc( const TLorentzVector& p4_1, const TLorentzVector& p4_2)
{
  float dr = 0.2;

  float dr_new = ROOT::Math::VectorUtil::DeltaR( p4_1, p4_2 );

  if(dr_new <= dr) return true;
  else return false;
}

void info(const Tau& entry);

int main(int argc, char * argv[])
{
  using LorentzVectorXYZ = ROOT::Math::LorentzVector<ROOT::Math::PxPyPzE4D<double>>;

  std::string outfile_name = argv[1];
  size_t number_of_files = strtol(argv[2], NULL, 10);
  std::vector<std::string> dirs;
  for (size_t i = 3; i < argc; ++i) dirs.push_back(argv[i]);
  std::vector<std::string> root_files_all(FindInputFiles(dirs,"^.*\\.root$","",""));
  size_t number_to_read = 0;
  if(number_of_files>=0) number_to_read = std::min(number_of_files,root_files_all.size());
  else number_to_read = root_files_all.size();

  std::vector<std::string> root_files(root_files_all.end() - std::min(root_files_all.size(), number_to_read), root_files_all.end());

  for(auto file: root_files) std::cout << file << std::endl;

  std::cout << "Number of files to process: " << root_files.size() << std::endl;
  auto tauTuple = std::make_shared<TauTuple>("taus", root_files);
  std::cout << "Number of entries: " << tauTuple->GetEntries() << std::endl;
  size_t n_entries = tauTuple->GetEntries();

  double up_lim = 200; // units?

  // Count identification histogram
  TH2D *h1_Tau_h_all = new TH2D("h1_Tau_h_all","All hadronic taus delta_vtx",300,0,up_lim, 1000, 0, 1000);
  TH2D *h1_Tau_h_reco = new TH2D("h1_Tau_h_reco","Reco hadronic taus delta_vtx",300,0,up_lim, 1000, 0, 1000);
  TH2D *h1_Tau_h_all_t = new TH2D("h1_Tau_h_all_t","All hadronic taus delta_vtx_transverse",300,0,up_lim, 1000, 0, 1000);
  TH2D *h1_Tau_h_reco_t = new TH2D("h1_Tau_h_reco_t","Reco hadronic taus delta_vtx_transverse",300,0,up_lim, 1000, 0, 1000);

  TH2D *h1_Tau_genpt_all = new TH2D("h1_Tau_genpt_all","All hadronic taus delta_vtx",300,0,up_lim, 1000, 0, 1000);
  TH2D *h1_Tau_genpt_reco = new TH2D("h1_Tau_genpt_reco","Reco hadronic taus delta_vtx",300,0,up_lim, 1000, 0, 1000);
  TH2D *h1_Tau_genpt_all_t = new TH2D("h1_Tau_genpt_all_t","All hadronic taus delta_vtx_transverse",300,0,up_lim, 1000, 0, 1000);
  TH2D *h1_Tau_genpt_reco_t = new TH2D("h1_Tau_genpt_reco_t","Reco hadronic taus delta_vtx_transverse",300,0,up_lim, 1000, 0, 1000);

  TH3D *h3_dm_disp = new TH3D("h3_dm_disp", "Decay Modes vs. taus delta_vt", 6,-0.5,5.5, // dm gen
                                                                             6,-0.5,5.5, // dm reco
                                                                             300,0,up_lim); // life time
  TH2D *h2_pt_disp = new TH2D("h3_pt_disp", "1 - pt_reco/pt_gen vs. taus delta_vt", 100,-2.0,2.0, // 1 - pt_reco/pt_gen
                                                                                    300,0,up_lim); // life time

  TH3D *h3_dm_disp_t = new TH3D("h3_dm_disp_t", "Decay Modes vs. taus delta_vt_t", 6,-0.5,5.5, // dm gen
                                                                                   6,-0.5,5.5, // dm reco
                                                                                   300,0,up_lim); // life time
  TH2D *h2_pt_disp_t = new TH2D("h3_pt_disp_t", "1 - pt_reco/pt_gen vs. taus delta_vt_t", 100,-2.0,2.0, // 1 - pt_reco/pt_gen
                                                                                          300,0,up_lim); // life time

  TH2D *pixhits_reco_disp = new TH2D("pixhits_reco_disp", "N hits in PIX (for reco tau tracks) vs. displ.", 200,0,100, 50, 0, 50);
  TH2D *pixhits_reco_disp_t = new TH2D("pixhits_reco_disp_t", "N hits in PIX (for reco tau tracks) vs. tr displ.", 200,0,100, 50, 0, 50);

  for(size_t current_entry = 0; current_entry < n_entries; ++current_entry)
  {
    if(current_entry % 10000 == 0) std::cout << "Events processed: " << current_entry << " ("
                                             << (int) ((double)current_entry/n_entries*100)
                                             << "%)" << std::endl;

    tauTuple->GetEntry(current_entry);
    const auto& entry = tauTuple->data();

    // std::cout << std::endl;
    // std::cout << "event number :" << entry.evt << std::endl;
    //
    // size_t n_gen_particles = entry.genParticle_pdgId.size();
    // for(size_t gen_idx = 0; gen_idx < n_gen_particles; ++gen_idx)
    // {
    //
    //   std::cout  << "idx: " << gen_idx << " "
    //   << "pdgId: " << entry.genParticle_pdgId[gen_idx] << " "
    //   << "pt: " << entry.genParticle_pt[gen_idx] << " "
    //   << "eta: " << entry.genParticle_eta[gen_idx] << " "
    //   << "phi: " << entry.genParticle_phi[gen_idx] << " "
    //   << " vtx "
    //   << " " << entry.genParticle_vtx_x[gen_idx]
    //   << " " << entry.genParticle_vtx_y[gen_idx]
    //   << " " << entry.genParticle_vtx_z[gen_idx]
    //   << std::endl;
    // }

    if(entry.genLepton_kind==5 && entry.genLepton_vis_pt>=15.0) // to take only hadronic Taus
    {

      auto genLeptons = reco_tau::gen_truth::GenLepton::fromRootTuple(
                         entry.genLepton_lastMotherIndex,
                         entry.genParticle_pdgId,
                         entry.genParticle_mother,
                         entry.genParticle_charge,
                         entry.genParticle_isFirstCopy,
                         entry.genParticle_isLastCopy,
                         entry.genParticle_pt,
                         entry.genParticle_eta,
                         entry.genParticle_phi,
                         entry.genParticle_mass,
                         entry.genParticle_vtx_x,
                         entry.genParticle_vtx_y,
                         entry.genParticle_vtx_z);

      const std::vector<reco_tau::gen_truth::GenParticle>& all_gen_particles = genLeptons.allParticles();
      int genTauDecayMode = gen_dm_encode(genLeptons.nChargedHadrons(), genLeptons.nNeutralHadrons());

      double disp{-9}, disp_t{-9};
      double gentau_pt = genLeptons.visibleP4().Pt();

      for(auto genparticle_: all_gen_particles)
      {
          if(std::abs(genparticle_.pdgId) == 15 && genparticle_.isLastCopy)
          {
              disp = genparticle_.vertex.r();
              disp_t = genparticle_.vertex.rho();
          }
      }
      assert(disp != -9);
      assert(disp_t != -9);

      // if(disp >= 500 && entry.tau_decayMode==0 && genTauDecayMode==1){
        // std::cout << std::endl;
        // std::cout << "event number :" << entry.evt << " Lumi: " << entry.lumi << std::endl;
        // genLeptons.PrintDecay(std::cout);
        // info(entry);
      // }

      h1_Tau_h_all->Fill(disp,entry.susy_ctau);
      h1_Tau_h_all_t->Fill(disp_t,entry.susy_ctau);
      h1_Tau_genpt_all->Fill(disp,gentau_pt);
      h1_Tau_genpt_all_t->Fill(disp_t,gentau_pt);

      TLorentzVector tau_p4;
      tau_p4.SetPtEtaPhiM(entry.tau_pt, entry.tau_eta, entry.tau_phi, entry.tau_mass);
      auto gen_p4 = genLeptons.visibleP4();
      double dR = ROOT::Math::VectorUtil::DeltaR(tau_p4,gen_p4);

      // if(entry.genLepton_index < 0 && entry.genJet_index >= 0) continue;
      if(entry.tau_decayMode >= 0 && entry.tau_decayModeFindingNewDMs == 1 && dR<=0.2) // if recontructed
      {

        Int_t nHits = 0;
        for(int track_i=0; track_i <= entry.pfCand_track_pt.size(); track_i++ ) {
          if(entry.pfCand_tauSignal[track_i]!=1) continue;
          nHits += entry.pfCand_nPixelHits[track_i];
        }
        if(entry.pfCand_track_pt.size()!=0){
          pixhits_reco_disp->Fill(disp,nHits);
          pixhits_reco_disp_t->Fill(disp_t,nHits);
        }


        h1_Tau_h_reco->Fill(disp,entry.susy_ctau);
        h1_Tau_h_reco_t->Fill(disp_t,entry.susy_ctau);
        h1_Tau_genpt_reco->Fill(disp,gentau_pt);
        h1_Tau_genpt_reco_t->Fill(disp_t,gentau_pt);
        h3_dm_disp->Fill(genTauDecayMode, dm_encode.at(entry.tau_decayMode), disp);
        h3_dm_disp_t->Fill(genTauDecayMode, dm_encode.at(entry.tau_decayMode), disp_t);
        h2_pt_disp->Fill(1.0 - entry.tau_pt/gentau_pt, disp);
        h2_pt_disp_t->Fill(1.0 - entry.tau_pt/gentau_pt, disp_t);
      }
    }
  }

  TFile *outputFile = new TFile(outfile_name.c_str(),"RECREATE");
  h1_Tau_h_all->Write();
  h1_Tau_h_reco->Write();
  h1_Tau_h_all_t->Write();
  h1_Tau_h_reco_t->Write();
  h1_Tau_genpt_all->Write();
  h1_Tau_genpt_reco->Write();
  h1_Tau_genpt_all_t->Write();
  h1_Tau_genpt_reco_t->Write();
  h3_dm_disp->Write();
  h2_pt_disp->Write();
  h3_dm_disp_t->Write();
  h2_pt_disp_t->Write();
  pixhits_reco_disp->Write();
  pixhits_reco_disp_t->Write();
  outputFile->Close();

  std::cout << "The StauEfficiency for TauTuple is executed!" << std::endl;
  return 0;
}

void info(const Tau& entry) {

  std::cout << "\nReco Tau:\n"
            << "pt: " << entry.tau_pt << " eta: " << entry.tau_eta << " phi: " << entry.tau_phi
            << " DM:" << entry.tau_decayMode
            << " vtx: " << entry.tau_sv_x << " " << entry.tau_sv_y << " " <<  entry.tau_sv_z
            << std::endl << std::endl;

  std::cout << "Lost Track:\n";

  for(int track_i=0; track_i <= entry.lostTrack_track_pt.size(); track_i++ ) {
  if(entry.lostTrack_tauSignal[track_i]!=1) continue;
  std::cout
            << "pt: " << entry.lostTrack_track_pt[track_i] << " eta: " << entry.lostTrack_track_eta[track_i] << " phi: " << entry.lostTrack_track_phi[track_i]
            << " charge: " << entry.lostTrack_charge[track_i]
            << " vtx: " << entry.lostTrack_vertex_x[track_i] << " " << entry.lostTrack_vertex_y[track_i] << " " << entry.lostTrack_vertex_z[track_i] << " " << entry.lostTrack_vertex_t[track_i] << " "
            << " nHits: " << entry.lostTrack_nHits[track_i]
            << " nPixelLayers: " << entry.lostTrack_nPixelLayers[track_i]
            << " nStripLayers: " << entry.lostTrack_nStripLayers[track_i]
            << " Tau Signal: " << entry.lostTrack_tauSignal[track_i]
            << std::endl;
  }

  std::cout << "PfCand Track:\n";

  for(int track_i=0; track_i <= entry.pfCand_track_pt.size(); track_i++ ) {
  if(entry.pfCand_tauSignal[track_i]!=1) continue;
  std::cout
            << "pt: " << entry.pfCand_track_pt[track_i] << " eta: " << entry.pfCand_track_eta[track_i] << " phi: " << entry.pfCand_track_phi[track_i]
            << " charge: " << entry.pfCand_charge[track_i]
            << " vtx: " << entry.pfCand_vertex_x[track_i] << " " << entry.pfCand_vertex_y[track_i] << " " << entry.pfCand_vertex_z[track_i] << " " << entry.pfCand_vertex_t[track_i] << " "
            << " nHits: " << entry.pfCand_nHits[track_i]
            << " nPixelLayers: " << entry.pfCand_nPixelLayers[track_i]
            << " nStripLayers: " << entry.pfCand_nStripLayers[track_i]
            << " Tau Signal: " << entry.lostTrack_tauSignal[track_i]
            << std::endl;
  }
  std::cout << "Iso Track:\n";

  for(int track_i=0; track_i <= entry.isoTrack_index.size(); track_i++ ) {
  // if(entry.isoTrack_tauSignal[track_i]!=1) continue;
  std::cout
            << "pt: " << entry.isoTrack_pt[track_i] << " eta: " << entry.isoTrack_eta[track_i] << " phi: " << entry.isoTrack_phi[track_i]
            << " charge: " << entry.isoTrack_charge[track_i] << " n_ValidHits: " << entry.isoTrack_n_ValidHits[track_i]
            << " n_ValidMuonHits: " << entry.isoTrack_n_ValidMuonHits[track_i]
            << " n_ValidPixelHits: " << entry.isoTrack_n_ValidPixelHits[track_i]
            << " n_ValidStripHits: " << entry.isoTrack_n_ValidStripHits[track_i]
            << std::endl;
  }


    std::cout << "--------------------------------------\n";
    std::cin.ignore();
}
