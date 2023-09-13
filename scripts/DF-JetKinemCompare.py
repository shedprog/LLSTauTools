import ROOT
import sys
import argparse
import glob
import os

sys.path.append("..")
import python.DrawUtils as DrawUtils
import python.Functions as MyFunc

ROOT.gInterpreter.Declare("#include \"../inc/GenLepton.h\"")

ROOT.gROOT.SetBatch(True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=\
    '''
    The following script is compering
    jet properties for BigNtuple
    created under the TauMLTools framework
    ''')
    parser.add_argument('-p','--paths', nargs='+', help='Full path to the datasets', required=True)
    parser.add_argument('-na','--names', nargs='+', help='Name of the cooresponding DataSet', required=True)
    parser.add_argument('-c','--cuts', nargs='+', help='Cuts for the cooresponding DataSet', required=True)
    parser.add_argument('-N','--number', nargs='+', help='Number of files to analyse', required=True)
    parser.add_argument('-o','--output', help='folder for the plot outputs', required=True)
    args = parser.parse_args()
    assert(len(args.paths)==\
           len(args.names)==\
           len(args.cuts))

    if not os.path.exists(args.output): os.makedirs(args.output)

    df = []
    filters = []
    hists = {"pt":[], "eta":[], "rho":[]}
    ROOT.EnableImplicitMT(10)
    print("Starting RDataFrame:")
    for i, path in enumerate(args.paths):
        files = glob.glob(path +"/**/*.root", recursive=True)
        print("name:", args.names[i], "cuts:", args.cuts[i])
        df.append(ROOT.RDataFrame("taus", files[:int(args.number[i])]))
        filters.append(df[-1].Filter(args.cuts[i], args.names[i]))
        hists["pt"].append(filters[-1].Histo1D(("pt",args.names[i], 100, 0.0, 1000), "jet_pt"))
        hists["eta"].append(filters[-1].Histo1D(("eta",args.names[i], 100, -2.5, 2.5), "jet_eta"))
        hists["rho"].append(filters[-1].Histo1D(("rho",args.names[i], 100, 0, 100), "rho"))

    canvas_pt = DrawUtils.GetCanvas("canvas_pt")
    DrawUtils.PlotHistList(canvas_pt, hists["pt"],"[GeV]","entries")
    DrawUtils.DrawHeader(canvas_pt, "P^{T}(jet)" , "#tau reco", "c#tau_{0}=1000mm")
    legend = DrawUtils.GetHistTitlesLegend(hists["pt"])
    DrawUtils.DrawLegend(canvas_pt, legend)
    canvas_pt.SaveAs(args.output+"/var_pt.pdf")

    canvas_eta = DrawUtils.GetCanvas("canvas_eta")
    DrawUtils.PlotHistList(canvas_eta, hists["eta"],"[-]","entries")
    DrawUtils.DrawHeader(canvas_eta, "#eta(jet)" , "#tau reco", "c#tau_{0}=1000mm")
    legend = DrawUtils.GetHistTitlesLegend(hists["eta"])
    DrawUtils.DrawLegend(canvas_eta, legend)
    canvas_eta.SaveAs(args.output+"/var_eta.pdf")

    canvas_pt = DrawUtils.GetCanvas("canvas_pt_log")
    DrawUtils.PlotHistList(canvas_pt, hists["pt"],"[GeV]","entries", log=True)
    DrawUtils.DrawHeader(canvas_pt, "P^{T}(jet)" , "#tau reco", "c#tau_{0}=1000mm")
    legend = DrawUtils.GetHistTitlesLegend(hists["pt"])
    DrawUtils.DrawLegend(canvas_pt, legend)
    canvas_pt.SaveAs(args.output+"/var_pt_log.pdf")

    canvas_eta = DrawUtils.GetCanvas("canvas_eta_log")
    DrawUtils.PlotHistList(canvas_eta, hists["eta"],"[-]","entries", log=True)
    DrawUtils.DrawHeader(canvas_eta, "#eta(jet)" , "#tau reco", "c#tau_{0}=1000mm")
    legend = DrawUtils.GetHistTitlesLegend(hists["eta"])
    DrawUtils.DrawLegend(canvas_eta, legend)
    canvas_eta.SaveAs(args.output+"/var_eta_log.pdf")

    canvas_rho = DrawUtils.GetCanvas("canvas_rho")
    DrawUtils.PlotHistList(canvas_rho, hists["rho"],"[-]","entries")
    DrawUtils.DrawHeader(canvas_rho, "Energy density" , "#tau reco", "c#tau_{0}=1000mm")
    legend = DrawUtils.GetHistTitlesLegend(hists["rho"])
    DrawUtils.DrawLegend(canvas_rho, legend)
    canvas_rho.SaveAs(args.output+"/var_rho.pdf")

    # ROOT.gApplication.Run()