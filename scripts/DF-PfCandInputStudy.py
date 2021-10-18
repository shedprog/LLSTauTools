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
    ["pfCand_pt",                   70, 0.0, 100 ],                  
    ["pfCand_eta",                  70, -2.5, 2.5 ],                        
    ["pfCand_phi",                  70, -3.15, 3.15 ],            
    ["pfCand_mass",                 70, -0.1, 0.2 ],                      
    ["pfCand_charge",               20,   -5.0, 5.0 ],         
    ["pfCand_particleType",         20,    0.0, 10.0],           
    ["pfCand_pvAssociationQuality", 20,    0.0, 10.0],             
    ["pfCand_fromPV",               10,    0.0, 5],                     
    ["pfCand_puppiWeight",          20,   0.0, 1.0],                         
    ["pfCand_puppiWeightNoLep",     20,   0.0, 1.0],                        
    ["pfCand_lostInnerHits",        70,  -1.0, 3.0],                    
    ["pfCand_nPixelHits",           11,  -1.0, 10.0],          
    ["pfCand_nHits",                31,  -1.0, 30.0],          
    ["pfCand_hasTrackDetails",      10,   -1.0, 2.0],                        
    ["pfCand_dxy",                  70, -0.1, 0.1],                       
    ["pfCand_dxy_error",            70, 0.0, 0.1],                       
    ["pfCand_dz",                   70,  -15,  15 ],                    
    ["pfCand_dz_error",             70,  0.0, 0.06 ],             
    ["pfCand_track_chi2",           35,  0.0, 35],                   
    ["pfCand_track_ndof",           20,  0.0, 35],                     
    ["pfCand_caloFraction",         70,  0.0, 2.5],                       
    ["pfCand_hcalFraction",         70,  0.0, 1.1],                       
    ["pfCand_rawCaloFraction",      20,  0.0, 1.0],                        
    ["pfCand_rawHcalFraction",      20,  0.0, 1.0],                        
    # ["pfCand_valid",                5,     0.0, 2.0],          
    # ["pfCand_px",                   1000,  0.0, 800 ],                      
    # ["pfCand_py",                   1000,  0.0, 800 ],                      
    # ["pfCand_pz",                   1000,  0.0, 800 ],                      
    # ["pfCand_E",                    1000,  0.0, 800 ],                       
    # ["jet_eta",                     1000, -2.3, 2.3 ],                       
    # ["jet_phi",                     1000, -3.15, 3.15 ],                  
    ["pfCand_deta",                 70, -1.0, 1.0 ],                    
    ["pfCand_dphi",                 70, -1.0, 1.0 ],
    ["n_pfCand",                   100,    0, 300]                       
]

if __name__ == "__main__":

    '''
    The following script is compering kinematicks of
    signal_class=0 and signal_class=1 for Flat ShufleMerge sample.
    '''

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--path', help='path to the folder with files')
    parser.add_argument('--output', help='the output path')
    parser.add_argument('--n-threads', help='number of threads', default=1)
    args = parser.parse_args()

    if not os.path.exists(args.output):
        os.makedirs(args.output)

    ROOT.EnableImplicitMT(1)

    df = ROOT.RDataFrame("taus", args.path+"/*.root")
    # df = ROOT.RDataFrame("taus", args.path)

    fs = [df.Filter('signal_class==0', 'Background'),
          df.Filter('signal_class==1', 'Signal')]

    hists = [{},{}]
    names = ["QCD", "Signal"]

    for i, f in enumerate(fs):
        f = f.Define('pfCand_deta','jet_eta-pfCand_eta').Define('pfCand_dphi','jet_phi-pfCand_phi')
        f = f.Define('n_pfCand', 'pfCand_pt.size()')
        for var in vars:
            hists[i][var[0]] = f.Histo1D((var[0], names[i], var[1], var[2], var[3]), var[0])
                                               
    print('All stats:')
    allCutsReport = df.Report()
    allCutsReport.Print()

    for var_list in vars:
        var = var_list[0]
        print(var, "is saved")
        canvas = DrawUtils.GetCanvas("canvas")
        DrawUtils.PlotHistList(canvas, [hists[1][var],hists[0][var]], "[-]", "entries")
        DrawUtils.DrawHeader(canvas, var , "", "c#tau_{0}=1000mm")
        DrawUtils.DrawLegend(canvas, DrawUtils.GetHistTitlesLegend([hists[1][var],hists[0][var]]))
        canvas.SaveAs(args.output+"/var_"+var+".png")

    # ROOT.gApplication.Run()