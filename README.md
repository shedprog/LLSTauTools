# LLSTauTools

Compile the modules:
```sh
source /cvmfs/sft.cern.ch/lcg/views/setupViews.sh LCG_99 x86_64-centos7-gcc10-opt
mkdir build
cd build
cmake3 ..
make
```

Tau reconstruction efficency for different disp. (to be run above TauML TauTuples):
```
./TauTuple_LifeTimeTauEfficiency -1 /pnfs/desy.de/cms/tier2/store/user/myshched/Signal2018ctau/SUS-RunIIFall18GS_ctau0p01-1000mm_mstau100_mlsp1-RAWSIM/crab_stau_mstau100_mlsp1/210308_080104/0000/

```
## Useful Tools
Check failed datasets in GridControl directory:
```sh
source ./scripts/gc_FailDataChecker.sh /nfs/dust/cms/user/mykytaua/softLLSTAU/NTupling_new/grid-configs/work.gc_MC_SUSYSignal2017_v3
```

To check the SimVertex and GenPart.vertex matching on GEN-SIM output, run:
```sh
cmsRun python/FWLite_GEN-SIM-RECO.py
```

Quick compare of the jet distributions:
```sh
python ./DF-JetKinemCompare.py \
--paths "/pnfs/desy.de/cms/tier2/store/user/myshched/ntuples-tau-pog/SUS-RunIISummer20UL18wmLHEGEN-stau100_lsp1_ctau1000mm-GENSIM_v2/crab_STAU_stau100_lsp1_ctau1000mm/211205_142830/0000" \
        "/pnfs/desy.de/cms/tier2/store/user/myshched/ntuples-tau-pog/SUS-RunIISummer20UL18wmLHEGEN-stau250_lsp1_ctau1000mm-GENSIM_v2/crab_STAU_stau250_lsp1_ctau1000mm/211205_142843/0000" \
        "/pnfs/desy.de/cms/tier2/store/user/myshched/ntuples-tau-pog/SUS-RunIISummer20UL18wmLHEGEN-stau400_lsp1_ctau1000mm-GENSIM_v2/crab_STAU_stau400_lsp1_ctau1000mm/211205_142854/0000" \
        "/nfs/dust/cms/user/mykytaua/dataLLSTAU/tuples-tau-pog/HN_trilepton_M-4_tau" \
-na "mstau100" "mstau250" "mstau400" "HNL_M4" \
-c "genLepton_kind==5&&jet_pt>5" "genLepton_kind==5&&jet_pt>5" "genLepton_kind==5&&jet_pt>5" "genLepton_kind==5&&jet_pt>5" \
-N 5 5 5 5 \
-o ./JetKinematicsCompare
```

Some code is copy from the following repos: 
https://github.com/cms-tau-pog/TauMLTools  
https://github.com/DesyTau/DesyTauAnalysesRun2_25ns  
