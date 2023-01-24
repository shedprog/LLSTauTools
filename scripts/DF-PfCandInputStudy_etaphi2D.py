import ROOT
import sys
import os
from itertools import product
import argparse

ROOT.gROOT.SetBatch(True)

# sys.path.append("..")
# sys.path.insert(0, "..")
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import python.DrawUtils as DrawUtils
import python.Functions as MyFunc

ROOT.gInterpreter.Declare(f"#include \"{os.path.dirname(os.path.realpath(__file__))}/../inc/GenLepton.h\"")

my_vars = {
    "pfCand_2D_type0" : [ 100, -0.5, 0.5, 100, -0.5, 0.5, "log"],
    "pfCand_2D_type1" : [ 100, -0.5, 0.5, 100, -0.5, 0.5, "log"],
    "pfCand_2D_type2" : [ 100, -0.5, 0.5, 100, -0.5, 0.5, "log"],
    "pfCand_2D_type3" : [ 100, -0.5, 0.5, 100, -0.5, 0.5, "log"],
    "pfCand_2D_type4" : [ 100, -0.5, 0.5, 100, -0.5, 0.5, "log"],
    "pfCand_2D_type5" : [ 100, -0.5, 0.5, 100, -0.5, 0.5, "log"],
    "pfCand_2D_type6" : [ 100, -0.5, 0.5, 100, -0.5, 0.5, "log"],
    "pfCand_2D_type7" : [ 100, -0.5, 0.5, 100, -0.5, 0.5, "log"],
}

## ParticleTypes:
# Undefined
# charged hadron
# electron
# muon
# photon
# neutral hadron
# HF tower identified as a hadron
# HF tower identified as an EM particle

if __name__ == "__main__":

    '''
    The following script is compering kinematicks of
    jetType=0 and jetType=1 for Flat ShufleMerge sample.
    '''

    parser = argparse.ArgumentParser(description='Plot pf candidates etaphi distributions.')
    parser.add_argument('--path', help='Path to the folder with files')
    parser.add_argument('--output', help='The output path')
    parser.add_argument('--cut', default="jetType==1)", help='Event selection')
    parser.add_argument('--n-threads', help='Number of threads', default=1)
    args = parser.parse_args()

    if not os.path.exists(args.output):
        os.makedirs(args.output)

    ROOT.EnableImplicitMT(1)

    # df = ROOT.RDataFrame("taus", args.path+"/*.root")
    df = ROOT.RDataFrame("taus", args.path)


    pf_filter = {}
    hists = {}


    f = df.Filter(args.cut, 'Selection')

    f = f.Define('pfCand_deta','jet_eta-pfCand_eta')
    f = f.Define('pfCand_dphi','DeltaPhi(jet_phi,pfCand_phi)')

    for t, var in enumerate(my_vars.keys()):

        pf_filter[var] = f

        pf_select = f"[(pfCand_jetDaughter == 1) && (pfCand_particleType=={str(t)})]"

        pf_filter[var] = pf_filter[var].Define('pfCand_deta_select','pfCand_deta'+pf_select)
        pf_filter[var] = pf_filter[var].Define('pfCand_dphi_select','pfCand_dphi'+pf_select)

        setups = my_vars[var]
        print(var, var, setups[0], setups[1], setups[2], setups[3], setups[4], setups[5])
        hists[var] = pf_filter[var].Histo2D((var, var, setups[0], setups[1], setups[2], setups[3], setups[4], setups[5]), "pfCand_deta_select", "pfCand_dphi_select")
        
                                               
    print('All stats:')
    allCutsReport = df.Report()
    allCutsReport.Print()

    for t, var in enumerate(my_vars.keys()):
        # var = var_list[0]
        print(var, "is saved")
        canvas = DrawUtils.GetCanvas("canvas")
        DrawUtils.PlotHist2D(canvas, hists[var], "eta", "phi")
        DrawUtils.DrawHeader(canvas, var , "", "c#tau_{0}=1000mm")
        if my_vars[var][6]=="log":
            canvas.SetLogz()
        canvas.Modified()
        canvas.Update()
        canvas.SaveAs(args.output+"/var_"+var+".png")

    # ROOT.gApplication.Run()