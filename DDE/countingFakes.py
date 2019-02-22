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
pi = rt.TMath.Pi()
####################################################################################################
plotDir     = '/eos/user/v/vstampf/plots/DDE/'
#plotDir     = '/t3home/vstampf/eos/plots/DDE/'
inDir       = '/eos/user/v/vstampf/ntuples/DDE_v0/'
inDir       = '/eos/user/v/vstampf/ntuples/DDE_v1_DiMuIso/'
inDir       = '/eos/user/v/vstampf/ntuples/DDE_v2/'
inDirv2     = '/eos/user/d/dezhu/HNL/ntuples/HN3Lv2.0/'
inDir_vs    = '/eos/user/v/vstampf/ntuples/HN3Lv2.0/'
sigDir_mee  = 'signal/mee/ntuples/'
sigDir_eee  = 'signal/eee/ntuples/'
dataDir_eee = 'data/2017/eee/ntuples/Single_ele_2017B/' 
tempDir     = '/eos/user/v/vstampf/ntuples/temp/'
treeDir     = '/eos/user/v/vstampf/ntuples/DDE_v2/prompt_m/added_trees/'
skimDir     = '/eos/user/v/vstampf/ntuples/skimmed_trees/'
m_dir       = 'prompt_m/'
e_dir       = 'prompt_e/'
suffix      = 'HNLTreeProducer/tree.root'
####################################################################################################
DYBBDir_mee     = '/t3home/vstampf/eos-david/ntuples/HN3Lv2.0/background/montecarlo/mee/partial/DYBB/'
DY50Dir_mee     = '/t3home/vstampf/eos-david/ntuples/HN3Lv2.0/background/montecarlo/mee/partial/DYJetsToLL_M50/'
DY50_extDir_mee = '/t3home/vstampf/eos-david/ntuples/HN3Lv2.0/background/montecarlo/mee/partial/DYJetsToLL_M50_ext/'
DY10Dir_mee     = '/t3home/vstampf/eos-david/ntuples/HN3Lv2.0/background/montecarlo/mee/partial/DYJetsToLL_M10to50/'
TT_dir_mee      = '/t3home/vstampf/eos-david/ntuples/HN3Lv2.0/background/montecarlo/mee/partial/TTJets_amcat_20190130/'  
W_dir_mee       = '/t3home/vstampf/eos-david/ntuples/HN3Lv2.0/background/montecarlo/mee/20190129/ntuples/WJetsToLNu/'
W_ext_dir_mee   = '/t3home/vstampf/eos-david/ntuples/HN3Lv2.0/background/montecarlo/mee/20190129/ntuples/WJetsToLNu_ext/'
####################################################################################################
DYBBDir_mem     = '/eos/user/v/vstampf/ntuples/HN3Lv2.0/background/montecarlo/mc_mem/DYBB/'
DY50Dir_mem     = '/eos/user/v/vstampf/ntuples/HN3Lv2.0/background/montecarlo/mc_mem/DYJetsToLL_M50/'
DY50_extDir_mem = '/eos/user/v/vstampf/ntuples/HN3Lv2.0/background/montecarlo/mc_mem/DYJetsToLL_M50_ext/'
DY10Dir_mem     = '/eos/user/v/vstampf/ntuples/HN3Lv2.0/background/montecarlo/mc_mem/DYJetsToLL_M10to50/'
TT_dir_mem      = '/eos/user/v/vstampf/ntuples/HN3Lv2.0/background/montecarlo/mc_mem/TTJets_amcat/'  
W_dir_mem       = '/eos/user/v/vstampf/ntuples/HN3Lv2.0/background/montecarlo/mc_mem/WJetsToLNu/'
W_ext_dir_mem   = '/eos/user/v/vstampf/ntuples/HN3Lv2.0/background/montecarlo/mc_mem/WJetsToLNu_ext/'
####################################################################################################
DYBBDir_mmm     = '/shome/vstampf/ntuples/mmm/partial/DYBB/'
DY50Dir_mmm     = '/shome/vstampf/ntuples/mmm/partial/DYJetsToLL_M50/'
DY50_extDir_mmm = '/shome/vstampf/ntuples/mmm/partial/DYJetsToLL_M50_ext/'
DY10Dir_mmm     = '/shome/vstampf/ntuples/mmm/partial/DYJetsToLL_M10to50/'
TT_dir_mmm      = '/t3home/vstampf/eos-david/ntuples/HN3Lv2.0/background/montecarlo/mmm/TTJets_amcat_TauDecayInfo/'  
W_dir_mmm       = '/t3home/vstampf/eos-david/ntuples/HN3Lv2.0/background/montecarlo/mmm/WJetsToLNu/'
W_ext_dir_mmm   = '/t3home/vstampf/eos-david/ntuples/HN3Lv2.0/background/montecarlo/mmm/WJetsToLNu_ext/'
####################################################################################################
DYBBDir_eee     = '/t3home/vstampf/eos/ntuples/HN3Lv2.0/background/montecarlo/mc_eee/partial/DYBB/'
DY50Dir_eee     = '/t3home/vstampf/eos/ntuples/HN3Lv2.0/background/montecarlo/mc_eee/partial/DYJetsToLL_M50/'
DY50_extDir_eee = '/t3home/vstampf/eos/ntuples/HN3Lv2.0/background/montecarlo/mc_eee/partial/DYJetsToLL_M50_ext/'
DY10Dir_eee     = '/t3home/vstampf/eos/ntuples/HN3Lv2.0/background/montecarlo/mc_eee/partial/DYJetsToLL_M10to50/'
TT_dir_eee      = '/t3home/vstampf/eos/ntuples/HN3Lv2.0/background/montecarlo/mc_eee/partial/TTJets_amcat/'  
W_dir_eee       = '/t3home/vstampf/eos/ntuples/HN3Lv2.0/background/montecarlo/mc_eee/partial/WJetsToLNu/'
W_ext_dir_eee   = '/t3home/vstampf/eos/ntuples/HN3Lv2.0/background/montecarlo/mc_eee/partial/WJetsToLNu_ext/'
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
                                    ## CUTS ##
####################################################################################################
disp0p5     = 'hnl_2d_disp > 0.5'
disp1       = 'hnl_2d_disp > 1'
M10         = 'hnl_m_01 > 10  &  hnl_m_02 > 10  &  hnl_m_12 > 10'
tt_disp_bj1 = disp0p5 + '  &  nbj > 0'
####################################################################################################
dPhi00 = '( (l0_phi-l0_gen_match_phi + 2*pi) * (l0_phi-l0_gen_match_phi < -pi) + (l0_phi-l0_gen_match_phi - 2*pi) * (l0_phi-l0_gen_match_phi > pi) )' 
dPhi11 = '( (l1_phi-l1_gen_match_phi + 2*pi) * (l1_phi-l1_gen_match_phi < -pi) + (l1_phi-l1_gen_match_phi - 2*pi) * (l1_phi-l1_gen_match_phi > pi) )' 
dPhi22 = '( (l2_phi-l2_gen_match_phi + 2*pi) * (l2_phi-l2_gen_match_phi < -pi) + (l2_phi-l2_gen_match_phi - 2*pi) * (l2_phi-l2_gen_match_phi > pi) )' 
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
                ##         FAKES / PROMPT         ##
####################################################################################################
'''
    sh... SimHit gen matching (included in miniAOD for PAT muons only)
    dr... dR     gen matching (done via RecoGenAnalyzer) 
'''
in_acc = 'abs(l0_eta) < 2.4  &  abs(l1_eta) < 2.4  &  abs(l2_eta) < 2.4'

l0_prompt_m_dr_old = '( (l0_gen_match_fromHardProcessFinalState == 1 | l0_gen_match_isPromptFinalState == 1) & abs(l0_gen_match_pdgid) == 13 )'
l1_prompt_m_dr_old = '( (l1_gen_match_fromHardProcessFinalState == 1 | l1_gen_match_isPromptFinalState == 1) & abs(l0_gen_match_pdgid) == 13 )'
l2_prompt_m_dr_old = '( (l2_gen_match_fromHardProcessFinalState == 1 | l2_gen_match_isPromptFinalState == 1) & abs(l0_gen_match_pdgid) == 13 )'

l0_prompt_m_dr =  '( (l0_gen_match_isDirectPromptTauDecayProductFinalState == 1 | l0_gen_match_isDirectHardProcessTauDecayProductFinalState == 1'
l0_prompt_m_dr += ' | l0_gen_match_fromHardProcessFinalState == 1 | l0_gen_match_isPromptFinalState == 1) & abs(l0_gen_match_pdgid) == 13'#& l0_is_real == 1'
# l0_prompt_m_dr += ' & l0_good_match )'
l0_prompt_m_dr += ' & sqrt( (l0_eta-l0_gen_match_eta)**2 + (' + dPhi00 + ')**2 ) < 0.04 & l0_pdgid == l0_gen_match_pdgid )'

l1_prompt_m_dr =  '( (l1_gen_match_isDirectPromptTauDecayProductFinalState == 1 | l1_gen_match_isDirectHardProcessTauDecayProductFinalState == 1'
l1_prompt_m_dr += ' | l1_gen_match_fromHardProcessFinalState == 1 | l1_gen_match_isPromptFinalState == 1) & abs(l1_gen_match_pdgid) == 13'#& l1_is_real == 1'
# l1_prompt_m_dr += ' & l1_good_match )'
l1_prompt_m_dr += ' & sqrt( (l1_eta-l1_gen_match_eta)**2 + (' + dPhi11 + ')**2 ) < 0.04 & l1_pdgid == l1_gen_match_pdgid )'

l2_prompt_m_dr =  '( (l2_gen_match_isDirectPromptTauDecayProductFinalState == 1 | l2_gen_match_isDirectHardProcessTauDecayProductFinalState == 1'
l2_prompt_m_dr += ' | l2_gen_match_fromHardProcessFinalState == 1 | l2_gen_match_isPromptFinalState == 1) & abs(l2_gen_match_pdgid) == 13'#& l2_is_real == 1'
# l2_prompt_m_dr += ' & l2_good_match )'
l2_prompt_m_dr += ' & sqrt( (l2_eta-l2_gen_match_eta)**2 + (' + dPhi22 + ')**2 ) < 0.04 & l2_pdgid == l2_gen_match_pdgid )'


l0_prompt_e_dr_old = '( (l0_gen_match_fromHardProcessFinalState == 1 | l0_gen_match_isPromptFinalState == 1) & abs(l0_gen_match_pdgid) == 11 )'
l1_prompt_e_dr_old = '( (l1_gen_match_fromHardProcessFinalState == 1 | l1_gen_match_isPromptFinalState == 1) & abs(l1_gen_match_pdgid) == 11 )'
l2_prompt_e_dr_old = '( (l2_gen_match_fromHardProcessFinalState == 1 | l2_gen_match_isPromptFinalState == 1) & abs(l2_gen_match_pdgid) == 11 )'

l0_prompt_e_dr =  '( (l0_gen_match_isDirectPromptTauDecayProductFinalState == 1 | l0_gen_match_isDirectHardProcessTauDecayProductFinalState == 1'
l0_prompt_e_dr += ' | l0_gen_match_fromHardProcessFinalState == 1 | l0_gen_match_isPromptFinalState == 1) & ( abs(l0_gen_match_pdgid) == 11 | abs(l0_gen_match_pdgid) == 22 )'
# l0_prompt_e_dr += ' & l0_good_match )'
l0_prompt_e_dr += ' & sqrt( (l0_eta-l0_gen_match_eta)**2 + (' + dPhi00 + ')**2 ) < 0.04 )'

l1_prompt_e_dr =  '( (l1_gen_match_isDirectPromptTauDecayProductFinalState == 1 | l1_gen_match_isDirectHardProcessTauDecayProductFinalState == 1'
l1_prompt_e_dr += ' | l1_gen_match_fromHardProcessFinalState == 1 | l1_gen_match_isPromptFinalState == 1) & ( abs(l1_gen_match_pdgid) == 11 | abs(l1_gen_match_pdgid) == 22 )'
# l1_prompt_e_dr += ' & l1_good_match )'
l1_prompt_e_dr += ' & sqrt( (l1_eta-l1_gen_match_eta)**2 + (' + dPhi11 + ')**2 ) < 0.04 )'

l2_prompt_e_dr =  '( (l2_gen_match_isDirectPromptTauDecayProductFinalState == 1 | l2_gen_match_isDirectHardProcessTauDecayProductFinalState == 1'
l2_prompt_e_dr += ' | l2_gen_match_fromHardProcessFinalState == 1 | l2_gen_match_isPromptFinalState == 1) & ( abs(l2_gen_match_pdgid) == 11 | abs(l2_gen_match_pdgid) == 22 )'
# l2_prompt_e_dr += ' & l2_good_match )'
l2_prompt_e_dr += ' & sqrt( (l2_eta-l2_gen_match_eta)**2 + (' + dPhi22 + ')**2 ) < 0.04 )'


l0_fake_m_dr = '( !' + l0_prompt_m_dr + ' )'  #'( (l0_gen_match_fromHardProcessFinalState == 0 & l0_gen_match_isPromptFinalState == 0) || abs(l0_gen_match_pdgid) != 13 )'
l1_fake_m_dr = '( !' + l1_prompt_m_dr + ' )' 
l2_fake_m_dr = '( !' + l2_prompt_m_dr + ' )' 

l0_fake_e_dr = '( !' + l0_prompt_e_dr + ' )' 
l1_fake_e_dr = '( !' + l1_prompt_e_dr + ' )' 
l2_fake_e_dr = '( !' + l2_prompt_e_dr + ' )' 

#at_least_one_prompt_m_dr = '(' + l1_prompt_m_dr + ')  ||  (' + l2_prompt_m_dr + ')'
#two_prompt_mm_dr = '(' + l1_prompt_m_dr + ')  &  (' + l2_prompt_m_dr + ')'

l0_prompt_m_sh_old = '( l0_simType == 4 | (l0_simType == 3 & l0_simFlavour == 15) )'
l1_prompt_m_sh_old = '( l1_simType == 4 | (l1_simType == 3 & l1_simFlavour == 15) )'
l2_prompt_m_sh_old = '( l2_simType == 4 | (l2_simType == 3 & l2_simFlavour == 15) )'

l0_prompt_m_sh  = '( abs(l0_simType) == 4 | l0_simFlavour == 15 )'
l1_prompt_m_sh  = '( abs(l1_simType) == 4 | l1_simFlavour == 15 )'
l2_prompt_m_sh  = '( abs(l2_simType) == 4 | l2_simFlavour == 15 )'

l0_prompt_m_sh  = '( l0_simType == 4 | l0_simFlavour == 15 )'
l1_prompt_m_sh  = '( l1_simType == 4 | l1_simFlavour == 15 )'
l2_prompt_m_sh  = '( l2_simType == 4 | l2_simFlavour == 15 )'

l0_fake_m_sh    = '( ! ' + l0_prompt_m_sh + ' )' 
l1_fake_m_sh    = '( ! ' + l1_prompt_m_sh + ' )' 
l2_fake_m_sh    = '( ! ' + l2_prompt_m_sh + ' )' 

l0_fake_m_sh_old = '( ! ' + l0_prompt_m_sh_old + ' )' #'(l0_simType != 4)'# & abs(l0_simType) < 1001)'
l1_fake_m_sh_old = '( ! ' + l1_prompt_m_sh_old + ' )' #'(l1_simType != 4)'# & abs(l1_simType) < 1001)'
l2_fake_m_sh_old = '( ! ' + l2_prompt_m_sh_old + ' )' #'(l2_simType != 4)'# & abs(l2_simType) < 1001)'

l1_heavyfake_m_sh = 'l1_simType == 3'
l2_heavyfake_m_sh = 'l2_simType == 3'


l1f_l2p_mm_sh        = '(' + l1_fake_m_sh   + ' & ' + l2_prompt_m_sh + ')'
l2f_l1p_mm_sh        = '(' + l2_fake_m_sh   + ' & ' + l1_prompt_m_sh + ')'
 
l1f_l2p_ee_dr        = '(' + l1_fake_e_dr   + ' & ' + l2_prompt_e_dr + ')'
l2f_l1p_ee_dr        = '(' + l2_fake_e_dr   + ' & ' + l1_prompt_e_dr + ')'

l0p_l1f_l2p_mmm_sh   = '(' + l1f_l2p_mm_sh  + ' & ' + l0_prompt_m_sh  + ')'
l0p_l2f_l1p_mmm_sh   = '(' + l2f_l1p_mm_sh  + ' & ' + l0_prompt_m_sh  + ')'

l0p_l1f_l2p_mee_shdr  = '(' + l1f_l2p_ee_dr + ' & ' + l0_prompt_m_sh  + ')'
l0p_l2f_l1p_mee_shdr  = '(' + l2f_l1p_ee_dr + ' & ' + l0_prompt_m_sh  + ')'


l1f_l2p_mm_sh_old     = '(' + l1_fake_m_sh_old          + ' & ' + l2_prompt_m_sh_old    + ')'
l2f_l1p_mm_sh_old     = '(' + l2_fake_m_sh_old          + ' & ' + l1_prompt_m_sh_old    + ')'
l1f_l2p_mm_dr         = '(' + l1_fake_m_dr              + ' & ' + l2_prompt_m_dr + ')'
l2f_l1p_mm_dr         = '(' + l2_fake_m_dr              + ' & ' + l1_prompt_m_dr + ')'
l0p_l1f_l2p_mm_sh_old = '(' + l1f_l2p_mm_sh             + ' & ' + l0_prompt_m_sh_old    + ')'
l0p_l2f_l1p_mm_sh_old = '(' + l2f_l1p_mm_sh             + ' & ' + l0_prompt_m_sh_old    + ')'

l1hf_l2p_mm_sh_old     = '(' + l1_heavyfake_m_sh        + ' & ' + l2_prompt_m_sh_old + ')'
l2hf_l1p_mm_sh_old     = '(' + l2_heavyfake_m_sh        + ' & ' + l1_prompt_m_sh_old + ')'
l0p_l1hf_l2p_mm_sh_old = '(' + l1hf_l2p_mm_sh_old       + ' & ' + l0_prompt_m_sh_old + ')'
l0p_l2hf_l1p_mm_sh_old = '(' + l2hf_l1p_mm_sh_old       + ' & ' + l0_prompt_m_sh_old + ')'

two_prompt_mm_sh_old   = '(' + l1_prompt_m_sh_old       + ' & ' + l2_prompt_m_sh_old + ')'
two_prompt_mm_sh       = '(' + l1_prompt_m_sh           + ' & ' + l2_prompt_m_sh     + ')'
two_prompt_mm_dr       = '(' + l1_prompt_m_dr           + ' & ' + l2_prompt_m_dr  + ' & l1_gen_match_pt != l2_gen_match_pt )'
two_prompt_ee_dr       = '(' + l1_prompt_e_dr           + ' & ' + l2_prompt_e_dr  + ' & l1_gen_match_pt != l2_gen_match_pt )'

one_fake_xor_mm_sh       = '(' + l1f_l2p_mm_sh          + ' | ' + l2f_l1p_mm_sh  +  ')' 
one_fake_xor_mm_dr       = '(' + l1f_l2p_mm_dr          + ' | ' + l2f_l1p_mm_dr  +  ' | (' + l1_prompt_m_dr + ' & ' + l2_prompt_m_dr + ' & l1_gen_match_pt == l2_gen_match_pt) )' 
one_fake_xor_ee_dr       = '(' + l1f_l2p_ee_dr          + ' | ' + l2f_l1p_ee_dr  +  ' | (' + l1_prompt_e_dr + ' & ' + l2_prompt_e_dr + ' & l1_gen_match_pt == l2_gen_match_pt) )' 

one_fake_xor_mm_sh_old   = '(' + l1f_l2p_mm_sh_old      + ' | ' + l2f_l1p_mm_sh_old +  ')' 
one_fake_xor_mee_shdr    = '(' + l0p_l1f_l2p_mee_shdr   + ' | ' + l0p_l2f_l1p_mee_shdr  +  ')' 

two_fakes_mm_sh          = '(' + l1_fake_m_sh           + ' & ' + l2_fake_m_sh        +  ')'  
two_fakes_mm_sh_old      = '(' + l1_fake_m_sh_old       + ' & ' + l2_fake_m_sh_old    +  ')'  
two_fakes_ee_dr          = '(' + l1_fake_e_dr           + ' & ' + l2_fake_e_dr   +  ')'  
two_fakes_mm_dr          = '(' + l1_fake_m_dr           + ' & ' + l2_fake_m_dr   +  ')'  

# sameJet     = '( l1_jet_pt == l2_jet_pt)'
# sameJet     = '( abs(l1_jet_pt - l2_jet_pt) < 1 )'
# sameJet     = '( abs(l1_jet_pt - l2_jet_pt) < 1 & hnl_dr_12 < 0.8 )' # 0.8 is twice the jet size
sameJet     = '( abs(l1_jet_pt - l2_jet_pt) < 1 & abs(l1_jet_eta - l2_jet_eta) < 1 & hnl_dr_12 < 0.8 )' # 0.8 is twice the jet size

twoFakes_sameJet_mm_dr  = '(' + two_fakes_mm_dr  + ' & ' + sameJet + ')' 
twoFakes_sameJet_mm_sh  = '(' + two_fakes_mm_sh  + ' & ' + sameJet + ')' 
twoFakes_sameJet_ee_dr  = '(' + two_fakes_ee_dr  + ' & ' + sameJet + ')' 

twoFakes_sameJet_mm_sh_old    = '(' + two_fakes_mm_sh_old   + ' & ' + sameJet + ')' 
twoFakes_sameJet_mmm_sh       = '(' + two_fakes_mm_sh       + ' & ' + sameJet + ' & ' + l0_prompt_m_sh   + ')' 

l1_LVtx_dr  = '( abs(l1_gen_match_vtx_x) + abs(l1_gen_match_vtx_y) + abs(l1_gen_match_vtx_z) )'
l2_LVtx_dr  = '( abs(l2_gen_match_vtx_x) + abs(l2_gen_match_vtx_y) + abs(l2_gen_match_vtx_z) )'

DeltaLVtx = '( ' + l1_LVtx_dr + ' - ' + l2_LVtx_dr + ' )' 
SumLVtx   = '( ' + l1_LVtx_dr + ' + ' + l2_LVtx_dr + ' )'

#sameVtx_dr = '( ( 2 *( ' + l1_vtx_dr + ' - ' + l2_vtx_dr + ' ) / ( ' + l1_vtx_dr + ' + ' + l2_vtx_dr + ' ) ) < 0.01 )'
#sameVtx_dr = '( ( ' + DeltaLVtx + ' / ' + SumLVtx + ' ) < 0.005 )'
sameVtx_dr = '( ' + DeltaLVtx + ' == 0 )'
sameVtx    = '( l2_simProdZ == l1_simProdZ & l1_simProdZ != 0 )'

twoFakes_sameVtx_mm_sh_old  = '(' + two_fakes_mm_sh        + ' & l2_simProdZ == l1_simProdZ & l1_simProdZ != 0)'  
twoFakes_sameVtx_mm_sh      = '(' + two_fakes_mm_sh        + ' & ' + sameVtx_dr     +  ')' 
twoFakes_sameVtx_mm_dr      = '(' + two_fakes_mm_dr        + ' & ' + sameVtx_dr     +  ')'
twoFakes_sameVtx_ee_dr      = '(' + two_fakes_ee_dr        + ' & ' + sameVtx_dr     +  ')'

twoFakes_sameVtxJet_mm_sh        = '(' + twoFakes_sameVtx_mm_sh    + ' & ' + sameJet + ')' 
twoFakes_sameVtxJet_mm_sh_l0p    = '(' + twoFakes_sameVtx_mm_sh    + ' & ' + sameJet + ' & ' + l0_prompt_m_sh_old      + ')'
twoFakes_sameVtxJet_mm_sh_l0p_dr = '(' + twoFakes_sameVtx_mm_dr + ' & ' + sameJet + ' & ' + l0_prompt_m_dr + ')'

twoHeavyFakes_mm_sh         = '(' + l1_heavyfake_m_sh  + ' & ' + l2_heavyfake_m_sh   +  ')'  
twoHeavyFakes_sameVtx_mm_sh = '(' + twoHeavyFakes_mm_sh + ' & l2_simProdZ == l1_simProdZ & l1_simProdZ != 0)'  

no_ghosts          = '( l1_simType < 1001 & l2_simType < 1001 )'
no_fakes_mm_sh_old = two_prompt_mm_sh_old
no_fakes_mm_sh     = two_prompt_mm_sh
no_fakes_mm_dr     = two_prompt_mm_dr
no_fakes_ee_dr     = two_prompt_ee_dr
####################################################################################################
####################################################################################################
              ##               LOOSE / TIGHT REGIONS                ##
####################################################################################################
              ##                 DOUBLE FAKE RATE                   ##  
####################################################################################################
DFR_LOOSE_MEE          =  ' & (l1_pt > 3 & l1_LooseNoIso & l2_pt > 3 & l2_LooseNoIso & l0_id_t & l0_reliso_rho_04 < 0.15 & hnl_iso04_rel_rhoArea < 1 )'     
DFR_LOOSENOTTIGHT_MEE  =  ' & (l1_pt > 3 & l1_LooseNoIso & l2_pt > 3 & l2_LooseNoIso & l0_id_t & l0_reliso_rho_04 < 0.15 & (l1_reliso05 > 0.2 | l2_reliso05 > 0.2) & hnl_iso04_rel_rhoArea < 1 )'#FIXME
DFR_TIGHT_MEE          =  ' & (l1_pt > 3 & l1_LooseNoIso & l2_pt > 3 & l2_LooseNoIso & l0_id_t & l0_reliso_rho_04 < 0.15 & l1_reliso05 < 0.2 & l2_reliso05 < 0.2 )' 
####################################################################################################
# FIXME
DFR_LOOSE_MEM          =  ' & (l1_pt > 3 & l1_LooseNoIso & l2_pt > 3 & l2_LooseNoIso & l0_id_t & l0_reliso_rho_03 < 0.15 & hnl_iso03_rel_rhoArea < 1 )'     
DFR_LOOSENOTTIGHT_MEM  =  ' & (l1_pt > 3 & l1_LooseNoIso & l2_pt > 3 & l2_LooseNoIso & l0_id_t & l0_reliso_rho_03 < 0.15 & (l1_reliso05 > 0.2 | l2_reliso05 > 0.2) & hnl_iso03_rel_rhoArea < 1 )'#FIXME
DFR_TIGHT_MEM          =  ' & (l1_pt > 3 & l1_MediumNoIso & l2_pt > 3 & l2_LooseNoIso & l0_id_t & l0_reliso_rho_03 < 0.15 & l1_reliso05 < 0.2 & l2_reliso05 < 0.2 )' 
####################################################################################################
DFR_LOOSE_MMM         = ' & (l1_pt > 3 & l2_pt > 3 & l0_id_t & l0_reliso_rho_04 < 0.15 & l1_id_l & l2_id_l & hnl_iso04_rel_rhoArea < 1 )'
DFR_LOOSENOTTIGHT_MMM = ' & (l1_pt > 3 & l2_pt > 3 & l0_id_t & l0_reliso_rho_04 < 0.15 & l1_id_l & l2_id_l & (l1_reliso_rho_04 > 0.15 | l2_reliso_rho_04 > 0.15) & hnl_iso04_rel_rhoArea < 1 )'# FIXME 
DFR_TIGHT_MMM         = ' & (l1_pt > 3 & l2_pt > 3 & l0_id_t & l0_reliso_rho_04 < 0.15 & l1_id_l & l2_id_l & l1_reliso_rho_04 < 0.15 & l2_reliso_rho_04 < 0.15 )' 
####################################################################################################
DFR_LOOSE_EEE         =  ' & (l1_pt > 3 & l1_LooseNoIso & l2_pt > 3 & l2_LooseNoIso & l0_eid_mva_iso_wp90 & l0_reliso05 < 0.15 & hnl_iso03_rel_rhoArea < 3 )' 
DFR_LOOSENOTTIGHT_EEE =  ' & (l1_pt > 3 & l1_LooseNoIso & l2_pt > 3 & l2_LooseNoIso & l0_eid_mva_iso_wp90 & l0_reliso05 < 0.15 & (l1_reliso05 > 0.15 | l2_reliso05 > 0.15) & hnl_iso04_rel_rhoArea < 3 )' # FIXME 
DFR_TIGHT_EEE         =  ' & (l1_pt > 3 & l1_MediumNoIso & l2_pt > 3 & l2_MediumNoIso & l0_eid_mva_iso_wp90 & l0_reliso05 < 0.15 & l1_reliso05 < 0.15 & l2_reliso05 < 0.15 )' 
####################################################################################################
DFR_LOOSE_EMM         = ' & (l1_pt > 3 & l2_pt > 3 & l0_eid_cut_loose & l0_reliso05 < 0.15 & l1_id_l & l2_id_l & hnl_iso04_rel_rhoArea < 1 )'
DFR_LOOSENOTTIGHT_EMM = ' & (l1_pt > 3 & l2_pt > 3 & l0_eid_cut_loose & l0_reliso05 < 0.15 & l1_id_l & l2_id_l & (l1_reliso_rho_04 > 0.15 | l2_reliso_rho_04 > 0.15) & hnl_iso04_rel_rhoArea < 1 )'  # FIXME 
DFR_TIGHT_EMM         = ' & (l1_pt > 3 & l2_pt > 3 & l0_eid_cut_loose & l0_reliso05 < 0.15 & l1_id_l & l2_id_l & l1_reliso_rho_04 < 0.15 & l2_reliso_rho_04 < 0.15 )' 
####################################################################################################
              ##                 SINGLE FAKE RATE                   ##  
####################################################################################################
l0l1_ee    = '(l1_pt > 3 & l0_eid_mva_iso_wp90 & l1_eid_mva_iso_wp90 & l0_reliso05 < 0.15 & l1_reliso05 < 0.15'
l0l1_ee    += ' & hnl_iso03_rel_rhoArea < 1 & abs(hnl_m_01 - 91.19) < 10 & l0_q * l1_q < 0 & abs(l0_dxy) < 0.05 & abs(l1_dxy) < 0.05)'
#l0l1_ee    += ' & hnl_iso03_rel_rhoArea < 1 & l0_q * l1_q < 0 & abs(l0_dxy) < 0.05 & abs(l1_dxy) < 0.05)'
l0l1_ee    += ' & ' + l0_prompt_e_dr + ' & ' + l1_prompt_e_dr 

l0l2_ee    = '(l2_pt > 3 & l0_eid_mva_iso_wp90 & l2_eid_mva_iso_wp90 & l0_reliso05 < 0.15 & l2_reliso05 < 0.15'
l0l2_ee    += ' & hnl_iso03_rel_rhoArea < 1 & abs(hnl_m_02 - 91.19) < 10 & l0_q * l2_q < 0 & abs(l0_dxy) < 0.05 & abs(l2_dxy) < 0.05)'
#l0l2_ee    += ' & hnl_iso03_rel_rhoArea < 1 & l0_q * l2_q < 0 & abs(l0_dxy) < 0.05 & abs(l2_dxy) < 0.05)'
l0l2_ee    += ' & ' + l0_prompt_e_dr + ' & ' + l2_prompt_e_dr
####################################################################################################
l0l1_me    = '(l1_pt > 3 & l0_id_t & l1_eid_mva_iso_wp90 & l0_reliso_rho_03 < 0.15 & l1_reliso05 < 0.15'
l0l1_me    += ' & hnl_iso03_rel_rhoArea < 1 & abs(hnl_m_01 - 91.19) < 10 & l0_q * l1_q < 0 & abs(l0_dxy) < 0.05 & abs(l1_dxy) < 0.05)'
l0l1_me    += ' & ' + l0_prompt_m_dr + ' & ' + l1_prompt_e_dr 
####################################################################################################
l0l2_em    = '(l2_pt > 3 & l0_eid_mva_iso_wp90 & l2_id_m & l0_reliso05 < 0.15 & l2_reliso_rho_03 < 0.15'
l0l2_em    += ' & hnl_iso03_rel_rhoArea < 1 & abs(hnl_m_02 - 91.19) < 10 & l0_q * l2_q < 0 & abs(l0_dxy) < 0.05 & abs(l2_dxy) < 0.05)'
l0l2_em    += ' & ' + l0_prompt_e_dr + ' & ' + l2_prompt_m_dr 
####################################################################################################
l0l1_mm    = 'l1_pt > 3 & l0_id_t & l1_id_t & l0_reliso_rho_03 < 0.15 & l1_reliso_rho_03 < 0.15'
l0l1_mm    += ' & hnl_iso03_rel_rhoArea < 2 & abs(hnl_m_01 - 91.19) < 10 & l0_q * l1_q < 0 & abs(l0_dxy) < 0.05 & abs(l1_dxy) < 0.05'
l0l1_mm    += ' & ' + l0_prompt_m_dr + ' & ' + l1_prompt_m_dr 

l0l2_mm    = 'l0_pt > 15 & l2_pt > 5 & l0_id_m & l2_id_m & l0_reliso_rho_03 < 0.15 & l2_reliso_rho_03 < 0.15'
#l0l2_mm    += ' & hnl_iso03_rel_rhoArea < 1 & abs(hnl_m_02 - 91.19) < 10 & l0_q * l2_q < 0 & abs(l0_dxy) < 0.05 & abs(l2_dxy) < 0.05'
l0l2_mm    += ' & l0_q * l2_q < 0 & abs(l0_dxy) < 0.05 & abs(l2_dxy) < 0.05 & abs(l1_reliso_rho_03) < 0.45'
l0l2_mm    += ' & ' + l0_prompt_m_dr + ' & ' + l2_prompt_m_dr 
####################################################################################################
l1_e_tight = 'l1_pt > 5 & l1_MediumNoIso & l1_reliso05 < 0.15 & abs(l1_dxy) > 0.05 & ' + l1_fake_e_dr
l2_e_tight = 'l2_pt > 5 & l2_MediumNoIso & l2_reliso05 < 0.15 & abs(l2_dxy) > 0.05 & ' + l2_fake_e_dr
l1_e_lnt   = 'l1_pt > 5 & l1_LooseNoIso  & l1_reliso05 > 0.15 & abs(l1_dxy) > 0.05 & ' + l1_fake_e_dr #FIXME
l2_e_lnt   = 'l2_pt > 5 & l2_LooseNoIso  & l2_reliso05 > 0.15 & abs(l2_dxy) > 0.05 & ' + l2_fake_e_dr #FIXME
l1_e_loose = 'l1_pt > 5 & l1_LooseNoIso  & abs(l1_dxy) > 0.05 & ' + l1_fake_e_dr
l2_e_loose = 'l2_pt > 5 & l2_LooseNoIso  & abs(l2_dxy) > 0.05 & ' + l2_fake_e_dr
####################################################################################################
l1_m_tight = 'l1_pt > 3 & l1_id_l & l1_reliso_rho_03 < 0.15 & ' + l1_fake_m_dr
l2_m_tight = 'l2_pt > 3 & l2_id_l & l2_reliso_rho_03 < 0.15 & ' + l2_fake_m_dr
l1_m_lnt   = 'l1_pt > 3 & l1_id_l & l1_reliso_rho_03 > 0.15 & ' + l1_fake_m_dr
l2_m_lnt   = 'l2_pt > 3 & l2_id_l & l2_reliso_rho_03 > 0.15 & ' + l2_fake_m_dr
l1_m_loose = 'l1_pt > 3 & l1_id_l & ' + l1_fake_m_dr
l2_m_loose = 'l2_pt > 3 & l2_id_l & ' + l2_fake_m_dr
####################################################################################################

####################################################################################################
Z_veto_01       = '( (l0_q + l1_q == 0) & (abs(hnl_m_01 - 91.2) > 15) )  &  (l0_q + l2_q != 0)  &  (l1_q + l2_q != 0)'
Z_veto_02       = '(l0_q + l1_q != 0)  &  ( (l0_q + l2_q == 0) & (abs(hnl_m_02 - 91.2) > 15) )  &  (l1_q + l2_q != 0)'
Z_veto_12       = '(l0_q + l1_q != 0)  &  (l0_q + l2_q != 0)  &  ( (l1_q + l2_q == 0) & (abs(hnl_m_12 - 91.2) > 15) )' 

Z_veto_01_02    = '( (l0_q + l1_q == 0) & (abs(hnl_m_01 - 91.2) > 15) )  &  ( (l0_q + l2_q == 0) & (abs(hnl_m_02 - 91.2) > 15) )  &  (l1_q + l2_q != 0)'  
Z_veto_01_12    = '( (l0_q + l1_q == 0) & (abs(hnl_m_01 - 91.2) > 15) )  &  (l0_q + l2_q != 0)  &  ( (l1_q + l2_q == 0) & (abs(hnl_m_12 - 91.2) > 15) )'  
Z_veto_02_12    = '(l0_q + l1_q != 0)  &  ( (l0_q + l2_q == 0) & (abs(hnl_m_02 - 91.2) > 15) )  &  ( (l1_q + l2_q == 0) & (abs(hnl_m_12 - 91.2) > 15) )'  

Z_veto_01_02_12 = '( (l0_q + l1_q == 0) & (abs(hnl_m_01 - 91.2) > 15) )  &  ( (l0_q + l2_q == 0) & (abs(hnl_m_02 - 91.2) > 15) )  &  ( (l1_q + l2_q == 0) & (abs(hnl_m_12 - 91.2) > 15) )'

single_Z_veto = '(  ' + Z_veto_01 + '   |   ' + Z_veto_02 + '   |   ' + Z_veto_12 + '  )'
double_Z_veto = '(  ' + Z_veto_01_02 + '   |   ' + Z_veto_01_12 + '   |   ' + Z_veto_02_12 + '  )'

Z_veto = '(   ' + single_Z_veto + '    |    ' + double_Z_veto + '    |    ' + Z_veto_01_02_12 + '   )' 

#twoLepObjIsoleq1  = ' & ( max(l1_reliso05_03 * l1_pt, l2_reliso05_03 * l2_pt) / (hnl_hn_vis_pt) ) < 1'
#twoLepObjIsoleq1  = ' & ( max(l1_reliso05 * l1_pt, l2_reliso05 * l2_pt) / (hnl_hn_vis_pt) ) < 1'
twoLepObjIsoleq1  = ' & ( max(l1_reliso_rho_04 * l1_pt, l2_reliso_rho_04 * l2_pt) / (hnl_hn_vis_pt) ) < 1'   ## FROM v2 ON
twoLepObjIsoleq1  = ' & hnl_iso04_rel_rhoArea < 1' 

PTCONE = '(  ( hnl_hn_vis_pt * (hnl_iso03_rel_rhoArea<0.15) ) + ( (hnl_iso03_rel_rhoArea>=0.15) * ( hnl_hn_vis_pt * (1. + hnl_iso03_rel_rhoArea - 0.15) ) )  )'

eta_0to1p2   = '( abs(l1_eta) < 1.2 & abs(l2_eta) < 1.2 )'
eta_1p2to2p1 = '( abs(l1_eta) > 1.2 & abs(l2_eta) > 1.2 & abs(l1_eta) < 2.1 & abs(l2_eta) < 2.1)'
eta_2p1to2p4 = '( abs(l1_eta) > 2.1 & abs(l2_eta) > 2.1 & abs(l1_eta) < 2.4 & abs(l2_eta) < 2.4)'

eta_bins = [['0_to_1p2'  , eta_0to1p2],
            ['1p2_to_2p1', eta_1p2to2p1],
            ['2p1_to_2p4', eta_2p1to2p4]]

cr_tt     = 'abs(hnl_m_12 - 91.18) > 15  &  abs(hnl_w_vis_m - 91.18) > 15  &  nbj >= 1'
q_pt      = 'l0_pt > 35  &  l1_pt > 4  &  l2_pt > 4  &  l1_q != l2_q'
im_par_l0 = 'abs(l0_dxy) < 0.045 & abs(l0_dz) < 0.2'
tt_v0 = cr_tt + ' & ' + q_pt + ' & ' + im_par_l0

isolst = [0.10,0.11,0.12,0.13,0.14,0.15,0.16,0.17,0.18,0.19,0.20]

b_pt_std    = np.arange(5.,105,5)
b_pt        = np.array([ 0., 5., 10., 15., 20., 25., 35., 50., 70.])
b_2d        = np.arange(0., 10, 0.2)
b_2d_sig    = np.arange(0., 50, 0.25)
b_2d_sig    = np.arange(0., 100, 0.5)
b_m         = np.arange(0., 5.25, 0.25)
b_M         = np.arange(0.,202,2)
b_eta       = np.array([0., 1.2, 2.1, 2.4]) 
b_rho       = np.arange(-100.,100,4)
b_rho_crs   = np.arange(0.,10,0.25)
b_rho       = np.arange(0.,15,0.25)
b_dR        = np.arange(0.,6.05,0.05)
b_dR        = np.arange(0.,0.85,0.05)
b_dR_coarse = np.arange(0.,6,0.2)
b_dR_Coarse = np.arange(0.,6,0.4)
b_z         = np.arange(-1.5,1.5,0.06)
b_abs_z     = np.arange(0.,2,0.05)
b_z_fine    = np.arange(-0.02,0.02,0.0001)
b_st        = np.arange(-20,20,1)
b_sf        = np.arange(-20,20,1)
b_y         = np.arange(0.,1.,0.1)
b_chi2      = np.arange(0.,1.05,0.05)

framer = rt.TH2F('','',len(b_pt)-1,b_pt,len(b_y)-1,b_y)
framer.GetYaxis().SetRangeUser(0.,0.5)
framer.GetYaxis().SetRangeUser(0.,1.0)
####################################################################################################

####################################################################################################
def countFakes(ch='mee',DZ=True,DISP=True):

    cuts = 'abs(l1_dz) < 2 & abs(l2_dz) < 2 & hnl_2d_disp > 0.5 & l1_q * l2_q < 0'

    promptMode = ch[0]
    pairMode = ch[1] + ch[2]

    samples = ['TT','DY']#,'TT','WJ']#
    sList = raw_input('\n\tchoose between TT, DY and WJ (inclusively)\n\t')

    samples = sList.split(',')

    if samples[0] == 'all': samples = ['TT','DY','WJ']

    SFR, DFR, dirs = selectCuts(ch)

    LOOSE, TIGHT, LOOSENOTTIGHT = DFR
    DYBB_dir, DY10_dir, DY50_dir, DY50_ext_dir, TT_dir, W_dir, W_ext_dir = dirs   

    cuts += TIGHT

    print '\n\tmode: %s\n'%ch

    N_ENTRIES = 0

    for sample in samples: 
        t = None
        if sample == 'DY':
            t = rt.TChain('tree')
            t.Add(DYBB_dir + suffix)
            t.Add(DY10_dir + suffix)
            t.Add(DY50_dir + suffix)
            t.Add(DY50_ext_dir + suffix)
            N_ENTRIES = t.GetEntries()
        if sample == 'TT':
            fin = rt.TFile(TT_dir + suffix)
            t = fin.Get('tree')
            N_ENTRIES = t.GetEntries()

        if sample == 'WJ':
            t = rt.TChain('tree')
            t.Add(W_dir + suffix)
            t.Add(W_ext_dir + suffix)
            N_ENTRIES = t.GetEntries()

        n_entries             = t.GetEntries(cuts) 

        print '\t', sample, 'entries before selection:', N_ENTRIES 
        print '\t',sample, 'entries after selection:', n_entries
        print '\n\t cuts: %s'%cuts
        print '\n\t TIGHT WP: %s\n' %TIGHT

        if promptMode == 'm': # SIMHIT IS MUON SPECIFIC
            n_l0_is_fake_sh  = t.GetEntries(cuts + ' & ' + l0_fake_m_sh)
            print '\t l0_is_fake_sh  \t\t'             , '{:.1%} \t\t'.format(n_l0_is_fake_sh/n_entries)      , n_l0_is_fake_sh    
            n_l0_is_fake_dr  = t.GetEntries(cuts + ' & ' + l0_fake_m_dr)

        if promptMode == 'e':
            n_l0_is_fake_dr       = t.GetEntries(cuts + ' & ' + l0_fake_e_dr)

        if pairMode == 'ee': 
            n_no_fakes_dr         = t.GetEntries(cuts + ' & ' + no_fakes_ee_dr)
            n_one_fake_xor_dr     = t.GetEntries(cuts + ' & ' + one_fake_xor_ee_dr)
            n_two_fakes_dr        = t.GetEntries(cuts + ' & ' + two_fakes_ee_dr)
            n_twoFakes_sameJet_dr = t.GetEntries(cuts + ' & ' + twoFakes_sameJet_ee_dr) 

        if pairMode == 'em': # SIMHIT IS MUON SPECIFIC
            n_no_fakes_dr         = t.GetEntries(cuts + ' & ' + no_fakes_em_dr)
            n_one_fake_xor_dr     = t.GetEntries(cuts + ' & ' + one_fake_xor_em_dr)
            n_two_fakes_dr        = t.GetEntries(cuts + ' & ' + two_fakes_em_dr)
            n_twoFakes_sameJet_dr = t.GetEntries(cuts + ' & ' + twoFakes_sameJet_em_dr) 

        if pairMode == 'mm': # SIMHIT IS MUON SPECIFIC
            n_no_fakes_dr         = t.GetEntries(cuts + ' & ' + no_fakes_mm_dr)
            n_one_fake_xor_dr     = t.GetEntries(cuts + ' & ' + one_fake_xor_mm_dr)
            n_two_fakes_dr        = t.GetEntries(cuts + ' & ' + two_fakes_mm_dr)
            n_twoFakes_sameJet_dr = t.GetEntries(cuts + ' & ' + twoFakes_sameJet_mm_dr) 

            n_no_fakes_sh            = t.GetEntries(cuts + ' & ' + no_fakes_mm_sh)
            print '\t no_fakes_sh \t\t\t'          , '{:.1%} \t\t'.format(n_no_fakes_sh/n_entries)                 , n_no_fakes_sh      

            n_one_fake_xor_sh        = t.GetEntries(cuts + ' & ' + one_fake_xor_mm_sh)
            print '\t one_fake_xor_sh \t\t'        , '{:.1%} \t\t'.format(n_one_fake_xor_sh/n_entries)             , n_one_fake_xor_sh      

            n_two_fakes_sh           = t.GetEntries(cuts + ' & ' + two_fakes_mm_sh)
            print '\t two_fakes_sh \t\t\t'         , '{:.1%} \t\t'.format(n_two_fakes_sh/n_entries)                , n_two_fakes_sh         

            n_twoFakes_sameJet_sh    = t.GetEntries(cuts + ' & ' + twoFakes_sameJet_mm_sh) # THIS IS UPDATED, NO WORRIES
            print '\t twoFakes_sameJet_sh \t\t'    , '{:.1%} \t\t'.format(n_twoFakes_sameJet_sh/n_two_fakes_sh)    , n_twoFakes_sameJet_sh   , '\t({:.1%})\n'.format(n_twoFakes_sameJet_sh/n_entries)

        # THE REST HOLDS IN ALL MODES
        print '\t l0_is_fake_dr \t\t\t'            , '{:.1%} \t\t'.format(n_l0_is_fake_dr/n_entries)              , n_l0_is_fake_dr     
        print '\t no_fakes_dr \t\t\t'              , '{:.1%} \t\t'.format(n_no_fakes_dr/n_entries)                , n_no_fakes_dr      
        print '\t one_fake_xor_dr \t\t'            , '{:.1%} \t\t'.format(n_one_fake_xor_dr/n_entries)            , n_one_fake_xor_dr      
        print '\t two_fakes_dr\t\t\t'              , '{:.1%} \t\t'.format(n_two_fakes_dr/n_entries)               , n_two_fakes_dr         
        print '\t twoFakes_sameJet_dr \t\t'        , '{:.1%} \t\t'.format(n_twoFakes_sameJet_dr/n_two_fakes_dr)   , n_twoFakes_sameJet_dr, '\t({:.1%})'.format(n_twoFakes_sameJet_dr/n_entries)

        sys.stdout = open(plotDir + sample + '_%s'%ch + '.py', 'w+')

        print '\t', sample, 'entries before selection:', N_ENTRIES 
        print '\t', sample, 'entries after selection:' , n_entries
        print '\n\t cuts: %s'%cuts
        print '\n\t TIGHT WP: %s\n' %TIGHT

        if pairMode == 'mm': # SIMHIT IS MUON SPECIFIC
            print '\t l0_is_fake_sh \t\t'            , '{:.1%} \t'.format(n_l0_is_fake_sh/n_entries)              , n_l0_is_fake_sh     
            print '\t no_fakes_sh \t\t'              , '{:.1%} \t'.format(n_no_fakes_sh/n_entries)                , n_no_fakes_sh      
            print '\t one_fake_xor_sh \t\t'          , '{:.1%} \t'.format(n_one_fake_xor_sh/n_entries)            , n_one_fake_xor_sh      
            print '\t two_fakes_sh \t\t'             , '{:.1%} \t'.format(n_two_fakes_sh/n_entries)               , n_two_fakes_sh         
            print '\t twoFakes_sameJet_sh \t'        , '{:.1%} \t'.format(n_twoFakes_sameJet_sh/n_two_fakes_sh)   , n_twoFakes_sameJet_sh   , '\t({:.1%})\n'.format(n_twoFakes_sameJet_sh/n_entries)

        print '\t l0_is_fake_dr \t\t'                , '{:.1%} \t'.format(n_l0_is_fake_dr/n_entries)              , n_l0_is_fake_dr     
        print '\t no_fakes_dr \t\t'                  , '{:.1%} \t'.format(n_no_fakes_dr/n_entries)                , n_no_fakes_dr      
        print '\t one_fake_xor_dr \t'                , '{:.1%} \t'.format(n_one_fake_xor_dr/n_entries)            , n_one_fake_xor_dr      
        print '\t two_fakes_dr\t\t'                  , '{:.1%} \t'.format(n_two_fakes_dr/n_entries)               , n_two_fakes_dr         
        print '\t twoFakes_sameJet_dr \t'            , '{:.1%} \t'.format(n_twoFakes_sameJet_dr/n_two_fakes_dr)   , n_twoFakes_sameJet_dr, '\t({:.1%})'.format(n_twoFakes_sameJet_dr/n_entries)
        
        sys.stderr = sys.__stderr__
        sys.stdout = sys.__stdout__

        print '\n\t', sample + '_%s\t\t done\n'%ch
####################################################################################################

####################################################################################################
def checkTTLratio(ch='mmm',sfr=True,dfr=False,file=True,mode='dr'):

    samples = ['TT','DY','WJ']

    print '\n\tmode: %s\n'%ch

    sList = raw_input('\tchoose between TT, DY and WJ (inclusively)\n\t')
    samples = sList.split(',')

    if samples[0] == 'all': samples = ['TT','DY','WJ']

    h_pt_1f = []; h_pt_2f = []; i = 0
    iso_cut = 0.15
    iso_str = str(int(iso_cut * 100))

    cuts = 'abs(l1_dz) < 2 & abs(l2_dz) < 2 & hnl_2d_disp > 0.5 & l1_q * l2_q < 0'

    N_ENTRIES = 0

    SFR, DFR, dirs = selectCuts(ch)

    l0l1, l0l2, l1_loose, l2_loose, l1_lnt, l2_lnt, l1_tight, l2_tight = SFR 
    LOOSE, TIGHT, LOOSENOTTIGHT = DFR
    DYBB_dir, DY10_dir, DY50_dir, DY50_ext_dir, TT_dir, W_dir, W_ext_dir = dirs   

    dRdefList, sHdefList = selectDefs(ch)

    if mode == 'dr':
        l0_is_fake, no_fakes, one_fake_xor, two_fakes, twoFakes_sameJet = dRdefList
    if mode == 'sh':
        l0_is_fake, no_fakes, one_fake_xor, two_fakes, twoFakes_sameJet = sHdefList

    if file == True:
        print '\n\t pT cone: %s\n' %PTCONE 
        sys.stdout = open(plotDir + 'FR_%s_%s' %(ch,samples) + '.py', 'w+')

    print '\n\t pT cone: %s\n' %PTCONE 

    for sample in samples: 
        t = None
        if sample == 'DY':
            t = rt.TChain('tree')
            t.Add(DYBB_dir + suffix)
            t.Add(DY10_dir + suffix)
            t.Add(DY50_dir + suffix)
            t.Add(DY50_ext_dir + suffix)
            N_ENTRIES = t.GetEntries()
        if sample == 'TT':
            fin = rt.TFile(TT_dir + suffix)
            t = fin.Get('tree')
            N_ENTRIES = t.GetEntries()
        if sample == 'WJ':
            t = rt.TChain('tree')
            t.Add(W_dir + suffix)
            t.Add(W_ext_dir + suffix)
            N_ENTRIES = t.GetEntries()

        if sfr:

            h_pt_1f_T_012  = rt.TH1F('pt_1f_T_012', 'pt_1f_T_012',len(b_pt)-1,b_pt)
            h_pt_1f_T_021  = rt.TH1F('pt_1f_T_021', 'pt_1f_T_021',len(b_pt)-1,b_pt)
            h_pt_1f_L_012  = rt.TH1F('pt_1f_L_012', 'pt_1f_L_012',len(b_pt)-1,b_pt)
            h_pt_1f_L_021  = rt.TH1F('pt_1f_L_021', 'pt_1f_L_021',len(b_pt)-1,b_pt)

    #            print '\t',sample, 'entries after loose selection:', t.GetEntries(SFR_DY_LOOSE_EEE)
    #            print '\n\t TIGHT WP: %s\n' %SFR_DY_TIGHT_EEE
    #            print '\n\t LOOSE WP: %s\n' %SFR_DY_LOOSE_EEE
    #            print '\n\t LNT WP: %s\n' %SFR_DY_LNT_EEE

    #        if sample == 'DY':

            cuts_SFR = '1'

            print '\tsample: %s, drawing single fakes ...'%sample
            print '\t',sample, 'entries after cuts:', t.GetEntries(cuts)
            print '\n\t cuts: %s'%cuts_SFR
            print '\n\t l0l1: %s\n'       %(l0l1)
            print '\n\t l0l2: %s\n'       %(l0l2)
            print '\n\t l1_loose: %s\n'   %(l1_loose)
            print '\n\t l1_tight: %s\n'   %(l1_tight)
            print '\n\t l2_loose: %s\n'   %(l2_loose)
            print '\n\t l2_tight: %s\n'   %(l2_tight)

        
            if ch in ['mmm','eee']:
                t.Draw('l1_pt >> pt_1f_T_021', cuts_SFR + ' & ' + l0l2 + ' & ' + l1_tight)
                t.Draw('l2_pt >> pt_1f_T_012', cuts_SFR + ' & ' + l0l1 + ' & ' + l2_tight)

            if ch == 'mem':
                t.Draw('l1_pt >> pt_1f_T_021', cuts_SFR + ' & ' + l0l2 + ' & ' + l1_tight)

            h_pt_1f_T_012.Add(h_pt_1f_T_021)
            print '\tentries tight:', h_pt_1f_T_012.GetEntries()

            if ch in ['mmm','eee']:
                t.Draw('l1_pt >> pt_1f_L_021', cuts_SFR + ' & ' + l0l2 + ' & ' + l1_loose)
                t.Draw('l2_pt >> pt_1f_L_012', cuts_SFR + ' & ' + l0l1 + ' & ' + l2_loose)

            if ch == 'mem':
                t.Draw('l1_pt >> pt_1f_L_021', cuts_SFR + ' & ' + l0l2 + ' & ' + l1_loose)

            h_pt_1f_L_012.Add(h_pt_1f_L_021)
            print '\tentries loose:', h_pt_1f_L_012.GetEntries()

            h_pt_1f.append(rt.TEfficiency(h_pt_1f_T_012, h_pt_1f_L_012))
            h_pt_1f[i].SetTitle('%s; p_{T} [GeV]; tight-to-loose ratio (single fakes)'%sample)
            h_pt_1f[i].SetMarkerColor(rt.kBlue+(4-i*2))
            h_pt_1f[i].SetFillColor(rt.kWhite)

            c_pt_1f = rt.TCanvas('ptCone_1f', 'ptCone_1f')
            framer.Draw()
            framer.GetYaxis().SetTitle('tight-to-loose ratio')
            framer.GetXaxis().SetTitle('p^{cone}_{T} [GeV]')
            h_pt_1f[i].Draw('same')
            pf.showlogoprelimsim('CMS')
            pf.showlumi(sample+'-'+ch)
            save(c_pt_1f, iso_cut, sample, ch)

            print '\n\tsingle-fakes done ...'
 
        if dfr:

            print '\n\tdrawing double fakes ...'

            cut_T = cuts + TIGHT ## UPDATED TO LIMIT JET-JUNK WITH LARGE DR
            cut_L = cuts + LOOSE ## UPDATED TO LIMIT JET-JUNK WITH LARGE DR

            n_entries             = t.GetEntries(cuts) 

            print '\n\t', sample, 'entries before selection:', N_ENTRIES 
            print '\t',sample, 'entries after cuts:', n_entries
            print '\n\t cuts: %s'%cuts
            print '\n\t TIGHT WP: %s\n' %TIGHT
            print '\n\t LOOSE WP: %s\n' %LOOSE
            print '\n\t LNT WP: %s\n' %LOOSENOTTIGHT

            h_pt_2f_L  = rt.TH1F('pt_cone_2f_L', 'pt_cone_2f_L',len(b_pt)-1,b_pt)

            h_pt_2f_T  = rt.TH1F('pt_cone_2f_T', 'pt_cone_2f_T',len(b_pt)-1,b_pt)

            t.Draw(PTCONE + ' >> pt_cone_2f_T', cut_T + ' & hnl_dr_12 < 0.8 & ' + twoFakes_sameJet)
            print '\tentries tight:', h_pt_2f_T.GetEntries()

            t.Draw(PTCONE + '>> pt_cone_2f_L' , cut_L + ' & hnl_dr_12 < 0.8 & ' + twoFakes_sameJet)
            print '\tentries loose:', h_pt_2f_L.GetEntries()

            print '\tdouble-fakes done'
      
            h_pt_2f.append(rt.TEfficiency(h_pt_2f_T, h_pt_2f_L))
            h_pt_2f[i].SetTitle('%s; p_{T}^{cone} [GeV]; tight-to-loose ratio (double fakes, same jet)'%sample)
            h_pt_2f[i].SetMarkerColor(rt.kGreen+i*2)
            h_pt_2f[i].SetFillColor(rt.kWhite)

            c_pt_2f = rt.TCanvas('ptCone_2f', 'ptCone_2f')
            framer.Draw()
            framer.GetYaxis().SetTitle('tight-to-loose ratio')
            framer.GetXaxis().SetTitle('p_{T}^{cone} [GeV]')
            h_pt_2f[i].Draw('same')
            pf.showlogoprelimsim('CMS')
            pf.showlumi(sample+'-'+ch)
            save(c_pt_2f, iso_cut, sample, ch)
 
#        if sample == 'DY':

        if sfr and dfr:

            c_pt_cmprd = rt.TCanvas('ptCone_cmprd', 'ptCone_cmprd')
            framer.Draw()
            framer.GetYaxis().SetTitle('tight-to-loose ratio')
            framer.GetXaxis().SetTitle('p_{T}^{cone} [GeV]')
            h_pt_1f[i].Draw('same')
            h_pt_1f[i].SetMarkerColor(rt.kRed+1+i)
            h_pt_2f[i].Draw('same')
            leg = rt.TLegend(0.57, 0.78, 0.80, 0.9)
            leg.AddEntry(h_pt_2f[i], 'double fakes')
            leg.AddEntry(h_pt_1f[i], 'single fakes ')
            leg.Draw()
            pf.showlumi(sample+'-'+ch)
            pf.showlogoprelimsim('CMS')
            save(c_pt_cmprd, iso_cut, sample, ch)

        i += 1

    if len(samples) > 1:

        rnch = len(samples)
#        if ch == 'mmm': rnch = 2

        if sfr:
            c_pt_1f = rt.TCanvas('ptCone_1f', 'ptCone_1f')
            framer.Draw()
            framer.GetYaxis().SetTitle('tight-to-loose ratio (single fakes)')
            framer.GetXaxis().SetTitle('p_{T}^{cone} [GeV]')
            leg = rt.TLegend(0.57, 0.78, 0.80, 0.9)
            for i in range(rnch):
                h_pt_1f[i].Draw('same')
                leg.AddEntry(h_pt_1f[i], h_pt_1f[i].GetTitle())
            leg.Draw()
        #    c_pt_1f.SetLogz()
            pf.showlogoprelimsim('CMS')
            save(c_pt_1f, iso_cut, 'cmbnd', ch)

        if dfr:
            c_pt_2f = rt.TCanvas('ptCone_2f', 'ptCone_2f')
            framer.Draw()
            framer.GetYaxis().SetTitle('tight-to-loose ratio (double fakes, same Jet)')
            framer.GetXaxis().SetTitle('p_{T}^{cone} [GeV]')
            leg = rt.TLegend(0.57, 0.78, 0.8, 0.9)
            for i in range(rnch): # forget WJ for now
                h_pt_2f[i].Draw('same')
                leg.AddEntry(h_pt_2f[i], h_pt_2f[i].GetTitle())
            leg.Draw()
            pf.showlogoprelimsim('CMS')
            save(c_pt_2f, iso_cut, 'cmbnd', ch)

    sys.stderr = sys.__stderr__
    sys.stdout = sys.__stdout__
    print '\n\t %s_%s_iso%s\t done'%(sample, ch, iso_str)

####################################################################################################

####################################################################################################
def measureTTLratio(isData=False,DISP=True,SPLIT=None,ch='eee'):
    iso_cut = 0.15
    iso_str = str(int(iso_cut * 100))
    sample_name = 'unknown'

    disp = ' & abs(l1_dz) < 2 & abs(l2_dz) < 2'
    dsp = ''
    if DISP == True:
        dsp = '_disp'
        disp += ' & hnl_2d_disp > 0.5'

    t = rt.TChain('tree')
#        fin = rt.TFile(sample) #inDir + TT_dir_m + suffix)
#        fin = rt.TFile(inDir + W_dir_m + suffix) # for debuggin: faster
#        t = fin.Get('tree')
#    sample_name = 'TTbar'
#        cut_T = twoFakes_sameJet_mm_sh + LepIDIsoPass(0, 't', iso_cut) + LepIDIsoPass(1, 'l', iso_cut) + LepIDIsoPass(2, 'l', iso_cut) + disp
#        cut_L = twoFakes_sameJet_mm_sh + LepIDIsoPass(0, 't', iso_cut) + bothLoose(iso_cut) + twoLepObjIsoleq1 + disp

    if ch == 'mmm': 

        if isData == True: 
           all_samples =  [inDir + data_m_B + suffix, inDir + data_m_C + suffix, inDir + data_m_D + suffix, inDir + data_m_F + suffix]

    if ch == 'eee': 

        TIGHT         =  ' & (l1_pt > 3 & l2_pt > 3 & l0_eid_cut_loose & l0_reliso05_04 < 0.15 & hnl_iso04_rel_rhoArea < 1 )'                     # & l1_eid_cut_loose & l2_eid_cut_loose )'
        LOOSE         =  ' & (l1_pt > 3 & l2_pt > 3 & l0_eid_cut_loose & l0_reliso05_04 < 0.15'                                                   # & l1_eid_cut_loose & l2_eid_cut_loose' 
        LOOSE         += ' & (l1_reliso05_04 > 0.15 | l2_reliso05_04 > 0.15) & hnl_iso04_rel_rhoArea < 1 )' 
        LOOSENOTTIGHT =  ' & (l1_pt > 3 & l2_pt > 3 & l0_eid_cut_loose & l0_reliso05_04 < 0.15 & l1_reliso05_04 < 0.15 & l2_reliso05_04 < 0.15 )' # & l1_eid_cut_loose & l2_eid_cut_loose )'

        twoFakes_sameJet_mm_sh = twoFakes_sameJet_ee_dr

        if isData == False: 
            all_samples = glob(inDirv2 + sigDir_eee + '*/HNLTreeProducer/tree.root')   
        if isData == True: 
            all_samples = [inDirv2 + dataDir_eee + suffix]
            sample_name = 'data'

    if ch == 'mee': 

        TIGHT         =  ' & (l1_pt > 3 & l2_pt > 3 & l0_id_t & l0_reliso_rho_04 < 0.15 & hnl_iso04_rel_rhoArea < 1 )'                     # & l1_eid_cut_loose & l2_eid_cut_loose )'
        LOOSE         =  ' & (l1_pt > 3 & l2_pt > 3 & l0_id_t & l0_reliso_rho_04 < 0.15'                                                   # & l1_eid_cut_loose & l2_eid_cut_loose' 
        LOOSE         += ' & (l1_reliso05_04 > 0.15 | l2_reliso05_04 > 0.15) & hnl_iso04_rel_rhoArea < 1 )' 
        LOOSENOTTIGHT =  ' & (l1_pt > 3 & l2_pt > 3 & l0_id_t & l0_reliso_rho_04 < 0.15 & l1_reliso05_04 < 0.15 & l2_reliso05_04 < 0.15 )' # & l1_eid_cut_loose & l2_eid_cut_loose )'

        twoFakes_sameJet_mm_sh = twoFakes_sameJet_ee_dr

        if isData == False: 
            all_samples = glob(inDirv2 + sigDir_mee + '*/HNLTreeProducer/tree.root')   
            sample_name = 'signal'

    for sample in all_samples: 
        t.Add(sample)


    if isData == False: 
        cut_T = twoFakes_sameJet_mm_sh + TIGHT + disp
        cut_L = twoFakes_sameJet_mm_sh + LOOSE + disp

    if isData == True: 
#        cut_T = 'abs(l1_jet_pt - l2_jet_pt) < 1 & nbj > 0 & hnl_2d_disp > 0.5 & abs(l1_dz) < 2 & abs(l2_dz) < 2' + LepIDIsoPass(0, 't', iso_cut) + LepIDIsoPass(1, 'l', iso_cut) + LepIDIsoPass(2, 'l', iso_cut)
#        cut_L = 'abs(l1_jet_pt - l2_jet_pt) < 1 & nbj > 0 & hnl_2d_disp > 0.5 & abs(l1_dz) < 2 & abs(l2_dz) < 2' + LepIDIsoPass(0, 't', iso_cut) + bothLoose(iso_cut) + twoLepObjIsoleq1 
        cut_T = 'abs(l1_jet_pt - l2_jet_pt) < 1 & hnl_dr_12 < 0.8 & nbj > 0 & hnl_2d_disp > 0.5 & abs(l1_dz) < 2 & abs(l2_dz) < 2' + TIGHT ## UPDATED TO LIMIT JET-JUNK WITH LARGE DR
        cut_L = 'abs(l1_jet_pt - l2_jet_pt) < 1 & hnl_dr_12 < 0.8 & nbj > 0 & hnl_2d_disp > 0.5 & abs(l1_dz) < 2 & abs(l2_dz) < 2' + LOOSE ## UPDATED TO LIMIT JET-JUNK WITH LARGE DR


    h_pt_eta_T = rt.TH2F('pt_eta_T','pt_eta_T',len(b_pt)-1,b_pt,len(b_eta)-1,b_eta)
    h_pt_eta_L = rt.TH2F('pt_eta_L','pt_eta_L',len(b_pt)-1,b_pt,len(b_eta)-1,b_eta)

    if SPLIT == 'geq':
        cut_T += ' & hnl_w_vis_m > 80'
        cut_L += ' & hnl_w_vis_m > 80'

    if SPLIT == 'leq':
        cut_T += ' & hnl_w_vis_m < 80'
        cut_L += ' & hnl_w_vis_m < 80'

    t.Draw('abs(hnl_hn_vis_eta) : ' + PTCONE + ' >> pt_eta_T', cut_T)
    t.Draw('abs(hnl_hn_vis_eta) : ' + PTCONE + ' >> pt_eta_L', cut_L)
    print 'tree entries T & L: ', t.GetEntries(cut_T), t.GetEntries(cut_L)

    print '%s iso%s ... double fakes done\nnumerator: %i, denominator: %i'%(sample_name, iso_str, h_pt_eta_T.GetEntries(), h_pt_eta_L.GetEntries())

#    h_pt_eta_d.Add(h_pt_eta_n) ## NOW BOTHLOOSE UPDATED, NO MORE ADDING NEEDED!

    c_pt_eta = rt.TCanvas('ptCone_eta', 'ptCone_eta')
    h_pt_eta_T.Divide(h_pt_eta_L)
    h_pt_eta_T.Draw('colz')
    h_pt_eta_T.SetTitle('; p_{T}^{cone} [GeV]; DiMuon |#eta|; tight-to-loose ratio')
    pf.showlogoprelimsim('CMS')
    pf.showTitle('TTL Ratio')
    save(c_pt_eta, iso_cut, 'TTL_' + sample_name, ch, '')

    # DO AGAIN WITH THREE DIFFERENT TEFFS TO GET ERROR
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
                   cut = twoFakes_sameJet_mm_sh + LepIDIsoPass(0, 't', iso_cut) + bothLoose(iso_cut) + twoLepObjIsoleq1 + disp )

        h,c = plot(tupel, var = 'hnl_m_12', name = '2fsJnw_m2l'+dsp, binsX = b_m, xtitle = 'm(#mu_{1}, #mu_{2})', 
               cut = twoFakes_sameJet_mm_sh + LepIDIsoPass(0, 't', iso_cut) + bothLoose(iso_cut) + twoLepObjIsoleq1 + disp )
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
                   cut = twoFakes_sameJet_mm_sh + LepIDIsoPass(0, 't', iso_cut) + bothLoose(iso_cut) + twoLepObjIsoleq1 + disp )
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
                    cut = two_fakes_mm_sh + '  &  !' + twoFakes_sameVtx_mm_sh, log=True)

        h, c = plot(tupel = tupel, var = 'l2_simType : l1_simType', name = 'simType_sameVtx',
                    binsX = b_st, binsY =  b_st, mode = 2, xtitle = '#simType(#mu_{1})', ytitle = 'simType(#mu_{2})', 
                    cut = two_fakes_mm_sh + '  &  ' + twoFakes_sameVtx_mm_sh, log=True)

        h, c = plot(tupel = tupel, var = Delta_R_l12 + ' : l2_simProdZ - l1_simProdZ', name = 'dZ_dR_sameVtxJet',
                    binsX = b_z, binsY =  b_dR, mode = 2, xtitle = '#DeltaZ(#mu_{1}, #mu_{2}) [cm]', ytitle = '#DeltaR(#mu_{1}, #mu_{2})', 
                    cut = twoFakes_sameVtxJet_mm_sh, log=True)

        h, c = plot(tupel = tupel, var = Delta_R_l12 + ' : l2_simProdZ - l1_simProdZ', name = 'dZ_dR_sameVtxdiffJet',
                    binsX = b_z, binsY =  b_dR, mode = 2, xtitle = '#DeltaZ(#mu_{1}, #mu_{2}) [cm]', ytitle = '#DeltaR(#mu_{1}, #mu_{2})', 
                    cut = twoFakes_sameVtx_mm_sh + ' & !' + sameJet, log=True)


        h, c = plot(tupel = tupel, var = Delta_R_l12, name = 'dR_sameVtxJet', binsX = b_dR, xtitle = '#DeltaR(#mu_{1}, #mu_{2})', cut = twoFakes_sameVtxJet_mm_sh + ' & hnl_2d_disp > 0.5', log=True)

        h, c = plot(tupel = tupel, var = Delta_R_l12, name = 'dR_sameVtxdiffJet', binsX = b_dR, xtitle = '#DeltaR(#mu_{1}, #mu_{2})', cut = twoFakes_sameVtx_mm_sh + '& !' + sameJet + ' & hnl_2d_disp > 0.5', log=True)

        h, c = plot(tupel = tupel, var = Delta_R_l12 + ' : l2_simProdZ - l1_simProdZ', name = 'dZ_dR_diffVtx',
                    binsX = b_z, binsY =  b_dR, mode = 2, xtitle = '#DeltaZ(#mu_{1}, #mu_{2}) [cm]', ytitle = '#DeltaR(#mu_{1}, #mu_{2})', 
                    cut = two_fakes_mm_sh + ' & !' + sameVtx + ' & hnl_2d_disp > 0.5', log=True)


        h, c = plot(tupel = tupel, var = 'abs(l2_simProdZ - l1_simProdZ)', name = 'dZ_sameJet', binsX = b_abs_z,
                    xtitle = '|#DeltaZ(#mu_{1}, #mu_{2})| [cm]', cut = twoFakes_sameJet_mm_sh + ' & hnl_2d_disp > 0.5', log=True)

        h, c = plot(tupel = tupel, var = 'abs(l2_simProdRho - l1_simProdRho)', name = 'dRho_sameJet', binsX = b_rho_crs, 
                    xtitle = '|#Delta#rho(#mu_{1}, #mu_{2})| [cm]', cut = twoFakes_sameJet_mm_sh + ' & hnl_2d_disp > 0.5', log=True)

        h, c = plot(tupel = tupel, var = 'abs(l2_simProdRho - l1_simProdRho) : abs(l2_simProdZ - l1_simProdZ)', name = 'dZ_dRho_sameJet',
                    binsX = b_abs_z, binsY =  b_rho_crs, mode = 2, xtitle = '|#DeltaZ(#mu_{1}, #mu_{2})| [cm]', ytitle = '|#Delta#rho(#mu_{1}, #mu_{2})| [cm]', 
                    cut = twoFakes_sameJet_mm_sh + ' & hnl_2d_disp > 0.5', log=True)


        h, c = plot(tupel = tupel, var = 'l2_simProdRho : l1_simProdRho', name = 'Rho_Rho_sameJet', cut = twoFakes_sameJet_mm_sh + ' & hnl_2d_disp > 0.5',
                    binsX = b_rho_crs, binsY =  b_rho_crs, mode = 2, xtitle = '#rho(#mu_{1}) [cm]', ytitle = '#rho(#mu_{2}) [cm]', log=True) 

        h, c = plot(tupel = tupel, var = 'l2_simProdZ : l1_simProdZ', name = 'Z_Z_sameJet', binsX = b_z, binsY = b_z, mode = 2,
                    xtitle = 'Z(#mu_{1}) [cm]', ytitle = 'Z(#mu_{2}) [cm]', cut = twoFakes_sameJet_mm_sh + ' & hnl_2d_disp > 0.5', log=True)
####################################################################################################
   
####################################################################################################
def checkpTdR():   
    t = rt.TChain('tree')

    t.Add(inDir + DYBB_dir_m + suffix)
    t.Add(inDir + DY50_dir_m + suffix)
    t.Add(inDir + DY50_ext_dir_m + suffix)
    t.Add(inDir + DY50_dir_m + suffix)
    t.Add(inDir + DY50_ext_dir_m + suffix)
 
#    t.Add(inDir + W_dir_m + suffix)
#    t.Add(inDir + W_ext_dir_m + suffix)

#    t.Add(inDir + TT_dir_m + suffix)

    cut_T   = 'hnl_2d_disp > 0.5 & abs(l1_dz) < 2 & abs(l2_dz) < 2' + TIGHT 
    cut_L   = 'hnl_2d_disp > 0.5 & abs(l1_dz) < 2 & abs(l2_dz) < 2' + LOOSE

    print t.GetEntries()
   
    h_pT_dR_iso    = rt.TH2F('pT_dR_iso','pT_dR_iso',len(b_pt_std)-1,b_pt_std,len(b_dR)-1,b_dR)
    h_pT_dR_noniso = rt.TH2F('pT_dR_noniso','pT_dR_noniso',len(b_pt_std)-1,b_pt_std,len(b_dR)-1,b_dR)

    t.Draw('hnl_dr_12:hnl_hn_vis_pt >> pT_dR_iso', cut_T)

    c_pT_dR_iso = rt.TCanvas('pt_dr_iso', 'pt_dr_iso')
    h_pT_dR_iso.SetTitle('; DiMuon p_{T} [GeV]; #DeltaR(#mu_{1}, #mu_{2}); Counts')
    h_pT_dR_iso.Draw('colz')
    pf.showlogoprelimsim('CMS')
    pf.showlumi('Tight')
    save(c_pT_dR_iso, 0.15, 'DDE_DY', 'mu', '')

    t.Draw('hnl_dr_12:hnl_hn_vis_pt >> pT_dR_noniso', cut_L)

    c_pT_dR_noniso = rt.TCanvas('pt_dr_noniso', 'pt_dr_noniso')
    h_pT_dR_noniso.SetTitle('; DiMuon p_{T} [GeV]; #DeltaR(#mu_{1}, #mu_{2}); Counts')
    h_pT_dR_noniso.Draw('colz')
    pf.showlogoprelimsim('CMS')
    pf.showlumi('Loose')
    save(c_pT_dR_noniso, 0.15, 'DDE_DY', 'mu', '')
####################################################################################################
   
####################################################################################################
def checkpTCone():
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

        b_pt  = np.arange(5.,105,5)
        b_dR  = np.arange(0.,0.825,0.025)

        h, c = plot(tupel = tupel, 
                    name = 'dR_pt_NoIso', 
                    var = 'hnl_dr_12 : hnl_hn_vis_pt', 
                    binsX = b_pt, binsY =  b_dR, mode = 2, iso = 0.15, 
                    xtitle = 'DiMuon p_{T} [GeV]', 
                    ytitle = '#DeltaR (#mu_{1}, #mu_{2})', 
                    cut = '1' + LepIDIsoFail(1, 'l', iso_cut) + LepIDIsoFail(2, 'l', iso_cut) + twoLepObjIsoleq1 + ' & hnl_2d_disp > 0.5 & abs(l1_dz) < 0.2 & abs(l2_dz) < 0.2') # + ' & ' + twoFakes_sameJet)

        h, c = plot(tupel = tupel, 
                    name = 'dR_pt_Iso', 
                    var = 'hnl_dr_12 : hnl_hn_vis_pt', 
                    binsX = b_pt, binsY =  b_dR, mode = 2, iso = 0.15,
                    xtitle = 'DiMuon p_{T} [GeV]', 
                    ytitle = '#DeltaR (#mu_{1}, #mu_{2})', 
                    cut = '1' + LepIDIsoPass(1, 'l', iso_cut) + LepIDIsoPass(2, 'l', iso_cut) + ' & hnl_2d_disp > 0.5 & abs(l1_dz) < 0.2 & abs(l2_dz) < 0.2') # + ' & ' + twoFakes_sameJet)

def notdo(): #former part of checkpTCone
        h, c = plot(tupel = tupel, 
                    name = 'ptJet_ptCone_sameJet_NoIso', 
                    var = ptCone2F_dimu(0.15) + ': l1_jet_pt', #ptCone2F(iso_cut) + ': l1_jet_pt',
                    binsX = b_pt, binsY =  b_pt, mode = 2, iso = 0.15, 
                    xtitle = '#mu_{1} Jet p_{T} [GeV]', 
                    ytitle = 'p_{T}^{cone} [GeV]', 
                    cut = twoFakes_sameJet_mm_sh + LepIDIsoFail(1, 't', iso_cut) + LepIDIsoFail(2, 't', iso_cut) + twoLepObjIsoleq1)

        h, c = plot(tupel = tupel, 
                    name = 'ptJet_ptCone_sameJet_Iso', 
                    var = ptCone2F_dimu(0.15) + ': l1_jet_pt', #ptCone2F(iso_cut) + ': l1_jet_pt',
                    binsX = b_pt, binsY =  b_pt, mode = 2, iso = 0.15, 
                    xtitle = '#mu_{1} Jet p_{T} [GeV]', 
                    ytitle = 'p_{T}^{cone} [GeV]', 
                    cut = twoFakes_sameJet_mm_sh + LepIDIsoPass(1, 't', iso_cut) + LepIDIsoPass(2, 't', iso_cut))
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
#    print 'cut: ', twoFakes_sameJet_mm_sh + LepIDIsoPass(1, 't', iso_cut) + LepIDIsoPass(2, 't', iso_cut)
##   t.Draw( 'hnl_hn_vis_pt >> obs_pt', twoFakes_sameJet_mm_sh + LepIDIsoPass(1, 't', iso_cut) + LepIDIsoPass(2, 't', iso_cut))
    t.Draw( 'hnl_hn_vis_pt >> obs_pt', 
    'abs(l1_jet_pt - l2_jet_pt) < 1 & hnl_w_vis_m > 80 & nbj == 0 & hnl_2d_disp > 0.5 ' + LepIDIsoPass(0, 't', iso_cut) + LepIDIsoPass(1, 't', iso_cut) + LepIDIsoPass(2, 't', iso_cut) ) # DATA !
    print 'pt done'
##   t.Draw( 'hnl_2d_disp >> obs_2disp', twoFakes_sameJet_mm_sh + LepIDIsoPass(1, 't', iso_cut) + LepIDIsoPass(2, 't', iso_cut))
    t.Draw( 'hnl_2d_disp >> obs_2disp', 
    'abs(l1_jet_pt - l2_jet_pt) < 1 & hnl_w_vis_m > 80 & nbj == 0 & hnl_2d_disp > 0.5 ' + LepIDIsoPass(0, 't', iso_cut) + LepIDIsoPass(1, 't', iso_cut) + LepIDIsoPass(2, 't', iso_cut) ) # DATA !
    print '2disp done'
##   t.Draw( 'hnl_m_12 >> obs_m_dimu', twoFakes_sameJet_mm_sh + LepIDIsoPass(1, 't', iso_cut) + LepIDIsoPass(2, 't', iso_cut))
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
##           '( ' + twoFakes_sameJet_mm_sh + LepIDIsoFail(1, 't', iso_cut) + LepIDIsoFail(2, 't', iso_cut) + ptEtaBin(ipt,ieta) + twoLepObjIsoleq1 + ') * %f'%weight_tt[ieta][ipt])
            '( abs(l1_jet_pt - l2_jet_pt) < 1 & hnl_w_vis_m > 80 & nbj == 0 & hnl_2d_disp > 0.5 ' + LepIDIsoPass(0, 't', iso_cut) + LepIDIsoFail(1, 't', iso_cut) + LepIDIsoFail(2, 't', iso_cut) + ptEtaBin(ipt,ieta) + twoLepObjIsoleq1 + ') * %f'%weight_data[ieta][ipt]) # DATA!

            t.Draw( 'hnl_2d_disp >>+ weighed_2disp',
##           '( ' + twoFakes_sameJet_mm_sh + LepIDIsoFail(1, 't', iso_cut) + LepIDIsoFail(2, 't', iso_cut) + ptEtaBin(ipt,ieta) + twoLepObjIsoleq1 + ') * %f'%weight_tt[ieta][ipt])
            '( abs(l1_jet_pt - l2_jet_pt) < 1 & hnl_w_vis_m > 80 & nbj == 0 & hnl_2d_disp > 0.5 ' + LepIDIsoPass(0, 't', iso_cut) + LepIDIsoFail(1, 't', iso_cut) + LepIDIsoFail(2, 't', iso_cut) + ptEtaBin(ipt,ieta) + twoLepObjIsoleq1 + ') * %f'%weight_data[ieta][ipt]) # DATA!

            t.Draw( 'hnl_m_12  >>+ weighed_m_dimu',
##           '( ' + twoFakes_sameJet_mm_sh + LepIDIsoFail(1, 't', iso_cut) + LepIDIsoFail(2, 't', iso_cut) + ptEtaBin(ipt,ieta) + twoLepObjIsoleq1 + ') * %f'%weight_tt[ieta][ipt])
            '( abs(l1_jet_pt - l2_jet_pt) < 1 & hnl_w_vis_m > 80 & nbj == 0 & hnl_2d_disp > 0.5 ' + LepIDIsoPass(0, 't', iso_cut) + LepIDIsoFail(1, 't', iso_cut) + LepIDIsoFail(2, 't', iso_cut) + ptEtaBin(ipt,ieta) + twoLepObjIsoleq1 + ') * %f'%weight_data[ieta][ipt]) # DATA!

            t.Draw( 'hnl_w_vis_m  >>+ weighed_m_triL',
            '( abs(l1_jet_pt - l2_jet_pt) < 1 & hnl_w_vis_m > 80 & nbj == 0 & hnl_2d_disp > 0.5 ' + LepIDIsoPass(0, 't', iso_cut) + LepIDIsoFail(1, 't', iso_cut) + LepIDIsoFail(2, 't', iso_cut) + ptEtaBin(ipt,ieta) + twoLepObjIsoleq1 + ') * %f'%weight_data[ieta][ipt]) # DATA!

    c_pt = rt.TCanvas('pt', 'pt')
    weighed_pt.SetMarkerColor(rt.kGreen+2)
    weighed_pt.SetTitle('; p_{T}^{cone} [GeV]; Counts')
    observed_pt.SetTitle('; p_{T}^{cone} [GeV]; Counts')
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
def applyTTL(isData=False, VLD=True, SPLIT=None):
    iso_cut = 0.15
    iso_str = str(int(iso_cut * 100))
    ch = 'mu'
    ch = 'mee'
    sample = 'data'
    
    if isData == False:
#        fin = rt.TFile(treeDir + 'tree_fr_liteTTbar.root') #TODO CHANGE TO FULL
#        fin = rt.TFile(tempDir + 'tree_fr_DR_TTbar.root') 
#        t = fin.Get('tree')
        t = rt.TChain('tree')

        if ch == 'eee': 

            LOOSE           =  DFR_LOOSE_EEE          
            LOOSENOTTIGHT   =  DFR_LOOSENOTTIGHT_EEE  
            TIGHT           =  DFR_TIGHT_EEE          

            all_samples = glob(inDirv2 + sigDir_eee + '*/HNLTreeProducer/tree.root')   

        if ch == 'mmm':

            LOOSE           =  DFR_LOOSE_MMM          
            LOOSENOTTIGHT   =  DFR_LOOSENOTTIGHT_MMM  
            TIGHT           =  DFR_TIGHT_MMM          

            all_samples = glob(tempDir + 'tree_fr_DR_TTbar_slice*.root')
            # sample = 'TTbar'

        if ch == 'mee': 

            LOOSE           =  DFR_LOOSE_MEE          
            LOOSENOTTIGHT   =  DFR_LOOSENOTTIGHT_MEE  
            TIGHT           =  DFR_TIGHT_MEE          

            all_samples = glob(inDirv2 + sigDir_mee + '*/HNLTreeProducer/tree.root')   

        for sample in all_samples: 
            t.Add(sample)

        cut_T     = twoFakes_sameJet_mm_sh + ' & hnl_2d_disp > 0.5 & abs(l1_dz) < 2 & abs(l2_dz) < 2' + TIGHT 
#        cut_T     += LepIDIsoPass(0, 't', iso_cut) + LepIDIsoPass(1, 'l', iso_cut) + LepIDIsoPass(2, 'l', iso_cut)
        cut_L   = twoFakes_sameJet_mm_sh + ' & hnl_2d_disp > 0.5 & abs(l1_dz) < 2 & abs(l2_dz) < 2' + LOOSE
#        cut_L  += LepIDIsoPass(0, 't', iso_cut) + LepIDIsoFail(1, 'l', iso_cut) + LepIDIsoFail(2, 'l', iso_cut) + twoLepObjIsoleq1
#        cut_L  += LepIDIsoPass(0, 't', iso_cut) + bothLoose(iso_cut) + twoLepObjIsoleq1
        cut_LNT = twoFakes_sameJet_mm_sh + ' & hnl_2d_disp > 0.5 & abs(l1_dz) < 2 & abs(l2_dz) < 2' + LOOSENOTTIGHT

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
        show = pf.showlogopreliminary()
 
    ### VALIDATE
    if VLD == True:
        cut_T   = cut_T_VLD
        cut_LNT = cut_LNT_VLD

    ### APPLY
    if VLD == False:
        cut_T   = cut_T_APL
        cut_LNT = cut_LNT_APL

    if SPLIT == 'leq':
        cut_T   += ' & ' + PTCONE + ' < 25'
        cut_LNT += ' & ' + PTCONE + ' < 25'

    if SPLIT == 'geq':
        cut_T   += ' & ' + PTCONE + ' > 25'
        cut_LNT += ' & ' + PTCONE + ' > 25'

    ## apply Z veto on all OS combinations:
    #cut_T   += ' & ' + Z_veto
    #cut_LNT += ' & ' + Z_veto

    ## apply cut on vtx fitting quality
    cut_T   += ' & sv_prob > 0.01'
    cut_LNT += ' & sv_prob > 0.01'

    print '\n\tcut T:', cut_T, '\n\tcut LNT:', cut_LNT

    weighed_pt         = rt.TH1F('weighed_pt',         'weighed_pt',        len(b_pt)-1, b_pt)
    weighed_dr_12      = rt.TH1F('weighed_dr_12',      'weighed_dr_12',     len(b_dR)-1, b_dR)
    weighed_2disp      = rt.TH1F('weighed_2disp',      'weighed_2disp',     len(b_2d)-1, b_2d)
    weighed_2disp_sig  = rt.TH1F('weighed_2disp_sig',  'weighed_2disp_sig', len(b_2d_sig)-1, b_2d_sig)
    weighed_m_dimu     = rt.TH1F('weighed_m_dimu',     'weighed_m_dimu',    len(b_m)-1, b_m)
    weighed_M_dimu     = rt.TH1F('weighed_M_dimu',     'weighed_M_dimu',    len(b_M)-1, b_M)
    weighed_M_01       = rt.TH1F('weighed_M_01',       'weighed_M_01',      len(b_M)-1, b_M)
    weighed_M_02       = rt.TH1F('weighed_M_02',       'weighed_M_02',      len(b_M)-1, b_M)
    weighed_m_triL     = rt.TH1F('weighed_m_triL',     'weighed_m_triL',    len(b_M)-1, b_M)
    observed_pt        = rt.TH1F('obs_pt',             'obs_pt',            len(b_pt)-1, b_pt)
    observed_dr_12     = rt.TH1F('obs_dr_12',          'obs_dr_12',         len(b_dR)-1, b_dR)
    observed_2disp     = rt.TH1F('obs_2disp',          'obs_2disp',         len(b_2d)-1, b_2d)
    observed_2disp_sig = rt.TH1F('obs_2disp_sig',      'obs_2disp_sig',     len(b_2d_sig)-1, b_2d_sig)
    observed_m_dimu    = rt.TH1F('obs_m_dimu',         'obs_m_dimu',        len(b_m)-1, b_m)
    observed_M_dimu    = rt.TH1F('obs_M_dimu',         'obs_M_dimu',        len(b_M)-1, b_M)
    observed_M_01      = rt.TH1F('obs_M_01',           'obs_M_01',          len(b_M)-1, b_M)
    observed_M_02      = rt.TH1F('obs_M_02',           'obs_M_02',          len(b_M)-1, b_M)
    observed_m_triL    = rt.TH1F('obs_m_triL',         'obs_m_triL',        len(b_M)-1, b_M)
                                                       
    print '\n\tentries:', t.GetEntriesFast()           
                                                       
    print '\tdrawing M_02 ...'

    t.Draw( 'hnl_m_02 >> obs_M_02', cut_T )  
    print '\tobs M_02 done'

    t.Draw( 'hnl_m_02  >> weighed_M_02',             '( ' + cut_LNT + ' ) * ( weight_fr/ (1 - weight_fr) )' )
    print '\tweighed M_02 done'

    c_M_02 = rt.TCanvas('M_02', 'M_02')
    weighed_M_02.SetLineColor(rt.kGreen+2); weighed_M_02.SetLineWidth(2); weighed_M_02.SetMarkerStyle(0)
    weighed_M_02.SetTitle('; m(#mu_{0},  #mu_{2}) [GeV]; Counts')
    observed_M_02.SetTitle('; m(#mu_{0},  #mu_{2}) [GeV]; Counts')
    observed_M_02.SetMarkerColor(rt.kMagenta+2)
    observed_M_02.Draw()
    weighed_M_02.Draw('histsame')
    leg = rt.TLegend(0.57, 0.78, 0.80, 0.9)
    leg.AddEntry(observed_M_02, 'observed')
    leg.AddEntry(weighed_M_02, 'expected')
    leg.Draw()
    show
    save(c_M_02, iso_cut, 'DDE_' + sample, ch, '')

    print '\tdrawing M_01 ...'

    t.Draw( 'hnl_m_01 >> obs_M_01', cut_T )  
    print '\tobs mass_01 done'

    t.Draw( 'hnl_m_01  >> weighed_M_01',             '( ' + cut_LNT + ' ) * ( weight_fr/ (1 - weight_fr) )' )
    print '\tweighed M_01 done'

    c_M_01 = rt.TCanvas('M_01', 'M_01')
    weighed_M_01.SetLineColor(rt.kGreen+2); weighed_M_01.SetLineWidth(2); weighed_M_01.SetMarkerStyle(0)
    weighed_M_01.SetTitle('; m(#mu_{0},  #mu_{1}) [GeV]; Counts')
    observed_M_01.SetTitle('; m(#mu_{0},  #mu_{1}) [GeV]; Counts')
    observed_M_01.SetMarkerColor(rt.kMagenta+2)
    observed_M_01.Draw()
    weighed_M_01.Draw('histsame')
    leg = rt.TLegend(0.57, 0.78, 0.80, 0.9)
    leg.AddEntry(observed_M_01, 'observed')
    leg.AddEntry(weighed_M_01, 'expected')
    leg.Draw()
    show
    save(c_M_01, iso_cut, 'DDE_' + sample, ch, '')

    print '\tdrawing dr_12 ...'

    t.Draw( 'hnl_dr_12 >> obs_dr_12', cut_T )  
    print '\tobs dr_12 done'

    t.Draw( 'hnl_dr_12  >> weighed_dr_12',             '( ' + cut_LNT + ' ) * ( weight_fr/ (1 - weight_fr) )' )
    print '\tweighed dr_12 done'

    c_dr_12 = rt.TCanvas('dr_12', 'dr_12')
    weighed_dr_12.SetLineColor(rt.kGreen+2); weighed_dr_12.SetLineWidth(2); weighed_dr_12.SetMarkerStyle(0)
    weighed_dr_12.SetTitle('; #DeltaR(#mu_{1}, #mu_{2}); Counts')
    observed_dr_12.SetTitle('; #DeltaR(#mu_{1}, #mu_{2}); Counts')
    observed_dr_12.SetMarkerColor(rt.kMagenta+2)
    observed_dr_12.Draw()
    weighed_dr_12.Draw('histsame')
    leg = rt.TLegend(0.57, 0.78, 0.80, 0.9)
    leg.AddEntry(observed_dr_12, 'observed')
    leg.AddEntry(weighed_dr_12, 'expected')
    leg.Draw()
    show
    save(c_dr_12, iso_cut, 'DDE_' + sample, ch, '')

    print '\n\tdrawing pt ...'

    t.Draw( PTCONE + ' >> obs_pt', cut_T ) 
#    t.Draw( 'hnl_hn_vis_pt >> obs_pt', cut_T ) 
    print '\tobs pt done'

    t.Draw( PTCONE + ' >> weighed_pt',  '( ' + cut_LNT + ' ) * ( weight_fr/ (1 - weight_fr) )' )
#    t.Draw( ptCone2F_dimu(iso_cut) + '>> weighed_pt',  '( ' + cut_LNT + ' ) * ( weight_fr/ (1 - weight_fr) )' )
    print '\tweighed pt done'

    c_pt = rt.TCanvas('pt', 'pt')
    weighed_pt.SetLineColor(rt.kGreen+2); weighed_pt.SetLineWidth(2); weighed_pt.SetMarkerStyle(0)
    weighed_pt.SetTitle('; p_{T}^{cone} [GeV]; Counts')
    observed_pt.SetTitle('; p_{T}^{cone} [GeV]; Counts')
    observed_pt.SetMarkerColor(rt.kMagenta+2)
    observed_pt.Draw()
    weighed_pt.Draw('histsame')
    leg = rt.TLegend(0.57, 0.78, 0.80, 0.9)
    leg.AddEntry(observed_pt, 'observed')
    leg.AddEntry(weighed_pt, 'expected')
    leg.Draw()
    show
    save(c_pt, iso_cut, 'DDE_' + sample, ch, '')

    print '\tdrawing 2disp ...'

    t.Draw( 'hnl_2d_disp >> obs_2disp', cut_T )   
    print '\tobs 2disp done'

    t.Draw( 'hnl_2d_disp >> weighed_2disp',            '( ' + cut_LNT + ' ) * ( weight_fr/ (1 - weight_fr) )' )
    print '\tweighed 2disp done'

    c_2disp = rt.TCanvas('2disp', '2disp')
    weighed_2disp.SetLineColor(rt.kGreen+2); weighed_2disp.SetLineWidth(2); weighed_2disp.SetMarkerStyle(0)
    weighed_2disp.SetTitle(';2D displacement [cm]; Counts')
    observed_2disp.SetTitle(';2D displacement [cm]; Counts')
    observed_2disp.SetMarkerColor(rt.kMagenta+2)
    observed_2disp.Draw()
    weighed_2disp.Draw('histsame')
    leg = rt.TLegend(0.57, 0.78, 0.80, 0.9)
    leg.AddEntry(observed_2disp, 'observed')
    leg.AddEntry(weighed_2disp, 'expected')
    leg.Draw()
    show
    save(c_2disp, iso_cut, 'DDE_' + sample, ch, '')

    print '\tdrawing m_dimu ...'

    t.Draw( 'hnl_m_12 >> obs_m_dimu', cut_T )  
    print '\tobs m_dimu done'

    t.Draw( 'hnl_m_12  >> weighed_m_dimu',             '( ' + cut_LNT + ' ) * ( weight_fr/ (1 - weight_fr) )' )
    print '\tweighed m_dimu done'

    c_m_dimu = rt.TCanvas('m_dimu', 'm_dimu')
    weighed_m_dimu.SetLineColor(rt.kGreen+2); weighed_m_dimu.SetLineWidth(2); weighed_m_dimu.SetMarkerStyle(0)
    weighed_m_dimu.SetTitle('; m(#mu_{1},  #mu_{2}) [GeV]; Counts')
    observed_m_dimu.SetTitle('; m(#mu_{1},  #mu_{2}) [GeV]; Counts')
    observed_m_dimu.SetMarkerColor(rt.kMagenta+2)
    observed_m_dimu.Draw()
    weighed_m_dimu.Draw('histsame')
    leg = rt.TLegend(0.57, 0.78, 0.80, 0.9)
    leg.AddEntry(observed_m_dimu, 'observed')
    leg.AddEntry(weighed_m_dimu, 'expected')
    leg.Draw()
    show
    save(c_m_dimu, iso_cut, 'DDE_' + sample, ch, '')

    print '\tdrawing M_dimu ...'

    t.Draw( 'hnl_m_12 >> obs_M_dimu', cut_T )  
    print '\tobs M_dimu done'

    t.Draw( 'hnl_m_12  >> weighed_M_dimu',             '( ' + cut_LNT + ' ) * ( weight_fr/ (1 - weight_fr) )' )
    print '\tweighed M_dimu done'

    c_M_dimu = rt.TCanvas('M_dimu', 'M_dimu')
    weighed_M_dimu.SetLineColor(rt.kGreen+2); weighed_M_dimu.SetLineWidth(2); weighed_M_dimu.SetMarkerStyle(0)
    weighed_M_dimu.SetTitle('; m(#mu_{1},  #mu_{2}) [GeV]; Counts')
    observed_M_dimu.SetTitle('; m(#mu_{1},  #mu_{2}) [GeV]; Counts')
    observed_M_dimu.SetMarkerColor(rt.kMagenta+2)
    observed_M_dimu.Draw()
    weighed_M_dimu.Draw('histsame')
    leg = rt.TLegend(0.57, 0.78, 0.80, 0.9)
    leg.AddEntry(observed_M_dimu, 'observed')
    leg.AddEntry(weighed_M_dimu, 'expected')
    leg.Draw()
    show
    save(c_M_dimu, iso_cut, 'DDE_' + sample, ch, '')

    print '\tdrawing m_triL ...'

    t.Draw( 'hnl_w_vis_m >> obs_m_triL', cut_T )  
    print '\tobs m_triL done'

    t.Draw( 'hnl_w_vis_m >> weighed_m_triL',           '( ' + cut_LNT + ' ) * ( weight_fr/ (1 - weight_fr) )' )
    print '\tweighed m_triL done'

    c_m_triL = rt.TCanvas('m_triL', 'm_triL')
    weighed_m_triL.SetLineColor(rt.kGreen+2); weighed_m_triL.SetLineWidth(2); weighed_m_triL.SetMarkerStyle(0)
    weighed_m_triL.SetTitle('; m(#mu_{0}, #mu_{1},  #mu_{2}) [GeV]; Counts')
    observed_m_triL.SetTitle('; m(#mu_{0}, #mu_{1},  #mu_{2}) [GeV]; Counts')
    observed_m_triL.SetMarkerColor(rt.kMagenta+2)
    observed_m_triL.Draw()
    weighed_m_triL.Draw('histsame')
    leg = rt.TLegend(0.57, 0.78, 0.80, 0.9)
    leg.AddEntry(observed_m_triL, 'observed')
    leg.AddEntry(weighed_m_triL, 'expected')
    leg.Draw()
    show
    save(c_m_triL, iso_cut, 'DDE_' + sample, ch, '')

    set_trace()

    print '\tdrawing 2disp/sig ...'                    

    t.Draw( 'hnl_2d_disp_sig >> obs_2disp_sig', cut_T )   
    print '\tobs 2disp/sig done'

    t.Draw( 'hnl_2d_disp_sig >> weighed_2disp_sig',            '( ' + cut_LNT + ' ) * ( weight_fr/ (1 - weight_fr) )' )
    print '\tweighed 2disp/sig done'

    c_2disp_sig = rt.TCanvas('2disp_sig', '2disp_sig')
    weighed_2disp_sig.SetLineColor(rt.kGreen+2); weighed_2disp_sig.SetLineWidth(2); weighed_2disp_sig.SetMarkerStyle(0)
    weighed_2disp_sig.SetTitle('; L_{2d}/#sigma ; Counts')
    observed_2disp_sig.SetTitle('; L_{2d}/#sigma; Counts')
    observed_2disp_sig.SetMarkerColor(rt.kMagenta+2)
    observed_2disp_sig.Draw()
    weighed_2disp_sig.Draw('histsame')
    leg = rt.TLegend(0.57, 0.78, 0.80, 0.9)
    leg.AddEntry(observed_2disp_sig, 'observed')
    leg.AddEntry(weighed_2disp_sig, 'expected')
    leg.Draw()
    show
    save(c_2disp_sig, iso_cut, 'DDE_' + sample, ch, '')

def ptEtaBin(ipt, ieta):
    iso_cut = 0.15
    ptlow = b_pt[ipt]; pthigh = b_pt[ipt+1]
    etalow = b_eta[ieta]; etahigh = b_eta[ieta+1]
    cut = ' & {ptcone} < {pthi} & {ptcone} > {ptlo} & {eta} < {etahi} & {eta} > {etalo}'.format( ptcone = ptCone2F_dimu(iso_cut), ptlo = ptlow, pthi = pthigh, eta = 'abs(hnl_hn_vis_eta)', etahi=etahigh, etalo = etalow)
    return cut

def checkpTdRinFRgeq25():
    fin = rt.TFile(treeDir + 'tree_fr_DR_data_v2.root')
    t = fin.Get('tree')

    cut_T   = 'abs(l1_jet_pt - l2_jet_pt) < 1 & hnl_dr_12 < 0.8 & hnl_w_vis_m > 80 & nbj == 0 & hnl_2d_disp > 0.5 & abs(l1_dz) < 2 & abs(l2_dz) < 2' + TIGHT
    cut_L   = 'abs(l1_jet_pt - l2_jet_pt) < 1 & hnl_dr_12 < 0.8 & hnl_w_vis_m > 80 & nbj == 0 & hnl_2d_disp > 0.5 & abs(l1_dz) < 2 & abs(l2_dz) < 2' + LOOSE
    cut_LNT = 'abs(l1_jet_pt - l2_jet_pt) < 1 & hnl_dr_12 < 0.8 & hnl_w_vis_m > 80 & nbj == 0 & hnl_2d_disp > 0.5 & abs(l1_dz) < 2 & abs(l2_dz) < 2' + LOOSENOTTIGHT

    cut_T   += ' & ' + PTCONE + ' > 25'
    cut_LNT += ' & ' + PTCONE + ' > 25'

    observed_pt_dr_12 = rt.TH2F('obs_pt_dr', 'obs_pt_dr', len(b_pt)-1, b_pt, len(b_dR)-1, b_dR)

    t.Draw( 'hnl_dr_12:' + PTCONE + ' >> obs_pt_dr', cut_T )

    c_pt_dr = rt.TCanvas('obs_pt_dr','obs_pt_dr'); c_pt_dr.cd()
    observed_pt_dr_12.SetTitle(';p_{T}^{cone} [GeV]; #DeltaR(#mu_{1}, #mu_{2});Counts')
    observed_pt_dr_12.Draw('colztext')
    pf.showlogopreliminary()
    c_pt_dr.Modified(); c_pt_dr.Update()
    
def checkpTpTinFRgeq25():
    fin = rt.TFile(treeDir + 'tree_fr_DR_data_v2.root')
    t = fin.Get('tree')

    cut_T   = 'abs(l1_jet_pt - l2_jet_pt) < 1 & hnl_dr_12 < 0.8 & hnl_w_vis_m > 80 & nbj == 0 & hnl_2d_disp > 0.5 & abs(l1_dz) < 2 & abs(l2_dz) < 2' + TIGHT
    cut_L   = 'abs(l1_jet_pt - l2_jet_pt) < 1 & hnl_dr_12 < 0.8 & hnl_w_vis_m > 80 & nbj == 0 & hnl_2d_disp > 0.5 & abs(l1_dz) < 2 & abs(l2_dz) < 2' + LOOSE
    cut_LNT = 'abs(l1_jet_pt - l2_jet_pt) < 1 & hnl_dr_12 < 0.8 & hnl_w_vis_m > 80 & nbj == 0 & hnl_2d_disp > 0.5 & abs(l1_dz) < 2 & abs(l2_dz) < 2' + LOOSENOTTIGHT

    cut_T   += ' & ' + PTCONE + ' > 25'
    cut_LNT += ' & ' + PTCONE + ' > 25'

    observed_pt_pt = rt.TH2F('obs_pt_pt', 'obs_pt_pt', len(b_pt)-1, b_pt, len(b_pt)-1, b_pt)

    t.Draw( 'l2_pt:l1_pt >> obs_pt_pt', cut_T )

    c_pt_pt = rt.TCanvas('obs_pt_pt','obs_pt_pt'); c_pt_pt.cd()
    observed_pt_pt.SetTitle(';p_{T}(#mu_{1}) [GeV]; p_{T}(#mu_{2}) [GeV]; Counts')
    observed_pt_pt.Draw('colztext')
    pf.showlogopreliminary()
    c_pt_pt.Modified(); c_pt_pt.Update()
 
    save(c_pt_pt, 0.15, 'DDE_data', 'mu', '') 
    
def checkDiMsChi2inFRgeq25():
    fin = rt.TFile(treeDir + 'tree_fr_DR_data_v2.root')
    t = fin.Get('tree')

    cut_T   = 'abs(l1_jet_pt - l2_jet_pt) < 1 & hnl_dr_12 < 0.8 & hnl_w_vis_m > 80 & nbj == 0 & hnl_2d_disp > 0.5 & abs(l1_dz) < 2 & abs(l2_dz) < 2' + TIGHT
    cut_L   = 'abs(l1_jet_pt - l2_jet_pt) < 1 & hnl_dr_12 < 0.8 & hnl_w_vis_m > 80 & nbj == 0 & hnl_2d_disp > 0.5 & abs(l1_dz) < 2 & abs(l2_dz) < 2' + LOOSE
    cut_LNT = 'abs(l1_jet_pt - l2_jet_pt) < 1 & hnl_dr_12 < 0.8 & hnl_w_vis_m > 80 & nbj == 0 & hnl_2d_disp > 0.5 & abs(l1_dz) < 2 & abs(l2_dz) < 2' + LOOSENOTTIGHT

    cut_T   += ' & ' + PTCONE + ' > 25'
    cut_LNT += ' & ' + PTCONE + ' > 25'

    observed_m01_chi2 = rt.TH2F('obs_m01_chi2', 'obs_m01_chi2',len(b_M)-1, b_M,len(b_chi2)-1, b_chi2)
    observed_m02_chi2 = rt.TH2F('obs_m02_chi2', 'obs_m02_chi2',len(b_M)-1, b_M,len(b_chi2)-1, b_chi2)
    observed_m12_chi2 = rt.TH2F('obs_m12_chi2', 'obs_m12_chi2',len(b_M)-1, b_M,len(b_chi2)-1, b_chi2)

    t.Draw( 'sv_prob:hnl_m_01 >> obs_m01_chi2', cut_T )

    c_m01_chi2 = rt.TCanvas('obs_m01_chi2','obs_m01_chi2'); c_m01_chi2.cd()
    observed_m01_chi2.SetTitle(';m(#mu_{0},#mu_{1}) [GeV]; SV probability; Counts')
    observed_m01_chi2.Draw('colz')
    pf.showlogopreliminary()
    c_m01_chi2.Modified(); c_m01_chi2.Update()
    save(c_m01_chi2, 0.15, 'DDE_data', 'mu', '') 

    t.Draw( 'sv_prob:hnl_m_02 >> obs_m02_chi2', cut_T )

    c_m02_chi2 = rt.TCanvas('obs_m02_chi2','obs_m02_chi2'); c_m02_chi2.cd()
    observed_m02_chi2.SetTitle(';m(#mu_{0},#mu_{2}) [GeV]; SV probability; Counts')
    observed_m02_chi2.Draw('colz')
    pf.showlogopreliminary()
    c_m02_chi2.Modified(); c_m02_chi2.Update()
    save(c_m02_chi2, 0.15, 'DDE_data', 'mu', '') 

    t.Draw( 'sv_prob:hnl_m_12 >> obs_m12_chi2', cut_T )

    c_m12_chi2 = rt.TCanvas('obs_m12_chi2','obs_m12_chi2'); c_m12_chi2.cd()
    observed_m12_chi2.SetTitle(';m(#mu_{1},#mu_{2}) [GeV]; SV probability; Counts')
    observed_m12_chi2.Draw('colz')
    pf.showlogopreliminary()
    c_m12_chi2.Modified(); c_m12_chi2.Update()
    save(c_m12_chi2, 0.15, 'DDE_data', 'mu', '') 
####################################################################################################

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

def save(knvs, iso=0, sample='', ch='', eta=''):
    if iso == 0: iso_str = '' 
    if iso != 0: iso_str = str(int(iso * 100))
    knvs.GetFrame().SetLineWidth(0)
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
        cut = '( ' + twoFakes_sameJet_mm_sh + LepIDIsoFail(1, 't', iso_cut) + LepIDIsoFail(2, 't', iso_cut) + ptEtaBin(ipt,ieta) + twoLepObjIsoleq1 + ') * %f'%weight_tt[ieta][ipt]
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

def selectCuts(channel):

    DFR = []; SFR = []; dirs = []

    if channel == 'eee':
        DYBB_dir       =   DYBBDir_eee     
        DY10_dir       =   DY10Dir_eee      
        DY50_dir       =   DY50Dir_eee      
        DY50_ext_dir   =   DY50_extDir_eee 
        W_dir          =   W_dir_eee
        W_ext_dir      =   W_ext_dir_eee
        TT_dir         =   TT_dir_eee

        TIGHT          =   DFR_TIGHT_EEE
        LOOSE          =   DFR_LOOSE_EEE
        LOOSENOTTIGHT  =   DFR_LOOSENOTTIGHT_EEE

        l0l1           = l0l1_ee
        l0l2           = l0l2_ee
        l1_loose       = l1_e_loose
        l2_loose       = l2_e_loose
        l1_lnt         = l1_e_lnt  
        l2_lnt         = l2_e_lnt  
        l1_tight       = l1_e_tight
        l2_tight       = l2_e_tight

    if channel == 'emm':
        DYBB_dir       =   DYBBDir_emm     
        DY10_dir       =   DY10Dir_emm      
        DY50_dir       =   DY50Dir_emm      
        DY50_ext_dir   =   DY50_extDir_emm 
        W_dir          =   W_dir_emm
        W_ext_dir      =   W_ext_dir_emm
        TT_dir         =   TT_dir_emm

        TIGHT          =   DFR_TIGHT_EMM
        LOOSE          =   DFR_LOOSE_EMM
        LOOSENOTTIGHT  =   DFR_LOOSENOTTIGHT_EMM

        l0l1           = l0l1_em
        l0l2           = l0l2_em
        l1_loose       = l1_m_loose
        l2_loose       = l2_m_loose
        l1_lnt         = l1_m_lnt  
        l2_lnt         = l2_m_lnt  
        l1_tight       = l1_m_tight
        l2_tight       = l2_m_tight


    if channel == 'mee':
        DYBB_dir       =   DYBBDir_mee     
        DY10_dir       =   DY10Dir_mee      
        DY50_dir       =   DY50Dir_mee      
        DY50_ext_dir   =   DY50_extDir_mee 
        W_dir          =   W_dir_mee
        W_ext_dir      =   W_ext_dir_mee
        TT_dir         =   TT_dir_mee

        TIGHT          =   DFR_TIGHT_MEE
        LOOSE          =   DFR_LOOSE_MEE
        LOOSENOTTIGHT  =   DFR_LOOSENOTTIGHT_MEE

        l0l1           = l0l1_me
        l0l2           = l0l2_me
        l1_loose       = l1_e_loose
        l2_loose       = l2_e_loose
        l1_lnt         = l1_e_lnt  
        l2_lnt         = l2_e_lnt  
        l1_tight       = l1_e_tight
        l2_tight       = l2_e_tight


    if channel == 'mem':
        DYBB_dir       =   DYBBDir_mem     
        DY10_dir       =   DY10Dir_mem      
        DY50_dir       =   DY50Dir_mem      
        DY50_ext_dir   =   DY50_extDir_mem 
        W_dir          =   W_dir_mem
        W_ext_dir      =   W_ext_dir_mem
        TT_dir         =   TT_dir_mem

        TIGHT          =   DFR_TIGHT_MEM
        LOOSE          =   DFR_LOOSE_MEM
        LOOSENOTTIGHT  =   DFR_LOOSENOTTIGHT_MEM

        l0l1           = l0l1_me
        l0l2           = l0l2_mm
        l1_loose       = l1_e_loose
        l2_loose       = l2_m_loose
        l1_lnt         = l1_e_lnt  
        l2_lnt         = l2_m_lnt  
        l1_tight       = l1_e_tight
        l2_tight       = l2_m_tight


    if channel == 'mmm':
        DYBB_dir       =   DYBBDir_mmm     
        DY10_dir       =   DY10Dir_mmm      
        DY50_dir       =   DY50Dir_mmm      
        DY50_ext_dir   =   DY50_extDir_mmm 
        W_dir          =   W_dir_mmm
        W_ext_dir      =   W_ext_dir_mmm
        TT_dir         =   TT_dir_mmm

        TIGHT          =   DFR_TIGHT_MMM
        LOOSE          =   DFR_LOOSE_MMM
        LOOSENOTTIGHT  =   DFR_LOOSENOTTIGHT_MMM

        l0l1           = l0l1_mm
        l0l2           = l0l2_mm
        l1_loose       = l1_m_loose
        l2_loose       = l2_m_loose
        l1_lnt         = l1_m_lnt  
        l2_lnt         = l2_m_lnt  
        l1_tight       = l1_m_tight
        l2_tight       = l2_m_tight

    SFR  = [l0l1, l0l2, l1_loose, l2_loose, l1_lnt, l2_lnt, l1_tight, l2_tight] 
    DFR  = [LOOSE, TIGHT, LOOSENOTTIGHT] 
    dirs = [DYBB_dir, DY10_dir, DY50_dir, DY50_ext_dir, TT_dir, W_dir, W_ext_dir] 

    return SFR, DFR, dirs 
######################################################################################

######################################################################################
def checkIso(ch='mmm'):

    SFR, DFR, dirs = selectCuts(ch)

    l0l1, l0l2, l1_loose, l2_loose, l1_lnt, l2_lnt, l1_tight, l2_tight = SFR 
    LOOSE, TIGHT, LOOSENOTTIGHT = DFR
    DYBB_dir, DY10_dir, DY50_dir, DY50_ext_dir, TT_dir, W_dir, W_ext_dir = dirs   

    t_dy = rt.TChain('tree')
    t_dy.Add(DYBB_dir + suffix)
    t_dy.Add(DY10_dir + suffix)
    t_dy.Add(DY50_dir + suffix)
    t_dy.Add(DY50_ext_dir + suffix)

    f_in_t = rt.TFile(TT_dir + suffix)
    t_tt = f_in_t.Get('tree')

    vars = {'l1_reliso05':'(180,0.05,9.05)', 'l1_reliso_rho_03':'(180,0.05,8.05)', 'l1_pt':'(50,2,102)', 'l2_pt':'(50,2,102)', 'l0_pt':'(50,2,102)', 'abs(l1_dxy)':'(60,0.05,3.05)'}
 
    for var in vars.keys()[0:1]:

        print'\n\tdrawing %s \n' %var

        t_tt.Draw('{var}>>TT{bins}'.format(var=var,bins=vars[var]),l0l2_mm)
        t_dy.Draw('{var}>>DY{bins}'.format(var=var,bins=vars[var]),l0l2_mm)

        dy = rt.gDirectory.Get('DY')
        dy.SetMarkerStyle(1); dy.SetMarkerSize(0.5); dy.SetLineColor(rt.kGreen+2); dy.SetMarkerColor(rt.kGreen+2); dy.SetTitle('DY')
        tt = rt.gDirectory.Get('TT')                                      
        tt.SetMarkerStyle(1); tt.SetMarkerSize(0.5); tt.SetLineColor(rt.kRed+2);   tt.SetMarkerColor(rt.kRed+2);   tt.SetTitle('TT')

        c = rt.TCanvas(var,var)
    #    framer.GetYaxis().SetTitle('Normalized entries')
    #    framer.GetXaxis().SetTitle(var)
        dy.DrawNormalized()
        tt.DrawNormalized('same')
        c.BuildLegend()
        pf.showlogoprelimsim('CMS')
        pf.showlumi(ch+'_'+var)
        save(c, sample='DY_TT_'+var, ch=ch)
 
    sys.stderr = sys.__stderr__
    sys.stdout = sys.__stdout__
####################################################################################################

####################################################################################################
def getIsoCDF(ch='mem'):

        #cumulative
        h_dy_c = rt.TH1F('iso_c_dy','iso_c_dy',180,0.05,9.05)
        h_tt_c = rt.TH1F('iso_c_tt','iso_c_tt',180,0.05,9.05)

        h_dy_c.SetMarkerStyle(1); h_dy_c.SetMarkerSize(0.5); h_dy_c.SetLineColor(rt.kGreen+2); h_dy_c.SetMarkerColor(rt.kGreen+2); h_dy_c.SetTitle('DY')
        h_tt_c.SetMarkerStyle(1); h_tt_c.SetMarkerSize(0.5); h_tt_c.SetLineColor(rt.kRed+2);   h_tt_c.SetMarkerColor(rt.kRed+2);   h_tt_c.SetTitle('TT')

        h_dy = rt.TFile(plotDir+'DY_TT_mem_l1_reliso_rho_03.root').Get('l1_reliso_rho_03').GetPrimitive('l1_reliso_rho_03DY')
        h_tt = rt.TFile(plotDir+'DY_TT_mem_l1_reliso_rho_03.root').Get('l1_reliso_rho_03').GetPrimitive('l1_reliso_rho_03TT')

        binCont_dy = 0
        binCont_tt = 0
        nBins = range(180)
        for i in nBins:
            binCont_dy += h_dy.GetBinContent(i+1)
            binCont_tt += h_tt.GetBinContent(i+1)
            h_dy_c.SetBinContent(i+1, binCont_dy) 
            h_tt_c.SetBinContent(i+1, binCont_tt)

        h_dy_by_tt = rt.TH1F('iso_c_div','iso_c_div',180,0.05,9.05)
        h_dy_by_tt.Divide(h_dy_c,h_tt_c)

        c = rt.TCanvas('iso_c','iso_c')
        h_dy_c.Draw()
        h_tt_c.Draw('same')
        c.BuildLegend()
        pf.showlogoprelimsim('CMS')
        pf.showlumi('mem-iso_cdf')
        save(c, sample='DY_TT', ch=ch)

        c = rt.TCanvas('iso_c_div','iso_c_div')
        h_dy_by_tt.Draw()
        pf.showlogoprelimsim('CMS')
        pf.showlumi('mem-iso_cdf_div')
        save(c, sample='DY_TT', ch=ch)
####################################################################################################

####################################################################################################
def selectDefs(ch):

    promptMode = ch[0]
    pairMode   = ch[1] + ch[2]

    l0_is_fake_dr, no_fakes_dr, one_fake_xor_dr, two_fakes_dr, twoFakes_sameJet_dr = '','','','','' 
    l0_is_fake_sh, no_fakes_sh, one_fake_xor_sh, two_fakes_sh, twoFakes_sameJet_sh = '','','','','' 
    
    if promptMode == 'm': 
        l0_is_fake_sh       = l0_fake_m_sh
        l0_is_fake_dr       = l0_fake_m_dr

    if promptMode == 'e':
        l0_is_fake_dr       = l0_fake_e_dr


    if pairMode == 'ee': 
        no_fakes_dr         = no_fakes_ee_dr
        one_fake_xor_dr     = one_fake_xor_ee_dr
        two_fakes_dr        = two_fakes_ee_dr
        twoFakes_sameJet_dr = twoFakes_sameJet_ee_dr 

    #TODO
#    if pairMode == 'em': 
#        no_fakes_dr         = no_fakes_em_dr
#        one_fake_xor_dr     = one_fake_xor_em_dr
#        two_fakes_dr        = two_fakes_em_dr
#        twoFakes_sameJet_dr = twoFakes_sameJet_em_dr 

    if pairMode == 'mm':
        no_fakes_dr         = no_fakes_mm_dr
        one_fake_xor_dr     = one_fake_xor_mm_dr
        two_fakes_dr        = two_fakes_mm_dr
        twoFakes_sameJet_dr = twoFakes_sameJet_mm_dr 

    dRdefList = [l0_is_fake_dr, no_fakes_dr, one_fake_xor_dr, two_fakes_dr, twoFakes_sameJet_dr]
    sHdefList = [l0_is_fake_sh, no_fakes_sh, one_fake_xor_sh, two_fakes_sh, twoFakes_sameJet_sh]
 
    return dRdefList, sHdefList 
######################################################################################

######################################################################################
cut_l0ml2m    = 'l0_pt > 25 & l2_pt > 15 & l0_id_m & l2_id_m & l0_reliso_rho_03 < 0.25 & l2_reliso_rho_03 < 0.25'
cut_l0ml2m    += ' & l0_q * l2_q < 0 & l1_pt > 5'

#l1_e_tight = 'l1_pt > 5 & l1_MediumNoIso & l1_reliso05 < 0.1 & abs(l1_dxy) > 0.05 & ' + l1_fake_e_dr
#l1_e_lnt   = 'l1_pt > 5 & l1_LooseNoIso  & l1_reliso05 > 0.1 & abs(l1_dxy) > 0.05 & ' + l1_fake_e_dr #FIXME
#l1_e_loose = 'l1_pt > 5 & l1_LooseNoIso  & abs(l1_dxy) > 0.05 & ' + l1_fake_e_dr

#l0_prompt_e_dr =  '( ( (dataset['l0_gen_match_isDirectPromptTauDecayProductFinalState'] == 1)  |  (dataset['l0_gen_match_isDirectHardProcessTauDecayProductFinalState'] == 1) '
#l0_prompt_e_dr += ' |  (dataset['l0_gen_match_fromHardProcessFinalState'] == 1)  |  (dataset['l0_gen_match_isPromptFinalState'] == 1) ) & ( abs( (dataset['l0_gen_match_pdgid']) == 11)  | abs( (dataset['l0_gen_match_pdgid']) == 22)  )'
# l0_prompt_e_dr += ' & l0_good_match )'
#l0_prompt_e_dr += ' &  ( sqrt( ( (dataset['l0_eta']-dataset['l0_gen_match_eta'])**2 + (' + dPhi00DS + ')**2 ) < 0.04 ) ) '

#dPhi00 = '( (FF(dataset['l0_phi']-dataset['l0_gen_match_phi'] + 2*pi) * (FF(dataset['l0_phi']-dataset['l0_gen_match_phi'] < -pi) + (FF(dataset['l0_phi']-dataset['l0_gen_match_phi'] - 2*pi) * (FF(dataset['l0_phi']-dataset['l0_gen_match_phi'] > pi) )' 

def skimTrees(ch,sample,treeDir,cut,START=0,STOP=1):

    treeFile = rt.TFile(treeDir+suffix) 
    tree     = treeFile.Get('tree')

    nevents = tree.GetEntries()
    aPop = 200000
    nslices = int(nevents/aPop) + 1
    print '\n\tnumber of slices:', nslices 

    RANGE = range(nslices)
    if STOP > 2: RANGE = range(START,STOP)
    for islice in RANGE:#[:3]:
        
        start =  islice  * aPop
        if (islice + 1) < nslices: stop = (islice + 1) * aPop
        if (islice + 1) == nslices: stop = nevents
        
        print '\n\tloading dataset for slice', (islice + 1)
        dataset = pandas.DataFrame(root_numpy.tree2array(tree, start=start, stop=stop, selection=cut))
        print '\tloading done'

        dataset ['l1e_dxy_geq_005'] = abs(dataset.l1_dxy) > 0.05
        dataset ['z_mass_leq_10']   = abs(dataset.hnl_m_02 - 91.19) < 10
        dataset ['l0m_prompt']      = abs(dataset.hnl_m_02 - 91.19) < 10
        dataset ['l1e_fake']        = abs(dataset.hnl_m_02 - 91.19) < 10
        dataset ['l2m_prompt']      = abs(dataset.hnl_m_02 - 91.19) < 10
        

        print '\tstaging out...'
        dataset.to_root(skimDir + 'SFR_%s_%s'%(ch,sample) + '_slice%d.root' %islice, key='tree')
        print '\tslice', (islice + 1), 'done'

def merge(ch, sample):

    tomerge = glob(skimDir + 'SFR_%s_%s'%(ch,sample) + '_slice*.root')
    command = 'hadd ' + skimDir + 'SFR_%s_%s'%(ch,sample) + '.root'

    for imerge in tomerge:
        command += ' ' + imerge
