from __future__ import division
from ROOT import gROOT as gr
from ROOT import RDataFrame as rdf
import os, platform
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

Linux-2.6.32-754.3.5.el6.x86_64-x86_64-with-redhat-6.6-Carbon         #T3
Linux-3.10.0-957.1.3.el7.x86_64-x86_64-with-centos-7.6.1810-Core      #LX+
'''
eos       = '/eos/user/v/vstampf/'
eos_david = '/eos/user/d/dezhu/HNL/'
if platform.platform() == 'Linux-2.6.32-754.3.5.el6.x86_64-x86_64-with-redhat-6.6-Carbon':
   eos       = '/t3home/vstampf/eos/'
   eos_david = '/t3home/vstampf/eos-david/'

pf.setpfstyle()

pi = rt.TMath.Pi()
####################################################################################################
skimDir = eos+'ntuples/skimmed_trees/'
plotDir = eos+'plots/DDE/'
suffix  = 'HNLTreeProducer/tree.root'
####################################################################################################
DYBBDir_mee     = eos_david+'ntuples/HN3Lv2.0/background/montecarlo/mee/partial/DYBB/'
DY50Dir_mee     = eos_david+'ntuples/HN3Lv2.0/background/montecarlo/mee/partial/DYJetsToLL_M50/'
DY50_extDir_mee = eos_david+'ntuples/HN3Lv2.0/background/montecarlo/mee/partial/DYJetsToLL_M50_ext/'
DY10Dir_mee     = eos_david+'ntuples/HN3Lv2.0/background/montecarlo/mee/partial/DYJetsToLL_M10to50/'
TT_dir_mee      = eos_david+'ntuples/HN3Lv2.0/background/montecarlo/mee/partial/TTJets_amcat_20190130/'  
W_dir_mee       = eos_david+'ntuples/HN3Lv2.0/background/montecarlo/mee/20190129/ntuples/WJetsToLNu/'
W_ext_dir_mee   = eos_david+'ntuples/HN3Lv2.0/background/montecarlo/mee/20190129/ntuples/WJetsToLNu_ext/'
####################################################################################################
DYBBDir_mem     = eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_mem/DYBB/'
DY50Dir_mem     = eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_mem/DYJetsToLL_M50/'
DY50_extDir_mem = eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_mem/DYJetsToLL_M50_ext/'
DY10Dir_mem     = eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_mem/DYJetsToLL_M10to50/'
TT_dir_mem      = eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_mem/TTJets_amcat/'  
W_dir_mem       = eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_mem/WJetsToLNu/'
W_ext_dir_mem   = eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_mem/WJetsToLNu_ext/'
####################################################################################################
DYBBDir_mmm     = '/work/vstampf/ntuples/mmm/partial/DYBB/'
DY50Dir_mmm     = '/work/vstampf/ntuples/mmm/partial/DYJetsToLL_M50/'
DY50_extDir_mmm = '/work/vstampf/ntuples/mmm/partial/DYJetsToLL_M50_ext/'
DY10Dir_mmm     = '/work/vstampf/ntuples/mmm/partial/DYJetsToLL_M10to50/'
TT_dir_mmm      = eos_david+'ntuples/HN3Lv2.0/background/montecarlo/mmm/TTJets_amcat_TauDecayInfo/'  
W_dir_mmm       = eos_david+'ntuples/HN3Lv2.0/background/montecarlo/mmm/WJetsToLNu/'
W_ext_dir_mmm   = eos_david+'ntuples/HN3Lv2.0/background/montecarlo/mmm/WJetsToLNu_ext/'
####################################################################################################
DYBBDir_eee     = eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_eee/partial/DYBB/'
DY50Dir_eee     = eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_eee/partial/DYJetsToLL_M50/'
DY50_extDir_eee = eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_eee/partial/DYJetsToLL_M50_ext/'
DY10Dir_eee     = eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_eee/partial/DYJetsToLL_M10to50/'
TT_dir_eee      = eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_eee/partial/TTJets_amcat/'  
W_dir_eee       = eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_eee/partial/WJetsToLNu/'
W_ext_dir_eee   = eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_eee/partial/WJetsToLNu_ext/'
####################################################################################################
DYBBDir_eem     = eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_eem/DYBB/'
DY50Dir_eem     = eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_eem/DYJetsToLL_M50/'
DY50_extDir_eem = eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_eem/DYJetsToLL_M50_ext/'
DY10Dir_eem     = eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_eem/DYJetsToLL_M10to50/'
TT_dir_eem      = eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_eem/TTJets_amcat/'  
W_dir_eem       = eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_eem/WJetsToLNu/'
W_ext_dir_eem   = eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_eem/WJetsToLNu_ext/'
####################################################################################################
dPhi00  =  '( (l0_phi-l0_gen_match_phi + 2*TMath::Pi()) * (l0_phi-l0_gen_match_phi < -TMath::Pi()) + (l0_phi-l0_gen_match_phi - 2*TMath::Pi()) * (l0_phi-l0_gen_match_phi > TMath::Pi())'\
           ' + (l0_phi-l0_gen_match_phi) * ( (l0_phi-l0_gen_match_phi > -TMath::Pi()) && (l0_phi-l0_gen_match_phi < TMath::Pi()) ) )' 

dPhi11  =  '( (l1_phi-l1_gen_match_phi + 2*TMath::Pi()) * (l1_phi-l1_gen_match_phi < -TMath::Pi()) + (l1_phi-l1_gen_match_phi - 2*TMath::Pi()) * (l1_phi-l1_gen_match_phi > TMath::Pi())'\
           ' + (l1_phi-l1_gen_match_phi) * ( (l1_phi-l1_gen_match_phi > -TMath::Pi()) && (l1_phi-l1_gen_match_phi < TMath::Pi()) ) )' 

dPhi22  =  '( (l2_phi-l2_gen_match_phi + 2*TMath::Pi()) * (l2_phi-l2_gen_match_phi < -TMath::Pi()) + (l2_phi-l2_gen_match_phi - 2*TMath::Pi()) * (l2_phi-l2_gen_match_phi > TMath::Pi())'\
           ' + (l2_phi-l2_gen_match_phi) * ( (l2_phi-l2_gen_match_phi > -TMath::Pi()) && (l2_phi-l2_gen_match_phi < TMath::Pi()) ) )' 
####################################################################################################
## SHITTY CODE TODO REMOVE!!
dPhi00  =  '( (l0_phi-l0_gen_match_phi + 2*TMath::Pi()) * (l0_phi-l0_gen_match_phi < -TMath::Pi()) + (l0_phi-l0_gen_match_phi - 2*TMath::Pi()) * (l0_phi-l0_gen_match_phi > TMath::Pi()) )'

dPhi11  =  '( (l1_phi-l1_gen_match_phi + 2*TMath::Pi()) * (l1_phi-l1_gen_match_phi < -TMath::Pi()) + (l1_phi-l1_gen_match_phi - 2*TMath::Pi()) * (l1_phi-l1_gen_match_phi > TMath::Pi()) )'

dPhi22  =  '( (l2_phi-l2_gen_match_phi + 2*TMath::Pi()) * (l2_phi-l2_gen_match_phi < -TMath::Pi()) + (l2_phi-l2_gen_match_phi - 2*TMath::Pi()) * (l2_phi-l2_gen_match_phi > TMath::Pi()) )'
####################################################################################################
l0_prompt_m_dr =  '( (l0_gen_match_isDirectPromptTauDecayProductFinalState == 1 || l0_gen_match_isDirectHardProcessTauDecayProductFinalState == 1'
l0_prompt_m_dr += ' || l0_gen_match_fromHardProcessFinalState == 1 || l0_gen_match_isPromptFinalState == 1) && abs(l0_gen_match_pdgid) == 13'#&& l0_is_real == 1'
#l0_prompt_m_dr += ' && l0_good_match == 1 )'
l0_prompt_m_dr += ' && sqrt( pow((l0_eta-l0_gen_match_eta),2) + pow((' + dPhi00 + '),2) ) < 0.04 && l0_pdgid == l0_gen_match_pdgid )' #FIXME

l1_prompt_m_dr =  '( (l1_gen_match_isDirectPromptTauDecayProductFinalState == 1 || l1_gen_match_isDirectHardProcessTauDecayProductFinalState == 1'
l1_prompt_m_dr += ' || l1_gen_match_fromHardProcessFinalState == 1 || l1_gen_match_isPromptFinalState == 1) && abs(l1_gen_match_pdgid) == 13'#&& l1_is_real == 1'
#l1_prompt_m_dr += ' && l1_good_match == 1 )'
l1_prompt_m_dr += ' && sqrt( pow((l1_eta-l1_gen_match_eta),2) + pow((' + dPhi11 + '),2) ) < 0.04 )'

l2_prompt_m_dr =  '( (l2_gen_match_isDirectPromptTauDecayProductFinalState == 1 || l2_gen_match_isDirectHardProcessTauDecayProductFinalState == 1'
l2_prompt_m_dr += ' || l2_gen_match_fromHardProcessFinalState == 1 || l2_gen_match_isPromptFinalState == 1) && abs(l2_gen_match_pdgid) == 13'#&& l2_is_real == 1'
#l2_prompt_m_dr += ' && l2_good_match == 1 )'
l2_prompt_m_dr += ' && sqrt( pow((l2_eta-l2_gen_match_eta),2) + pow((' + dPhi22 + '),2) ) < 0.04 && l2_pdgid == l2_gen_match_pdgid )' #FIXME

l0_prompt_e_dr =  '( (l0_gen_match_isDirectPromptTauDecayProductFinalState == 1 || l0_gen_match_isDirectHardProcessTauDecayProductFinalState == 1'
l0_prompt_e_dr += ' || l0_gen_match_fromHardProcessFinalState == 1 || l0_gen_match_isPromptFinalState == 1) && ( abs(l0_gen_match_pdgid) == 11 || abs(l0_gen_match_pdgid) == 22 )'
#l0_prompt_e_dr += ' && l0_good_match == 1 )'
l0_prompt_e_dr += ' && sqrt( pow((l0_eta-l0_gen_match_eta),2) + pow((' + dPhi00 + '),2) ) < 0.04 )'

l1_prompt_e_dr =  '( (l1_gen_match_isDirectPromptTauDecayProductFinalState == 1 || l1_gen_match_isDirectHardProcessTauDecayProductFinalState == 1'
l1_prompt_e_dr += ' || l1_gen_match_fromHardProcessFinalState == 1 || l1_gen_match_isPromptFinalState == 1) && ( abs(l1_gen_match_pdgid) == 11 || abs(l1_gen_match_pdgid) == 22 )'
#l1_prompt_e_dr += ' && l1_good_match == 1 )'
l1_prompt_e_dr += ' && sqrt( pow((l1_eta-l1_gen_match_eta),2) + pow((' + dPhi11 + '),2) ) < 0.04 )'

l2_prompt_e_dr =  '( (l2_gen_match_isDirectPromptTauDecayProductFinalState == 1 || l2_gen_match_isDirectHardProcessTauDecayProductFinalState == 1'
l2_prompt_e_dr += ' || l2_gen_match_fromHardProcessFinalState == 1 || l2_gen_match_isPromptFinalState == 1) && ( abs(l2_gen_match_pdgid) == 11 || abs(l2_gen_match_pdgid) == 22 )'
#l2_prompt_e_dr += ' && l2_good_match == 1 )'
l2_prompt_e_dr += ' && sqrt( pow((l2_eta-l2_gen_match_eta),2) + pow((' + dPhi22 + '),2) ) < 0.04 )'

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
DFR_LOOSE_MEE          =  ' && (l1_pt > 3 && l1_LooseNoIso == 1 && l2_pt > 3 && l2_LooseNoIso == 1 && l0_id_t == 1 && l0_reliso_rho_04 < 0.15 && hnl_iso04_rel_rhoArea < 1 )'     
DFR_LOOSENOTTIGHT_MEE  =  ' && (l1_pt > 3 && l1_LooseNoIso == 1 && l2_pt > 3 && l2_LooseNoIso == 1 && l0_id_t == 1 && l0_reliso_rho_04 < 0.15 && (l1_reliso05 > 0.2 || l2_reliso05 > 0.2) && hnl_iso04_rel_rhoArea < 1 )'#FIXME
DFR_TIGHT_MEE          =  ' && (l1_pt > 3 && l1_LooseNoIso == 1 && l2_pt > 3 && l2_LooseNoIso == 1 && l0_id_t == 1 && l0_reliso_rho_04 < 0.15 && l1_reliso05 < 0.2 && l2_reliso05 < 0.2 )' 
####################################################################################################
# FIXME
DFR_LOOSE_MEM          =  ' && (l1_pt > 3 && l1_LooseNoIso == 1 && l2_pt > 3 && l2_LooseNoIso == 1 && l0_id_t == 1 && l0_reliso_rho_03 < 0.15 && hnl_iso03_rel_rhoArea < 1 )'     
DFR_LOOSENOTTIGHT_MEM  =  ' && (l1_pt > 3 && l1_LooseNoIso == 1 && l2_pt > 3 && l2_LooseNoIso == 1 && l0_id_t == 1 && l0_reliso_rho_03 < 0.15 && (l1_reliso05 > 0.2 || l2_reliso05 > 0.2) && hnl_iso03_rel_rhoArea < 1 )'#FIXME
DFR_TIGHT_MEM          =  ' && (l1_pt > 3 && l1_MediumNoIso == 1 && l2_pt > 3 && l2_LooseNoIso == 1 && l0_id_t == 1 && l0_reliso_rho_03 < 0.15 && l1_reliso05 < 0.2 && l2_reliso05 < 0.2 )' 
####################################################################################################
DFR_LOOSE_MMM         = ' && (l1_pt > 3 && l2_pt > 3 && l0_id_t == 1 && l0_reliso_rho_04 < 0.15 && l1_id_l == 1 && l2_id_l == 1 && hnl_iso04_rel_rhoArea < 1 )'
DFR_LOOSENOTTIGHT_MMM = ' && (l1_pt > 3 && l2_pt > 3 && l0_id_t == 1 && l0_reliso_rho_04 < 0.15 && l1_id_l == 1 && l2_id_l == 1 && (l1_reliso_rho_04 > 0.15 || l2_reliso_rho_04 > 0.15) && hnl_iso04_rel_rhoArea < 1 )'# FIXME 
DFR_TIGHT_MMM         = ' && (l1_pt > 3 && l2_pt > 3 && l0_id_t == 1 && l0_reliso_rho_04 < 0.15 && l1_id_l == 1 && l2_id_l == 1 && l1_reliso_rho_04 < 0.15 && l2_reliso_rho_04 < 0.15 )' 
####################################################################################################
DFR_LOOSE_EEE         =  ' && (l1_pt > 3 && l1_LooseNoIso == 1 && l2_pt > 3 && l2_LooseNoIso == 1 && l0_eid_mva_iso_wp90 == 1 && l0_reliso05 < 0.15 && hnl_iso03_rel_rhoArea < 3 )' 
DFR_LOOSENOTTIGHT_EEE =  ' && (l1_pt > 3 && l1_LooseNoIso == 1 && l2_pt > 3 && l2_LooseNoIso == 1 && l0_eid_mva_iso_wp90 == 1 && l0_reliso05 < 0.15 && (l1_reliso05 > 0.15 || l2_reliso05 > 0.15) && hnl_iso04_rel_rhoArea < 3 )' 
DFR_TIGHT_EEE         =  ' && (l1_pt > 3 && l1_MediumNoIso == 1 && l2_pt > 3 && l2_MediumNoIso == 1 && l0_eid_mva_iso_wp90 == 1 && l0_reliso05 < 0.15 && l1_reliso05 < 0.15 && l2_reliso05 < 0.15 )' 
####################################################################################################
DFR_LOOSE_EMM         = ' && (l1_pt > 3 && l2_pt > 3 && l0_eid_cut_loose && l0_reliso05 < 0.15 && l1_id_l == 1 && l2_id_l == 1 && hnl_iso04_rel_rhoArea < 1 )'
DFR_LOOSENOTTIGHT_EMM = ' && (l1_pt > 3 && l2_pt > 3 && l0_eid_cut_loose && l0_reliso05 < 0.15 && l1_id_l == 1 && l2_id_l == 1 && (l1_reliso_rho_04 > 0.15 || l2_reliso_rho_04 > 0.15) && hnl_iso04_rel_rhoArea < 1 )'  # FIXME 
DFR_TIGHT_EMM         = ' && (l1_pt > 3 && l2_pt > 3 && l0_eid_cut_loose && l0_reliso05 < 0.15 && l1_id_l == 1 && l2_id_l == 1 && l1_reliso_rho_04 < 0.15 && l2_reliso_rho_04 < 0.15 )' 
####################################################################################################
              ##                 SINGLE FAKE RATE                   ##  
####################################################################################################
l0l1_ee    = '(l1_pt > 5 && l0_eid_mva_iso_wp90 == 1 && l1_eid_mva_iso_wp90 == 1 && l0_reliso05 < 0.15 && l1_reliso05 < 0.15'
#l0l1_ee    += ' && hnl_iso03_rel_rhoArea < 1 && abs(hnl_m_01 - 91.19) < 10 && l0_q * l1_q < 0 && abs(l0_dxy) < 0.05 && abs(l1_dxy) < 0.05)'
l0l1_ee    += ' && l0_q * l1_q < 0 && abs(l0_dxy) < 0.05 && abs(l1_dxy) < 0.05)' # && hnl_iso03_rel_rhoArea < 1'
l0l1_ee    += ' && ' + l0_prompt_e_dr + ' && ' + l1_prompt_e_dr + ' && abs(l2_dxy) > 0.01' 

l0l2_ee    = '(l2_pt > 3 && l0_eid_mva_iso_wp90 == 1 && l2_eid_mva_iso_wp90 == 1 && l0_reliso05 < 0.15 && l2_reliso05 < 0.15'
#l0l2_ee    += ' && hnl_iso03_rel_rhoArea < 1 && abs(hnl_m_02 - 91.19) < 10 && l0_q * l2_q < 0 && abs(l0_dxy) < 0.05 && abs(l2_dxy) < 0.05)'
l0l2_ee    += ' && hnl_iso03_rel_rhoArea < 1 && l0_q * l2_q < 0 && abs(l0_dxy) < 0.05 && abs(l2_dxy) < 0.05)'
l0l2_ee    += ' && ' + l0_prompt_e_dr + ' && ' + l2_prompt_e_dr
####################################################################################################
l0l1_me    = '(l1_pt > 3 && l0_id_t == 1 && l1_eid_mva_iso_wp90 == 1 && l0_reliso_rho_03 < 0.15 && l1_reliso05 < 0.15'
l0l1_me    += ' && hnl_iso03_rel_rhoArea < 1 && abs(hnl_m_01 - 91.19) < 10 && l0_q * l1_q < 0 && abs(l0_dxy) < 0.05 && abs(l1_dxy) < 0.05)'
l0l1_me    += ' && ' + l0_prompt_m_dr + ' && ' + l1_prompt_e_dr + ' && abs(l2_dxy) > 0.01' 
####################################################################################################
l0l2_em    = '(l2_pt > 3 && l0_eid_mva_iso_wp90 && l2_id_m == 1 && l0_reliso05 < 0.15 && l2_reliso_rho_03 < 0.15'
l0l2_em    += ' && hnl_iso03_rel_rhoArea < 1 && abs(hnl_m_02 - 91.19) < 10 && l0_q * l2_q < 0 && abs(l0_dxy) < 0.05 && abs(l2_dxy) < 0.05)'
l0l2_em    += ' && ' + l0_prompt_e_dr + ' && ' + l2_prompt_m_dr 
####################################################################################################
l0l1_mm    = 'l1_pt > 3 && l0_id_t == 1 && l1_id_t == 1 && l0_reliso_rho_03 < 0.15 && l1_reliso_rho_03 < 0.15'
l0l1_mm    += ' && hnl_iso03_rel_rhoArea < 2 && abs(hnl_m_01 - 91.19) < 10 && l0_q * l1_q < 0 && abs(l0_dxy) < 0.05 && abs(l1_dxy) < 0.05'
l0l1_mm    += ' && ' + l0_prompt_m_dr + ' && ' + l1_prompt_m_dr 

l0l2_mm    = 'l0_pt > 15 && l2_pt > 5 && l0_id_m == 1 && l2_id_m == 1 && l0_reliso_rho_03 < 0.15 && l2_reliso_rho_03 < 0.15'
#l0l2_mm    += ' && hnl_iso03_rel_rhoArea < 1 && abs(hnl_m_02 - 91.19) < 10 && l0_q * l2_q < 0 && abs(l0_dxy) < 0.05 && abs(l2_dxy) < 0.05'
l0l2_mm    += ' && l0_q * l2_q < 0 && abs(l0_dxy) < 0.05 && abs(l2_dxy) < 0.05 && abs(l1_reliso_rho_03) < 1.1'
#l0l2_mm    += ' && l0_q * l2_q < 0 && abs(l0_dxy) < 0.05 && abs(l2_dxy) < 0.05 && abs(l1_reliso_rho_03) < 0.35' # DON'T CHANGE, STATE OF THE ART
l0l2_mm    += ' && ' + l0_prompt_m_dr + ' && ' + l2_prompt_m_dr 
####################################################################################################
l1_e_tight = 'l1_pt > 5 && l1_MediumNoIso == 1 && l1_reliso_rho_03 < 0.15 && abs(l1_dxy) > 0.01 && ' + l1_fake_e_dr
#l1_e_tight = 'l1_pt > 5 && l1_MediumWithIso == 1 && l1_reliso_rho_03 < 0.10 && abs(l1_dxy) > 0.01 && ' + l1_fake_e_dr # DON'T CHANGE, STATE OF THE ART
l1_e_lnt   = 'l1_pt > 5 && (l1_MediumWithIso == 0 || l1_reliso_rho_03 > 0.15) && abs(l1_dxy) > 0.01 && ' + l1_fake_e_dr 
l1_e_loose = 'l1_pt > 5 && abs(l1_dxy) > 0.01 && ' + l1_fake_e_dr # DON'T CHANGE, STATE OF THE ART

l2_e_tight = 'l2_pt > 5 && l2_MediumWithIso == 1 && l2_reliso_rho_03 < 0.10 && abs(l2_dxy) > 0.05 && ' + l2_fake_e_dr
l2_e_lnt   = 'l2_pt > 5 && l2_LooseNoIso == 1 && l2_reliso_rho_03 > 0.10 && abs(l2_dxy) > 0.01 && ' + l2_fake_e_dr #FIXME
#l1_e_loose = 'l1_pt > 5 && l1_LooseNoIso  && abs(l1_dxy) > 0.01 && ' + l1_fake_e_dr # DON'T CHANGE, STATE OF THE ART
l2_e_loose = 'l2_pt > 5 && l2_LooseNoIso == 1 && abs(l2_dxy) > 0.05 && ' + l2_fake_e_dr
####################################################################################################
l1_m_tight = 'l1_pt > 5 && l1_id_l == 1 && l1_reliso_rho_03 < 0.15 && abs(l1_dxy) > 0.01 && ' + l1_fake_m_dr
l2_m_tight = 'l2_pt > 5 && l2_id_l == 1 && l2_reliso_rho_03 < 0.15 && abs(l2_dxy) > 0.01 && ' + l2_fake_m_dr
l1_m_lnt   = 'l1_pt > 5 && l1_id_l == 1 && l1_reliso_rho_03 > 0.15 && abs(l1_dxy) > 0.01 && ' + l1_fake_m_dr
l2_m_lnt   = 'l2_pt > 5 && l2_id_l == 1 && l2_reliso_rho_03 > 0.15 && abs(l2_dxy) > 0.01 && ' + l2_fake_m_dr
l1_m_loose = 'l1_pt > 5 && l1_id_l == 1 && abs(l1_dxy) > 0.01 && ' + l1_fake_m_dr
l2_m_loose = 'l2_pt > 5 && l2_id_l == 1 && abs(l2_dxy) > 0.01 && ' + l2_fake_m_dr
####################################################################################################

####################################################################################################
l2_e_tight_M_10 = 'l2_pt > 5 && l2_MediumNoIso == 1 && l2_reliso05 < 0.10 && abs(l2_dxy) > 0.05 && ' + l2_fake_e_dr
l2_e_tight_M_15 = 'l2_pt > 5 && l2_MediumNoIso == 1 && l2_reliso05 < 0.15 && abs(l2_dxy) > 0.05 && ' + l2_fake_e_dr
l2_e_tight_M_20 = 'l2_pt > 5 && l2_MediumNoIso == 1 && l2_reliso05 < 0.20 && abs(l2_dxy) > 0.05 && ' + l2_fake_e_dr
l2_e_tight_M_10 = 'l2_pt > 5 && l2_LooseNoIso == 1 && l2_reliso05 < 0.10 && abs(l2_dxy) > 0.05 && ' + l2_fake_e_dr
l2_e_tight_M_15 = 'l2_pt > 5 && l2_LooseNoIso == 1 && l2_reliso05 < 0.15 && abs(l2_dxy) > 0.05 && ' + l2_fake_e_dr
l2_e_tight_M_20 = 'l2_pt > 5 && l2_LooseNoIso == 1 && l2_reliso05 < 0.20 && abs(l2_dxy) > 0.05 && ' + l2_fake_e_dr
l2_e_loose      = 'l2_pt > 5 && l2_LooseNoIso == 1 && abs(l2_dxy) > 0.05 && ' + l2_fake_e_dr
####################################################################################################
#l0l2_mm    = 'l0_pt > 15 && l2_pt > 5 && l0_id_m == 1 && l2_id_m == 1 && l0_reliso_rho_03 < 0.15 && l2_reliso_rho_03 < 0.15'
#l0l2_mm    += ' && hnl_iso03_rel_rhoArea < 1 && abs(hnl_m_02 - 91.19) < 10 && l0_q * l2_q < 0 && abs(l0_dxy) < 0.05 && abs(l2_dxy) < 0.05'
#l0l2_mm    += ' && l0_q * l2_q < 0 && abs(l0_dxy) < 0.05 && abs(l2_dxy) < 0.05 && abs(l1_reliso05) < 5'
#l0l2_mm    += ' && ' + l0_prompt_m_dr + ' && ' + l2_prompt_m_dr 
####################################################################################################
#base_l0l2_mm  = 'l0_pt > 15 && l2_pt > 5 && l0_id_m == 1 && l2_id_m == 1 && l0_reliso_rho_03 < 0.15 && l2_reliso_rho_03 < 0.15'
#base_l0l2_mm += ' && l0_q * l2_q < 0 && abs(l0_dxy) < 0.05 && abs(l2_dxy) < 0.05 && abs(l1_dxy) > 0.01  && ' + l0_prompt_m_dr + ' && ' + l2_prompt_m_dr + ' && ' + l1_fake_e_dr

PTCONE = '(  ( hnl_hn_vis_pt * (hnl_iso03_rel_rhoArea<0.15) ) + ( (hnl_iso03_rel_rhoArea>=0.15) * ( hnl_hn_vis_pt * (1. + hnl_iso03_rel_rhoArea - 0.15) ) )  )'
#h =f2.Histo1D(("l1_pt","",len(b_pt)-1,b_pt),"l1_pt")

#d.Histo1D('l1_pt')

#d.Histo1D('l1_pt')

#asd = d.Histo1D('l1_pt')

#h = f1.Histo1D(("asd","",10,0,100),"l1_pt")

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

brl0 = np.arange(0.,1.,0.01)
brl1 = np.arange(1.,10,0.05)
brl2 = np.arange(10.,20.2,0.2)
b_reliso = np.concatenate((brl0,brl1,brl2),axis=None)

framer = rt.TH2F('','',len(b_pt)-1,b_pt,len(b_y)-1,b_y)
framer.GetYaxis().SetRangeUser(0.,0.5)
framer.GetYaxis().SetRangeUser(0.,1.0)
#framer.GetYaxis().SetRangeUser(0.01,0.5)
######################################################################################

######################################################################################
l_eta = {'_eta_00t08' : 'abs(l1_eta) < 0.8', '_eta_08t15' : 'abs(l1_eta) > 0.8 & abs(l1_eta) < 1.479', '_eta_15t25' : 'abs(l1_eta) > 1.479 & abs(l1_eta) < 2.5'}

l_pt   = { '_pt0t5'   : 'ptcone < 5',                  '_pt5t10' : 'ptcone > 5 && ptcone < 10',  '_pt10t15' : 'ptcone > 10 && ptcone < 15', '_pt15t20' : 'ptcone > 15 && ptcone < 20',
           '_pt20t25' : 'ptcone > 20 && ptcone < 25', '_pt25t35' : 'ptcone > 25 && ptcone < 35', '_pt35t50' : 'ptcone > 35 && ptcone < 50', '_pt50t70' : 'ptcone > 50'}# && ptcone < 70'}
    
def selectBins(ch='mem'):

    if ch == 'mem':
        f_in = rt.TFile(plotDir+'DY_TT_TTL_mem_ptCone_eta.root')
        c = f_in.Get('ptCone_eta')
        h = c.GetPrimitive('pt_eta_T')

    sfr =  '   ({eta00t08} && {pt0t5})   * {eta00t08_pt0t5}'  .format(eta00t08 = l_eta['_eta_00t08'], pt0t5   = l_pt['_pt0t5']  , eta00t08_pt0t5   = h.GetBinContent(1,1)/(1-h.GetBinContent(1,1))) 
    sfr += ' + ({eta00t08} && {pt5t10})  * {eta00t08_pt5t10}' .format(eta00t08 = l_eta['_eta_00t08'], pt5t10  = l_pt['_pt5t10'] , eta00t08_pt5t10  = h.GetBinContent(2,1)/(1-h.GetBinContent(2,1)))
    sfr += ' + ({eta00t08} && {pt10t15}) * {eta00t08_pt10t15}'.format(eta00t08 = l_eta['_eta_00t08'], pt10t15 = l_pt['_pt10t15'], eta00t08_pt10t15 = h.GetBinContent(3,1)/(1-h.GetBinContent(3,1)))
    sfr += ' + ({eta00t08} && {pt15t20}) * {eta00t08_pt15t20}'.format(eta00t08 = l_eta['_eta_00t08'], pt15t20 = l_pt['_pt15t20'], eta00t08_pt15t20 = h.GetBinContent(4,1)/(1-h.GetBinContent(4,1)))
    sfr += ' + ({eta00t08} && {pt20t25}) * {eta00t08_pt20t25}'.format(eta00t08 = l_eta['_eta_00t08'], pt20t25 = l_pt['_pt20t25'], eta00t08_pt20t25 = h.GetBinContent(5,1)/(1-h.GetBinContent(5,1)))
    sfr += ' + ({eta00t08} && {pt25t35}) * {eta00t08_pt25t35}'.format(eta00t08 = l_eta['_eta_00t08'], pt25t35 = l_pt['_pt25t35'], eta00t08_pt25t35 = h.GetBinContent(6,1)/(1-h.GetBinContent(6,1)))
    sfr += ' + ({eta00t08} && {pt35t50}) * {eta00t08_pt35t50}'.format(eta00t08 = l_eta['_eta_00t08'], pt35t50 = l_pt['_pt35t50'], eta00t08_pt35t50 = h.GetBinContent(7,1)/(1-h.GetBinContent(7,1)))
    sfr += ' + ({eta00t08} && {pt50t70}) * {eta00t08_pt50t70}'.format(eta00t08 = l_eta['_eta_00t08'], pt50t70 = l_pt['_pt50t70'], eta00t08_pt50t70 = h.GetBinContent(8,1)/(1-h.GetBinContent(8,1)))
    sfr += ' + ({eta08t15} && {pt0t5})   * {eta08t15_pt0t5}'  .format(eta08t15 = l_eta['_eta_08t15'], pt0t5   = l_pt['_pt0t5']  , eta08t15_pt0t5   = h.GetBinContent(1,2)/(1-h.GetBinContent(1,2))) 
    sfr += ' + ({eta08t15} && {pt5t10})  * {eta08t15_pt5t10}' .format(eta08t15 = l_eta['_eta_08t15'], pt5t10  = l_pt['_pt5t10'] , eta08t15_pt5t10  = h.GetBinContent(2,2)/(1-h.GetBinContent(2,2)))
    sfr += ' + ({eta08t15} && {pt10t15}) * {eta08t15_pt10t15}'.format(eta08t15 = l_eta['_eta_08t15'], pt10t15 = l_pt['_pt10t15'], eta08t15_pt10t15 = h.GetBinContent(3,2)/(1-h.GetBinContent(3,2)))
    sfr += ' + ({eta08t15} && {pt15t20}) * {eta08t15_pt15t20}'.format(eta08t15 = l_eta['_eta_08t15'], pt15t20 = l_pt['_pt15t20'], eta08t15_pt15t20 = h.GetBinContent(4,2)/(1-h.GetBinContent(4,2)))
    sfr += ' + ({eta08t15} && {pt20t25}) * {eta08t15_pt20t25}'.format(eta08t15 = l_eta['_eta_08t15'], pt20t25 = l_pt['_pt20t25'], eta08t15_pt20t25 = h.GetBinContent(5,2)/(1-h.GetBinContent(5,2)))
    sfr += ' + ({eta08t15} && {pt25t35}) * {eta08t15_pt25t35}'.format(eta08t15 = l_eta['_eta_08t15'], pt25t35 = l_pt['_pt25t35'], eta08t15_pt25t35 = h.GetBinContent(6,2)/(1-h.GetBinContent(6,2)))
    sfr += ' + ({eta08t15} && {pt35t50}) * {eta08t15_pt35t50}'.format(eta08t15 = l_eta['_eta_08t15'], pt35t50 = l_pt['_pt35t50'], eta08t15_pt35t50 = h.GetBinContent(7,2)/(1-h.GetBinContent(7,2)))
    sfr += ' + ({eta08t15} && {pt50t70}) * {eta08t15_pt50t70}'.format(eta08t15 = l_eta['_eta_08t15'], pt50t70 = l_pt['_pt50t70'], eta08t15_pt50t70 = h.GetBinContent(8,2)/(1-h.GetBinContent(8,2)))
    sfr += ' + ({eta15t25} && {pt0t5})   * {eta15t25_pt0t5}'  .format(eta15t25 = l_eta['_eta_15t25'], pt0t5   = l_pt['_pt0t5']  , eta15t25_pt0t5   = h.GetBinContent(1,3)/(1-h.GetBinContent(1,3))) 
    sfr += ' + ({eta15t25} && {pt5t10})  * {eta15t25_pt5t10}' .format(eta15t25 = l_eta['_eta_15t25'], pt5t10  = l_pt['_pt5t10'] , eta15t25_pt5t10  = h.GetBinContent(2,3)/(1-h.GetBinContent(2,3)))
    sfr += ' + ({eta15t25} && {pt10t15}) * {eta15t25_pt10t15}'.format(eta15t25 = l_eta['_eta_15t25'], pt10t15 = l_pt['_pt10t15'], eta15t25_pt10t15 = h.GetBinContent(3,3)/(1-h.GetBinContent(3,3)))
    sfr += ' + ({eta15t25} && {pt15t20}) * {eta15t25_pt15t20}'.format(eta15t25 = l_eta['_eta_15t25'], pt15t20 = l_pt['_pt15t20'], eta15t25_pt15t20 = h.GetBinContent(4,3)/(1-h.GetBinContent(4,3)))
    sfr += ' + ({eta15t25} && {pt20t25}) * {eta15t25_pt20t25}'.format(eta15t25 = l_eta['_eta_15t25'], pt20t25 = l_pt['_pt20t25'], eta15t25_pt20t25 = h.GetBinContent(5,3)/(1-h.GetBinContent(5,3)))
    sfr += ' + ({eta15t25} && {pt25t35}) * {eta15t25_pt25t35}'.format(eta15t25 = l_eta['_eta_15t25'], pt25t35 = l_pt['_pt25t35'], eta15t25_pt25t35 = h.GetBinContent(6,3)/(1-h.GetBinContent(6,3)))
    sfr += ' + ({eta15t25} && {pt35t50}) * {eta15t25_pt35t50}'.format(eta15t25 = l_eta['_eta_15t25'], pt35t50 = l_pt['_pt35t50'], eta15t25_pt35t50 = h.GetBinContent(7,3)/(1-h.GetBinContent(7,3)))
    sfr += ' + ({eta15t25} && {pt50t70}) * {eta15t25_pt50t70}'.format(eta15t25 = l_eta['_eta_15t25'], pt50t70 = l_pt['_pt50t70'], eta15t25_pt50t70 = h.GetBinContent(8,3)/(1-h.GetBinContent(8,3)))

    return sfr
######################################################################################

######################################################################################
def measureTTLratio(ch='mem',isData=False):

    SFR, DFR, dirs = selectCuts(ch)

    l0l1, l0l2, l1_loose, l2_loose, l1_lnt, l2_lnt, l1_tight, l2_tight = SFR 

#    cuts_SFR = l_eta[eta]
    
    if isData == False:

        if ch == 'mem':
            
            chain =rt.TChain('tree')
            chain.Add(eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_mem/DYJetsToLL_M50/HNLTreeProducer/tree.root')
            chain.Add(eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_mem/DYJetsToLL_M50_ext/HNLTreeProducer/tree.root')
            chain.Add(eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_mem/TTJets_amcat/HNLTreeProducer/tree.root')

            ## FROM MAR 8 to match with def of MR in applyTTLratio (cf below)
            ####################################################################################################
            l0l2    = 'l0_pt > 27 && l2_pt > 5 && l0_id_m == 1 && l2_id_m == 1 && l0_reliso_rho_03 < 0.15 && l2_reliso_rho_03 < 0.15'
            l0l2    += ' && l0_q * l2_q < 0 && abs(l0_dxy) < 0.05  && abs(l0_dz) < 0.2 && abs(l2_dxy) < 0.05 && abs(l2_dz) < 0.2 && abs(l1_reliso_rho_03) < 1.1'
            ####################################################################################################
            l1_tight = 'l1_pt > 5 && l1_MediumNoIso == 1 && l1_reliso_rho_03 < 0.15 && abs(l1_dxy) > 0.01'
            l1_lnt   = 'l1_pt > 5 && (l1_MediumWithIso == 0  || l1_reliso_rho_03 > 0.15) && abs(l1_dxy) > 0.01'
            l1_loose = 'l1_pt > 5 && abs(l1_dxy) > 0.01'
            ####################################################################################################

            df = rdf(chain)
    #
            print '\n\tchain made.'
     
            mshReg = 'hnl_w_vis_m > 80'

#            f0 = df.Filter(cuts_SFR + ' && ' + l0l2 + ' && ' + l1_loose)
            f0 = df.Filter(l0l2 + ' && ' + l1_loose + ' && ' + mshReg)

    print '\n\tf0 entries:', f0.Count().GetValue()

    df0 = f0.Define('ptcone', PTCONE)

    print '\n\tptcone defined.'

    dfl = df0.Define('abs_l1_eta', 'abs(l1_eta)')

    print '\n\tabs_l1_eta defined.'

    dft = dfl.Filter(l1_tight)

    print '\n\ttight df defined.'

    _pt_eta_T = dft.Histo2D(('pt_eta_T','pt_eta_T',len(b_pt)-1,b_pt,len(b_eta)-1,b_eta),'ptcone','abs_l1_eta')
    _pt_eta_L = dfl.Histo2D(('pt_eta_L','pt_eta_L',len(b_pt)-1,b_pt,len(b_eta)-1,b_eta),'ptcone','abs_l1_eta')

    h_pt_eta_T = _pt_eta_T.GetPtr()
    h_pt_eta_L = _pt_eta_L.GetPtr()

    print '\n\tentries T & L: ', h_pt_eta_T.GetEntries(), h_pt_eta_L.GetEntries()

    c_pt_eta = rt.TCanvas('ptCone_eta', 'ptCone_eta')
    h_pt_eta_T.Divide(h_pt_eta_L)
    h_pt_eta_T.Draw('colztextE')
    h_pt_eta_T.SetTitle('; p_{T}^{cone} [GeV]; DiMuon |#eta|; tight-to-loose ratio')
    pf.showlogoprelimsim('CMS')
    pf.showlumi('SFR_'+ch)
    save(c_pt_eta, sample='DY_TT_TTL_noTruth', ch=ch)

    # DO AGAIN WITH THREE DIFFERENT TEFFS TO GET ERROR
####################################################################################################

####################################################################################################
def checkTTLratio(ch='mem',eta_split=True,sfr=True,dfr=False):

    l_eta  = {'_eta_all' : '1'}

    if eta_split == True: 
        if ch == 'mem':
            l_eta = {'_eta_00t08' : 'abs(l1_eta) < 0.8', '_eta_08t15' : 'abs(l1_eta) > 0.8 & abs(l1_eta) < 1.479', '_eta_15t25' : 'abs(l1_eta) > 1.479 & abs(l1_eta) < 2.5'}

#    print l_eta

    samples = ['TT','DY','WJ']

    print '\n\tmode: %s\n'%ch

    sList = raw_input('\tchoose between TT, DY and WJ (inclusively)\n\t')
    samples = sList.split(',')

    if samples[0] == 'all': samples = ['TT','DY','WJ']

    iso_cut = 0.15
    iso_str = str(int(iso_cut * 100))

    cuts_DFR = 'abs(l1_dz) < 2 & abs(l2_dz) < 2 & hnl_2d_disp > 0.5 & l1_q * l2_q < 0'

#    N_ENTRIES = 0

    SFR, DFR, dirs = selectCuts(ch)

    l0l1, l0l2, l1_loose, l2_loose, l1_lnt, l2_lnt, l1_tight, l2_tight = SFR 
    LOOSE, TIGHT, LOOSENOTTIGHT = DFR
    DYBB_dir, DY10_dir, DY50_dir, DY50_ext_dir, TT_dir, W_dir, W_ext_dir = dirs   

    dRdefList, sHdefList = selectDefs(ch)

    l0_is_fake, no_fakes, one_fake_xor, two_fakes, twoFakes_sameJet = dRdefList

    sys.stdout = Logger(plotDir + 'FR_%s_%s' %(ch,samples))

    print '\n\t pT cone: %s\n' %PTCONE 

    for eta in l_eta.keys():
        h_pt_1f = []; h_pt_2f = []; i = 0

        for sample in samples: 
            t = None
            if sample == 'DY':
                t = rt.TChain('tree')
                t.Add(DYBB_dir + suffix)
                t.Add(DY10_dir + suffix)
                t.Add(DY50_dir + suffix)
                t.Add(DY50_ext_dir + suffix)
                df = rdf(t)
                print'\n\tchain made.'
                N_ENTRIES = df.Count()
            if sample == 'TT':
                fin = rt.TFile(TT_dir + suffix)
                t = fin.Get('tree')
                df = rdf(t)
                N_ENTRIES = df.Count()
            if sample == 'WJ':
                t = rt.TChain('tree')
                t.Add(W_dir + suffix)
                t.Add(W_ext_dir + suffix)
                df = rdf(t)
                N_ENTRIES = df.Count()

            if sfr:

                print '\tsample: %s, drawing single fakes ...'%sample

                h_pt_1f_T_012  = rt.TH1F('pt_1f_T_012', 'pt_1f_T_012',len(b_pt)-1,b_pt)
                h_pt_1f_T_021  = rt.TH1F('pt_1f_T_021', 'pt_1f_T_021',len(b_pt)-1,b_pt)
                h_pt_1f_L_012  = rt.TH1F('pt_1f_L_012', 'pt_1f_L_012',len(b_pt)-1,b_pt)
                h_pt_1f_L_021  = rt.TH1F('pt_1f_L_021', 'pt_1f_L_021',len(b_pt)-1,b_pt)

        #            print '\t',sample, 'entries after loose selection:', t.GetEntries(SFR_DY_LOOSE_EEE)
        #            print '\n\t TIGHT WP: %s\n' %SFR_DY_TIGHT_EEE
        #            print '\n\t LOOSE WP: %s\n' %SFR_DY_LOOSE_EEE
        #            print '\n\t LNT WP: %s\n' %SFR_DY_LNT_EEE

        #        if sample == 'DY':

                cuts_SFR = '1 && ' + l_eta[eta]
                cuts_l = cuts_SFR + ' && ' + l0l2 + ' && ' + l1_loose

                f0 = df.Filter(cuts_l)
                print '\tloose defined.'

                dfl = f0.Define('ptcone', PTCONE)
                print '\tptcone defined.'

                dft = dfl.Filter(l1_tight)
                print '\ttight defined.'
                
                print '\n\t cuts: %s'                         %cuts_SFR
                print '\n\t l0l1: %s\n'                       %(l0l1)
                print '\n\t l0l2: %s\n'                       %(l0l2)
                print '\n\t l1_loose: %s\n'                   %(l1_loose)
                print '\n\t l1_tight: %s\n'                   %(l1_tight)
                print '\n\t l2_loose: %s\n'                   %(l2_loose)
                print '\n\t l2_tight: %s\n'                   %(l2_tight)

                print '\t',sample, 'entries loose:',          f0.Count().GetValue()
                print '\t',sample, 'entries tight:',          dft.Count().GetValue()

            
                if ch in ['mmm','eee']:
                    t.Draw('l1_pt >> pt_1f_T_021', cuts_SFR + ' & ' + l0l2 + ' & ' + l1_tight)
                    t.Draw('l2_pt >> pt_1f_T_012', cuts_SFR + ' & ' + l0l1 + ' & ' + l2_tight)

                if ch == 'mem':
#                    t.Draw('l1_pt >> pt_1f_T_021', cuts_SFR + ' & ' + l0l2 + ' & ' + l1_tight)
                    _h_pt_1f_T_021 = dft.Histo1D(('pt_1f_T_021', 'pt_1f_T_021',len(b_pt)-1,b_pt), 'ptcone')
                    h_pt_1f_T_021 = _h_pt_1f_T_021.GetPtr()

                if ch == 'eem':
                    t.Draw('l2_pt >> pt_1f_T_012', cuts_SFR + ' & ' + l0l1 + ' & ' + l2_tight)

                h_pt_1f_T_012.Add(h_pt_1f_T_021)
                print '\tentries tight:', h_pt_1f_T_012.GetEntries()

                if ch in ['mmm','eee']:
                    t.Draw('l1_pt >> pt_1f_L_021', cuts_SFR + ' & ' + l0l2 + ' & ' + l1_loose)
                    t.Draw('l2_pt >> pt_1f_L_012', cuts_SFR + ' & ' + l0l1 + ' & ' + l2_loose)

                if ch == 'mem':
#                    t.Draw('l1_pt >> pt_1f_L_021', cuts_SFR + ' & ' + l0l2 + ' & ' + l1_loose)
                    _h_pt_1f_L_021 = dfl.Histo1D(('pt_1f_L_021', 'pt_1f_L_021',len(b_pt)-1,b_pt), 'ptcone')
                    h_pt_1f_L_021 = _h_pt_1f_L_021.GetPtr()

                if ch == 'eem':
                    t.Draw('l2_pt >> pt_1f_T_012', cuts_SFR + ' & ' + l0l1 + ' & ' + l2_loose)

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
#                c.SetLogy()
                h_pt_1f[i].Draw('same')
                pf.showlogoprelimsim('CMS')
                pf.showlumi(sample+'-'+ch+eta)
                save(c_pt_1f, iso_cut, sample, ch+eta)

                print '\n\tsingle-fakes done ...'
     
            if dfr:

                print '\n\tdrawing double fakes ...'

                cut_T = cuts + TIGHT ## UPDATED TO LIMIT JET-JUNK WITH LARGE DR
                cut_L = cuts + LOOSE ## UPDATED TO LIMIT JET-JUNK WITH LARGE DR

                n_entries             = t.GetEntries(cuts) 

                print '\n\t', sample, 'entries before selection:', N_ENTRIES.GetValue() 
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
                pf.showlumi(sample+'-'+ch+eta)
                save(c_pt_2f, iso_cut, sample, ch+eta)
     
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
                pf.showlumi(sample+'-'+ch+eta)
                pf.showlogoprelimsim('CMS')
                save(c_pt_cmprd, iso_cut, sample, ch+eta)

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
                pf.showlumi(ch+eta)
                pf.showlogoprelimsim('CMS')
                save(c_pt_1f, iso_cut, 'cmbnd', ch+eta)

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
                pf.showlumi(ch+eta)
                pf.showlogoprelimsim('CMS')
                save(c_pt_2f, iso_cut, 'cmbnd', ch+eta)

    sys.stderr = sys.__stderr__
    sys.stdout = sys.__stdout__
    print '\n\t %s_%s_iso%s\t done'%(sample, ch+eta, iso_str)

####################################################################################################

####################################################################################################
def applyTTL(isData=False, VLD=True, eta_split=False):

    l_eta  = {'_eta_all' : '1'}

    if eta_split == True: 
        l_eta = {'_eta_00t08' : 'abs(l1_eta) < 0.8', '_eta_08t15' : 'abs(l1_eta) > 0.8 && abs(l1_eta) < 1.479', '_eta_15t25' : 'abs(l1_eta) > 1.479 && abs(l1_eta) < 2.5'}

    ch = 'mem'
    sample = 'mc'

    SFR, DFR, dirs = selectCuts(ch)

    l0l1, l0l2, l1_loose, l2_loose, l1_lnt, l2_lnt, l1_tight, l2_tight = SFR 

    cuts_SFR = '1==1' #l_eta[eta]
    
    if isData == False:

        t = rt.TChain('tree')

        if ch == 'mem':
            
            chain =rt.TChain('tree')
            chain.Add(eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_mem/DYJetsToLL_M50/HNLTreeProducer/tree.root')
            chain.Add(eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_mem/DYJetsToLL_M50_ext/HNLTreeProducer/tree.root')
#            chain.Add(eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_mem/TTJets_amcat/HNLTreeProducer/tree.root')
            df_tt = rdf('tree', eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_mem/TTJets_amcat/HNLTreeProducer/tree.root')

            ## FROM MAR 5 
            ####################################################################################################
            l0l2    = 'l0_pt > 27 && l2_pt > 5 && l0_id_m == 1 && l2_id_m == 1 && l0_reliso_rho_03 < 0.15 && l2_reliso_rho_03 < 0.15'
            l0l2    += ' && l0_q * l2_q < 0 && abs(l0_dxy) < 0.05  && abs(l0_dz) < 0.2 && abs(l2_dxy) < 0.05 && abs(l2_dz) < 0.2 && abs(l1_reliso_rho_03) < 1.1'
            ####################################################################################################
            l1_tight = 'l1_pt > 5 && l1_MediumNoIso == 1 && l1_reliso_rho_03 < 0.15 && abs(l1_dxy) > 0.05'
            l1_lnt   = 'l1_pt > 5 && (l1_MediumWithIso == 0  || l1_reliso_rho_03 > 0.15) && abs(l1_dxy) > 0.05'
            l1_loose = 'l1_pt > 5 && abs(l1_dxy) > 0.05'
            ####################################################################################################

            appReg = 'hnl_w_vis_m < 80'

            cuts_SFR += ' && ' + appReg

        if split == True:

            df_dy = rdf(chain)
            f0_dy = df_dy.Filter(cuts_SFR + ' && ' + l0l2 + ' && ' + l1_loose)
            f0_tt = df_tt.Filter(cuts_SFR + ' && ' + l0l2 + ' && ' + l1_loose)

        if split == False:

            df = rdf(chain)
            f0 = df.Filter(cuts_SFR + ' && ' + l0l2 + ' && ' + l1_loose)

    print '\n\t l0l2: %s\n'       %(l0l2)
    print '\n\t l1_loose: %s\n'   %(l1_loose)
    print '\n\t l1_lnt: %s\n'     %(l1_lnt)
    print '\n\t l1_tight: %s\n'   %(l1_tight)

    print '\n\t weights. dy: %0.2f. tt: %0.2f; initial entries. dy: %d, tt: %d' %(w_dy, w_tt, n_dy, n_tt)

    print '\n\t cuts: %s'%cuts_SFR

    if split == False:

        dfl   = f0.Define('ptcone', PTCONE)
        dfl0  = dfl.Filter(l1_lnt)
        print '\n\tlnt df defined.'

        print '\n\tlnt df events:', dfl0.Count().GetValue()

        dflnt = dfl0.Define('fover1minusf', selectBins(ch))
        print '\n\tweight f/(1-f) defined. (without lumi/data normalization)'

        dft   = dfl.Filter(l1_tight)
        print '\n\ttight df defined.'

        print '\n\ttight df events:', dft.Count().GetValue()

        print '\n\tf0 entries:', f0.Count().GetValue()

    if split == True:

        n_dy = df_dy.Count().GetValue()
        n_tt = df_tt.Count().GetValue()

        # weights
        # dy50:  xSec    = 1921.8*3 pb
        # tt:    xSec    = 831.76 pb
        w_dy = 1 # ( 41000./n_dy ) * 1921.8 * 3 # Lumi data / lumi mc = lumi data / ( n mc / xsec mc) = ( lumi data / n mc ) * xsec mc 
        w_tt = 1 # ( 41000./n_tt ) * 831.76     # Lumi data / lumi mc = lumi data / ( n mc / xsec mc) = ( lumi data / n mc ) * xsec mc 

        print '\n\tf0_dy entries:', f0_dy.Count().GetValue()
        print '\n\tf0_tt entries:', f0_tt.Count().GetValue()

        dfl_dy   = f0_dy.Define('ptcone', PTCONE)
        dfl_tt   = f0_tt.Define('ptcone', PTCONE)
        print '\n\tptcone defined.'

        dfl0_dy  = dfl_dy.Filter(l1_lnt)
        dfl0_tt  = dfl_tt.Filter(l1_lnt)
        print '\n\tlnt df defined.'

        print '\n\tlnt df_dy events:', dfl0_dy.Count().GetValue()
        print '\n\tlnt df_tt events:', dfl0_tt.Count().GetValue()

        dflnt_dy = dfl0_dy.Define('fover1minusf', '(' + selectBins(ch) + ') * %f' %w_dy )
        dflnt_tt = dfl0_tt.Define('fover1minusf', '(' + selectBins(ch) + ') * %f' %w_tt )
        print '\n\tweight f/(1-f) defined. (including lumi/data normalization)'

        dft_dy   = dfl_dy.Filter(l1_tight)
        dft_tt   = dfl_tt.Filter(l1_tight)
        print '\n\ttight df defined.'

        print '\n\ttight df events:', dft_dy.Count().GetValue()
        print '\n\ttight df events:', dft_tt.Count().GetValue()


    if split == False:

        whd_pt         = dflnt.Histo1D(('whd_pt',         'whd_pt',        len(b_pt)-1,      b_pt),     'ptcone',            'fover1minusf')
        whd_dr_12      = dflnt.Histo1D(('whd_dr_12',      'whd_dr_12',     len(b_dR)-1,      b_dR),     'hnl_dr_12',         'fover1minusf')
        whd_2disp      = dflnt.Histo1D(('whd_2disp',      'whd_2disp',     len(b_2d)-1,      b_2d),     'hnl_2d_disp',       'fover1minusf')
        whd_2disp_sig  = dflnt.Histo1D(('whd_2disp_sig',  'whd_2disp_sig', len(b_2d_sig)-1,  b_2d_sig), 'hnl_2d_disp_sig',   'fover1minusf')
        whd_m_dimu     = dflnt.Histo1D(('whd_m_dimu',     'whd_m_dimu',    len(b_m)-1,       b_m),      'hnl_m_12',          'fover1minusf')
        whd_BGM_dimu   = dflnt.Histo1D(('whd_BGM_dimu',   'whd_BGM_dimu',  len(b_M)-1,       b_M),      'hnl_m_12',          'fover1minusf')
        whd_BGM_01     = dflnt.Histo1D(('whd_BGM_01',     'whd_BGM_01',    len(b_M)-1,       b_M),      'hnl_m_01',          'fover1minusf')
        whd_BGM_02     = dflnt.Histo1D(('whd_BGM_02',     'whd_BGM_02',    len(b_M)-1,       b_M),      'hnl_m_02',          'fover1minusf')
        whd_m_triL     = dflnt.Histo1D(('whd_m_triL',     'whd_m_triL',    len(b_M)-1,       b_M),      'hnl_w_vis_m',       'fover1minusf')
     
        obs_pt         = dft.Histo1D(('obs_pt',         'obs_pt',        len(b_pt)-1,     b_pt),     'ptcone'         )
        obs_dr_12      = dft.Histo1D(('obs_dr_12',      'obs_dr_12',     len(b_dR)-1,     b_dR),     'hnl_dr_12'      )
        obs_2disp      = dft.Histo1D(('obs_2disp',      'obs_2disp',     len(b_2d)-1,     b_2d),     'hnl_2d_disp'    )
        obs_2disp_sig  = dft.Histo1D(('obs_2disp_sig',  'obs_2disp_sig', len(b_2d_sig)-1, b_2d_sig), 'hnl_2d_disp_sig')
        obs_m_dimu     = dft.Histo1D(('obs_m_dimu',     'obs_m_dimu',    len(b_m)-1,      b_m),      'hnl_m_12'       )
        obs_BGM_dimu   = dft.Histo1D(('obs_BGM_dimu',   'obs_BGM_dimu',  len(b_M)-1,      b_M),      'hnl_m_12'       )
        obs_BGM_01     = dft.Histo1D(('obs_BGM_01',     'obs_BGM_01',    len(b_M)-1,      b_M),      'hnl_m_01'       )
        obs_BGM_02     = dft.Histo1D(('obs_BGM_02',     'obs_BGM_02',    len(b_M)-1,      b_M),      'hnl_m_02'       )
        obs_m_triL     = dft.Histo1D(('obs_m_triL',     'obs_m_triL',    len(b_M)-1,      b_M),      'hnl_w_vis_m'    )

    h_list = { 'pt'          : [whd_pt,        obs_pt,       ';p_{T}^{cone} [GeV]; Counts'], 
               'dr_12'       : [whd_dr_12,     obs_dr_12,    ';#DeltaR(l_{1},  l_{2}); Counts'], 
               '2disp'       : [whd_2disp,     obs_2disp,    ';2d_disp [cm]; Counts'], 
               '2disp_sig'   : [whd_2disp_sig, obs_2disp_sig,';2d_disp_sig ; Counts'], 
               'm_dimu'      : [whd_m_dimu,    obs_m_dimu,   ';m(l_{1},  l_{2}) [GeV]; Counts'], 
               'M_dimu'      : [whd_BGM_dimu,  obs_BGM_dimu, ';m(l_{1},  l_{2}) [GeV]; Counts'], 
               'M_01'        : [whd_BGM_01,    obs_BGM_01,   ';m(l_{0},  l_{1}) [GeV]; Counts'], 
               'M_02'        : [whd_BGM_02,    obs_BGM_02,   ';m(l_{0},  l_{2}) [GeV]; Counts'], 
               'm_triL'      : [whd_m_triL,    obs_m_triL,   ';m(l_{0},  l_{1},  l_{2}) [GeV]; Counts'], }


    if split == True:

        whd_dy_pt         = dflnt_dy.Histo1D(('whd_pt',         'whd_pt',        len(b_pt)-1,      b_pt),     'ptcone',            'fover1minusf')
        whd_dy_dr_12      = dflnt_dy.Histo1D(('whd_dr_12',      'whd_dr_12',     len(b_dR)-1,      b_dR),     'hnl_dr_12',         'fover1minusf')
        whd_dy_2disp      = dflnt_dy.Histo1D(('whd_2disp',      'whd_2disp',     len(b_2d)-1,      b_2d),     'hnl_2d_disp',       'fover1minusf')
        whd_dy_2disp_sig  = dflnt_dy.Histo1D(('whd_2disp_sig',  'whd_2disp_sig', len(b_2d_sig)-1,  b_2d_sig), 'hnl_2d_disp_sig',   'fover1minusf')
        whd_dy_m_dimu     = dflnt_dy.Histo1D(('whd_m_dimu',     'whd_m_dimu',    len(b_m)-1,       b_m),      'hnl_m_12',          'fover1minusf')
        whd_dy_BGM_dimu   = dflnt_dy.Histo1D(('whd_BGM_dimu',   'whd_BGM_dimu',  len(b_M)-1,       b_M),      'hnl_m_12',          'fover1minusf')
        whd_dy_BGM_01     = dflnt_dy.Histo1D(('whd_BGM_01',     'whd_BGM_01',    len(b_M)-1,       b_M),      'hnl_m_01',          'fover1minusf')
        whd_dy_BGM_02     = dflnt_dy.Histo1D(('whd_BGM_02',     'whd_BGM_02',    len(b_M)-1,       b_M),      'hnl_m_02',          'fover1minusf')
        whd_dy_m_triL     = dflnt_dy.Histo1D(('whd_m_triL',     'whd_m_triL',    len(b_M)-1,       b_M),      'hnl_w_vis_m',       'fover1minusf')
              
        whd_tt_pt         = dflnt_tt.Histo1D(('whd_pt',         'whd_pt',        len(b_pt)-1,      b_pt),     'ptcone',            'fover1minusf')
        whd_tt_dr_12      = dflnt_tt.Histo1D(('whd_dr_12',      'whd_dr_12',     len(b_dR)-1,      b_dR),     'hnl_dr_12',         'fover1minusf')
        whd_tt_2disp      = dflnt_tt.Histo1D(('whd_2disp',      'whd_2disp',     len(b_2d)-1,      b_2d),     'hnl_2d_disp',       'fover1minusf')
        whd_tt_2disp_sig  = dflnt_tt.Histo1D(('whd_2disp_sig',  'whd_2disp_sig', len(b_2d_sig)-1,  b_2d_sig), 'hnl_2d_disp_sig',   'fover1minusf')
        whd_tt_m_dimu     = dflnt_tt.Histo1D(('whd_m_dimu',     'whd_m_dimu',    len(b_m)-1,       b_m),      'hnl_m_12',          'fover1minusf')
        whd_tt_BGM_dimu   = dflnt_tt.Histo1D(('whd_BGM_dimu',   'whd_BGM_dimu',  len(b_M)-1,       b_M),      'hnl_m_12',          'fover1minusf')
        whd_tt_BGM_01     = dflnt_tt.Histo1D(('whd_BGM_01',     'whd_BGM_01',    len(b_M)-1,       b_M),      'hnl_m_01',          'fover1minusf')
        whd_tt_BGM_02     = dflnt_tt.Histo1D(('whd_BGM_02',     'whd_BGM_02',    len(b_M)-1,       b_M),      'hnl_m_02',          'fover1minusf')
        whd_tt_m_triL     = dflnt_tt.Histo1D(('whd_m_triL',     'whd_m_triL',    len(b_M)-1,       b_M),      'hnl_w_vis_m',       'fover1minusf')

        obs_dy_pt         = dft_dy.Histo1D(('obs_pt',         'obs_pt',        len(b_pt)-1,     b_pt),     'ptcone'         )
        obs_dy_dr_12      = dft_dy.Histo1D(('obs_dr_12',      'obs_dr_12',     len(b_dR)-1,     b_dR),     'hnl_dr_12'      )
        obs_dy_2disp      = dft_dy.Histo1D(('obs_2disp',      'obs_2disp',     len(b_2d)-1,     b_2d),     'hnl_2d_disp'    )
        obs_dy_2disp_sig  = dft_dy.Histo1D(('obs_2disp_sig',  'obs_2disp_sig', len(b_2d_sig)-1, b_2d_sig), 'hnl_2d_disp_sig')
        obs_dy_m_dimu     = dft_dy.Histo1D(('obs_m_dimu',     'obs_m_dimu',    len(b_m)-1,      b_m),      'hnl_m_12'       )
        obs_dy_BGM_dimu   = dft_dy.Histo1D(('obs_BGM_dimu',   'obs_BGM_dimu',  len(b_M)-1,      b_M),      'hnl_m_12'       )
        obs_dy_BGM_01     = dft_dy.Histo1D(('obs_BGM_01',     'obs_BGM_01',    len(b_M)-1,      b_M),      'hnl_m_01'       )
        obs_dy_BGM_02     = dft_dy.Histo1D(('obs_BGM_02',     'obs_BGM_02',    len(b_M)-1,      b_M),      'hnl_m_02'       )
        obs_dy_m_triL     = dft_dy.Histo1D(('obs_m_triL',     'obs_m_triL',    len(b_M)-1,      b_M),      'hnl_w_vis_m'    )
              
        obs_tt_pt         = dft_tt.Histo1D(('obs_pt',         'obs_pt',        len(b_pt)-1,     b_pt),     'ptcone'         )
        obs_tt_dr_12      = dft_tt.Histo1D(('obs_dr_12',      'obs_dr_12',     len(b_dR)-1,     b_dR),     'hnl_dr_12'      )
        obs_tt_2disp      = dft_tt.Histo1D(('obs_2disp',      'obs_2disp',     len(b_2d)-1,     b_2d),     'hnl_2d_disp'    )
        obs_tt_2disp_sig  = dft_tt.Histo1D(('obs_2disp_sig',  'obs_2disp_sig', len(b_2d_sig)-1, b_2d_sig), 'hnl_2d_disp_sig')
        obs_tt_m_dimu     = dft_tt.Histo1D(('obs_m_dimu',     'obs_m_dimu',    len(b_m)-1,      b_m),      'hnl_m_12'       )
        obs_tt_BGM_dimu   = dft_tt.Histo1D(('obs_BGM_dimu',   'obs_BGM_dimu',  len(b_M)-1,      b_M),      'hnl_m_12'       )
        obs_tt_BGM_01     = dft_tt.Histo1D(('obs_BGM_01',     'obs_BGM_01',    len(b_M)-1,      b_M),      'hnl_m_01'       )
        obs_tt_BGM_02     = dft_tt.Histo1D(('obs_BGM_02',     'obs_BGM_02',    len(b_M)-1,      b_M),      'hnl_m_02'       )
        obs_tt_m_triL     = dft_tt.Histo1D(('obs_m_triL',     'obs_m_triL',    len(b_M)-1,      b_M),      'hnl_w_vis_m'    )

        h_list = { 'pt'          : [whd_dy_pt,        whd_tt_pt,        obs_dy_pt,        obs_tt_pt,       ';p_{T}^{cone} [GeV]; Counts'], 
                   'dr_12'       : [whd_dy_dr_12,     whd_tt_dr_12,     obs_dy_dr_12,     obs_tt_dr_12,    ';#DeltaR(l_{1},  l_{2}); Counts'], 
                   '2disp'       : [whd_dy_2disp,     whd_tt_2disp,     obs_dy_2disp,     obs_tt_2disp,    ';2d_disp [cm]; Counts'], 
                   '2disp_sig'   : [whd_dy_2disp_sig, whd_tt_2disp_sig, obs_dy_2disp_sig, obs_tt_2disp_sig,';2d_disp_sig ; Counts'], 
                   'm_dimu'      : [whd_dy_m_dimu,    whd_tt_m_dimu,    obs_dy_m_dimu,    obs_tt_m_dimu,    ';m(l_{1},  l_{2}) [GeV]; Counts'], 
                   'M_dimu'      : [whd_dy_BGM_dimu,  whd_tt_BGM_dimu,  obs_dy_BGM_dimu,  obs_tt_BGM_dimu,  ';m(l_{1},  l_{2}) [GeV]; Counts'], 
                   'M_01'        : [whd_dy_BGM_01,    whd_tt_BGM_01,    obs_dy_BGM_01,    obs_tt_BGM_01,    ';m(l_{0},  l_{1}) [GeV]; Counts'], 
                   'M_02'        : [whd_dy_BGM_02,    whd_tt_BGM_02,    obs_dy_BGM_02,    obs_tt_BGM_02,    ';m(l_{0},  l_{2}) [GeV]; Counts'], 
                   'm_triL'      : [whd_dy_m_triL,    whd_tt_m_triL,    obs_dy_m_triL,    obs_tt_m_triL,    ';m(l_{0},  l_{1},  l_{2}) [GeV]; Counts'], }

    for k in h_list.keys():

        print'\n\tdrawing', k 

        if split == False:
            whd = h_list[k][0].GetPtr()
            obs = h_list[k][1].GetPtr()

        if split == True:
            whd_dy = h_list[k][0].GetPtr()
            whd_tt = h_list[k][1].GetPtr()
            obs_dy = h_list[k][2].GetPtr()
            obs_tt = h_list[k][3].GetPtr()

            whd_dy.Add(whd_tt)
            obs_dy.Add(obs_tt)

            whd = whd_dy; obs = obs_dy

        if k == 'pt':
            print '\n\tyields. weighed: %0.2f, observed: %0.2f' %(whd.GetEntries(), obs.GetEntries())

        c = rt.TCanvas(k, k)
        whd.SetLineColor(rt.kGreen+2); whd.SetLineWidth(2); whd.SetMarkerStyle(0)
        whd.SetTitle(h_list[k][4] if split == True else h_list[k][2])
        obs.SetTitle(h_list[k][4] if split == True else h_list[k][2])
        obs.SetMarkerColor(rt.kMagenta+2)
        obs.Draw()
        whd.Draw('histEsame')
        leg = rt.TLegend(0.57, 0.78, 0.80, 0.9)
        leg.AddEntry(obs, 'observed')
        leg.AddEntry(whd, 'expected')
        leg.Draw()
        pf.showlogoprelimsim('CMS')
        pf.showlumi('SFR_'+ch)
        save(c, sample='DDE', ch=ch)
######################################################################################

######################################################################################
def checkStuff(ch='mem',ID='L',eta_split=False):

    l_eta  = {'_eta_all' : '1'}

    if eta_split == True: 
        if ch == 'mem':
            l_eta = {'_eta_00t08' : 'abs(l1_eta) < 0.8', '_eta_08t15' : 'abs(l1_eta) > 0.8 & abs(l1_eta) < 1.479', '_eta_15t25' : 'abs(l1_eta) > 1.479 & abs(l1_eta) < 2.5'}

    for i_eta in l_eta.keys():

        if ch == 'eee':
            chain =rt.TChain('tree')
            chain.Add(eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_eee/partial_25_2/DYJetsToLL_M50/HNLTreeProducer/tree.root')
            chain.Add(eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_eee/partial_25_2/DYJetsToLL_M50_ext/HNLTreeProducer/tree.root')

            d_dy = rdf(chain)
            d_tt = rdf('tree', eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_eee_25_2/partial/TTJets_amcat/HNLTreeProducer/tree.root')

            f0_dy_l0l1 = d_dy.Filter(l0l1_ee)
            f0_dy_l0l2 = d_dy.Filter(l0l2_ee)
            f0_tt_l0l1 = d_tt.Filter(l0l1_ee)
            f0_tt_l0l2 = d_tt.Filter(l0l2_ee)

            if ID=='L':
                f0_dy_l0l1 = f0_dy_l0l1.Filter(l0l1_ee + ' && l1_LooseNoIso == 1')
                f0_dy_l0l2 = f0_dy_l0l2.Filter(l0l2_ee + ' && l2_LooseNoIso == 1')
                f0_tt_l0l1 = f0_tt_l0l1.Filter(l0l1_ee + ' && l1_LooseNoIso == 1')
                f0_tt_l0l2 = f0_tt_l0l2.Filter(l0l2_ee + ' && l2_LooseNoIso == 1')

            if ID=='M':
                f0_dy_l0l1 = f0_dy_l0l1.Filter(l0l1_ee + ' && l1_MediumNoIso == 1')
                f0_dy_l0l2 = f0_dy_l0l2.Filter(l0l2_ee + ' && l2_MediumNoIso == 1')
                f0_tt_l0l1 = f0_tt_l0l1.Filter(l0l1_ee + ' && l1_MediumNoIso == 1')
                f0_tt_l0l2 = f0_tt_l0l2.Filter(l0l2_ee + ' && l2_MediumNoIso == 1')

            if ID=='T':
                f0_dy_l0l1 = f0_dy_l0l1.Filter(l0l1_ee + ' && l1_MediumWithIso == 1')
                f0_dy_l0l2 = f0_dy_l0l2.Filter(l0l2_ee + ' && l2_MediumWithIso == 1')
                f0_tt_l0l1 = f0_tt_l0l1.Filter(l0l1_ee + ' && l1_MediumWithIso == 1')
                f0_tt_l0l2 = f0_tt_l0l2.Filter(l0l2_ee + ' && l2_MediumWithIso == 1')
        

        if ch == 'eem':
            chain =rt.TChain('tree')
            chain.Add(eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_eem/DYJetsToLL_M50/HNLTreeProducer/tree.root')
            chain.Add(eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_eem/DYJetsToLL_M50_ext/HNLTreeProducer/tree.root')

            d_dy = rdf(chain)
            d_tt = rdf('tree', eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_eem/TTJets_amcat/HNLTreeProducer/tree.root')

            f0_dy = d_dy.Filter(l0l1_ee + ' && ' + l2_fake_m_dr)
            f0_tt = d_tt.Filter(l0l1_ee + ' && ' + l2_fake_m_dr)

            if ID=='L':
                f0_dy = d_dy.Filter(l0l1_ee + ' && l2_id_l == 1 && ' + l2_fake_m_dr)
                f0_tt = d_tt.Filter(l0l1_ee + ' && l2_id_l == 1 && ' + l2_fake_m_dr)

            if ID=='M':
                f0_dy = d_dy.Filter(l0l1_ee + ' && l2_id_m == 1 && ' + l2_fake_m_dr)
                f0_tt = d_tt.Filter(l0l1_ee + ' && l2_id_m == 1 && ' + l2_fake_m_dr)

            if ID=='MM':
                f0_dy = d_dy.Filter(l0l1_ee + ' && l2_Medium == 1 && ' + l2_fake_m_dr)
                f0_tt = d_tt.Filter(l0l1_ee + ' && l2_Medium == 1 && ' + l2_fake_m_dr)


        if ch == 'mem':
            chain =rt.TChain('tree')
            chain.Add(eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_mem/DYJetsToLL_M50/HNLTreeProducer/tree.root')
#            chain.Add('/work/dezhu/4_production/production_20190306_BkgMC/mem/ntuples/DYJetsToLL_M50/HNLTreeProducer/tree.root')
            chain.Add(eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_mem/DYJetsToLL_M50_ext/HNLTreeProducer/tree.root')
#            chain.Add('/work/dezhu/4_production/production_20190306_BkgMC/mem/ntuples/DYJetsToLL_M50_ext/HNLTreeProducer/tree.root')

            d_dy = rdf(chain)
            d_tt = rdf('tree', eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_mem/TTJets_amcat/HNLTreeProducer/tree.root')
#            d_tt = rdf('tree', '/work/dezhu/4_production/production_20190306_BkgMC/mem/ntuples/TTJets/HNLTreeProducer/tree.root')

            #FIXME TODO DEBUGGING FEB 22/MAR 13 discrepancy
            base_l0l2_mm  = 'l0_pt > 15 && l2_pt > 5 && l0_id_m && l2_id_m && l0_reliso_rho_03 < 0.15 && l2_reliso_rho_03 < 0.15'
            base_l0l2_mm += ' && l0_q * l2_q < 0 && abs(l0_dxy) < 0.05 && abs(l2_dxy) < 0.05'

            base = base_l0l2_mm + ' && ' + l_eta[i_eta]

            print '\n\t',base    

            f0_dy = d_dy.Filter(base)
            f0_tt = d_tt.Filter(base)

            if ID=='L':
                f0_dy = d_dy.Filter(base + ' && l1_LooseNoIso == 1')
                f0_tt = d_tt.Filter(base + ' && l1_LooseNoIso == 1')

            if ID=='M':
                f0_dy = d_dy.Filter(base + ' && l1_MediumNoIso == 1')
                f0_tt = d_tt.Filter(base + ' && l1_MediumNoIso == 1')

            if ID=='T':
                f0_dy = d_dy.Filter(base + ' && l1_MediumWithIso == 1')
                f0_tt = d_tt.Filter(base + ' && l1_MediumWithIso == 1')

        n_d_dy = d_dy.Count()
        n_d_tt = d_tt.Count()

    #    if not ch =='eee': 

    #        f0_dy = f0_dy.Define('abs_l1_dxy', 'abs(l1_dxy)') 
    #        f0_tt = f0_tt.Define('abs_l1_dxy', 'abs(l1_dxy)') 

    #        f0_dy = f0_dy.Define('l1_abs_iso_rho', 'l1_reliso_rho_03 * l1_pt') 
    #        f0_tt = f0_tt.Define('l1_abs_iso_rho', 'l1_reliso_rho_03 * l1_pt') 

    #        f0_dy = f0_dy.Define('l1_abs_iso_db', 'l1_reliso05 * l1_pt') 
    #        f0_tt = f0_tt.Define('l1_abs_iso_db', 'l1_reliso05 * l1_pt') 

    #        n_f0_dy = f0_dy.Count()
    #        n_f0_tt = f0_tt.Count()

        if ch in ['eee','mmm']:
            n_f0_dy_l0l1 = f0_dy_l0l1.Count()
            n_f0_dy_l0l2 = f0_dy_l0l2.Count()
            n_f0_tt_l0l1 = f0_tt_l0l1.Count()
            n_f0_tt_l0l2 = f0_tt_l0l2.Count()
       
        if ch in ['eem','mem']:

            n_f0_dy = f0_dy.Count()
            n_f0_tt = f0_tt.Count()

    #        f0_dy_l0l1 = f0_dy_l0l1.Define('abs_l1_dxy', 'abs(l1_dxy)') 
    #        f0_tt_l0l2 = f0_tt_l0l2.Define('abs_l1_dxy', 'abs(l1_dxy)') 

        SFR, DFR, dirs = selectCuts(ch)

        l0l1, l0l2, l1_loose, l2_loose, l1_lnt, l2_lnt, l1_tight, l2_tight = SFR 

        # ele
        vars = {'reliso_rho_03':[1500,0.01,15.01]}#, 'reliso05':[1500,0.01,15.01]}
        #'pt':[50,0.,102],  'abs_iso_rho': [150,0,150], 'abs_iso_db': [150,0,150]}#,  'l2_pt':[50,2,102], 'l0_pt':[50,2,102], 'abs_dxy':[60,0.05,3.05]}
        
        # mu
    #    vars = { 'reliso_dB_05':[1500,0.01,15.01], 'reliso_rho_03':[1500,0.01,15.01]}

        if ch =='eem': 
            print'\n\tDY after pre-sel: %d, initial: %d'   %(n_f0_dy.GetValue(), n_d_dy.GetValue())
            print'\n\tTT after pre-sel: %d, initial: %d\n' %(n_f0_tt.GetValue(), n_d_tt.GetValue())

        if ch =='mem': 
            print'\n\tDY after pre-sel: %d, initial: %d'   %(n_f0_dy.GetValue(), n_d_dy.GetValue())
            print'\n\tTT after pre-sel: %d, initial: %d\n' %(n_f0_tt.GetValue(), n_d_tt.GetValue())

        if ch == 'eee':
            print'\n\tDY after pre-sel: %d, initial: %d'   %(n_f0_dy_l0l1.GetValue(), n_d_dy.GetValue())
            print'\n\tDY after pre-sel: %d, initial: %d'   %(n_f0_dy_l0l2.GetValue(), n_d_dy.GetValue())
            print'\n\tTT after pre-sel: %d, initial: %d'   %(n_f0_tt_l0l1.GetValue(), n_d_tt.GetValue())
            print'\n\tTT after pre-sel: %d, initial: %d\n' %(n_f0_tt_l0l2.GetValue(), n_d_tt.GetValue())
     
        for var in vars.keys():

            print'\n\t%s: drawing %s \n' %(i_eta,var)

            if ch =='eem': 
                h_dy = f0_dy.Histo1D(('l2_'+var+'DY','l2_'+var+'DY',vars[var][0],vars[var][1],vars[var][2]),'l2_'+var)
                h_tt = f0_tt.Histo1D(('l2_'+var+'TT','l2_'+var+'TT',vars[var][0],vars[var][1],vars[var][2]),'l2_'+var)

            if ch =='mem': 
                h_dy = f0_dy.Histo1D(('l1_'+var+'DY','l1_'+var+'DY',vars[var][0],vars[var][1],vars[var][2]),'l1_'+var)
                h_tt = f0_tt.Histo1D(('l1_'+var+'TT','l1_'+var+'TT',vars[var][0],vars[var][1],vars[var][2]),'l1_'+var)

            if ch == 'eee':
                h_dy_l0l1= f0_dy_l0l1.Histo1D(('l1_'+var+'DY_l0l1','l1_'+var+'DY_l0l1',vars[var][0],vars[var][1],vars[var][2]),'l1_'+var)
                h_dy_l0l2= f0_dy_l0l2.Histo1D(('l2_'+var+'DY_l0l2','l2_'+var+'DY_l0l2',vars[var][0],vars[var][1],vars[var][2]),'l2_'+var)
                h_tt_l0l1= f0_tt_l0l1.Histo1D(('l1_'+var+'TT_l0l1','l1_'+var+'TT_l0l1',vars[var][0],vars[var][1],vars[var][2]),'l1_'+var)
                h_tt_l0l2= f0_tt_l0l2.Histo1D(('l2_'+var+'TT_l0l2','l2_'+var+'TT_l0l2',vars[var][0],vars[var][1],vars[var][2]),'l2_'+var)

                h_dy_l0l1.Add(h_dy_l0l2); h_dy = h_dy_l0l1
                h_tt_l0l1.Add(h_tt_l0l2); h_tt = h_tt_l0l1

            h_dy.SetMarkerStyle(1); h_dy.SetMarkerSize(0.7); h_dy.SetMarkerColor(rt.kGreen+2); h_dy.SetTitle('DY')
            h_tt.SetMarkerStyle(1); h_tt.SetMarkerSize(0.7); h_tt.SetMarkerColor(rt.kRed+2);   h_tt.SetTitle('TT')

            CH=ch
            if l_eta[i_eta] != '1': CH=ch+i_eta

            c = rt.TCanvas(var,var)
            h_dy.DrawNormalized()
            h_tt.DrawNormalized('same')
            c.BuildLegend()
            pf.showlogoprelimsim('CMS')
            pf.showlumi(CH+'_'+var)
            save(c, sample='DY_TT_ID'+ID, ch=CH)
######################################################################################

######################################################################################
def getIsoCDF(ch='mem',ID='No',eta='1',mode='rho', abs=False):

        #ch = 'isoNo_'+ch
        ID = 'ID'+ID
        if eta in ['00t08', '08t15', '15t25']: ch += '_eta_' + eta
        #cumulative
        h_dy_c     = rt.TH1F('iso_c_dy', 'iso_c_dy',  1500,0.01,15.01)
        h_tt_c     = rt.TH1F('iso_c_tt', 'iso_c_tt',  1500,0.01,15.01)
        h_dy_by_tt = rt.TH1F('iso_c_div','iso_c_div', 1500,0.01,15.01)

        h_dy_c.SetMarkerStyle(1); h_dy_c.SetMarkerSize(0.5); h_dy_c.SetLineColor(rt.kGreen+2); h_dy_c.SetMarkerColor(rt.kGreen+2); h_dy_c.SetTitle('DY')
        h_tt_c.SetMarkerStyle(1); h_tt_c.SetMarkerSize(0.5); h_tt_c.SetLineColor(rt.kRed+2);   h_tt_c.SetMarkerColor(rt.kRed+2);   h_tt_c.SetTitle('TT')

        if mode == 'rho':
            h_dy = rt.TFile(plotDir+'DY_TT_'+ID+'_'+ch+'_reliso_rho_03.root').Get('reliso_rho_03').GetPrimitive('l1_reliso_rho_03DY')
            h_tt = rt.TFile(plotDir+'DY_TT_'+ID+'_'+ch+'_reliso_rho_03.root').Get('reliso_rho_03').GetPrimitive('l1_reliso_rho_03TT')

#           if abs== True:
#               h_dy = rt.TFile(plotDir+'DY_TT_mem_abs_iso_rho.root').Get('abs_iso_rho').GetPrimitive('l1_abs_iso_rhoDY')
#               h_tt = rt.TFile(plotDir+'DY_TT_mem_abs_iso_rho.root').Get('abs_iso_rho').GetPrimitive('l1_abs_iso_rhoTT')

        if mode == 'db':
            h_dy = rt.TFile(plotDir+'DY_TT_'+ch+'_reliso05.root').Get('reliso05').GetPrimitive('l1_reliso05DY')
            h_tt = rt.TFile(plotDir+'DY_TT_'+ch+'_reliso05.root').Get('reliso05').GetPrimitive('l1_reliso05TT')

#           if abs== True:
#               h_dy = rt.TFile(plotDir+'DY_TT_mem_abs_iso_db.root').Get('abs_iso_db').GetPrimitive('l1_abs_iso_dbDY')
#               h_tt = rt.TFile(plotDir+'DY_TT_mem_abs_iso_db.root').Get('abs_iso_db').GetPrimitive('l1_abs_iso_dbTT')
 
#        mode += '_abs'

        binCont_dy = 0
        binCont_tt = 0
        nBins = range(1500)
        for i in nBins:
            binCont_dy += h_dy.GetBinContent(i+1)
            binCont_tt += h_tt.GetBinContent(i+1)
            h_dy_c.SetBinContent(i+1, binCont_dy) 
            h_tt_c.SetBinContent(i+1, binCont_tt)

        h_dy_by_tt.Divide(h_dy_c,h_tt_c)

        c = rt.TCanvas('iso_c_'+mode,'iso_c_'+mode)
        h_dy_c.Draw()
        h_tt_c.Draw('same')
        c.BuildLegend()
        pf.showlogoprelimsim('CMS')
        pf.showlumi(ch+'_iso_cdf_'+mode)
        save(c, sample='DY_TT_'+ID, ch=ch)

        c = rt.TCanvas('iso_c_div_'+mode,'iso_c_div_'+mode)
        h_dy_by_tt.Draw()
        pf.showlogoprelimsim('CMS')
        pf.showlumi(ch+'_iso_cdf_div_'+mode)
        save(c, sample='DY_TT_'+ID, ch=ch)
####################################################################################################

####################################################################################################
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


    if channel == 'eem':
        DYBB_dir       =   DYBBDir_eem     
        DY10_dir       =   DY10Dir_eem      
        DY50_dir       =   DY50Dir_eem      
        DY50_ext_dir   =   DY50_extDir_eem 
        W_dir          =   W_dir_eem
        W_ext_dir      =   W_ext_dir_eem
        TT_dir         =   TT_dir_eem

        TIGHT          =   DFR_TIGHT_EMM
        LOOSE          =   DFR_LOOSE_EMM
        LOOSENOTTIGHT  =   DFR_LOOSENOTTIGHT_EMM

        l0l1           = l0l1_ee
        l0l2           = l0l2_em
        l1_loose       = l1_e_loose
        l2_loose       = l2_m_loose
        l1_lnt         = l1_e_lnt  
        l2_lnt         = l2_m_lnt  
        l1_tight       = l1_e_tight
        l2_tight       = l2_m_tight


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
        l0_is_fake_sh       = None #l0_fake_m_sh
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
######################################################################################

######################################################################################
# https://stackoverflow.com/questions/616645/how-to-duplicate-sys-stdout-to-a-log-file
class Logger(object):
    def __init__(self, fileName):
        self.terminal = sys.stdout
        self.log = open(fileName+'.log', 'a')

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message) 
