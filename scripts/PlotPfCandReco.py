import ROOT
import sys
import os

sys.path.append(os.path.dirname(sys.argv[0])+"/..")
import python.DrawUtils as DrawUtils

ROOT.gROOT.SetBatch(True)

if __name__ == "__main__":

    '''
    The following script is drawing the plots
    of the events where of pfCands and lostTracks matches stau
    $ ./TauTuple_pfCandStudy --output <file_output>.root --input <dataset> --n-files -1
    $ python ./PlotPfCand.py <file_output>.root 
    '''

    file = ROOT.TFile.Open(str(sys.argv[1]), 'read')

    h1_Tau_h_all = file.Get('h1_Tau_h_all')
    h1_Tau_h_reco = file.Get('h1_Tau_h_reco')
    h1_lostTrack_to_stau_match = file.Get('h1_lostTrack_stau')
    h1_pfCand_to_stau_match = file.Get('h1_pfCand_stau')
    h1_lostTrack_to_pion_match = file.Get('h1_lostTrack_pion')
    h1_pfCand_to_pion_match = file.Get('h1_pfCand_pion')

    h1_Tau_h_all.SetTitle("All hadronic taus")
    h1_Tau_h_reco.SetTitle("HPS reco taus")
    h1_lostTrack_to_stau_match.SetTitle("#tilde{#tau} match to lostTrack")
    h1_pfCand_to_stau_match.SetTitle("#tilde{#tau} match to pfCand")
    h1_lostTrack_to_pion_match.SetTitle("#pi^{#pm} match to lostTrack")
    h1_pfCand_to_pion_match.SetTitle("#pi^{#pm} match to pfCand")

    h1_Tau_h_all.SetMinimum(50.0)
    h1_Tau_h_reco.SetMinimum(50.0)
    h1_lostTrack_to_stau_match.SetMinimum(50.0)
    h1_pfCand_to_stau_match.SetMinimum(50.0)
    h1_lostTrack_to_pion_match.SetMinimum(50.0)
    h1_pfCand_to_pion_match.SetMinimum(50.0)

    # GetXaxis()->SetRangeUser(min, max);
    MergeBin = 15
    h1_Tau_h_all.Rebin(MergeBin)
    h1_Tau_h_reco.Rebin(MergeBin)
    h1_lostTrack_to_stau_match.Rebin(MergeBin)
    h1_pfCand_to_stau_match.Rebin(MergeBin)
    h1_lostTrack_to_pion_match.Rebin(MergeBin)
    h1_pfCand_to_pion_match.Rebin(MergeBin)
 
    h1_Tau_h_all.GetXaxis().SetRangeUser(-1.0, 120.0)
    h1_Tau_h_reco.GetXaxis().SetRangeUser(-1.0, 120.0)
    h1_lostTrack_to_stau_match.GetXaxis().SetRangeUser(-1.0, 120.0)
    h1_pfCand_to_stau_match.GetXaxis().SetRangeUser(-1.0, 120.0)
    h1_lostTrack_to_pion_match.GetXaxis().SetRangeUser(-1.0, 120.0)
    h1_pfCand_to_pion_match.GetXaxis().SetRangeUser(-1.0, 120.0)

    hists = [
        h1_Tau_h_all,
        h1_Tau_h_reco,
        h1_lostTrack_to_stau_match,
        h1_pfCand_to_stau_match,
        h1_lostTrack_to_pion_match,
        h1_pfCand_to_pion_match
    ]

    canvas ,pad1, pad2 = DrawUtils.GetCanvasPads("canvas")
    DrawUtils.PlotHistList(pad1, hists, "[cm]", "entries")
    DrawUtils.DrawHeader(pad1, "match dR<0.05" , "#tau reco", "c#tau_{0}=1000mm")
    legend = DrawUtils.GetHistTitlesLegend(hists)
    DrawUtils.DrawLegend(pad1, legend)
    pad1.SetLogy()
    pad2.cd()
    pad2.SetGridy()
    ratio_h = DrawUtils.createRatio(h1_Tau_h_reco, h1_Tau_h_all,"eff.")
    ratio_h.GetXaxis().SetTitle("displacement [cm]")
    ratio_h.Draw()
    canvas.cd()
    canvas.SaveAs("pfCand_match.pdf")
