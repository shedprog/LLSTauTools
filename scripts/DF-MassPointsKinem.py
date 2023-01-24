import ROOT
import sys
import os
from itertools import product
import argparse
import glob

sys.path.append("..")
import python.DrawUtils as DrawUtils
import python.Functions as MyFunc

ROOT.gInterpreter.Declare("#include \"../inc/GenLepton.h\"")

ROOT.gROOT.SetBatch(True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=\
    '''
    The following script is performing the comperison of kinematic
    varaiables for different mass points. The script is run
    above BigTauTuple files that are created with TauMLTools.
    ''')
    parser.add_argument('-p','--paths', nargs='+', help='Full path to the datasets', required=True)
    parser.add_argument('-na','--names', nargs='+', help='Name of the cooresponding DataSet', required=True)
    parser.add_argument('-c','--cuts', nargs='+', help='Cuts for the cooresponding DataSet', required=True)
    parser.add_argument('-N','--number', nargs='+', help='Number of files to analyse', required=True)
    parser.add_argument('-o','--output', help='folder for the plot outputs', required=True)
    args = parser.parse_args()
    try:
        assert(len(args.paths)==\
               len(args.names)==\
               len(args.cuts))
        cuts = args.cuts
    except:
        assert(len(args.paths)==\
               len(args.names))
        cuts = [args.cuts[0] for _ in args.paths]
        

    if not os.path.exists(args.output): os.makedirs(args.output)

    ROOT.EnableImplicitMT(10)
    df = []
    filters = []
    hists = {
             "vis_pt": [],
             "vis_eta": [],
             "vis_mass": [],
             "displ" : [],
             "displ_tr" : [],
             "stau_E"  : [],
             "stau_mass"   : [],
             "dRtaustau"   : [],
             "Angle_taustau" : [],
             "dRjetstau"     : [],
             "rel_pt" : [],
             "d_mass" : [],
             "dR_tau_jet" : []
            }
    # for mstau, mlsp, ctau0 in grid:
    for i, path in enumerate(args.paths):
        files = glob.glob(path +"/**/*.root", recursive=True)
        print("name:", args.names[i], "cuts:", cuts[i])
        print("files: ", files[:int(args.number[i])])
        df.append(ROOT.RDataFrame("taus", files[:int(args.number[i])]))

        filters.append(df[-1].Filter("genLepton_kind==5", args.names[i]+"_base"))
        # filters[-1] = filters[-1].Filter("","has gen stau")
        # General kinematic check:
        get_kinem = MyFunc.DataFrameFunc.get_gen_info()
        filters[-1] = filters[-1].Define('gentau_info',get_kinem)\
                                 .Define('vis_pt','std::get<0>(gentau_info).Pt()')\
                                 .Define('vis_eta','std::get<0>(gentau_info).Eta()')\
                                 .Define('vis_mass','std::get<0>(gentau_info).mass()')\
                                 .Define('Lxy', 'std::get<1>(gentau_info).Rho()')\
                                 .Define('Lxyz', 'std::get<1>(gentau_info).R()')\
                                 .Define('Lz', 'std::get<1>(gentau_info).Z()')\
                                 .Define('stau_E', 'std::get<2>(gentau_info).E()')\
                                 .Define('stau_mass', 'std::get<2>(gentau_info).M()')\
                                 .Define('dR_stau_tau','ROOT::Math::VectorUtil::DeltaR\
                                     (std::get<0>(gentau_info),std::get<2>(gentau_info))')\
                                 .Define('Angle_taustau','ROOT::Math::VectorUtil::Angle\
                                     (std::get<0>(gentau_info),std::get<2>(gentau_info))')\
                                 .Define('jetp4','reco_tau::gen_truth::LorentzVectorM(jet_pt, jet_eta, jet_phi, jet_mass)')\
                                 .Define('dR_stau_jet','ROOT::Math::VectorUtil::DeltaR\
                                     (std::get<2>(gentau_info),jetp4)')\
                                 .Define('rel_pt', '(jet_pt-vis_pt)/vis_pt')\
                                 .Define('d_mass', 'jet_mass-vis_mass')\
                                 .Define('dR_tau_jet', 'ROOT::Math::VectorUtil::DeltaR(std::get<0>(gentau_info),jetp4)')

        # Apply extra cuts
        filters[-1] = filters[-1].Filter(cuts[i], args.names[i])

        hists['vis_pt'].append(filters[-1].Histo1D(("vis_pt",
                                                    f"vis_pt, {args.names[i]}",
                                                    60, 0.0, 800), "vis_pt"))
        hists['vis_eta'].append(filters[-1].Histo1D(("vis_eta",
                                                    f"vis_eta, {args.names[i]}",
                                                    40, -3.0, 3.0), "vis_eta"))
        hists['vis_mass'].append(filters[-1].Histo1D(("vis_mass",
                                                    f"vis_mass, {args.names[i]}",
                                                    100, 0.0, 2.3), "vis_mass"))
        hists['displ'].append(filters[-1].Histo1D(("Lxyz",
                                                    f"displ., {args.names[i]}",
                                                    200, 0, 200), "Lxyz"))
        hists['displ_tr'].append(filters[-1].Histo1D(("Lxy",
                                                    f"displ. tr, {args.names[i]}",
                                                    200, 0, 200), "Lxy"))
        hists['stau_E'].append(filters[-1].Histo1D(("stau_E",
                                                    f"gen stau_E. tr, {args.names[i]}",
                                                    50, 0, 2000), "stau_E"))
        hists['stau_mass'].append(filters[-1].Histo1D(("stau_M",
                                                    f"gen stau_M. tr, {args.names[i]}",
                                                    1000, 0, 500), "stau_mass"))
        hists['dRtaustau'].append(filters[-1].Histo1D(("dRtaustau",
                                                    f"gen dR(tau,stau), {args.names[i]}",
                                                    50, 0, 5.0), "dR_stau_tau"))
        hists['Angle_taustau'].append(filters[-1].Histo1D(("Angle_taustau",
                                                    f"gen Angle(tau,stau), {args.names[i]}",
                                                    100, 0, 3.0), "Angle_taustau"))
        hists['dRjetstau'].append(filters[-1].Histo1D(("dRjetstau",
                                                    f"gen dR(seedjet,stau), {args.names[i]}",
                                                    100, 0, 5.0), "dR_stau_jet"))
        hists['rel_pt'].append(filters[-1].Histo1D(("rel_pt",
                                                    f"(rel_pt, {args.names[i]}",
                                                    150, -2.0, 2.0), "rel_pt"))
        hists['d_mass'].append(filters[-1].Histo1D(("d_mass",
                                                    f"(d_mass, {args.names[i]}",
                                                    100, -5.0, 15.0), "d_mass"))
        hists['dR_tau_jet'].append(filters[-1].Histo1D(("dR_tau_jet",
                                                    f"(dR_tau_jet, {args.names[i]}",
                                                    100, -1.0, 1.0), "dR_tau_jet"))


        
    print('All stats:')
    # allCutsReport = df.Report()
    # allCutsReport.Print()

    canvas = DrawUtils.GetCanvas("canvas_pt")
    DrawUtils.PlotHistList(canvas, hists['vis_pt'],"[GeV]","entries")
    DrawUtils.DrawHeader(canvas, "P^{T}_{vis}(#tau)" , "#tau reco", "c#tau_{0}=1000mm")
    legend = DrawUtils.GetHistTitlesLegend(hists["vis_pt"])
    DrawUtils.DrawLegend(canvas, legend)
    canvas.SaveAs(args.output+"/vis_pt.pdf")

    canvas = DrawUtils.GetCanvas("canvas_eta")
    DrawUtils.PlotHistList(canvas, hists['vis_eta'],"[-]","entries")
    DrawUtils.DrawHeader(canvas, "#eta_{vis}(#tau)" , "#tau reco", "c#tau_{0}=1000mm")
    legend = DrawUtils.GetHistTitlesLegend(hists["vis_eta"])
    DrawUtils.DrawLegend(canvas, legend)
    canvas.SaveAs(args.output+"/vis_eta.pdf")

    canvas = DrawUtils.GetCanvas("canvas_mass")
    DrawUtils.PlotHistList(canvas, hists['vis_mass'],"[-]","entries")
    DrawUtils.DrawHeader(canvas, "M_{vis}(#tau)" , "#tau reco", "c#tau_{0}=1000mm")
    legend = DrawUtils.GetHistTitlesLegend(hists["vis_mass"])
    DrawUtils.DrawLegend(canvas, legend)
    canvas.SaveAs(args.output+"/vis_mass.pdf")

    canvas = DrawUtils.GetCanvas("canvas_displ")
    DrawUtils.PlotHistList(canvas, hists['displ'],"[cm]","entries")
    DrawUtils.DrawHeader(canvas, "d(#tau)" , "#tau reco", "c#tau_{0}=1000mm")
    legend = DrawUtils.GetHistTitlesLegend(hists["displ"])
    DrawUtils.DrawLegend(canvas, legend)
    canvas.SaveAs(args.output+"/displ.pdf")

    canvas = DrawUtils.GetCanvas("canvas_displ_tr")
    DrawUtils.PlotHistList(canvas, hists['displ_tr'], "[cm]","entries")
    DrawUtils.DrawHeader(canvas, "d^{T}(#tau)" , "#tau reco", "c#tau_{0}=1000mm")
    legend = DrawUtils.GetHistTitlesLegend(hists["displ_tr"])
    DrawUtils.DrawLegend(canvas, legend)
    canvas.SaveAs(args.output+"/displ_tr.pdf")

    canvas = DrawUtils.GetCanvas("canvas_stau_mass")
    DrawUtils.PlotHistList(canvas, hists['stau_mass'],"[GeV]","entries")
    DrawUtils.DrawHeader(canvas, "gen m(#tau)" , "#tau reco", "c#tau_{0}=1000mm")
    legend = DrawUtils.GetHistTitlesLegend(hists["stau_mass"])
    DrawUtils.DrawLegend(canvas, legend)
    canvas.SaveAs(args.output+"/stau_mass.pdf")

    canvas = DrawUtils.GetCanvas("canvas_stau_E")
    DrawUtils.PlotHistList(canvas, hists['stau_E'],"[GeV]","entries")
    DrawUtils.DrawHeader(canvas, "gen E(#tau)" , "#tau reco", "c#tau_{0}=1000mm")
    legend = DrawUtils.GetHistTitlesLegend(hists["stau_E"])
    DrawUtils.DrawLegend(canvas, legend)
    canvas.SaveAs(args.output+"/stau_E.pdf")

    canvas = DrawUtils.GetCanvas("canvas_dRtaustau")
    DrawUtils.PlotHistList(canvas, hists['dRtaustau'],"[dR]","entries")
    DrawUtils.DrawHeader(canvas, "dR(tau,stau)" , "#tau reco", "c#tau_{0}=1000mm")
    legend = DrawUtils.GetHistTitlesLegend(hists["dRtaustau"])
    DrawUtils.DrawLegend(canvas, legend)
    canvas.SaveAs(args.output+"/dRtaustau.pdf")

    canvas = DrawUtils.GetCanvas("canvas_Angle_taustau")
    DrawUtils.PlotHistList(canvas, hists['Angle_taustau'],"[rad]","entries")
    DrawUtils.DrawHeader(canvas, "Angle(tau,stau)" , "#tau reco", "c#tau_{0}=1000mm")
    legend = DrawUtils.GetHistTitlesLegend(hists["Angle_taustau"])
    DrawUtils.DrawLegend(canvas, legend)
    canvas.SaveAs(args.output+"/Angle_taustau.pdf")

    canvas = DrawUtils.GetCanvas("canvas_dRjetstau")
    DrawUtils.PlotHistList(canvas, hists['dRjetstau'],"[dR]","entries")
    DrawUtils.DrawHeader(canvas, "dR(ak4jet,stau)" , "#tau reco", "c#tau_{0}=1000mm")
    legend = DrawUtils.GetHistTitlesLegend(hists["dRjetstau"])
    DrawUtils.DrawLegend(canvas, legend)
    canvas.SaveAs(args.output+"/dRjetstau.pdf")

    canvas = DrawUtils.GetCanvas("canvas_rel_pt")
    DrawUtils.PlotHistList(canvas, hists['rel_pt'],"[(jet_pt-vis_pt)/vis_pt]","entries")
    DrawUtils.DrawHeader(canvas, "rel_pt" , "#tau reco", "c#tau_{0}=1000mm")
    legend = DrawUtils.GetHistTitlesLegend(hists["rel_pt"])
    DrawUtils.DrawLegend(canvas, legend)
    canvas.SaveAs(args.output+"/rel_pt.pdf")

    canvas = DrawUtils.GetCanvas("canvas_d_mass")
    DrawUtils.PlotHistList(canvas, hists['d_mass'],"jet_mass-vis_mass","entries")
    DrawUtils.DrawHeader(canvas, "d_mass" , "#tau reco", "c#tau_{0}=1000mm")
    legend = DrawUtils.GetHistTitlesLegend(hists["d_mass"])
    DrawUtils.DrawLegend(canvas, legend)
    canvas.SaveAs(args.output+"/d_mass.pdf")

    canvas = DrawUtils.GetCanvas("canvas_dR_tau_jet")
    DrawUtils.PlotHistList(canvas, hists['dR_tau_jet'],"dR_tau_jet","entries")
    DrawUtils.DrawHeader(canvas, "dR_tau_jet" , "#tau reco", "c#tau_{0}=1000mm")
    legend = DrawUtils.GetHistTitlesLegend(hists["dR_tau_jet"])
    DrawUtils.DrawLegend(canvas, legend)
    canvas.SaveAs(args.output+"/dR_tau_jet.pdf")

    # ROOT.gApplication.Run()
