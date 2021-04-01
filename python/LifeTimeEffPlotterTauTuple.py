import ROOT
import sys
import os

def createRatio(h1, h2, name):
    h3 = h1.Clone(name)
    h3.SetLineColor(ROOT.kBlack)
    h3.SetMarkerStyle(21)
    h3.SetTitle("")
    h3.SetMinimum(0.0)
    h3.SetMaximum(1.0)
    # Set up plot for markers and errors
    h3.Sumw2()
    h3.SetStats(0)
    h3.Divide(h2)

    # Adjust y-axis settings
    y = h3.GetYaxis()
    y.SetTitle("ratio")
    y.SetNdivisions(505)
    y.SetTitleSize(20)
    y.SetTitleFont(43)
    y.SetTitleOffset(1.55)
    y.SetLabelFont(43)
    y.SetLabelSize(15)

    # Adjust x-axis settings
    x = h3.GetXaxis()
    x.SetTitleSize(20)
    x.SetTitleFont(43)
    x.SetTitleOffset(4.0)
    x.SetLabelFont(43)
    x.SetLabelSize(15)

    return h3

def createCanvasPads():
    c = ROOT.TCanvas("c", "canvas", 800, 800)
    # Upper histogram plot is pad1
    pad1 = ROOT.TPad("pad1", "pad1", 0, 0.3, 1, 1.0)
    pad1.SetBottomMargin(0)  # joins upper and lower plot
    pad1.SetGridx()
    pad1.Draw()
    # Lower ratio plot is pad2
    c.cd()  # returns to main canvas before defining pad2
    pad2 = ROOT.TPad("pad2", "pad2", 0, 0.05, 1, 0.3)
    pad2.SetTopMargin(0)  # joins upper and lower plot
    pad2.SetBottomMargin(0.2)
    pad2.SetGridx()
    pad2.Draw()

    return c, pad1, pad2

if __name__ == "__main__":

    file = ROOT.TFile.Open(str(sys.argv[1]), 'read')
    try:
        os.stat("out")
    except:
        os.mkdir("out")

    # Reco efficiency Plot ----------------------------->

    h1_Tau_h_all = file.Get('h1_Tau_h_all').ProjectionX()
    h1_Tau_h_reco = file.Get('h1_Tau_h_reco').ProjectionX()
    h1_Tau_h_all_t = file.Get('h1_Tau_h_all_t').ProjectionX() # transverse plane displacement
    h1_Tau_h_reco_t = file.Get('h1_Tau_h_reco_t').ProjectionX() # transverse plane displacement

    # h1_Tau_h_all.GetXaxis().SetRangeUser(0.,150.)
    # h1_Tau_h_reco.GetXaxis().SetRangeUser(0.,150.)
    # h1_Tau_h_all_t.GetXaxis().SetRangeUser(0.,150.)
    # h1_Tau_h_reco_t.GetXaxis().SetRangeUser(0.,150.)

    # h1_Tau_h_all.SetMinimum(0.9)
    # h1_Tau_h_reco.SetMinimum(0.9)
    # h1_Tau_h_all_t.SetMinimum(0.9)
    # h1_Tau_h_reco_t.SetMinimum(0.9)

    h1_Tau_h_all.Rebin(5)
    h1_Tau_h_reco.Rebin(5)
    h1_Tau_h_all_t.Rebin(5)
    h1_Tau_h_reco_t.Rebin(5)

    # abs delta vertex
    h1_ratio_reco = createRatio(h1_Tau_h_reco, h1_Tau_h_all,"h3")

    canvas_eff, pad1, pad2 = createCanvasPads()
    ROOT.gStyle.SetOptStat(0)
    h1_Tau_h_all.SetLineColor(4)
    h1_Tau_h_all.GetYaxis().SetTitle("entries")
    h1_Tau_h_reco.SetLineColor(2)
    pad1.cd()
    pad1.SetLogy();
    h1_Tau_h_all.Draw()
    h1_Tau_h_reco.Draw("same")
    pad2.cd()
    h1_ratio_reco.GetXaxis().SetTitle("#delta vtx [cm]")
    h1_ratio_reco.Draw()
    canvas_eff.SaveAs('out/effdisplacement.pdf')

    # Reco transverse efficiency Plot ----------------------------->
    h1_ratio_reco_t = createRatio(h1_Tau_h_reco_t, h1_Tau_h_all_t, "h3")

    canvas_eff, pad1, pad2 = createCanvasPads()
    ROOT.gStyle.SetOptStat(0)
    h1_Tau_h_all_t.SetLineColor(4)
    h1_Tau_h_all_t.GetYaxis().SetTitle("entries")
    h1_Tau_h_reco_t.SetLineColor(2)
    pad1.cd()
    pad1.SetLogy();
    h1_Tau_h_all_t.Draw()
    h1_Tau_h_reco_t.Draw("same")
    pad2.cd()
    h1_ratio_reco_t.GetXaxis().SetTitle("#delta transverse vtx [cm]")
    h1_ratio_reco_t.Draw()
    canvas_eff.SaveAs('out/effdisplacement_t.pdf')

    # Reco efficiency Plot by pt bins ----------------------------->
    canvas = ROOT.TCanvas('canvas', '', 500, 500)
    legend = ROOT.TLegend(0.5,0.7,0.9,0.9)
    # pt_bins = [0, 20, 40, 60, 80, 100, 120, 140]
    # pt_bins = [0, 20, 40]
    pt_bins = [0, 20, 40, 60, 80, 1000]

    h1_Tau_pt_reco = []
    h1_Tau_pt_all = []
    h1_ratio_reco = []
    for i, pt in enumerate(pt_bins[:-1]):

        h1_Tau_pt_reco.append(file.Get('h1_Tau_genpt_reco').Clone("h_genpt_reco"+str(i)))
        h1_Tau_pt_reco[-1].Rebin(20)
        h1_Tau_pt_reco[-1] = h1_Tau_pt_reco[-1].ProjectionX("h_reco"+str(i),
                         h1_Tau_pt_reco[-1].GetYaxis().FindFixBin(pt_bins[i]),
                         h1_Tau_pt_reco[-1].GetYaxis().FindFixBin(pt_bins[i+1]))

        h1_Tau_pt_all.append(file.Get('h1_Tau_genpt_all').Clone("h_genpt_all"+str(i)))
        h1_Tau_pt_all[-1].Rebin(20)
        h1_Tau_pt_all[-1] = h1_Tau_pt_all[-1].ProjectionX("h_all"+str(i),
                         h1_Tau_pt_all[-1].GetYaxis().FindFixBin(pt_bins[i]),
                         h1_Tau_pt_all[-1].GetYaxis().FindFixBin(pt_bins[i+1]))

        h1_ratio_reco.append(createRatio(h1_Tau_pt_reco[-1],
                                         h1_Tau_pt_all[-1],
                                         "h_ratio"+str(i)))
        print("Reco Entries: ", h1_Tau_pt_reco[-1].Integral())
        h1_ratio_reco[-1].SetLineColor(2+i)
        h1_ratio_reco[-1].SetMarkerStyle(0)
        h1_ratio_reco[-1].SetLineWidth(2)
        if i==0:
            h1_ratio_reco[-1].Draw("HIST E")
        else:
            h1_ratio_reco[-1].Draw("HIST E SAME")

        legend.AddEntry(h1_ratio_reco[-1],str(pt_bins[i])+"GeV<pt<"+str(pt_bins[i+1])+"GeV","l")
    legend.Draw("same")
    canvas.SaveAs('out/efficiency_ptbins.pdf')

    # Reco decay mode Plots ----------------------------->
    devide_field = 6
    labels = ['Other','#pi', '#pi#pi^{0}s', '3#pi', '3#pi#pi^{0}s', '']

    h3_dm_disp = file.Get("h3_dm_disp")
    zn_bins = h3_dm_disp.GetZaxis().GetNbins()
    step = int(zn_bins/devide_field/2)

    canvas = ROOT.TCanvas('canvas', '', 1000, 500)
    # ROOT.gStyle.SetTextSize(22);
    ROOT.gStyle.SetOptStat(11);
    canvas.Divide(int(devide_field/2),2,0,0)

    h3_dm_disp_ = []
    dm_projection = []
    for i in range(devide_field):
        h3_dm_disp_.append(h3_dm_disp.Clone("h3_"+str(i)))
        h3_dm_disp_[i].GetZaxis().SetRange(step*i+1, step*(i+1))
        dm_projection.append(h3_dm_disp_[i].Project3D("xy").Clone("h2_"+str(i)))
        for y_bin in range(1, dm_projection[i].GetYaxis().GetNbins()+1):
            dm_projection[i].GetYaxis().SetBinLabel(y_bin, labels[y_bin-1])
        for x_bin in range(1, dm_projection[i].GetXaxis().GetNbins()+1):
            dm_projection[i].GetXaxis().SetBinLabel(x_bin, labels[x_bin-1])
        canvas.cd(i+1)
        dm_projection[i].SetTitle(str(h3_dm_disp_[i].GetZaxis().GetBinLowEdge(step*i+1)) + "-" +
                                  str(h3_dm_disp_[i].GetZaxis().GetBinUpEdge(step*(i+1))))
        dm_projection[i].GetXaxis().SetLabelSize(0.07);
        dm_projection[i].GetYaxis().SetLabelSize(0.07);
        dm_projection[i].Draw("coltext")

    canvas.SaveAs('out/dm_migration.pdf')

    # Reco pt  ----------------------------->
    canvas = ROOT.TCanvas('canvas', '', 500, 500)
    legend = ROOT.TLegend(0.5,0.7,0.9,0.9)

    h2_pt = file.Get("h1_Tau_genpt_all").ProjectionY()
    h2_pt.GetXaxis().SetTitle("pt_gen")
    h2_pt_r = file.Get("h1_Tau_genpt_reco").ProjectionY()
    h2_pt_r.GetXaxis().SetTitle("pt_gen")

    legend.AddEntry(h2_pt,"all","l")
    legend.AddEntry(h2_pt_r,"reco","l")

    h2_pt.Draw()
    h2_pt_r.Draw("same")
    legend.Draw("same")

    canvas.SaveAs('out/genpt.pdf')

    # Reco pt plot ----------------------------->
    canvas = ROOT.TCanvas('canvas', '', 500, 500)
    h2_pt_disp = file.Get("h3_pt_disp").ProjectionX()
    h2_pt_disp.GetXaxis().SetTitle("1 - pt_reco/pt_gen")
    h2_pt_disp.Draw()
    canvas.SaveAs('out/pt_reco_comp.pdf')

    file.Close()
