from DataFormats.FWLite import Events, Handle
import ROOT
import numpy as np


def isFrom(object_part, pdgId):
    mother = object_part.mother(0)
    # print "pdgId:", object_part.pdgId(), object_part.pt(), "xy:",object_part.vertex().x(), object_part.vertex().y()
    if mother:
        if abs(mother.pdgId()) == pdgId:
            return True
        else:
            return isFrom(mother, pdgId)
    else:
        return False


if __name__ == '__main__':

    files = ['/afs/desy.de/user/m/mykytaua/STAU_test_300.root']

    # x: displacement [cm], y: SimVertex-GenVertex [cm]
    from_stau_xy = [[], []]
    all_xy = [[], []]

    for f_name in files:

        print "FILE: ", f_name

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
        labelsHits = ["TrackerHitsPixelBarrelHighTof",
                      "TrackerHitsPixelBarrelLowTof",
                      "TrackerHitsPixelEndcapHighTof",
                      "TrackerHitsPixelEndcapLowTof"]

        n_ev = 0
        for n_ev, ev in enumerate(events):
            print "event: ", n_ev
            if n_ev % 1000 == 0:
                print n_ev, "events"
            # if n_ev > 2000:
            #     break

            ev.getByLabel(labelGEN, handleGEN)
            gen_particle = handleGEN.product()

            ev.getByLabel(labelTracks, handleTracks)
            tracks = handleTracks.product()

            ev.getByLabel(labelVertex, handleVertex)
            vertex = handleVertex.product()

            # for gen in gen_particle:
            #     # if gen.vertex().rho() > 100.0:
            #     if isFrom(gen,1000015):
            #         print gen.pdgId()
            # mother = gen.mother()
            # if mother:
            #     print mother.pdgId()

            # len_ = len(gen_particle)
            # print(len(tracks), len(vertex))
            for tr in tracks:
                '''
                This part checks:
                1.  If there is a track which coresponds to genParticle
                    with transverse vertex position larger than  dis_transv [cm]
                    (also added condition that momentum points outside the cms tracker)
                2.  If there is a track which coresponds to stau (pdgId == 1000015)
                '''

                if (not tr.noVertex()) and (not tr.noGenpart()):

                    dist = (vertex[tr.vertIndex()].position().x(
                            )-gen_particle[tr.genpartIndex()-1].vertex().x())**2
                    dist += (vertex[tr.vertIndex()].position().y() -
                             gen_particle[tr.genpartIndex()-1].vertex().y())**2
                    dist += (vertex[tr.vertIndex()].position().z() -
                             gen_particle[tr.genpartIndex()-1].vertex().z())**2
                    dist = np.sqrt(dist)
                    
                    if dist>0.05:
                        if isFrom(gen_particle[tr.genpartIndex()-1],1000015):
                            from_stau_xy[0].append(
                                gen_particle[tr.genpartIndex()-1].eta())
                            from_stau_xy[1].append(gen_particle[tr.genpartIndex()-1].pt())
                        else:
                            all_xy[0].append(abs(gen_particle[tr.genpartIndex()-1].eta()))
                            all_xy[1].append(gen_particle[tr.genpartIndex()-1].pt())

                    # if abs(gen_particle[tr.genpartIndex()-pl].pdgId())==11:
                    #     from_stau_xy[0].append(gen_particle[tr.genpartIndex()-1].vertex().rho())
                    #     from_stau_xy[1].append(dist)
                    # else:
                    #     all_xy[0].append(gen_particle[tr.genpartIndex()-1].vertex().rho())
                    #     all_xy[1].append(dist)

            # raw_input("stop")

    stau_tgraph = ROOT.TGraph(len(from_stau_xy[0]), np.array(
        from_stau_xy[0]), np.array(from_stau_xy[1]))
    stau_tgraph.SetMarkerStyle(8)
    stau_tgraph.SetMarkerSize(0.5)
    stau_tgraph.SetMarkerColor(3)

    all_tgraph = ROOT.TGraph(len(all_xy[0]), np.array(all_xy[0]), np.array(all_xy[1]))
    all_tgraph.GetXaxis().SetTitle("|#eta|")
    all_tgraph.GetYaxis().SetTitle("pt [GeV]")
    # all_tgraph.GetXaxis().SetRangeUser(0, 5.0)
    # all_tgraph.GetYaxis().SetRangeUser(0, 500.0)
    all_tgraph.SetMarkerStyle(8)
    all_tgraph.SetMarkerSize(0.5)
    all_tgraph.SetMarkerColor(4)

    c = ROOT.TCanvas("c", "c", 1000, 800)

    c.SetLogy()
    all_tgraph.SetMaximum(500)
    all_tgraph.SetMinimum(0.1)

    stau_tgraph.SetMaximum(500)
    stau_tgraph.SetMinimum(0.1)

    all_tgraph.Draw("ap")
    stau_tgraph.Draw("p")

    legend = ROOT.TLegend(0.6, 0.8, 0.95, 0.95)
    legend.AddEntry(stau_tgraph, "stau decay chain", "p")
    legend.AddEntry(all_tgraph, "other particles", "p")
    legend.Draw("same")

    # tau_tgraph = ROOT.TGraph(len(from_stau_xy[0]), np.array(from_stau_xy[0]), np.array(from_stau_xy[1]))
    # stau_tgraph.SetMarkerStyle(20)
    # stau_tgraph.SetMarkerSize(0.5)
    # stau_tgraph.SetMarkerColor(2)

    # all_tgraph = ROOT.TGraph(len(all_xy[0]), np.array(all_xy[0]), np.array(all_xy[1]))
    # all_tgraph.GetXaxis().SetTitle("Transverse Displacment [cm]")
    # all_tgraph.GetYaxis().SetTitle("|#vec{SimVertex}-#vec{GenVertex}|")
    # all_tgraph.GetXaxis().SetRangeUser(0, 10.0)
    # all_tgraph.GetYaxis().SetRangeUser(0, 2.0)
    # all_tgraph.SetMarkerStyle(20)
    # all_tgraph.SetMarkerSize(0.5)
    # all_tgraph.SetMarkerColor(4)

    # c = ROOT.TCanvas()
    # all_tgraph.Draw("ap")
    # stau_tgraph.Draw("p")

    # legend = ROOT.TLegend(0.6,0.75,1.0,1.0)
    # legend.AddEntry(stau_tgraph,"electrons","p")
    # legend.AddEntry(all_tgraph,"other particles","p")
    # legend.Draw("same")

    c.Print("GEN-SIMvtx_pteta_stau_color.pdf")

