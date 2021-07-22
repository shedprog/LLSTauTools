import ROOT
import sys
import os
from itertools import product

sys.path.append("..")
import python.DrawUtils as DrawUtils

ROOT.gInterpreter.Declare("#include \"../inc/GenLepton.h\"")

get_visP4='''
auto genLeptons = 
reco_tau::gen_truth::GenLepton::fromRootTuple(
                genLepton_lastMotherIndex,
                genParticle_pdgId,
                genParticle_mother,
                genParticle_charge,
                genParticle_isFirstCopy,
                genParticle_isLastCopy,
                genParticle_pt,
                genParticle_eta,
                genParticle_phi,
                genParticle_mass,
                genParticle_vtx_x,
                genParticle_vtx_y,
                genParticle_vtx_z);
const ROOT::Math::LorentzVector<ROOT::Math::PxPyPzE4D<double>>&
    visP4 = genLeptons.visibleP4();
return visP4;
'''

if __name__ == "__main__":

    '''
    The following script is performing the comperison of kinematic
    varaiables for different mass points. The script is run
    above BigTauTuple files that are created with TauMLTools.
    python ./MassPointStat.py <PATH_TO_TAUBIGTUPLES>
    '''

    path_to_files = sys.argv[1]

    ROOT.EnableImplicitMT(10)

    # df = ROOT.RDataFrame("taus", path_to_files+"/*.root")
    df = ROOT.RDataFrame("taus", path_to_files)

    hadronic_taus = df.Filter('genLepton_kind==5', 'Hadronic Taus Candidates')

    mstau_list = [100, 250, 400]
    mlsp_list  = [1, 20]
    ctau0_list = [1000]

    grid = list(product(*[mstau_list, mlsp_list, ctau0_list]))
    print("Mass ponts ",len(grid))

    filters = []
    hists = {
             "vis_pt":[],
             "vis_eta":[],
            }
    for mstau, mlsp, ctau0 in grid:

        filters.append(hadronic_taus.Filter(
                f'susy_mstau=={mstau} && susy_mlsp=={mlsp} && susy_ctau=={ctau0}',
                f'mstau={mstau} mlsp={mlsp} ctau0={ctau0}'))
        
        filters[-1] = filters[-1].Define('visP4',get_visP4)\
                                 .Define('vis_pt','visP4.Pt()')\
                                 .Define('vis_eta','visP4.Eta()')

        hists['vis_pt'].append(filters[-1].Histo1D(("vis_pt",
                                                    f"vis_pt, MS({mstau}_{mlsp}_{ctau0})",
                                                    60, 0.0, 800), "vis_pt"))
        hists['vis_eta'].append(filters[-1].Histo1D(("vis_eta",
                                                    f"vis_eta, MS({mstau}_{mlsp}_{ctau0})",
                                                    40, -3.0, 3.0), "vis_eta"))
                                
    
    print('All stats:')
    allCutsReport = df.Report()
    allCutsReport.Print()

    canvas_pt = DrawUtils.GetCanvas("canvas_pt")
    DrawUtils.PlotHistList(canvas_pt, hists['vis_pt'],"visible pt")
    DrawUtils.DrawHeader(canvas_pt, "P^{T}_{vis}(#tau)" , "Preliminary", "Reco Study")
    DrawUtils.DrawLegend(canvas_pt, DrawUtils.GetHistTitlesLegend(hists["vis_pt"]))

    canvas_eta = DrawUtils.GetCanvas("eta")
    DrawUtils.PlotHistList(canvas_eta, hists['vis_eta'],"visible eta")
    DrawUtils.DrawHeader(canvas_eta, "#eta_{vis}(#tau)" , "Preliminary", "Reco Study")
    DrawUtils.DrawLegend(canvas_eta, DrawUtils.GetHistTitlesLegend(hists["vis_eta"]))

    ROOT.gApplication.Run()