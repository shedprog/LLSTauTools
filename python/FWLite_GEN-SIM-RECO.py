from DataFormats.FWLite import Events, Handle
import ROOT
import numpy as np

if __name__ == '__main__':

    files = ['/pnfs/desy.de/cms/tier2/store/user/myshched/SUS-RunIIFall18GS-production/SUS-RunIIFall18GS_ctau0p01-1000mm_mstau100_mlsp1-RAWSIM-RAWSIM/SUS-RunIIFall18GS_ctau0p01-1000mm_mstau100_mlsp1-RAWSIM/SUS-RunIIFall18GS_ctau0p01-1000mm_mstau100_mlsp1-RAWSIM/210224_130933/0000/SUS-RunIIFall18GS-00022_100.root', '/pnfs/desy.de/cms/tier2/store/user/myshched/SUS-RunIIFall18GS-production/SUS-RunIIFall18GS_ctau0p01-1000mm_mstau100_mlsp1-RAWSIM-RAWSIM/SUS-RunIIFall18GS_ctau0p01-1000mm_mstau100_mlsp1-RAWSIM/SUS-RunIIFall18GS_ctau0p01-1000mm_mstau100_mlsp1-RAWSIM/210224_130933/0000/SUS-RunIIFall18GS-00022_101.root', '/pnfs/desy.de/cms/tier2/store/user/myshched/SUS-RunIIFall18GS-production/SUS-RunIIFall18GS_ctau0p01-1000mm_mstau100_mlsp1-RAWSIM-RAWSIM/SUS-RunIIFall18GS_ctau0p01-1000mm_mstau100_mlsp1-RAWSIM/SUS-RunIIFall18GS_ctau0p01-1000mm_mstau100_mlsp1-RAWSIM/210224_130933/0000/SUS-RunIIFall18GS-00022_102.root']


    for f_name in files:

        events = Events(f_name)

        # Tracks check part
        handleGEN = Handle('std::vector<reco::GenParticle>')
        handleTracks = Handle('std::vector<SimTrack> ')
        labelGEN = 'genParticles'
        labelTracks = 'g4SimHits'

        # Hists check part
        handleHits = Handle('std::vector<PSimHit> ')
        labelsHits = [ "TrackerHitsPixelBarrelHighTof",
                       "TrackerHitsPixelBarrelLowTof",
                       "TrackerHitsPixelEndcapHighTof",
                       "TrackerHitsPixelEndcapLowTof" ]

        n_ev = 0
        for n_ev, ev in enumerate(events):
            if n_ev % 1000 == 0:
                print n_ev, "events"
            # if n_ev > 10:
            #     break

            ev.getByLabel(labelGEN, handleGEN)
            gen_particle = handleGEN.product()

            ev.getByLabel(labelTracks, handleTracks)
            tracks = handleTracks.product()

            Tracker_nHits = np.zeros((4,1600000), dtype=int)
            # Tracker_nHits_x = [[[] for j in range(1600000)] for i in range(4)]
            # Tracker_nHits_z = [[[] for j in range(1600000)] for i in range(4)]
            # Tracker_nHits_y = [[[] for j in range(1600000)] for i in range(4)]

            for i, label in enumerate(labelsHits):
                '''
                In this part, hits inside PIXEL tracker
                are accumulated
                '''
                ev.getByLabel(labelTracks, label, handleHits)
                hits = handleHits.product()
                for hit in hits:
                    Tracker_nHits[i][hit.trackId()]+=1

                    # Tracker_nHits_x[i][hit.trackId()].append(hit.entryPoint().x())
                    # Tracker_nHits_z[i][hit.trackId()].append(hit.entryPoint().y())
                    # Tracker_nHits_y[i][hit.trackId()].append(hit.entryPoint().z())

            for tr in tracks:
                '''
                This part checks:
                1.  If there is a track which coresponds to genParticle
                    with transverse vertex position larger than  dis_transv [cm]
                    (also added condition that momentum points outside the cms)
                2.  If there is a track which coresponds to stau (pdgId == 1000015)
                '''
                dis_transv = 500.0

                if tr.genpartIndex() >= 0:

                    if(gen_particle[tr.genpartIndex()-1].vertex().rho()>=dis_transv \
                       and (gen_particle[tr.genpartIndex()-1].vertex().x()<0) == (gen_particle[tr.genpartIndex()-1].momentum().x()<0) \
                       and (gen_particle[tr.genpartIndex()-1].vertex().y()<0) == (gen_particle[tr.genpartIndex()-1].momentum().y()<0) \
                       and (gen_particle[tr.genpartIndex()-1].vertex().z()<0) == (gen_particle[tr.genpartIndex()-1].momentum().z()<0)):

                        print ">"+str(dis_transv)+"[cm] transverse plane:", \
                            "pdgId:", gen_particle[tr.genpartIndex()-1].pdgId(), \
                            "pt:", gen_particle[tr.genpartIndex()-1].pt(), \
                            "vtx rho:", gen_particle[tr.genpartIndex()-1].vertex().rho(), \
                            "vtx abs:", gen_particle[tr.genpartIndex()-1].vertex().r(), \
                            "PixelBarrelHighTof:", Tracker_nHits[0][tr.trackId()], \
                            "PixelBarrelLowTof:", Tracker_nHits[1][tr.trackId()], \
                            "PixelEndcapHighTof:", Tracker_nHits[2][tr.trackId()], \
                            "PixelEndcapLowTof:", Tracker_nHits[3][tr.trackId()]
                        # print Tracker_nHits_x[0][tr.trackId()], \
                        #       Tracker_nHits_z[0][tr.trackId()], \
                        #       Tracker_nHits_y[0][tr.trackId()]
                        # print Tracker_nHits_x[1][tr.trackId()], \
                        #       Tracker_nHits_z[1][tr.trackId()], \
                        #       Tracker_nHits_y[1][tr.trackId()]
                        # print Tracker_nHits_x[2][tr.trackId()], \
                        #       Tracker_nHits_z[2][tr.trackId()], \
                        #       Tracker_nHits_y[2][tr.trackId()]
                        # print Tracker_nHits_x[3][tr.trackId()], \
                        #       Tracker_nHits_z[3][tr.trackId()], \
                        #       Tracker_nHits_y[3][tr.trackId()]

                    if(abs(gen_particle[tr.genpartIndex()-1].pdgId())>=1000000):

                        print "stau particle track!: ~~~~~~~~~~~~> ", \
                            "pdgId: ", gen_particle[tr.genpartIndex()-1].pdgId(), \
                            "vtx rho: ", gen_particle[tr.genpartIndex()-1].vertex().rho(), \
                            "vtx abs: ", gen_particle[tr.genpartIndex()-1].vertex().r()

        # exit()
