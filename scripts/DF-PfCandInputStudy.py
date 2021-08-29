import ROOT
import sys
import os
from itertools import product
import argparse

sys.path.append("..")
import python.DrawUtils as DrawUtils
import python.Functions as MyFunc

ROOT.gInterpreter.Declare("#include \"../inc/GenLepton.h\"")

var = [
    ["pfCand_pt",                   1000, 0.0, 800  ],                  
    ["pfCand_eta",                  1000, -2.3, 2.3 ],                        
    ["pfCand_phi",                  1000, -3.15, 3.15 ],            
    ["pfCand_mass",                 1000, -1.0, 1.0 ],                      
    ["pfCand_charge",               20,   -5.0, 5.0 ],         
    ["pfCand_particleType",         20,    0.0, 10.0],           
    ["pfCand_pvAssociationQuality", 1000,             
    ["pfCand_fromPV",               1000,                      
    ["pfCand_puppiWeight",          1000,                         
    ["pfCand_puppiWeightNoLep",     1000,                        
    ["pfCand_lostInnerHits",        1000,                       
    ["pfCand_nPixelHits",           1000,                      
    ["pfCand_nHits",                1000,                       
    ["pfCand_hasTrackDetails",      1000,                         
    ["pfCand_dxy",                  1000,                         
    ["pfCand_dxy_error",            1000,                       
    ["pfCand_dz",                   1000,                      
    ["pfCand_dz_error",             1000,                        
    ["pfCand_track_chi2",           1000,                      
    ["pfCand_track_ndof",           1000,                      
    ["pfCand_caloFraction",         1000,                        
    ["pfCand_hcalFraction",         1000,                        
    ["pfCand_rawCaloFraction",      1000,                         
    ["pfCand_rawHcalFraction",      1000,                         
    ["pfCand_valid",                1000,                       
    ["pfCand_px",                   1000,                      
    ["pfCand_py",                   1000,                      
    ["pfCand_pz",                   1000,                      
    ["pfCand_E",                    1000,                       
    ["jet_eta",                     1000,                        
    ["jet_phi",                     1000,                        
    ["pfCand_deta",                 1000,                        
    ["pfCand_dphi",                 1000,                           
]

if __name__ == "__main__":

    '''
    The following script is performing the study of pfCand
    for the charged stau case. The script is run
    above BigTauTuple files that are created with TauMLTools.
    '''

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--path', help='path to the folder with files')
    parser.add_argument('--n-threads', help='number of threads', default=1)
    args = parser.parse_args()


    ROOT.EnableImplicitMT(1)

    # df = ROOT.RDataFrame("taus", args.path+"/*.root")
    df = ROOT.RDataFrame("taus", args.path)
    hadronic_taus = df.Filter('genLepton_kind==5', 'Hadronic Taus Candidates')

    hists = {}

    # General kinematic check:
 
    # hadronic_taus = hadronic_taus.Define('gentau_info',get_kinem)\
    #                              .Define('vis_pt','std::get<0>(gentau_info).Pt()')\

    hists['pfCand_pt']                   = hadronic_taus.Histo1D(("pfCand_pt", "pfCand_pt", 1000, 0.0, 800), "pfCand_pt")
    hists['pfCand_eta']                  = hadronic_taus.Histo1D(("pfCand_eta", "pfCand_eta", , 0.0, 800), "pfCand_eta")
    hists['pfCand_phi']                  = hadronic_taus.Histo1D(("pfCand_phi", "pfCand_phi", 60, 0.0, 800), "pfCand_phi")
    hists['pfCand_pt']                   = hadronic_taus.Histo1D(("pfCand_pt", "pfCand_pt", 60, 0.0, 800), "pfCand_pt")
    hists['pfCand_mass']                 = hadronic_taus.Histo1D(("pfCand", "pfCand", 1001, -1.0, 1.0), "pfCand_mass")
    hists['pfCand_charge']               = hadronic_taus.Histo1D(("pfCand_charge", "pfCand_charge", 60, 0.0, 800), "pfCand_charge")
    hists['pfCand_particleType']         = hadronic_taus.Histo1D(("pfCand_particleType", "pfCand_particleType", 60, 0.0, 800), "pfCand_particleType")
    hists['pfCand_pvAssociationQuality'] = hadronic_taus.Histo1D(("pfCand_pvAssociationQuality", "pfCand_pvAssociationQuality", 60, 0.0, 800), "pfCand_pvAssociationQuality")
    hists['pfCand_fromPV']               = hadronic_taus.Histo1D(("pfCand_fromPV", "pfCand_fromPV", 60, 0.0, 800), "pfCand_fromPV")
    hists['pfCand_puppiWeight']          = hadronic_taus.Histo1D(("pfCand_puppiWeight", "pfCand_puppiWeight", 60, 0.0, 800), "pfCand_puppiWeight")
    hists['pfCand_puppiWeightNoLep']     = hadronic_taus.Histo1D(("pfCand_puppiWeightNoLep", "pfCand_puppiWeightNoLep", 60, 0.0, 800), "pfCand_puppiWeightNoLep")
    hists['pfCand_lostInnerHits']        = hadronic_taus.Histo1D(("pfCand_lostInnerHits", "pfCand_lostInnerHits", 60, 0.0, 800), "pfCand_lostInnerHits")
    hists['pfCand_nPixelHits']           = hadronic_taus.Histo1D(("pfCand_nPixelHits", "pfCand_nPixelHits", 60, 0.0, 800), "pfCand_nPixelHits")
    hists['pfCand_nHits']                = hadronic_taus.Histo1D(("pfCand_nHits", "pfCand_nHits", 60, 0.0, 800), "pfCand_nHits")
    hists['pfCand_hasTrackDetails']      = hadronic_taus.Histo1D(("pfCand_hasTrackDetails", "pfCand_hasTrackDetails", 60, 0.0, 800), "pfCand_hasTrackDetails")
    hists['pfCand_dxy']                  = hadronic_taus.Histo1D(("pfCand_dxy", "pfCand_dxy", 60, 0.0, 800), "pfCand_dxy")
    hists['pfCand_dxy_error']            = hadronic_taus.Histo1D(("pfCand_dxy_error", "pfCand_dxy_error", 60, 0.0, 800), "pfCand_dxy_error")
    hists['pfCand_dz']                   = hadronic_taus.Histo1D(("pfCand_dz", "pfCand_dz", 60, 0.0, 800), "pfCand_dz")
    hists['pfCand_dz_error']             = hadronic_taus.Histo1D(("pfCand_dz_error", "pfCand_dz_error", 60, 0.0, 800), "pfCand_dz_error")
    hists['pfCand_track_chi2']           = hadronic_taus.Histo1D(("pfCand_track_chi2", "pfCand_track_chi2", 60, 0.0, 800), "pfCand_track_chi2")
    hists['pfCand_track_ndof']           = hadronic_taus.Histo1D(("pfCand_track_ndof", "pfCand_track_ndof", 60, 0.0, 800), "pfCand_track_ndof")
    hists['pfCand_caloFraction']         = hadronic_taus.Histo1D(("pfCand_caloFraction", "pfCand_caloFraction", 60, 0.0, 800), "pfCand_caloFraction")
    hists['pfCand_hcalFraction']         = hadronic_taus.Histo1D(("pfCand_hcalFraction", "pfCand_hcalFraction", 60, 0.0, 800), "pfCand_hcalFraction")
    hists['pfCand_rawCaloFraction']      = hadronic_taus.Histo1D(("pfCand_rawCaloFraction", "pfCand_rawCaloFraction", 60, 0.0, 800), "pfCand_rawCaloFraction")
    hists['pfCand_rawHcalFraction']      = hadronic_taus.Histo1D(("pfCand_rawHcalFraction", "pfCand_rawHcalFraction", 60, 0.0, 800), "pfCand_rawHcalFraction")
    hists['pfCand_valid']                = hadronic_taus.Histo1D(("pfCand_valid", "pfCand_valid", 60, 0.0, 800), "pfCand_valid")
    hists['pfCand_px']                   = hadronic_taus.Histo1D(("pfCand_px", "pfCand_px", 60, 0.0, 800), "pfCand_px")
    hists['pfCand_py']                   = hadronic_taus.Histo1D(("pfCand_py", "pfCand_py", 60, 0.0, 800), "pfCand_py")
    hists['pfCand_pz']                   = hadronic_taus.Histo1D(("pfCand_pz", "pfCand_pz", 60, 0.0, 800), "pfCand_pz")
    hists['pfCand_E']                    = hadronic_taus.Histo1D(("pfCand_E", "pfCand_E", 1000, -100.0, 800), "pfCand_E")
    hists['jet_eta']                     = hadronic_taus.Histo1D(("jet_eta", "jet_eta", 60, 0.0, 800), "jet_eta")
    hists['jet_phi']                     = hadronic_taus.Histo1D(("jet_phi", "jet_phi", 60, 0.0, 800), "jet_phi")
    hists['pfCand_deta']                 = hadronic_taus.Histo1D(("pfCand_deta", "pfCand_deta", 60, 0.0, 800), "pfCand_deta")
    hists['pfCand_dphi']                 = hadronic_taus.Histo1D(("pfCand_dphi", "pfCand_dphi", 60, 0.0, 800), "pfCand_dphi")
        
    print('All stats:')
    allCutsReport = df.Report()
    allCutsReport.Print()

    canvas_pt = DrawUtils.GetCanvas("canvas_pt")
    DrawUtils.PlotHistList(canvas_pt, [hists['pfCand_mass']]    ,"[GeV]","entries")
    DrawUtils.DrawHeader(canvas_pt, "???" , "#tau reco", "c#tau_{0}=1000mm")
    DrawUtils.DrawLegend(canvas_pt, DrawUtils.GetHistTitlesLegend([hists['pfCand_mass']]))
    # canvas_pt.SetLogy()

    # canvas_E = DrawUtils.GetCanvas("canvas_E")
    # DrawUtils.PlotHistList(canvas_E, [hists['pfCand_E'] ]    ,"[GeV]","entries")
    # DrawUtils.DrawHeader(canvas_E, "???" , "#tau reco", "c#tau_{0}=1000mm")
    # DrawUtils.DrawLegend(canvas_E, DrawUtils.GetHistTitlesLegend([hists['pfCand_E'] ]))
    # canvas_E.SetLogy()

    ROOT.gApplication.Run()