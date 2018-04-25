########################## 
# Import relevant modules
##########################
import ROOT
import numpy as np
from glob import glob
import tools
import time
from array import array
import sys

########################## 
# Global Root settings
##########################
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetPalette(ROOT.kBird)

# When this static function is called with sumw2=kTRUE, all new histograms will automatically activate the storage of the sum of squares of errors
ROOT.TH1.SetDefaultSumw2()


########################## 
# Prepare chain of trees
##########################
    
# Returns a TChain object which either contains all samples (allsamples = True) or a selected sample (allsamples = False) with different displacements. 
def makechain(allsamples):    

    #access multiple trees by "chaining" them
    chain = ROOT.TChain('tree')
    all_files = glob('/afs/cern.ch/user/d/dezhu/workspace/HNL/ntuples/*/HNLGenTreeProducer/tree.root')

    if allsamples == True:
        for sample in all_files [:]: #for the first 10 files
            chain.Add(sample)

    if allsamples == False:
        chain.Add('/afs/cern.ch/user/d/dezhu/workspace/HNL/ntuples/HN3L_M_1_V_0p00282842712475_e_onshell/HNLGenTreeProducer/tree.root')
        chain.Add('/afs/cern.ch/user/d/dezhu/workspace/HNL/ntuples/HN3L_M_1_V_0p00316227766017_e_onshell/HNLGenTreeProducer/tree.root')
        chain.Add('/afs/cern.ch/user/d/dezhu/workspace/HNL/ntuples/HN3L_M_1_V_0p004472135955_e_onshell/HNLGenTreeProducer/tree.root')
        chain.Add('/afs/cern.ch/user/d/dezhu/workspace/HNL/ntuples/HN3L_M_1_V_0p004472135955_mu_onshell/HNLGenTreeProducer/tree.root')
        chain.Add('/afs/cern.ch/user/d/dezhu/workspace/HNL/ntuples/HN3L_M_1_V_0p00547722557505_e_onshell/HNLGenTreeProducer/tree.root')
        chain.Add('/afs/cern.ch/user/d/dezhu/workspace/HNL/ntuples/HN3L_M_1_V_0p00547722557505_mu_onshell/HNLGenTreeProducer/tree.root')
        chain.Add('/afs/cern.ch/user/d/dezhu/workspace/HNL/ntuples/HN3L_M_1_V_0p00707106781187_e_onshell/HNLGenTreeProducer/tree.root')
        chain.Add('/afs/cern.ch/user/d/dezhu/workspace/HNL/ntuples/HN3L_M_1_V_0p00707106781187_mu_onshell/HNLGenTreeProducer/tree.root')
        chain.Add('/afs/cern.ch/user/d/dezhu/workspace/HNL/ntuples/HN3L_M_1_V_0p00836660026534_e_onshell/HNLGenTreeProducer/tree.root')
        chain.Add('/afs/cern.ch/user/d/dezhu/workspace/HNL/ntuples/HN3L_M_1_V_0p00836660026534_mu_onshell/HNLGenTreeProducer/tree.root')
        chain.Add('/afs/cern.ch/user/d/dezhu/workspace/HNL/ntuples/HN3L_M_2_V_0p00244948974278_e_onshell/HNLGenTreeProducer/tree.root')
        chain.Add('/afs/cern.ch/user/d/dezhu/workspace/HNL/ntuples/HN3L_M_2_V_0p00244948974278_mu_onshell/HNLGenTreeProducer/tree.root')
        chain.Add('/afs/cern.ch/user/d/dezhu/workspace/HNL/ntuples/HN3L_M_2_V_0p01_e_onshell/HNLGenTreeProducer/tree.root')
        chain.Add('/afs/cern.ch/user/d/dezhu/workspace/HNL/ntuples/HN3L_M_2_V_0p01_mu_onshell/HNLGenTreeProducer/tree.root')
        chain.Add('/afs/cern.ch/user/d/dezhu/workspace/HNL/ntuples/HN3L_M_2p1_V_0p00244948974278_e_onshell/HNLGenTreeProducer/tree.root')
        chain.Add('/afs/cern.ch/user/d/dezhu/workspace/HNL/ntuples/HN3L_M_2p1_V_0p00244948974278_mu_onshell/HNLGenTreeProducer/tree.root')
        chain.Add('/afs/cern.ch/user/d/dezhu/workspace/HNL/ntuples/HN3L_M_2p1_V_0p00282842712475_e_onshell/HNLGenTreeProducer/tree.root')
        chain.Add('/afs/cern.ch/user/d/dezhu/workspace/HNL/ntuples/HN3L_M_2p1_V_0p00282842712475_mu_onshell/HNLGenTreeProducer/tree.root')
        chain.Add('/afs/cern.ch/user/d/dezhu/workspace/HNL/ntuples/HN3L_M_2p1_V_0p00316227766017_e_onshell/HNLGenTreeProducer/tree.root')
        chain.Add('/afs/cern.ch/user/d/dezhu/workspace/HNL/ntuples/HN3L_M_2p1_V_0p00316227766017_mu_onshell/HNLGenTreeProducer/tree.root')

    nentries = chain.GetEntries()
    print('Created a TChain object with %d events.'%(nentries))
    return chain

########################## 
# Additional tools
##########################
    
def progress(count, total, status=''):
        sys.stdout.flush()
        bar_len = 60
        filled_len = int(round(bar_len * count / float(total)))
        percents = round(100.0 * count / float(total), 1)
        bar = '=' * (filled_len-1) + '>' +'-' * (bar_len - filled_len)
        sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
