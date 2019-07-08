//This namespace implements the pt cone correction for kinematic variables during the implementation of fake rate estimated backgrounds
//to compile, run in ROOT once:
//gROOT->ProcessLine(".L modules/pt_ConeCorrection.h+");

#include "TLorentzVector.h"
#include <algorithm>
using namespace std;

namespace pt_ConeCorrection{
    double pCone( double p, double relIso){
        return p * std::max(1.0, 1.0 + relIso - 0.2);
    }
    double dimass(double l1_px, double l1_py, double l1_pz, double l1_e, double l2_px, double l2_py, double l2_pz, double l2_e){
        TLorentzVector v1;
        TLorentzVector v2;
        v1.SetPxPyPzE(l1_px,l1_py,l1_pz,l1_e);
        v2.SetPxPyPzE(l2_px,l2_py,l2_pz,l2_e);
        TLorentzVector v3;
        v3=v1+v2;
        return  v3.M();
    }
}

