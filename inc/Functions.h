#include "TLorentzVector.h"
#include "Math/VectorUtil.h"

const std::map<unsigned int, unsigned int> dm_encode = { // dm finder encode
    {0, 1},                 // oneProng 0Pi0
    {1, 2}, {2, 2}, {3, 2}, // oneProng Pi0s
    {10,3},                 // 3Prong 0Pi0
    {11,4}, {12,4},         // 3Prong Pi0s
    {5, 0}, {6, 0},         // 2Prong Decays (Other)
};

const int gen_dm_encode (unsigned int nCharged, unsigned int nNutral) // gen encode
{
  switch (nCharged) {
       case 1:
          if(nNutral==0) return 1;  // oneProng 0Pi0
          else return 2;            // oneProng Pi0s
          break;
       case 3:
          if(nNutral==0) return 3;    // 3Prong 0Pi0
          else return 4;              // 3Prong Pi0s
          break;
       case 2:
          return 0; // 2Prong Decays (Other)
          break;
       case 5:
          return 0; // rare 5 prongs (Other)
          break;
       case 4:
          return 0; // rare 5 prongs (Other)
          break;
  }
  std::cout << "nCharged: " << nCharged << " nNutral: " << nNutral << std::endl;
  throw std::runtime_error("Error! Decay mode does not exists!");
  return 0;
}

bool dR_calc( const TLorentzVector& p4_1, const TLorentzVector& p4_2)
{
  float dr = 0.2;

  float dr_new = ROOT::Math::VectorUtil::DeltaR( p4_1, p4_2 );

  if(dr_new <= dr) return true;
  else return false;
}