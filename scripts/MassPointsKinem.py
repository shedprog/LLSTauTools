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
    The following script is performing the comperison of kinematic
    varaiables for different mass points. The script is run
    above BigTauTuple files that are created with TauMLTools.
    python ./MassPointsKinem.py <PATH_TO_TAUBIGTUPLES>
    '''

    path_to_files = sys.argv[1]

    ROOT.EnableImplicitMT(10)

    df = ROOT.RDataFrame("taus", path_to_files+"/*.root")
    # df = ROOT.RDataFrame("taus", path_to_files)

    hadronic_taus = df.Filter('genLepton_kind==5', 'Hadronic Taus Candidates')

    mstau_list = [100, 250, 400]
    mlsp_list  = [1, 20]
    ctau0_list = [1000]

    grid = list(product(*[mstau_list, mlsp_list, ctau0_list]))
    print("Mass ponts ",len(grid))

    filters = []
    hists = {
             "vis_pt":[],
             "vis_eta":[],
             "displ" : [],
             "displ_tr" : [],
             "stau_E"  : [],
             "stau_mass"   : [],
             "dRtaustau"   : [],
             "Angle_taustau" : [],
             "dRjetstau"     : []
            }
    for mstau, mlsp, ctau0 in grid:

        filters.append(hadronic_taus.Filter(
                f'susy_mstau=={mstau} && susy_mlsp=={mlsp} && susy_ctau=={ctau0}',
                f'mstau={mstau} mlsp={mlsp} ctau0={ctau0}'))
        
        # General kinematic check:
        get_kinem = MyFunc.DataFrameFunc.get_gen_info()
        filters[-1] = filters[-1].Define('gentau_info',get_kinem)\
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
                                 .Define('jetp4','reco_tau::gen_truth::LorentzVectorM(jet_pt, jet_eta, jet_phi, jet_mass)')\
                                 .Define('dR_stau_jet','ROOT::Math::VectorUtil::DeltaR\
                                     (std::get<2>(gentau_info),jetp4)')

        # filters[-1] =  filters[-1].Filter('jetp4.Pt()>1.0 && jetp4.Pt()<1000', 'have jet')

        hists['vis_pt'].append(filters[-1].Histo1D(("vis_pt",
                                                    f"vis_pt, MS({mstau}_{mlsp}_{ctau0})",
                                                    60, 0.0, 800), "vis_pt"))
        hists['vis_eta'].append(filters[-1].Histo1D(("vis_eta",
                                                    f"vis_eta, MS({mstau}_{mlsp}_{ctau0})",
                                                    40, -3.0, 3.0), "vis_eta"))
        hists['displ'].append(filters[-1].Histo1D(("displ",
                                                    f"displ., MS({mstau}_{mlsp}_{ctau0})",
                                                    50, 0, 150), "d"))
        hists['displ_tr'].append(filters[-1].Histo1D(("displ_tr",
                                                    f"displ. tr, MS({mstau}_{mlsp}_{ctau0})",
                                                    50, 0, 150), "dt"))
        hists['stau_E'].append(filters[-1].Histo1D(("stau_E",
                                                    f"gen stau_E. tr, MS({mstau}_{mlsp}_{ctau0})",
                                                    50, 0, 2000), "stau_E"))
        hists['stau_mass'].append(filters[-1].Histo1D(("stau_M",
                                                    f"gen stau_M. tr, MS({mstau}_{mlsp}_{ctau0})",
                                                    1000, 0, 500), "stau_mass"))
        hists['dRtaustau'].append(filters[-1].Histo1D(("dRtaustau",
                                                    f"gen dR(tau,stau), MS({mstau}_{mlsp}_{ctau0})",
                                                    50, 0, 5.0), "dR_stau_tau"))
        hists['Angle_taustau'].append(filters[-1].Histo1D(("Angle_taustau",
                                                    f"gen Angle(tau,stau), MS({mstau}_{mlsp}_{ctau0})",
                                                    100, 0, 3.0), "Angle_taustau"))
        hists['dRjetstau'].append(filters[-1].Histo1D(("dRjetstau",
                                                    f"gen dR(seedjet,stau), MS({mstau}_{mlsp}_{ctau0})",
                                                    100, 0, 5.0), "dR_stau_jet"))
        
    print('All stats:')
    allCutsReport = df.Report()
    allCutsReport.Print()

    canvas_pt = DrawUtils.GetCanvas("canvas_pt")
    DrawUtils.PlotHistList(canvas_pt, hists['vis_pt'],"[GeV]","entries")
    DrawUtils.DrawHeader(canvas_pt, "P^{T}_{vis}(#tau)" , "#tau reco", "c#tau_{0}=1000mm")
    DrawUtils.DrawLegend(canvas_pt, DrawUtils.GetHistTitlesLegend(hists["vis_pt"]))

    canvas_eta = DrawUtils.GetCanvas("canvas_eta")
    DrawUtils.PlotHistList(canvas_eta, hists['vis_eta'],"[-]","entries")
    DrawUtils.DrawHeader(canvas_eta, "#eta_{vis}(#tau)" , "#tau reco", "c#tau_{0}=1000mm")
    DrawUtils.DrawLegend(canvas_eta, DrawUtils.GetHistTitlesLegend(hists["vis_eta"]))

    canvas_eta = DrawUtils.GetCanvas("canvas_displ")
    DrawUtils.PlotHistList(canvas_eta, hists['displ'],"[cm]","entries")
    DrawUtils.DrawHeader(canvas_eta, "d(#tau)" , "#tau reco", "c#tau_{0}=1000mm")
    DrawUtils.DrawLegend(canvas_eta, DrawUtils.GetHistTitlesLegend(hists["displ"]))

    canvas_eta = DrawUtils.GetCanvas("canvas_displ_tr")
    DrawUtils.PlotHistList(canvas_eta, hists['displ_tr'], "[cm]","entries")
    DrawUtils.DrawHeader(canvas_eta, "d^{T}(#tau)" , "#tau reco", "c#tau_{0}=1000mm")
    DrawUtils.DrawLegend(canvas_eta, DrawUtils.GetHistTitlesLegend(hists["displ_tr"]))

    canvas_eta = DrawUtils.GetCanvas("canvas_stau_mass")
    DrawUtils.PlotHistList(canvas_eta, hists['stau_mass'],"[GeV]","entries")
    DrawUtils.DrawHeader(canvas_eta, "gen m(#tau)" , "#tau reco", "c#tau_{0}=1000mm")
    DrawUtils.DrawLegend(canvas_eta, DrawUtils.GetHistTitlesLegend(hists["stau_mass"]))

    canvas_eta = DrawUtils.GetCanvas("canvas_stau_E")
    DrawUtils.PlotHistList(canvas_eta, hists['stau_E'],"[GeV]","entries")
    DrawUtils.DrawHeader(canvas_eta, "gen E(#tau)" , "#tau reco", "c#tau_{0}=1000mm")
    DrawUtils.DrawLegend(canvas_eta, DrawUtils.GetHistTitlesLegend(hists["stau_E"]))

    canvas_eta = DrawUtils.GetCanvas("canvas_dRtaustau")
    DrawUtils.PlotHistList(canvas_eta, hists['dRtaustau'],"[dR]","entries")
    DrawUtils.DrawHeader(canvas_eta, "dR(tau,stau)" , "#tau reco", "c#tau_{0}=1000mm")
    DrawUtils.DrawLegend(canvas_eta, DrawUtils.GetHistTitlesLegend(hists["dRtaustau"]))

    canvas_eta = DrawUtils.GetCanvas("canvas_Angle_taustau")
    DrawUtils.PlotHistList(canvas_eta, hists['Angle_taustau'],"[rad]","entries")
    DrawUtils.DrawHeader(canvas_eta, "Angle(tau,stau)" , "#tau reco", "c#tau_{0}=1000mm")
    DrawUtils.DrawLegend(canvas_eta, DrawUtils.GetHistTitlesLegend(hists["Angle_taustau"]))

    canvas_eta = DrawUtils.GetCanvas("canvas_dRjetstau")
    DrawUtils.PlotHistList(canvas_eta, hists['dRjetstau'],"[dR]","entries")
    DrawUtils.DrawHeader(canvas_eta, "dR(ak4jet,stau)" , "#tau reco", "c#tau_{0}=1000mm")
    DrawUtils.DrawLegend(canvas_eta, DrawUtils.GetHistTitlesLegend(hists["dRjetstau"]))

    ROOT.gApplication.Run()
