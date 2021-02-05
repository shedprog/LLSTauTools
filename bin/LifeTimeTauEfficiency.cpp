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

bool MatchGenToTau( const TLorentzVector& p4_1, const TLorentzVector& p4_2)
{
  float dr = 0.2;

  float dr_new = ROOT::Math::VectorUtil::DeltaR( p4_1, p4_2 );

  if(dr_new <= dr) return true;
  else return false;
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

  // Histograms to File
  TH1F *h1_Tau_h_all = new TH1F("h1_Tau_h_all","All hadronic taus lifetime",1000,0,100);
  TH1F *h1_Tau_h_reco = new TH1F("h1_Tau_h_reco","Reco hadronic taus lifetime",1000,0,100);
  TH1F *h1_Tau_h_ratio = new TH1F("h1_Tau_h_ratio","Reco/All hadronic taus lifetime",1000,0,100);

  // TH1F *h1_Tau_h_byLooseDeepTau_all = new TH1F("h1_Tau_h_byLooseDeepTau_all","All hadronic taus lifetime byLooseDeepTau",1000,0,100);
  TH1F *h1_Tau_h_byLooseDeepTau_reco = new TH1F("h1_Tau_h_byLooseDeepTau_reco","Reco hadronic taus lifetime byLooseDeepTau",1000,0,100);
  TH1F *h1_Tau_h_byLooseDeepTau_ratio = new TH1F("h1_Tau_h_byLooseDeepTau_ratio","Reco/All hadronic taus lifetime byLooseDeepTau",1000,0,100);

  // TH1F *h1_Tau_h_byMediumDeepTau_all = new TH1F("h1_Tau_h_byMediumDeepTau_all","All hadronic taus lifetime byMediumDeepTau",1000,0,100);
  TH1F *h1_Tau_h_byMediumDeepTau_reco = new TH1F("h1_Tau_h_byMediumDeepTau_reco","Reco hadronic taus lifetime byMediumDeepTau",1000,0,100);
  TH1F *h1_Tau_h_byMediumDeepTau_ratio = new TH1F("h1_Tau_h_byMediumDeepTau_ratio","Reco/All hadronic taus lifetime byMediumDeepTau",1000,0,100);

  // TH1F *h1_Tau_h_byTightDeepTau_all = new TH1F("h1_Tau_h_byTightDeepTau_all","All hadronic taus lifetime byTightDeepTau",1000,0,100);
  TH1F *h1_Tau_h_byTightDeepTau_reco = new TH1F("h1_Tau_h_byTightDeepTau_reco","Reco hadronic taus lifetime byTightDeepTau",1000,0,100);
  TH1F *h1_Tau_h_byTightDeepTau_ratio = new TH1F("h1_Tau_h_byTightDeepTau_ratio","Reco/All hadronic taus lifetime byTightDeepTau",1000,0,100);


  // Start of the analysis
  size_t goodTaus = 0;
  size_t hadronicTaus = 0;
  size_t hadronicTaus_reco = 0;
  for (size_t iEntry=0; iEntry<numberOfEntries; iEntry++) {
    maintree->GetEntry(iEntry);
    if (iEntry%1000==0) std::cout << "processed " << iEntry << " events" << std::endl;

    float stau_lifetime = maintree->SusyLifeTime;

    size_t n_gentau = maintree->gentau_count;
    for (size_t gentau_i=0; gentau_i<n_gentau; gentau_i++) {

      // Chose only good gentaus
      if(maintree->gentau_fromHardProcess[gentau_i]!=1
        || maintree->gentau_status[gentau_i]!=2) continue;
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
        // std::cout << "tau, match: " << maintree->tau_genmatch[tau_i] << " DM:" << maintree->tau_decayMode[tau_i] << std::endl;
        tau_p4.SetPxPyPzE(maintree->tau_px[tau_i],
                          maintree->tau_py[tau_i],
                          maintree->tau_pz[tau_i],
                          maintree->tau_e[tau_i]);
        bool isMatch = MatchGenToTau(gen_p4, tau_p4);
        if(isMatch) {
          hadronicTaus_reco++;

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

        }
      }
    }
  }

  h1_Tau_h_ratio->Divide(h1_Tau_h_all);
  h1_Tau_h_byLooseDeepTau_ratio->Divide(h1_Tau_h_all);
  h1_Tau_h_byMediumDeepTau_ratio->Divide(h1_Tau_h_all);
  h1_Tau_h_byTightDeepTau_ratio->Divide(h1_Tau_h_all);

  TFile *outputFile = new TFile("LifeTimeEfficiency.root","RECREATE");
  h1_Tau_h_all->Write();
  h1_Tau_h_reco->Write();
  h1_Tau_h_ratio->Write();
  // h1_Tau_h_byLooseDeepTau_all->Write();
  h1_Tau_h_byLooseDeepTau_reco->Write();
  h1_Tau_h_byLooseDeepTau_ratio->Write();
  // h1_Tau_h_byMediumDeepTau_all->Write();
  h1_Tau_h_byMediumDeepTau_reco->Write();
  h1_Tau_h_byMediumDeepTau_ratio->Write();
  // h1_Tau_h_byTightDeepTau_all->Write();
  h1_Tau_h_byTightDeepTau_reco->Write();
  h1_Tau_h_byTightDeepTau_ratio->Write();
  outputFile->Close();

  std::cout << "Good taus: " << goodTaus << std::endl;
  std::cout << "Good taus (expected): " << numberOfEntries*2 << std::endl;
  std::cout << "Hadronic Tau: " << hadronicTaus << std::endl;
  std::cout << "Reco Hadronic Tau: " << hadronicTaus_reco << std::endl;

  std::cout << "The StauEfficiency is executed!" << std::endl;
  return 0;
}
