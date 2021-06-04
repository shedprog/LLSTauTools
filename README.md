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
./LifeTimeTauEfficiencyTauTuple 1 /pnfs/desy.de/cms/tier2/store/user/myshched/Signal2018ctau/SUS-RunIIFall18GS_ctau0p01-1000mm_mstau100_mlsp1-RAWSIM/crab_stau_mstau100_mlsp1/210308_080104/0000/

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

Some code is copy from the following repos: 
https://github.com/cms-tau-pog/TauMLTools  
https://github.com/DesyTau/DesyTauAnalysesRun2_25ns  
