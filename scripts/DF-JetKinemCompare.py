import ROOT
import sys
import argparse
import glob

sys.path.append("..")
import python.DrawUtils as DrawUtils
import python.Functions as MyFunc

ROOT.gInterpreter.Declare("#include \"../inc/GenLepton.h\"")

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
    args = parser.parse_args()
    assert(len(args.paths)==\
           len(args.names)==\
           len(args.cuts))

    df = []
    filters = []
    hists = {"pt":[], "eta":[]}
    ROOT.EnableImplicitMT(10)
    for i, path in enumerate(args.paths):
        files = glob.glob(path +"/*.root")
        print("name:",args.names[i],"cuts:",args.cuts[i])
        df.append(ROOT.RDataFrame("taus", files[:int(args.number[i])]))
        filters.append(df[-1].Filter(args.cuts[i], args.names[i]))
        hists["pt"].append(filters[-1].Histo1D(("pt",args.names[i], 200, 0.0, 800), "jet_pt"))
        hists["eta"].append(filters[-1].Histo1D(("eta",args.names[i], 60, -2.5, 2.5), "jet_eta"))

    canvas_pt = DrawUtils.GetCanvas("canvas_pt")
    DrawUtils.PlotHistList(canvas_pt, hists["pt"],"[GeV]","entries")
    DrawUtils.DrawHeader(canvas_pt, "P^{T}(jet)" , "#tau reco", "c#tau_{0}=1000mm")
    DrawUtils.DrawLegend(canvas_pt, DrawUtils.GetHistTitlesLegend(hists["pt"]))

    canvas_eta = DrawUtils.GetCanvas("canvas_eta")
    DrawUtils.PlotHistList(canvas_eta, hists["eta"],"[GeV]","entries")
    DrawUtils.DrawHeader(canvas_eta, "eta(jet)" , "#tau reco", "c#tau_{0}=1000mm")
    DrawUtils.DrawLegend(canvas_eta, DrawUtils.GetHistTitlesLegend(hists["eta"]))

    ROOT.gApplication.Run()