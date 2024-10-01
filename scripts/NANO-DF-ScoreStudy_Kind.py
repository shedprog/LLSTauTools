import ROOT
import sys
import os
from itertools import product
import argparse
import numpy as np

# ROOT.gROOT.SetBatch(True)
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

ROOT.gInterpreter.Declare(f"#include \"{os.path.dirname(__file__)}/../inc/GenLeptonNano.h\"")

sys.path.append("..")
import python.DrawUtils as DrawUtils

ROOT.gROOT.SetBatch(True)


ROOT.gInterpreter.Declare("""
namespace JetTypeSelection {

static const double jet_pt = 20;
static const double jet_eta = 2.4;

static const double genLepton_jet_dR = 0.3;
static const double genLepton_jet_iso_dR = 0.5;
}                          
""")

# Function to get jet score if the match to genLepton.kind() == kind
ROOT.gInterpreter.Declare("""
ROOT::VecOps::RVec<Float_t> jet_score(std::vector<reco_tau::gen_truth::GenLepton> genLeptons,
                                      ROOT::VecOps::RVec<Float_t>& Jet_pt,
                                      ROOT::VecOps::RVec<Float_t>& Jet_eta,
                                      ROOT::VecOps::RVec<Float_t>& Jet_phi,
                                      ROOT::VecOps::RVec<Float_t>& Jet_mass,
                                      ROOT::VecOps::RVec<Float_t>& Jet_score,
                                      int kind)
{
   ROOT::VecOps::RVec<Float_t> jet_score;
   for (auto lepton: genLeptons) {
      std::cout << "lepton.kind() = " << static_cast<int>(lepton.kind()) << std::endl;
      if(static_cast<int>(lepton.kind())!=kind) continue;
      for(int jet_i=0; jet_i < Jet_pt.size(); jet_i++) {
         // kinematic jet cuts
         if(Jet_pt[jet_i] < JetTypeSelection::jet_pt || std::abs(Jet_eta[jet_i]) > JetTypeSelection::jet_eta) continue;
         ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double>> jet_p4
                     ( Jet_pt[jet_i], Jet_eta[jet_i], Jet_phi[jet_i], Jet_mass[jet_i] );
         auto visible_tau = lepton.visibleP4();
         double dR = ROOT::Math::VectorUtil::DeltaR(jet_p4, visible_tau);
         if( dR < JetTypeSelection::genLepton_jet_dR ) jet_score.push_back(Jet_score[jet_i]);      
      }
   }
   return jet_score;
}
""")

ROOT.gInterpreter.Declare("""
ROOT::VecOps::RVec<Float_t> jet_other_score(std::vector<reco_tau::gen_truth::GenLepton> genLeptons,
                                      ROOT::VecOps::RVec<Float_t>& Jet_pt,
                                      ROOT::VecOps::RVec<Float_t>& Jet_eta,
                                      ROOT::VecOps::RVec<Float_t>& Jet_phi,
                                      ROOT::VecOps::RVec<Float_t>& Jet_mass,
                                      ROOT::VecOps::RVec<Float_t>& Jet_score,
                                      ROOT::VecOps::RVec<Float_t>& GenJet_pt,
                                      ROOT::VecOps::RVec<Float_t>& GenJet_eta,
                                      ROOT::VecOps::RVec<Float_t>& GenJet_phi,
                                      ROOT::VecOps::RVec<Float_t>& GenJet_mass
                                      )
{
   ROOT::VecOps::RVec<Float_t> jet_score;
   
   for(int gen_i=0; gen_i < GenJet_pt.size(); gen_i++) {
      ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double>> gen_jet_p4
      ( GenJet_pt[gen_i], GenJet_eta[gen_i], GenJet_phi[gen_i], GenJet_mass[gen_i] );
      for(int jet_i=0; jet_i < Jet_pt.size(); jet_i++) {
         // kinematic jet cuts
         if(Jet_pt[jet_i] < JetTypeSelection::jet_pt || std::abs(Jet_eta[jet_i]) > JetTypeSelection::jet_eta) continue;
         ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double>> jet_p4
         ( Jet_pt[jet_i], Jet_eta[jet_i], Jet_phi[jet_i], Jet_mass[jet_i] );
         if( ROOT::Math::VectorUtil::DeltaR(jet_p4, gen_jet_p4) < JetTypeSelection::genLepton_jet_dR )
         {
            bool matched = false;
            for (auto lepton: genLeptons) {
               auto visible_tau = lepton.visibleP4();
               if( ROOT::Math::VectorUtil::DeltaR(jet_p4, visible_tau) < JetTypeSelection::genLepton_jet_iso_dR )
                  matched = true;
            }
            if(!matched) jet_score.push_back(Jet_score[jet_i]);
         }
      }
   }
   return jet_score;
}
""")

ROOT.gInterpreter.Declare("""
ROOT::VecOps::RVec<Float_t> jet_pu_score(std::vector<reco_tau::gen_truth::GenLepton> genLeptons,
                                      ROOT::VecOps::RVec<Float_t>& Jet_pt,
                                      ROOT::VecOps::RVec<Float_t>& Jet_eta,
                                      ROOT::VecOps::RVec<Float_t>& Jet_phi,
                                      ROOT::VecOps::RVec<Float_t>& Jet_mass,
                                      ROOT::VecOps::RVec<Float_t>& Jet_score,
                                      ROOT::VecOps::RVec<Float_t>& GenJet_pt,
                                      ROOT::VecOps::RVec<Float_t>& GenJet_eta,
                                      ROOT::VecOps::RVec<Float_t>& GenJet_phi,
                                      ROOT::VecOps::RVec<Float_t>& GenJet_mass
                                      )
{
   ROOT::VecOps::RVec<Float_t> jet_score;
   
   for(int jet_i=0; jet_i < Jet_pt.size(); jet_i++) {
      // kinematic jet cuts
      if(Jet_pt[jet_i] < JetTypeSelection::jet_pt || std::abs(Jet_eta[jet_i]) > JetTypeSelection::jet_eta) continue;
      ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double>> jet_p4
      ( Jet_pt[jet_i], Jet_eta[jet_i], Jet_phi[jet_i], Jet_mass[jet_i] );
      {
         bool matched = false;
         for(int gen_i=0; gen_i < GenJet_pt.size(); gen_i++) {
            ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double>> gen_jet_p4
            ( GenJet_pt[gen_i], GenJet_eta[gen_i], GenJet_phi[gen_i], GenJet_mass[gen_i] );
            if( ROOT::Math::VectorUtil::DeltaR(jet_p4, gen_jet_p4) < JetTypeSelection::genLepton_jet_iso_dR )
               matched = true;
         }
         for (auto lepton: genLeptons) {
            auto visible_tau = lepton.visibleP4();
            if( ROOT::Math::VectorUtil::DeltaR(jet_p4, visible_tau) < JetTypeSelection::genLepton_jet_iso_dR )
               matched = true;
         }
         if(!matched) jet_score.push_back(Jet_score[jet_i]);
      }
   }
   return jet_score;
}
""")



hists = {}

if __name__ == "__main__":

   parser = argparse.ArgumentParser(description='Count the objects consistenly with training definition.')
   parser.add_argument('--input', help='path to the NanoAOD file')
   parser.add_argument('-o','--output', help='folder for the plot outputs', required=True)
   args = parser.parse_args()
   
   if not os.path.exists(args.output): os.makedirs(args.output)

   ROOT.EnableImplicitMT(1)

   df = ROOT.RDataFrame("Events", args.input)

   df = df.Define("genLeptons", """reco_tau::gen_truth::GenLepton::fromNanoAOD(GenPart_pt, GenPart_eta,
                              GenPart_phi, GenPart_mass, GenPart_vertexX,GenPart_vertexY, GenPart_vertexZ, GenPart_genPartIdxMother, GenPart_pdgId,
                              GenPart_statusFlags, event)""")

   df = df.Define("jet_score_1", "jet_score(genLeptons, Jet_pt, Jet_eta, Jet_phi, Jet_mass, Jet_disTauTag_score1, 1)")
   df = df.Define("jet_score_2", "jet_score(genLeptons, Jet_pt, Jet_eta, Jet_phi, Jet_mass, Jet_disTauTag_score1, 2)")
   df = df.Define("jet_score_3", "jet_score(genLeptons, Jet_pt, Jet_eta, Jet_phi, Jet_mass, Jet_disTauTag_score1, 3)")
   df = df.Define("jet_score_4", "jet_score(genLeptons, Jet_pt, Jet_eta, Jet_phi, Jet_mass, Jet_disTauTag_score1, 4)")
   df = df.Define("jet_score_5", "jet_score(genLeptons, Jet_pt, Jet_eta, Jet_phi, Jet_mass, Jet_disTauTag_score1, 5)")
   df = df.Define("jet_score_other", "jet_other_score(genLeptons, Jet_pt, Jet_eta, Jet_phi, Jet_mass, Jet_disTauTag_score1, GenJet_pt, GenJet_eta, GenJet_phi, GenJet_mass)")
   df = df.Define("jet_score_pu", "jet_pu_score(genLeptons, Jet_pt, Jet_eta, Jet_phi, Jet_mass, Jet_disTauTag_score1, GenJet_pt, GenJet_eta, GenJet_phi, GenJet_mass)")

   hists['jet_score_1'] = df.Histo1D(("jet_kind_1",f"jet from electron", 100, 0.0, 1.0), "jet_score_1")
   hists['jet_score_2'] = df.Histo1D(("jet_kind_2",f"jet from muon", 100, 0.0, 1.0), "jet_score_2")
   hists['jet_score_3'] = df.Histo1D(("jet_kind_3",f"jet from tau->electron", 100, 0.0, 1.0), "jet_score_3")
   hists['jet_score_4'] = df.Histo1D(("jet_kind_4",f"jet from tau->muon", 100, 0.0, 1.0), "jet_score_4")
   hists['jet_score_5'] = df.Histo1D(("jet_kind_5",f"jet from tau->hadrons", 100, 0.0, 1.0), "jet_score_5")
   hists['jet_score_other'] = df.Histo1D(("jet_kind_6",f"jet from other gen jet", 100, 0.0, 1.0), "jet_score_other")
   hists['jet_score_pu'] = df.Histo1D(("jet_kind_pu",f"jet from other pu", 100, 0.0, 1.0), "jet_score_pu")

   canvas = DrawUtils.GetCanvas("canvas_score_1")
   DrawUtils.PlotHistList(canvas, [hists['jet_score_1']],"jet from electron prob.","arb. units", rescale=False, logY=True)
   DrawUtils.DrawHeader(canvas, "Private work (CMS simulation)", "#tau-reco")
   canvas.SaveAs(args.output+"/jet_score_1.png")
   
   canvas = DrawUtils.GetCanvas("canvas_score_2")
   DrawUtils.PlotHistList(canvas, [hists['jet_score_2']],"jet from muon prob.","arb. units", rescale=False, logY=True)
   DrawUtils.DrawHeader(canvas, "Private work (CMS simulation)", "#tau-reco")
   canvas.SaveAs(args.output+"/jet_score_2.png")
   
   canvas = DrawUtils.GetCanvas("canvas_score_3")
   DrawUtils.PlotHistList(canvas, [hists['jet_score_3']],"jet from tau->electron prob.","arb. units", rescale=False, logY=True)
   DrawUtils.DrawHeader(canvas, "Private work (CMS simulation)", "#tau-reco")
   canvas.SaveAs(args.output+"/jet_score_3.png")
   
   canvas = DrawUtils.GetCanvas("canvas_score_4")
   DrawUtils.PlotHistList(canvas, [hists['jet_score_4']],"jet from tau->muon prob.","arb. units", rescale=False, logY=True)
   DrawUtils.DrawHeader(canvas, "Private work (CMS simulation)", "#tau-reco")
   canvas.SaveAs(args.output+"/jet_score_4.png")
   
   canvas = DrawUtils.GetCanvas("canvas_score_5")
   DrawUtils.PlotHistList(canvas, [hists['jet_score_5']],"jet from tau->hadrons prob.","arb. units", rescale=False, logY=True)
   DrawUtils.DrawHeader(canvas, "Private work (CMS simulation)", "#tau-reco")
   canvas.SaveAs(args.output+"/jet_score_5.png")
   
   canvas = DrawUtils.GetCanvas("canvas_score_other")
   DrawUtils.PlotHistList(canvas, [hists['jet_score_other']],"jet from other gen jet prob.","arb. units", rescale=False, logY=True)
   DrawUtils.DrawHeader(canvas, "Private work (CMS simulation)", "#tau-reco")
   canvas.SaveAs(args.output+"/jet_score_other.png")
   
   canvas = DrawUtils.GetCanvas("canvas_score_pu")
   DrawUtils.PlotHistList(canvas, [hists['jet_score_pu']],"jet from other pu prob.","arb. units", rescale=False, logY=True)
   DrawUtils.DrawHeader(canvas, "Private work (CMS simulation)", "#tau-reco")
   canvas.SaveAs(args.output+"/jet_score_pu.png")
   
   # bkgr = hists['jet_score_other'].Clone()
   # bkgr.SetDirectory(0)
   # bkgr.Scale(1.0/bkgr.Integral())
   # sig = hists['jet_score_5'].Clone()
   # sig.SetDirectory(0)
   # sig.Scale(1.0/sig.Integral())
   # sig.Divide(bkgr)
   # sig.GetXaxis().SetRangeUser(0.98, 1.001)
   
   # canvas = DrawUtils.GetCanvas("canvas_score_ratio")
   # DrawUtils.PlotHistList(canvas, [sig],"prob.","sig/bkgr", rescale=False, logY=True)
   # DrawUtils.DrawHeader(canvas, "Private work (CMS simulation)", "#tau-reco")
   # canvas.SaveAs(args.output+"/jet_score_ratio.png")