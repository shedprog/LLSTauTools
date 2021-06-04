import ROOT
import sys
import os
from array import array
ROOT.gROOT.SetBatch(True)


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
    c = ROOT.TCanvas("c", "canvas", 1000, 1000)
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

    # setting log binning
    # limits_cm = [0.0, 100.0]
    # n_bins = 10
    # disp_edge_cm = sorted([0.1, 0.2, 0.5, 1.0, 2.0, 5.0, 10.0, 20.0, 40.0, 60.0, 80.0, 100.0])
    # bin_edges = array('d',disp_edge_cm)
    # n = len(bin_edges)-1

    # Reco efficiency Plot ----------------------------->

    h1_Tau_h_all = file.Get('h1_Tau_h_all').ProjectionX()
    h1_Tau_h_reco = file.Get('h1_Tau_h_reco').ProjectionX()
    # transverse plane displacement
    h1_Tau_h_all_t = file.Get('h1_Tau_h_all_t').ProjectionX()
    # transverse plane displacement
    h1_Tau_h_reco_t = file.Get('h1_Tau_h_reco_t').ProjectionX()

    # h1_Tau_h_all_ = file.Get('h1_Tau_h_all').ProjectionX()
    # h1_Tau_h_reco_ = file.Get('h1_Tau_h_reco').ProjectionX()
    # h1_Tau_h_all_t_ = file.Get('h1_Tau_h_all_t').ProjectionX() # transverse plane displacement
    # h1_Tau_h_reco_t_ = file.Get('h1_Tau_h_reco_t').ProjectionX() # transverse plane displacement

    # h1_Tau_h_all.GetXaxis().SetLimits(0,10)
    # h1_Tau_h_reco.GetXaxis().SetLimits(0,10)
    # h1_Tau_h_all_t.GetXaxis().SetLimits(0,10)
    # h1_Tau_h_reco_t.GetXaxis().SetLimits(0,10)

    # h1_Tau_h_all.SetMinimum(0.9)
    # h1_Tau_h_reco.SetMinimum(0.9)
    # h1_Tau_h_all_t.SetMinimum(0.9)
    # h1_Tau_h_reco_t.SetMinimum(0.9)

    MergeBin = 2
    h1_Tau_h_all.Rebin(MergeBin)
    h1_Tau_h_reco.Rebin(MergeBin)
    h1_Tau_h_all_t.Rebin(MergeBin)
    h1_Tau_h_reco_t.Rebin(MergeBin)

    # h1_Tau_h_all = h1_Tau_h_all_.Rebin(n, "h1_Tau_h_all_new", bin_edges)
    # h1_Tau_h_reco = h1_Tau_h_reco_.Rebin(n, "h1_Tau_h_reco_new", bin_edges)
    # h1_Tau_h_all_t = h1_Tau_h_all_t_.Rebin(n, "h1_Tau_h_all_t_new", bin_edges)
    # h1_Tau_h_reco_t = h1_Tau_h_reco_t_.Rebin(n, "h1_Tau_h_reco_t_new", bin_edges)

    h1_Tau_h_all.GetXaxis().SetRangeUser(0., 100.)
    h1_Tau_h_reco.GetXaxis().SetRangeUser(0., 100.)
    h1_Tau_h_all_t.GetXaxis().SetRangeUser(0., 100.)
    h1_Tau_h_reco_t.GetXaxis().SetRangeUser(0., 100.)

    # abs delta vertex
    h1_ratio_reco = createRatio(h1_Tau_h_reco, h1_Tau_h_all, "h3")

    canvas_eff, pad1, pad2 = createCanvasPads()
    ROOT.gStyle.SetOptStat(0)
    h1_Tau_h_all.SetLineColor(4)
    h1_Tau_h_all.GetYaxis().SetTitle("entries")
    h1_Tau_h_reco.SetLineColor(2)
    pad1.cd()
    pad1.SetLogy()
    pad1.SetLogx()
    h1_Tau_h_all.SetMinimum(0.5)
    h1_Tau_h_reco.SetMinimum(0.5)
    h1_Tau_h_all.Draw()
    h1_Tau_h_reco.Draw("same")

    pad2.cd()
    pad2.SetLogx()
    h1_ratio_reco.SetMarkerStyle(2)
    h1_ratio_reco.SetMarkerSize(1)
    h1_ratio_reco.GetXaxis().SetTitle("displacement [cm]")
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
    pad1.SetLogy()
    pad1.SetLogx()
    h1_Tau_h_all_t.SetMinimum(0.5)
    h1_Tau_h_reco_t.SetMinimum(0.5)
    h1_Tau_h_all_t.Draw()
    h1_Tau_h_reco_t.Draw("same")
    pad2.cd()
    pad2.SetLogx()
    h1_ratio_reco_t.SetMarkerStyle(2)
    h1_ratio_reco_t.SetMarkerSize(1)
    h1_ratio_reco_t.GetXaxis().SetTitle("transverse displacement [cm]")
    h1_ratio_reco_t.Draw()
    canvas_eff.SaveAs('out/effdisplacement_t.pdf')

    # Reco efficiency Plot by pt bins ----------------------------->
    canvas = ROOT.TCanvas('canvas', '', 1600, 900)
    legend = ROOT.TLegend(0.6, 0.7, 0.9, 0.9)
    # pt_bins = [0, 20, 40, 60, 80, 100, 120, 140]
    # pt_bins = [0, 20, 40]
    pt_bins = [0, 20, 40, 60, 80, 200, 1000]

    h1_Tau_pt_reco = []
    h1_Tau_pt_all = []
    h1_ratio_reco = []

    rebin_size = 10

    for i, pt in enumerate(pt_bins[:-1]):

        h1_Tau_pt_reco.append(
            file.Get('h1_Tau_genpt_reco_t').Clone("h_genpt_reco"+str(i)))
        h1_Tau_pt_reco[-1].Rebin(rebin_size)
        h1_Tau_pt_reco[-1] = h1_Tau_pt_reco[-1].ProjectionX("h_reco"+str(i),
                                                            h1_Tau_pt_reco[-1].GetYaxis(
        ).FindFixBin(pt_bins[i]),
            h1_Tau_pt_reco[-1].GetYaxis().FindFixBin(pt_bins[i+1]))

        h1_Tau_pt_all.append(
            file.Get('h1_Tau_genpt_all_t').Clone("h_genpt_all"+str(i)))
        h1_Tau_pt_all[-1].Rebin(rebin_size)
        h1_Tau_pt_all[-1] = h1_Tau_pt_all[-1].ProjectionX("h_all"+str(i),
                                                          h1_Tau_pt_all[-1].GetYaxis(
        ).FindFixBin(pt_bins[i]),
            h1_Tau_pt_all[-1].GetYaxis().FindFixBin(pt_bins[i+1]))

        # h1_ratio_reco.append(createRatio(h1_Tau_pt_reco[-1],
        #                                  h1_Tau_pt_all[-1],
        #                                  "h_ratio"+str(i)))
        h1_ratio_reco.append(h1_Tau_pt_reco[-1].Clone("h1_Tau_pt_reco"+str(i)))

        h1_ratio_reco[-1].SetMinimum(0.0)
        h1_ratio_reco[-1].SetMaximum(1.0)
        h1_ratio_reco[-1].Sumw2()
        h1_ratio_reco[-1].SetStats(0)
        
        h1_ratio_reco[-1].Divide(h1_Tau_pt_all[-1])

        h1_ratio_reco[-1].GetXaxis().SetRangeUser(0., 100.)
        print("Reco Entries: ", h1_Tau_pt_reco[-1].Integral())
        h1_ratio_reco[-1].SetMaximum(1.5)
        h1_ratio_reco[-1].GetXaxis().SetTitle("transverse displacement [cm]")
        h1_ratio_reco[-1].GetYaxis().SetTitle("reco efficiency")
        h1_ratio_reco[-1].SetLineColor(2+i)
        h1_ratio_reco[-1].SetMarkerStyle(0)
        h1_ratio_reco[-1].SetLineWidth(1)

        if i == 0:
            h1_ratio_reco[-1].Draw("HIST E")
        else:
            h1_ratio_reco[-1].Draw("HIST E SAME")

        legend.AddEntry(
            h1_ratio_reco[-1], str(pt_bins[i])+"GeV<pt<"+str(pt_bins[i+1])+"GeV", "l")
    legend.Draw("same")
    canvas.SaveAs('out/efficiency_ptbins_t.pdf')

    # Reco decay mode Plots ----------------------------->

    def normilize_xaxis(input_h: ROOT.TH2) -> ROOT.TH2:
        normilized_h = input_h.Clone()
        projection = input_h.ProjectionX()
        # print("projection:", projection.GetXaxis().GetNbins())
        for x_bin in range(input_h.GetXaxis().GetNbins()+2):
            norm = projection.GetBinContent(x_bin)
            # print("norm: ", norm)
            for y_bin in range(input_h.GetYaxis().GetNbins()+2):
                if norm == 0:
                    normilized_h.SetBinContent(x_bin, y_bin, 0)
                else:
                    normilized_h.SetBinContent(x_bin, y_bin,
                                               round(normilized_h.GetBinContent(x_bin, y_bin)/norm, 2))
        return normilized_h

    labels = ['Other', '#pi', '#pi#pi^{0}s', '3#pi', '3#pi#pi^{0}s', '']
    displ_list = [0.0, 0.1, 0.5, 5.0, 20.0, 50.0, 100.0]

    h3_dm_disp = file.Get("h3_dm_disp_t")
    # zn_bins = h3_dm_disp.GetZaxis().GetNbins()
    # step = int(zn_bins/devide_field/2)

    canvas = ROOT.TCanvas('canvas', '', 1600, 900)
    # ROOT.gStyle.SetTextSize(22);
    ROOT.gStyle.SetOptStat(11)
    canvas.Divide(int(len(displ_list)/2), 2, 0, 0)

    h3_dm_disp_ = []
    dm_projection = []
    for i in range(len(displ_list)-1):
        h3_dm_disp_.append(h3_dm_disp.Clone("h3_"+str(i)))

        # h3_dm_disp_[i].GetZaxis().SetRange(step*i+1, step*(i+1)
        # dm_projection.append(h3_dm_disp_[i].Project3D("xy").Clone("h2_"+str(i)))

        h3_dm_disp_[i].GetZaxis().SetRange(
            h3_dm_disp_[i].GetZaxis().FindFixBin(displ_list[i]),
            h3_dm_disp_[i].GetZaxis().FindFixBin(displ_list[i+1]))
        dm_projection.append(normilize_xaxis(
            h3_dm_disp_[i].Project3D("xy").Clone("h2_"+str(i))))

        for y_bin in range(1, dm_projection[i].GetYaxis().GetNbins()+1):
            dm_projection[i].GetYaxis().SetBinLabel(y_bin, labels[y_bin-1])
        for x_bin in range(1, dm_projection[i].GetXaxis().GetNbins()+1):
            dm_projection[i].GetXaxis().SetBinLabel(x_bin, labels[x_bin-1])

        canvas.cd(i+1)

        pad = canvas.GetPad(i+1)
        pad.SetLeftMargin(0.1)
        pad.SetBottomMargin(0.1)
        pad.SetTopMargin(0.07)
        pad.SetRightMargin(0.1)
        pad.SetFillColor(0)
        pad.SetBorderMode(1)

        # dm_projection[i].SetTitle(str(h3_dm_disp_[i].GetZaxis().GetBinLowEdge(step*i+1)) + "-" +
        #                           str(h3_dm_disp_[i].GetZaxis().GetBinUpEdge(step*(i+1))))
        dm_projection[i].SetTitle("xy displacement: [" +
                                  str(displ_list[i]) + "-" + str(displ_list[i+1]) + "] cm")
        dm_projection[i].GetYaxis().SetTitle("<reco>")
        dm_projection[i].GetXaxis().SetTitle("<gen>")
        dm_projection[i].GetXaxis().SetLabelSize(0.06)
        dm_projection[i].GetYaxis().SetLabelSize(0.06)
        dm_projection[i].SetMarkerSize(1.5)
        dm_projection[i].Draw("coltext")

    canvas.SaveAs('out/dm_migration_t.pdf')

    # 1 - pt_reco/pt_gen for different intervals -------------------->
    canvas = ROOT.TCanvas('canvas', '', 1600, 900)
    ROOT.gStyle.SetOptStat(0)
    cm_sep = 10.0  # cm
    displ_list = [0.0, 0.1, 0.5, 5.0, 20.0, 50.0, 100.0]
    canvas.Divide(int(len(displ_list)/2), 2, 0, 0)

    h2_pt_disp_ = file.Get("h3_pt_disp_t")
    legend = ROOT.TLegend(0.6, 0.75, 0.9, 0.9)

    h3_pt_disp_ = []
    pt_projection = []
    for i in range(len(displ_list)-1):
        h3_pt_disp_.append(h2_pt_disp_.Clone("h_pt_"+str(i)))
        pt_projection.append(h3_pt_disp_[-1].ProjectionX("pt_projection_"+str(i),
                             h2_pt_disp_.GetYaxis().FindFixBin(displ_list[i]),
                             h2_pt_disp_.GetYaxis().FindFixBin(displ_list[i+1])))
        pt_projection[i].Rebin(2)
        pt_projection[i].Scale(1.0/pt_projection[i].GetEntries())
        canvas.cd(i+1)

        pad = canvas.GetPad(i+1)
        pad.SetLeftMargin(0.1)
        pad.SetBottomMargin(0.1)
        pad.SetTopMargin(0.07)
        pad.SetRightMargin(0.1)
        pad.SetFillColor(0)
        pad.SetBorderMode(1)

        # pt_projection[i].GetXaxis().SetLabelSize(0.07)
        # pt_projection[i].GetYaxis().SetLabelSize(0.07)
        pt_projection[i].GetYaxis().SetTitle("arb. units")
        pt_projection[i].GetXaxis().SetTitle("1 - pt_reco/pt_gen")
        pt_projection[i].SetTitle("xy displacement: [" +
                                  str(displ_list[i]) + "-" + str(displ_list[i+1]) + "] cm")
        pt_projection[i].SetMaximum(1.1*pt_projection[0].GetMaximum())
        pt_projection[0].SetLineColor(2)
        pt_projection[i].Draw("HIST")
        pt_projection[0].Draw("HIST SAME")

    canvas.SaveAs('out/efficiency_recoPt.pdf')

    # Reco pt  ----------------------------->
    canvas = ROOT.TCanvas('canvas', '', 1600, 900)
    legend = ROOT.TLegend(0.5, 0.7, 0.9, 0.9)

    h2_pt = file.Get("h1_Tau_genpt_all").ProjectionY()
    h2_pt.GetXaxis().SetTitle("pt_gen")
    h2_pt_r = file.Get("h1_Tau_genpt_reco").ProjectionY()
    h2_pt_r.GetXaxis().SetTitle("pt_gen")

    legend.AddEntry(h2_pt, "all", "l")
    legend.AddEntry(h2_pt_r, "reco", "l")

    h2_pt.Draw()
    h2_pt_r.Draw("same")
    legend.Draw("same")

    canvas.SaveAs('out/pt_spectra.pdf')

    file.Close()
