from DataFormats.FWLite import Events, Handle
import ROOT
import numpy as np
import glob

def PrintDecay(par, indent, d_indent):

    print indent + \
        "+->pdgId:", par.pdgId(), \
        "pt:", par.pt(), \
        "vtx rho:", par.vertex().rho(), \
        "vtx abs:", par.vertex().r(), \
        "status:", par.status(), "" if par.status()!=8 else "<---", \
        "final:", par.isLastCopy()

    daughters = par.daughterRefVector()
    size = daughters.size()
    for i, child in enumerate(daughters):
        s = '|' if i<size-1 else ' '
        PrintDecay(child, indent + d_indent + "  ", s)

if __name__ == '__main__':
    
    path = '/pnfs/desy.de/cms/tier2/store/user/myshched/SUS-RunIIFall18GS-production-new/SUS-RunIIFall18GS_ctau1000mm_mstau100_250_400_mlsp1_20-MiniAOD/SUS-RunIIFall18GS_ctau1000mm_mstau100_250_400_mlsp1_20-RAWSIM/SUS-RunIIFall18GS_ctau1000mm_mstau100_250_400_mlsp1_20-MiniAOD/210715_153717/0000'
    files = glob.glob(path+'/*.root')

    for f_name in files:
        
        print "FILE: ",f_name
        events = Events(f_name)

        # Gen par info
        handleGEN = Handle('std::vector<reco::GenParticle>')
        labelGEN = 'prunedGenParticles'

        statuses = []
        stau_mother = 0
        other_mother = 0
        for n_ev, ev in enumerate(events):

            ev.getByLabel(labelGEN, handleGEN)
            gen_particle = handleGEN.product()

            for gen in gen_particle:
                
                if abs(gen.pdgId())==15:
                    statuses.append(gen.status())
                
                if abs(gen.pdgId())==15 and gen.status()==23:
                    if abs(gen.motherRef().pdgId())==1000015:
                        stau_mother=stau_mother+1
                    else:
                        other_mother=other_mother+1

                # if abs(gen.pdgId())==15 and abs(gen.motherRef().pdgId())!=15:
                # if(abs(gen.pdgId())==15 and gen.status()==91):
                    # PrintDecay(gen.motherRef(), "", "")
                    # raw_input("stop")
        print(set(statuses), stau_mother, other_mother)