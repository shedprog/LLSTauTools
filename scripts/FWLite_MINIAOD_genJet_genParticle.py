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
    files = ['/pnfs/desy.de/cms/tier2/store/user/myshched/mc/UL2018-pythia-v5-100cm/SUS-RunIISummer20UL18GEN-stau100_lsp1_ctau100mm_v5/MiniAOD/220525_205521/0000/SUS-RunIISummer20UL18MiniAODv2-LLStau_10.root']

    for f_name in files:
        
        print "FILE: ",f_name

        events = Events(f_name)

        # Gen par info
        handleGENjet = Handle('std::vector<reco::GenJet>')
        labelGENjet = 'slimmedGenJets'
        
        handleGEN = Handle('std::vector<reco::GenParticle>')
        labelGEN = 'genParticlePlusGeant'
        
	for ev in events:

            ev.getByLabel(labelGENjet, handleGENjet)
            genJets = handleGENjet.product()           

            ev.getByLabel(labelGEN, handleGEN)
            gen_particle = handleGEN.product()
            
            for gen in gen_particle:

                # if abs(gen.pdgId())==1000015 and gen.statusFlags().isLastCopy():
                #     PrintDecay(gen,"","")

                if abs(gen.pdgId())==15 and abs(gen.motherRef().pdgId())!=15:
                    PrintDecay(gen.motherRef(),"","")
	    
	    for genJet in genJets:

                    print "genJet.pt=", genJet.pt(), "genJet.eta=", genJet.eta()

		    n_part = genJet.numberOfDaughters()
		    for part_idx in range(n_part):
			    par = genJet.daughter(part_idx)
    			    print "pdgId:", par.pdgId(), \
    			          "pt:", par.pt(), \
    			          "vtx rho:", par.vx(), \
    			          "vtx abs:", par.vy(), \
    			          "status:", par.status()
            raw_input("stop")
