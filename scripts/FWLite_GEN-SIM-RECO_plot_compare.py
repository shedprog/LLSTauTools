from DataFormats.FWLite import Events, Handle
import ROOT
import numpy as np
import os

def get_files(prefix, das_name):
    cmd = "dasgoclient --query=\"file dataset=" \
        +  das_name + " instance=prod/phys03\""
    print cmd
    res = os.popen(cmd).read()
    return [prefix + path for path in res.split('\n')]

if __name__ == '__main__':

    # files = [
    #         '/pnfs/desy.de/cms/tier2/store/user/myshched/mc/SUS-RunIISummer20UL18wmLHEGEN-stau400_lsp1_ctau1000mm-GENSIM/GENSIM/211101_173846/0000/SUS-RunIISummer20UL18wmLHEGEN-LLStau_1.root',
    #         '/pnfs/desy.de/cms/tier2/store/user/myshched/mc/SUS-RunIISummer20UL18wmLHEGEN-stau400_lsp1_ctau1000mm-GENSIM/GENSIM/211101_173846/0000/SUS-RunIISummer20UL18wmLHEGEN-LLStau_10.root'
    #         ]
    # files = [
    #     "/pnfs/desy.de/cms/tier2/store/user/myshched/mc/SUS-RunIISummer20UL18wmLHEGEN-stau400_lsp1_ctau1000mm-GENSIM/GENSIM/211101_173846/0000/SUS-RunIISummer20UL18wmLHEGEN-LLStau_794.root",
    #     "/pnfs/desy.de/cms/tier2/store/user/myshched/mc/SUS-RunIISummer20UL18wmLHEGEN-stau400_lsp1_ctau1000mm-GENSIM/GENSIM/211101_173846/0000/SUS-RunIISummer20UL18wmLHEGEN-LLStau_795.root",
    #     "/pnfs/desy.de/cms/tier2/store/user/myshched/mc/SUS-RunIISummer20UL18wmLHEGEN-stau400_lsp1_ctau1000mm-GENSIM/GENSIM/211101_173846/0000/SUS-RunIISummer20UL18wmLHEGEN-LLStau_796.root",
    #     "/pnfs/desy.de/cms/tier2/store/user/myshched/mc/SUS-RunIISummer20UL18wmLHEGEN-stau400_lsp1_ctau1000mm-GENSIM/GENSIM/211101_173846/0000/SUS-RunIISummer20UL18wmLHEGEN-LLStau_797.root"
    # ]
    #files=["/nfs/dust/cms/user/mykytaua/dataLLSTAU/MCprod_tests/SUS-RunIISummer20UL18wmLHEGEN-LLStau.root"]

    # files = ['./SUS-RunIISummer20UL18wmLHEGEN-LLStau.root']
    files = [
        "/pnfs/desy.de/cms/tier2/store/user/myshched/mc/SUS-RunIISummer20UL18wmLHEGEN-stau400_lsp1_ctau1000mm-GENSIM/GENSIM/211101_173846/0000/SUS-RunIISummer20UL18wmLHEGEN-LLStau_794.root",
        "/pnfs/desy.de/cms/tier2/store/user/myshched/mc/SUS-RunIISummer20UL18wmLHEGEN-stau400_lsp1_ctau1000mm-GENSIM/GENSIM/211101_173846/0000/SUS-RunIISummer20UL18wmLHEGEN-LLStau_795.root"
        ]

    # prefix="root://cmsxrootd.fnal.gov//"
    # files = get_files(prefix, "/Staus_M_500_1000mm_14TeV_Run3MC/fiorendi-GENSIM-71ae861820d55e64e1036ab966b9822a/USER")[:50]

    # old MC premix:
    # path_my = "/pnfs/desy.de/cms/tier2/store/user/myshched/SUS-RunIIFall18GS-production-new/SUS-RunIIFall18GS_ctau1000mm_mstau100_250_400_mlsp1_20-RAWSIM/SUS-RunIIFall18GS_ctau1000mm_mstau100_250_400_mlsp1_20-RAWSIM/SUS-RunIIFall18GS_ctau1000mm_mstau100_250_400_mlsp1_20-RAWSIM/210701_181221/0000"
    # files = [
    #     path_my + "/SUS-RunIIFall18GS-00022_320.root",
    #     path_my + "/SUS-RunIIFall18GS-00022_546.root", 
    #     path_my + "/SUS-RunIIFall18GS-00022_771.root", 
    #     path_my + "/SUS-RunIIFall18GS-00022_997.root",
    #     path_my + "/SUS-RunIIFall18GS-00022_321.root",
    #     path_my + "/SUS-RunIIFall18GS-00022_547.root", 
    #     path_my + "/SUS-RunIIFall18GS-00022_772.root", 
    #     path_my + "/SUS-RunIIFall18GS-00022_998.root",
    #     path_my + "/SUS-RunIIFall18GS-00022_322.root",
    #     path_my + "/SUS-RunIIFall18GS-00022_548.root", 
    #     path_my + "/SUS-RunIIFall18GS-00022_773.root", 
    #     path_my + "/SUS-RunIIFall18GS-00022_999.root",
    #     path_my + "/SUS-RunIIFall18GS-00022_323.root",
    #     path_my + "/SUS-RunIIFall18GS-00022_549.root", 
    #     path_my + "/SUS-RunIIFall18GS-00022_774.root",
    # ]

    # x: displacement [cm], y: SimVertex-GenVertex [cm]
    # from_stau_xy = [[], []]
    # all_xy = [[], []]

    disp, pt, mass = [], [], []
    for i, file in enumerate(files):
        disp.append( ROOT.TH1D("disp"+str(i),"disp",100, 0, 100) )
        pt.append( ROOT.TH1D("pt"+str(i),"pt",100, 0, 1000) )
        mass.append( ROOT.TH1D("mass"+str(i),"mass", 100, 0, 1000) )


    for i, f_name in enumerate(files):
        print "FILE: ", f_name

        events = Events(f_name)


        # Gen par info
        handleGEN = Handle('std::vector<reco::GenParticle>')
        labelGEN = 'genParticlePlusGeant'
        # labelGEN = 'genParticles'


        n_ev = 0
        for n_ev, ev in enumerate(events):
            print "event", n_ev
      
            ev.getByLabel(labelGEN, handleGEN)
            gen_particle = handleGEN.product()



            for gen in gen_particle:
                if abs(gen.pdgId())==15:
                    if abs(gen.motherRef().pdgId())>=1000000:
                        disp_ = gen.vertex().x()**2+gen.vertex().y()**2+gen.vertex().z()**2
                        mass[i].Fill(gen.motherRef().mass())
                        disp[i].Fill(disp_)
                        pt[i].Fill(gen.motherRef().pt())

     

    pref = "compare_"
    dir_out = "./output/"
    try:
        os.stat(dir_out)
    except:
        os.mkdir(dir_out)
    
    c = ROOT.TCanvas("c", "c", 1000, 800)
    disp[0].GetXaxis().SetTitle("[cm]")
    disp[0].Draw()
    disp[1].GetXaxis().SetTitle("[cm]")
    disp[1].SetLineColor(2)
    disp[1].Draw("same")
    c.Print(dir_out + pref + "genParticle_vtx.pdf")
    c.SetLogy()
    c.Print(dir_out + pref + "genParticle_vtx_log.pdf")

    c1 = ROOT.TCanvas("c1","c1", 1000, 800)
    pt[0].Draw()
    pt[1].SetLineColor(2)
    pt[1].Draw("same")
    c1.Print(dir_out + pref + "genParticle_pt.pdf")

    c_m = ROOT.TCanvas("c_m","c_m", 1000, 800)
    mass[0].Draw()
    mass[1].SetLineColor(2)
    mass[1].Draw("same")
    c_m.Print(dir_out + pref + "genParticle_mass.pdf")
