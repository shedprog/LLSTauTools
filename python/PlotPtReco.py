import ROOT
import sys
import os

if __name__ == "__main__":

    file = ROOT.TFile.Open(str(sys.argv[1]), 'read')
    file2 = ROOT.TFile.Open(str(sys.argv[2]), 'read')

    canvas = ROOT.TCanvas('canvas', '', 1000, 500)
    canvas.Divide(2,1,0,0)

    ROOT.gStyle.SetOptStat(0)

    h2_pt_disp_ = file.Get("h3_pt_disp")
    h2_pt_disp2_ = file2.Get("h3_pt_disp")

    # for disp < 10 cm
    canvas.cd(1)
    legend = ROOT.TLegend(0.6,0.75,1.0,1.0)
    # legend.SetTextSize(5)
    h2_pt_disp_1 = h2_pt_disp_.ProjectionX("h1_1",
                               h2_pt_disp_.GetYaxis().FindFixBin(0.0),
                               h2_pt_disp_.GetYaxis().FindFixBin(5.0))
    h2_pt_disp2_1 = h2_pt_disp2_.ProjectionX("h1_2",
                               h2_pt_disp_.GetYaxis().FindFixBin(0.0),
                               h2_pt_disp_.GetYaxis().FindFixBin(5.0))

    print(h2_pt_disp_1.Integral(), h2_pt_disp2_1.Integral())
    h2_pt_disp2_1.Scale(h2_pt_disp_1.GetEntries()/h2_pt_disp2_1.GetEntries())

    legend.AddEntry(h2_pt_disp_1,str(sys.argv[1]),"l")
    legend.AddEntry(h2_pt_disp2_1,str(sys.argv[2]),"l")

    h2_pt_disp_1.GetXaxis().SetTitle("1 - pt_reco/pt_gen")
    h2_pt_disp2_1.GetXaxis().SetTitle("1 - pt_reco/pt_gen")

    h2_pt_disp_1.SetLineColor(2)
    h2_pt_disp2_1.SetLineColor(4)

    h2_pt_disp_1.SetTitle("< 5cm")
    h2_pt_disp_1.Draw("HIST")
    h2_pt_disp2_1.Draw("HIST SAME")
    legend.Draw("same")

    # for disp > 10 cm
    canvas.cd(2)
    legend2 = ROOT.TLegend(0.6,0.75,1.0,1.0)
    # legend2.SetTextSize(5)
    h2_pt_disp_2 = h2_pt_disp_.ProjectionX("h2_1",
                               h2_pt_disp_.GetYaxis().FindFixBin(5.0),
                               h2_pt_disp_.GetYaxis().FindFixBin(200.0))
    h2_pt_disp2_2 = h2_pt_disp2_.ProjectionX("h2_2",
                               h2_pt_disp_.GetYaxis().FindFixBin(5.0),
                               h2_pt_disp_.GetYaxis().FindFixBin(200.0))

    print(h2_pt_disp_2.Integral(), h2_pt_disp2_2.Integral())
    h2_pt_disp2_2.Scale(h2_pt_disp_2.GetEntries()/h2_pt_disp2_2.GetEntries())

    legend2.AddEntry(h2_pt_disp_2,str(sys.argv[1]),"l")
    legend2.AddEntry(h2_pt_disp2_2,str(sys.argv[2]),"l")

    h2_pt_disp_2.GetXaxis().SetTitle("1 - pt_reco/pt_gen")
    h2_pt_disp2_2.GetXaxis().SetTitle("1 - pt_reco/pt_gen")

    h2_pt_disp_2.SetLineColor(2)
    h2_pt_disp2_2.SetLineColor(4)

    h2_pt_disp_2.SetTitle("> 5cm")
    h2_pt_disp_2.Draw("HIST")
    h2_pt_disp2_2.Draw("HIST SAME")
    legend2.Draw("same")


    canvas.SaveAs('pt_reco_comp.pdf')
