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
    
    path = '/pnfs/desy.de/cms/tier2/store/user/myshched/mc/UL2018-pythia-v4/SUS-RunIISummer20UL18GEN-stau400_lsp1_ctau1000mm_v4/MiniAOD/220129_220038/0000/'
    files = glob.glob(path+'/*.root')

    for f_name in files:
        
        print "FILE: ",f_name
        events = Events(f_name)

        # Gen par info
        handleGEN = Handle('std::vector<reco::GenParticle>')
        labelGEN = 'prunedGenParticles'

        statuses = []
        expected_case = 0
        other_cases = 0
        for n_ev, ev in enumerate(events):

            ev.getByLabel(labelGEN, handleGEN)
            gen_particle = handleGEN.product()

            for gen in gen_particle:
                
                if abs(gen.pdgId())==15:
                    statuses.append(gen.status())
                
                if abs(gen.pdgId())==15 and gen.status()==23:

                    normal_case = True
                    ref = gen.daughterRefVector()
                    for d in ref:
                        if d.pdgId()==22 or abs(d.pdgId())==15 or abs(d.pdgId())==11:
                            normal_case = True
                        else:
                            PrintDecay(gen.motherRef(), "", "")
                            normal_case = False
                            break

                    if abs(gen.motherRef().pdgId())==1000015 and normal_case:
                        expected_case=expected_case+1
                    else:
                        other_cases=other_cases+1

                # if abs(gen.pdgId())==15 and abs(gen.motherRef().pdgId())!=15:
                # if(abs(gen.pdgId())==15 and gen.status()==91):
                    # PrintDecay(gen.motherRef(), "", "")
                    # raw_input("stop")

        print(set(statuses), expected_case, other_cases)
