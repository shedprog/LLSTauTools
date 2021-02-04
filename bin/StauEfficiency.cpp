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

#include "TLorentzVector.h"
#include "TRandom.h"
#include "AC1B.h"
#include "FileTools.h"

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

  // Start of the analysis
  size_t goodTaus = 0;
  size_t hadronicTaus = 0;
  for (size_t iEntry=0; iEntry<numberOfEntries; iEntry++) {
    maintree->GetEntry(iEntry);
    if (iEntry%1000==0) std::cout << "processed " << iEntry << " events" << std::endl;

    size_t n_gentau = maintree->gentau_count;
    for (size_t gentau_i=0; gentau_i<n_gentau; gentau_i++) {

      // Chose only good gentaus
      if(maintree->gentau_fromHardProcess[gentau_i]!=1 || maintree->gentau_status[gentau_i]!=2)
        continue;
      goodTaus++;

      // If hadronic tau


    }

  }
  std::cout << "Good taus: " << goodTaus << std::endl;
  std::cout << "Good taus (expected): " << numberOfEntries*2 << std::endl;

  std::cout << "The StauEfficiency is executed!" << std::endl;
  return 0;
}
