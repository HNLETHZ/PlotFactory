
void dostuff () 
   {ROOT::EnableImplicitMT(); // Tell ROOT you want to go parallel


    std::string fDYBB     = "/eos/user/d/dezhu/HNL/ntuples/HN3Lv2.0/background/montecarlo/production20190318/mmm/ntuples/DYBB/HNLTreeProducer/tree.root";
    std::string fDY50     = "/eos/user/d/dezhu/HNL/ntuples/HN3Lv2.0/background/montecarlo/production20190318/mmm/ntuples/DYJetsToLL_M50/HNLTreeProducer/tree.root";
    std::string fDY50_ext = "/eos/user/d/dezhu/HNL/ntuples/HN3Lv2.0/background/montecarlo/production20190318/mmm/ntuples/DYJetsToLL_M50_ext/HNLTreeProducer/tree.root";
    std::string fTT       = "/eos/user/d/dezhu/HNL/ntuples/HN3Lv2.0/background/montecarlo/production20190318/mmm/ntuples/TTJets_ext/HNLTreeProducer/tree.root";

    //ROOT::RDataFrame df("tree", {fDYBB, fDY50, fDY50_ext, fTT});
    ROOT::RDataFrame df("tree", {fDY50, fDY50_ext});

    auto f0 = df.Filter("l1_pt < 50");
    std::cout << f0.Count().GetValue() << endl;
    
    }
