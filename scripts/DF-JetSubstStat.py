import ROOT
import sys
import os
from itertools import product

sys.path.append("..")
import python.DrawUtils as DrawUtils
import python.Functions as MyFunc

ROOT.gInterpreter.Declare("#include \"../inc/GenLepton.h\"")

if __name__ == "__main__":

    '''
    The following script is performing the study of statistic
    of genLepton_kind and corresponding matched_jet substructure
    python ./DF-JetSubst.py <PATH_TO_TAUBIGTUPLES>
    '''

    ROOT.EnableImplicitMT(10)

    path_to_files = sys.argv[1]
    df = ROOT.RDataFrame("taus", path_to_files+"/*.root")
    # df = ROOT.RDataFrame("taus", path_to_files)
    
    taus_kinds = {}
    taus_kinds["Electron"]    =  df.Filter('genLepton_kind==1', 'Electron Candidates')
    taus_kinds["Muon"]        =  df.Filter('genLepton_kind==2', 'Muon Candidates')
    taus_kinds["TauElectron"] =  df.Filter('genLepton_kind==3', 'TauElectron Candidates')
    taus_kinds["TauMuon"]     =  df.Filter('genLepton_kind==4', 'TauMuon Candidates')
    taus_kinds["Tau"]         =  df.Filter('genLepton_kind==5', 'Tau Candidates')
    taus_kinds["Other"]       =  df.Filter('genLepton_kind==6', 'Other Candidates')
    taus_kinds["No_GenLepton"]=  df.Filter('genLepton_kind<=0', 'No GenLepton')

    taus_kinds_matchObj = {}
    for kind in taus_kinds:
        taus_kinds_matchObj[kind] = \
            [
                taus_kinds[kind].Filter('genJet_index>=0', kind + ': match genJet'),
                taus_kinds[kind].Filter('tau_index>=0', kind + ': match tau'),
                taus_kinds[kind].Filter('boostedTau_index>=0',  kind + ': match boosted_tau'),
                taus_kinds[kind].Filter('fatJet_index>=0', kind + ': match fat-jet'),
                taus_kinds[kind].Filter('jet_index>=0', kind + ': match jet'),
                taus_kinds[kind].Filter('genJet_index<0 && tau_index<0 && boostedTau_index<0 &&'+\
                                        'fatJet_index<0 && jet_index<0 ', kind + ': no match'),
            ]

    df.Report().Print()