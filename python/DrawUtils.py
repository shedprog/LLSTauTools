import ROOT
from typing import List

def GetCanvas(name : str) -> ROOT.TCanvas:
    c = ROOT.TCanvas(name, name, 1000, 1000)
    SetMyStyle()
    return c

def PlotHistList(canvas : ROOT.TCanvas,
                 hist_list : List[ROOT.TH1],
                 x_axis_title: str,
                 y_axis_title: str) -> None:
    '''
    Ploting List of histograms
    on the single pad
    '''
    canvas.cd()
    max_y = 0
    for i, h in enumerate(hist_list):
        max_y = max(max_y, h.GetMaximum())
        h.GetXaxis().SetTitle(x_axis_title)
        h.GetYaxis().SetTitle(y_axis_title)
        h.SetLineColor(ColorIterator(i))
        h.SetLineWidth(3)
        h.Draw("same") if i!=0 else h.Draw()
    hist_list[0].SetMaximum(max_y+0.1*max_y) # to fix ranges 
    canvas.Modified()
    canvas.Update()
    
def GetHistTitlesLegend(hist_list : List[ROOT.TH1]) -> ROOT.TLegend:
    legend = ROOT.TLegend(0.6, 0.7, 0.9, 0.9)
    for hist in hist_list:
        t = hist.GetTitle()
        legend.AddEntry(hist.GetValue(), t, "l")
    return legend

def DrawLegend(canvas : ROOT.TCanvas,
               legend : ROOT.TLegend):
    canvas.cd()
    legend.Draw()
    canvas.Modified()
    canvas.Update()

def SetMyStyle() -> None:
    '''
    Style options
    '''
    # ROOT.gROOT.SetBatch()
    ROOT.gROOT.ForceStyle(ROOT.kTRUE)

    ROOT.TGaxis.SetExponentOffset(-0.07, 0.0035, "y")
    ROOT.gStyle.SetLegendBorderSize(0)
    ROOT.gStyle.SetFillStyle(0)
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetOptTitle(0)

    ROOT.gStyle.SetHistLineWidth(3)
    ROOT.gStyle.SetHistLineStyle(1)

def DrawHeader(pad : ROOT.TPad,
               titleText : str,
               cmsText : str, 
               lumiText : str):
    pad.cd()

    padWidth = pad.GetWw() * pad.GetWNDC()
    padHeight = pad.GetWh() * pad.GetHNDC()

    textSize = 30./padWidth if padHeight > padWidth else 30./padHeight

    channelLine = ROOT.TLatex()
    channelLine.SetTextFont(42)
    channelLine.SetTextSize(textSize)
    channelLine.DrawLatexNDC(0.11, 0.92, titleText)

    cmsLine = ROOT.TLatex()
    cmsLine.SetTextFont(62)
    cmsLine.SetTextSize(textSize)
    cmsLine.DrawLatexNDC(0.33, 0.92, "CMS")

    cmsTextLine = ROOT.TLatex()
    cmsTextLine.SetTextFont(52)
    cmsTextLine.SetTextSize(textSize)
    cmsTextLine.DrawLatexNDC(0.4, 0.92, cmsText)

    #CMS Work in Progres and Lumi information
    lumiLine = ROOT.TLatex()
    lumiLine.SetTextFont(42)
    lumiLine.SetTextSize(textSize)
    lumiLine.DrawLatexNDC(0.64, 0.92, lumiText)

    pad.Modified()
    pad.Update()

def ColorIterator(index : int) -> int:
    # kWhite  = 0,   kBlack  = 1,   kGray    = 920,  kRed    = 632,  kGreen  = 416,
    # kBlue   = 600, kYellow = 400, kMagenta = 616,  kCyan   = 432,  kOrange = 800,
    # kSpring = 820, kTeal   = 840, kAzure   =  860, kViolet = 880,  kPink   = 900
    cs = 1
    colow_wheel = [ cs + ROOT.kBlue,
                    cs + ROOT.kRed,
                    cs + ROOT.kGreen,
                    cs + ROOT.kMagenta,
                    cs + ROOT.kYellow,
                    cs + ROOT.kCyan ]
    color_idx =  colow_wheel +\
                [x - 5 for x in colow_wheel] +\
                [x - 10 for x in colow_wheel]
    return color_idx[index]