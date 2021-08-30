import ROOT
import sys
import os
from itertools import product
import argparse

ROOT.gROOT.SetBatch(True)

sys.path.append("..")
import python.DrawUtils as DrawUtils
import python.Functions as MyFunc

ROOT.gInterpreter.Declare("#include \"../inc/GenLepton.h\"")

vars = [
    ["pfCand_pt",                   1000, 0.0, 800  ],                  
    ["pfCand_eta",                  1000, -2.3, 2.3 ],                        
    ["pfCand_phi",                  1000, -3.15, 3.15 ],            
    ["pfCand_mass",                 1000, -1.0, 1.0 ],                      
    ["pfCand_charge",               20,   -5.0, 5.0 ],         
    ["pfCand_particleType",         20,    0.0, 10.0],           
    ["pfCand_pvAssociationQuality", 20,    0.0, 10.0],             
    ["pfCand_fromPV",               20,    0.0, 10.0],                     
    ["pfCand_puppiWeight",          100,   0.0, 1.0],                         
    ["pfCand_puppiWeightNoLep",     100,   0.0, 1.0],                        
    ["pfCand_lostInnerHits",        100,  -1.0, 10.0],                    
    ["pfCand_nPixelHits",           100,  -1.0, 20.0],          
    ["pfCand_nHits",                200,  -1.0, 100.0],          
    ["pfCand_hasTrackDetails",      10,   -1.0, 2.0],                        
    ["pfCand_dxy",                  100, -1.0, 1.0],                       
    ["pfCand_dxy_error",            100, -1.0, 1.0],                       
    ["pfCand_dz",                   100, -20 , 20 ],                    
    ["pfCand_dz_error",             100, -1.0, 1.0],            
    ["pfCand_track_chi2",           100, -100, 100],                   
    ["pfCand_track_ndof",           100, -100, 100],                     
    ["pfCand_caloFraction",         100,  0.0, 2.5],                       
    ["pfCand_hcalFraction",         100,  0.0, 2.5],                       
    ["pfCand_rawCaloFraction",      100,  0.0, 2.5],                        
    ["pfCand_rawHcalFraction",      100,  0.0, 2.5],                        
    # ["pfCand_valid",                5,     0.0, 2.0],          
    # ["pfCand_px",                   1000,  0.0, 800 ],                      
    # ["pfCand_py",                   1000,  0.0, 800 ],                      
    # ["pfCand_pz",                   1000,  0.0, 800 ],                      
    # ["pfCand_E",                    1000,  0.0, 800 ],                       
    ["jet_eta",                     1000, -2.3, 2.3 ],                       
    ["jet_phi",                     1000, -3.15, 3.15 ],                  
    # ["pfCand_deta",                 1000, -1.0, 1.0 ],                    
    # ["pfCand_dphi",                 1000, -1.0, 1.0 ]                         
]

if __name__ == "__main__":

    '''
    The following script is performing the study of pfCand
    for the charged stau case. The script is run
    above BigTauTuple files that are created with TauMLTools.
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
    hadronic_taus = df.Filter('genLepton_kind==5', 'Hadronic Taus Candidates')

    hists = {}
    # General kinematic check:
    hadronic_taus = hadronic_taus.Define('pfCand_deta','jet_eta-pfCand_eta')\
                                 .Define('pfCand_dphi','jet_phi-pfCand_phi')
    for var in vars:
        hists[var[0]] = hadronic_taus.Histo1D((var[0], var[0], var[1], var[2], var[3]), var[0])
    
    hists["pfCand_deta"] = hadronic_taus.Histo1D(("pfCand_deta", "pfCand_deta",
                                                  100, -1.0, 1.0), "pfCand_deta")
    hists["pfCand_dphi"] = hadronic_taus.Histo1D(("pfCand_dphi", "pfCand_dphi",
                                                  100, -3.15, 3.15), "pfCand_dphi")                                                  

    print('All stats:')
    allCutsReport = df.Report()
    allCutsReport.Print()

    for var in hists:
        print(var, "is saved")
        canvas = DrawUtils.GetCanvas("canvas")
        DrawUtils.PlotHistList(canvas, [hists[var]], "[-]", "entries")
        DrawUtils.DrawHeader(canvas, var , "#tau reco", "c#tau_{0}=1000mm")
        DrawUtils.DrawLegend(canvas, DrawUtils.GetHistTitlesLegend([hists[var]]))
        canvas.SaveAs(args.output+"/var_"+var+".png")

    # ROOT.gApplication.Run()