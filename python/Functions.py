

class DataFrameFunc:

    @staticmethod
    def sum_up_var(var: str):
        sum=f'''
        std::vector<size_t> indices(pfCand_pt.size());
        std::iota(indices.begin(), indices.end(), 0);

        // sort PfCands by pt
        std::sort(indices.begin(), indices.end(), [&](size_t a, size_t b) {'{'}
            return pfCand_pt.at(a) > pfCand_pt.at(b);
        {'}'});
        size_t upper_index = indices.size()<50 ? indices.size() : 50;
        float sum = 0.0;
        for(size_t i = 0; i < upper_index; i++) {'{'}
            sum+={var}.at(i);
        {'}'}

        return sum;
        '''
        return sum

    @staticmethod
    def get_gen_info():
        get_kinem='''
        auto genLeptons = 
        reco_tau::gen_truth::GenLepton::fromRootTuple<ROOT::VecOps::RVec>(
                        genLepton_lastMotherIndex,
                        genParticle_pdgId,
                        genParticle_mother,
                        genParticle_charge,
                        genParticle_isFirstCopy,
                        genParticle_isLastCopy,
                        genParticle_pt,
                        genParticle_eta,
                        genParticle_phi,
                        genParticle_mass,
                        genParticle_vtx_x,
                        genParticle_vtx_y,
                        genParticle_vtx_z);
        const reco_tau::gen_truth::LorentzVectorXYZ&
            visP4 = genLeptons.visibleP4();
        const reco_tau::gen_truth::Point3D&
            vtx = reco_tau::gen_truth::GenLepton::getPartVertex(genLeptons, 15);
        const reco_tau::gen_truth::LorentzVectorM&
            stauP4 = reco_tau::gen_truth::GenLepton::getPartP4(genLeptons, 1000015);

        return std::make_tuple(visP4, vtx, stauP4);
        '''
        return get_kinem

    # def gen_jet_match():
    #     '''
    #     const reco_tau::gen_truth::LorentzVectorM& jetP4 = 