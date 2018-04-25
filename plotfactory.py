########################## 
# Import relevant modules
##########################
import ROOT
import numpy as np
from glob import glob
import time
from array import array
import sys


########################## 
# Prepare chain of trees
##########################
#This is the location where all ntuples are stored. Adapt the location to your path. 
ntup_dir = '/afs/cern.ch/user/d/dezhu/workspace/HNL/ntuples/'    

# Returns a TChain object which either contains all samples (allsamples = True) or a selected sample (allsamples = False) with different displacements. 
def makechain(allsamples):    

    #access multiple trees by "chaining" them
    chain = ROOT.TChain('tree')
    all_files = glob(ntup_dir + '*/HNLGenTreeProducer/tree.root')

    if allsamples == True:
        for sample in all_files [:]: #for the first 10 files
            chain.Add(sample)

    if allsamples == False:
        chain.Add(ntup_dir + 'HN3L_M_1_V_0p00282842712475_e_onshell/HNLGenTreeProducer/tree.root')
        chain.Add(ntup_dir + 'HN3L_M_1_V_0p00316227766017_e_onshell/HNLGenTreeProducer/tree.root')
        chain.Add(ntup_dir + 'HN3L_M_1_V_0p004472135955_e_onshell/HNLGenTreeProducer/tree.root')
        chain.Add(ntup_dir + 'HN3L_M_1_V_0p004472135955_mu_onshell/HNLGenTreeProducer/tree.root')
        chain.Add(ntup_dir + 'HN3L_M_1_V_0p00547722557505_e_onshell/HNLGenTreeProducer/tree.root')
        chain.Add(ntup_dir + 'HN3L_M_1_V_0p00547722557505_mu_onshell/HNLGenTreeProducer/tree.root')
        chain.Add(ntup_dir + 'HN3L_M_1_V_0p00707106781187_e_onshell/HNLGenTreeProducer/tree.root')
        chain.Add(ntup_dir + 'HN3L_M_1_V_0p00707106781187_mu_onshell/HNLGenTreeProducer/tree.root')
        chain.Add(ntup_dir + 'HN3L_M_1_V_0p00836660026534_e_onshell/HNLGenTreeProducer/tree.root')
        chain.Add(ntup_dir + 'HN3L_M_1_V_0p00836660026534_mu_onshell/HNLGenTreeProducer/tree.root')
        chain.Add(ntup_dir + 'HN3L_M_2_V_0p00244948974278_e_onshell/HNLGenTreeProducer/tree.root')
        chain.Add(ntup_dir + 'HN3L_M_2_V_0p00244948974278_mu_onshell/HNLGenTreeProducer/tree.root')
        chain.Add(ntup_dir + 'HN3L_M_2_V_0p01_e_onshell/HNLGenTreeProducer/tree.root')
        chain.Add(ntup_dir + 'HN3L_M_2_V_0p01_mu_onshell/HNLGenTreeProducer/tree.root')
        chain.Add(ntup_dir + 'HN3L_M_2p1_V_0p00244948974278_e_onshell/HNLGenTreeProducer/tree.root')
        chain.Add(ntup_dir + 'HN3L_M_2p1_V_0p00244948974278_mu_onshell/HNLGenTreeProducer/tree.root')
        chain.Add(ntup_dir + 'HN3L_M_2p1_V_0p00282842712475_e_onshell/HNLGenTreeProducer/tree.root')
        chain.Add(ntup_dir + 'HN3L_M_2p1_V_0p00282842712475_mu_onshell/HNLGenTreeProducer/tree.root')
        chain.Add(ntup_dir + 'HN3L_M_2p1_V_0p00316227766017_e_onshell/HNLGenTreeProducer/tree.root')
        chain.Add(ntup_dir + 'HN3L_M_2p1_V_0p00316227766017_mu_onshell/HNLGenTreeProducer/tree.root')

    nentries = chain.GetEntries()
    print('Created a TChain object with %d events.'%(nentries))
    return chain

########################## 
# Style settings
##########################
def makestyle():
    pfstyle = ROOT.TStyle('pfstyle','pfstyle')

    pfstyle.SetOptTitle(0)
    pfstyle.SetOptStat(0)

    # Canvas
    pfstyle.SetCanvasDefH(800)
    pfstyle.SetCanvasDefW(900)
    
    # Use plain black on white colors
    icol = 0
    pfstyle.SetFrameBorderMode(icol)
    pfstyle.SetCanvasBorderMode(icol)
    pfstyle.SetPadBorderMode(icol)
    pfstyle.SetPadColor(icol)
    pfstyle.SetCanvasColor(icol)
    pfstyle.SetStatColor(icol)

    # Set the paper & margin sizes
    pfstyle.SetPaperSize(20,26)
    pfstyle.SetPadTopMargin(0.05)
    pfstyle.SetPadRightMargin(0.05)
    pfstyle.SetPadBottomMargin(0.12)
    pfstyle.SetPadLeftMargin(0.15)

    # Use large fonts
    font = 42
    tsize = 0.045
    
    
    # When this static function is called with sumw2=kTRUE, all new histograms will automatically activate the storage of the sum of squares of errors
    ROOT.TH1.SetDefaultSumw2()

    return pfstyle


########################## 
# Additional tools
##########################

# prints out a progressbar which will be flushed at the terminal
def progressbar(count, total, status=''):
        sys.stdout.flush()
        bar_len = 60
        filled_len = int(round(bar_len * count / float(total)))
        percents = round(100.0 * count / float(total), 1)
        bar = '=' * (filled_len-1) + '>' +'-' * (bar_len - filled_len)
        sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
