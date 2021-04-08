from DataFormats.FWLite import Events, Handle
import ROOT
import numpy as np

if __name__ == '__main__':

    f_name = '/pnfs/desy.de/cms/tier2/store/user/myshched/SUS-RunIIFall18GS-production/SUS-RunIIFall18GS_ctau0p01-1000mm_mstau100_mlsp1-RAWSIM-RAWSIM/SUS-RunIIFall18GS_ctau0p01-1000mm_mstau100_mlsp1-RAWSIM/SUS-RunIIFall18GS_ctau0p01-1000mm_mstau100_mlsp1-RAWSIM/210224_130933/0000/SUS-RunIIFall18GS-00022_100.root'
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

        for i, label in enumerate(labelsHits):
            '''
            In this part, hits inside PIXEL tracker
            are accumulated
            '''
            ev.getByLabel(labelTracks, label, handleHits)
            hits = handleHits.product()
            for hit in hits:
                Tracker_nHits[i][hit.trackId()]+=1

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

                    print ">"+str(dis_transv)+"[cm] transverse plane: ", \
                        "pdgId: ", gen_particle[tr.genpartIndex()-1].pdgId(), \
                        "vtx rho: ", gen_particle[tr.genpartIndex()-1].vertex().rho(), \
                        "vtx abs: ", gen_particle[tr.genpartIndex()-1].vertex().r(), \
                        "PixelBarrelHighTof: ", Tracker_nHits[0][tr.trackId()], \
                        "PixelBarrelLowTof: ", Tracker_nHits[1][tr.trackId()], \
                        "PixelEndcapHighTof: ", Tracker_nHits[2][tr.trackId()], \
                        "PixelEndcapLowTof: ", Tracker_nHits[3][tr.trackId()]

                if(abs(gen_particle[tr.genpartIndex()-1].pdgId())>=1000000):

                    print "stau particle track!: ~~~~~~~~~~~~> ", \
                        "pdgId: ", gen_particle[tr.genpartIndex()-1].pdgId(), \
                        "vtx rho: ", gen_particle[tr.genpartIndex()-1].vertex().rho(), \
                        "vtx abs: ", gen_particle[tr.genpartIndex()-1].vertex().r()

        # exit()
