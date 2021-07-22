import ROOT
import sys
import os
import numpy as np

if __name__ == "__main__":

    file = ROOT.TFile.Open(str(sys.argv[1]), 'read')
    try:
        os.stat("out")
    except:
        os.mkdir("out")


    # lifetime vs. displacement checks --------------------->
    canvas = ROOT.TCanvas('canvas', '', 1000, 500)
    ROOT.gStyle.SetOptStat(11);
    lifetimes = [0.05, 0.1, 0.5, 1, 2.5, 5, 7.5, 10]
    canvas.Divide(4,2,0,0)

    h2_Tau_h_all = file.Get('h1_Tau_h_all')

    r = 0.05 #%
    for i, lt in enumerate(lifetimes):
        LifeTimePlot = file.Get('h1_Tau_h_all').ProjectionX("lt"+str(i),
            h2_Tau_h_all.GetYaxis().FindBin(lt-r*lt),h2_Tau_h_all.GetYaxis().FindBin(lt+r*lt))
        canvas.cd(i+1)
        ROOT.gPad.SetLogy()
        LifeTimePlot.SetTitle("ctau="+str(lt))
        LifeTimePlot.GetXaxis().SetRangeUser(0.,100.)
        LifeTimePlot.GetXaxis().SetTitle("#delta vtx [units]")
        LifeTimePlot.Draw()

    canvas.SaveAs('out/lifetimes.pdf')


    # lifetime vs. displacement checks comul--------------------->
    # canvas = ROOT.TCanvas('canvas', '', 1000, 500)
    # # ROOT.gStyle.SetOptStat(11)
    # lifetimes = [0.05, 0.1, 0.5, 1, 2.5, 5, 7.5, 10]
    # # canvas.Divide(4,2,0,0)
    # h2_Tau_h_all = file.Get('h1_Tau_h_all')
    #
    # r = 0.05 #%
    # # for i, lt in enumerate(lifetimes):
    # #     LifeTimePlot = file.Get('h1_Tau_h_all').ProjectionX("lt"+str(i),
    # #         h2_Tau_h_all.GetYaxis().FindBin(lt-r*lt),h2_Tau_h_all.GetYaxis().FindBin(lt+r*lt))
    # #     LifeTimePlot_com = LifeTimePlot.GetCumulative()
    # #     LifeTimePlot_com.Scale(1.0/LifeTimePlot.Integral())
    # #     canvas.cd(i+1)
    # #     LifeTimePlot_com.SetTitle("ctau="+str(lt))
    # #     LifeTimePlot_com.GetXaxis().SetRangeUser(0.,20.)
    # #     LifeTimePlot_com.GetXaxis().SetTitle("#delta vtx [units]")
    # #     LifeTimePlot_com.Draw()
    # #
    # #     line1 = ROOT.TLine(0.05,0.63,0.80,0.63)
    # #     line1.SetLineWidth(8)
    # #     line1.SetLineColor(2)
    # #     line1.Draw()
    #
    # def Nfunc(x, par):
    #    return 1.0-np.exp(-x[0]/par[0]);
    #
    # func = ROOT.TF1("func",Nfunc,0,100,2);
    # func.SetParameters(10000.0, 1.0);
    #
    # # Fit histogram
    # lt = 10.0
    # i = 1
    #
    # LifeTimePlot = file.Get('h1_Tau_h_all').ProjectionX("lt"+str(i),
    #     h2_Tau_h_all.GetYaxis().FindBin(lt-r*lt),h2_Tau_h_all.GetYaxis().FindBin(lt+r*lt))
    # LifeTimePlot_com = LifeTimePlot.GetCumulative()
    # LifeTimePlot_com.Scale(1.0/LifeTimePlot.Integral())
    # LifeTimePlot_com.SetTitle("ctau="+str(lt))
    # LifeTimePlot_com.GetXaxis().SetRangeUser(0.,100.)
    # LifeTimePlot_com.GetXaxis().SetTitle("#delta vtx [units]")
    # LifeTimePlot_com.Draw()
    #
    # LifeTimePlot_com.Fit("func","IR")
    #
    # canvas.SaveAs('out/lifetimes_comul.pdf')

    file.Close()
