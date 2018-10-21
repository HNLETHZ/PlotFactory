from __future__ import division
from ROOT import gROOT as gr
import os
import ROOT as rt
import numpy as np
import plotfactory as pf
from glob import glob
import sys
from pdb import set_trace
from copy import deepcopy
from os.path import normpath, basename, split
from collections import OrderedDict
from multiprocessing import Pool
from multiprocessing.dummy import Pool
import pandas, root_numpy
import root_pandas
from itertools import product
#gr.SetBatch(True) # NEEDS TO BE SET FOR MULTIPROCESSING OF plot.Draw()
pf.setpfstyle()
####################################################################################################
plotDir  = '/eos/user/v/vstampf/plots/DDE/'
inDir   = '/eos/user/v/vstampf/ntuples/DDE_v0/'
inDir   = '/eos/user/v/vstampf/ntuples/DDE_v1_DiMuIso/'
inDir   = '/eos/user/v/vstampf/ntuples/DDE_v2/'
tempDir = '/eos/user/v/vstampf/ntuples/temp/'
treeDir = '/eos/user/v/vstampf/ntuples/DDE_v2/prompt_m/added_trees/'
m_dir   = 'prompt_m/'
e_dir   = 'prompt_e/'
suffix  = 'HNLTreeProducer/tree.root'
####################################################################################################
DY50_dir_e           = 'prompt_e/DYJetsToLL_M50/'
DY50_ext_dir_e       = 'prompt_e/DYJetsToLL_M50_ext/'
DY10to50_dir_e       = 'prompt_e/DYJetsToLL_M10to50/'
DY10to50_ext_dir_e   = 'prompt_e/DYJetsToLL_M10to50_ext/'
DYBB_dir_e           = 'prompt_e/DYBB/'
TT_dir_e             = 'prompt_e/TTJets/'  
W_dir_e              = 'prompt_e/WJetsToLNu/'
W_ext_dir_e          = 'prompt_e/WJetsToLNu_ext/'
####################################################################################################
DY50_dir_m           = 'prompt_m/DYJetsToLL_M50/'
DY50_ext_dir_m       = 'prompt_m/DYJetsToLL_M50_ext/'
DY10to50_dir_m       = 'prompt_m/DYJetsToLL_M10to50/'
DY10to50_ext_dir_m   = 'prompt_m/DYJetsToLL_M10to50_ext/'
DYBB_dir_m           = 'prompt_m/DYBB/'
TT_dir_m             = 'prompt_m/TTJets/'  
TT_dir_m             = 'prompt_m/partial/TTJets/'  
W_dir_m              = 'prompt_m/WJetsToLNu/'
W_ext_dir_m          = 'prompt_m/WJetsToLNu_ext/'
data_m_B             = 'prompt_m/Single_mu_2017B/'
data_m_C             = 'prompt_m/partial/Single_mu_2017C/'
data_m_D             = 'prompt_m/Single_mu_2017D/'
data_m_E             = 'prompt_m/partial/Single_mu_2017E/'
data_m_F             = 'prompt_m/partial/Single_mu_2017F/'
DYBB_dir_m           = 'prompt_m/partial/DYBB/'
DY10to50_dir_m       = 'prompt_m/partial/DYJetsToLL_M10to50/'
DY10to50_ext_dir_m   = 'prompt_m/partial/DYJetsToLL_M10to50_ext/'
DY50_dir_m           = 'prompt_m/partial/DYJetsToLL_M50/'
DY50_ext_dir_m       = 'prompt_m/partial/DYJetsToLL_M50_ext/'
W_dir_m              = 'prompt_m/partial/WJetsToLNu/'
W_ext_dir_m          = 'prompt_m/partial/WJetsToLNu_ext/'
####################################################################################################
samples =  [W_dir_e, W_ext_dir_e, TT_dir_e, DYBB_dir_e, DY50_dir_e, DY10to50_ext_dir_e, DY10to50_dir_e, DY50_ext_dir_e] #NOT YET PROCESSED
samples += [W_dir_m, W_ext_dir_m, TT_dir_m, DYBB_dir_m, DY50_dir_m, DY10to50_ext_dir_m, DY10to50_dir_m, DY50_ext_dir_m]
####################################################################################################
## CUTS ##
####################################################################################################
disp0p5     = 'hnl_2d_disp > 0.5'
disp1       = 'hnl_2d_disp > 1'
M10         = 'hnl_m_01 > 10  &  hnl_m_02 > 10  &  hnl_m_12 > 10'
tt_disp_bj1 = disp0p5 + '  &  nbj > 0'
####################################################################################################
threeMu_pt_rlxd =   'l1_pt > 20  &  l2_pt > 4  &  l0_pt > 4'\
                '  &  abs(l0_dz) < 0.2 &  abs(l1_dz) < 0.2 &  abs(l2_dz) < 0.2 '\
                '  &  abs(l0_dxy) < 0.045 &  abs(l1_dxy) < 0.045 &  abs(l2_dxy) < 0.045 '\
                '  & l0_id_m & l1_id_m & l2_id_m '\
                '  & abs(l0_eta) < 2.4 & abs(l1_eta) < 2.4 & abs(l2_eta) < 2.4 '\
                '  & l0_reliso05_03 < 0.1 & l1_reliso05_03 < 0.1 & l2_reliso05_03 < 0.1 '\
                '  & hnl_dr_01 > 0.05 & hnl_dr_02 > 0.05 & hnl_dr_12 > 0.05 '
####################################################################################################
threeMu         =   'l1_pt > 20  &  l2_pt > 10  &  l0_pt > 27'\
                '  &  abs(l0_dz) < 0.2 &  abs(l1_dz) < 0.2 &  abs(l2_dz) < 0.2 '\
                '  &  abs(l0_dxy) < 0.045 &  abs(l1_dxy) < 0.045 &  abs(l2_dxy) < 0.045 '\
                '  & l0_id_m & l1_id_m & l2_id_m '\
                '  & abs(l0_eta) < 2.4 & abs(l1_eta) < 2.4 & abs(l2_eta) < 2.4 '\
                '  & l0_reliso05_03 < 0.1 & l1_reliso05_03 < 0.1 & l2_reliso05_03 < 0.1 '\
                '  & hnl_dr_01 > 0.05 & hnl_dr_02 > 0.05 & hnl_dr_12 > 0.05 '
####################################################################################################
mltlst = [ ##  sample          , cuts 
            [W_dir_e           , ['1'              , '1'            ]],
            [W_ext_dir_e       , ['1'              , '1'            ]],
            [TT_dir_e          , ['1'              , '1'            ]], 
            [DYBB_dir_e        , ['1'              , '1'            ]],
            [DY50_dir_e        , ['1'              , '1'            ]], 
            [DY10to50_ext_dir_e, ['1'              , '1'            ]],
            [W_dir_m           , ['1'              , '1'            ]],
            [W_ext_dir_m       , ['1'              , '1'            ]],
            [TT_dir_m          , ['1'              , '1'            ]], 
            [DYBB_dir_m        , ['1'              , '1'            ]],
            [DY50_dir_m        , ['1'              , '1'            ]], 
            [DY10to50_ext_dir_m, ['1'              , '1'            ]],
            [DY10to50_dir_m    , ['1'              , '1'            ]],
            [TT_dir_e          , ['tt_disp_bj1'    , tt_disp_bj1    ]], 
            [TT_dir_m          , ['tt_disp_bj1'    , tt_disp_bj1    ]], 
            [DY50_dir_m        , ['threeMu'        , threeMu        ]],
            [DY10to50_dir_m    , ['threeMu_pt_rlxd', threeMu_pt_rlxd]],
            [DY10to50_ext_dir_m, ['threeMu_pt_rlxd', threeMu_pt_rlxd]],
        ]
####################################################################################################
## FAKES / PROMPT ##
####################################################################################################
in_acc = 'abs(l0_eta) < 2.4  &  abs(l2_eta) < 2.4  &  abs(l2_eta) < 2.4'

l0_prompt_m_dr = '( (l0_gen_match_fromHardProcessFinalState == 1 | l0_gen_match_isPromptFinalState == 1) & abs(l0_gen_match_pdgid) == 13 )'
l0_prompt_e_dr = '( (l0_gen_match_fromHardProcessFinalState == 1 | l0_gen_match_isPromptFinalState == 1) & abs(l0_gen_match_pdgid) == 11 )'
l1_prompt_dr   = '( (l1_gen_match_fromHardProcessFinalState == 1 | l1_gen_match_isPromptFinalState == 1) & abs(l0_gen_match_pdgid) == 13 )'
l2_prompt_dr   = '( (l2_gen_match_fromHardProcessFinalState == 1 | l2_gen_match_isPromptFinalState == 1) & abs(l0_gen_match_pdgid) == 13 )'

l0_fake_m_dr = '( !' + l0_prompt_m_dr + ')'  #'( (l0_gen_match_fromHardProcessFinalState == 0 & l0_gen_match_isPromptFinalState == 0) || abs(l0_gen_match_pdgid) != 13 )'
l0_fake_e_dr = '( !' + l0_prompt_e_dr + ')'  #'( (l0_gen_match_fromHardProcessFinalState == 0 & l0_gen_match_isPromptFinalState == 0) || abs(l0_gen_match_pdgid) != 11 )'
l1_fake_dr   = '( !' + l1_prompt_dr   + ')' 
l2_fake_dr   = '( !' + l2_prompt_dr   + ')' 

#at_least_one_prompt_dr = '(' + l1_prompt_dr + ')  ||  (' + l2_prompt_dr + ')'
#two_prompt_dr = '(' + l1_prompt_dr + ')  &  (' + l2_prompt_dr + ')'

l0_prompt = '( l0_simType == 4 | (l0_simType == 3 & l0_simFlavour == 15) )'
l1_prompt = '( l1_simType == 4 | (l1_simType == 3 & l1_simFlavour == 15) )'
l2_prompt = '( l2_simType == 4 | (l2_simType == 3 & l2_simFlavour == 15) )'

l0_prompt_new = '( abs(l0_simType) == 4 | l0_simFlavour == 15 )'
l1_prompt_new = '( abs(l1_simType) == 4 | l1_simFlavour == 15 )'
l2_prompt_new = '( abs(l2_simType) == 4 | l2_simFlavour == 15 )'

l0_fake_new = '( ! ' + l0_prompt_new + ' )' 
l1_fake_new = '( ! ' + l1_prompt_new + ' )' 
l2_fake_new = '( ! ' + l2_prompt_new + ' )' 

l1f_l2p_new     = '(' + l1_fake_new  + ' & ' + l2_prompt_new + ')'
l2f_l1p_new     = '(' + l2_fake_new  + ' & ' + l1_prompt_new + ')'
l1f_l2p_l0p_new = '(' + l1f_l2p_new  + ' & ' + l0_prompt_new + ')'
l2f_l1p_l0p_new = '(' + l2f_l1p_new  + ' & ' + l0_prompt_new + ')'

l0_fake = '( ! ' + l0_prompt + ' )' #(l0_simType != 4)'# & abs(l0_simType) < 1001)'
l1_fake = '( ! ' + l1_prompt + ' )' #'(l1_simType != 4)'# & abs(l1_simType) < 1001)'
l2_fake = '( ! ' + l2_prompt + ' )' #'(l2_simType != 4)'# & abs(l2_simType) < 1001)'

l1_heavyfake = 'l1_simType == 3'
l2_heavyfake = 'l2_simType == 3'

l1f_l2p     = '(' + l1_fake    + ' & ' + l2_prompt    + ')'
l2f_l1p     = '(' + l2_fake    + ' & ' + l1_prompt    + ')'
l1f_l2p_dr  = '(' + l1_fake_dr + ' & ' + l2_prompt_dr + ')'
l2f_l1p_dr  = '(' + l2_fake_dr + ' & ' + l1_prompt_dr + ')'
l1f_l2p_l0p = '(' + l1f_l2p    + ' & ' + l0_prompt    + ')'
l2f_l1p_l0p = '(' + l2f_l1p    + ' & ' + l0_prompt    + ')'

l1hf_l2p     = '(' + l1_heavyfake + ' & ' + l2_prompt + ')'
l2hf_l1p     = '(' + l2_heavyfake + ' & ' + l1_prompt + ')'
l1hf_l2p_l0p = '(' + l1hf_l2p     + ' & ' + l0_prompt + ')'
l2hf_l1p_l0p = '(' + l2hf_l1p     + ' & ' + l0_prompt + ')'

l1_LVtx_dr  = '( abs(l1_gen_match_vtx_x) + abs(l1_gen_match_vtx_y) + abs(l1_gen_match_vtx_z) )'
l2_LVtx_dr  = '( abs(l2_gen_match_vtx_x) + abs(l2_gen_match_vtx_y) + abs(l2_gen_match_vtx_z) )'

DeltaLVtx = '( ' + l1_LVtx_dr + ' - ' + l2_LVtx_dr + ' )' 
SumLVtx   = '( ' + l1_LVtx_dr + ' + ' + l2_LVtx_dr + ' )'

#sameVtx_dr = '( ( 2 *( ' + l1_vtx_dr + ' - ' + l2_vtx_dr + ' ) / ( ' + l1_vtx_dr + ' + ' + l2_vtx_dr + ' ) ) < 0.01 )'
#sameVtx_dr = '( ( ' + DeltaLVtx + ' / ' + SumLVtx + ' ) < 0.005 )'
sameVtx_dr = '( ' + DeltaLVtx + ' == 0 )'
sameVtx    = '( l2_simProdZ == l1_simProdZ & l1_simProdZ != 0 )'

two_prompt            = '(' + l1_prompt     + ' & ' + l2_prompt      +  ')'
two_prompt_new        = '(' + l1_prompt_new + ' & ' + l2_prompt_new  +  ')'
two_prompt_dr         = '(' + l1_prompt_dr  + ' & ' + l2_prompt_dr   +  ')'
one_fake_xor          = '(' + l1f_l2p       + ' | ' + l2f_l1p        +  ')' 
one_fake_xor_new      = '(' + l1f_l2p_new   + ' | ' + l2f_l1p_new    +  ')' 
one_fake_xor_dr       = '(' + l1f_l2p_dr    + ' | ' + l2f_l1p_dr     +  ')' 
two_fakes             = '(' + l1_fake       + ' & ' + l2_fake        +  ')'  
two_fakes_new         = '(' + l1_fake_new   + ' & ' + l2_fake_new    +  ')'  
two_fakes_dr          = '(' + l1_fake_dr    + ' & ' + l2_fake_dr     +  ')'  
twoHeavyFakes         = '(' + l1_heavyfake  + ' & ' + l2_heavyfake   +  ')'  
twoFakes_sameVtx      = '(' + two_fakes     + ' & l2_simProdZ == l1_simProdZ & l1_simProdZ != 0)'  
twoFakes_sameVtx_dr   = '(' + two_fakes_dr  + ' & ' + sameVtx_dr     +  ')'
twoHeavyFakes_sameVtx = '(' + twoHeavyFakes + ' & l2_simProdZ == l1_simProdZ & l1_simProdZ != 0)'  

no_ghosts    = '( l1_simType < 1001 & l2_simType < 1001 )'
no_fakes     = two_prompt
no_fakes_new = two_prompt_new
no_fakes_dr  = two_prompt_dr

#sameJet     = '( l1_jet_pt == l2_jet_pt)'
#sameJet     = '( abs(l1_jet_pt - l2_jet_pt) < 1 )'
sameJet     = '( abs(l1_jet_pt - l2_jet_pt) < 1 & hnl_dr_12 < 0.8 )' # 0.8 is twice the jet size
twoFakes_sameJet           = '(' + two_fakes           + ' & ' + sameJet + ')' 
twoFakes_sameJet_dr        = '(' + two_fakes_dr        + ' & ' + sameJet + ')' 
twoFakes_sameJet_new       = '(' + two_fakes_new       + ' & ' + sameJet + ')' 
twoFakes_sameJet_l0p_new   = '(' + two_fakes_new       + ' & ' + sameJet + ' & ' + l0_prompt_new  + ')' 
twoFakes_sameVtxJet        = '(' + twoFakes_sameVtx    + ' & ' + sameJet + ')' 
twoFakes_sameVtxJet_l0p    = '(' + twoFakes_sameVtx    + ' & ' + sameJet + ' & ' + l0_prompt      + ')'
twoFakes_sameVtxJet_l0p_dr = '(' + twoFakes_sameVtx_dr + ' & ' + sameJet + ' & ' + l0_prompt_m_dr + ')'

def LepIDIsoPass(lep, ID, iso_cut):
#    cut_var = ' & l%i_id_%s & l%i_reliso05_03 < %f'%(lep, ID, lep, iso_cut)
#    cut_var = ' & l%i_id_%s & l%i_reliso05 < %f'%(lep, ID, lep, iso_cut)
    cut_var = ' & l%i_id_%s & l%i_reliso_rho_04 < %f'%(lep, ID, lep, iso_cut) ## FROM v2 ON
    return cut_var

def LepIDIsoFail(lep, ID, iso_cut):
#    cut_var = ' & l%i_id_%s & l%i_reliso05_03 > %f'%(lep, ID, lep, iso_cut)
#    cut_var = ' & l%i_id_%s & l%i_reliso05 > %f'%(lep, ID, lep, iso_cut)
    cut_var = ' & l%i_id_%s & l%i_reliso_rho_04 > %f'%(lep, ID, lep, iso_cut) ## FROM v2 ON
    return cut_var

def LepIDIsoFail_leq1(lep, ID, iso_cut):
#    cut_var = ' & l%i_id_%s & l%i_reliso05_03 > %f & l%i_reliso05_03 < 1'%(lep, ID, lep, iso_cut, lep)
#    cut_var = ' & l%i_id_%s & l%i_reliso05 > %f & l%i_reliso05 < 1'%(lep, ID, lep, iso_cut, lep)
    cut_var = ' & l%i_id_%s & l%i_reliso_rho_04 > %f & l%i_reliso_rho_04 < 1'%(lep, ID, lep, iso_cut, lep)  ## FROM v2 ON
    return cut_var

def bothLoose(iso_cut): 
    bL =  '& ( ( 1 ' + LepIDIsoFail(1, 'l', iso_cut) + LepIDIsoFail(2, 'l', iso_cut) + ' ) | ( 1 ' 
    bL += LepIDIsoFail(1, 'l', iso_cut) + LepIDIsoPass(2, 'l', iso_cut) + ' ) | ( 1 '
    bL += LepIDIsoPass(1, 'l', iso_cut) + LepIDIsoFail(2, 'l', iso_cut) + ' ) | ( 1 '
    bL += LepIDIsoPass(1, 'l', iso_cut) + LepIDIsoPass(2, 'l', iso_cut) + ' ) )'

    bL = ' & hnl_iso04_rel_rhoArea > %f'%iso_cut 
    return bL

LOOSE         = ' & (l1_pt > 3 & l2_pt > 3 & l0_id_t & l0_reliso_rho_04 < 0.15 & l1_id_l & l2_id_l & hnl_iso04_rel_rhoArea < 1 )'
LOOSENOTTIGHT = ' & (l1_pt > 3 & l2_pt > 3 & l0_id_t & l0_reliso_rho_04 < 0.15 & l1_id_l & l2_id_l & (l1_reliso_rho_04 > 0.15 | l2_reliso_rho_04 > 0.15) & hnl_iso04_rel_rhoArea < 1 )' 
TIGHT         = ' & (l1_pt > 3 & l2_pt > 3 & l0_id_t & l0_reliso_rho_04 < 0.15 & l1_id_l & l2_id_l & l1_reliso_rho_04 < 0.15 & l2_reliso_rho_04 < 0.15 )' 

#twoLepObjIsoleq1  = ' & ( max(l1_reliso05_03 * l1_pt, l2_reliso05_03 * l2_pt) / (hnl_hn_vis_pt) ) < 1'
#twoLepObjIsoleq1  = ' & ( max(l1_reliso05 * l1_pt, l2_reliso05 * l2_pt) / (hnl_hn_vis_pt) ) < 1'
twoLepObjIsoleq1  = ' & ( max(l1_reliso_rho_04 * l1_pt, l2_reliso_rho_04 * l2_pt) / (hnl_hn_vis_pt) ) < 1'   ## FROM v2 ON
twoLepObjIsoleq1  = ' & hnl_iso04_rel_rhoArea < 1' 

def ptConeLep(lep, iso_cut):
#    fill_var = '(l%i_pt) * (1 + l%i_reliso05_03 - %f)'%(lep, lep, iso_cut)
#    fill_var = '(l%i_pt) * (1 + l%i_reliso05 - %f)'%(lep, lep, iso_cut)
    fill_var = '(l%i_pt) * (1 + l%i_reliso_rho_04 - %f)'%(lep, lep, iso_cut)
    return fill_var

def ptCone2F(iso_cut):
    fill_var = '(hnl_hn_vis_pt) * (1 - %f) + max(l1_pt * l1_reliso05_03, l2_pt * l2_reliso05_03)'%iso_cut
    return fill_var

def ptCone2F_dimu(iso_cut):
#    fill_var = '(hnl_hn_vis_pt) * (1 - %f) + max(l1_pt * l1_reliso05_03, l2_pt * l2_reliso05_03) + (hnl_dr_12 / 0.5) * min(l1_pt * l1_reliso05_03, l2_pt * l2_reliso05_03)'%iso_cut
#    fill_var = '(hnl_hn_vis_pt) * (1 - %f) + max(l1_pt * l1_reliso05, l2_pt * l2_reliso05) + (hnl_dr_12 / 0.5) * min(l1_pt * l1_reliso05, l2_pt * l2_reliso05)'%iso_cut
#    fill_var = '(hnl_hn_vis_pt) * (1 - %f + hnl_iso03_rel_deltaBeta)'%iso_cut
#    fill_var = '(hnl_hn_vis_pt) * (1 - %f + hnl_iso03_rel_rhoArea)'%iso_cut
#    fill_var = '(hnl_hn_vis_pt) * (1 - %f + hnl_iso04_rel_deltaBeta)'%iso_cut
    fill_var = '(hnl_hn_vis_pt) * (1 - %f + hnl_iso04_rel_rhoArea)'%iso_cut
    return fill_var

PTCONE = '(  ( hnl_hn_vis_pt * (hnl_iso04_rel_rhoArea<0.15) ) + ( (hnl_iso04_rel_rhoArea>=0.15) * ( hnl_hn_vis_pt * (1. + hnl_iso04_rel_rhoArea - 0.15) ) )  )'

eta_0to1p2   = '( abs(l1_eta) < 1.2 & abs(l2_eta) < 1.2 )'
eta_1p2to2p1 = '( abs(l1_eta) > 1.2 & abs(l2_eta) > 1.2 & abs(l1_eta) < 2.1 & abs(l2_eta) < 2.1)'
eta_2p1to2p4 = '( abs(l1_eta) > 2.1 & abs(l2_eta) > 2.1 & abs(l1_eta) < 2.4 & abs(l2_eta) < 2.4)'

eta_bins = [['0_to_1p2'  , eta_0to1p2],
            ['1p2_to_2p1', eta_1p2to2p1],
            ['2p1_to_2p4', eta_2p1to2p4]]

isolst = [0.10,0.11,0.12,0.13,0.14,0.15,0.16,0.17,0.18,0.19,0.20]

b_pt_old    = np.arange(5.,100,5)
b_pt        = np.array([ 0., 5., 10., 15., 20., 25., 35., 50., 70.])
b_2d        = np.arange(0., 10, 0.2)
b_m         = np.arange(0., 5, 0.25)
b_M         = np.arange(0.,200,2)
b_eta       = np.array([0., 1.2, 2.1, 2.4]) 
b_rho       = np.arange(-100.,100,4)
b_rho_crs   = np.arange(0.,10,0.25)
b_rho       = np.arange(0.,15,0.25)
b_dR        = np.arange(0.,6,0.05)
b_dR_coarse = np.arange(0.,6,0.2)
b_dR_Coarse = np.arange(0.,6,0.4)
b_z         = np.arange(-1.5,1.5,0.06)
b_abs_z     = np.arange(0.,2,0.05)
b_z_fine    = np.arange(-0.02,0.02,0.0001)
b_st        = np.arange(-20,20,1)
b_sf        = np.arange(-20,20,1)
b_y = np.arange(0.,1.,0.1)
framer = rt.TH2F('','',len(b_pt)-1,b_pt,len(b_y)-1,b_y)
framer.GetYaxis().SetRangeUser(0.,0.5)

cr_tt     = 'abs(hnl_m_12 - 91.18) > 15  &  abs(hnl_w_vis_m - 91.18) > 15  &  nbj >= 1'
q_pt      = 'l0_pt > 35  &  l1_pt > 4  &  l2_pt > 4  &  l1_q != l2_q'
im_par_l0 = 'abs(l0_dxy) < 0.045 & abs(l0_dz) < 0.2'
tt_v0 = cr_tt + ' & ' + q_pt + ' & ' + im_par_l0
####################################################################################################
def countFakesWithoutCuts(sample_dir):
    ch = basename(split(normpath(sample_dir))[0]) 
    sample_name = basename(normpath(sample_dir))
    fin = rt.TFile(inDir + sample_dir + suffix)
    t = fin.Get('tree')
    n_entries            = t.GetEntriesFast() 
    n_one_fake_xor       = t.GetEntries(one_fake_xor)
    n_two_fakes          = t.GetEntries(two_fakes)
    n_twoFakes_sameVtx = t.GetEntries(twoFakes_sameVtx)
    print sample_name + '_%s\n\t entries \t\t'%ch, '100.0% \t'                                        , n_entries 
    print '\t one_fake_xor \t\t'          , '{:.1%} \t'.format(n_one_fake_xor/n_entries)       , n_one_fake_xor      
    print '\t two_fakes \t\t'             , '{:.1%} \t'.format(n_two_fakes/n_entries)          , n_two_fakes         
    print '\t twoFakes_sameVtx \t'        , '{:.1%} \t'.format(n_twoFakes_sameVtx/n_entries)   , n_twoFakes_sameVtx
    print ''
        
####################################################################################################
def countFakes(DZ=True,DISP=True):
    samples = ['WJ','TT','DY']
    cuts = 'l0_id_t & l0_reliso_rho_04 < 0.15 & l1_id_l & l2_id_l & l1_reliso_rho_04 < 0.15 & l2_reliso_rho_04 < 0.15'
    if DZ == True:
        cuts += ' & abs(l1_dz) < 2 & abs(l2_dz) < 2'
    if DISP == True:
        cuts += ' & hnl_2d_disp > 0.5'
    ch = 'mu'
    for sample in samples: 
        if sample == 'DY':
            t = rt.TChain('tree')
            t.Add(inDir + DYBB_dir_m + suffix)
            t.Add(inDir + DY50_dir_m + suffix)
            t.Add(inDir + DY50_ext_dir_m + suffix)
            t.Add(inDir + DY50_dir_m + suffix)
            t.Add(inDir + DY50_ext_dir_m + suffix)
            print '\t', sample, 'entries before selection:', t.GetEntries()
        if sample == 'TT':
            fin = rt.TFile(inDir + TT_dir_m + suffix)
            t = fin.Get('tree')
            print '\t', sample, 'entries before selection:', t.GetEntries()
        if sample == 'WJ':
            t = rt.TChain('tree')
            t.Add(inDir + W_dir_m + suffix)
            t.Add(inDir + W_ext_dir_m + suffix)
            print '\t', sample, 'entries before selection:', t.GetEntries()
        n_entries             = t.GetEntries(cuts) 
        print '\t',sample, 'entries after selection:', n_entries
        print '\t cuts:', cuts
        if ch == 'mu':
            n_l0_is_fake      = t.GetEntries(cuts + ' & ' + l0_fake_new)
            n_l0_is_fake_dr   = t.GetEntries(cuts + ' & ' + l0_fake_m_dr)
        if ch == 'e':
            n_l0_is_fake      = 0
            n_l0_is_fake_dr   = t.GetEntries(cuts + ' & ' + l0_fake_e_dr)
        print '\t l0_is_fake \t\t'            , '{:.1%} \t'.format(n_l0_is_fake/n_entries)                 , n_l0_is_fake     
        print '\t l0_is_fake_dr \t\t'         , '{:.1%} \t'.format(n_l0_is_fake_dr/n_entries)              , n_l0_is_fake_dr     

        n_no_fakes            = t.GetEntries(cuts + ' & ' + no_fakes_new)
        print '\t no_fakes \t\t'              , '{:.1%} \t'.format(n_no_fakes/n_entries)                   , n_no_fakes      

        n_no_fakes_dr         = t.GetEntries(cuts + ' & ' + no_fakes_dr)
        print '\t no_fakes_dr \t\t'           , '{:.1%} \t'.format(n_no_fakes_dr/n_entries)                , n_no_fakes_dr      

        n_one_fake_xor        = t.GetEntries(cuts + ' & ' + one_fake_xor_new)
        print '\t one_fake_xor \t\t'          , '{:.1%} \t'.format(n_one_fake_xor/n_entries)               , n_one_fake_xor      

        n_one_fake_xor_dr     = t.GetEntries(cuts + ' & ' + one_fake_xor_dr)
        print '\t one_fake_xor_dr \t'         , '{:.1%} \t'.format(n_one_fake_xor_dr/n_entries)            , n_one_fake_xor_dr      

        n_two_fakes           = t.GetEntries(cuts + ' & ' + two_fakes_new)
        print '\t two_fakes \t\t'             , '{:.1%} \t'.format(n_two_fakes/n_entries)                  , n_two_fakes         

        n_two_fakes_dr        = t.GetEntries(cuts + ' & ' + two_fakes_dr)
        print '\t two_fakes_dr\t\t'           , '{:.1%} \t'.format(n_two_fakes_dr/n_entries)               , n_two_fakes_dr         

        n_twoFakes_sameJet    = t.GetEntries(cuts + ' & ' + twoFakes_sameJet_new) # THIS IS UPDATED, NO WORRIES
        print '\t twoFakes_sameJet \t'        , '{:.1%} \t'.format(n_twoFakes_sameJet/n_two_fakes)         , n_twoFakes_sameJet   , '\t({:.1%})'.format(n_twoFakes_sameJet/n_entries)

        n_twoFakes_sameVtx    = t.GetEntries(cuts + ' & ' + twoFakes_sameVtx)
        print '\t twoFakes_sameVtx \t'        , '{:.1%} \t'.format(n_twoFakes_sameVtx/n_two_fakes)         , n_twoFakes_sameVtx   , '\t({:.1%})'.format(n_twoFakes_sameVtx/n_entries)

        n_twoFakes_sameVtx_dr = t.GetEntries(cuts + ' & ' + twoFakes_sameVtx_dr)
        print '\t twoFakes_sameVtx_dr\t'      , '{:.1%} \t'.format(n_twoFakes_sameVtx_dr/n_two_fakes_dr)   , n_twoFakes_sameVtx_dr, '\t({:.1%})'.format(n_twoFakes_sameVtx_dr/n_entries)

        n_twoFakes_sameVtxJet = t.GetEntries(cuts + ' & ' + twoFakes_sameVtxJet)
        print '\t twoFakes_sameVtxJet \t'     , '{:.1%} \t'.format(n_twoFakes_sameVtxJet/n_two_fakes)      , n_twoFakes_sameVtxJet, '\t({:.1%})'.format(n_twoFakes_sameVtxJet/n_entries)


        if DZ == True: sample += '_dz'
        if DISP ==True: sample += '_disp'
        sys.stdout = open(plotDir + sample + '_%s'%ch + '.py', 'w+')

        print '\n\t', sample + '_%s \n\tcuts:\t%s \n'%(ch, cuts)
        print '\t entries \t\t'               , '100.0% \t'                                                , n_entries 
        print '\t l0_is_fake \t\t'            , '{:.1%} \t'.format(n_l0_is_fake/n_entries)                 , n_l0_is_fake     
        print '\t l0_is_fake_dr \t\t'         , '{:.1%} \t'.format(n_l0_is_fake_dr/n_entries)              , n_l0_is_fake_dr     
        print '\t no_fakes \t\t'              , '{:.1%} \t'.format(n_no_fakes/n_entries)                   , n_no_fakes      
        print '\t no_fakes_dr \t\t'           , '{:.1%} \t'.format(n_no_fakes_dr/n_entries)                , n_no_fakes_dr      
        print '\t one_fake_xor \t\t'          , '{:.1%} \t'.format(n_one_fake_xor/n_entries)               , n_one_fake_xor      
        print '\t one_fake_xor_dr \t'         , '{:.1%} \t'.format(n_one_fake_xor_dr/n_entries)            , n_one_fake_xor_dr      
        print '\t two_fakes \t\t'             , '{:.1%} \t'.format(n_two_fakes/n_entries)                  , n_two_fakes         
        print '\t two_fakes_dr\t\t'           , '{:.1%} \t'.format(n_two_fakes_dr/n_entries)               , n_two_fakes_dr         
        print '\t twoFakes_sameVtx \t'        , '{:.1%} \t'.format(n_twoFakes_sameVtx/n_two_fakes)         , n_twoFakes_sameVtx   , '\t({:.1%})'.format(n_twoFakes_sameVtx/n_entries)
        print '\t twoFakes_sameJet \t'        , '{:.1%} \t'.format(n_twoFakes_sameJet/n_two_fakes)         , n_twoFakes_sameJet   , '\t({:.1%})'.format(n_twoFakes_sameJet/n_entries)
        print '\t twoFakes_sameVtxJet \t'     , '{:.1%} \t'.format(n_twoFakes_sameVtxJet/n_two_fakes)      , n_twoFakes_sameVtxJet, '\t({:.1%})'.format(n_twoFakes_sameVtxJet/n_entries)
        print '\t twoFakes_sameVtx_dr\t'      , '{:.1%} \t'.format(n_twoFakes_sameVtx_dr/n_two_fakes_dr)   , n_twoFakes_sameVtx_dr, '\t({:.1%})'.format(n_twoFakes_sameVtx_dr/n_entries)
        print ''
        
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        
        print '\t', sample + '_%s\t\t done\n'%ch
####################################################################################################

####################################################################################################
def measureTTLratio(isData=False,DISP=True):
    iso_cut = 0.15
    iso_str = str(int(iso_cut * 100))
    ch          = 'mu'
    sample_name = 'data'

    disp = ' & abs(l1_dz) < 2 & abs(l2_dz) < 2'
    dsp = ''
    if DISP == True:
        dsp = '_disp'
        disp += ' & hnl_2d_disp > 0.5'

    if isData == False: 
        fin = rt.TFile(inDir + TT_dir_m + suffix)
#        fin = rt.TFile(inDir + W_dir_m + suffix) # for debuggin: faster
        t = fin.Get('tree')
        sample_name = 'TTbar'
#        cut_T = twoFakes_sameJet_new + LepIDIsoPass(0, 't', iso_cut) + LepIDIsoPass(1, 'l', iso_cut) + LepIDIsoPass(2, 'l', iso_cut) + disp
#        cut_L = twoFakes_sameJet_new + LepIDIsoPass(0, 't', iso_cut) + bothLoose(iso_cut) + twoLepObjIsoleq1 + disp
        cut_T = twoFakes_sameJet_new + TIGHT + disp
        cut_L = twoFakes_sameJet_new + LOOSE + disp

    if isData == True: 
    ## DATA
        t = rt.TChain('tree')
        t.Add(inDir + data_m_B + suffix)
        t.Add(inDir + data_m_C + suffix)
        t.Add(inDir + data_m_D + suffix)
        t.Add(inDir + data_m_F + suffix)
#        cut_T = 'abs(l1_jet_pt - l2_jet_pt) < 1 & nbj > 0 & hnl_2d_disp > 0.5 & abs(l1_dz) < 2 & abs(l2_dz) < 2' + LepIDIsoPass(0, 't', iso_cut) + LepIDIsoPass(1, 'l', iso_cut) + LepIDIsoPass(2, 'l', iso_cut)
#        cut_L = 'abs(l1_jet_pt - l2_jet_pt) < 1 & nbj > 0 & hnl_2d_disp > 0.5 & abs(l1_dz) < 2 & abs(l2_dz) < 2' + LepIDIsoPass(0, 't', iso_cut) + bothLoose(iso_cut) + twoLepObjIsoleq1 
        cut_T = 'abs(l1_jet_pt - l2_jet_pt) < 1 & hnl_dr_12 < 0.8 & nbj > 0 & hnl_2d_disp > 0.5 & abs(l1_dz) < 2 & abs(l2_dz) < 2' + TIGHT ## UPDATED TO LIMIT JET-JUNK WITH LARGE DR
        cut_L = 'abs(l1_jet_pt - l2_jet_pt) < 1 & hnl_dr_12 < 0.8 & nbj > 0 & hnl_2d_disp > 0.5 & abs(l1_dz) < 2 & abs(l2_dz) < 2' + LOOSE ## UPDATED TO LIMIT JET-JUNK WITH LARGE DR

    h_pt_eta_T = rt.TH2F('pt_eta_T','pt_eta_T',len(b_pt)-1,b_pt,len(b_eta)-1,b_eta)
    h_pt_eta_L = rt.TH2F('pt_eta_L','pt_eta_L',len(b_pt)-1,b_pt,len(b_eta)-1,b_eta)

    t.Draw('abs(hnl_hn_vis_eta) : ' + PTCONE + ' >> pt_eta_T', cut_T)
    t.Draw('abs(hnl_hn_vis_eta) : ' + PTCONE + ' >> pt_eta_L', cut_L)
    print 'tree entries T & L: ', t.GetEntries(cut_T), t.GetEntries(cut_L)

    print '%s iso%s ... two fakes done\nnumerator: %i, denominator: %i'%(sample_name, iso_str, h_pt_eta_T.GetEntries(), h_pt_eta_L.GetEntries())


#    h_pt_eta_d.Add(h_pt_eta_n) ## NOW BOTHLOOSE UPDATED, NO MORE ADDING NEEDED!

    c_pt_eta = rt.TCanvas('ptCone_eta', 'ptCone_eta')
    h_pt_eta_T.Divide(h_pt_eta_L)
    h_pt_eta_T.Draw('colz')
    h_pt_eta_T.SetTitle('; p_{T}^{Cone} [GeV]; DiMuon |#eta|; tight-to-loose ratio')
    pf.showlogoprelimsim('CMS')
    pf.showTitle('TTL Ratio')
    save(c_pt_eta, iso_cut, 'TTL_' + sample_name, ch, '')

    # DO AGAIN WITH THREE DIFFERENT TEFFS TO GET ERROR
####################################################################################################

####################################################################################################
def checkTTLratio(DISP=True):
    samples = ['DY', 'TT', 'WJ']
    h_pt_1f = []; h_pt_2f = []; i = 0
    iso_cut = 0.15
    iso_str = str(int(iso_cut * 100))
    ch = 'mu'

    disp = ' & abs(l1_dz) < 2 & abs(l2_dz) < 2'
    dsp = ''
    if DISP == True:
        dsp = '_disp'
        disp += ' & hnl_2d_disp > 0.5'

    for sample in samples: 
        if sample == 'DY':
            t = rt.TChain('tree')
            t.Add(inDir + DYBB_dir_m + suffix)
            t.Add(inDir + DY50_dir_m + suffix)
            t.Add(inDir + DY50_ext_dir_m + suffix)
            t.Add(inDir + DY50_dir_m + suffix)
            t.Add(inDir + DY50_ext_dir_m + suffix)
            print sample, t.GetEntries()
        if sample == 'TT':
            fin = rt.TFile(inDir + TT_dir_m + suffix)
            t = fin.Get('tree')
            print sample, t.GetEntries()
        if sample == 'WJ':
            t = rt.TChain('tree')
            t.Add(inDir + W_dir_m + suffix)
            t.Add(inDir + W_ext_dir_m + suffix)
            print sample, t.GetEntries()
        if DISP == True:
            sample += dsp 

        h_pt_l1_d  = rt.TH1F('pt_cone_l1_d', 'pt_cone_l1_d',len(b_pt)-1,b_pt)
        h_pt_l2_d  = rt.TH1F('pt_cone_l2_d', 'pt_cone_l2_d',len(b_pt)-1,b_pt)
        h_pt_2f_L  = rt.TH1F('pt_cone_2f_L', 'pt_cone_2f_L',len(b_pt)-1,b_pt)

        h_pt_l1_n  = rt.TH1F('pt_cone_l1_n', 'pt_cone_l1_n',len(b_pt)-1,b_pt)
        h_pt_l2_n  = rt.TH1F('pt_cone_l2_n', 'pt_cone_l2_n',len(b_pt)-1,b_pt)
        h_pt_2f_T  = rt.TH1F('pt_cone_2f_T', 'pt_cone_2f_T',len(b_pt)-1,b_pt)


        print 'drawing %s iso%s ...'%(sample, iso_str)

#        print '1f cuts', l1hf_l2p_l0p_new + LepIDIsoPass(0, 't', iso_cut) + LepIDIsoPass(1, 't', iso_cut)
#        print '2f cuts', twoFakes_sameJet_new + LepIDIsoPass(0, 't', iso_cut) + LepIDIsoPass(1, 't', iso_cut) + LepIDIsoPass(2, 't', iso_cut)
 
#        t.Draw(                  'l1_pt >> pt_cone_l1_n' , l1f_l2p_l0p_new + LepIDIsoPass(0, 't', iso_cut) + LepIDIsoPass(1, 't', iso_cut) + ' & hnl_2d_disp > 0.5')
#        t.Draw(ptConeLep(1, iso_cut) + '>> pt_cone_l1_d' , l1f_l2p_l0p_new + LepIDIsoPass(0, 't', iso_cut) + LepIDIsoFail_leq1(1, 't', iso_cut) + ' & hnl_2d_disp > 0.5')
#        print '%s iso%s ... l1 done'%(sample, iso_str)
# 
#        t.Draw(                  'l2_pt >> pt_cone_l2_n' , l2f_l1p_l0p_new + LepIDIsoPass(0, 't', iso_cut) + LepIDIsoPass(2, 't', iso_cut) + ' & hnl_2d_disp > 0.5')
#        t.Draw(ptConeLep(2, iso_cut) + '>> pt_cone_l2_d' , l2f_l1p_l0p_new + LepIDIsoPass(0, 't', iso_cut) + LepIDIsoFail_leq1(2, 't', iso_cut) + ' & hnl_2d_disp > 0.5')
#        print '%s iso%s ... l2 done'%(sample, iso_str)

#        t.Draw('hnl_hn_vis_pt >> pt_cone_2f_T', 
        t.Draw(PTCONE + ' >> pt_cone_2f_T', 
#               twoFakes_sameJet_new + LepIDIsoPass(0, 't', iso_cut) + LepIDIsoPass(1, 'l', iso_cut) + LepIDIsoPass(2, 'l', iso_cut) + disp )
               twoFakes_sameJet_new + TIGHT + disp)
#               twoFakes_sameJet_l0p_new + LepIDIsoPass(0, 't', iso_cut) + LepIDIsoPass(1, 'l', iso_cut) + LepIDIsoPass(2, 'l', iso_cut) + disp )
# IMO MORE JUSTIFIED NOT TO REQUIRE L0P SINCE IN DATA WE DON'T KNOW EITHER
#        t.Draw(ptCone2F_dimu(iso_cut) + '>> pt_cone_2f_L' ,
        t.Draw(PTCONE + '>> pt_cone_2f_L' ,
#               twoFakes_sameJet_new + LepIDIsoPass(0, 't', iso_cut) + bothLoose(iso_cut) + twoLepObjIsoleq1 + disp )
               twoFakes_sameJet_new + LOOSE + disp )    
               #### FULL BULK
#               twoFakes_sameJet_new + LepIDIsoPass(0, 't', iso_cut) + bothLoose(iso_cut) + disp )
#               twoFakes_sameJet_l0p_new + LepIDIsoPass(0, 't', iso_cut) + bothLoose(iso_cut) + twoLepObjIsoleq1 + disp )
        print '%s iso%s ... two fakes done'%(sample, iso_str)

        h_pt_1f.append(rt.TEfficiency(h_pt_l1_n, h_pt_l1_d))
        h_pt_1f[i].SetTitle('%s; p_{T}^{Cone} [GeV]; tight-to-loose ratio (one fake)'%sample)
        h_pt_1f[i].SetMarkerColor(rt.kGreen+i*2)

        c_pt_1f = rt.TCanvas('ptCone_1f', 'ptCone_1f')
        h_pt_1f[i].Draw()
        pf.showlogoprelimsim('CMS')
#        save(c_pt_1f, iso_cut, sample, ch, eta)

        h_pt_2f.append(rt.TEfficiency(h_pt_2f_T, h_pt_2f_L))
        h_pt_2f[i].SetTitle('%s; p_{T}^{Cone} [GeV]; tight-to-loose ratio (two fakes same jet)'%sample)
        h_pt_2f[i].SetMarkerColor(rt.kGreen+i*2)

        c_pt_2f = rt.TCanvas('ptCone_2f', 'ptCone_2f')
        h_pt_2f[i].Draw()
        pf.showlogoprelimsim('CMS')
        save(c_pt_2f, iso_cut, sample, ch)

        c_pt_cmprd = rt.TCanvas('ptCone_cmprd', 'ptCone_cmprd')
        framer.Draw()
        framer.GetYaxis().SetTitle('tight-to-loose ratio')
        framer.GetXaxis().SetTitle('p_{T}^{Cone} [GeV]')
        h_pt_1f[i].Draw('same')
        h_pt_1f[i].SetMarkerColor(rt.kBlue)
        h_pt_2f[i].Draw('same')
        leg = rt.TLegend(0.47, 0.78, 0.7, 0.9)
        leg.AddEntry(h_pt_2f[i], 'two fakes')
        leg.AddEntry(h_pt_1f[i], 'one fake ')
        leg.Draw()
        pf.showlogoprelimsim('CMS')
#        save(c_pt_cmprd, iso_cut, sample, ch, eta)

        i += 1

    if len(samples) > 1:

        c_pt_1f = rt.TCanvas('ptCone_1f', 'ptCone_1f')
        framer.Draw()
        framer.GetYaxis().SetTitle('tight-to-loose ratio')
        framer.GetXaxis().SetTitle('p_{T}^{Cone} [GeV]')
        for i in range(len(samples)):
            h_pt_1f[i].Draw('same')
        c_pt_1f.BuildLegend(0.18, 0.78, 0.41, 0.9)
    #    c_pt_1f.SetLogz()
        pf.showlogoprelimsim('CMS')
#        save(c_pt_1f, iso_cut, 'cmbnd', ch)

        c_pt_2f = rt.TCanvas('ptCone_2f', 'ptCone_2f')
        framer.Draw()
        framer.GetYaxis().SetTitle('tight-to-loose ratio')
        framer.GetXaxis().SetTitle('p_{T}^{Cone} [GeV]')
        leg = rt.TLegend(0.57, 0.78, 0.8, 0.9)
        for i in range(len(samples)-1): # forget WJ for now
            h_pt_2f[i].Draw('same')
            leg.AddEntry(h_pt_2f[i], h_pt_2f[i].GetTitle())
        leg.Draw()
        pf.showlogoprelimsim('CMS')
        save(c_pt_2f, iso_cut, 'cmbnd'+dsp, ch)

    print sample + '_%s_iso%s\t done'%(ch, iso_str)
####################################################################################################

####################################################################################################
def checkDRandM12(DISP=True):
    iso_cut = 0.15
    disp = ''
    dsp = ''
    if DISP == True:
       disp = ' & hnl_2d_disp > 0.5'
       dsp = '_disp'
    tupels = [ [DY50_ext_dir_m, ['', '1']], [TT_dir_m, ['', '1']], [W_ext_dir_m, ['', '1']] ]
    for tupel in tupels:
        h,c = plot(tupel, var = 'hnl_dr_12', name = '2fsJnw_dR'+dsp, binsX = b_dR, xtitle = '#DeltaR(#mu_{1}, #mu_{2})', 
                   cut = twoFakes_sameJet_new + LepIDIsoPass(0, 't', iso_cut) + bothLoose(iso_cut) + twoLepObjIsoleq1 + disp )

        h,c = plot(tupel, var = 'hnl_m_12', name = '2fsJnw_m2l'+dsp, binsX = b_m, xtitle = 'm(#mu_{1}, #mu_{2})', 
               cut = twoFakes_sameJet_new + LepIDIsoPass(0, 't', iso_cut) + bothLoose(iso_cut) + twoLepObjIsoleq1 + disp )
####################################################################################################

####################################################################################################
def checkTypeFlavour(DISP=True):
    iso_cut = 0.15
    disp = ''
    dsp = ''
    if DISP == True:
       disp = ' & hnl_2d_disp > 0.5'
       dsp = '_disp'
    tupels = [ [DY50_ext_dir_m, ['', '1']], [TT_dir_m, ['', '1']]]#, [W_ext_dir_m, ['', '1']] ]
    for tupel in tupels:
        h,c = plot(tupel, var = 'l1_simFlavour : l1_simType', name = '2fsJnw_sT_sF'+dsp, binsX = b_st, binsY = b_sf, xtitle = 'simType(#mu_{1})', ytitle = 'simFlavour(#mu_{2})', mode = 2, 
                   cut = twoFakes_sameJet_new + LepIDIsoPass(0, 't', iso_cut) + bothLoose(iso_cut) + twoLepObjIsoleq1 + disp )
####################################################################################################

####################################################################################################
def TTbarStudy():
    tupels = [[TT_dir_m, ['1', '1']], [TT_dir_m, ['disp0p5', 'hnl_2d_disp > 0.5']], [DY50_dir_m, ['1','1']], [W_dir_m, ['1','1']],]
    tupels = [tupels[0]]
    for tupel in tupels: 
        iso_cut = 0.15
        sample_dir, cutuple = tupel
        cut_name = cutuple[0]
        cuts = cutuple[1]
        iso_str = str(int(iso_cut * 100))

        b_rho       = np.arange(-100.,100,4)
        b_rho_crs= np.arange(0.,10,0.25)
        b_rho    = np.arange(0.,15,0.25)
        b_dR        = np.arange(0.,6,0.05)
        b_dR_coarse = np.arange(0.,6,0.2)
        b_dR_Coarse = np.arange(0.,6,0.4)
        b_z         = np.arange(-1.5,1.5,0.06)
        b_abs_z     = np.arange(0.,2,0.05)
        b_z_fine    = np.arange(-0.02,0.02,0.0001)
        b_st        = np.arange(-20,20,1)

        Delta_R_l12 = 'sqrt( (l2_simPhi - l1_simPhi)^2 + (l2_simEta - l1_simEta)^2 )'

        h, c = plot(tupel = tupel, var = 'l2_simProdRho - l1_simProdRho', name = 'dRho',
                    binsX = b_rho_crs, xtitle = '#Delta#rho(#mu_{1}, #mu_{2}) [cm]', cut = two_fakes, log=True)

        h, c = plot(tupel = tupel, var = 'l2_simProdZ - l1_simProdZ', name = 'dZ',
                    binsX = b_z, xtitle = '#DeltaZ(#mu_{1}, #mu_{2}) [cm]', cut = two_fakes, log=True)

        h, c = plot(tupel = tupel, var = Delta_R_l12 + ' : l2_simProdZ - l1_simProdZ', name = 'dZ_dR',
                    binsX = b_z, binsY =  b_dR, mode = 2, xtitle = '#DeltaZ(#mu_{1}, #mu_{2}) [cm]', ytitle = '#DeltaR(#mu_{1}, #mu_{2})', 
                    cut = two_fakes, log=True)

        h, c = plot(tupel = tupel, var = 'l2_simType : l1_simType', name = 'simType_diffVtx',
                    binsX = b_st, binsY =  b_st, mode = 2, xtitle = '#simType(#mu_{1})', ytitle = 'simType(#mu_{2})', 
                    cut = two_fakes + '  &  !' + twoFakes_sameVtx, log=True)

        h, c = plot(tupel = tupel, var = 'l2_simType : l1_simType', name = 'simType_sameVtx',
                    binsX = b_st, binsY =  b_st, mode = 2, xtitle = '#simType(#mu_{1})', ytitle = 'simType(#mu_{2})', 
                    cut = two_fakes + '  &  ' + twoFakes_sameVtx, log=True)

        h, c = plot(tupel = tupel, var = Delta_R_l12 + ' : l2_simProdZ - l1_simProdZ', name = 'dZ_dR_sameVtxJet',
                    binsX = b_z, binsY =  b_dR, mode = 2, xtitle = '#DeltaZ(#mu_{1}, #mu_{2}) [cm]', ytitle = '#DeltaR(#mu_{1}, #mu_{2})', 
                    cut = twoFakes_sameVtxJet, log=True)

        h, c = plot(tupel = tupel, var = Delta_R_l12 + ' : l2_simProdZ - l1_simProdZ', name = 'dZ_dR_sameVtxdiffJet',
                    binsX = b_z, binsY =  b_dR, mode = 2, xtitle = '#DeltaZ(#mu_{1}, #mu_{2}) [cm]', ytitle = '#DeltaR(#mu_{1}, #mu_{2})', 
                    cut = twoFakes_sameVtx + ' & !' + sameJet, log=True)


        h, c = plot(tupel = tupel, var = Delta_R_l12, name = 'dR_sameVtxJet', binsX = b_dR, xtitle = '#DeltaR(#mu_{1}, #mu_{2})', cut = twoFakes_sameVtxJet + ' & hnl_2d_disp > 0.5', log=True)

        h, c = plot(tupel = tupel, var = Delta_R_l12, name = 'dR_sameVtxdiffJet', binsX = b_dR, xtitle = '#DeltaR(#mu_{1}, #mu_{2})', cut = twoFakes_sameVtx + '& !' + sameJet + ' & hnl_2d_disp > 0.5', log=True)

        h, c = plot(tupel = tupel, var = Delta_R_l12 + ' : l2_simProdZ - l1_simProdZ', name = 'dZ_dR_diffVtx',
                    binsX = b_z, binsY =  b_dR, mode = 2, xtitle = '#DeltaZ(#mu_{1}, #mu_{2}) [cm]', ytitle = '#DeltaR(#mu_{1}, #mu_{2})', 
                    cut = two_fakes + ' & !' + sameVtx + ' & hnl_2d_disp > 0.5', log=True)


        h, c = plot(tupel = tupel, var = 'abs(l2_simProdZ - l1_simProdZ)', name = 'dZ_sameJet', binsX = b_abs_z,
                    xtitle = '|#DeltaZ(#mu_{1}, #mu_{2})| [cm]', cut = twoFakes_sameJet + ' & hnl_2d_disp > 0.5', log=True)

        h, c = plot(tupel = tupel, var = 'abs(l2_simProdRho - l1_simProdRho)', name = 'dRho_sameJet', binsX = b_rho_crs, 
                    xtitle = '|#Delta#rho(#mu_{1}, #mu_{2})| [cm]', cut = twoFakes_sameJet + ' & hnl_2d_disp > 0.5', log=True)

        h, c = plot(tupel = tupel, var = 'abs(l2_simProdRho - l1_simProdRho) : abs(l2_simProdZ - l1_simProdZ)', name = 'dZ_dRho_sameJet',
                    binsX = b_abs_z, binsY =  b_rho_crs, mode = 2, xtitle = '|#DeltaZ(#mu_{1}, #mu_{2})| [cm]', ytitle = '|#Delta#rho(#mu_{1}, #mu_{2})| [cm]', 
                    cut = twoFakes_sameJet + ' & hnl_2d_disp > 0.5', log=True)


        h, c = plot(tupel = tupel, var = 'l2_simProdRho : l1_simProdRho', name = 'Rho_Rho_sameJet', cut = twoFakes_sameJet + ' & hnl_2d_disp > 0.5',
                    binsX = b_rho_crs, binsY =  b_rho_crs, mode = 2, xtitle = '#rho(#mu_{1}) [cm]', ytitle = '#rho(#mu_{2}) [cm]', log=True) 

        h, c = plot(tupel = tupel, var = 'l2_simProdZ : l1_simProdZ', name = 'Z_Z_sameJet', binsX = b_z, binsY = b_z, mode = 2,
                    xtitle = 'Z(#mu_{1}) [cm]', ytitle = 'Z(#mu_{2}) [cm]', cut = twoFakes_sameJet + ' & hnl_2d_disp > 0.5', log=True)
####################################################################################################
   
####################################################################################################
def checkpTCone(eta_bin):
    eta, eta_cut = eta_bin
    tupels = [[TT_dir_m, ['1', '1']], [TT_dir_m, ['disp0p5', 'hnl_2d_disp > 0.5']], [DY50_dir_m, ['1','1']], [W_dir_m, ['1','1']],]
    tupels = [tupels[0]]
    h_ptcone_jetpt_sj_Iso = []; c_ptcone_jetpt_sj_Nso = []; i = 0
    for tupel in tupels: 
        iso_cut = 0.15
        sample_dir, cutuple = tupel
        cut_name = cutuple[0]
        cuts = cutuple[1]
        iso_str = str(int(iso_cut * 100))
    #    iso_str += '_stf=3'
        ch = basename(split(normpath(sample_dir))[0]) 
        sample_name = basename(normpath(sample_dir))
        fin = rt.TFile(inDir + sample_dir + suffix)
        t = fin.Get('tree')

        b_pt  = np.arange(5.,100,5)
        b_dR  = np.arange(0.,0.5,0.025)

        h, c = plot(tupel = tupel, 
                    name = 'ptJet_ptCone_sameJet_NoIso', 
                    var = ptCone2F_dimu(0.15) + ': l1_jet_pt', #ptCone2F(iso_cut) + ': l1_jet_pt',
                    binsX = b_pt, binsY =  b_pt, mode = 2, iso = 0.15, 
                    xtitle = '#mu_{1} Jet p_{T} [GeV]', 
                    ytitle = 'p_{T}^{Cone} [GeV]', 
                    cut = twoFakes_sameJet + LepIDIsoFail(1, 't', iso_cut) + LepIDIsoFail(2, 't', iso_cut) + twoLepObjIsoleq1)

        h, c = plot(tupel = tupel, 
                    name = 'ptJet_ptCone_sameJet_Iso', 
                    var = ptCone2F_dimu(0.15) + ': l1_jet_pt', #ptCone2F(iso_cut) + ': l1_jet_pt',
                    binsX = b_pt, binsY =  b_pt, mode = 2, iso = 0.15, 
                    xtitle = '#mu_{1} Jet p_{T} [GeV]', 
                    ytitle = 'p_{T}^{Cone} [GeV]', 
                    cut = twoFakes_sameJet + LepIDIsoPass(1, 't', iso_cut) + LepIDIsoPass(2, 't', iso_cut))

        h, c = plot(tupel = tupel, 
                    name = 'dR_pt_NoIso', 
                    var = 'hnl_dr_12 : hnl_hn_vis_pt', 
                    binsX = b_pt, binsY =  b_dR, mode = 2, iso = 0.15, 
                    xtitle = 'DiMuon p_{T} [GeV]', 
                    ytitle = '#DeltaR (#mu_{1}, #mu_{2})', 
                    cut = '1' + LepIDIsoFail(1, 't', iso_cut) + LepIDIsoFail(2, 't', iso_cut) + twoLepObjIsoleq1 + ' & hnl_2d_disp > 0.5') # + ' & ' + twoFakes_sameJet)

        h, c = plot(tupel = tupel, 
                    name = 'dR_pt_Iso', 
                    var = 'hnl_dr_12 : hnl_hn_vis_pt', 
                    binsX = b_pt, binsY =  b_dR, mode = 2, iso = 0.15,
                    xtitle = 'DiMuon p_{T} [GeV]', 
                    ytitle = '#DeltaR (#mu_{1}, #mu_{2})', 
                    cut = '1' + LepIDIsoPass(1, 't', iso_cut) + LepIDIsoPass(2, 't', iso_cut) + ' & hnl_2d_disp > 0.5') # + ' & ' + twoFakes_sameJet)
####################################################################################################
   
####################################################################################################
def applyTTL_old(isData=False):
    iso_cut = 0.15
    iso_str = str(int(iso_cut * 100))

    if isData == False:
        fin = rt.TFile(inDir + TT_dir_m + suffix)
        t = fin.Get('tree')

    if isData == True:
        t = rt.TChain('tree')
        t.Add(inDir + data_m_B + suffix)
        t.Add(inDir + data_m_C + suffix)
        t.Add(inDir + data_m_D + suffix)
        t.Add(inDir + data_m_E + suffix)
        t.Add(inDir + data_m_F + suffix)

    ## get FR(eta, pt)
    fin_tt = rt.TFile(plotDir + 'TTL_partial_ptCone_eta_iso15_eta.root')
    c_tt = fin_tt.Get('ptCone_eta')
    h_tt = c_tt.GetPrimitive('pt_cone_eta_n')

    fin_data = rt.TFile(plotDir + 'TTL_data_prompt_m_ptCone_eta_iso15.root')
    c_data = fin_data.Get('ptCone_eta')
    h_data = c_data.GetPrimitive('pt_cone_eta_n')
 
    weight_tt = np.zeros((3,8))
    weight_data = np.zeros((3,8))

    for ieta in range(3):
        for ipt in range(8):
            weight_tt[ieta][ipt]   = (  h_tt.GetBinContent(ipt + 1,ieta + 1)  / ( 1 - h_tt.GetBinContent(ipt + 1,ieta + 1)   ) )
            weight_data[ieta][ipt] = ( h_data.GetBinContent(ipt + 1,ieta + 1) / ( 1 - h_data.GetBinContent(ipt + 1,ieta + 1) ) )

    print weight_tt, '\n'

    print weight_data

    b_M = np.arange(0.,200,2)

    weighed_pt        = rt.TH1F('weighed_pt',     'weighed_pt',     len(b_pt)-1, b_pt)
    weighed_2disp     = rt.TH1F('weighed_2disp',  'weighed_2disp',  len(b_2d)-1, b_2d)
    weighed_m_dimu    = rt.TH1F('weighed_m_dimu', 'weighed_m_dimu', len(b_m)-1, b_m)
    weighed_m_triL    = rt.TH1F('weighed_m_triL', 'weighed_m_triL', len(b_M)-1, b_M)
    observed_pt       = rt.TH1F('obs_pt',         'obs_pt',         len(b_pt)-1, b_pt)
    observed_2disp    = rt.TH1F('obs_2disp',      'obs_2disp',      len(b_2d)-1, b_2d)
    observed_m_dimu   = rt.TH1F('obs_m_dimu',     'obs_m_dimu',     len(b_m)-1, b_m)
    observed_m_triL   = rt.TH1F('obs_m_triL',     'obs_m_triL',     len(b_M)-1, b_M)

    print 'drawing observed ...'
#    print 'cut: ', twoFakes_sameJet + LepIDIsoPass(1, 't', iso_cut) + LepIDIsoPass(2, 't', iso_cut)
##   t.Draw( 'hnl_hn_vis_pt >> obs_pt', twoFakes_sameJet + LepIDIsoPass(1, 't', iso_cut) + LepIDIsoPass(2, 't', iso_cut))
    t.Draw( 'hnl_hn_vis_pt >> obs_pt', 
    'abs(l1_jet_pt - l2_jet_pt) < 1 & hnl_w_vis_m > 80 & nbj == 0 & hnl_2d_disp > 0.5 ' + LepIDIsoPass(0, 't', iso_cut) + LepIDIsoPass(1, 't', iso_cut) + LepIDIsoPass(2, 't', iso_cut) ) # DATA !
    print 'pt done'
##   t.Draw( 'hnl_2d_disp >> obs_2disp', twoFakes_sameJet + LepIDIsoPass(1, 't', iso_cut) + LepIDIsoPass(2, 't', iso_cut))
    t.Draw( 'hnl_2d_disp >> obs_2disp', 
    'abs(l1_jet_pt - l2_jet_pt) < 1 & hnl_w_vis_m > 80 & nbj == 0 & hnl_2d_disp > 0.5 ' + LepIDIsoPass(0, 't', iso_cut) + LepIDIsoPass(1, 't', iso_cut) + LepIDIsoPass(2, 't', iso_cut) ) # DATA !
    print '2disp done'
##   t.Draw( 'hnl_m_12 >> obs_m_dimu', twoFakes_sameJet + LepIDIsoPass(1, 't', iso_cut) + LepIDIsoPass(2, 't', iso_cut))
    t.Draw( 'hnl_m_12 >> obs_m_dimu', 
    'abs(l1_jet_pt - l2_jet_pt) < 1 & hnl_w_vis_m > 80 & nbj == 0 & hnl_2d_disp > 0.5 ' + LepIDIsoPass(0, 't', iso_cut) + LepIDIsoPass(1, 't', iso_cut) + LepIDIsoPass(2, 't', iso_cut) ) # DATA !
    print 'dimu mass done'

    t.Draw( 'hnl_w_vis_m >> obs_m_triL', 
    'abs(l1_jet_pt - l2_jet_pt) < 1 & hnl_w_vis_m > 80 & nbj == 0 & hnl_2d_disp > 0.5 ' + LepIDIsoPass(0, 't', iso_cut) + LepIDIsoPass(1, 't', iso_cut) + LepIDIsoPass(2, 't', iso_cut) ) # DATA !
    print 'tri lep mass done'
    print 'drawing observed done'

    for ieta in range(3):
        for ipt in range(8):
            print 'ipt =', ipt, ' ieta = ', ieta
            print ptEtaBin(ipt,ieta)
            t.Draw( ptCone2F_dimu(iso_cut) + ' >>+ weighed_pt',
##           '( ' + twoFakes_sameJet + LepIDIsoFail(1, 't', iso_cut) + LepIDIsoFail(2, 't', iso_cut) + ptEtaBin(ipt,ieta) + twoLepObjIsoleq1 + ') * %f'%weight_tt[ieta][ipt])
            '( abs(l1_jet_pt - l2_jet_pt) < 1 & hnl_w_vis_m > 80 & nbj == 0 & hnl_2d_disp > 0.5 ' + LepIDIsoPass(0, 't', iso_cut) + LepIDIsoFail(1, 't', iso_cut) + LepIDIsoFail(2, 't', iso_cut) + ptEtaBin(ipt,ieta) + twoLepObjIsoleq1 + ') * %f'%weight_data[ieta][ipt]) # DATA!

            t.Draw( 'hnl_2d_disp >>+ weighed_2disp',
##           '( ' + twoFakes_sameJet + LepIDIsoFail(1, 't', iso_cut) + LepIDIsoFail(2, 't', iso_cut) + ptEtaBin(ipt,ieta) + twoLepObjIsoleq1 + ') * %f'%weight_tt[ieta][ipt])
            '( abs(l1_jet_pt - l2_jet_pt) < 1 & hnl_w_vis_m > 80 & nbj == 0 & hnl_2d_disp > 0.5 ' + LepIDIsoPass(0, 't', iso_cut) + LepIDIsoFail(1, 't', iso_cut) + LepIDIsoFail(2, 't', iso_cut) + ptEtaBin(ipt,ieta) + twoLepObjIsoleq1 + ') * %f'%weight_data[ieta][ipt]) # DATA!

            t.Draw( 'hnl_m_12  >>+ weighed_m_dimu',
##           '( ' + twoFakes_sameJet + LepIDIsoFail(1, 't', iso_cut) + LepIDIsoFail(2, 't', iso_cut) + ptEtaBin(ipt,ieta) + twoLepObjIsoleq1 + ') * %f'%weight_tt[ieta][ipt])
            '( abs(l1_jet_pt - l2_jet_pt) < 1 & hnl_w_vis_m > 80 & nbj == 0 & hnl_2d_disp > 0.5 ' + LepIDIsoPass(0, 't', iso_cut) + LepIDIsoFail(1, 't', iso_cut) + LepIDIsoFail(2, 't', iso_cut) + ptEtaBin(ipt,ieta) + twoLepObjIsoleq1 + ') * %f'%weight_data[ieta][ipt]) # DATA!

            t.Draw( 'hnl_w_vis_m  >>+ weighed_m_triL',
            '( abs(l1_jet_pt - l2_jet_pt) < 1 & hnl_w_vis_m > 80 & nbj == 0 & hnl_2d_disp > 0.5 ' + LepIDIsoPass(0, 't', iso_cut) + LepIDIsoFail(1, 't', iso_cut) + LepIDIsoFail(2, 't', iso_cut) + ptEtaBin(ipt,ieta) + twoLepObjIsoleq1 + ') * %f'%weight_data[ieta][ipt]) # DATA!

    c_pt = rt.TCanvas('pt', 'pt')
    weighed_pt.SetMarkerColor(rt.kGreen+2)
    weighed_pt.SetTitle('; p_{T}^{Cone} [GeV]; Counts')
    observed_pt.SetTitle('; p_{T}^{Cone} [GeV]; Counts')
    observed_pt.SetMarkerColor(rt.kMagenta+2)
    weighed_pt.Draw()
    observed_pt.Draw('same')
    leg = rt.TLegend(0.57, 0.78, 0.80, 0.9)
    leg.AddEntry(observed_pt, 'observed')
    leg.AddEntry(weighed_pt, 'expected')
    leg.Draw()
    pf.showlogoprelimsim('CMS')
    save(c_pt, iso_cut, 'check', '', '')

    c_2disp = rt.TCanvas('2disp', '2disp')
    weighed_2disp.SetMarkerColor(rt.kGreen+2)
    weighed_2disp.SetTitle(';2D displacement [cm]; Counts')
    observed_2disp.SetTitle(';2D displacement [cm]; Counts')
    observed_2disp.SetMarkerColor(rt.kMagenta+2)
    weighed_2disp.Draw()
    observed_2disp.Draw('same')
    leg = rt.TLegend(0.57, 0.78, 0.80, 0.9)
    leg.AddEntry(observed_2disp, 'observed')
    leg.AddEntry(weighed_2disp, 'expected')
    leg.Draw()
    pf.showlogoprelimsim('CMS')
    save(c_2disp, iso_cut, 'check', '', '')

    c_mass = rt.TCanvas('mass', 'mass')
    weighed_m_dimu.SetMarkerColor(rt.kGreen+2)
    weighed_m_dimu.SetTitle('; m(#mu_{1},  #mu_{2}); Counts')
    observed_m_dimu.SetTitle('; m(#mu_{1},  #mu_{2}); Counts')
    observed_m_dimu.SetMarkerColor(rt.kMagenta+2)
    weighed_m_dimu.Draw()
    observed_m_dimu.Draw('same')
    leg = rt.TLegend(0.57, 0.78, 0.80, 0.9)
    leg.AddEntry(observed_m_dimu, 'observed')
    leg.AddEntry(weighed_m_dimu, 'expected')
    leg.Draw()
    pf.showlogoprelimsim('CMS')
    save(c_mass, iso_cut, 'check', '', '')

    c_3l_mass = rt.TCanvas('3l_mass', '3l_mass')
    weighed_m_triL.SetMarkerColor(rt.kGreen+2)
    weighed_m_triL.SetTitle('; m(#mu_{0}, #mu_{1},  #mu_{2}); Counts')
    observed_m_triL.SetTitle('; m(#mu_{0}, #mu_{1},  #mu_{2}); Counts')
    observed_m_triL.SetMarkerColor(rt.kMagenta+2)
    weighed_m_triL.Draw()
    observed_m_triL.Draw('same')
    leg = rt.TLegend(0.57, 0.78, 0.80, 0.9)
    leg.AddEntry(observed_m_triL, 'observed')
    leg.AddEntry(weighed_m_triL, 'expected')
    leg.Draw()
    pf.showlogoprelimsim('CMS')
    save(c_3l_mass, iso_cut, 'check', '', '')
####################################################################################################
   
####################################################################################################
def applyTTL(isData=False, VLD=True):
    iso_cut = 0.15
    iso_str = str(int(iso_cut * 100))
    ch = 'mu'
    sample = 'data'
    if isData == False:
#        fin = rt.TFile(treeDir + 'tree_fr_liteTTbar.root') #TODO CHANGE TO FULL
#        fin = rt.TFile(tempDir + 'tree_fr_DR_TTbar.root') 
#        t = fin.Get('tree')
        t = rt.TChain('tree')
        all_files = glob(tempDir + 'tree_fr_DR_TTbar_slice*.root')
        for sample in all_files:
            t.Add(sample)
        sample = 'TTbar'
        cut_T     = twoFakes_sameJet_new + ' & hnl_2d_disp > 0.5 & abs(l1_dz) < 2 & abs(l2_dz) < 2' + TIGHT 
#        cut_T     += LepIDIsoPass(0, 't', iso_cut) + LepIDIsoPass(1, 'l', iso_cut) + LepIDIsoPass(2, 'l', iso_cut)
        cut_L   = twoFakes_sameJet_new + ' & hnl_2d_disp > 0.5 & abs(l1_dz) < 2 & abs(l2_dz) < 2' + LOOSE
#        cut_L  += LepIDIsoPass(0, 't', iso_cut) + LepIDIsoFail(1, 'l', iso_cut) + LepIDIsoFail(2, 'l', iso_cut) + twoLepObjIsoleq1
#        cut_L  += LepIDIsoPass(0, 't', iso_cut) + bothLoose(iso_cut) + twoLepObjIsoleq1
        cut_LNT = twoFakes_sameJet_new + ' & hnl_2d_disp > 0.5 & abs(l1_dz) < 2 & abs(l2_dz) < 2' + LOOSENOTTIGHT

    if isData == True:
        fin = rt.TFile(treeDir + 'tree_fr_DR_data_v2.root') #TODO CHANGE TO FULL
        t = fin.Get('tree')
#        t = rt.TChain('tree')
#        all_files = glob(tempDir + 'tree_fr_DR_data_slice*.root')
#        for sample in all_files:
#            t.Add(sample)
#            print sample, t.GetEntries()
        cut_T_APL   = 'abs(l1_jet_pt - l2_jet_pt) < 1 & hnl_dr_12 < 0.8 & hnl_w_vis_m > 80 & nbj == 0 & hnl_2d_disp > 0.5 & abs(l1_dz) < 2 & abs(l2_dz) < 2' + TIGHT
        cut_L_APL   = 'abs(l1_jet_pt - l2_jet_pt) < 1 & hnl_dr_12 < 0.8 & hnl_w_vis_m > 80 & nbj == 0 & hnl_2d_disp > 0.5 & abs(l1_dz) < 2 & abs(l2_dz) < 2' + LOOSE
        cut_LNT_APL = 'abs(l1_jet_pt - l2_jet_pt) < 1 & hnl_dr_12 < 0.8 & hnl_w_vis_m > 80 & nbj == 0 & hnl_2d_disp > 0.5 & abs(l1_dz) < 2 & abs(l2_dz) < 2' + LOOSENOTTIGHT

        ### VALIDATION ###
        cut_T_VLD   = 'abs(l1_jet_pt - l2_jet_pt) < 1 & hnl_dr_12 < 0.8 & nbj > 0 & hnl_2d_disp > 0.5 & abs(l1_dz) < 2 & abs(l2_dz) < 2' + TIGHT 
        cut_L_VLD   = 'abs(l1_jet_pt - l2_jet_pt) < 1 & hnl_dr_12 < 0.8 & nbj > 0 & hnl_2d_disp > 0.5 & abs(l1_dz) < 2 & abs(l2_dz) < 2' + LOOSE 
        cut_LNT_VLD = 'abs(l1_jet_pt - l2_jet_pt) < 1 & hnl_dr_12 < 0.8 & nbj > 0 & hnl_2d_disp > 0.5 & abs(l1_dz) < 2 & abs(l2_dz) < 2' + LOOSENOTTIGHT
 
    ### VALIDATE
    if VLD == True:
        cut_T   = cut_T_VLD
        cut_LNT = cut_LNT_VLD

    ### APPLY
    if VLD == False:
        cut_T   = cut_T_APL
        cut_LNT = cut_LNT_APL

    print '\n\tcut T:', cut_T, '\n\tcut LNT:', cut_LNT

    weighed_pt        = rt.TH1F('weighed_pt',     'weighed_pt',     len(b_pt)-1, b_pt)
    weighed_2disp     = rt.TH1F('weighed_2disp',  'weighed_2disp',  len(b_2d)-1, b_2d)
    weighed_m_dimu    = rt.TH1F('weighed_m_dimu', 'weighed_m_dimu', len(b_m)-1, b_m)
    weighed_M_dimu    = rt.TH1F('weighed_M_dimu', 'weighed_M_dimu', len(b_M)-1, b_M)
    weighed_m_triL    = rt.TH1F('weighed_m_triL', 'weighed_m_triL', len(b_M)-1, b_M)
    observed_pt       = rt.TH1F('obs_pt',         'obs_pt',         len(b_pt)-1, b_pt)
    observed_2disp    = rt.TH1F('obs_2disp',      'obs_2disp',      len(b_2d)-1, b_2d)
    observed_m_dimu   = rt.TH1F('obs_m_dimu',     'obs_m_dimu',     len(b_m)-1, b_m)
    observed_M_dimu   = rt.TH1F('obs_M_dimu',     'obs_M_dimu',     len(b_M)-1, b_M)
    observed_m_triL   = rt.TH1F('obs_m_triL',     'obs_m_triL',     len(b_M)-1, b_M)

    print '\n\tentries:', t.GetEntriesFast()

    print '\n\tdrawing pt ...'

    t.Draw( 'hnl_hn_vis_pt >> obs_pt', cut_T ) 
    print '\tobs pt done'

    t.Draw( ptCone2F_dimu(iso_cut) + '>> weighed_pt',  '( ' + cut_LNT + ' ) * ( weight_fr/ (1 - weight_fr) )' )
    print '\tweighed pt done'

    c_pt = rt.TCanvas('pt', 'pt')
    weighed_pt.SetMarkerColor(rt.kGreen+2)
    weighed_pt.SetTitle('; p_{T}^{Cone} [GeV]; Counts')
    observed_pt.SetTitle('; p_{T}^{Cone} [GeV]; Counts')
    observed_pt.SetMarkerColor(rt.kMagenta+2)
    weighed_pt.Draw('hist')
    observed_pt.Draw('same')
    leg = rt.TLegend(0.57, 0.78, 0.80, 0.9)
    leg.AddEntry(observed_pt, 'observed')
    leg.AddEntry(weighed_pt, 'expected')
    leg.Draw()
    pf.showlogoprelimsim('CMS')
    save(c_pt, iso_cut, 'DDE_' + sample, ch, '')

    print '\tdrawing 2disp ...'

    t.Draw( 'hnl_2d_disp >> obs_2disp', cut_T )   
    print '\tobs 2disp done'

    t.Draw( 'hnl_2d_disp >> weighed_2disp',            '( ' + cut_LNT + ' ) * ( weight_fr/ (1 - weight_fr) )' )
    print '\tweighed 2disp done'

    c_2disp = rt.TCanvas('2disp', '2disp')
    weighed_2disp.SetMarkerColor(rt.kGreen+2)
    weighed_2disp.SetTitle(';2D displacement [cm]; Counts')
    observed_2disp.SetTitle(';2D displacement [cm]; Counts')
    observed_2disp.SetMarkerColor(rt.kMagenta+2)
    weighed_2disp.Draw('hist')
    observed_2disp.Draw('same')
    leg = rt.TLegend(0.57, 0.78, 0.80, 0.9)
    leg.AddEntry(observed_2disp, 'observed')
    leg.AddEntry(weighed_2disp, 'expected')
    leg.Draw()
    pf.showlogoprelimsim('CMS')
    save(c_2disp, iso_cut, 'DDE_' + sample, ch, '')

    print '\tdrawing dimu mass ...'

    t.Draw( 'hnl_m_12 >> obs_m_dimu', cut_T )  
    print '\tobs dimu mass done'

    t.Draw( 'hnl_m_12  >> weighed_m_dimu',             '( ' + cut_LNT + ' ) * ( weight_fr/ (1 - weight_fr) )' )
    print '\tweighed dimu mass done'

    c_mass = rt.TCanvas('mass', 'mass')
    weighed_m_dimu.SetMarkerColor(rt.kGreen+2)
    weighed_m_dimu.SetTitle('; m(#mu_{1},  #mu_{2}); Counts')
    observed_m_dimu.SetTitle('; m(#mu_{1},  #mu_{2}); Counts')
    observed_m_dimu.SetMarkerColor(rt.kMagenta+2)
    weighed_m_dimu.Draw('hist')
    observed_m_dimu.Draw('same')
    leg = rt.TLegend(0.57, 0.78, 0.80, 0.9)
    leg.AddEntry(observed_m_dimu, 'observed')
    leg.AddEntry(weighed_m_dimu, 'expected')
    leg.Draw()
    pf.showlogoprelimsim('CMS')
    save(c_mass, iso_cut, 'DDE_' + sample, ch, '')

    print '\tdrawing dimu mass_high ...'

    t.Draw( 'hnl_m_12 >> obs_M_dimu', cut_T )  
    print '\tobs dimu mass_high done'

    t.Draw( 'hnl_m_12  >> weighed_M_dimu',             '( ' + cut_LNT + ' ) * ( weight_fr/ (1 - weight_fr) )' )
    print '\tweighed dimu mass_high done'

    c_mass_high = rt.TCanvas('mass_high', 'mass_high')
    weighed_M_dimu.SetMarkerColor(rt.kGreen+2)
    weighed_M_dimu.SetTitle('; m(#mu_{1},  #mu_{2}); Counts')
    observed_M_dimu.SetTitle('; m(#mu_{1},  #mu_{2}); Counts')
    observed_M_dimu.SetMarkerColor(rt.kMagenta+2)
    weighed_M_dimu.Draw('hist')
    observed_M_dimu.Draw('same')
    leg = rt.TLegend(0.57, 0.78, 0.80, 0.9)
    leg.AddEntry(observed_M_dimu, 'observed')
    leg.AddEntry(weighed_M_dimu, 'expected')
    leg.Draw()
    pf.showlogoprelimsim('CMS')
    save(c_mass_high, iso_cut, 'DDE_' + sample, ch, '')

    print '\tdrawing tri lep mass ...'

    t.Draw( 'hnl_w_vis_m >> obs_m_triL', cut_T )  
    print '\tobs tri lep mass done'

    t.Draw( 'hnl_w_vis_m >> weighed_m_triL',           '( ' + cut_LNT + ' ) * ( weight_fr/ (1 - weight_fr) )' )
    print '\tweighed tri lep mass done'

    c_3l_mass = rt.TCanvas('3l_mass', '3l_mass')
    weighed_m_triL.SetMarkerColor(rt.kGreen+2)
    weighed_m_triL.SetTitle('; m(#mu_{0}, #mu_{1},  #mu_{2}); Counts')
    observed_m_triL.SetTitle('; m(#mu_{0}, #mu_{1},  #mu_{2}); Counts')
    observed_m_triL.SetMarkerColor(rt.kMagenta+2)
    weighed_m_triL.Draw('hist')
    observed_m_triL.Draw('same')
    leg = rt.TLegend(0.57, 0.78, 0.80, 0.9)
    leg.AddEntry(observed_m_triL, 'observed')
    leg.AddEntry(weighed_m_triL, 'expected')
    leg.Draw()
    pf.showlogoprelimsim('CMS')
    save(c_3l_mass, iso_cut, 'DDE_' + sample, ch, '')

def ptEtaBin(ipt, ieta):
    iso_cut = 0.15
    ptlow = b_pt[ipt]; pthigh = b_pt[ipt+1]
    etalow = b_eta[ieta]; etahigh = b_eta[ieta+1]
    cut = ' & {ptcone} < {pthi} & {ptcone} > {ptlo} & {eta} < {etahi} & {eta} > {etalo}'.format( ptcone = ptCone2F_dimu(iso_cut), ptlo = ptlow, pthi = pthigh, eta = 'abs(hnl_hn_vis_eta)', etahi=etahigh, etalo = etalow)
    return cut


#print '\n'
#pool = Pool(processes=len(isolst))
#print('number of processes (ie. samples): %i'%len(isolst))
#pool.map(checkTTLratio, isolst)

#print '\n'
#pool = Pool(processes=len(eta_bins))
#print('number of processes (ie. samples): %i'%len(eta_bins))
#pool.map(checkTTLratio, eta_bins)
#checkTTLratio(['0-to-2.4', l0_prompt])

#print '\n'
#TTbarStudy()

#print '\n'
#pool = Pool(processes=len(mltlst))
#print('number of processes (ie. samples): %i'%len(mltlst))
#pool.map(countFakes, mltlst) 
#countFakes([TT_dir_m          , ['disp0p5', 'hnl_2d_disp > 0.5']])
#countFakes([TT_dir_m          , ['disp0p5_pt15', 'hnl_2d_disp > 0.5 & l1_pt > 15 & l2_pt > 15']])
####################################################################################################
def th1(name, bins, xtitle=''):
    h = rt.TH1F('h_%s'%name, name, len(bins)-1, bins)
#    h.name = name
    h.SetTitle('%s; %s; Counts'%(name, xtitle))
    return h

def th2(name, binsX, binsY, xtitle='', ytitle=''):
    h = rt.TH2F('h_%s'%name, name, len(binsX)-1, binsX, len(binsY)-1, binsY)
    h.SetTitle('%s; %s; %s'%(name, xtitle, ytitle))
    return h

def fill(tree, hist, var, cut='', opt=''):
    tree, hist, var, cut, opt
#    tree.Draw('{v} >> h_{h}'.format( v=var, h=hist.GetName() ), cut, opt)
    tree.Draw('{v} >> {h}'.format( v=var, h=hist.GetName() ), cut, opt)
    print '\tvar: {v} \n\tcut: {c}'.format(v=var, c=cut)
    print 'entries: ', hist.GetEntries()
    return hist

def save(knvs, iso, sample='', ch='', eta=''):
    iso_str = str(int(iso * 100))
    knvs.Modified(); knvs.Update()
    if len(eta):
        knvs.SaveAs('{dr}{smpl}_{ch}_{ttl}_iso{iso}_eta{eta}.png' .format(dr=plotDir, smpl=sample, ttl=knvs.GetTitle(), ch=ch, iso=iso_str, eta=eta))
        knvs.SaveAs('{dr}{smpl}_{ch}_{ttl}_iso{iso}_eta{eta}.pdf' .format(dr=plotDir, smpl=sample, ttl=knvs.GetTitle(), ch=ch, iso=iso_str, eta=eta))
        knvs.SaveAs('{dr}{smpl}_{ch}_{ttl}_iso{iso}_eta{eta}.root'.format(dr=plotDir, smpl=sample, ttl=knvs.GetTitle(), ch=ch, iso=iso_str, eta=eta))
    else:
        knvs.SaveAs('{dr}{smpl}_{ch}_{ttl}_iso{iso}.png' .format(dr=plotDir, smpl=sample, ttl=knvs.GetTitle(), ch=ch, iso=iso_str))
        knvs.SaveAs('{dr}{smpl}_{ch}_{ttl}_iso{iso}.pdf' .format(dr=plotDir, smpl=sample, ttl=knvs.GetTitle(), ch=ch, iso=iso_str))
        knvs.SaveAs('{dr}{smpl}_{ch}_{ttl}_iso{iso}.root'.format(dr=plotDir, smpl=sample, ttl=knvs.GetTitle(), ch=ch, iso=iso_str))
    
def draw(hist, mode=1, log=False):
    c = rt.TCanvas(hist.GetName(), hist.GetName())
    if mode == 2:
        hist.Draw('colz') 
        if log == True: c.SetLogz()
    if mode == 1:
        hist.Draw('ep') 
        if log == True: c.SetLogy()
    if mode == 'eff':
        framer.Draw()
        hist.Draw('same')
    pf.showlogoprelimsim('CMS')
    # pf.showTitle('iso_cut = 0.%s'%iso_str)
    pf.showTitle(hist.GetName())
    c.Modified; c.Update()
    return c

def plot(tupel, name, var, binsX, binsY=[], xtitle='', ytitle='', mode=1, cut='', log=False, opt='', iso=0.15, eta_bin=['full', '']):
    sample_dir, cutuple = tupel
    eta = eta_bin[0]
    eta_cut = eta_bin[1]
    cut_name = cutuple[0]
    fin = rt.TFile(inDir + sample_dir + suffix)
    t = fin.Get('tree')

    if len(cutuple[1]) > 3: cut += ' & ' + cutuple[1]
    if len(eta_cut) > 3:    cut += ' & ' + eta_cut
    ch     = basename(split(normpath(sample_dir))[0]) 
    sample = basename(normpath(sample_dir))
    if mode == 1: 
        hist = th1(name, binsX, xtitle)
    if mode == 2: 
        hist = th2(name, binsX, binsY, xtitle, ytitle)
    if mode == 'eff':
        numer = th1('%s_n'%name, binsX, xtitle)
        denom = th1('%s_d'%name, binsX, xtitle)
        # TODO finish this mode

    print '\nsample name: {s}_{ch}, entries: {n}'.format(s=sample, ch=ch, n=t.GetEntries())
    print '\tfilling hist: {h}'.format(h=hist.GetName())
    filled_hist = fill(t, hist, var, cut, opt)
    print '\thist: {h} entries: {n}\n'.format(h=hist.GetName(), n=filled_hist.GetEntries())
    c = draw(filled_hist, mode, log)
    save(c, iso, sample, ch, eta)
    return filled_hist, c

#class weighedHist(object):

def fillWeighedHist(tupel):
#    tree, var, bins, ieta, ipt, isData = tupel
    tree, hist, ieta, ipt, isData = tupel
    histoasd = th1('tempasd_ipt%i_ieta%i'%(ipt,ieta), b_pt)
    print 'drawing th1: h_tempasd_ipt%i_ieta%i ...'%(ipt,ieta)
    iso_cut = 0.15
    if isData == True:
        cut = '( hnl_w_vis_m > 80 & nbj == 0 & hnl_2d_disp > 0.5 '
        cut += LepIDIsoPass(0, 't', iso_cut) + LepIDIsoFail(1, 't', iso_cut) + LepIDIsoFail(2, 't', iso_cut) + ptEtaBin(ipt,ieta) + twoLepObjIsoleq1 
        cut = '(' + cut + ') * %f'%weight_data[ieta][ipt]
    if isData == False:
        cut = '( ' + twoFakes_sameJet + LepIDIsoFail(1, 't', iso_cut) + LepIDIsoFail(2, 't', iso_cut) + ptEtaBin(ipt,ieta) + twoLepObjIsoleq1 + ') * %f'%weight_tt[ieta][ipt]
#    filled_hist = fill(tree, hist, var, cut)
    tree.Draw('{v} >> {h}'.format( v=var, h=histoasd.GetName() ), cut)
    print '\tvar: {v} \n\tcut: {c}'.format(v=var, c=cut)
    print 'entries: ', histoasd.GetEntries()
    print 'th1: h_temp_ipt%i_ieta%i... done'%(ipt,ieta)
    return histoasd

def makeCheckPlots(tree, var, bins, isData=False):
    print 'is data :', isData
    ieta = 0; ipt = 0
    h = th1('h', bins)
    histo = th1('temp_ipt%i_ieta%i'%(ipt,ieta), bins)
#    tupel = [tree, var, bins, ieta, ipt, isData]
    tupels = []
    for ieta in range(3):
        for ipt in range(8):
            #tupels.append(makeTupel(tree, var, bins, ieta, ipt, isData))
            tupels.append(makeTupel(tree, histo, ieta, ipt, isData))
    pool = Pool(processes=24)
    filled_hist = pool.map(fillWeighedHist, [tupels[3]]) 
#    for ih in h_result:
#        h.Add(ih)
#    hist = fillWeighedHist(tupels[3])

#def makeTupel(tree, var, bins, ieta, ipt, isData):
def makeTupel(tree, hist, ieta, ipt, isData):
#    tupel = [tree, var, bins, ieta, ipt, isData]
    tupel = [tree, hist, ieta, ipt, isData]
    return tupel

#    ## get FR(eta, pt)
#fin_tt = rt.TFile(plotDir + 'TTL_partial_ptCone_eta_iso15_eta.root')
#c_tt = fin_tt.Get('ptCone_eta')
#h_tt = c_tt.GetPrimitive('pt_cone_eta_n')
#
#fin_data = rt.TFile(plotDir + 'TTL_data_prompt_m_ptCone_eta_iso15.root')
#c_data = fin_data.Get('ptCone_eta')
#h_data = c_data.GetPrimitive('pt_cone_eta_n')
#
#weight_tt = np.zeros((3,8))
#weight_data = np.zeros((3,8))
#
#for ieta in range(3):
#    for ipt in range(8):
#        weight_tt[ieta][ipt]   = (  h_tt.GetBinContent(ipt + 1,ieta + 1)  / ( 1 - h_tt.GetBinContent(ipt + 1,ieta + 1)   ) )
#        weight_data[ieta][ipt] = ( h_data.GetBinContent(ipt + 1,ieta + 1) / ( 1 - h_data.GetBinContent(ipt + 1,ieta + 1) ) )

def addBranch(isData=False,START=0,STOP=1):

    sample = 'TTbar'
 
    if isData == True:  
        fin_data = rt.TFile(plotDir + 'FR_meshR/TTL_data_mu_ptCone_eta_iso15.root')
        c_data = fin_data.Get('ptCone_eta')
        h_data = c_data.GetPrimitive('pt_eta_T')
        h_fr = h_data
        tree = rt.TChain('tree')
        tree.Add(inDir + data_m_B + suffix)
        tree.Add(inDir + data_m_C + suffix)
        tree.Add(inDir + data_m_D + suffix)
        tree.Add(inDir + data_m_F + suffix)
        sample = 'data'

    if isData == False:
        fin_tt = rt.TFile(plotDir + 'FR_meshR/TTL_TTbar_mu_ptCone_eta_iso15.root')
        c_tt = fin_tt.Get('ptCone_eta')
        h_tt = c_tt.GetPrimitive('pt_eta_T')
        h_fr = h_tt
        fin = rt.TFile(inDir + TT_dir_m + suffix)
        tree = fin.Get('tree')

    nevents = tree.GetEntries()
    isocut = 0.15
    apop = 100000

    # convert into a numpy array
    frs = root_numpy.hist2array(h_fr)
    xbins = np.array([h_fr.GetXaxis().GetBinUpEdge(i) for i in range(h_fr.GetNbinsX()+1)])
    ybins = np.array([h_fr.GetYaxis().GetBinUpEdge(i) for i in range(h_fr.GetNbinsY()+1)])

    @np.vectorize
    def fakeRate(pt, eta): #, frs, xbins, ybins):
        ipt  = min(max(np.where(pt >=xbins)[0]), len(xbins)-2) # if overflow, just stick to the last bin
        ieta = min(max(np.where(eta>=ybins)[0]), len(ybins)-2)
        return frs[ipt][ieta]

#    def ds_iso(DS):
#        bewl = ( (DS.l1_id_l == 1) & (DS.l1_reliso_rho_04 < 0.15) & (DS.l2_id_l == 1) & (DS.l2_reliso_rho_04 < 0.15) )
#        return bewl
#    def ds_noniso(DS):
#        bewl = ( (DS.l1_id_l == 1) & (DS.l1_reliso_rho_04 > 0.15) | (DS.l2_id_l == 1) & (DS.l2_reliso_rho_04 > 0.15) )
#        return bewl

    # some validation
    # ipts  = np.linspace(0., 100., 20)
    # ietas = np.linspace(0., 3.  , 6 )
    # 
    # for ipt, ieta in product(ipts, ietas):
    #     print 'pt = %.1f \teta = %.1f \t\t fake rate = %.5f' %(ipt, ieta, fakeRate(ipt, ieta))
    # https://github.com/vinzenzstampf/PlotFactory/blob/master/DDE/countingFakes.py#L646-L677

    # proceed 200k events a pop
    nslices = int(nevents/apop) + 1
    print '\n\tnumber of slices:', nslices 
#    for islice in range(nslices-1):#[:3]:
    RANGE = range(nslices)
    if STOP > 2: RANGE = range(START,STOP)
    for islice in RANGE:#[:3]:
        
        start =  islice      * apop
        if (islice + 1) < nslices: stop = (islice + 1) * apop
        if (islice + 1) == nslices: stop = nevents
        
        print '\n\tloading dataset for slice', (islice + 1)
#        dataset = pandas.DataFrame(root_numpy.root2array(ifile, 'tree', start=start, stop=stop))
        dataset = pandas.DataFrame(root_numpy.tree2array(tree, start=start, stop=stop))
        dataset['aux_index'] = np.arange(start,stop)
        print '\tloading done'

        dataset_iso    = dataset.iloc[np.where(dataset.hnl_iso04_rel_rhoArea< isocut)[0], :]
        dataset_noniso = dataset.iloc[np.where(dataset.hnl_iso04_rel_rhoArea>=isocut)[0], :]
#        dataset_iso    = dataset.iloc[np.where(   ds_iso(dataset))[0], :]
#        dataset_noniso = dataset.iloc[np.where(ds_noniso(dataset))[0], :]

        dataset_iso   ['weight_fr'] = fakeRate(dataset_iso   .hnl_hn_vis_pt                                                       , np.abs(dataset_iso   .hnl_hn_vis_eta))
        dataset_noniso['weight_fr'] = fakeRate(dataset_noniso.hnl_hn_vis_pt * (1. + dataset_noniso.hnl_iso04_rel_rhoArea - isocut), np.abs(dataset_noniso.hnl_hn_vis_eta))

        frames = [dataset_iso, dataset_noniso]

        out_dataset = pandas.concat(frames)
        out_dataset.sort_values(['aux_index'], inplace=True)

        print '\tstaging out...'
        out_dataset.to_root(tempDir + 'tree_fr_DR_' + sample + '_slice%d.root' %islice, key='tree')
        print '\tslice', (islice + 1), 'done'

    # tree->Scan("hnl_iso04_rel_rhoArea:weight_fr:(hnl_hn_vis_pt*(hnl_iso04_rel_rhoArea<0.15)) + ((hnl_iso04_rel_rhoArea>=0.15)*(hnl_hn_vis_pt*(1. + hnl_iso04_rel_rhoArea - 0.15))):abs(hnl_hn_vis_eta):__index__:aux_index","", "colsize=15")

    tomerge = glob(tempDir + 'tree_fr_DR_' + sample + '_slice*.root')
#    tomerge = glob(tempDir + 'tree_fr_' + sample + '_slice*.root')

#    command = 'hadd ' + treeDir + 'tree_fr_' + sample + '.root'
    command = 'hadd ' + treeDir + 'tree_fr_DR_' + sample + '.root'
    for imerge in tomerge:
        command += ' ' + imerge

#    os.system(command)
#    os.system('rm ' + tempDir + '*.root')
