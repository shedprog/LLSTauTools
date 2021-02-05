# This script takes LifeTimeEfficiency.root on input and plot nice plots

import ROOT
import sys

file = ROOT.TFile.Open(str(sys.argv[1]), 'read')
canvas = ROOT.TCanvas('canvas', '', 1000, 500)
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

hist1.GetXaxis().SetTitle("c#tau [cm]")
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
file.Close()
