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

#include "AC1B.h"
#include "FileTools.h"

// enum class genTauDecayMode {
//   oneProng0Pi0 = 0,
//   oneProng1Pi0 = 1,
//   oneProng2Pi0 = 2,
//   oneProngOther = 3,
//   threeProng0Pi0 = 4,
//   threeProng1Pi0 = 5,
//   threeProngOther = 6,
//   rare = 7
// }

bool matchGenToTau( const TLorentzVector& p4_1, const TLorentzVector& p4_2)
{
  float dr = 0.2;

  float dr_new = ROOT::Math::VectorUtil::DeltaR( p4_1, p4_2 );

  if(dr_new <= dr) return true;
  else return false;
}

void printGenTaus(const AC1B* maintree, const size_t& gentau_i)
{
  if(gentau_i==0)
    std::cout << "----------------------------------------" << std::endl;
  std::cout << "tau_i:" << gentau_i << " | "
            << maintree->gentau_fromHardProcess[gentau_i] << " "
            << maintree->gentau_fromHardProcessBeforeFSR[gentau_i] << " "
            << maintree->gentau_isDecayedLeptonHadron[gentau_i] << " "
            << maintree->gentau_isDirectHadronDecayProduct[gentau_i] << " "
            << maintree->gentau_isDirectHardProcessTauDecayProduct[gentau_i] << " "
            << maintree->gentau_isDirectPromptTauDecayProduct[gentau_i] << " "
            << maintree->gentau_isDirectTauDecayProduct[gentau_i] << " "
            << maintree->gentau_isFirstCopy[gentau_i] << " "
            << maintree->gentau_isHardProcess[gentau_i] << " "
            << maintree->gentau_isHardProcessTauDecayProduct[gentau_i] << " "
            << maintree->gentau_isLastCopy[gentau_i] << " "
            << maintree->gentau_isLastCopyBeforeFSR[gentau_i] << " "
            << maintree->gentau_isPrompt[gentau_i] << " "
            << maintree->gentau_isPromptTauDecayProduct[gentau_i] << " "
            << maintree->gentau_isTauDecayProduct[gentau_i] << " "
            << maintree->gentau_status[gentau_i] << " ";
  std::cout << " ";
  std::cin.ignore();
}

int main(int argc, char * argv[])
{
  std::cout << "StauEfficiency is started" << std::endl;

  std::string ntupleName("makeroottree/AC1B");

  // Reading input parms.
  size_t number_of_files = strtol(argv[1], NULL, 10);
  std::vector<std::string> dirs;
  for (size_t i = 2; i < argc; ++i) dirs.push_back(argv[i]);
  std::vector<std::string> root_files_all(FindInputFiles(dirs,"^.*\\.root$","",""));

  size_t number_to_read = 0;
  if(number_of_files>=0) number_to_read = std::min(number_of_files,root_files_all.size());
  else number_to_read = root_files_all.size();

  TChain *AllFilesTChain = new TChain(TString(ntupleName));
  std::cout << "Root files to be analyzed: " << number_to_read << std::endl;
  for (size_t i = 0; i < number_to_read; ++i) {
    std::cout << root_files_all[i] << std::endl;
    AllFilesTChain->Add(root_files_all[i].c_str());
  }

  // Open TTree from TChain
  AC1B *maintree = new AC1B(AllFilesTChain);
  if(maintree==NULL)
    throw std::runtime_error("AC1B can not be obtained from TChain");
  size_t numberOfEntries = maintree->GetEntries();
  std::cout << "Number of entries in Tree = " << numberOfEntries << std::endl;

  // Count identification histogram
  TH1F *h1_Tau_h_all = new TH1F("h1_Tau_h_all","All hadronic taus lifetime",1000,0,100);
  TH1F *h1_Tau_h_reco = new TH1F("h1_Tau_h_reco","Reco hadronic taus lifetime",1000,0,100);
  TH1F *h1_Tau_h_ratio = new TH1F("h1_Tau_h_ratio","Reco/All hadronic taus lifetime",1000,0,100);
  TH1F *h1_Tau_h_byLooseDeepTau_reco = new TH1F("h1_Tau_h_byLooseDeepTau_reco","Reco hadronic taus lifetime byLooseDeepTau",1000,0,100);
  TH1F *h1_Tau_h_byLooseDeepTau_ratio = new TH1F("h1_Tau_h_byLooseDeepTau_ratio","Reco/All hadronic taus lifetime byLooseDeepTau",1000,0,100);
  TH1F *h1_Tau_h_byMediumDeepTau_reco = new TH1F("h1_Tau_h_byMediumDeepTau_reco","Reco hadronic taus lifetime byMediumDeepTau",1000,0,100);
  TH1F *h1_Tau_h_byMediumDeepTau_ratio = new TH1F("h1_Tau_h_byMediumDeepTau_ratio","Reco/All hadronic taus lifetime byMediumDeepTau",1000,0,100);
  TH1F *h1_Tau_h_byTightDeepTau_reco = new TH1F("h1_Tau_h_byTightDeepTau_reco","Reco hadronic taus lifetime byTightDeepTau",1000,0,100);
  TH1F *h1_Tau_h_byTightDeepTau_ratio = new TH1F("h1_Tau_h_byTightDeepTau_ratio","Reco/All hadronic taus lifetime byTightDeepTau",1000,0,100);

  // Reconstructed vars
  // pt
  TH1F *h1_dpt_0p01and0p05 = new TH1F("h1_dpt_0p01and0p05","delta pt 0.01mm-0.05mm",1000,-1000,1000);
  TH1F *h1_dpt_0p1and0p5 = new TH1F("h1_dpt_0p1and0p5","delta pt 0.1mm-0.5mm",1000,-1000,1000);
  TH1F *h1_dpt_1p0 = new TH1F("h1_dpt_1p0","delta pt 1.0mm",1000,-1000,1000);
  TH1F *h1_dpt_2p5 = new TH1F("h1_dpt_2p5","delta pt 2.5mm",1000,-1000,1000);
  TH1F *h1_dpt_5p0 = new TH1F("h1_dpt_5p0","delta pt 5.0mm",1000,-1000,1000);
  TH1F *h1_dpt_7p5 = new TH1F("h1_dpt_7p5","delta pt 7.5mm",1000,-1000,1000);
  TH1F *h1_dpt_10p0 = new TH1F("h1_dpt_10p0","delta pt 10.0mm",1000,-1000,1000);
  // eta
  TH1F *h1_deta_0p01and0p05 = new TH1F("h1_eta_0p01and0p05","delta eta 0.01mm-0.05mm",1000,-0.2,0.2);
  TH1F *h1_deta_0p1and0p5 = new TH1F("h1_eta_0p1and0p5","delta eta 0.1mm-0.5mm",1000,-0.2,0.2);
  TH1F *h1_deta_1p0 = new TH1F("h1_eta_1p0","delta eta 1.0mm",1000,-0.2,0.2);
  TH1F *h1_deta_2p5 = new TH1F("h1_eta_2p5","delta eta 2.5mm",1000,-0.2,0.2);
  TH1F *h1_deta_5p0 = new TH1F("h1_eta_5p0","delta eta 5.0mm",1000,-0.2,0.2);
  TH1F *h1_deta_7p5 = new TH1F("h1_eta_7p5","delta eta 7.5mm",1000,-0.2,0.2);
  TH1F *h1_deta_10p0 = new TH1F("h1_eta_10p0","delta eta 10.0mm",1000,-0.2,0.2);
  // phi
  TH1F *h1_dphi_0p01and0p05 = new TH1F("h1_dphi_0p01and0p05","delta phi 0.01mm-0.05mm",1000,-0.2,0.2);
  TH1F *h1_dphi_0p1and0p5 = new TH1F("h1_dphi_0p1and0p5","delta phi 0.1mm-0.5mm",1000,-0.2,0.2);
  TH1F *h1_dphi_1p0 = new TH1F("h1_dphi_1p0","delta phi 1.0mm",1000,-0.2,0.2);
  TH1F *h1_dphi_2p5 = new TH1F("h1_dphi_2p5","delta phi 2.5mm",1000,-0.2,0.2);
  TH1F *h1_dphi_5p0 = new TH1F("h1_dphi_5p0","delta phi 5.0mm",1000,-0.2,0.2);
  TH1F *h1_dphi_7p5 = new TH1F("h1_dphi_7p5","delta phi 7.5mm",1000,-0.2,0.2);
  TH1F *h1_dphi_10p0 = new TH1F("h1_dphi_10p0","delta phi 10.0mm",1000,-0.2,0.2);
  // mass
  TH1F *h1_dm_0p01and0p05 = new TH1F("h1_dm_0p01and0p05","delta mass 0.01mm-0.05mm",1000,-20,20);
  TH1F *h1_dm_0p1and0p5 = new TH1F("h1_dm_0p1and0p5","delta mass 0.1mm-0.5mm",1000,-20,20);
  TH1F *h1_dm_1p0 = new TH1F("h1_dm_1p0","delta mass 1.0mm",1000,-20,20);
  TH1F *h1_dm_2p5 = new TH1F("h1_dm_2p5","delta mass 2.5mm",1000,-20,20);
  TH1F *h1_dm_5p0 = new TH1F("h1_dm_5p0","delta mass 5.0mm",1000,-20,20);
  TH1F *h1_dm_7p5 = new TH1F("h1_dm_7p5","delta mass 7.5mm",1000,-20,20);
  TH1F *h1_dm_10p0 = new TH1F("h1_dm_10p0","delta mass 10.0mm",1000,-20,20);

  TH2F *DMm_0p01and0p05 = new TH2F("DMm_0p01and0p05", "Decay Mode Migration 0p01and0p05", 9, 0, 9, 8, 0, 8);
  TH2F *DMm_0p1and0p5 = new TH2F("DMm_0p1and0p5", "Decay Mode Migration 0p1and0p5", 9, 0, 9, 8, 0, 8);
  TH2F *DMm_1p0 = new TH2F("DMm_1p0", "Decay Mode Migration 1p0", 9, 0, 9, 8, 0, 8);
  TH2F *DMm_2p5 = new TH2F("DMm_2p5", "Decay Mode Migration 2p5", 9, 0, 9, 8, 0, 8);
  TH2F *DMm_5p0 = new TH2F("DMm_5p0", "Decay Mode Migration 5p0", 9, 0, 9, 8, 0, 8);
  TH2F *DMm_7p5 = new TH2F("DMm_7p5", "Decay Mode Migration 7p5", 9, 0, 9, 8, 0, 8);
  TH2F *DMm_10p0 = new TH2F("DMm_10p0", "Decay Mode Migration 10p0", 9, 0, 9, 8, 0, 8);

  // Start of the analysis
  size_t goodTaus = 0;
  size_t hadronicTaus = 0;
  size_t hadronicTaus_reco = 0;
  for (size_t iEntry=0; iEntry<numberOfEntries; iEntry++) {
    maintree->GetEntry(iEntry);
    if (iEntry%1000==0) std::cout << "processed " << iEntry << " events" << std::endl;

    float stau_lifetime = maintree->SusyLifeTime;
    // std::cout << std::setprecision (15) << stau_lifetime << std::endl;

    size_t n_gentau = maintree->gentau_count;
    for (size_t gentau_i=0; gentau_i<n_gentau; gentau_i++) {
      // printGenTaus(maintree, gentau_i);

      // Chose only good gentaus
      if(maintree->gentau_fromHardProcess[gentau_i]!=1
        || maintree->gentau_status[gentau_i]!=2
        ) continue;
      goodTaus++;

      // If hadronic tau
      if(maintree->gentau_decayMode[gentau_i] >= 8) continue;
      hadronicTaus++;

      h1_Tau_h_all->Fill(stau_lifetime);

      TLorentzVector gen_p4, tau_p4;
      gen_p4.SetPxPyPzE(maintree->gentau_px[gentau_i],
                        maintree->gentau_py[gentau_i],
                        maintree->gentau_pz[gentau_i],
                        maintree->gentau_e[gentau_i]);

      size_t n_tau = maintree->tau_count;
      for (size_t tau_i=0; tau_i<n_tau; tau_i++) {

        tau_p4.SetPxPyPzE(maintree->tau_px[tau_i],
                          maintree->tau_py[tau_i],
                          maintree->tau_pz[tau_i],
                          maintree->tau_e[tau_i]);
        bool isMatch = matchGenToTau(gen_p4, tau_p4);

        if(isMatch) {
          hadronicTaus_reco++;

          if(stau_lifetime>=0.01 && stau_lifetime<=0.0501) {
            h1_dpt_0p01and0p05->Fill(gen_p4.Pt()-tau_p4.Pt());
            h1_deta_0p01and0p05->Fill(gen_p4.Eta()-tau_p4.Eta());
            h1_dphi_0p01and0p05->Fill(gen_p4.Phi()-tau_p4.Phi());
            h1_dm_0p01and0p05->Fill(gen_p4.M()-tau_p4.M());
            DMm_0p01and0p05->Fill(maintree->tau_decayMode[tau_i], maintree->gentau_decayMode[gentau_i]);
          } else if(stau_lifetime>=0.1 && stau_lifetime<=0.501){
            h1_dpt_0p1and0p5->Fill(gen_p4.Pt()-tau_p4.Pt());
            h1_deta_0p1and0p5->Fill(gen_p4.Eta()-tau_p4.Eta());
            h1_dphi_0p1and0p5->Fill(gen_p4.Phi()-tau_p4.Phi());
            h1_dm_0p1and0p5->Fill(gen_p4.M()-tau_p4.M());
            DMm_0p1and0p5->Fill(maintree->tau_decayMode[tau_i], maintree->gentau_decayMode[gentau_i]);
          } else if(stau_lifetime==1.0){
            h1_dpt_1p0->Fill(gen_p4.Pt()-tau_p4.Pt());
            h1_deta_1p0->Fill(gen_p4.Eta()-tau_p4.Eta());
            h1_dphi_1p0->Fill(gen_p4.Phi()-tau_p4.Phi());
            h1_dm_1p0->Fill(gen_p4.M()-tau_p4.M());
            DMm_1p0->Fill(maintree->tau_decayMode[tau_i], maintree->gentau_decayMode[gentau_i]);
          } else if(stau_lifetime==2.5){
            h1_dpt_2p5->Fill(gen_p4.Pt()-tau_p4.Pt());
            h1_deta_2p5->Fill(gen_p4.Eta()-tau_p4.Eta());
            h1_dphi_2p5->Fill(gen_p4.Phi()-tau_p4.Phi());
            h1_dm_2p5->Fill(gen_p4.M()-tau_p4.M());
            DMm_2p5->Fill(maintree->tau_decayMode[tau_i], maintree->gentau_decayMode[gentau_i]);
          } else if(stau_lifetime==5.0){
            h1_dpt_5p0->Fill(gen_p4.Pt()-tau_p4.Pt());
            h1_deta_5p0->Fill(gen_p4.Eta()-tau_p4.Eta());
            h1_dphi_5p0->Fill(gen_p4.Phi()-tau_p4.Phi());
            h1_dm_5p0->Fill(gen_p4.M()-tau_p4.M());
            DMm_5p0->Fill(maintree->tau_decayMode[tau_i], maintree->gentau_decayMode[gentau_i]);
          } else if(stau_lifetime==7.5){
            h1_dpt_7p5->Fill(gen_p4.Pt()-tau_p4.Pt());
            h1_deta_7p5->Fill(gen_p4.Eta()-tau_p4.Eta());
            h1_dphi_7p5->Fill(gen_p4.Phi()-tau_p4.Phi());
            h1_dm_7p5->Fill(gen_p4.M()-tau_p4.M());
            DMm_7p5->Fill(maintree->tau_decayMode[tau_i], maintree->gentau_decayMode[gentau_i]);
          } else if(stau_lifetime==10.0){
            h1_dpt_10p0->Fill(gen_p4.Pt()-tau_p4.Pt());
            h1_deta_10p0->Fill(gen_p4.Eta()-tau_p4.Eta());
            h1_dphi_10p0->Fill(gen_p4.Phi()-tau_p4.Phi());
            h1_dm_10p0->Fill(gen_p4.M()-tau_p4.M());
            DMm_10p0->Fill(maintree->tau_decayMode[tau_i], maintree->gentau_decayMode[gentau_i]);
          }

          h1_Tau_h_reco->Fill(stau_lifetime);
          h1_Tau_h_ratio->Fill(stau_lifetime);

          if(maintree->tau_byLooseDeepTau2017v2p1VSe[tau_i] ==1 &&
             maintree->tau_byLooseDeepTau2017v2p1VSjet[tau_i] ==1 &&
             maintree->tau_byLooseDeepTau2017v2p1VSmu[tau_i] ==1)
             {
                h1_Tau_h_byLooseDeepTau_reco->Fill(stau_lifetime);
                h1_Tau_h_byLooseDeepTau_ratio->Fill(stau_lifetime);
             }

          if(maintree->tau_byMediumDeepTau2017v2p1VSe[tau_i] ==1 &&
              maintree->tau_byMediumDeepTau2017v2p1VSjet[tau_i] ==1 &&
              maintree->tau_byMediumDeepTau2017v2p1VSmu[tau_i] ==1)
              {
                h1_Tau_h_byMediumDeepTau_reco->Fill(stau_lifetime);
                h1_Tau_h_byMediumDeepTau_ratio->Fill(stau_lifetime);
              }

          if(maintree->tau_byTightDeepTau2017v2p1VSe[tau_i] ==1 &&
             maintree->tau_byTightDeepTau2017v2p1VSjet[tau_i] ==1 &&
             maintree->tau_byTightDeepTau2017v2p1VSmu[tau_i] ==1)
             {
               h1_Tau_h_byTightDeepTau_reco->Fill(stau_lifetime);
               h1_Tau_h_byTightDeepTau_ratio->Fill(stau_lifetime);
             }

        } else {
          // if gentau does not not match
          if(stau_lifetime>=0.01 && stau_lifetime<=0.0501)
              DMm_0p01and0p05->Fill(8, maintree->gentau_decayMode[gentau_i]);
          else if(stau_lifetime>=0.1 && stau_lifetime<=0.501)
              DMm_0p1and0p5->Fill(8, maintree->gentau_decayMode[gentau_i]);
          else if(stau_lifetime==1.0)
              DMm_1p0->Fill(8, maintree->gentau_decayMode[gentau_i]);
          else if(stau_lifetime==2.5)
              DMm_2p5->Fill(8, maintree->gentau_decayMode[gentau_i]);
          else if(stau_lifetime==5.0)
              DMm_5p0->Fill(8, maintree->gentau_decayMode[gentau_i]);
          else if(stau_lifetime==7.5)
              DMm_7p5->Fill(8, maintree->gentau_decayMode[gentau_i]);
          else if(stau_lifetime==10.0)
              DMm_10p0->Fill(8, maintree->gentau_decayMode[gentau_i]);
        }
      }
    }
  }

  h1_Tau_h_ratio->Divide(h1_Tau_h_all);
  h1_Tau_h_byLooseDeepTau_ratio->Divide(h1_Tau_h_all);
  h1_Tau_h_byMediumDeepTau_ratio->Divide(h1_Tau_h_all);
  h1_Tau_h_byTightDeepTau_ratio->Divide(h1_Tau_h_all);

  // Create histograms

  TFile *outputFile = new TFile("LifeTimeEfficiency.root","RECREATE");
  h1_Tau_h_all->Write();
  h1_Tau_h_reco->Write();
  h1_Tau_h_ratio->Write();
  h1_Tau_h_byLooseDeepTau_reco->Write();
  h1_Tau_h_byLooseDeepTau_ratio->Write();
  h1_Tau_h_byMediumDeepTau_reco->Write();
  h1_Tau_h_byMediumDeepTau_ratio->Write();
  h1_Tau_h_byTightDeepTau_reco->Write();
  h1_Tau_h_byTightDeepTau_ratio->Write();
  h1_dpt_0p01and0p05->Write();
  h1_dpt_0p1and0p5->Write();
  h1_dpt_1p0->Write();
  h1_dpt_2p5->Write();
  h1_dpt_5p0->Write();
  h1_dpt_7p5->Write();
  h1_dpt_10p0->Write();
  h1_deta_0p01and0p05->Write();
  h1_deta_0p1and0p5->Write();
  h1_deta_1p0->Write();
  h1_deta_2p5->Write();
  h1_deta_5p0->Write();
  h1_deta_7p5->Write();
  h1_deta_10p0->Write();
  h1_dphi_0p01and0p05->Write();
  h1_dphi_0p1and0p5->Write();
  h1_dphi_1p0->Write();
  h1_dphi_2p5->Write();
  h1_dphi_5p0->Write();
  h1_dphi_7p5->Write();
  h1_dphi_10p0->Write();
  h1_dm_0p01and0p05->Write();
  h1_dm_0p1and0p5->Write();
  h1_dm_1p0->Write();
  h1_dm_2p5->Write();
  h1_dm_5p0->Write();
  h1_dm_7p5->Write();
  h1_dm_10p0->Write();
  DMm_0p01and0p05->Write();
  DMm_0p1and0p5->Write();
  DMm_1p0->Write();
  DMm_2p5->Write();
  DMm_5p0->Write();
  DMm_7p5->Write();
  DMm_10p0->Write();
  outputFile->Close();

  std::cout << "Good taus: " << goodTaus << std::endl;
  std::cout << "Good taus (expected): " << numberOfEntries*2 << std::endl;
  std::cout << "Hadronic Tau: " << hadronicTaus << std::endl;
  std::cout << "Reco Hadronic Tau: " << hadronicTaus_reco << std::endl;

  std::cout << "The StauEfficiency is executed!" << std::endl;
  return 0;
}
