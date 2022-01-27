from DataFormats.FWLite import Events, Handle
import ROOT
import numpy as np

def PrintDecay(par, indent, d_indent):
    print indent + \
        "+->pdgId:", par.pdgId(), \
        "pt:", par.pt(), \
        "vtx rho:", par.vertex().rho(), \
        "vtx abs:", par.vertex().r(), \
        "status:", par.status(), "" if par.status()!=8 else "<---"
    

    daughters = par.daughterRefVector()
    size = daughters.size()
    for i, child in enumerate(daughters):
        s = '|' if i<size-1 else ' '
        PrintDecay(child, indent + d_indent + "  ", s)

if __name__ == '__main__':
    
    # files = ['/afs/cern.ch/user/m/myshched/STauGENProduction/test_prod_HNL/EXO-RunIIFall18wmLHEGS-00889.root']
    files = ['/afs/cern.ch/user/m/myshched/STauGENProduction/LLSTauProduction20UL18_test/script/SUS-RunIIFall18GS-00022.root']

    for f_name in files:
        
        print "FILE: ",f_name

        events = Events(f_name)

        # Gen par info
        handleGEN = Handle('std::vector<reco::GenParticle>')
        labelGEN = 'genParticlePlusGeant'

        n_ev = 0
        for n_ev, ev in enumerate(events):
            print "event: ", n_ev
            if n_ev % 1000 == 0:
                print n_ev, "events"

            ev.getByLabel(labelGEN, handleGEN)
            gen_particle = handleGEN.product()

            for gen in gen_particle:

                # if abs(gen.pdgId())==1000015 and gen.statusFlags().isLastCopy():
                #     PrintDecay(gen,"","")

                if abs(gen.pdgId())==15 and abs(gen.motherRef().pdgId())!=15:
                    PrintDecay(gen.motherRef(),"","")


            raw_input("stop")
