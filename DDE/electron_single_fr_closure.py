import ROOT
import root_pandas
import pickle
import numpy as np
import pandas as pd
from root_numpy import root2array
from collections import OrderedDict
import matplotlib.pyplot as plt

ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch(True)
ROOT.TH1.SetDefaultSumw2()

with open('electron_single_fr_tight_to_loose.pck') as f1:
    weights = pickle.load(f1)

bins = np.array([0., 5., 10., 15., 40., 100.])

@np.vectorize
def addFrWeights(ptcone, eta, weights):
    ''' Add tight-to-loose weights f/1-f
    '''
    if abs(eta)>1.5:
        if ptcone > 40.: return weights['1p5to2p5']['inclusive'][4]/(1.-weights['1p5to2p5']['inclusive'][4])
        if ptcone > 15.: return weights['1p5to2p5']['inclusive'][3]/(1.-weights['1p5to2p5']['inclusive'][3])
        if ptcone > 10.: return weights['1p5to2p5']['inclusive'][2]/(1.-weights['1p5to2p5']['inclusive'][2])
        if ptcone >  5.: return weights['1p5to2p5']['inclusive'][1]/(1.-weights['1p5to2p5']['inclusive'][1])
        if ptcone >  0.: return weights['1p5to2p5']['inclusive'][0]/(1.-weights['1p5to2p5']['inclusive'][0])
    if abs(eta)>0.8:
        if ptcone > 40.: return weights['0p8to1p5']['inclusive'][4]/(1.-weights['0p8to1p5']['inclusive'][4])
        if ptcone > 15.: return weights['0p8to1p5']['inclusive'][3]/(1.-weights['0p8to1p5']['inclusive'][3])
        if ptcone > 10.: return weights['0p8to1p5']['inclusive'][2]/(1.-weights['0p8to1p5']['inclusive'][2])
        if ptcone >  5.: return weights['0p8to1p5']['inclusive'][1]/(1.-weights['0p8to1p5']['inclusive'][1])
        if ptcone >  0.: return weights['0p8to1p5']['inclusive'][0]/(1.-weights['0p8to1p5']['inclusive'][0])
    if abs(eta)>0.:
        if ptcone > 40.: return weights['0to0p8']['inclusive'][4]/(1.-weights['0to0p8']['inclusive'][4])
        if ptcone > 15.: return weights['0to0p8']['inclusive'][3]/(1.-weights['0to0p8']['inclusive'][3])
        if ptcone > 10.: return weights['0to0p8']['inclusive'][2]/(1.-weights['0to0p8']['inclusive'][2])
        if ptcone >  5.: return weights['0to0p8']['inclusive'][1]/(1.-weights['0to0p8']['inclusive'][1])
        if ptcone >  0.: return weights['0to0p8']['inclusive'][0]/(1.-weights['0to0p8']['inclusive'][0])
    


baseline_selection = '&'.join([
    'l0_pt>27 & abs(l0_eta)<2.4 & l0_id_t & l0_dz<0.2 & l0_dxy<0.05 & l0_reliso_rho_04<0.2', # l0 genuine
    'l2_pt>15 & abs(l2_eta)<2.4 & l2_id_t & l2_dz<0.2 & l2_dxy<0.05 & l2_reliso_rho_04<0.2', # l2 genuine 
    'hnl_q_02==0'                                                                          , # opposite charge
    'l1_pt>5 & abs(l1_eta)<2.5 & l1_dz<0.2 & l1_dxy>0.05'                                  , # l1 kinematics and impact parameter
    'l1_gen_match_pdgid!=22'                                                               , # no conversions 
#     'hnl_dr_01>0.3 & hnl_dr_12>0.3'                                                        , # distance from genuine leptons
])

files = [
    '/work/dezhu/4_production/production_20190306_BkgMC/mem/ntuples/DYBB/HNLTreeProducer/tree.root'              ,
    '/work/dezhu/4_production/production_20190306_BkgMC/mem/ntuples/DYJetsToLL_M50/HNLTreeProducer/tree.root'    ,
    '/work/dezhu/4_production/production_20190306_BkgMC/mem/ntuples/DYJetsToLL_M50_ext/HNLTreeProducer/tree.root',
#     '/work/dezhu/4_production/production_20190306_BkgMC/mem/ntuples/TTJets/HNLTreeProducer/tree.root'            ,
]

# dataset = pd.DataFrame(root2array(files, 'tree', selection=baseline_selection))
# 
# print 'adding variables to dataset...'
# dataset['l1_pt_cone'       ] = dataset['l1_pt'] * (1. + dataset['l0_reliso_rho_04'])
# dataset['l1_ele_sfr_weight'] = addFrWeights(dataset['l1_pt_cone'], dataset['l1_pt_cone'], weights)
# print '...done'
# 
# dataset.to_root('dy.root', key='tree', store_index=False)


fin = ROOT.TFile.Open('dy.root', 'read')
fin.cd()
tree = fin.Get('tree')


# h_mass_obs   = ROOT.TH1F('h_mass_obs'  , '', 150, 0, 150)
# h_mass_exp_1 = ROOT.TH1F('h_mass_exp_1', '', 150, 0, 150)
# h_mass_exp_2 = ROOT.TH1F('h_mass_exp_2', '', 150, 0, 150)
# h_mass_exp_3 = ROOT.TH1F('h_mass_exp_3', '', 150, 0, 150)

# h_mass_obs   = ROOT.TH1F('h_mass_obs'  , '', 125, 0, 250)
# h_mass_exp_1 = ROOT.TH1F('h_mass_exp_1', '', 125, 0, 250)
# h_mass_exp_2 = ROOT.TH1F('h_mass_exp_2', '', 125, 0, 250)
# h_mass_exp_3 = ROOT.TH1F('h_mass_exp_3', '', 125, 0, 250)


h_mass_obs   = ROOT.TH1F('h_mass_obs'  , '', 100, 0, 1)
h_mass_exp_1 = ROOT.TH1F('h_mass_exp_1', '', 100, 0, 1)
h_mass_exp_2 = ROOT.TH1F('h_mass_exp_2', '', 100, 0, 1)
h_mass_exp_3 = ROOT.TH1F('h_mass_exp_3', '', 100, 0, 1)


# tree.Draw('hnl_m_02 >> h_mass_obs'  , 'l1_MediumNoIso==1 & l1_reliso_rho_04<0.2')
# tree.Draw('hnl_m_02 >> h_mass_exp_1', '(l1_ele_sfr_weight)*(!(l1_MediumNoIso==1 & l1_reliso_rho_04<0.2) & l1_reliso_rho_04<0.45 & abs(l1_eta)<=0.8)')
# tree.Draw('hnl_m_02 >> h_mass_exp_2', '(l1_ele_sfr_weight)*(!(l1_MediumNoIso==1 & l1_reliso_rho_04<0.2) & l1_reliso_rho_04<0.60 & abs(l1_eta)>0.8 & abs(l1_eta)<=1.5)')
# tree.Draw('hnl_m_02 >> h_mass_exp_3', '(l1_ele_sfr_weight)*(!(l1_MediumNoIso==1 & l1_reliso_rho_04<0.2) & l1_reliso_rho_04<0.50 & abs(l1_eta)>1.5)')

# tree.Draw('hnl_w_vis_m >> h_mass_obs'  , 'l1_MediumNoIso==1 & l1_reliso_rho_04<0.2')
# tree.Draw('hnl_w_vis_m >> h_mass_exp_1', '(l1_ele_sfr_weight)*(!(l1_MediumNoIso==1 & l1_reliso_rho_04<0.2) & l1_reliso_rho_04<0.45 & abs(l1_eta)<=0.8)')
# tree.Draw('hnl_w_vis_m >> h_mass_exp_2', '(l1_ele_sfr_weight)*(!(l1_MediumNoIso==1 & l1_reliso_rho_04<0.2) & l1_reliso_rho_04<0.60 & abs(l1_eta)>0.8 & abs(l1_eta)<=1.5)')
# tree.Draw('hnl_w_vis_m >> h_mass_exp_3', '(l1_ele_sfr_weight)*(!(l1_MediumNoIso==1 & l1_reliso_rho_04<0.2) & l1_reliso_rho_04<0.50 & abs(l1_eta)>1.5)')

tree.Draw('sv_prob >> h_mass_obs'  , 'l1_MediumNoIso==1 & l1_reliso_rho_04<0.2')
tree.Draw('sv_prob >> h_mass_exp_1', '(l1_ele_sfr_weight)*(!(l1_MediumNoIso==1 & l1_reliso_rho_04<0.2) & l1_reliso_rho_04<0.45 & abs(l1_eta)<=0.8)')
tree.Draw('sv_prob >> h_mass_exp_2', '(l1_ele_sfr_weight)*(!(l1_MediumNoIso==1 & l1_reliso_rho_04<0.2) & l1_reliso_rho_04<0.60 & abs(l1_eta)>0.8 & abs(l1_eta)<=1.5)')
tree.Draw('sv_prob >> h_mass_exp_3', '(l1_ele_sfr_weight)*(!(l1_MediumNoIso==1 & l1_reliso_rho_04<0.2) & l1_reliso_rho_04<0.50 & abs(l1_eta)>1.5)')

h_mass_obs.Draw('histe')
h_mass_exp_1.Add(h_mass_exp_2)
h_mass_exp_1.Add(h_mass_exp_3)

h_mass_exp_1.SetMarkerStyle(8)
h_mass_exp_1.Draw('ep same')

h_mass_obs.SetMaximum(1.2*max([hh.GetMaximum() for hh in [h_mass_obs, h_mass_exp_1, h_mass_exp_2, h_mass_exp_3]]))

ROOT.gPad.Update()
# ROOT.gPad.SaveAs('2l_mass_closure.pdf')
# ROOT.gPad.SaveAs('3l_mass_closure.pdf')
# ROOT.gPad.SaveAs('2l_mass_closure_extended.pdf')
# ROOT.gPad.SaveAs('3l_mass_closure_extended.pdf')
# ROOT.gPad.SaveAs('dr02.pdf')
# ROOT.gPad.SaveAs('dr12.pdf')
# ROOT.gPad.SaveAs('m02.pdf')
ROOT.gPad.SetLogy(True)
ROOT.gPad.SaveAs('sv_prob.pdf')

