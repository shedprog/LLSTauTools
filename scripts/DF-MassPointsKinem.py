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

# python ./DF-MassPointsKinem.py --paths "/pnfs/desy.de/cms/tier2/store/user/myshched/new-ntuples-tau-pog-v4/SUS-RunIISummer20UL18GEN-stau100_lsp1_ctau1000mm_v4" "/pnfs/desy.de/cms/tier2/store/user/myshched/new-ntuples-tau-pog-v4/SUS-RunIISummer20UL18GEN-stau100_lsp1_ctau100mm_v6" "/pnfs/desy.de/cms/tier2/store/user/myshched/new-ntuples-tau-pog-v4/SUS-RunIISummer20UL18GEN-stau250_lsp1_ctau1000mm_v4" "/pnfs/desy.de/cms/tier2/store/user/myshched/new-ntuples-tau-pog-v4/SUS-RunIISummer20UL18GEN-stau250_lsp1_ctau100mm_v6" "/pnfs/desy.de/cms/tier2/store/user/myshched/new-ntuples-tau-pog-v4/SUS-RunIISummer20UL18GEN-stau400_lsp1_ctau1000mm_v4" "/pnfs/desy.de/cms/tier2/store/user/myshched/new-ntuples-tau-pog-v4/SUS-RunIISummer20UL18GEN-stau400_lsp1_ctau100mm_v6" -na "s#tau 100GeV #tau_{0}=1m" "s#tau 100GeV #tau_{0}=10cm" "s#tau 250GeV #tau_{0}=1m" "s#tau 250GeV #tau_{0}=10cm" "s#tau 400GeV #tau_{0}=1m" "s#tau 400GeV #tau_{0}=10cm" -c "(jet_pt>30)&&(abs(jet_eta)<2.3)&&(genLepton_kind==4)" -N 4 4 4 4 4 4 -o ./output/DF-MassPointsKinem

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
    assert(len(args.paths)==\
           len(args.names))

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
             "dRjetstau"     : []
            }
    # for mstau, mlsp, ctau0 in grid:
    for i, path in enumerate(args.paths):
        files = glob.glob(path + "/**/*.root",recursive=True)
        print("name:", args.names[i], "cuts:", args.cuts[0])
        print("files: ", files[:int(args.number[i])])
        df.append(ROOT.RDataFrame("taus", files[:int(args.number[i])]))

        filters.append(df[-1].Filter(args.cuts[0], args.names[i]))
        # filters[-1] = filters[-1].Filter("","has gen stau")
        # General kinematic check:
        get_kinem = MyFunc.DataFrameFunc.get_gen_info()
        filters[-1] = filters[-1].Define('gentau_info',get_kinem) \
                                 .Define('vis_pt','std::get<0>(gentau_info).Pt()')\
                                 .Define('vis_eta','std::get<0>(gentau_info).Eta()')\
                                 .Define('vis_mass','std::get<0>(gentau_info).mass()')\
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

        hists['vis_pt'].append(filters[-1].Histo1D(("vis_pt",
                                                    f"{args.names[i]}",
                                                    100, 0.0, 800), "vis_pt"))
        hists['vis_eta'].append(filters[-1].Histo1D(("vis_eta",
                                                    f"{args.names[i]}",
                                                    50, -3.0, 3.0), "vis_eta"))
        hists['vis_mass'].append(filters[-1].Histo1D(("vis_mass",
                                                    f"{args.names[i]}",
                                                    50, 0.0, 2.3), "vis_mass"))
        hists['displ'].append(filters[-1].Histo1D(("displ",
                                                    f"{args.names[i]}",
                                                    50, 0, 100), "d"))
        hists['displ_tr'].append(filters[-1].Histo1D(("displ_tr",
                                                    f"{args.names[i]}",
                                                    50, 0, 100), "dt"))
        hists['stau_E'].append(filters[-1].Histo1D(("stau_E",
                                                    f"{args.names[i]}",
                                                    50, 0, 2000), "stau_E"))
        hists['stau_mass'].append(filters[-1].Histo1D(("stau_M",
                                                    f"{args.names[i]}",
                                                    100, 0, 500), "stau_mass"))
        hists['dRtaustau'].append(filters[-1].Histo1D(("dRtaustau",
                                                    f"{args.names[i]}",
                                                    50, 0, 5.0), "dR_stau_tau"))
        hists['Angle_taustau'].append(filters[-1].Histo1D(("Angle_taustau",
                                                    f"{args.names[i]}",
                                                    50, 0, 3.0), "Angle_taustau"))
        hists['dRjetstau'].append(filters[-1].Histo1D(("dRjetstau",
                                                    f"{args.names[i]}",
                                                    50, 0, 5.0), "dR_stau_jet"))
        
    # print('All stats:')
    # for frame in df:
    #     allCutsReport = frame.Report()
    #     allCutsReport.Print()
    # exit()
    canvas = DrawUtils.GetCanvas("canvas_Angle_taustau")
    DrawUtils.PlotHistList(canvas, hists['Angle_taustau'],"#alpha (#tau,s#tau) [rad]","arb. units", rescale=True)
    DrawUtils.DrawHeader(canvas, "Private work (CMS simulation)", "#tau-reco")
    legend = DrawUtils.GetHistTitlesLegend(hists["Angle_taustau"])
    DrawUtils.DrawLegend(canvas, legend)
    canvas.SaveAs(args.output+"/Angle_taustau.pdf")
    
    canvas = DrawUtils.GetCanvas("canvas_pt")
    DrawUtils.PlotHistList(canvas, hists['vis_pt'],"p^{T}_{vis}(#tau) [GeV]","arb. units", rescale=True)
    DrawUtils.DrawHeader(canvas, "Private work (CMS simulation)", "#tau-reco")
    legend = DrawUtils.GetHistTitlesLegend(hists["vis_pt"])
    DrawUtils.DrawLegend(canvas, legend)
    canvas.SaveAs(args.output+"/vis_pt.pdf")

    canvas = DrawUtils.GetCanvas("canvas_eta")
    DrawUtils.PlotHistList(canvas, hists['vis_eta'],"#eta_{vis}(#tau) [-]","arb. units", rescale=True)
    DrawUtils.DrawHeader(canvas, "Private work (CMS simulation)", "#tau-reco")
    legend = DrawUtils.GetHistTitlesLegend(hists["vis_eta"])
    DrawUtils.DrawLegend(canvas, legend)
    canvas.SaveAs(args.output+"/vis_eta.pdf")


    canvas = DrawUtils.GetCanvas("canvas_mass")
    DrawUtils.PlotHistList(canvas, hists['vis_mass'],"mass_{vis}(#tau) [GeV]","arb. units", rescale=True)
    DrawUtils.DrawHeader(canvas, "Private work (CMS simulation)", "#tau-reco")
    legend = DrawUtils.GetHistTitlesLegend(hists["vis_mass"])
    DrawUtils.DrawLegend(canvas, legend)
    canvas.SaveAs(args.output+"/vis_mass.pdf")

    canvas = DrawUtils.GetCanvas("canvas_displ")
    # canvas.SetLogy()
    DrawUtils.PlotHistList(canvas, hists['displ'],"Displacement [cm]","arb. units", rescale=True)
    DrawUtils.DrawHeader(canvas, "Private work (CMS simulation)", "#tau-reco")
    legend = DrawUtils.GetHistTitlesLegend(hists["displ"])
    DrawUtils.DrawLegend(canvas, legend)
    canvas.SaveAs(args.output+"/displ.pdf")

    canvas = DrawUtils.GetCanvas("canvas_displ_tr")
    # canvas.SetLogy()
    DrawUtils.PlotHistList(canvas, hists['displ_tr'], "Transverse displacement [cm]","arb. units", rescale=True)
    DrawUtils.DrawHeader(canvas, "Private work (CMS simulation)", "#tau-reco")
    legend = DrawUtils.GetHistTitlesLegend(hists["displ_tr"])
    DrawUtils.DrawLegend(canvas, legend)
    canvas.SaveAs(args.output+"/displ_tr.pdf")

    canvas = DrawUtils.GetCanvas("canvas_stau_mass")
    DrawUtils.PlotHistList(canvas, hists['stau_mass'],"True mass(#tau)","arb. units", rescale=True)
    DrawUtils.DrawHeader(canvas, "Private work (CMS simulation)", "#tau-reco")
    legend = DrawUtils.GetHistTitlesLegend(hists["stau_mass"])
    DrawUtils.DrawLegend(canvas, legend)
    canvas.SaveAs(args.output+"/stau_mass.pdf")

    canvas = DrawUtils.GetCanvas("canvas_stau_E")
    DrawUtils.PlotHistList(canvas, hists['stau_E'],"#tau energy [GeV]","arb. units", rescale=True)
    DrawUtils.DrawHeader(canvas, "Private work (CMS simulation)", "#tau-reco")
    legend = DrawUtils.GetHistTitlesLegend(hists["stau_E"])
    DrawUtils.DrawLegend(canvas, legend)
    canvas.SaveAs(args.output+"/stau_E.pdf")

    canvas = DrawUtils.GetCanvas("canvas_dRtaustau")
    DrawUtils.PlotHistList(canvas, hists['dRtaustau'],"dR(#tau,s#tau) [-]","arb. units", rescale=True)
    DrawUtils.DrawHeader(canvas, "Private work (CMS simulation)", "#tau-reco")
    legend = DrawUtils.GetHistTitlesLegend(hists["dRtaustau"])
    DrawUtils.DrawLegend(canvas, legend)
    canvas.SaveAs(args.output+"/dRtaustau.pdf")

    canvas = DrawUtils.GetCanvas("canvas_dRjetstau")
    DrawUtils.PlotHistList(canvas, hists['dRjetstau'],"dR(AK4-jet,s#tau) [-]","arb. units", rescale=True)
    DrawUtils.DrawHeader(canvas, "Private work (CMS simulation)", "#tau-reco")
    legend = DrawUtils.GetHistTitlesLegend(hists["dRjetstau"])
    DrawUtils.DrawLegend(canvas, legend)
    canvas.SaveAs(args.output+"/dRjetstau.pdf")

    # ROOT.gApplication.Run()
