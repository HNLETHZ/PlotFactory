from __future__ import division
from ROOT import gROOT as gr
from ROOT import RDataFrame as rdf
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
from itertools import product
'''
WATCH OUT THAT CODE HAS TO BE C++ COMPATIBLE
'''

chain =rt.TChain('tree')
chain.Add('/eos/user/v/vstampf/ntuples/HN3Lv2.0/background/montecarlo/mc_mem/DYJetsToLL_M50/HNLTreeProducer/tree.root')
chain.Add('/eos/user/v/vstampf/ntuples/HN3Lv2.0/background/montecarlo/mc_mem/DYJetsToLL_M50_ext/HNLTreeProducer/tree.root')

d_dy = rdf(chain)
d_tt = rdf('tree', '/eos/user/v/vstampf/ntuples/HN3Lv2.0/background/montecarlo/mc_mem/TTJets_amcat/HNLTreeProducer/tree.root')

pf.setpfstyle()

####################################################################################################
skimDir = '/eos/user/v/vstampf/ntuples/skimmed_trees/'
plotDir = '/eos/user/v/vstampf/plots/DDE/'
suffix  = 'HNLTreeProducer/tree.root'
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
l0_prompt_m_dr =  '( (l0_gen_match_isDirectPromptTauDecayProductFinalState == 1 || l0_gen_match_isDirectHardProcessTauDecayProductFinalState == 1'
l0_prompt_m_dr += ' || l0_gen_match_fromHardProcessFinalState == 1 || l0_gen_match_isPromptFinalState == 1) && abs(l0_gen_match_pdgid) == 13'#&& l0_is_real == 1'
l0_prompt_m_dr += ' && l0_good_match )'

l1_prompt_m_dr =  '( (l1_gen_match_isDirectPromptTauDecayProductFinalState == 1 || l1_gen_match_isDirectHardProcessTauDecayProductFinalState == 1'
l1_prompt_m_dr += ' || l1_gen_match_fromHardProcessFinalState == 1 || l1_gen_match_isPromptFinalState == 1) && abs(l1_gen_match_pdgid) == 13'#&& l1_is_real == 1'
l1_prompt_m_dr += ' && l1_good_match )'

l2_prompt_m_dr =  '( (l2_gen_match_isDirectPromptTauDecayProductFinalState == 1 || l2_gen_match_isDirectHardProcessTauDecayProductFinalState == 1'
l2_prompt_m_dr += ' || l2_gen_match_fromHardProcessFinalState == 1 || l2_gen_match_isPromptFinalState == 1) && abs(l2_gen_match_pdgid) == 13'#&& l2_is_real == 1'
l2_prompt_m_dr += ' && l2_good_match )'

l0_prompt_e_dr =  '( (l0_gen_match_isDirectPromptTauDecayProductFinalState == 1 || l0_gen_match_isDirectHardProcessTauDecayProductFinalState == 1'
l0_prompt_e_dr += ' || l0_gen_match_fromHardProcessFinalState == 1 || l0_gen_match_isPromptFinalState == 1) && ( abs(l0_gen_match_pdgid) == 11 || abs(l0_gen_match_pdgid) == 22 )'
l0_prompt_e_dr += ' && l0_good_match )'

l1_prompt_e_dr =  '( (l1_gen_match_isDirectPromptTauDecayProductFinalState == 1 || l1_gen_match_isDirectHardProcessTauDecayProductFinalState == 1'
l1_prompt_e_dr += ' || l1_gen_match_fromHardProcessFinalState == 1 || l1_gen_match_isPromptFinalState == 1) && ( abs(l1_gen_match_pdgid) == 11 || abs(l1_gen_match_pdgid) == 22 )'
l1_prompt_e_dr += ' && l1_good_match )'

l2_prompt_e_dr =  '( (l2_gen_match_isDirectPromptTauDecayProductFinalState == 1 || l2_gen_match_isDirectHardProcessTauDecayProductFinalState == 1'
l2_prompt_e_dr += ' || l2_gen_match_fromHardProcessFinalState == 1 || l2_gen_match_isPromptFinalState == 1) && ( abs(l2_gen_match_pdgid) == 11 || abs(l2_gen_match_pdgid) == 22 )'
l2_prompt_e_dr += ' && l2_good_match )'

l0_fake_m_dr = '( !' + l0_prompt_m_dr + ' )' 
l1_fake_m_dr = '( !' + l1_prompt_m_dr + ' )' 
l2_fake_m_dr = '( !' + l2_prompt_m_dr + ' )' 

l0_fake_e_dr = '( !' + l0_prompt_e_dr + ' )' 
l1_fake_e_dr = '( !' + l1_prompt_e_dr + ' )' 
l2_fake_e_dr = '( !' + l2_prompt_e_dr + ' )' 
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
l0l2_mm    += ' & l0_q * l2_q < 0 & abs(l0_dxy) < 0.05 & abs(l2_dxy) < 0.05 & abs(l1_reliso05) < 0.43'
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
l2_e_tight_M_10 = 'l2_pt > 5 && l2_MediumNoIso && l2_reliso05 < 0.10 && abs(l2_dxy) > 0.05 && ' + l2_fake_e_dr
l2_e_tight_M_15 = 'l2_pt > 5 && l2_MediumNoIso && l2_reliso05 < 0.15 && abs(l2_dxy) > 0.05 && ' + l2_fake_e_dr
l2_e_tight_M_20 = 'l2_pt > 5 && l2_MediumNoIso && l2_reliso05 < 0.20 && abs(l2_dxy) > 0.05 && ' + l2_fake_e_dr
l2_e_tight_M_10 = 'l2_pt > 5 && l2_LooseNoIso  && l2_reliso05 < 0.10 && abs(l2_dxy) > 0.05 && ' + l2_fake_e_dr
l2_e_tight_M_15 = 'l2_pt > 5 && l2_LooseNoIso  && l2_reliso05 < 0.15 && abs(l2_dxy) > 0.05 && ' + l2_fake_e_dr
l2_e_tight_M_20 = 'l2_pt > 5 && l2_LooseNoIso  && l2_reliso05 < 0.20 && abs(l2_dxy) > 0.05 && ' + l2_fake_e_dr
l2_e_loose      = 'l2_pt > 5 && l2_LooseNoIso  && abs(l2_dxy) > 0.05 && ' + l2_fake_e_dr
####################################################################################################
#l0l2_mm    = 'l0_pt > 15 && l2_pt > 5 && l0_id_m && l2_id_m && l0_reliso_rho_03 < 0.15 && l2_reliso_rho_03 < 0.15'
#l0l2_mm    += ' && hnl_iso03_rel_rhoArea < 1 && abs(hnl_m_02 - 91.19) < 10 && l0_q * l2_q < 0 && abs(l0_dxy) < 0.05 && abs(l2_dxy) < 0.05'
#l0l2_mm    += ' && l0_q * l2_q < 0 && abs(l0_dxy) < 0.05 && abs(l2_dxy) < 0.05 && abs(l1_reliso05) < 5'
#l0l2_mm    += ' && ' + l0_prompt_m_dr + ' && ' + l2_prompt_m_dr 
####################################################################################################
base_l0l2_mm  = 'l0_pt > 15 && l2_pt > 5 && l0_id_m && l2_id_m && l0_reliso_rho_03 < 0.15 && l2_reliso_rho_03 < 0.15'
base_l0l2_mm += ' && l0_q * l2_q < 0 && abs(l0_dxy) < 0.05 && abs(l2_dxy) < 0.05 && abs(l1_reliso05) < 5'

#h =f2.Histo1D(("l1_pt","",len(b_pt)-1,b_pt),"l1_pt")

#d.Histo1D('l1_pt')
def Draw():

    f0_dy = d_dy.Filter(base_l0l2_mm)
    f0_tt = d_tt.Filter(base_l0l2_mm)

    c = rt.TCanvas()

#d.Histo1D('l1_pt')

#asd = d.Histo1D('l1_pt')


#h = f1.Histo1D(("asd","",10,0,100),"l1_pt")

######################################################################################

######################################################################################
def checkStuff(ch='mem'):

    n_d_dy = d_dy.Count()
    n_d_tt = d_tt.Count()

    f0_dy = d_dy.Filter(base_l0l2_mm)
    f0_tt = d_tt.Filter(base_l0l2_mm)

    n_f0_dy = f0_dy.Count()
    n_f0_tt = f0_tt.Count()

    df0_dy = f0_dy.Define('abs_l1_dxy', 'abs(l1_dxy)') 
    df0_tt = f0_tt.Define('abs_l1_dxy', 'abs(l1_dxy)') 

    SFR, DFR, dirs = selectCuts(ch)

    l0l1, l0l2, l1_loose, l2_loose, l1_lnt, l2_lnt, l1_tight, l2_tight = SFR 

    vars = {'l1_reliso05':[180,0.05,9.05], 'l1_reliso_rho_03':[180,0.05,9.05], 'l1_pt':[50,2,102], 'l2_pt':[50,2,102], 'l0_pt':[50,2,102], 'abs_l1_dxy':[60,0.05,3.05]}

    print'\n\tDY at base_l0l2_mm: %d, initial: %d' %(n_f0_dy.GetValue(), n_d_dy.GetValue())
    print'\n\tTT at base_l0l2_mm: %d, initial: %d\n' %(n_f0_tt.GetValue(), n_d_tt.GetValue())
 
    for var in vars.keys():

        print'\n\tdrawing %s \n' %var

#        set_trace()
        h_dy = df0_dy.Histo1D((var+'DY',var+'DY',vars[var][0],vars[var][1],vars[var][2]),var)
        h_tt = df0_tt.Histo1D((var+'TT',var+'TT',vars[var][0],vars[var][1],vars[var][2]),var)

        h_dy.SetMarkerStyle(0); h_dy.SetMarkerSize(0.5); h_dy.SetMarkerColor(rt.kGreen+2); h_dy.SetTitle('DY')
        h_tt.SetMarkerStyle(0); h_tt.SetMarkerSize(0.5); h_tt.SetMarkerColor(rt.kRed+2);   h_tt.SetTitle('TT')

        c = rt.TCanvas(var,var)
        h_dy.DrawNormalized()
        h_tt.DrawNormalized('same')
        c.BuildLegend()
        pf.showlogoprelimsim('CMS')
        pf.showlumi(ch+'_'+var)
        save(c, sample='DY_TT', ch=ch)
######################################################################################

######################################################################################
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
######################################################################################

######################################################################################
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
def save(knvs, iso=0, sample='', ch='', eta=''):
    if iso == 0: iso_str = '' 
    if iso != 0: iso_str = '_iso' + str(int(iso * 100))
    knvs.GetFrame().SetLineWidth(0)
    knvs.Modified(); knvs.Update()
    if len(eta):
        knvs.SaveAs('{dr}{smpl}_{ch}_{ttl}{iso}_eta{eta}.png' .format(dr=plotDir, smpl=sample, ttl=knvs.GetTitle(), ch=ch, iso=iso_str, eta=eta))
        knvs.SaveAs('{dr}{smpl}_{ch}_{ttl}{iso}_eta{eta}.pdf' .format(dr=plotDir, smpl=sample, ttl=knvs.GetTitle(), ch=ch, iso=iso_str, eta=eta))
        knvs.SaveAs('{dr}{smpl}_{ch}_{ttl}{iso}_eta{eta}.root'.format(dr=plotDir, smpl=sample, ttl=knvs.GetTitle(), ch=ch, iso=iso_str, eta=eta))
    else:
        knvs.SaveAs('{dr}{smpl}_{ch}_{ttl}{iso}.png' .format(dr=plotDir, smpl=sample, ttl=knvs.GetTitle(), ch=ch, iso=iso_str))
        knvs.SaveAs('{dr}{smpl}_{ch}_{ttl}{iso}.pdf' .format(dr=plotDir, smpl=sample, ttl=knvs.GetTitle(), ch=ch, iso=iso_str))
        knvs.SaveAs('{dr}{smpl}_{ch}_{ttl}{iso}.root'.format(dr=plotDir, smpl=sample, ttl=knvs.GetTitle(), ch=ch, iso=iso_str))
