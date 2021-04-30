from DataFormats.FWLite import Events, Handle
import ROOT
import numpy as np

if __name__ == '__main__':

    # files = ['/afs/cern.ch/user/m/myshched/STauGENProduction/test_prod_my/SUS-RunIIFall18GS-00022.root']
    files = [
    '/pnfs/desy.de/cms/tier2/store/user/myshched/SUS-RunIIFall18GS-production/SUS-RunIIFall18GS_ctau0p01-1000mm_mstau100_mlsp1-RAWSIM-RAWSIM/SUS-RunIIFall18GS_ctau0p01-1000mm_mstau100_mlsp1-RAWSIM/SUS-RunIIFall18GS_ctau0p01-1000mm_mstau100_mlsp1-RAWSIM/210224_130933/0000/SUS-RunIIFall18GS-00022_1.root',
    # '/pnfs/desy.de/cms/tier2/store/user/myshched/SUS-RunIIFall18GS-production/SUS-RunIIFall18GS_ctau0p01-1000mm_mstau100_mlsp1-RAWSIM-RAWSIM/SUS-RunIIFall18GS_ctau0p01-1000mm_mstau100_mlsp1-RAWSIM/SUS-RunIIFall18GS_ctau0p01-1000mm_mstau100_mlsp1-RAWSIM/210224_130933/0000/SUS-RunIIFall18GS-00022_10.root',
    # '/pnfs/desy.de/cms/tier2/store/user/myshched/SUS-RunIIFall18GS-production/SUS-RunIIFall18GS_ctau0p01-1000mm_mstau100_mlsp1-RAWSIM-RAWSIM/SUS-RunIIFall18GS_ctau0p01-1000mm_mstau100_mlsp1-RAWSIM/SUS-RunIIFall18GS_ctau0p01-1000mm_mstau100_mlsp1-RAWSIM/210224_130933/0000/SUS-RunIIFall18GS-00022_100.root',
    # '/pnfs/desy.de/cms/tier2/store/user/myshched/SUS-RunIIFall18GS-production/SUS-RunIIFall18GS_ctau0p01-1000mm_mstau100_mlsp1-RAWSIM-RAWSIM/SUS-RunIIFall18GS_ctau0p01-1000mm_mstau100_mlsp1-RAWSIM/SUS-RunIIFall18GS_ctau0p01-1000mm_mstau100_mlsp1-RAWSIM/210224_130933/0000/SUS-RunIIFall18GS-00022_101.root'
    ]


    dist_GENSIMvtx = ROOT.TH2D("dist_GENSIMvtx","distance SIMvtx-GENvtx vs. displacement", 200, 0, 10, 200, 0, 10)

    for f_name in files:
        
        print "FILE: ",f_name

        events = Events(f_name)

        # Tracks info part
        handleTracks = Handle('std::vector<SimTrack>')
        labelTracks = 'g4SimHits'

        # Gen par info
        handleGEN = Handle('std::vector<reco::GenParticle>')
        labelGEN = 'genParticles'

        # Vertex info part
        handleVertex = Handle('std::vector<SimVertex>')
        labelVertex = 'g4SimHits'

        # Hists info part
        handleHits = Handle('std::vector<PSimHit> ')
        labelsHits = [ "TrackerHitsPixelBarrelHighTof",
                       "TrackerHitsPixelBarrelLowTof",
                       "TrackerHitsPixelEndcapHighTof",
                       "TrackerHitsPixelEndcapLowTof" ]

        n_ev = 0
        for n_ev, ev in enumerate(events):
            print "event: ", n_ev
            if n_ev % 1000 == 0:
                print n_ev, "events"
            if n_ev> 2000:
                break

            ev.getByLabel(labelGEN, handleGEN)
            gen_particle = handleGEN.product()

            ev.getByLabel(labelTracks, handleTracks)
            tracks = handleTracks.product()

            ev.getByLabel(labelVertex, handleVertex)
            vertex = handleVertex.product()

            
            for tr in tracks:
                '''
                This part checks:
                1.  If there is a track which coresponds to genParticle
                    with transverse vertex position larger than  dis_transv [cm]
                    (also added condition that momentum points outside the cms tracker)
                2.  If there is a track which coresponds to stau (pdgId == 1000015)
                '''

                if (not tr.noVertex()) and (not tr.noGenpart()):

                    dist  = (vertex[tr.vertIndex()].position().x()-gen_particle[tr.genpartIndex()-1].vertex().x())**2
                    dist += (vertex[tr.vertIndex()].position().y()-gen_particle[tr.genpartIndex()-1].vertex().y())**2
                    dist += (vertex[tr.vertIndex()].position().z()-gen_particle[tr.genpartIndex()-1].vertex().z())**2
                    dist = np.sqrt(dist)
                    dist_GENSIMvtx.Fill(gen_particle[tr.genpartIndex()-1].vertex().rho(),dist)


            # raw_input("stop")
    c = ROOT.TCanvas()
    dist_GENSIMvtx.GetXaxis().SetTitle("Transverse Displacment [cm]")
    dist_GENSIMvtx.GetYaxis().SetTitle("|#vec{SimVertex}-#vec{GenVertex}|")
    dist_GENSIMvtx.Draw("colz")
    c.Print("GENSIMvtx.pdf")