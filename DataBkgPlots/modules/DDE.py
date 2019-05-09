from modules.officialStyle import officialStyle
import plotfactory as pf
from modules.Samples import createSampleLists, setSumWeights
from modules.Selections import getSelection
from ROOT import ROOT, RDataFrame, TH1F, TFile, TTree, TTreeFormula, TCanvas, TPaveText, TBox, gStyle,TChain
import numpy as np

from pdb import set_trace

# Using official CMS Style
# officialStyle(gStyle)
pf.setpfstyle()

# Enable ROOT's implicit multi-threading for all objects that provide an internal parallelisation mechanism
ROOT.EnableImplicitMT()

def makeDataFrameBase(analysis_dir,server,channel):
    sample_dict = {}
    samples_all, samples_data = createSampleLists(analysis_dir=analysis_dir, server = server, channel=channel)
    working_samples = samples_data
    working_samples = setSumWeights(working_samples)
    print('###########################################################')
    print'# %d samples to be used:'%(len(working_samples))
    print('###########################################################')
    for w in working_samples: print('{:<20}{:<20}'.format(*[w.name,('path: '+w.ana_dir)]))
    #TChain'ing all data samples together
    chain = TChain('tree')
    for i,s in enumerate(working_samples):
        sample = working_samples[0]
        file_name = '/'.join([sample.ana_dir, sample.dir_name, sample.tree_prod_name, 'tree.root'])
        chain.Add(file_name)
        
    dataframe = RDataFrame(chain)
    weight = 'weight * lhe_weight'
    dataframe = dataframe.Define('w',weight)\
                        .Define('l1_ptCone',ptCone('1'))\
                        .Define('abs_l1_eta','abs(l1_eta)')
    set_trace()
    return dataframe

def ptCone(lepton):
    PTCONE = '((l%s_pt*(l%s_reliso_rho_03<0.2))+((l%s_reliso_rho_03>=0.2)*(l%s_pt*(1. + l%s_reliso_rho_03 - 0.2))))'%(lepton,lepton,lepton,lepton,lepton)
    return PTCONE

def drawCommand(lepton):
    command = 'l%s_eta:'%(lepton) + ptCone(lepton)
    return command

def map_FR(dataframe, channel):
    weight = 'weight * lhe_weight'
    # bins_ptCone = np.array([5.,15.,25.,35.,70.])
    # bins_eta = np.array([0.,1.2,2.1,2.4])
    bins_ptCone = np.array([5., 10., 15., 20., 25., 35., 50., 70.])
    bins_eta    = np.array([0., 1.2, 2.1, 2.4]) 

    selection_LL_correlated = '(' + ' & '.join([getSelection(channel,'baseline'),getSelection(channel,'LL_correlated')]) + ')' 
    selection_TT_correlated = '(' + ' & '.join([getSelection(channel,'baseline'),getSelection(channel,'LL_correlated'),getSelection(channel,'TT')]) + ')' 

    set_trace()
    h_LL_correlated = dataframe\
            .Filter(selection_LL_correlated)\
            .Histo2D(('h_LL_correlated','h_LL_correlated',len(bins_ptCone)-1,bins_ptCone, len(bins_eta)-1, bins_eta),'l1_ptCone','l1_eta')


    #name the axis, also initiate the dataframe call
    # h_LL_correlated.SetTitle(';l1 ptCone [GeV]; l1_eta')

    h_TT_correlated = dataframe\
            .Filter(selection_TT_correlated)\
            .Histo2D(('h_TT_correlated','h_TT_correlated',len(bins_ptCone)-1,bins_ptCone, len(bins_eta)-1, bins_eta),'l1_ptCone','l1_eta')

    #name the axis, also initiate the dataframe call
    # h_TT_correlated.SetTitle(';l1 ptCone [GeV]; l1_eta')


    #just a quick measurement
    selection_baseline = getSelection(channel,'baseline')  
    # h_baseline = dataframe\
            # .Filter(selection_baseline)\
            # .Histo2D(('h_TT_correlated','h_TT_correlated',len(bins_ptCone)-1,bins_ptCone, len(bins_eta)-1, bins_eta),'l1_ptCone','l1_eta')
            # .Histo2D(('h_baseline','h_baseline',20,10.,100.,20,0.,1.),'hnl_hn_vis_pt','hnl_dr_12')
    h_baseline = dataframe\
            .Histo2D(('h_TT_correlated','h_TT_correlated',len(bins_ptCone)-1,bins_ptCone, len(bins_eta)-1, bins_eta),'l1_ptCone','l1_eta')
            # .Histo2D(('h_baseline','h_baseline',20,10.,100.,20,0.01,.8),'hnl_hn_vis_pt','hnl_dr_12')
    # h_baseline.SetTitle(';DiMuon p_T [GeV]; #DeltaR(#mu1, #mu2)')
    h_baseline.SetTitle(';l1 ptCone [GeV]; l1_eta')


    # temporarily making a drawing section to test the current code
    # hist = h_TT_correlated.Clone()
    # hist = h_LL_correlated.Clone()
    hist = h_baseline.Clone()
    # hist.Divide(h_LL_correlated.Clone())
    can = TCanvas('can', '')
    hist.Draw('colz')
    # pf.showlumi('xxx fb^{-1} (xxx TeV)')
    pf.showlumi('%d entries'%(hist.GetEntries()))
    pf.showlogopreliminary()
    can.Update()
    set_trace()


def main():
    # define basic config into
    analysis_dir = '/home/dehuazhu/SESSD/4_production/'
    server = 'starseeker'
    channel = 'mmm'

    # prepare the dataframe
    dataframe = makeDataFrameBase(analysis_dir,server,channel)
    set_trace()

    # measure Fakerate within the measurement region
    map_FR(dataframe,channel)

if __name__ == '__main__':
    main()
