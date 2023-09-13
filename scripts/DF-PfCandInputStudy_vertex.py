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

ROOT.gInterpreter.Declare(f"#include \"{os.path.dirname(__file__)}/../inc/GenLepton.h\"")

vars = [
    ["pfCand_vertex_xy",  50, 0.0, 900, "log"],
    ["pfCand_vertex_z",  50, -1000, 1000, "log"],
]

if __name__ == "__main__":

    '''
    The following script is compering kinematicks of
    jetType=0 and jetType=1 for Flat ShufleMerge sample.
    '''

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--path', help='path to the folder with files')
    parser.add_argument('--output', help='the output path')
    parser.add_argument('--n-threads', help='number of threads', default=1)
    args = parser.parse_args()

    if not os.path.exists(args.output):
        os.makedirs(args.output)

    ROOT.EnableImplicitMT(1)

    # df = ROOT.RDataFrame("taus", args.path+"/*.root")
    df = ROOT.RDataFrame("taus", args.path)

    fs = [df.Filter('jetType==1', 'Signal'),
          df.Filter('jetType==0', 'Background')]

    hists = [{},{}]
    names = ["Signal", "QCD"]

    for i, f in enumerate(fs):

        # f = f.Filter('pfCand_jetDaughter == 1', 'Select Jet Pfcands only')
        f = f.Define('pfCand_deta','jet_eta-pfCand_eta')
        f = f.Define('pfCand_dphi','DeltaPhi(jet_phi,pfCand_phi)')
        f = f.Define('pfCand_vertex_xy', 'sqrt( pfCand_vertex_x*pfCand_vertex_x + pfCand_vertex_y*pfCand_vertex_y )')

        f = f.Define('n_pfCand_j', 'pfCand_pt[pfCand_jetDaughter == 1].size()')
        for var in vars:
            f = f.Define(var[0]+'_j', var[0]+'[pfCand_jetDaughter == 1]')

        # f = f.Define('n_pfCand_j', 'pfCand_pt.size()')
        # for var in vars:
        #     f = f.Define(var[0]+'_j', var[0])

        for var in vars:
            hists[i][var[0]] = f.Histo1D((var[0], names[i], var[1], var[2], var[3]), var[0]+'_j')
        
                                               
    print('All stats:')
    allCutsReport = df.Report()
    allCutsReport.Print()

    for var_list in vars:
        var = var_list[0]
        print(var, "is saved")
        canvas = DrawUtils.GetCanvas("canvas")
        DrawUtils.PlotHistList(canvas, [hists[1][var],hists[0][var]], "[-]", "entries")
        DrawUtils.DrawHeader(canvas, var , "", "c#tau_{0}=1000mm")
        # DrawUtils.DrawLegend(canvas, )
        l = DrawUtils.GetHistTitlesLegend([hists[1][var],hists[0][var]])
        l.Draw()
        if var_list[4]=="log":
            canvas.SetLogy()
        canvas.Modified()
        canvas.Update()
        canvas.SaveAs(args.output+"/var_"+var+".png")

