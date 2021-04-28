from DataFormats.FWLite import Events, Handle
import ROOT
import numpy as np

if __name__ == '__main__':

    files = ['/afs/cern.ch/user/m/myshched/STauGENProduction/test_prod_my/SUS-RunIIFall18GS-00022.root']
    # files = ['/afs/cern.ch/user/m/myshched/STauGENProduction/test_prod_T1qqqq/SUS-RunIISummer15GS-00239.root']
    # files = ['root://cmsxrootd.fnal.gov//store/mc/RunIIFall17GS/ADDGravToGG_NegInt-0_LambdaT-10000_M-1000To2000_TuneCP2_13TeV-pythia8/GEN-SIM/93X_mc2017_realistic_v3-v1/90000/042BDB3E-0E0E-E911-91E3-EC0D9A0B3080.root']

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


            ev.getByLabel(labelGEN, handleGEN)
            gen_particle = handleGEN.product()

            ev.getByLabel(labelTracks, handleTracks)
            tracks = handleTracks.product()

            ev.getByLabel(labelVertex, handleVertex)
            vertex = handleVertex.product()

            Tracker_nHits = np.zeros((4,10000000), dtype=int)
            for i, label in enumerate(labelsHits):
                '''
                In this part, hits inside PIXEL tracker
                are accumulated
                '''
                ev.getByLabel(labelTracks, label, handleHits)
                hits = handleHits.product()
                for hit in hits:
                    Tracker_nHits[i][hit.trackId()]+=1


            # for gen in gen_particle:
            #     # if(gen.vertex().r()>=10.0):
            #     print "pdgId:", gen.pdgId(), \
            #         "pt:", gen.pt(), \
            #         "vtx rho:", gen.vertex().rho(), \
            #         "vtx abs:", gen.vertex().r()
            
            for tr in tracks:
                '''
                This part checks:
                1.  If there is a track which coresponds to genParticle
                    with transverse vertex position larger than  dis_transv [cm]
                    (also added condition that momentum points outside the cms tracker)
                2.  If there is a track which coresponds to stau (pdgId == 1000015)
                '''

                if (not tr.noVertex()) and (not tr.noGenpart()):

                    if(round(vertex[tr.vertIndex()].position().x(),2)!=round(gen_particle[tr.genpartIndex()-1].vertex().x(),2) \
                       or round(vertex[tr.vertIndex()].position().y(),2)!=round(gen_particle[tr.genpartIndex()-1].vertex().y(),2) \
                       or round(vertex[tr.vertIndex()].position().z(),2)!=round(gen_particle[tr.genpartIndex()-1].vertex().z(),2)):
                            if(gen_particle[tr.genpartIndex()-1].pdgId()!=22): # skip gammas
                                print "vertex does not match: ", "pdgId:", gen_particle[tr.genpartIndex()-1].pdgId()
                                print "vertIndex: ", vertex[tr.vertIndex()].position().x(), \
                                                    vertex[tr.vertIndex()].position().y(), \
                                                    vertex[tr.vertIndex()].position().z()
                                print "genPart: ", gen_particle[tr.genpartIndex()-1].vertex().x(), \
                                                gen_particle[tr.genpartIndex()-1].vertex().y(), \
                                                gen_particle[tr.genpartIndex()-1].vertex().z()
                
                dis_transv = 500.0 #cm

                if not tr.noGenpart():

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

                    if(abs(gen_particle[tr.genpartIndex()-1].pdgId())>=1000000):

                        print "stau particle track!: ~~~~~~~~~~~~> ", \
                            "pdgId: ", gen_particle[tr.genpartIndex()-1].pdgId(), \
                            "vtx rho: ", gen_particle[tr.genpartIndex()-1].vertex().rho(), \
                            "vtx abs: ", gen_particle[tr.genpartIndex()-1].vertex().r(), \
                            "PixelBarrelHighTof:", Tracker_nHits[0][tr.trackId()], \
                            "PixelBarrelLowTof:", Tracker_nHits[1][tr.trackId()], \
                            "PixelEndcapHighTof:", Tracker_nHits[2][tr.trackId()], \
                            "PixelEndcapLowTof:", Tracker_nHits[3][tr.trackId()]

            raw_input("stop")
