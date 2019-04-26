#include <iostream>
#include <ROOT/RDataFrame.hxx>

#include "TCanvas.h"
#include "TLegend.h"
#include "TH2D.h"
#include "TH1D.h"
#include "TF1.h"
#include "TFile.h"
#include "THStack.h"
#include "TGraphErrors.h"

using namespace std;

const string plotDir = "/eos/user/v/vstampf/plots/DDE/";

/*
int len (ARRAY) {
int size = *(&ARRAY + 1) - ARRAY;
return size; }
*/

int main (){

ROOT::EnableImplicitMT(); // Tell ROOT you want to go parallel

const Double_t b_eta_mu [4] = {0., 1.2, 2.1, 2.4}; 
const Double_t b_eta_ele[4] = {0., 0.8, 1.479, 2.5};
const Double_t b_pt     [9] = {0., 5., 10., 15., 20., 25., 35., 50., 70.};
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
///// ENERGY-IN-CONE CORRECTED PT
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
const string PTCONE   = "(  ( hnl_hn_vis_pt * (hnl_iso04_rel_rhoArea<0.2) ) + ( (hnl_iso04_rel_rhoArea>=0.2) * ( hnl_hn_vis_pt * (1. + hnl_iso04_rel_rhoArea - 0.2) ) )  )";
const string PTCONEL1 = "(  ( l1_pt         * (l1_reliso_rho_04<0.2) )      + ( (l1_reliso_rho_04>=0.2)      * ( l1_pt         * (1. + l1_reliso_rho_04 - 0.2) ) )  )";
const string PTCONEL2 = "(  ( l2_pt         * (l2_reliso_rho_04<0.2) )      + ( (l2_reliso_rho_04>=0.2)      * ( l2_pt         * (1. + l2_reliso_rho_04 - 0.2) ) )  )";
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////// FAKEABLE OBJECTS AND PROMPT LEPTON DEFINITIONS
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////// PROMPT LEPTONS
const string l0_m = "l0_pt > 25 && abs(l0_eta) < 2.4 && abs(l0_dz) < 0.2 && abs(l0_dxy) < 0.05 && l0_reliso_rho_04 < 0.2 && l0_id_m == 1";                  // l0 genuine muon
const string l1_m = "l1_pt > 10 && abs(l1_eta) < 2.4 && abs(l1_dz) < 0.2 && abs(l1_dxy) < 0.05 && l1_reliso_rho_04 < 0.2 && l1_id_m == 1";                  // l1 genuine muon 
const string l2_m = "l2_pt > 10 && abs(l2_eta) < 2.4 && abs(l2_dz) < 0.2 && abs(l2_dxy) < 0.05 && l2_reliso_rho_04 < 0.2 && l2_id_m == 1";                  // l2 genuine muon 

const string l0_e = "l0_pt > 25 && abs(l0_eta) < 2.5 && abs(l0_dz) < 0.2 && abs(l0_dxy) < 0.05 && l0_reliso_rho_04 < 0.2 && l0_eid_mva_iso_wp90 == 1";      // l0 genuine electron
const string l1_e = "l1_pt > 10 && abs(l1_eta) < 2.5 && abs(l1_dz) < 0.2 && abs(l1_dxy) < 0.05 && l1_reliso_rho_04 < 0.2 && l1_eid_mva_iso_wp90 == 1";      // l1 genuine electron 
const string l2_e = "l2_pt > 10 && abs(l2_eta) < 2.5 && abs(l2_dz) < 0.2 && abs(l2_dxy) < 0.05 && l2_reliso_rho_04 < 0.2 && l2_eid_mva_iso_wp90 == 1";      // l2 genuine electron 

////// FAKEABLE OBJECTS
const string l1_m_loose  = "l1_pt > 5 && abs(l1_eta) < 2.4 && abs(l1_dz) < 2 && abs(l1_dxy) > 0.05";                                              // l1 kinematics and impact parameter
const string l1_m_tight  = l1_m_loose + " &&  l1_Medium == 1 && l1_reliso_rho_04 < 0.2";
const string l1_m_lnt    = l1_m_loose + " && (l1_Medium == 0 || l1_reliso_rho_04 > 0.2)";

const string l2_m_loose  = "l2_pt > 5 && abs(l2_eta) < 2.4 && abs(l2_dz) < 2 && abs(l2_dxy) > 0.05";                                              // l2 kinematics and impact parameter
const string l2_m_tight  = l2_m_loose + " &&  l2_Medium == 1 && l2_reliso_rho_04 < 0.2";
const string l2_m_lnt    = l2_m_loose + " && (l2_Medium == 0 || l2_reliso_rho_04 > 0.2)";

const string l1_e_loose  = "l1_pt > 5 && abs(l1_eta) < 2.5 && abs(l1_dz) < 2 && abs(l1_dxy) > 0.05";                                              // l1 kinematics and impact parameter
const string l1_e_tight  = l1_e_loose + " &&  l1_MediumNoIso == 1 && l1_reliso_rho_04 < 0.2";
const string l1_e_lnt    = l1_e_loose + " && (l1_MediumNoIso == 0 || l1_reliso_rho_04 > 0.2)";

const string l2_e_loose  = "l2_pt > 5 && abs(l2_eta) < 2.5 && abs(l2_dz) < 2 && abs(l2_dxy) > 0.05";                                              // l2 kinematics and impact parameter
const string l2_e_tight  = l2_e_loose + " &&  l2_MediumNoIso == 1 && l2_reliso_rho_04 < 0.2";
const string l2_e_lnt    = l2_e_loose + " && (l2_MediumNoIso == 0 || l2_reliso_rho_04 > 0.2)";
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//              #//                 DOUBLE FAKE RATE                   #//  
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////// DFR:: LOOSE CUTS OBTAINED THROUGH CDF HEAVY/LIGHT COMPARISON 
string DFR_MMM_L_CUT = "";
string DFR_MEM_L_CUT = " && hnl_iso04_rel_rhoArea < 0.6";
 
////// DFR::MMM 
string DFR_MMM_L   =  l0_m + " && " + l1_m_loose + " && " + l2_m_loose; 
       DFR_MMM_L   += " && hnl_q_12 == 0";                                  // opposite charge 
       DFR_MMM_L   += DFR_MMM_L_CUT;                                        // reliso bound for LOOSE cf. checkIso_mmm_220319
string DFR_MMM_LNT =  DFR_MMM_L + " && ";  // FIXME                          
string DFR_MMM_T   =  DFR_MMM_L + " && " + l1_m_tight + " && " + l2_m_tight;

////// DFR::MMM 
string DFR_MEM_L   =  l0_m + " && " + l1_e_loose + " && " + l2_m_loose; 
       DFR_MEM_L   += " && hnl_q_12 == 0";                                  // opposite charge 
       DFR_MEM_L   += DFR_MEM_L_CUT;                                        // reliso bound for LOOSE cf. checkIso_mmm_220319
string DFR_MEM_LNT =  DFR_MEM_L + " && ";  // FIXME                          
string DFR_MEM_T   =  DFR_MEM_L + " && " + l1_e_tight + " && " + l2_m_tight;
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//              #//                 SINGLE FAKE RATE                   #//  
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////// SFR:: LOOSE CUTS OBTAINED THROUGH CDF HEAVY/LIGHT COMPARISON 
string SFR_MMM_L_CUT_021 = " && ( (l1_reliso_rho_03 < 0.42 && abs(l1_eta) < 1.2) || (l1_reliso_rho_03 < 0.35 && abs(l1_eta) > 1.2) )";
string SFR_MMM_L_CUT_012 = " && ( (l2_reliso_rho_03 < 0.42 && abs(l2_eta) < 1.2) || (l2_reliso_rho_03 < 0.35 && abs(l2_eta) > 1.2) )";
string SFR_MEM_L_CUT = " && ( (l1_reliso_rho_03 < 0.6  && abs(l1_eta) < 0.8) || (l1_reliso_rho_03 < 0.35 && abs(l1_eta) > 0.8) )";

////// SFR::MMM 
string SFR_MMM_021_L   =  l0_m + " && " + l2_m + " && " + l1_m_loose; 
       SFR_MMM_021_L   += " && hnl_q_02 == 0";                                        // opposite charge 
       SFR_MMM_021_L   += SFR_MMM_L_CUT_021;                                    // reliso bound for LOOSE cf. checkIso_mmm_220319 
string SFR_MMM_021_LNT =  SFR_MMM_021_L + " && " + l1_m_lnt;
string SFR_MMM_021_T   =  SFR_MMM_021_L + " && " + l1_m_tight; 

string SFR_MMM_012_L   =  l0_m + " && " + l1_m + " && " + l2_m_loose; 
       SFR_MMM_012_L   += " && hnl_q_01 == 0";                    // opposite charge 
       SFR_MMM_012_L   += SFR_MMM_L_CUT_012;                // reliso bound for LOOSE cf. checkIso_mmm_220319 
string SFR_MMM_012_LNT =  SFR_MMM_012_L + " && " + l2_m_lnt;
string SFR_MMM_012_T   =  SFR_MMM_012_L + " && " + l2_m_tight; 


string fDYBB     = "/eos/user/d/dezhu/HNL/ntuples/HN3Lv2.0/background/montecarlo/production20190318/mmm/ntuples/DYBB/HNLTreeProducer/tree.root";
string fDY50     = "/eos/user/d/dezhu/HNL/ntuples/HN3Lv2.0/background/montecarlo/production20190318/mmm/ntuples/DYJetsToLL_M50/HNLTreeProducer/tree.root";
string fDY50_ext = "/eos/user/d/dezhu/HNL/ntuples/HN3Lv2.0/background/montecarlo/production20190318/mmm/ntuples/DYJetsToLL_M50_ext/HNLTreeProducer/tree.root";
string fTT       = "/eos/user/d/dezhu/HNL/ntuples/HN3Lv2.0/background/montecarlo/production20190318/mmm/ntuples/TTJets_ext/HNLTreeProducer/tree.root";
string data_B    = "root://cms-xrd-transit.cern.ch//store/user/dezhu/2_ntuples/HN3Lv2.0/mmm/data/Single_mu_2017B/HNLTreeProducer/tree.root";

//ROOT::RDataFrame df("tree", {fDYBB, fDY50, fDY50_ext, fTT});

ROOT::RDataFrame df("tree", data_B);

cout << "\n\t total entries: " << df.Count().GetValue() << endl;

////// GENERAL 
const string * ptconel1 = &PTCONEL1;
const string * ptconel2 = &PTCONEL2;

string cuts_FR = "hnl_dr_12 > 0.3";

string cuts_FR_012 = cuts_FR + " && " + SFR_MMM_012_L;
string cuts_FR_021 = cuts_FR + " && " + SFR_MMM_021_L;
string * tight_021 = &SFR_MMM_021_T;
string * tight_012 = &SFR_MMM_012_T;
bool mode012 = true;
bool mode021 = true;

cout << "\n\tcuts: "  << cuts_FR << endl;
const Double_t (*b_eta) [4] = & b_eta_mu;


auto h_pt_eta_T_012 = TH2D("pt_eta_T_012","pt_eta_T_012", 3, b_pt, 8, *b_eta);
auto h_pt_eta_L_012 = TH2D("pt_eta_L_012","pt_eta_L_012", 3, b_pt, 8, *b_eta);

auto h_pt_eta_T_021 = TH2D("pt_eta_T_021","pt_eta_T_021", 3, b_pt, 8, *b_eta);
auto h_pt_eta_L_021 = TH2D("pt_eta_L_021","pt_eta_L_021", 3, b_pt, 8, *b_eta);

if (mode021 == true) {

    auto f0_021 = df.Filter(cuts_FR_021);

    cout << "\n\tf0_021 entries: " << f0_021.Count().GetValue() << endl;

    auto df0_021 = f0_021.Define("ptcone021", *ptconel1);
    cout << "\n\tptcone021 defined." << endl;
    
    auto dfL_021 = df0_021.Define("abs_l1_eta", "abs(l1_eta)");
    cout << "\n\tabs_l1_eta defined." << endl;
    
    auto dfT_021 = dfL_021.Filter(*tight_021);
    cout << "\n\ttight df_021 defined." << endl;

    cout << "\n\tloose 021: "        <<  (cuts_FR_021) << endl;
    cout << "\n\ttight 021: "        << *tight_021 << endl;
    cout << "\n\ttotal loose 021: "  <<  f0_021.Count().GetValue() << endl;

    auto     _pt_eta_T_021 = dfT_021.Histo2D({"pt_eta_T_021","pt_eta_T_021", 3, b_pt, 8, *b_eta}, "ptcone021","abs_l1_eta");
    auto     _pt_eta_L_021 = dfL_021.Histo2D({"pt_eta_L_021","pt_eta_L_021", 3, b_pt, 8, *b_eta}, "ptcone021","abs_l1_eta");
 
    h_pt_eta_T_021.Add(_pt_eta_T_021.GetPtr());
    h_pt_eta_L_021.Add(_pt_eta_L_021.GetPtr());
    }

if (mode012 == true) {

    auto f0_012 = df.Filter(cuts_FR_012);

    cout << "\n\tf0_012 entries: " << f0_012.Count().GetValue() << endl;

    auto df0_012 = f0_012.Define("ptcone012", *ptconel2);
    cout << "\n\tptcone012 defined." << endl;
    
    auto dfL_012 = df0_012.Define("abs_l2_eta", "abs(l2_eta)");
    cout << "\n\tabs_l1_eta defined." << endl;
    
    auto dfT_012 = dfL_012.Filter(*tight_012);
    cout << "\n\ttight df_012 defined." << endl;

    cout << "\n\tloose 012: "       <<  cuts_FR_012 << "\n" << endl;
    cout << "\n\ttight 012: "       << * tight_012   << "\n" << endl;
    cout << "\n\ttotal loose 012: " <<  f0_012.Count().GetValue() << endl;

    auto     _pt_eta_T_012 = dfT_012.Histo2D({"pt_eta_T_012","pt_eta_T_012", 3, b_pt, 8, *b_eta}, "ptcone012","abs_l2_eta");
    auto     _pt_eta_L_012 = dfL_012.Histo2D({"pt_eta_L_012","pt_eta_L_012", 3, b_pt, 8, *b_eta}, "ptcone012","abs_l2_eta");

    h_pt_eta_T_012.Add(_pt_eta_T_012.GetPtr());
    h_pt_eta_L_012.Add(_pt_eta_L_012.GetPtr());
    }

h_pt_eta_T_012.Add(&h_pt_eta_T_021);
h_pt_eta_L_012.Add(&h_pt_eta_L_021);

cout << "\n\tentries T && L: " << h_pt_eta_T_012.GetEntries() << ", " << h_pt_eta_L_012.GetEntries() << endl;

auto c_pt_eta = TCanvas("ptCone_eta", "ptCone_eta");
h_pt_eta_T_012.Divide(&h_pt_eta_L_012);
h_pt_eta_T_012.Draw("colztextE");
h_pt_eta_T_012.SetAxisRange(0.,70,"X");
h_pt_eta_T_012.SetTitle("; p_{T}^{cone} [GeV]; DiMuon |#eta|; tight-to-loose ratio");
c_pt_eta.SaveAs("/eos/user/v/vstampf/plots/DDE/DATA_T2Lratio_mmm_eta_ptcone.root");
c_pt_eta.SaveAs("/eos/user/v/vstampf/plots/DDE/DATA_T2Lratio_mmm_eta_ptcone.pdf");
c_pt_eta.SaveAs("/eos/user/v/vstampf/plots/DDE/DATA_T2Lratio_mmm_eta_ptcone.png");

//    f0.Snapshot("")
return 0;
    }

/*
#include <iostream>

#include "TCanvas.h"
#include "TLegend.h"
#include "TH2D.h"
#include "TH1D.h"
#include "TF1.h"
#include "TFile.h"
#include "THStack.h"
#include "TGraphErrors.h"
#include "TGraphErrors.h"


std::string getCutLabel( float theMin, float theMax, const std::string& name, const std::string& units="" );



int main( int argc, char* argv[] ) {


  if( argc<2 ) {
    std::cout << "USAGE: ./drawDataMC [configFileName] [lumi/shape]" << std::endl;
    std::cout << "Exiting." << std::endl;
    exit(11);
  }


  MT2DrawTools::setStyle();

  std::string configFileName(argv[1]);
  MT2Config cfg(configFileName);

  bool shapeNorm = false;
  if( argc>2 ) {
    std::string normType(argv[2]);
    if( normType=="lumi" ) shapeNorm=false;
    else if( normType=="shape" ) shapeNorm=true;
    else {
      std::cout << "-> Only "lumi" and "shape" are supported normTypes." << std::endl;
      exit(17);
    }
  }


  if( shapeNorm )
    std::cout << "-> Using shape normalization." << std::endl;
  else
    std::cout << "-> Using lumi normalization." << std::endl;


  std::string mcFile = cfg.getEventYieldDir() + "/analyses.root";
  std::string dataFile = cfg.getEventYieldDir() + "/analyses.root";

  MT2Analysis<MT2EstimateTree>* zjets = MT2Analysis<MT2EstimateTree>::readFromFile(mcFile, "ZJets");
  zjets->setFullName("Z+Jets");
  zjets->setColor(kZJets);

  MT2Analysis<MT2EstimateTree>* wjets = MT2Analysis<MT2EstimateTree>::readFromFile(mcFile, "WJets");
  wjets->setFullName("W+Jets");
  wjets->setColor(kWJets);

  MT2Analysis<MT2EstimateTree>* top   = MT2Analysis<MT2EstimateTree>::readFromFile(mcFile, "Top");
  top->setFullName("Top");
  top->setColor(kTop);

  MT2Analysis<MT2EstimateTree>* qcd   = MT2Analysis<MT2EstimateTree>::readFromFile(mcFile, "QCD");
  qcd->setFullName("QCD");
  qcd->setColor(kQCD);

  MT2Analysis<MT2EstimateTree>* data = MT2Analysis<MT2EstimateTree>::readFromFile(dataFile, "data");
  data->setFullName("Data");

  std::vector< MT2Analysis<MT2EstimateTree>* > mc;
  mc.push_back(qcd);
  mc.push_back(wjets);
  mc.push_back(zjets);
  mc.push_back(top);

  std::string plotsDir = cfg.getEventYieldDir() + "/plotsDataMC";
  if( shapeNorm ) plotsDir += "_shape";


  MT2DrawTools dt(plotsDir, cfg.lumi() );
  dt.set_shapeNorm( shapeNorm );

  dt.set_data( data );
  dt.set_mc( &mc );

}

//\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
//
def map_FR(ch="mem",mode="sfr",isData=True):

    sfr = False; dfr = False
    if mode == "sfr": sfr = True
    if mode == "dfr": dfr = True

    plotDir = makeFolder("map_FR_%s"%ch)
    cout << "\n\tplotDir: ", plotDir << endl;
    sys.stdout = Logger(plotDir + "map_FR_%s" %ch)

    mode021 = False; mode012 = False; mshReg = ""
    cuts_FR_021 = ""; cuts_FR_012 = ""
    input = "MC"
    if isData == True: input = "DATA"

    //// PREPARE CUTS AND FILES
    SFR, DFR, dirs = selectCuts(ch)

    SFR_021_L, SFR_012_L, SFR_021_LNT, SFR_012_LNT, SFR_021_T, SFR_012_T = SFR 
    DFR_L, DFR_T, DFR_LNT = DFR
    DYBB_dir, DY10_dir, DY50_dir, DY50_ext_dir, TT_dir, W_dir, W_ext_dir = dirs   

    dRdefList, sHdefList = selectDefs(ch)

    l0_is_fake, no_fakes, one_fake_xor, two_fakes, twoFakes_sameJet = dRdefList
    
    mshReg  = "hnl_w_vis_m > 80"
    mshReg  = "1 == 1"

    if sfr:

        ///// GENERAL 
        ptconel1 = PTCONEL1
        ptconel2 = PTCONEL2
        cout << "\n\tdrawing single fakes ..." << endl;

        cuts_FR = mshReg + " && hnl_dr_12 > 0.3"

        ///// CHANNEL SPECIFIC
        if ch == "eem":
            mode012 = True
            cuts_FR_012 = cuts_FR + " && " + SFR_EEM_012_L
            tight_021 = SFR_EEM_021_T

        if ch == "mmm":
            cuts_FR_012 = cuts_FR + " && " + SFR_MMM_012_L
            cuts_FR_021 = cuts_FR + " && " + SFR_MMM_021_L
            tight_021 = SFR_MMM_021_T
            tight_012 = SFR_MMM_012_T
            mode012 = True
            mode021 = True

        if ch == "mem":

            mode021 = True
            b_eta = b_eta_ele

            cuts_FR_021 =  cuts_FR + " && " + SFR_MEM_021_L 
            cuts_FR_021 += " && hnl_dr_01 > 0.3"                                                        // no conversions, only use this to measure t2l ratio 
            tight_021   = SFR_MEM_021_T

            if isData == False:
                cuts_FR_021  += " && l1_gen_match_pdgid != 22 && label == 1"  // DY50 only

        if ch == "mmm":
            mode021 = True
            mode012 = True
            b_eta = b_eta_mu

            if isData == False:
                cuts_FR_021  += " && l1_gen_match_pdgid != 22"// && label == 1" // DY50 only
                cuts_FR_012  += " && l2_gen_match_pdgid != 22"// && label == 1" // DY50 only

            cuts_FR_012 = cuts_FR + " && " + SFR_MMM_012_L 
            cuts_FR_021 = cuts_FR + " && " + SFR_MMM_021_L 

            cuts_FR_021 += " && hnl_dr_01 > 0.3"                                                        // no conversions, only use this to measure t2l ratio 
            cuts_FR_012 += " && hnl_dr_02 > 0.3"                                                        // no conversions, only use this to measure t2l ratio 

            tight_012   = SFR_MMM_012_T
            tight_021   = SFR_MMM_021_T

    if dfr:

        ///// GENERAL 
        ptconel1 = PTCONE
        cout << "\n\tdrawing double fakes ..." << endl;
        cuts_FR = "hnl_dr_12 < 0.3"

        ///// CHANNEL SPECIFIC
        if ch == "mem":
            mode021 = True

            cuts_FR_021 = cuts_FR + " && " + DFR_MEM_L
            tight_021 = DFR_MEM_T
            b_eta = b_eta_mu

            if isData == False:
                cuts_FR_021  += " && l1_gen_match_pdgid != 22 && label == 1"  // DY50 only

    h_pt_eta_T_012  = rt.TH2F("pt_eta_T_012","pt_eta_T_012",len(b_pt)-1,b_pt,len(b_eta)-1,b_eta)
    h_pt_eta_T_021  = rt.TH2F("pt_eta_T_021","pt_eta_T_021",len(b_pt)-1,b_pt,len(b_eta)-1,b_eta)
    h_pt_eta_L_012  = rt.TH2F("pt_eta_L_012","pt_eta_L_012",len(b_pt)-1,b_pt,len(b_eta)-1,b_eta)
    h_pt_eta_L_021  = rt.TH2F("pt_eta_L_021","pt_eta_L_021",len(b_pt)-1,b_pt,len(b_eta)-1,b_eta)

    //// PREPARE TREES
    t = None
    t = rt.TChain("tree")
    t.Add(data_B_mmm)
    df = rdf(t)
    print"\n\tchain made."
    N_ENTRIES = df.Count()

    if mode021 == True:

        f0_021 = df.Filter(cuts_FR_021)

        cout << "\n\tf0_021 entries: ", f0_021.Count().GetValue() << endl;

        df0_021 = f0_021.Define("ptcone021", ptconel1)
        cout << "\n\tptcone021 defined." << endl;

        dfL_021 = df0_021.Define("abs_l1_eta", "abs(l1_eta)")
        cout << "\n\tabs_l1_eta defined." << endl;

        dfT_021 = dfL_021.Filter(tight_021)
        cout << "\n\ttight df_021 defined." << endl;

        _pt_eta_T_021 = dfT_021.Histo2D(("pt_eta_T_021","pt_eta_T_021",len(b_pt)-1,b_pt,len(b_eta)-1,b_eta),"ptcone021","abs_l1_eta")
        _pt_eta_L_021 = dfL_021.Histo2D(("pt_eta_L_021","pt_eta_L_021",len(b_pt)-1,b_pt,len(b_eta)-1,b_eta),"ptcone021","abs_l1_eta")

        h_pt_eta_T_021 = _pt_eta_T_021.GetPtr()
        h_pt_eta_L_021 = _pt_eta_L_021.GetPtr()

    if mode012 == True:

        f0_012 = df.Filter(cuts_FR_012)

        cout << "\n\tf0_012 entries: ", f0_012.Count().GetValue() << endl;

        df0_012 = f0_012.Define("ptcone012", ptconel2)
        cout << "\n\tptcone012 defined." << endl;

        dfL_012 = df0_012.Define("abs_l2_eta", "abs(l2_eta)")
        cout << "\n\tabs_l2_eta defined." << endl;

        dfT_012 = dfL_012.Filter(tight_012)
        cout << "\n\ttight df_012 defined." << endl;

        _pt_eta_T_012 = dfT_012.Histo2D(("pt_eta_T_012","pt_eta_T_012",len(b_pt)-1,b_pt,len(b_eta)-1,b_eta),"ptcone012","abs_l2_eta")
        _pt_eta_L_012 = dfL_012.Histo2D(("pt_eta_L_012","pt_eta_L_012",len(b_pt)-1,b_pt,len(b_eta)-1,b_eta),"ptcone012","abs_l2_eta")

        h_pt_eta_T_012 = _pt_eta_T_012.GetPtr()
        h_pt_eta_L_012 = _pt_eta_L_012.GetPtr()

    h_pt_eta_T_012.Add(h_pt_eta_T_021)
    h_pt_eta_L_012.Add(h_pt_eta_L_021)

    cout << "\n\t cuts: %s"                    %cuts_FR << endl;
    if mode012 ==True:
        cout << "\n\t loose 012: %s\n"         %(cuts_FR_012) << endl;
        cout << "\n\t tight 012: %s\n"         %(tight_012) << endl;
        cout << "\ttotal loose 012: %s\n"      %f0_012.Count().GetValue() << endl;
    if mode021 ==True:
        cout << "\n\t loose 021: %s\n"         %(cuts_FR_021) << endl;
        cout << "\n\t tight 021: %s\n"         %(tight_021) << endl;
        cout << "\ttotal loose 021: %s\n"      %f0_021.Count().GetValue() << endl;

    cout << "\n\tentries T && L: ", h_pt_eta_T_012.GetEntries(), h_pt_eta_L_012.GetEntries() << endl;

    c_pt_eta = rt.TCanvas("ptCone_eta", "ptCone_eta")
    h_pt_eta_T_012.Divide(h_pt_eta_L_012)
    h_pt_eta_T_012.Draw("colztextE")
    h_pt_eta_T_012.SetTitle("; p_{T}^{cone} [GeV]; DiMuon |#eta|; tight-to-loose ratio")
    pf.showlogoprelimsim("CMS")
    pf.showlumi("SFR_"+ch)
    save(knvs=c_pt_eta, sample="%s_T2Lratio"%input, ch=ch, DIR=plotDir)

    sys.stderr = sys.__stderr__
    sys.stdout = sys.__stdout__
    // DO AGAIN WITH THREE DIFFERENT TEFFS TO GET ERROR
*/
