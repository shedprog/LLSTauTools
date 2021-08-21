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
    The following script is performing the study of pfCand/isoTracks/lostTracks
    for the charged stau case. The script is run
    above BigTauTuple files that are created with TauMLTools.
    python ./MassPointStat.py <PATH_TO_TAUBIGTUPLES>
    '''

    path_to_files = sys.argv[1]

    ROOT.EnableImplicitMT(10)

    df = ROOT.RDataFrame("taus", path_to_files+"/*.root")
    # df = ROOT.RDataFrame("taus", path_to_files)

    hadronic_taus = df.Filter('genLepton_kind==5', 'Hadronic Taus Candidates')

    hists = {}

    # General kinematic check:
    get_kinem = MyFunc.DataFrameFunc.get_gen_info()
    hadronic_taus = hadronic_taus.Define('gentau_info',get_kinem)\
                                 .Define('vis_pt','std::get<0>(gentau_info).Pt()')\
                                 .Define('vis_eta','std::get<0>(gentau_info).Eta()')\
                                 .Define('dt', 'std::get<1>(gentau_info).Rho()')\
                                 .Define('d', 'std::get<1>(gentau_info).R()')\
                                 .Define('stau_E', 'std::get<2>(gentau_info).E()')\
                                 .Define('stau_mass', 'std::get<2>(gentau_info).M()')\
                                 .Define('dR_stau_tau','ROOT::Math::VectorUtil::DeltaR\
                                     (std::get<0>(gentau_info),std::get<2>(gentau_info))')\
                                 .Define('Angle_taustau','ROOT::Math::VectorUtil::Angle\
                                     (std::get<0>(gentau_info),std::get<2>(gentau_info))')\

    hists['vis_pt'] = hadronic_taus.Histo1D(("vis_pt", f"some hist", 60, 0.0, 800), "vis_pt")
        
    print('All stats:')
    allCutsReport = df.Report()
    allCutsReport.Print()

    canvas_pt = DrawUtils.GetCanvas("canvas_pt")
    DrawUtils.PlotHistList(canvas_pt, hists['vis_pt'],"[GeV]","entries")
    DrawUtils.DrawHeader(canvas_pt, "P^{T}_{vis}(#tau)" , "#tau reco", "c#tau_{0}=1000mm")
    DrawUtils.DrawLegend(canvas_pt, DrawUtils.GetHistTitlesLegend(hists["vis_pt"]))


    ROOT.gApplication.Run()