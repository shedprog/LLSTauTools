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
    # ["pfCand_valid",        4, 0, 4  ],
    ["pfCand_pt",           100, 0.0, 400 , "log"],
    ["pfCand_eta",          70, -2.5, 2.5, "lin"],
    ["pfCand_phi",          70, -3.3, 3.3, "lin"],
    ["pfCand_mass",         70, -0.2, 0.3 , "log"],
    ["pfCand_charge",       20, -5.0, 5.0 , "lin"],
    ["pfCand_puppiWeight",  32, -0.1, 1.1, "log"],
    ["pfCand_puppiWeightNoLep",  32, -0.1, 1.1  , "log"],
    ["pfCand_lostInnerHits",     70, -1.0, 3.0 , "lin"],
    ["pfCand_nPixelHits",   11, -1.0, 11.0 , "lin"],
    ["pfCand_nHits",        31, -1.0, 40.0 , "lin"],
    ["pfCand_hasTrackDetails", 10, -1.0, 2.0, "lin"],
    ["pfCand_dxy",          70, -0.2, 0.2, "log"],
    ["pfCand_dxy_error",    70, -0.02, 0.2, "log"],
    ["pfCand_dz",           70, -30,  30, "log"],
    ["pfCand_dz_error",     70, -0.02, 0.2 , "log"],
    ["pfCand_track_chi2",   20,  0.0, 45, "lin"],
    ["pfCand_track_ndof",   20,  0.0, 45, "lin"],
    ["pfCand_caloFraction", 70, -0.02, 3.5, "log"],
    ["pfCand_hcalFraction", 70, -0.02, 1.5, "log"],
    ["pfCand_rawCaloFraction", 40, 0.0, 1.2, "log"],
    ["pfCand_rawHcalFraction", 40, 0.0, 1.2, "log"],
    ["pfCand_deta",         70, -1.0, 1.0, "lin"],
    ["pfCand_dphi",         70, -1.0, 1.0, "lin"],
    ["pfCand_particleType", 20, 0.0, 10.0, "lin"],
    ["pfCand_pvAssociationQuality",  20, 0.0, 10.0, "lin"],
    ["pfCand_fromPV",  10, 0.0, 5, "lin"],
    ["pfCand_vertex_xy",  50, 0.0, 90, "log"],
    ["pfCand_vertex_z",  50, -100, 100, "log"],
    ["n_pfCand",       150, 0, 150, "lin"]
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
        for var in vars[:-1]:
            f = f.Define(var[0]+'_j', var[0]+'[pfCand_jetDaughter == 1]')

        # f = f.Define('n_pfCand_j', 'pfCand_pt.size()')
        # for var in vars[:-1]:
        #     f = f.Define(var[0]+'_j', var[0])

        for var in vars:
            hists[i][var[0]] = f.Histo1D((var[0], names[i], var[1], var[2], var[3]), var[0]+'_j')
        
        

        # sums: here we try to calculate sums because they might be differ for two datasets
        # the scale is multiplied by 50 expecting that we take 50 pfCands
        # for var in vars[:-1]:
        #     f = f.Define("sum_"+var[0], MyFunc.DataFrameFunc.sum_up_var(var[0]))
        #     hists[i]["sum_"+var[0]] = f.Histo1D(("sum_"+var[0], names[i], var[1],
        #                                         var[2] if var[2]>=0 else var[2]*50,var[3]*50),
        #                                         "sum_"+var[0])

                                               
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

    # for var_list in vars[:-1]:
    #     var = "sum_"+var_list[0]
    #     print(var, "is saved")
    #     canvas = DrawUtils.GetCanvas("canvas")
    #     DrawUtils.PlotHistList(canvas, [hists[1][var],hists[0][var]], "[-]", "entries")
    #     DrawUtils.DrawHeader(canvas, var , "", "c#tau_{0}=1000mm")
    #     # DrawUtils.DrawLegend(canvas, DrawUtils.GetHistTitlesLegend([hists[1][var],hists[0][var]]))
    #     l = DrawUtils.GetHistTitlesLegend([hists[1][var],hists[0][var]])
    #     l.Draw()
    #     canvas.Modified()
    #     canvas.Update()
    #     canvas.SaveAs(args.output+"/var_"+var+".png")

    # ROOT.gApplication.Run()