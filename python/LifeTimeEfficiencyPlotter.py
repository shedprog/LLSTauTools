# This script takes LifeTimeEfficiency.root on input and plot nice plots

import ROOT
import sys

############################ ID
def id_plot(file: ROOT.TFile) -> None:

    canvas = ROOT.TCanvas('canvas', '', 1600, 900)
    ROOT.gStyle.SetOptStat(0);
    hist1 = file.Get('h1_Tau_h_ratio')
    hist2 = file.Get('h1_Tau_h_byLooseDeepTau_ratio')
    hist3 = file.Get('h1_Tau_h_byMediumDeepTau_ratio')
    hist4 = file.Get('h1_Tau_h_byTightDeepTau_ratio')

    hist_pass_all = file.Get('h1_Tau_h_all')
    hist_pass_reco = file.Get('h1_Tau_h_reco')
    hist_pass_DTLoose = file.Get('h1_Tau_h_byLooseDeepTau_reco')
    hist_pass_DTMed = file.Get('h1_Tau_h_byMediumDeepTau_reco')
    hist_pass_DTTight = file.Get('h1_Tau_h_byTightDeepTau_reco')

    hist1.GetXaxis().SetRangeUser(0.,11.)
    hist2.GetXaxis().SetRangeUser(0.,11.)
    hist3.GetXaxis().SetRangeUser(0.,11.)
    hist4.GetXaxis().SetRangeUser(0.,11.)

    hist1.SetMarkerStyle(20)
    hist2.SetMarkerStyle(20)
    hist3.SetMarkerStyle(20)
    hist4.SetMarkerStyle(20)

    hist1.SetMarkerColor(40)
    hist2.SetMarkerColor(41)
    hist3.SetMarkerColor(42)
    hist4.SetMarkerColor(43)

    hist1.GetXaxis().SetTitle("c#tau [mm]")
    hist1.GetYaxis().SetTitle("matched to reco::taus / all hadronic taus")

    hist1.Draw("P")
    hist2.Draw("PSAME")
    hist3.Draw("PSAME")
    hist4.Draw("PSAME")

    legend = ROOT.TLegend(0.6,0.75,0.9,0.9);
    legend.AddEntry(hist1,"No cut on reconstructed tau","p");
    legend.AddEntry(hist2,"reconstructed tau pass LooseDeepTau","p");
    legend.AddEntry(hist3,"reconstructed tau pass MediumDeepTau","p");
    legend.AddEntry(hist4,"reconstructed tau pass TightDeepTau","p");
    legend.Draw();

    legend2 = ROOT.TLegend(0.3,0.75,0.6,0.9);
    legend2.AddEntry("","Hadronic taus: "+str(hist_pass_all.GetEntries()),"");
    legend2.AddEntry("","Matched taus: "+str(hist_pass_reco.GetEntries()),"");
    legend2.AddEntry("","Matched taus + DeepTauAllLoose: "+str(hist_pass_DTLoose.GetEntries()),"");
    legend2.AddEntry("","Matched taus + DeepTauAllMedium: "+str(hist_pass_DTMed.GetEntries()),"");
    legend2.AddEntry("","Matched taus + DeepTauAllTight: "+str(hist_pass_DTTight.GetEntries()),"");
    legend2.Draw();

    canvas.SaveAs('LifeTimeTauEfficiency.pdf')

############################ Reco Pt
def dpt_plot(file: ROOT.TFile) -> None:

    canvas = ROOT.TCanvas('canvas', '', 1600, 900)
    canvas.Divide(4,2,0,0)
    hist1 = file.Get("h1_dpt_0p01and0p05")
    hist2 = file.Get("h1_dpt_0p1and0p5")
    hist3 = file.Get("h1_dpt_1p0")
    hist4 = file.Get("h1_dpt_2p5")
    hist5 = file.Get("h1_dpt_5p0")
    hist6 = file.Get("h1_dpt_7p5")
    hist7 = file.Get("h1_dpt_10p0")

    # gStyle->SetOptStat(1111111);
    # gStyle->SetStatY(0.9);
    # gStyle->SetStatX(0.9);
    ROOT.gStyle.SetStatW(0.4);
    ROOT.gStyle.SetStatH(0.3);

    canvas.cd(1)
    hist1.GetXaxis().SetRangeUser(-200.,400.)
    hist1.GetYaxis().SetRangeUser(0.,27000.)
    hist1.Draw()

    canvas.cd(2)
    hist2.GetXaxis().SetRangeUser(-200.,400.)
    hist2.GetYaxis().SetRangeUser(0.,27000.)
    hist2.Draw()

    canvas.cd(3)
    hist3.GetXaxis().SetRangeUser(-200.,400.)
    hist3.GetYaxis().SetRangeUser(0.,27000.)
    hist3.Draw()

    canvas.cd(4)
    hist4.GetXaxis().SetRangeUser(-200.,400.)
    hist4.GetYaxis().SetRangeUser(0.,27000.)
    hist4.Draw()

    canvas.cd(5)
    hist5.GetXaxis().SetRangeUser(-200.,400.)
    hist5.GetYaxis().SetRangeUser(0.,27000.)
    hist5.Draw()

    canvas.cd(6)
    hist6.GetXaxis().SetRangeUser(-200.,400.)
    hist6.GetYaxis().SetRangeUser(0.,27000.)
    hist6.Draw()

    canvas.cd(7)
    hist7.GetXaxis().SetRangeUser(-200.,400.)
    hist7.GetYaxis().SetRangeUser(0.,27000.)
    hist7.Draw()

    canvas.SaveAs('dpt_reco.pdf')

############################ Reco Eta
def deta_plot(file: ROOT.TFile) -> None:

    canvas = ROOT.TCanvas('canvas', '', 1600, 900)
    canvas.Divide(4,2,0,0)
    hist1 = file.Get("h1_eta_0p01and0p05")
    hist2 = file.Get("h1_eta_0p1and0p5")
    hist3 = file.Get("h1_eta_1p0")
    hist4 = file.Get("h1_eta_2p5")
    hist5 = file.Get("h1_eta_5p0")
    hist6 = file.Get("h1_eta_7p5")
    hist7 = file.Get("h1_eta_10p0")

    # gStyle->SetOptStat(1111111);
    # gStyle->SetStatY(0.9);
    # gStyle->SetStatX(0.9);
    ROOT.gStyle.SetStatW(0.4);
    ROOT.gStyle.SetStatH(0.3);

    canvas.cd(1)
    hist1.GetXaxis().SetRangeUser(-0.05,0.05)
    hist1.GetYaxis().SetRangeUser(0.,32000.)
    hist1.Draw()

    canvas.cd(2)
    hist2.GetXaxis().SetRangeUser(-0.05,0.05)
    hist2.GetYaxis().SetRangeUser(0.,32000.)
    hist2.Draw()

    canvas.cd(3)
    hist3.GetXaxis().SetRangeUser(-0.05,0.05)
    hist3.GetYaxis().SetRangeUser(0.,32000.)
    hist3.Draw()

    canvas.cd(4)
    hist4.GetXaxis().SetRangeUser(-0.05,0.05)
    hist4.GetYaxis().SetRangeUser(0.,32000.)
    hist4.Draw()

    canvas.cd(5)
    hist5.GetXaxis().SetRangeUser(-0.05,0.05)
    hist5.GetYaxis().SetRangeUser(0.,32000.)
    hist5.Draw()

    canvas.cd(6)
    hist6.GetXaxis().SetRangeUser(-0.05,0.05)
    hist6.GetYaxis().SetRangeUser(0.,32000.)
    hist6.Draw()

    canvas.cd(7)
    hist7.GetXaxis().SetRangeUser(-0.05,0.05)
    hist7.GetYaxis().SetRangeUser(0.,32000.)
    hist7.Draw()

    canvas.SaveAs('deta_reco.pdf')

############################ Reco dphi
def dphi_plot(file: ROOT.TFile) -> None:

    canvas = ROOT.TCanvas('canvas', '', 1600, 900)
    canvas.Divide(4,2,0,0)
    hist1 = file.Get("h1_dphi_0p01and0p05")
    hist2 = file.Get("h1_dphi_0p1and0p5")
    hist3 = file.Get("h1_dphi_1p0")
    hist4 = file.Get("h1_dphi_2p5")
    hist5 = file.Get("h1_dphi_5p0")
    hist6 = file.Get("h1_dphi_7p5")
    hist7 = file.Get("h1_dphi_10p0")

    # gStyle->SetOptStat(1111111);
    # gStyle->SetStatY(0.9);
    # gStyle->SetStatX(0.9);
    ROOT.gStyle.SetStatW(0.4);
    ROOT.gStyle.SetStatH(0.3);

    canvas.cd(1)
    hist1.GetXaxis().SetRangeUser(-0.05,0.05)
    hist1.GetYaxis().SetRangeUser(0.,32000.)
    hist1.Draw()

    canvas.cd(2)
    hist2.GetXaxis().SetRangeUser(-0.05,0.05)
    hist2.GetYaxis().SetRangeUser(0.,32000.)
    hist2.Draw()

    canvas.cd(3)
    hist3.GetXaxis().SetRangeUser(-0.05,0.05)
    hist3.GetYaxis().SetRangeUser(0.,32000.)
    hist3.Draw()

    canvas.cd(4)
    hist4.GetXaxis().SetRangeUser(-0.05,0.05)
    hist4.GetYaxis().SetRangeUser(0.,32000.)
    hist4.Draw()

    canvas.cd(5)
    hist5.GetXaxis().SetRangeUser(-0.05,0.05)
    hist5.GetYaxis().SetRangeUser(0.,32000.)
    hist5.Draw()

    canvas.cd(6)
    hist6.GetXaxis().SetRangeUser(-0.05,0.05)
    hist6.GetYaxis().SetRangeUser(0.,32000.)
    hist6.Draw()

    canvas.cd(7)
    hist7.GetXaxis().SetRangeUser(-0.05,0.05)
    hist7.GetYaxis().SetRangeUser(0.,32000.)
    hist7.Draw()

    canvas.SaveAs('dphi_reco.pdf')

########################### Reco Pt
def dmass_plot(file: ROOT.TFile) -> None:

    canvas = ROOT.TCanvas('canvas', '', 1600, 900)
    canvas.Divide(4,2,0,0)
    hist1 = file.Get("h1_dm_0p01and0p05")
    hist2 = file.Get("h1_dm_0p1and0p5")
    hist3 = file.Get("h1_dm_1p0")
    hist4 = file.Get("h1_dm_2p5")
    hist5 = file.Get("h1_dm_5p0")
    hist6 = file.Get("h1_dm_7p5")
    hist7 = file.Get("h1_dm_10p0")

    # gStyle->SetOptStat(1111111);
    # gStyle->SetStatY(0.9);
    # gStyle->SetStatX(0.9);
    ROOT.gStyle.SetStatW(0.4);
    ROOT.gStyle.SetStatH(0.3);

    canvas.cd(1)
    hist1.GetXaxis().SetRangeUser(-0.5,2.5)
    hist1.GetYaxis().SetRangeUser(0.,160000.)
    hist1.Draw()

    canvas.cd(2)
    hist2.GetXaxis().SetRangeUser(-0.5,2.5)
    hist2.GetYaxis().SetRangeUser(0.,160000.)
    hist2.Draw()

    canvas.cd(3)
    hist3.GetXaxis().SetRangeUser(-0.5,2.5)
    hist3.GetYaxis().SetRangeUser(0.,160000.)
    hist3.Draw()

    canvas.cd(4)
    hist4.GetXaxis().SetRangeUser(-0.5,2.5)
    hist4.GetYaxis().SetRangeUser(0.,160000.)
    hist4.Draw()

    canvas.cd(5)
    hist5.GetXaxis().SetRangeUser(-0.5,2.5)
    hist5.GetYaxis().SetRangeUser(0.,160000.)
    hist5.Draw()

    canvas.cd(6)
    hist6.GetXaxis().SetRangeUser(-0.5,2.5)
    hist6.GetYaxis().SetRangeUser(0.,160000.)
    hist6.Draw()

    canvas.cd(7)
    hist7.GetXaxis().SetRangeUser(-0.5,2.5)
    hist7.GetYaxis().SetRangeUser(0.,160000.)
    hist7.Draw()

    canvas.SaveAs('dmass_reco.pdf')

file = ROOT.TFile.Open(str(sys.argv[1]), 'read')
dpt_plot(file)
deta_plot(file)
dphi_plot(file)
dmass_plot(file)
id_plot(file)
file.Close()
