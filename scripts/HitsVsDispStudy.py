import ROOT
import sys
import os

if __name__ == "__main__":

    file = ROOT.TFile.Open(str(sys.argv[1]), 'read')
    try:
        os.stat("out_hists")
    except:
        os.mkdir("out_hists")
    filename = os.path.basename(str(sys.argv[1]))

    # transverse
    nHits_tr = file.Get('pixhits_reco_disp_t').ProfileX("profile",1,-1,"i")

    canvas_profile = ROOT.TCanvas("canvas", "Calibration", 1600, 900)
    # ROOT.gStyle.SetOptStat(0)
    canvas_profile.cd()
    canvas_profile.SetGrid()

    nHits_tr.SetTitle("pfCand_nPixelHits for pfCand in RecoTau")
    nHits_tr.GetYaxis().SetTitle("#sum(pfCans_nHits)")
    nHits_tr.GetYaxis().SetRangeUser(4.0, 8.0)
    nHits_tr.GetXaxis().SetTitle("#delta tr vtx [cm]")
    nHits_tr.SetLineColor(2)
    nHits_tr.SetLineWidth(1)
    nHits_tr.Rebin(1)
    nHits_tr.Draw("HIST E")

    canvas_profile.Update()
    canvas_profile.SaveAs("out_hists/"+filename+"_tra.pdf")

    # Absolute
    nHits_abs = file.Get('pixhits_reco_disp').ProfileX("profile",1,-1,"i")

    canvas_profile = ROOT.TCanvas("canvas", "Calibration", 1600, 900)
    # ROOT.gStyle.SetOptStat(0)
    canvas_profile.cd()
    canvas_profile.SetGrid()

    nHits_abs.SetTitle("pfCand_nHits for pfCand in RecoTau")
    nHits_abs.GetYaxis().SetTitle("#sum(pfCans_nHits)")
    nHits_abs.GetXaxis().SetTitle("#delta abs vtx [cm]")
    nHits_abs.GetYaxis().SetRangeUser(4.0, 8.0)
    nHits_abs.SetLineColor(2)
    nHits_abs.SetLineWidth(1)
    nHits_abs.Rebin(1)
    nHits_abs.Draw("HIST E")

    canvas_profile.Update()
    canvas_profile.SaveAs("out_hists/"+filename+"_abs.pdf")
