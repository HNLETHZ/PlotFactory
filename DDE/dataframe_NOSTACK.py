from __future__ import division
from ROOT import gROOT as gr
from ROOT import RDataFrame as rdf
import os, platform
import ROOT as rt
import numpy as np
import plotfactory as pf
from glob import glob
import re, sys
from datetime import datetime
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
###########################################################################################################################################################################################
skimDir = eos+'ntuples/skimmed_trees/'
plotDir = eos+'plots/DDE/'
suffix  = 'HNLTreeProducer/tree.root'
###########################################################################################################################################################################################
DYBBDir_mee     = eos_david+'ntuples/HN3Lv2.0/background/montecarlo/mee/partial/DYBB/'
DY50Dir_mee     = eos_david+'ntuples/HN3Lv2.0/background/montecarlo/mee/partial/DYJetsToLL_M50/'
DY50_extDir_mee = eos_david+'ntuples/HN3Lv2.0/background/montecarlo/mee/partial/DYJetsToLL_M50_ext/'
DY10Dir_mee     = eos_david+'ntuples/HN3Lv2.0/background/montecarlo/mee/partial/DYJetsToLL_M10to50/'
TT_dir_mee      = eos_david+'ntuples/HN3Lv2.0/background/montecarlo/mee/partial/TTJets_amcat_20190130/'  
W_dir_mee       = eos_david+'ntuples/HN3Lv2.0/background/montecarlo/mee/20190129/ntuples/WJetsToLNu/'
W_ext_dir_mee   = eos_david+'ntuples/HN3Lv2.0/background/montecarlo/mee/20190129/ntuples/WJetsToLNu_ext/'
###########################################################################################################################################################################################
# version with last plots 3_15_19
DYBBDir_mem     = eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_mem/DYBB/'
DY50Dir_mem     = eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_mem/DYJetsToLL_M50/'
DY50_extDir_mem = eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_mem/DYJetsToLL_M50_ext/'
DY10Dir_mem     = eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_mem/DYJetsToLL_M10to50/'
TT_dir_mem      = eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_mem/TTJets_amcat/'  
W_dir_mem       = eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_mem/WJetsToLNu/'
W_ext_dir_mem   = eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_mem/WJetsToLNu_ext/'
###########################################################################################################################################################################################
# latest version 3_18_19
DYBBDir_mem     = eos_david+'ntuples/HN3Lv2.0/background/montecarlo/production20190318/mem/ntuples/DYBB/'
DY50Dir_mem     = eos_david+'ntuples/HN3Lv2.0/background/montecarlo/production20190318/mem/ntuples/DYJetsToLL_M50/'
DY50_extDir_mem = eos_david+'ntuples/HN3Lv2.0/background/montecarlo/production20190318/mem/ntuples/DYJetsToLL_M50_ext/'
DY10Dir_mem     = eos_david+'ntuples/HN3Lv2.0/background/montecarlo/production20190318/mem/ntuples/DYJetsToLL_M10to50/'
TT_dir_mem      = eos_david+'ntuples/HN3Lv2.0/background/montecarlo/production20190318/mem/ntuples/TTJets/'  
W_dir_mem       = eos_david+'ntuples/HN3Lv2.0/background/montecarlo/production20190318/mem/ntuples/WJetsToLNu/'
W_ext_dir_mem   = eos_david+'ntuples/HN3Lv2.0/background/montecarlo/production20190318/mem/ntuples/WJetsToLNu_ext/'
###########################################################################################################################################################################################
DYBBDir_mmm     = eos_david+'ntuples/HN3Lv2.0/background/montecarlo/production20190318/mmm/ntuples/DYBB/'
DY50Dir_mmm     = eos_david+'ntuples/HN3Lv2.0/background/montecarlo/production20190318/mmm/ntuples/DYJetsToLL_M50/'
DY50_extDir_mmm = eos_david+'ntuples/HN3Lv2.0/background/montecarlo/production20190318/mmm/ntuples/DYJetsToLL_M50_ext/'
DY10Dir_mmm     = eos_david+'ntuples/HN3Lv2.0/background/montecarlo/production20190318/mmm/ntuples/DYJetsToLL_M10to50/'
TT_dir_mmm      = eos_david+'ntuples/HN3Lv2.0/background/montecarlo/production20190318/mmm/ntuples/TTJets/'  
W_dir_mmm       = eos_david+'ntuples/HN3Lv2.0/background/montecarlo/production20190318/mmm/ntuples/WJetsToLNu/'
W_ext_dir_mmm   = eos_david+'ntuples/HN3Lv2.0/background/montecarlo/production20190318/mmm/ntuples/WJetsToLNu_ext/'
#######################################################################################################################################################################################################
DYBBDir_eee     = eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_eee/partial/DYBB/'
DY50Dir_eee     = eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_eee/partial/DYJetsToLL_M50/'
DY50_extDir_eee = eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_eee/partial/DYJetsToLL_M50_ext/'
DY10Dir_eee     = eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_eee/partial/DYJetsToLL_M10to50/'
TT_dir_eee      = eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_eee/partial/TTJets_amcat/'  
W_dir_eee       = eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_eee/partial/WJetsToLNu/'
W_ext_dir_eee   = eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_eee/partial/WJetsToLNu_ext/'
###########################################################################################################################################################################################
DYBBDir_eem     = eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_eem/DYBB/'
DY50Dir_eem     = eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_eem/DYJetsToLL_M50/'
DY50_extDir_eem = eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_eem/DYJetsToLL_M50_ext/'
DY10Dir_eem     = eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_eem/DYJetsToLL_M10to50/'
TT_dir_eem      = eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_eem/TTJets_amcat/'  
W_dir_eem       = eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_eem/WJetsToLNu/'
W_ext_dir_eem   = eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_eem/WJetsToLNu_ext/'
###########################################################################################################################################################################################
##### GEN MATCHING: DELTA PHI PERIODICITY
###########################################################################################################################################################################################
dPhi00  =  '( (l0_phi-l0_gen_match_phi + 2*TMath::Pi()) * (l0_phi-l0_gen_match_phi < -TMath::Pi()) + (l0_phi-l0_gen_match_phi - 2*TMath::Pi()) * (l0_phi-l0_gen_match_phi > TMath::Pi())'\
           ' + (l0_phi-l0_gen_match_phi) * ( (l0_phi-l0_gen_match_phi > -TMath::Pi()) && (l0_phi-l0_gen_match_phi < TMath::Pi()) ) )' 

dPhi11  =  '( (l1_phi-l1_gen_match_phi + 2*TMath::Pi()) * (l1_phi-l1_gen_match_phi < -TMath::Pi()) + (l1_phi-l1_gen_match_phi - 2*TMath::Pi()) * (l1_phi-l1_gen_match_phi > TMath::Pi())'\
           ' + (l1_phi-l1_gen_match_phi) * ( (l1_phi-l1_gen_match_phi > -TMath::Pi()) && (l1_phi-l1_gen_match_phi < TMath::Pi()) ) )' 

dPhi22  =  '( (l2_phi-l2_gen_match_phi + 2*TMath::Pi()) * (l2_phi-l2_gen_match_phi < -TMath::Pi()) + (l2_phi-l2_gen_match_phi - 2*TMath::Pi()) * (l2_phi-l2_gen_match_phi > TMath::Pi())'\
           ' + (l2_phi-l2_gen_match_phi) * ( (l2_phi-l2_gen_match_phi > -TMath::Pi()) && (l2_phi-l2_gen_match_phi < TMath::Pi()) ) )' 
###########################################################################################################################################################################################
##### GEN MATCHING: DEFINE PROMPT AND FAKE LEPTONS
###########################################################################################################################################################################################
l0_prompt_m_dr =  '( (l0_gen_match_isDirectPromptTauDecayProductFinalState == 1 || l0_gen_match_isDirectHardProcessTauDecayProductFinalState == 1'
l0_prompt_m_dr += ' || l0_gen_match_fromHardProcessFinalState == 1 || l0_gen_match_isPromptFinalState == 1) && abs(l0_gen_match_pdgid) == 13'#&& l0_is_real == 1'
l0_prompt_m_dr += ' && sqrt( pow((l0_eta-l0_gen_match_eta),2) + pow((' + dPhi00 + '),2) ) < 0.04 )' 

l1_prompt_m_dr =  '( (l1_gen_match_isDirectPromptTauDecayProductFinalState == 1 || l1_gen_match_isDirectHardProcessTauDecayProductFinalState == 1'
l1_prompt_m_dr += ' || l1_gen_match_fromHardProcessFinalState == 1 || l1_gen_match_isPromptFinalState == 1) && abs(l1_gen_match_pdgid) == 13'#&& l1_is_real == 1'
l1_prompt_m_dr += ' && sqrt( pow((l1_eta-l1_gen_match_eta),2) + pow((' + dPhi11 + '),2) ) < 0.04 )'

l2_prompt_m_dr =  '( (l2_gen_match_isDirectPromptTauDecayProductFinalState == 1 || l2_gen_match_isDirectHardProcessTauDecayProductFinalState == 1'
l2_prompt_m_dr += ' || l2_gen_match_fromHardProcessFinalState == 1 || l2_gen_match_isPromptFinalState == 1) && abs(l2_gen_match_pdgid) == 13'#&& l2_is_real == 1'
l2_prompt_m_dr += ' && sqrt( pow((l2_eta-l2_gen_match_eta),2) + pow((' + dPhi22 + '),2) ) < 0.04 )' 

l0_prompt_e_dr =  '( (l0_gen_match_isDirectPromptTauDecayProductFinalState == 1 || l0_gen_match_isDirectHardProcessTauDecayProductFinalState == 1'
l0_prompt_e_dr += ' || l0_gen_match_fromHardProcessFinalState == 1 || l0_gen_match_isPromptFinalState == 1) && ( abs(l0_gen_match_pdgid) == 11 || abs(l0_gen_match_pdgid) == 22 )'
l0_prompt_e_dr += ' && sqrt( pow((l0_eta-l0_gen_match_eta),2) + pow((' + dPhi00 + '),2) ) < 0.04 )'

l1_prompt_e_dr =  '( (l1_gen_match_isDirectPromptTauDecayProductFinalState == 1 || l1_gen_match_isDirectHardProcessTauDecayProductFinalState == 1'
l1_prompt_e_dr += ' || l1_gen_match_fromHardProcessFinalState == 1 || l1_gen_match_isPromptFinalState == 1) && ( abs(l1_gen_match_pdgid) == 11 || abs(l1_gen_match_pdgid) == 22 )'
l1_prompt_e_dr += ' && sqrt( pow((l1_eta-l1_gen_match_eta),2) + pow((' + dPhi11 + '),2) ) < 0.04 )'

l1_prompt_e_dr_noConv  = '( (l1_gen_match_isDirectPromptTauDecayProductFinalState == 1 || l1_gen_match_isDirectHardProcessTauDecayProductFinalState == 1'
l1_prompt_e_dr_noConv += ' || l1_gen_match_fromHardProcessFinalState == 1 || l1_gen_match_isPromptFinalState == 1) && abs(l1_gen_match_pdgid) == 11'
l1_prompt_e_dr_noConv += ' && sqrt( pow((l1_eta-l1_gen_match_eta),2) + pow((' + dPhi11 + '),2) ) < 0.04 )'

l2_prompt_e_dr =  '( (l2_gen_match_isDirectPromptTauDecayProductFinalState == 1 || l2_gen_match_isDirectHardProcessTauDecayProductFinalState == 1'
l2_prompt_e_dr += ' || l2_gen_match_fromHardProcessFinalState == 1 || l2_gen_match_isPromptFinalState == 1) && ( abs(l2_gen_match_pdgid) == 11 || abs(l2_gen_match_pdgid) == 22 )'
l2_prompt_e_dr += ' && sqrt( pow((l2_eta-l2_gen_match_eta),2) + pow((' + dPhi22 + '),2) ) < 0.04 )'

l0_fake_m_dr = '( !' + l0_prompt_m_dr + ' )' 
l1_fake_m_dr = '( !' + l1_prompt_m_dr + ' )' 
l2_fake_m_dr = '( !' + l2_prompt_m_dr + ' )' 

l0_fake_e_dr = '( !' + l0_prompt_e_dr + ' )' 
l1_fake_e_dr = '( !' + l1_prompt_e_dr + ' )' 
l2_fake_e_dr = '( !' + l2_prompt_e_dr + ' )' 

l1_fake_e_dr_noConv = '( !' + l1_prompt_e_dr_noConv + ' )' 
###########################################################################################################################################################################################
              ##               LOOSE / TIGHT REGIONS                ##
DFR_LOOSE_MEE          = None
DFR_LOOSENOTTIGHT_MEE  = None
DFR_TIGHT_MEE          = None
######################## None
# FIXME
DFR_LOOSE_MEM          = None
DFR_LOOSENOTTIGHT_MEM  = None
DFR_TIGHT_MEM          = None
######################## None
DFR_LOOSE_MMM         =  None
DFR_LOOSENOTTIGHT_MMM =  None
DFR_TIGHT_MMM         =  None
######################## None
DFR_LOOSE_EEE         =  None
DFR_LOOSENOTTIGHT_EEE =  None
DFR_TIGHT_EEE         =  None
######################## None
DFR_LOOSE_EMM         =  None
DFR_LOOSENOTTIGHT_EMM =  None
DFR_TIGHT_EMM         =  None
###########################################################################################################################################################################################
              ##                 SINGLE FAKE RATE                   ##  
###########################################################################################################################################################################################
### RICCARDO 19_3_19
l0l2_mm  = 'l0_pt > 25 && abs(l0_eta) < 2.4 && l0_id_m == 1 && abs(l0_dz) < 0.2 && abs(l0_dxy) < 0.05 && l0_reliso_rho_03 < 0.2'      # l0 genuine
l0l2_mm += ' && l2_pt > 10 && abs(l2_eta) < 2.4 && l2_id_m == 1 && abs(l2_dz) < 0.2 && abs(l2_dxy) < 0.05 && l2_reliso_rho_03 < 0.2'  # l2 genuine 
l0l2_mm += ' && hnl_q_02 == 0'                                                                                                        # opposite charge

l1_e_loose  = 'l1_pt > 5 && abs(l1_eta) < 2.5 && abs(l1_dz) < 2 && abs(l1_dxy) > 0.05'                                              # l1 kinematics and impact parameter
#l1_e_loose += ' && l1_gen_match_pdgid != 22'                                                                                          # no conversions 

#l1_e_loose += ' && l1_reliso_rho_03 < .35'                                                                                            # reliso bound for LOOSE cf. checkIso_mem_220319 

l1_e_tight = l1_e_loose + ' && l1_MediumNoIso == 1 && l1_reliso_rho_03 < 0.2'
l1_e_lnt   = l1_e_loose + ' && (l1_MediumNoIso == 0 || l1_reliso_rho_03 > 0.2)'

### LET'S DO THE SAME FOR MMM 22_3_19
l1_m_loose  = 'l1_pt > 5 && abs(l1_eta) < 2.4 && abs(l1_dz) < 2 && abs(l1_dxy) > 0.05'                                              # l1 kinematics and impact parameter
#l1_m_loose += ' && l1_gen_match_pdgid != 22'                                                                                          # no conversions 

#l1_m_loose += ' && l1_reliso_rho_03 < 0.5'                                                                                            # reliso bound for LOOSE cf. checkIso_mmm_220319 

l1_m_tight = l1_m_loose + ' && l1_Medium == 1 && l1_reliso_rho_03 < 0.2'
l1_m_lnt   = l1_m_loose + ' && (l1_Medium == 0 || l1_reliso_rho_03 > 0.2)'

l0l1_mm  = 'l0_pt > 25 && abs(l0_eta) < 2.4 && l0_id_m == 1 && abs(l0_dz) < 0.2 && abs(l0_dxy) < 0.05 && l0_reliso_rho_03 < 0.2'      # l0 genuine
l0l1_mm += ' && l1_pt > 10 && abs(l1_eta) < 2.4 && l1_id_m == 1 && abs(l1_dz) < 0.2 && abs(l1_dxy) < 0.05 && l1_reliso_rho_03 < 0.2'  # l1 genuine 
l0l1_mm += ' && hnl_q_01 == 0'                                                                                                        # opposite charge

l2_m_loose  = 'l2_pt > 5 && abs(l2_eta) < 2.4 && abs(l2_dz) < 2 && abs(l2_dxy) > 0.05'                                              # l2 kinematics and impact parameter

#l2_m_loose += ' && l2_reliso_rho_03 < 0.5'                                                                                            # reliso bound for LOOSE cf. checkIso_mmm_220319 

l2_m_tight = l2_m_loose + ' && l2_Medium == 1 && l2_reliso_rho_03 < 0.2'
l2_m_lnt   = l2_m_loose + ' && (l2_Medium == 0 || l2_reliso_rho_03 > 0.2)'

### AND EEM
l0l1_ee  = 'l0_pt > 27 && abs(l0_eta) < 2.5 && l0_id_t == 1 && abs(l0_dz) < 0.2 && abs(l0_dxy) < 0.05 && l0_reliso_rho_03 < 0.2'      # l0 genuine
l0l1_ee += ' && l1_pt > 15 && abs(l1_eta) < 2.5 && l1_id_t == 1 && abs(l1_dz) < 0.2 && abs(l1_dxy) < 0.05 && l1_reliso_rho_03 < 0.2'  # l1 genuine 
l0l1_ee += ' && hnl_q_01 == 0'                                                                                                        # opposite charge
###########################################################################################################################################################################################
### FAKEABLE OBJECTS AND PROMPT LEPTON DEFINITIONS
###########################################################################################################################################################################################
### PROMPT LEPTONS
l0_m = 'l0_pt > 27 && abs(l0_eta) < 2.4 && abs(l0_dz) < 0.2 && abs(l0_dxy) < 0.05 && l0_reliso_rho_04 < 0.2 && l0_id_t == 1'                  # l0 genuine muon

l1_m = 'l1_pt > 15 && abs(l1_eta) < 2.4 && abs(l1_dz) < 0.2 && abs(l1_dxy) < 0.05 && l1_reliso_rho_04 < 0.2 && l1_id_t == 1'                  # l1 genuine muon 

l2_m = 'l2_pt > 15 && abs(l2_eta) < 2.4 && abs(l2_dz) < 0.2 && abs(l2_dxy) < 0.05 && l2_reliso_rho_04 < 0.2 && l2_id_t == 1'                  # l2 genuine muon 

l0_e = 'l0_pt > 27 && abs(l0_eta) < 2.5 && abs(l0_dz) < 0.2 && abs(l0_dxy) < 0.05 && l0_reliso_rho_04 < 0.2 && l0_eid_mva_iso_wp90 == 1'      # l0 genuine electron

l1_e = 'l1_pt > 15 && abs(l1_eta) < 2.5 && abs(l1_dz) < 0.2 && abs(l1_dxy) < 0.05 && l1_reliso_rho_04 < 0.2 && l1_eid_mva_iso_wp90 == 1'      # l1 genuine electron 

l2_e = 'l2_pt > 15 && abs(l2_eta) < 2.5 && abs(l2_dz) < 0.2 && abs(l2_dxy) < 0.05 && l2_reliso_rho_04 < 0.2 && l2_eid_mva_iso_wp90 == 1'      # l2 genuine electron 

### FAKEABLE OBJECTS
l1_m_loose  = 'l1_pt > 5 && abs(l1_eta) < 2.4 && abs(l1_dz) < 0.2 && abs(l1_dxy) > 0.05'                                              # l1 kinematics and impact parameter
l1_m_tight  = l1_m_loose + ' &&  l1_Medium == 1 && l1_reliso_rho_04 < 0.2'
l1_m_lnt    = l1_m_loose + ' && (l1_Medium == 0 || l1_reliso_rho_04 > 0.2)'

l2_m_loose  = 'l2_pt > 5 && abs(l2_eta) < 2.4 && abs(l2_dz) < 0.2 && abs(l2_dxy) > 0.05'                                              # l2 kinematics and impact parameter
l2_m_tight  = l2_m_loose + ' &&  l2_Medium == 1 && l2_reliso_rho_04 < 0.2'
l2_m_lnt    = l2_m_loose + ' && (l2_Medium == 0 || l2_reliso_rho_04 > 0.2)'

l1_e_loose  = 'l1_pt > 5 && abs(l1_eta) < 2.5 && abs(l1_dz) < 0.2 && abs(l1_dxy) > 0.05'                                              # l1 kinematics and impact parameter
l1_e_tight  = l1_e_loose + ' &&  l1_MediumNoIso == 1 && l1_reliso_rho_04 < 0.2'
l1_e_lnt    = l1_e_loose + ' && (l1_MediumNoIso == 0 || l1_reliso_rho_04 > 0.2)'

l2_e_loose  = 'l2_pt > 5 && abs(l2_eta) < 2.5 && abs(l2_dz) < 0.2 && abs(l2_dxy) > 0.05'                                              # l2 kinematics and impact parameter
l2_e_tight  = l2_e_loose + ' &&  l2_MediumNoIso == 1 && l2_reliso_rho_04 < 0.2'
l2_e_lnt    = l2_e_loose + ' && (l2_MediumNoIso == 0 || l2_reliso_rho_04 > 0.2)'

# TRY TO BUILD DFR OUT OF THE ABOVE
i:


### ADDTIONAL CUTS
ADD_SFR_L0L2 = 'hnl_q_02 == 0'                                                                                                        # opposite charge
ADD_SFR_L0L1 = 'hnl_q_01 == 0'                                                                                                        # opposite charge

SFR_LOOSE_MEM_L1 = ' && l1_reliso_rho_04 < 1.0'                                                                                            # reliso bound for LOOSE cf. checkIso_mem_220319 

SFR_LOOSE_MMM_L1 = ' && l1_reliso_rho_04 < 0.5'                                                                                            # reliso bound for LOOSE cf. checkIso_mmm_220319 
SFR_LOOSE_MMM_L2 = ' && l2_reliso_rho_04 < 0.5'                                                                                            # reliso bound for LOOSE cf. checkIso_mmm_220319 

###########################################################################################################################################################################################
### ENERGY-IN-CONE CORRECTED PT
###########################################################################################################################################################################################
PTCONE   = '(  ( hnl_hn_vis_pt * (hnl_iso03_rel_rhoArea<0.2) ) + ( (hnl_iso03_rel_rhoArea>=0.2) * ( hnl_hn_vis_pt * (1. + hnl_iso03_rel_rhoArea - 0.2) ) )  )'
PTCONEL1 = '(  ( l1_pt * (l1_reliso_rho_03<0.2) ) + ( (l1_reliso_rho_03>=0.2) * ( l1_pt * (1. + l1_reliso_rho_03 - 0.2) ) )  )'
PTCONEL2 = '(  ( l2_pt * (l2_reliso_rho_03<0.2) ) + ( (l2_reliso_rho_03>=0.2) * ( l2_pt * (1. + l2_reliso_rho_03 - 0.2) ) )  )'
###########################################################################################################################################################################################
### BINNING FOR CLOSURE TEST 
###########################################################################################################################################################################################
b_pt_std    = np.arange(5.,105,5)
b_pt        = np.array([ 0., 5., 10., 15., 20., 25., 35., 50., 70.])
#b_2d        = np.arange(0., 10, 0.2)
b_2d        = np.arange(0., 11, 1)
#b_2d_sig    = np.arange(0., 50, 0.25)
#b_2d_sig    = np.arange(0., 100, 0.5)
b_2d_sig    = np.arange(0., 105, 5)
#b_m         = np.arange(0., 5.25, 0.25)
b_m         = np.arange(0.,11,1)
#b_M         = np.arange(0.,202,2)
b_M         = np.arange(0.,210,10)
b_eta       = np.array([0., 1.2, 2.1, 2.4]) 
#b_rho       = np.arange(-100.,100,4)
b_rho       = np.arange(0.,15,0.25)
b_rho_crs   = np.arange(0.,10,0.25)
#b_dR        = np.arange(0.,6.05,0.05)
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
def selectBins(ch='mem',lep=1):

    l_pt   = { '_pt0t5'   : 'ptcone < 5',                  '_pt5t10' : 'ptcone > 5 && ptcone < 10',  '_pt10t15' : 'ptcone > 10 && ptcone < 15', '_pt15t20' : 'ptcone > 15 && ptcone < 20',
               '_pt20t25' : 'ptcone > 20 && ptcone < 25', '_pt25t35' : 'ptcone > 25 && ptcone < 35', '_pt35t50' : 'ptcone > 35 && ptcone < 50', '_pt50t70' : 'ptcone > 50'}# && ptcone < 70'}
    for i in l_pt.keys(): 
        l_pt[i] = re.sub('ptcone','ptcone021',l_pt[i])

    if ch == 'mem':
        f_in = rt.TFile(plotDir+'DY_TT_WJ_T2Lratio_mem_ptCone_eta.root')
    
        l_eta = {'eta_bin_0' : 'abs(l1_eta) < 0.8', 'eta_bin_1' : 'abs(l1_eta) > 0.8 && abs(l1_eta) < 1.479', 'eta_bin_2' : 'abs(l1_eta) > 1.479 && abs(l1_eta) < 2.5'}

    if ch == 'mmm':
        f_in = rt.TFile(plotDir+'DY_TT_WJ_T2Lratio_mmm_ptCone_eta.root')
        l_eta = {'eta_bin_0' : 'abs(l1_eta) < 1.2', 'eta_bin_1' : 'abs(l1_eta) > 1.2 && abs(l1_eta) < 2.1', 'eta_bin_2' : 'abs(l1_eta) > 2.1 && abs(l1_eta) < 2.4'}
  
    if lep == 2: 
        for i in l_eta.keys(): 
            l_eta[i] = re.sub('l1_eta','l2_eta',l_eta[i])
        for i in l_pt.keys(): 
            l_pt[i] = re.sub('ptcone021','ptcone012',l_pt[i])

    c = f_in.Get('ptCone_eta')
    h = c.GetPrimitive('pt_eta_T_012')

    sfr =  '   ({eta00t08} && {pt0t5})   * {eta00t08_pt0t5}'  .format(eta00t08 = l_eta['eta_bin_0'], pt0t5   = l_pt['_pt0t5']  , eta00t08_pt0t5   = h.GetBinContent(1,1)/(1-h.GetBinContent(1,1))) 
    sfr += ' + ({eta00t08} && {pt5t10})  * {eta00t08_pt5t10}' .format(eta00t08 = l_eta['eta_bin_0'], pt5t10  = l_pt['_pt5t10'] , eta00t08_pt5t10  = h.GetBinContent(2,1)/(1-h.GetBinContent(2,1)))
    sfr += ' + ({eta00t08} && {pt10t15}) * {eta00t08_pt10t15}'.format(eta00t08 = l_eta['eta_bin_0'], pt10t15 = l_pt['_pt10t15'], eta00t08_pt10t15 = h.GetBinContent(3,1)/(1-h.GetBinContent(3,1)))
    sfr += ' + ({eta00t08} && {pt15t20}) * {eta00t08_pt15t20}'.format(eta00t08 = l_eta['eta_bin_0'], pt15t20 = l_pt['_pt15t20'], eta00t08_pt15t20 = h.GetBinContent(4,1)/(1-h.GetBinContent(4,1)))
    sfr += ' + ({eta00t08} && {pt20t25}) * {eta00t08_pt20t25}'.format(eta00t08 = l_eta['eta_bin_0'], pt20t25 = l_pt['_pt20t25'], eta00t08_pt20t25 = h.GetBinContent(5,1)/(1-h.GetBinContent(5,1)))
    sfr += ' + ({eta00t08} && {pt25t35}) * {eta00t08_pt25t35}'.format(eta00t08 = l_eta['eta_bin_0'], pt25t35 = l_pt['_pt25t35'], eta00t08_pt25t35 = h.GetBinContent(6,1)/(1-h.GetBinContent(6,1)))
    sfr += ' + ({eta00t08} && {pt35t50}) * {eta00t08_pt35t50}'.format(eta00t08 = l_eta['eta_bin_0'], pt35t50 = l_pt['_pt35t50'], eta00t08_pt35t50 = h.GetBinContent(7,1)/(1-h.GetBinContent(7,1)))
    sfr += ' + ({eta00t08} && {pt50t70}) * {eta00t08_pt50t70}'.format(eta00t08 = l_eta['eta_bin_0'], pt50t70 = l_pt['_pt50t70'], eta00t08_pt50t70 = h.GetBinContent(8,1)/(1-h.GetBinContent(8,1)))
    sfr += ' + ({eta08t15} && {pt0t5})   * {eta08t15_pt0t5}'  .format(eta08t15 = l_eta['eta_bin_1'], pt0t5   = l_pt['_pt0t5']  , eta08t15_pt0t5   = h.GetBinContent(1,2)/(1-h.GetBinContent(1,2))) 
    sfr += ' + ({eta08t15} && {pt5t10})  * {eta08t15_pt5t10}' .format(eta08t15 = l_eta['eta_bin_1'], pt5t10  = l_pt['_pt5t10'] , eta08t15_pt5t10  = h.GetBinContent(2,2)/(1-h.GetBinContent(2,2)))
    sfr += ' + ({eta08t15} && {pt10t15}) * {eta08t15_pt10t15}'.format(eta08t15 = l_eta['eta_bin_1'], pt10t15 = l_pt['_pt10t15'], eta08t15_pt10t15 = h.GetBinContent(3,2)/(1-h.GetBinContent(3,2)))
    sfr += ' + ({eta08t15} && {pt15t20}) * {eta08t15_pt15t20}'.format(eta08t15 = l_eta['eta_bin_1'], pt15t20 = l_pt['_pt15t20'], eta08t15_pt15t20 = h.GetBinContent(4,2)/(1-h.GetBinContent(4,2)))
    sfr += ' + ({eta08t15} && {pt20t25}) * {eta08t15_pt20t25}'.format(eta08t15 = l_eta['eta_bin_1'], pt20t25 = l_pt['_pt20t25'], eta08t15_pt20t25 = h.GetBinContent(5,2)/(1-h.GetBinContent(5,2)))
    sfr += ' + ({eta08t15} && {pt25t35}) * {eta08t15_pt25t35}'.format(eta08t15 = l_eta['eta_bin_1'], pt25t35 = l_pt['_pt25t35'], eta08t15_pt25t35 = h.GetBinContent(6,2)/(1-h.GetBinContent(6,2)))
    sfr += ' + ({eta08t15} && {pt35t50}) * {eta08t15_pt35t50}'.format(eta08t15 = l_eta['eta_bin_1'], pt35t50 = l_pt['_pt35t50'], eta08t15_pt35t50 = h.GetBinContent(7,2)/(1-h.GetBinContent(7,2)))
    sfr += ' + ({eta08t15} && {pt50t70}) * {eta08t15_pt50t70}'.format(eta08t15 = l_eta['eta_bin_1'], pt50t70 = l_pt['_pt50t70'], eta08t15_pt50t70 = h.GetBinContent(8,2)/(1-h.GetBinContent(8,2)))
    sfr += ' + ({eta15t25} && {pt0t5})   * {eta15t25_pt0t5}'  .format(eta15t25 = l_eta['eta_bin_2'], pt0t5   = l_pt['_pt0t5']  , eta15t25_pt0t5   = h.GetBinContent(1,3)/(1-h.GetBinContent(1,3))) 
    sfr += ' + ({eta15t25} && {pt5t10})  * {eta15t25_pt5t10}' .format(eta15t25 = l_eta['eta_bin_2'], pt5t10  = l_pt['_pt5t10'] , eta15t25_pt5t10  = h.GetBinContent(2,3)/(1-h.GetBinContent(2,3)))
    sfr += ' + ({eta15t25} && {pt10t15}) * {eta15t25_pt10t15}'.format(eta15t25 = l_eta['eta_bin_2'], pt10t15 = l_pt['_pt10t15'], eta15t25_pt10t15 = h.GetBinContent(3,3)/(1-h.GetBinContent(3,3)))
    sfr += ' + ({eta15t25} && {pt15t20}) * {eta15t25_pt15t20}'.format(eta15t25 = l_eta['eta_bin_2'], pt15t20 = l_pt['_pt15t20'], eta15t25_pt15t20 = h.GetBinContent(4,3)/(1-h.GetBinContent(4,3)))
    sfr += ' + ({eta15t25} && {pt20t25}) * {eta15t25_pt20t25}'.format(eta15t25 = l_eta['eta_bin_2'], pt20t25 = l_pt['_pt20t25'], eta15t25_pt20t25 = h.GetBinContent(5,3)/(1-h.GetBinContent(5,3)))
    sfr += ' + ({eta15t25} && {pt25t35}) * {eta15t25_pt25t35}'.format(eta15t25 = l_eta['eta_bin_2'], pt25t35 = l_pt['_pt25t35'], eta15t25_pt25t35 = h.GetBinContent(6,3)/(1-h.GetBinContent(6,3)))
    sfr += ' + ({eta15t25} && {pt35t50}) * {eta15t25_pt35t50}'.format(eta15t25 = l_eta['eta_bin_2'], pt35t50 = l_pt['_pt35t50'], eta15t25_pt35t50 = h.GetBinContent(7,3)/(1-h.GetBinContent(7,3)))
    sfr += ' + ({eta15t25} && {pt50t70}) * {eta15t25_pt50t70}'.format(eta15t25 = l_eta['eta_bin_2'], pt50t70 = l_pt['_pt50t70'], eta15t25_pt50t70 = h.GetBinContent(8,3)/(1-h.GetBinContent(8,3)))

    return sfr
######################################################################################

######################################################################################
def make_FR_map(ch='mem',mode='sfr',isData=False):

    plotDir = makeFolder('make_FR_map_%s'%ch)
    print '\n\tplotDir:', plotDir
    sys.stdout = Logger(plotDir + 'make_FR_map_%s' %ch)
    mode021 = False; mode012 = False; mshReg = ''

    if mode == 'sfr':
        mshReg  = 'hnl_w_vis_m > 80 && hnl_dr_12 > 0.3'
        mshReg  = 'hnl_dr_12 > 0.3' # RIC: FIRST DO VALIDITY TEST OF THE METHOD
        if ch == 'mem':
            mshReg  += ' && l1_gen_match_pdgid != 22'

    if mode == 'dfr':
        mshReg = 'hnl_w_vis_m > 80 && hnl_dr_12 < 0.3'

    h_pt_eta_T_012  = rt.TH2F('pt_eta_T_012','pt_eta_T_012',len(b_pt)-1,b_pt,len(b_eta)-1,b_eta)
    h_pt_eta_T_021  = rt.TH2F('pt_eta_T_021','pt_eta_T_021',len(b_pt)-1,b_pt,len(b_eta)-1,b_eta)
    h_pt_eta_L_012  = rt.TH2F('pt_eta_L_012','pt_eta_L_012',len(b_pt)-1,b_pt,len(b_eta)-1,b_eta)
    h_pt_eta_L_021  = rt.TH2F('pt_eta_L_021','pt_eta_L_021',len(b_pt)-1,b_pt,len(b_eta)-1,b_eta)
    
    ### PREPARE CUTS AND FILES
    SFR, DFR, dirs = selectCuts(ch)

    l0l1, l0l2, l1_loose, l2_loose, l1_lnt, l2_lnt, l1_tight, l2_tight = SFR 
    LOOSE, TIGHT, LOOSENOTTIGHT = DFR
    DYBB_dir, DY10_dir, DY50_dir, DY50_ext_dir, TT_dir, W_dir, W_ext_dir = dirs   

    dRdefList, sHdefList = selectDefs(ch)

    l0_is_fake, no_fakes, one_fake_xor, two_fakes, twoFakes_sameJet = dRdefList
    
    ### PREPARE TREES
    t = None
#    t = rt.TChain('tree')
#    t.Add(DYBB_dir + suffix)
#    t.Add(DY10_dir + suffix)
#    t.Add(DY50_dir + suffix)
#    t.Add(DY50_ext_dir + suffix)
#    t.Add(TT_dir + suffix)
##    t.Add(W_dir + suffix)
#    t.Add(W_ext_dir + suffix)
    fin = rt.TFile('/afs/cern.ch/work/m/manzoni/public/forVinzenzDavid/mme_tree.root'); t = fin.Get('tree')
    df = rdf(t)
    print'\n\tchain made.'
    N_ENTRIES = df.Count()

    if ch == 'mem':

        mode021 = True
        l1_loose += ' && hnl_dr_01 > 0.3'                                                        # no conversions, only use this to measure t2l ratio 
        l1_loose += ' && ( (l1_reliso_rho_03 < 0.6 && abs(l1_eta) < 0.8) || (l1_reliso_rho_03 < 0.35 && abs(l1_eta) > 0.8) )'

        f0_021 = df.Filter(l0l2 + ' && ' + l1_loose + ' && ' + mshReg)

    if ch == 'mmm':

        mode021 = True
        mode012 = True

        l1_loose += ' && hnl_dr_01 > 0.3'                                                        # no conversions, only use this to measure t2l ratio 
        l2_loose += ' && hnl_dr_02 > 0.3'                                                        # no conversions, only use this to measure t2l ratio 

        f0_012 = df.Filter(l0l1 + ' && ' + l2_loose + ' && ' + mshReg)
        f0_021 = df.Filter(l0l2 + ' && ' + l1_loose + ' && ' + mshReg)


    if mode021 == True:

        print '\n\tf0_021 entries:', f0_021.Count().GetValue()

        df0_021 = f0_021.Define('ptcone021', PTCONEL1)
        print '\n\tptcone021 defined.'

        dfl_021 = df0_021.Define('abs_l1_eta', 'abs(l1_eta)')
        print '\n\tabs_l1_eta defined.'

        dft_021 = dfl_021.Filter(l1_tight)
        print '\n\ttight df_021 defined.'

        _pt_eta_T_021 = dft_021.Histo2D(('pt_eta_T_021','pt_eta_T_021',len(b_pt)-1,b_pt,len(b_eta)-1,b_eta),'ptcone021','abs_l1_eta')
        _pt_eta_L_021 = dfl_021.Histo2D(('pt_eta_L_021','pt_eta_L_021',len(b_pt)-1,b_pt,len(b_eta)-1,b_eta),'ptcone021','abs_l1_eta')

        h_pt_eta_T_021 = _pt_eta_T_021.GetPtr()
        h_pt_eta_L_021 = _pt_eta_L_021.GetPtr()

    if mode012 == True:

        print '\n\tf0_012 entries:', f0_012.Count().GetValue()

        df0_012 = f0_012.Define('ptcone012', PTCONEL2)
        print '\n\tptcone012 defined.'

        dfl_012 = df0_012.Define('abs_l2_eta', 'abs(l2_eta)')
        print '\n\tabs_l2_eta defined.'

        dft_012 = dfl_012.Filter(l1_tight)
        print '\n\ttight df_012 defined.'

        _pt_eta_T_012 = dft_012.Histo2D(('pt_eta_T_012','pt_eta_T_012',len(b_pt)-1,b_pt,len(b_eta)-1,b_eta),'ptcone012','abs_l2_eta')
        _pt_eta_L_012 = dfl_012.Histo2D(('pt_eta_L_012','pt_eta_L_012',len(b_pt)-1,b_pt,len(b_eta)-1,b_eta),'ptcone012','abs_l2_eta')

        h_pt_eta_T_012 = _pt_eta_T_012.GetPtr()
        h_pt_eta_L_012 = _pt_eta_L_012.GetPtr()

    h_pt_eta_T_012.Add(h_pt_eta_T_021)
    h_pt_eta_L_012.Add(h_pt_eta_L_021)

    print '\n\t cuts: %s'                %mshReg
    if mode012 ==True:
        print '\n\t l0l1: %s\n'          %(l0l1)
        print '\n\t l2_loose: %s\n'      %(l2_loose)
        print '\n\t l2_tight: %s\n'      %(l2_tight)
        print '\ttotal loose: %s\n'      %f0_012.Count().GetValue()

    if mode021 ==True:
        print '\n\t l0l2: %s\n'          %(l0l2)
        print '\n\t l1_loose: %s\n'      %(l1_loose)
        print '\n\t l1_tight: %s\n'      %(l1_tight)
        print '\ttotal loose: %s\n'      %f0_021.Count().GetValue()


    print '\n\tentries T && L: ', h_pt_eta_T_012.GetEntries(), h_pt_eta_L_012.GetEntries()

    c_pt_eta = rt.TCanvas('ptCone_eta', 'ptCone_eta')
    h_pt_eta_T_012.Divide(h_pt_eta_L_012)
    h_pt_eta_T_012.Draw('colztextE')
    h_pt_eta_T_012.SetTitle('; p_{T}^{cone} [GeV]; DiMuon |#eta|; tight-to-loose ratio')
    pf.showlogoprelimsim('CMS')
    pf.showlumi('SFR_'+ch)
    save(knvs=c_pt_eta, sample='DY_TT_WJ_T2Lratio', ch=ch, DIR=plotDir)

    sys.stderr = sys.__stderr__
    sys.stdout = sys.__stdout__
    # DO AGAIN WITH THREE DIFFERENT TEFFS TO GET ERROR
###########################################################################################################################################################################################

###########################################################################################################################################################################################
def checkTTLratio_JetFlavor(ch='mmm',eta_split=True,sfr=True,dfr=False,fullSplit=False,dbg=False):

    plotDir = makeFolder('checkTTLratio_%s'%ch)
    print '\n\tplotDir:', plotDir
    sys.stdout = Logger(plotDir + 'checkTTLratio_%s' %ch)
    print '\n\tmode: %s\n'%ch
    l_eta = None
    l_eta  = OrderedDict()
    l_eta['_eta_all'] = '1 == 1'
    l_cuts_sfr = ['1 == 1','1 == 1','1 == 1']

    if eta_split == True: 

        if ch == 'mem' or ch == 'eee':
            l_eta = None
            l_eta = OrderedDict()
            l_eta ['_eta_00t08'] = 'abs(l1_eta) < 0.8'; l_eta ['_eta_08t15'] = 'abs(l1_eta) > 0.8 && abs(l1_eta) < 1.479'; l_eta ['_eta_15t25'] = 'abs(l1_eta) > 1.479 && abs(l1_eta) < 2.5'

            l_cuts_sfr = ['l1_reliso_rho_03 < 0.6','l1_reliso_rho_03 < 0.35','l1_reliso_rho_03 < 0.35']

        if ch == 'mmm' or ch == 'eem':
            l_eta = None
            l_eta = OrderedDict()
            l_eta ['_eta_00t12'] = 'abs(l1_eta) < 1.2'; l_eta ['_eta_12t21'] = 'abs(l1_eta) > 1.2 && abs(l1_eta) < 2.1'; l_eta ['_eta_21t24'] = 'abs(l1_eta) > 2.1 && abs(l1_eta) < 2.4'


    ### PREPARE CUTS AND FILES
    SFR, DFR, dirs = selectCuts(ch)

    l0l1, l0l2, l1_loose, l2_loose, l1_lnt, l2_lnt, l1_tight, l2_tight = SFR 
    LOOSE, TIGHT, LOOSENOTTIGHT = DFR
    DYBB_dir, DY10_dir, DY50_dir, DY50_ext_dir, TT_dir, W_dir, W_ext_dir = dirs   

    dRdefList, sHdefList = selectDefs(ch)

    l0_is_fake, no_fakes, one_fake_xor, two_fakes, twoFakes_sameJet = dRdefList
    
    ### PREPARE TREES
    t = None
    t = rt.TChain('tree')
#    t = rt.TChain('tree')
#    t.Add(DYBB_dir + suffix)
#    t.Add(DY10_dir + suffix)
#    t.Add(DY50_dir + suffix)
#    t.Add(DY50_ext_dir + suffix)
#    t.Add(TT_dir + suffix)
##    t.Add(W_dir + suffix)
#    t.Add(W_ext_dir + suffix)
    fin = rt.TFile('/afs/cern.ch/work/m/manzoni/public/forVinzenzDavid/mme_tree.root'); t = fin.Get('tree')
    df = rdf(t)
    print'\n\tchain made.'
    N_ENTRIES = df.Count()

    if dfr:

        #### CHANNEL SPECIFIC
        if ch == 'eem':
            mode012 = True
            cuts_FR += ' && abs(l2_gen_match_pdgid) != 22'

        if ch == 'mem':
            mode021 = True
            cuts_FR += ' && abs(l1_gen_match_pdgid) != 22'

        if ch == 'mmm':
           mode012 = True
           mode021 = True

        #### GENERAL DOUBLE FAKES 
        print '\n\tdrawing double fakes ...'
        mode021 = False; mode012 = False

        cuts_FR = 'hnl_dr_12 < 0.3'

        PTCONE021 = PTCONE
        PTCONE012 = PTCONE

        cuts_l_021 = cuts_FR + ' && l1_jet_flavour_parton != -99 && ' + l0l2 + ' && ' + l1_loose
        cuts_l_012 = cuts_FR + ' && l2_jet_flavour_parton != -99 && ' + l0l1 + ' && ' + l2_loose 


    if sfr:

        #### CHANNEL SPECIFIC
        if ch == 'eem':
            mode012 = True
            cuts_FR += ' && abs(l2_gen_match_pdgid) != 22'

        if ch == 'mem':
            mode021 = True
            cuts_FR += ' && abs(l1_gen_match_pdgid) != 22'

        if ch == 'mmm':
           mode012 = True
           mode021 = True

        #### GENERAL SINGLE FAKES 
        print '\n\tdrawing single fakes ...'
        mode021 = False; mode012 = False

        cuts_FR = 'hnl_dr_12 > 0.3'

        PTCONE021 = PTCONEL1
        PTCONE012 = PTCONEL2

        cuts_l_021 = cuts_FR + ' && l1_jet_flavour_parton != -99 && ' + l0l2 + ' && ' + l1_loose
        cuts_l_012 = cuts_FR + ' && l2_jet_flavour_parton != -99 && ' + l0l1 + ' && ' + l2_loose 

    ### PREPARE DATAFRAMES
    if mode021 == True:
        f0_021 = df.Filter(cuts_l_021)
        print '\n\tloose 021 defined.'

        dfl_021 = f0_021.Define('ptcone021', PTCONE021)
        print '\n\tptcone 021: %s\n' %PTCONE021
        print '\tptcone 021 defined.'

        if fullSplit == False:
            dfl_021_light = dfl_021.Filter('abs(l1_jet_flavour_parton) != 4 && abs(l1_jet_flavour_parton) != 5')
            dfl_021_heavy = dfl_021.Filter('abs(l1_jet_flavour_parton) == 4 || abs(l1_jet_flavour_parton) == 5')

        if fullSplit == True:
            dfl_021_b     = dfl_021.Filter('abs(l1_jet_flavour_parton) == 5')
            dfl_021_c     = dfl_021.Filter('abs(l1_jet_flavour_parton) == 4')
            dfl_021_glu   = dfl_021.Filter('abs(l1_jet_flavour_parton) == 21 || abs(l1_jet_flavour_parton) == 9')
            dfl_021_light = dfl_021.Filter('abs(l1_jet_flavour_parton) == 3 || abs(l1_jet_flavour_parton) == 2 || abs(l1_jet_flavour_parton) == 1')
            dfl_021_other = dfl_021.Filter('abs(l1_jet_flavour_parton) != 1 && abs(l1_jet_flavour_parton) != 2 && abs(l1_jet_flavour_parton) != 3 && abs(l1_jet_flavour_parton) != 4'\
                                           ' && abs(l1_jet_flavour_parton) != 5 && abs(l1_jet_flavour_parton) != 9 && abs(l1_jet_flavour_parton) != 21')
        print '\tflavours 021 defined.'

        if fullSplit == False:
            dfl_021_light_eta0 = dfl_021_light.Filter(l_eta[l_eta.keys()[0]])
            dfl_021_heavy_eta0 = dfl_021_heavy.Filter(l_eta[l_eta.keys()[0]])

            dfl_021_light_eta1 = dfl_021_light.Filter(l_eta[l_eta.keys()[1]])
            dfl_021_heavy_eta1 = dfl_021_heavy.Filter(l_eta[l_eta.keys()[1]])

            dfl_021_light_eta2 = dfl_021_light.Filter(l_eta[l_eta.keys()[2]])
            dfl_021_heavy_eta2 = dfl_021_heavy.Filter(l_eta[l_eta.keys()[2]])

        if fullSplit == True:
            dfl_021_c_eta0     = dfl_021_c    .Filter(l_eta[l_eta.keys()[0]])
            dfl_021_b_eta0     = dfl_021_b    .Filter(l_eta[l_eta.keys()[0]])
            dfl_021_glu_eta0   = dfl_021_glu  .Filter(l_eta[l_eta.keys()[0]])
            dfl_021_light_eta0 = dfl_021_light.Filter(l_eta[l_eta.keys()[0]])
            dfl_021_other_eta0 = dfl_021_other.Filter(l_eta[l_eta.keys()[0]])
 
            dfl_021_c_eta1     = dfl_021_c    .Filter(l_eta[l_eta.keys()[1]])
            dfl_021_b_eta1     = dfl_021_b    .Filter(l_eta[l_eta.keys()[1]])
            dfl_021_glu_eta1   = dfl_021_glu  .Filter(l_eta[l_eta.keys()[1]])
            dfl_021_light_eta1 = dfl_021_light.Filter(l_eta[l_eta.keys()[1]])
            dfl_021_other_eta1 = dfl_021_other.Filter(l_eta[l_eta.keys()[1]])
 
            dfl_021_c_eta2     = dfl_021_c    .Filter(l_eta[l_eta.keys()[2]])
            dfl_021_b_eta2     = dfl_021_b    .Filter(l_eta[l_eta.keys()[2]])
            dfl_021_glu_eta2   = dfl_021_glu  .Filter(l_eta[l_eta.keys()[2]])
            dfl_021_light_eta2 = dfl_021_light.Filter(l_eta[l_eta.keys()[2]])
            dfl_021_other_eta2 = dfl_021_other.Filter(l_eta[l_eta.keys()[2]])
        print '\tloose 021 eta defined.'

        if fullSplit == False:
            dft_021_light_eta0 = dfl_021_light_eta0.Filter(l1_tight)
            dft_021_heavy_eta0 = dfl_021_heavy_eta0.Filter(l1_tight)

            dft_021_light_eta1 = dfl_021_light_eta1.Filter(l1_tight)
            dft_021_heavy_eta1 = dfl_021_heavy_eta1.Filter(l1_tight)

            dft_021_light_eta2 = dfl_021_light_eta2.Filter(l1_tight)
            dft_021_heavy_eta2 = dfl_021_heavy_eta2.Filter(l1_tight)

        if fullSplit == True:
            dft_021_c_eta0     = dfl_021_c_eta0    .Filter(l1_tight)
            dft_021_b_eta0     = dfl_021_b_eta0    .Filter(l1_tight)
            dft_021_glu_eta0   = dfl_021_glu_eta0  .Filter(l1_tight)
            dft_021_light_eta0 = dfl_021_light_eta0.Filter(l1_tight)
            dft_021_other_eta0 = dfl_021_other_eta0.Filter(l1_tight)

            dft_021_c_eta1     = dfl_021_c_eta1    .Filter(l1_tight)
            dft_021_b_eta1     = dfl_021_b_eta1    .Filter(l1_tight)
            dft_021_glu_eta1   = dfl_021_glu_eta1  .Filter(l1_tight)
            dft_021_light_eta1 = dfl_021_light_eta1.Filter(l1_tight)
            dft_021_other_eta1 = dfl_021_other_eta1.Filter(l1_tight)

            dft_021_c_eta2     = dfl_021_c_eta2    .Filter(l1_tight)
            dft_021_b_eta2     = dfl_021_b_eta2    .Filter(l1_tight)
            dft_021_glu_eta2   = dfl_021_glu_eta2  .Filter(l1_tight)
            dft_021_light_eta2 = dfl_021_light_eta2.Filter(l1_tight)
            dft_021_other_eta2 = dfl_021_other_eta2.Filter(l1_tight)
        print '\ttight 021 defined.'

        if fullSplit == False:
            _dfl_021_light = [dfl_021_light_eta0, dfl_021_light_eta1, dfl_021_light_eta2]
            _dfl_021_heavy = [dfl_021_heavy_eta0, dfl_021_heavy_eta1, dfl_021_heavy_eta2]

            _dft_021_light = [dft_021_light_eta0, dft_021_light_eta1, dft_021_light_eta2]
            _dft_021_heavy = [dft_021_heavy_eta0, dft_021_heavy_eta1, dft_021_heavy_eta2]

        if fullSplit == True:
            _dfl_021_c     = [dfl_021_c_eta0    , dfl_021_c_eta1    , dfl_021_c_eta2    ] 
            _dfl_021_b     = [dfl_021_b_eta0    , dfl_021_b_eta1    , dfl_021_b_eta2    ] 
            _dfl_021_glu   = [dfl_021_glu_eta0  , dfl_021_glu_eta1  , dfl_021_glu_eta2  ]
            _dfl_021_light = [dfl_021_light_eta0, dfl_021_light_eta1, dfl_021_light_eta2]
            _dfl_021_other = [dfl_021_other_eta0, dfl_021_other_eta1, dfl_021_other_eta2]
      
            _dft_021_c     = [dft_021_c_eta0    , dft_021_c_eta1    , dft_021_c_eta2    ] 
            _dft_021_b     = [dft_021_b_eta0    , dft_021_b_eta1    , dft_021_b_eta2    ] 
            _dft_021_glu   = [dft_021_glu_eta0  , dft_021_glu_eta1  , dft_021_glu_eta2  ]
            _dft_021_light = [dft_021_light_eta0, dft_021_light_eta1, dft_021_light_eta2]
            _dft_021_other = [dft_021_other_eta0, dft_021_other_eta1, dft_021_other_eta2]


    if mode012 == True:
        f0_012 = df.Filter(cuts_l_012)
        print '\n\tloose 012 defined.'

        dfl_012 = f0_012.Define('ptcone012', PTCONE012)
        print '\n\tptcone 012: %s\n' %PTCONE012
        print '\tptcone 012 defined.'

        if fullSplit == False:
            dfl_012_light = dfl_012.Filter('abs(l2_jet_flavour_parton) != 4 && abs(l2_jet_flavour_parton) != 5')
            dfl_012_heavy = dfl_012.Filter('abs(l2_jet_flavour_parton) == 4 || abs(l2_jet_flavour_parton) == 5')

        if fullSplit == True:
            dfl_012_b     = dfl_012.Filter('abs(l2_jet_flavour_parton) == 5')
            dfl_012_c     = dfl_012.Filter('abs(l2_jet_flavour_parton) == 4')
            dfl_012_glu   = dfl_012.Filter('abs(l2_jet_flavour_parton) == 21 || abs(l2_jet_flavour_parton) == 9')
            dfl_012_light = dfl_012.Filter('abs(l2_jet_flavour_parton) == 3 || abs(l2_jet_flavour_parton) == 2 || abs(l2_jet_flavour_parton) == 1')
            dfl_012_other = dfl_012.Filter('abs(l2_jet_flavour_parton) != 1 && abs(l2_jet_flavour_parton) != 2 && abs(l2_jet_flavour_parton) != 3 && abs(l2_jet_flavour_parton) != 4'\
                                           ' && abs(l2_jet_flavour_parton) != 5 && abs(l2_jet_flavour_parton) != 9 && abs(l2_jet_flavour_parton) != 21')
        print '\tflavours 012 defined.'

        if fullSplit == False:
            dfl_012_light_eta0 = dfl_012_light.Filter(re.sub('l1_eta','l2_eta',l_eta[l_eta.keys()[0]]))
            dfl_012_heavy_eta0 = dfl_012_heavy.Filter(re.sub('l1_eta','l2_eta',l_eta[l_eta.keys()[0]]))

            dfl_012_light_eta1 = dfl_012_light.Filter(re.sub('l1_eta','l2_eta',l_eta[l_eta.keys()[1]]))
            dfl_012_heavy_eta1 = dfl_012_heavy.Filter(re.sub('l1_eta','l2_eta',l_eta[l_eta.keys()[1]]))

            dfl_012_light_eta2 = dfl_012_light.Filter(re.sub('l1_eta','l2_eta',l_eta[l_eta.keys()[2]]))
            dfl_012_heavy_eta2 = dfl_012_heavy.Filter(re.sub('l1_eta','l2_eta',l_eta[l_eta.keys()[2]]))

        if fullSplit == True:
            dfl_012_c_eta0     = dfl_012_c    .Filter(re.sub('l1_eta','l2_eta',l_eta[l_eta.keys()[0]]))
            dfl_012_b_eta0     = dfl_012_b    .Filter(re.sub('l1_eta','l2_eta',l_eta[l_eta.keys()[0]]))
            dfl_012_glu_eta0   = dfl_012_glu  .Filter(re.sub('l1_eta','l2_eta',l_eta[l_eta.keys()[0]]))
            dfl_012_light_eta0 = dfl_012_light.Filter(re.sub('l1_eta','l2_eta',l_eta[l_eta.keys()[0]]))
            dfl_012_other_eta0 = dfl_012_other.Filter(re.sub('l1_eta','l2_eta',l_eta[l_eta.keys()[0]]))
 
            dfl_012_c_eta1     = dfl_012_c    .Filter(re.sub('l1_eta','l2_eta',l_eta[l_eta.keys()[1]]))
            dfl_012_b_eta1     = dfl_012_b    .Filter(re.sub('l1_eta','l2_eta',l_eta[l_eta.keys()[1]]))
            dfl_012_glu_eta1   = dfl_012_glu  .Filter(re.sub('l1_eta','l2_eta',l_eta[l_eta.keys()[1]]))
            dfl_012_light_eta1 = dfl_012_light.Filter(re.sub('l1_eta','l2_eta',l_eta[l_eta.keys()[1]]))
            dfl_012_other_eta1 = dfl_012_other.Filter(re.sub('l1_eta','l2_eta',l_eta[l_eta.keys()[1]]))
 
            dfl_012_c_eta2     = dfl_012_c    .Filter(re.sub('l1_eta','l2_eta',l_eta[l_eta.keys()[2]]))
            dfl_012_b_eta2     = dfl_012_b    .Filter(re.sub('l1_eta','l2_eta',l_eta[l_eta.keys()[2]]))
            dfl_012_glu_eta2   = dfl_012_glu  .Filter(re.sub('l1_eta','l2_eta',l_eta[l_eta.keys()[2]]))
            dfl_012_light_eta2 = dfl_012_light.Filter(re.sub('l1_eta','l2_eta',l_eta[l_eta.keys()[2]]))
            dfl_012_other_eta2 = dfl_012_other.Filter(re.sub('l1_eta','l2_eta',l_eta[l_eta.keys()[2]]))
        print '\tloose 012 eta defined.'

        if fullSplit == False:
            dft_012_light_eta0 = dfl_012_light_eta0.Filter(l2_tight)
            dft_012_heavy_eta0 = dfl_012_heavy_eta0.Filter(l2_tight)

            dft_012_light_eta1 = dfl_012_light_eta1.Filter(l2_tight)
            dft_012_heavy_eta1 = dfl_012_heavy_eta1.Filter(l2_tight)

            dft_012_light_eta2 = dfl_012_light_eta2.Filter(l2_tight)
            dft_012_heavy_eta2 = dfl_012_heavy_eta2.Filter(l2_tight)

        if fullSplit == True:
            dft_012_c_eta0     = dfl_012_c_eta0    .Filter(l2_tight)
            dft_012_b_eta0     = dfl_012_b_eta0    .Filter(l2_tight)
            dft_012_glu_eta0   = dfl_012_glu_eta0  .Filter(l2_tight)
            dft_012_light_eta0 = dfl_012_light_eta0.Filter(l2_tight)
            dft_012_other_eta0 = dfl_012_other_eta0.Filter(l2_tight)
 
            dft_012_c_eta1     = dfl_012_c_eta1    .Filter(l2_tight)
            dft_012_b_eta1     = dfl_012_b_eta1    .Filter(l2_tight)
            dft_012_glu_eta1   = dfl_012_glu_eta1  .Filter(l2_tight)
            dft_012_light_eta1 = dfl_012_light_eta1.Filter(l2_tight)
            dft_012_other_eta1 = dfl_012_other_eta1.Filter(l2_tight)
 
            dft_012_c_eta2     = dfl_012_c_eta2    .Filter(l2_tight)
            dft_012_b_eta2     = dfl_012_b_eta2    .Filter(l2_tight)
            dft_012_glu_eta2   = dfl_012_glu_eta2  .Filter(l2_tight)
            dft_012_light_eta2 = dfl_012_light_eta2.Filter(l2_tight)
            dft_012_other_eta2 = dfl_012_other_eta2.Filter(l2_tight)
        print '\ttight 012 defined.'

        if fullSplit == False:
            _dft_012_light = [dft_012_light_eta0, dft_012_light_eta1, dft_012_light_eta2]
            _dft_012_heavy = [dft_012_heavy_eta0, dft_012_heavy_eta1, dft_012_heavy_eta2]

            _dfl_012_light = [dfl_012_light_eta0, dfl_012_light_eta1, dfl_012_light_eta2]
            _dfl_012_heavy = [dfl_012_heavy_eta0, dfl_012_heavy_eta1, dfl_012_heavy_eta2]

        if fullSplit == True:
            _dfl_012_c     = [dfl_012_c_eta0    , dfl_012_c_eta1    , dfl_012_c_eta2    ] 
            _dfl_012_b     = [dfl_012_b_eta0    , dfl_012_b_eta1    , dfl_012_b_eta2    ] 
            _dfl_012_glu   = [dfl_012_glu_eta0  , dfl_012_glu_eta1  , dfl_012_glu_eta2  ]
            _dfl_012_light = [dfl_012_light_eta0, dfl_012_light_eta1, dfl_012_light_eta2]
            _dfl_012_other = [dfl_012_other_eta0, dfl_012_other_eta1, dfl_012_other_eta2]
      
            _dft_012_c     = [dft_012_c_eta0    , dft_012_c_eta1    , dft_012_c_eta2    ] 
            _dft_012_b     = [dft_012_b_eta0    , dft_012_b_eta1    , dft_012_b_eta2    ] 
            _dft_012_glu   = [dft_012_glu_eta0  , dft_012_glu_eta1  , dft_012_glu_eta2  ]
            _dft_012_light = [dft_012_light_eta0, dft_012_light_eta1, dft_012_light_eta2]
            _dft_012_other = [dft_012_other_eta0, dft_012_other_eta1, dft_012_other_eta2]

        
        print '\n\t cuts: %s'                %cuts_FR
        if mode012 ==True:
            print '\n\t l0l1: %s\n'          %(l0l1)
            print '\n\t l2_loose: %s\n'      %(l2_loose)
            print '\n\t l2_tight: %s\n'      %(l2_tight)
            print '\ttotal loose: %s\n'      %f0_012.Count().GetValue()
        if mode021 ==True:
            print '\n\t l0l2: %s\n'          %(l0l2)
            print '\n\t l1_loose: %s\n'      %(l1_loose)
            print '\n\t l1_tight: %s\n'      %(l1_tight)
            print '\ttotal loose: %s\n'      %f0_021.Count().GetValue()

    h_pt_1f = {}; h_pt_2f = []; i = 0
    for eta in l_eta.keys():
        print '\n\teta:', eta

        if sfr:

            if mode012 == True:
                if fullSplit == True:
                    print'\t','df 012 sum loose:',     _dfl_012_c[i].Count().GetValue() + _dfl_012_light[i].Count().GetValue() + \
                                                       _dfl_012_other[i].Count().GetValue() + _dfl_012_b[i].Count().GetValue() + _dfl_012_glu[i].Count().GetValue()
                    print'\t','df 012 entries loose:', _dfl_012_c[i].Count().GetValue(), _dfl_012_light[i].Count().GetValue(), \
                                                       _dfl_012_b[i].Count().GetValue(), _dfl_012_other[i].Count().GetValue(), _dfl_012_glu[i].Count().GetValue()
                    print'\t','df 012 sum tight:',     _dft_012_c[i].Count().GetValue() + _dft_012_light[i].Count().GetValue() + \
                                                       _dft_012_other[i].Count().GetValue() + _dft_012_b[i].Count().GetValue() + _dft_012_glu[i].Count().GetValue()
                    print'\t','df 012 entries tight:', _dft_012_c[i].Count().GetValue(), _dft_012_light[i].Count().GetValue(), \
                                                       _dft_012_b[i].Count().GetValue(), _dft_012_other[i].Count().GetValue(), _dft_012_glu[i].Count().GetValue()
                if fullSplit == False:
                    print'\t','df 012 sum loose:',     _dfl_012_heavy[i].Count().GetValue() + _dfl_012_light[i].Count().GetValue()
                    print'\t','df 012 entries loose:', _dfl_012_heavy[i].Count().GetValue(), _dfl_012_light[i].Count().GetValue()
                    print'\t','df 012 sum tight:',     _dft_012_heavy[i].Count().GetValue() + _dft_012_light[i].Count().GetValue()
                    print'\t','df 012 entries tight:', _dft_012_heavy[i].Count().GetValue(), _dft_012_light[i].Count().GetValue()
            if mode021 == True:
                if fullSplit == True:
                    print'\t','df 021 sum loose:',     _dfl_021_c[i].Count().GetValue() + _dfl_021_light[i].Count().GetValue() + \
                                                       _dfl_021_other[i].Count().GetValue() + _dfl_021_b[i].Count().GetValue() + _dfl_021_glu[i].Count().GetValue()
                    print'\t','df 021 entries loose:', _dfl_021_c[i].Count().GetValue(), _dfl_021_light[i].Count().GetValue(), \
                                                       _dfl_021_b[i].Count().GetValue(), _dfl_021_other[i].Count().GetValue(), _dfl_021_glu[i].Count().GetValue()
                    print'\t','df 021 sum tight:',     _dft_021_c[i].Count().GetValue() + _dft_021_light[i].Count().GetValue() + \
                                                       _dft_021_other[i].Count().GetValue() + _dft_021_b[i].Count().GetValue() + _dft_021_glu[i].Count().GetValue()
                    print'\t','df 021 entries tight:', _dft_021_c[i].Count().GetValue(), _dft_021_light[i].Count().GetValue(), \
                                                       _dft_021_b[i].Count().GetValue(), _dft_021_other[i].Count().GetValue(), _dft_021_glu[i].Count().GetValue()
                if fullSplit == False:
                    print'\t','df 021 sum loose:',     _dfl_021_heavy[i].Count().GetValue() + _dfl_021_light[i].Count().GetValue()
                    print'\t','df 021 entries loose:', _dfl_021_heavy[i].Count().GetValue(), _dfl_021_light[i].Count().GetValue()
                    print'\t','df 021 sum tight:',     _dft_021_heavy[i].Count().GetValue() + _dft_021_light[i].Count().GetValue()
                    print'\t','df 021 entries tight:', _dft_021_heavy[i].Count().GetValue(), _dft_021_light[i].Count().GetValue()

            h_pt_1f_T_012  = rt.TH1F('pt_1f_T_012', 'pt_1f_T_012',len(b_pt)-1,b_pt)
            h_pt_1f_T_021  = rt.TH1F('pt_1f_T_021', 'pt_1f_T_021',len(b_pt)-1,b_pt)
            h_pt_1f_L_012  = rt.TH1F('pt_1f_L_012', 'pt_1f_L_012',len(b_pt)-1,b_pt)
            h_pt_1f_L_021  = rt.TH1F('pt_1f_L_021', 'pt_1f_L_021',len(b_pt)-1,b_pt)

            h_pt_1f_T_012_light = rt.TH1F('pt_1f_T_012_light', 'pt_1f_T_012_light',len(b_pt)-1,b_pt)
            h_pt_1f_T_021_light = rt.TH1F('pt_1f_T_021_light', 'pt_1f_T_021_light',len(b_pt)-1,b_pt)
            h_pt_1f_L_012_light = rt.TH1F('pt_1f_L_012_light', 'pt_1f_L_012_light',len(b_pt)-1,b_pt)
            h_pt_1f_L_021_light = rt.TH1F('pt_1f_L_021_light', 'pt_1f_L_021_light',len(b_pt)-1,b_pt)

            if fullSplit == False:
                h_pt_1f_T_012_heavy = rt.TH1F('pt_1f_T_012_heavy', 'pt_1f_T_012_heavy',len(b_pt)-1,b_pt)
                h_pt_1f_T_021_heavy = rt.TH1F('pt_1f_T_021_heavy', 'pt_1f_T_021_heavy',len(b_pt)-1,b_pt)
                h_pt_1f_L_012_heavy = rt.TH1F('pt_1f_L_012_heavy', 'pt_1f_L_012_heavy',len(b_pt)-1,b_pt)
                h_pt_1f_L_021_heavy = rt.TH1F('pt_1f_L_021_heavy', 'pt_1f_L_021_heavy',len(b_pt)-1,b_pt)

            if fullSplit == True:
                h_pt_1f_T_012_other = rt.TH1F('pt_1f_T_012_other', 'pt_1f_T_012_other',len(b_pt)-1,b_pt)
                h_pt_1f_T_021_other = rt.TH1F('pt_1f_T_021_other', 'pt_1f_T_021_other',len(b_pt)-1,b_pt)
                h_pt_1f_L_012_other = rt.TH1F('pt_1f_L_012_other', 'pt_1f_L_012_other',len(b_pt)-1,b_pt)
                h_pt_1f_L_021_other = rt.TH1F('pt_1f_L_021_other', 'pt_1f_L_021_other',len(b_pt)-1,b_pt)

                h_pt_1f_T_012_glu = rt.TH1F('pt_1f_T_012_glu', 'pt_1f_T_012_glu',len(b_pt)-1,b_pt)
                h_pt_1f_T_021_glu = rt.TH1F('pt_1f_T_021_glu', 'pt_1f_T_021_glu',len(b_pt)-1,b_pt)
                h_pt_1f_L_012_glu = rt.TH1F('pt_1f_L_012_glu', 'pt_1f_L_012_glu',len(b_pt)-1,b_pt)
                h_pt_1f_L_021_glu = rt.TH1F('pt_1f_L_021_glu', 'pt_1f_L_021_glu',len(b_pt)-1,b_pt)

                h_pt_1f_T_012_c = rt.TH1F('pt_1f_T_012_c', 'pt_1f_T_012_c',len(b_pt)-1,b_pt)
                h_pt_1f_T_021_c = rt.TH1F('pt_1f_T_021_c', 'pt_1f_T_021_c',len(b_pt)-1,b_pt)
                h_pt_1f_L_012_c = rt.TH1F('pt_1f_L_012_c', 'pt_1f_L_012_c',len(b_pt)-1,b_pt)
                h_pt_1f_L_021_c = rt.TH1F('pt_1f_L_021_c', 'pt_1f_L_021_c',len(b_pt)-1,b_pt)

                h_pt_1f_T_012_b = rt.TH1F('pt_1f_T_012_b', 'pt_1f_T_012_b',len(b_pt)-1,b_pt)
                h_pt_1f_T_021_b = rt.TH1F('pt_1f_T_021_b', 'pt_1f_T_021_b',len(b_pt)-1,b_pt)
                h_pt_1f_L_012_b = rt.TH1F('pt_1f_L_012_b', 'pt_1f_L_012_b',len(b_pt)-1,b_pt)
                h_pt_1f_L_021_b = rt.TH1F('pt_1f_L_021_b', 'pt_1f_L_021_b',len(b_pt)-1,b_pt)

            ### FILLING
            if mode021 ==True:

                if fullSplit == False:
                    _h_pt_1f_T_021_light = _dft_021_light[i].Histo1D(('pt_1f_T_021_light', 'pt_1f_T_021_light',len(b_pt)-1,b_pt), 'ptcone021')
                    _h_pt_1f_T_021_heavy = _dft_021_heavy[i].Histo1D(('pt_1f_T_021_heavy', 'pt_1f_T_021_heavy',len(b_pt)-1,b_pt), 'ptcone021')

                    _h_pt_1f_L_021_light = _dfl_021_light[i].Histo1D(('pt_1f_L_021_light', 'pt_1f_L_021_light',len(b_pt)-1,b_pt), 'ptcone021')
                    _h_pt_1f_L_021_heavy = _dfl_021_heavy[i].Histo1D(('pt_1f_L_021_heavy', 'pt_1f_L_021_heavy',len(b_pt)-1,b_pt), 'ptcone021')

                    h_pt_1f_T_021_light  = _h_pt_1f_T_021_light.GetPtr()
                    h_pt_1f_T_021_heavy  = _h_pt_1f_T_021_heavy.GetPtr()

                    h_pt_1f_L_021_light  = _h_pt_1f_L_021_light.GetPtr()
                    h_pt_1f_L_021_heavy  = _h_pt_1f_L_021_heavy.GetPtr()

                if fullSplit == True:
                    _h_pt_1f_T_021_c     = _dft_021_c[i]    .Histo1D(('pt_1f_T_021_c'    , 'pt_1f_T_021_c'    ,len(b_pt)-1,b_pt), 'ptcone021')
                    _h_pt_1f_T_021_glu   = _dft_021_glu[i]  .Histo1D(('pt_1f_T_021_glu'  , 'pt_1f_T_021_glu'  ,len(b_pt)-1,b_pt), 'ptcone021')
                    _h_pt_1f_T_021_b     = _dft_021_b[i]    .Histo1D(('pt_1f_T_021_b'    , 'pt_1f_T_021_b'    ,len(b_pt)-1,b_pt), 'ptcone021')
                    _h_pt_1f_T_021_light = _dft_021_light[i].Histo1D(('pt_1f_T_021_light', 'pt_1f_T_021_light',len(b_pt)-1,b_pt), 'ptcone021')
                    _h_pt_1f_T_021_other = _dft_021_other[i].Histo1D(('pt_1f_T_021_other', 'pt_1f_T_021_other',len(b_pt)-1,b_pt), 'ptcone021')

                    _h_pt_1f_L_021_c     = _dfl_021_c[i]    .Histo1D(('pt_1f_L_021_c'    , 'pt_1f_L_021_c'    ,len(b_pt)-1,b_pt), 'ptcone021')
                    _h_pt_1f_L_021_glu   = _dfl_021_glu[i]  .Histo1D(('pt_1f_L_021_glu'  , 'pt_1f_L_021_glu'  ,len(b_pt)-1,b_pt), 'ptcone021')
                    _h_pt_1f_L_021_b     = _dfl_021_b[i]    .Histo1D(('pt_1f_L_021_b'    , 'pt_1f_L_021_b'    ,len(b_pt)-1,b_pt), 'ptcone021')
                    _h_pt_1f_L_021_light = _dfl_021_light[i].Histo1D(('pt_1f_L_021_light', 'pt_1f_L_021_light',len(b_pt)-1,b_pt), 'ptcone021')
                    _h_pt_1f_L_021_other = _dfl_021_other[i].Histo1D(('pt_1f_L_021_other', 'pt_1f_L_021_other',len(b_pt)-1,b_pt), 'ptcone021')

                    h_pt_1f_T_021_c      = _h_pt_1f_T_021_c.GetPtr()
                    h_pt_1f_T_021_glu    = _h_pt_1f_T_021_glu.GetPtr()
                    h_pt_1f_T_021_b      = _h_pt_1f_T_021_b.GetPtr()
                    h_pt_1f_T_021_light  = _h_pt_1f_T_021_light.GetPtr()
                    h_pt_1f_T_021_other  = _h_pt_1f_T_021_other.GetPtr()

                    h_pt_1f_L_021_c      = _h_pt_1f_L_021_c.GetPtr()
                    h_pt_1f_L_021_glu    = _h_pt_1f_L_021_glu.GetPtr()
                    h_pt_1f_L_021_b      = _h_pt_1f_L_021_b.GetPtr()
                    h_pt_1f_L_021_light  = _h_pt_1f_L_021_light.GetPtr()
                    h_pt_1f_L_021_other  = _h_pt_1f_L_021_other.GetPtr()
                print '\n\tfilling 021 done.'

            if mode012 ==True:

                if fullSplit == False:
                    _h_pt_1f_T_012_light = _dft_012_light[i].Histo1D(('pt_1f_T_012_light', 'pt_1f_T_012_light',len(b_pt)-1,b_pt), 'ptcone012')
                    _h_pt_1f_T_012_heavy = _dft_012_heavy[i].Histo1D(('pt_1f_T_012_heavy', 'pt_1f_T_012_heavy',len(b_pt)-1,b_pt), 'ptcone012')

                    _h_pt_1f_L_012_light = _dfl_012_light[i].Histo1D(('pt_1f_L_012_light', 'pt_1f_L_012_light',len(b_pt)-1,b_pt), 'ptcone012')
                    _h_pt_1f_L_012_heavy = _dfl_012_heavy[i].Histo1D(('pt_1f_L_012_heavy', 'pt_1f_L_012_heavy',len(b_pt)-1,b_pt), 'ptcone012')

                    h_pt_1f_T_012_light  = _h_pt_1f_T_012_light.GetPtr()
                    h_pt_1f_T_012_heavy  = _h_pt_1f_T_012_heavy.GetPtr()

                    h_pt_1f_L_012_light  = _h_pt_1f_L_012_light.GetPtr()
                    h_pt_1f_L_012_heavy  = _h_pt_1f_L_012_heavy.GetPtr()

                if fullSplit == True:
                    _h_pt_1f_T_012_c     = _dft_012_c[i]    .Histo1D(('pt_1f_T_012_c'    , 'pt_1f_T_012_c'    ,len(b_pt)-1,b_pt), 'ptcone012')
                    _h_pt_1f_T_012_glu   = _dft_012_glu[i]  .Histo1D(('pt_1f_T_012_glu'  , 'pt_1f_T_012_glu'  ,len(b_pt)-1,b_pt), 'ptcone012')
                    _h_pt_1f_T_012_b     = _dft_012_b[i]    .Histo1D(('pt_1f_T_012_b'    , 'pt_1f_T_012_b'    ,len(b_pt)-1,b_pt), 'ptcone012')
                    _h_pt_1f_T_012_light = _dft_012_light[i].Histo1D(('pt_1f_T_012_light', 'pt_1f_T_012_light',len(b_pt)-1,b_pt), 'ptcone012')
                    _h_pt_1f_T_012_other = _dft_012_other[i].Histo1D(('pt_1f_T_012_other', 'pt_1f_T_012_other',len(b_pt)-1,b_pt), 'ptcone012')
                                                  
                    _h_pt_1f_L_012_c     = _dfl_012_c[i]    .Histo1D(('pt_1f_L_012_c'    , 'pt_1f_L_012_c'    ,len(b_pt)-1,b_pt), 'ptcone012')
                    _h_pt_1f_L_012_glu   = _dfl_012_glu[i]  .Histo1D(('pt_1f_L_012_glu'  , 'pt_1f_L_012_glu'  ,len(b_pt)-1,b_pt), 'ptcone012')
                    _h_pt_1f_L_012_b     = _dfl_012_b[i]    .Histo1D(('pt_1f_L_012_b'    , 'pt_1f_L_012_b'    ,len(b_pt)-1,b_pt), 'ptcone012')
                    _h_pt_1f_L_012_light = _dfl_012_light[i].Histo1D(('pt_1f_L_012_light', 'pt_1f_L_012_light',len(b_pt)-1,b_pt), 'ptcone012')
                    _h_pt_1f_L_012_other = _dfl_012_other[i].Histo1D(('pt_1f_L_012_other', 'pt_1f_L_012_other',len(b_pt)-1,b_pt), 'ptcone012')

                    h_pt_1f_T_012_c      = _h_pt_1f_T_012_c.GetPtr()
                    h_pt_1f_T_012_glu    = _h_pt_1f_T_012_glu.GetPtr()
                    h_pt_1f_T_012_b      = _h_pt_1f_T_012_b.GetPtr()
                    h_pt_1f_T_012_light  = _h_pt_1f_T_012_light.GetPtr()
                    h_pt_1f_T_012_other  = _h_pt_1f_T_012_other.GetPtr()

                    h_pt_1f_L_012_c      = _h_pt_1f_L_012_c.GetPtr()
                    h_pt_1f_L_012_glu    = _h_pt_1f_L_012_glu.GetPtr()
                    h_pt_1f_L_012_b      = _h_pt_1f_L_012_b.GetPtr()
                    h_pt_1f_L_012_light  = _h_pt_1f_L_012_light.GetPtr()
                    h_pt_1f_L_012_other  = _h_pt_1f_L_012_other.GetPtr()
                print '\n\tfilling 012 done.'


            ### ADDING 012 + 021
            if fullSplit == False:
                h_pt_1f_T_012_light.Add(h_pt_1f_T_021_light)
                h_pt_1f_T_012_heavy.Add(h_pt_1f_T_021_heavy)
                print '\n\th entries tight:', h_pt_1f_T_012_heavy.GetEntries(), h_pt_1f_T_012_light.GetEntries()
                print '\th sum tight:', h_pt_1f_T_012_heavy.GetEntries() + h_pt_1f_T_012_light.GetEntries()

                h_pt_1f_T_012.Add(h_pt_1f_T_012_light)  
                h_pt_1f_T_012.Add(h_pt_1f_T_012_heavy)  
                print '\th entries tight:', h_pt_1f_T_012.GetEntries()

                h_pt_1f_L_012_light.Add(h_pt_1f_L_021_light)
                h_pt_1f_L_012_heavy.Add(h_pt_1f_L_021_heavy)
                print '\n\th entries  loose:', h_pt_1f_L_012_heavy.GetEntries(), h_pt_1f_L_012_light.GetEntries()
                print '\th sum loose:', h_pt_1f_L_012_heavy.GetEntries() + h_pt_1f_L_012_light.GetEntries()

                h_pt_1f_L_012.Add(h_pt_1f_L_012_light)  
                h_pt_1f_L_012.Add(h_pt_1f_L_012_heavy)  
                print '\th entries loose:', h_pt_1f_L_012.GetEntries()

            if fullSplit == True:
                h_pt_1f_T_012_c    .Add(h_pt_1f_T_021_c)
                h_pt_1f_T_012_b    .Add(h_pt_1f_T_021_b)
                h_pt_1f_T_012_glu  .Add(h_pt_1f_T_021_glu)
                h_pt_1f_T_012_other.Add(h_pt_1f_T_021_other)
                h_pt_1f_T_012_light.Add(h_pt_1f_T_021_light)
                print '\n\th entries tight:', h_pt_1f_T_012_c.GetEntries(), h_pt_1f_T_012_light.GetEntries(), h_pt_1f_T_012_b.GetEntries(), h_pt_1f_T_012_other.GetEntries(), h_pt_1f_T_012_glu.GetEntries()
                print '\th sum tight:', h_pt_1f_T_012_c.GetEntries() + h_pt_1f_T_012_light.GetEntries() + h_pt_1f_T_012_b.GetEntries() + h_pt_1f_T_012_other.GetEntries() + h_pt_1f_T_012_glu.GetEntries()

                h_pt_1f_T_012.Add(h_pt_1f_T_012_b)  
                h_pt_1f_T_012.Add(h_pt_1f_T_012_glu)  
                h_pt_1f_T_012.Add(h_pt_1f_T_012_c)  
                h_pt_1f_T_012.Add(h_pt_1f_T_012_light)  
                h_pt_1f_T_012.Add(h_pt_1f_T_012_other)  
                print '\th entries tight:', h_pt_1f_T_012.GetEntries()

                h_pt_1f_L_012_c    .Add(h_pt_1f_L_021_c)
                h_pt_1f_L_012_b    .Add(h_pt_1f_L_021_b)
                h_pt_1f_L_012_glu  .Add(h_pt_1f_L_021_glu)
                h_pt_1f_L_012_other.Add(h_pt_1f_L_021_other)
                h_pt_1f_L_012_light.Add(h_pt_1f_L_021_light)
                print '\n\th entries  loose:', h_pt_1f_L_012_c.GetEntries(), h_pt_1f_L_012_light.GetEntries(), h_pt_1f_L_012_b.GetEntries(), h_pt_1f_L_012_other.GetEntries(), h_pt_1f_L_012_glu.GetEntries()
                print '\th sum loose:', h_pt_1f_L_012_c.GetEntries() + h_pt_1f_L_012_light.GetEntries() + h_pt_1f_L_012_b.GetEntries() + h_pt_1f_L_012_other.GetEntries() + h_pt_1f_L_012_glu.GetEntries()

                h_pt_1f_L_012.Add(h_pt_1f_L_012_b)  
                h_pt_1f_L_012.Add(h_pt_1f_L_012_glu)  
                h_pt_1f_L_012.Add(h_pt_1f_L_012_c)  
                h_pt_1f_L_012.Add(h_pt_1f_L_012_light)  
                h_pt_1f_L_012.Add(h_pt_1f_L_012_other)  
                print '\th entries loose:', h_pt_1f_L_012.GetEntries()

            ### EFFICIENCIES
            if fullSplit == False:
                h_pt_1f['light'] = rt.TEfficiency(h_pt_1f_T_012_light, h_pt_1f_L_012_light)
                h_pt_1f['heavy'] = rt.TEfficiency(h_pt_1f_T_012_heavy, h_pt_1f_L_012_heavy)

                h_pt_1f['light'].SetTitle('light; p_{T} [GeV]; tight-to-loose ratio (single fakes)')
                h_pt_1f['heavy'].SetTitle('heavy; p_{T} [GeV]; tight-to-loose ratio (single fakes)')

                h_pt_1f['light'].SetMarkerColor(rt.kBlue+1)
                h_pt_1f['heavy'].SetMarkerColor(rt.kRed+1)

                h_pt_1f['light'].SetFillColor(rt.kWhite)
                h_pt_1f['heavy'].SetFillColor(rt.kWhite)

            if fullSplit == True:
                h_pt_1f['c']     = rt.TEfficiency(h_pt_1f_T_012_c,     h_pt_1f_L_012_c)
                h_pt_1f['b']     = rt.TEfficiency(h_pt_1f_T_012_b,     h_pt_1f_L_012_b)
                h_pt_1f['glu']   = rt.TEfficiency(h_pt_1f_T_012_glu,   h_pt_1f_L_012_glu)
                h_pt_1f['light'] = rt.TEfficiency(h_pt_1f_T_012_light, h_pt_1f_L_012_light)
                h_pt_1f['other'] = rt.TEfficiency(h_pt_1f_T_012_other, h_pt_1f_L_012_other)
                h_pt_1f['all']   = rt.TEfficiency(h_pt_1f_T_012,       h_pt_1f_L_012)

                h_pt_1f['c']    .SetTitle(    'c; p_{T} [GeV]; tight-to-loose ratio (single fakes)')
                h_pt_1f['glu']  .SetTitle(  'glu; p_{T} [GeV]; tight-to-loose ratio (single fakes)')
                h_pt_1f['b']    .SetTitle(    'b; p_{T} [GeV]; tight-to-loose ratio (single fakes)')
                h_pt_1f['other'].SetTitle('other; p_{T} [GeV]; tight-to-loose ratio (single fakes)')
                h_pt_1f['light'].SetTitle('light; p_{T} [GeV]; tight-to-loose ratio (single fakes)')
                h_pt_1f['all'].  SetTitle(  'all; p_{T} [GeV]; tight-to-loose ratio (single fakes)')

                h_pt_1f['b']    .SetMarkerColor(rt.kRed+1)
                h_pt_1f['glu']  .SetMarkerColor(rt.kYellow+3)
                h_pt_1f['c']    .SetMarkerColor(rt.kMagenta+1)
                h_pt_1f['other'].SetMarkerColor(rt.kGreen+1)
                h_pt_1f['light'].SetMarkerColor(rt.kBlue+1)
                h_pt_1f['all']  .SetMarkerColor(rt.kBlack)

                h_pt_1f['c']    .SetFillColor(rt.kWhite)
                h_pt_1f['glu']  .SetFillColor(rt.kWhite)
                h_pt_1f['b']    .SetFillColor(rt.kWhite)
                h_pt_1f['other'].SetFillColor(rt.kWhite)
                h_pt_1f['light'].SetFillColor(rt.kWhite)
                h_pt_1f['all']  .SetFillColor(rt.kWhite)

            ### DEBUGGING: LOG HISTO'S TO FILE
            if dbg == True:
                outfile = rt.TFile(plotDir + '1f_hists.root', 'recreate')
                outfile.cd()
                h_pt_1f_T_012.Write()
                h_pt_1f_L_012.Write()
                h_pt_1f_T_012_b.Write()
                h_pt_1f_L_012_light.Write()
                h_pt_1f_T_012_c.Write()
                h_pt_1f_L_012_light.Write()
                h_pt_1f['c']    .Write()
                h_pt_1f['b']    .Write()
                h_pt_1f['glu']  .Write()
                h_pt_1f['light'].Write()
                h_pt_1f['other'].Write()
                h_pt_1f['all']  .Write()
                outfile.Close()

            ### PLOTTING
            c_pt_1f = rt.TCanvas('ptCone_1f', 'ptCone_1f')
            framer.Draw()
            framer.GetYaxis().SetTitle('tight-to-loose ratio')
            framer.GetXaxis().SetTitle('p^{cone}_{T} [GeV]')
#                c.SetLogy()
            h_pt_1f['light'].Draw('same')
            leg = rt.TLegend(0.57, 0.78, 0.80, 0.9)
            leg.AddEntry(h_pt_1f['light'], h_pt_1f['light'].GetTitle())
            if fullSplit == True:
                h_pt_1f['b']    .Draw('same')
                h_pt_1f['c']    .Draw('same')
                h_pt_1f['glu']  .Draw('same')
                h_pt_1f['other'].Draw('same')
                h_pt_1f['all']  .Draw('same')
                leg.AddEntry(h_pt_1f['b']    , h_pt_1f['b']    .GetTitle())
                leg.AddEntry(h_pt_1f['c']    , h_pt_1f['c']    .GetTitle())
                leg.AddEntry(h_pt_1f['glu']  , h_pt_1f['glu']  .GetTitle())
                leg.AddEntry(h_pt_1f['other'], h_pt_1f['other'].GetTitle())
                leg.AddEntry(h_pt_1f['all']  , h_pt_1f['all']  .GetTitle())
            if fullSplit == False:
                h_pt_1f['heavy'].Draw('same')
                leg.AddEntry(h_pt_1f['heavy'], h_pt_1f['heavy'].GetTitle())
            leg.Draw()
            pf.showlogoprelimsim('CMS')
            pf.showlumi(ch+eta)
            save(knvs=c_pt_1f, sample='TT_DY_WJ', ch=ch+eta, DIR=plotDir)

            print '\n\tsingle-fakes done ...'
 
        if dfr:

            cuts_FR = 'abs(l1_dz) < 2 && abs(l2_dz) < 2 && hnl_2d_disp > 0.5 && l1_q * l2_q < 0'
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

            t.Draw(PTCONE + ' >> pt_cone_2f_T', cut_T + ' && hnl_dr_12 < 0.8 && ' + twoFakes_sameJet)
            print '\tentries tight:', h_pt_2f_T.GetEntries()

            t.Draw(PTCONE + '>> pt_cone_2f_L' , cut_L + ' && hnl_dr_12 < 0.8 && ' + twoFakes_sameJet)
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
            save(knvs=c_pt_2f, sample='', ch=ch+eta)

        i += 1
        print '\n\t %s done'%eta
 

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
        save(knvs=c_pt_cmprd, sample='', ch=ch+eta)

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
        save(knvs=c_pt_2f, sample='cmbnd', ch=ch+eta)

    print '\n\t %s done'%ch
    sys.stderr = sys.__stderr__
    sys.stdout = sys.__stdout__
###########################################################################################################################################################################################

###########################################################################################################################################################################################
def closureTest(ch='mmm', eta_split=False, isData=False, VLD=False):
    
    plotDir = makeFolder('closureTest_%s'%ch)
    print '\n\tplotDir:', plotDir
    sys.stdout = Logger(plotDir + 'closureTest_%s' %ch)

    print '\n\tmode: %s\n'%ch
    l_eta  = {'_eta_all' : '1 == 1'}
    l_cuts_sfr = ['1 == 1', '1 == 1', '1 == 1']

    if eta_split == True: 

        if ch == 'mem':
            l_eta = {'_eta_00t08' : 'abs(l1_eta) < 0.8', '_eta_08t15' : 'abs(l1_eta) > 0.8 && abs(l1_eta) < 1.479', '_eta_15t25' : 'abs(l1_eta) > 1.479 && abs(l1_eta) < 2.5'}
            l_cuts_sfr = ['l1_reliso_rho_03 < 0.6','l1_reliso_rho_03 < 0.35','l1_reliso_rho_03 < 0.35']

        if ch == 'mmm':
            l_eta = {'_eta_00t12' : 'abs(l1_eta) < 1.2', '_eta_12t21' : 'abs(l1_eta) > 1.2 && abs(l1_eta) < 2.1', '_eta_21t24' : 'abs(l1_eta) > 2.1 && abs(l1_eta) < 2.4'}

    ### PREPARE CUTS AND FILES
    SFR, DFR, dirs = selectCuts(ch)

    l0l1, l0l2, l1_loose, l2_loose, l1_lnt, l2_lnt, l1_tight, l2_tight = SFR 
    LOOSE, TIGHT, LOOSENOTTIGHT = DFR
    DYBB_dir, DY10_dir, DY50_dir, DY50_ext_dir, TT_dir, W_dir, W_ext_dir = dirs   

    dRdefList, sHdefList = selectDefs(ch)

    l0_is_fake, no_fakes, one_fake_xor, two_fakes, twoFakes_sameJet = dRdefList

    ### APPLICATION REGION
    appReg = 'hnl_w_vis_m < 80'
    appReg = '1 == 1' # RIC: FIRST DO VALIDITY TEST OF THE METHOD

    ii = 0
    for eta in l_eta.keys():
        h_pt_1f = {}; h_pt_2f = []; i = 0

        ### PREPARE TREES
        t = None
    #    t = rt.TChain('tree')
    #    t.Add(DYBB_dir + suffix)
    #    t.Add(DY10_dir + suffix)
    #    t.Add(DY50_dir + suffix)
    #    t.Add(DY50_ext_dir + suffix)
    #    t.Add(TT_dir + suffix)
    ##    t.Add(W_dir + suffix)
    #    t.Add(W_ext_dir + suffix)
        fin = rt.TFile('/afs/cern.ch/work/m/manzoni/public/forVinzenzDavid/mme_tree.root'); t = fin.Get('tree')
        df = rdf(t)
        print'\n\tchain made.'

#        cuts_SFR = 'hnl_dr_12 > 0.4 && abs(91.19 - hnl_m_01) > 10 && abs(91.19 - hnl_m_02) > 10 && ' + l_eta[eta]
        cuts_SFR = appReg + ' && hnl_dr_12 > 0.3 && ' + l_eta[eta] + ' && ' + l_cuts_sfr[ii]
        ii += 1
        print '\n\t cuts: %s'%cuts_SFR
        
        if isData == False:
            
            mode021 = False; mode012 = False

            if ch == 'mem':
                mode021 = True
                l1_loose += ' && ( (l1_reliso_rho_03 < 0.6 && abs(l1_eta) < 0.8) || (l1_reliso_rho_03 < 0.35 && abs(l1_eta) > 0.8) )'
                
            if ch == 'mmm':
                mode021 = True
                mode012 = True

            if mode021 == True:

                print '\n\t l0l2: %s\n'       %(l0l2)
                print '\n\t l1_loose: %s\n'   %(l1_loose)
                print '\n\t l1_lnt: %s\n'     %(l1_lnt)
                print '\n\t l1_tight: %s\n'   %(l1_tight)

                f0_021 = df.Filter(cuts_FR + ' && ' + l0l2 + ' && ' + l1_loose)
                print '\n\tloose df 021 defined.'

                dfl_021   = f0_021.Define('ptcone021', PTCONE)
                dfl0_021  = dfl_021.Filter(l1_lnt)
                print '\n\tlnt df 021 defined.'

                print '\n\tlnt df 021 events:', dfl0_021.Count().GetValue()

                dflnt_021 = dfl0_021.Define('fover1minusf021', selectBins(ch=ch,lep=1))
                if label == True:
                    dflntDYbb_021   = dflnt_021.Filter('label == 0')# && abs(l1_gen_match_pdgid) != 22 && l1_gen_match_isPromptFinalState == 0')
                    dflntDY50_021   = dflnt_021.Filter('label == 1 && abs(l1_gen_match_pdgid) != 22 && l1_gen_match_isPromptFinalState == 0')
                    dflntTT_021     = dflnt_021.Filter('label == 2')# && abs(l1_gen_match_pdgid) != 22 && l1_gen_match_isPromptFinalState == 0')
                    dflnt_extConv   = dflnt_021.Filter('abs(l1_gen_match_pdgid) == 22') 
                    dflnt_intConv   = dflnt_021.Filter('l1_gen_match_isPromptFinalState == 1') 
                print '\n\tweight f/(1-f)  021 defined. (without lumi/data normalization)'

                dft_021     = dfl_021.Filter(l1_tight)
                if label == True:
                    dftDYbb_021   = dft_021.Filter('label == 0')# && abs(l1_gen_match_pdgid) != 22 && l1_gen_match_isPromptFinalState == 0')
                    dftDY50_021   = dft_021.Filter('label == 1 && abs(l1_gen_match_pdgid) != 22 && l1_gen_match_isPromptFinalState == 0')
                    dftTT_021     = dft_021.Filter('label == 2')# && abs(l1_gen_match_pdgid) != 22 && l1_gen_match_isPromptFinalState == 0')
                    dft_extConv   = dft_021.Filter('abs(l1_gen_match_pdgid) == 22') 
                    dft_intConv   = dft_021.Filter('l1_gen_match_isPromptFinalState == 1') 
                print '\n\ttight df 021 defined.'

                print '\n\ttight df 021 events:', dft_021.Count().GetValue()

                print '\n\tf0 021 entries:', f0_021.Count().GetValue()

            if mode012 == True:

                print '\n\t l0l1: %s\n'       %(l0l1)
                print '\n\t l2_loose: %s\n'   %(l2_loose)
                print '\n\t l2_lnt: %s\n'     %(l2_lnt)
                print '\n\t l2_tight: %s\n'   %(l2_tight)

                f0_012 = df.Filter(cuts_FR + ' && ' + l0l1 + ' && ' + l2_loose)
                print '\n\tloose df 012 defined.'

                dfl_012   = f0_012.Define('ptcone012', PTCONE)
                dfl0_012  = dfl_012.Filter(l2_lnt)
                print '\n\tlnt df 012 defined.'

                print '\n\tlnt df 012 events:', dfl0_012.Count().GetValue()

                dflnt_012 = dfl0_012.Define('fover1minusf012', selectBins(ch=ch,lep=2))
                print '\n\tweight f/(1-f)  012 defined. (without lumi/data normalization)'

                dft_012   = dfl_012.Filter(l2_tight)
                print '\n\ttight df 012 defined.'

                print '\n\ttight df 012 events:', dft_012.Count().GetValue()

                print '\n\tf0 012 entries:', f0_012.Count().GetValue()


        if mode021 == True:

            if label == False:
                obs_021_pt         = dft_021.Histo1D(('obs_021_pt',         'obs_021_pt',        len(b_pt)-1,     b_pt),     'ptcone021'      )
                obs_021_dr_12      = dft_021.Histo1D(('obs_021_dr_12',      'obs_021_dr_12',     len(b_dR)-1,     b_dR),     'hnl_dr_12'      )
                obs_021_2disp      = dft_021.Histo1D(('obs_021_2disp',      'obs_021_2disp',     len(b_2d)-1,     b_2d),     'hnl_2d_disp'    )
                obs_021_2disp_sig  = dft_021.Histo1D(('obs_021_2disp_sig',  'obs_021_2disp_sig', len(b_2d_sig)-1, b_2d_sig), 'hnl_2d_disp_sig')
                obs_021_m_dimu     = dft_021.Histo1D(('obs_021_m_dimu',     'obs_021_m_dimu',    len(b_m)-1,      b_m),      'hnl_m_12'       )
                obs_021_BGM_dimu   = dft_021.Histo1D(('obs_021_BGM_dimu',   'obs_021_BGM_dimu',  len(b_M)-1,      b_M),      'hnl_m_12'       )
                obs_021_BGM_01     = dft_021.Histo1D(('obs_021_BGM_01',     'obs_021_BGM_01',    len(b_M)-1,      b_M),      'hnl_m_01'       )
                obs_021_BGM_02     = dft_021.Histo1D(('obs_021_BGM_02',     'obs_021_BGM_02',    len(b_M)-1,      b_M),      'hnl_m_02'       )
                obs_021_m_triL     = dft_021.Histo1D(('obs_021_m_triL',     'obs_021_m_triL',    len(b_M)-1,      b_M),      'hnl_w_vis_m'    )

                whd_021_pt         = dflnt_021.Histo1D(('whd_021_pt',         'whd_021_pt',        len(b_pt)-1,      b_pt),     'ptcone021',         'fover1minusf021')
                whd_021_dr_12      = dflnt_021.Histo1D(('whd_021_dr_12',      'whd_021_dr_12',     len(b_dR)-1,      b_dR),     'hnl_dr_12',         'fover1minusf021')
                whd_021_2disp      = dflnt_021.Histo1D(('whd_021_2disp',      'whd_021_2disp',     len(b_2d)-1,      b_2d),     'hnl_2d_disp',       'fover1minusf021')
                whd_021_2disp_sig  = dflnt_021.Histo1D(('whd_021_2disp_sig',  'whd_021_2disp_sig', len(b_2d_sig)-1,  b_2d_sig), 'hnl_2d_disp_sig',   'fover1minusf021')
                whd_021_m_dimu     = dflnt_021.Histo1D(('whd_021_m_dimu',     'whd_021_m_dimu',    len(b_m)-1,       b_m),      'hnl_m_12',          'fover1minusf021')
                whd_021_BGM_dimu   = dflnt_021.Histo1D(('whd_021_BGM_dimu',   'whd_021_BGM_dimu',  len(b_M)-1,       b_M),      'hnl_m_12',          'fover1minusf021')
                whd_021_BGM_01     = dflnt_021.Histo1D(('whd_021_BGM_01',     'whd_021_BGM_01',    len(b_M)-1,       b_M),      'hnl_m_01',          'fover1minusf021')
                whd_021_BGM_02     = dflnt_021.Histo1D(('whd_021_BGM_02',     'whd_021_BGM_02',    len(b_M)-1,       b_M),      'hnl_m_02',          'fover1minusf021')
                whd_021_m_triL     = dflnt_021.Histo1D(('whd_021_m_triL',     'whd_021_m_triL',    len(b_M)-1,       b_M),      'hnl_w_vis_m',       'fover1minusf021')

                h_list_021 = { 'pt'          : [whd_021_pt,        obs_021_pt,        ],
                               'dr_12'       : [whd_021_dr_12,     obs_021_dr_12,     ],
                               '2disp'       : [whd_021_2disp,     obs_021_2disp,     ],
                               '2disp_sig'   : [whd_021_2disp_sig, obs_021_2disp_sig, ],
                               'm_dimu'      : [whd_021_m_dimu,    obs_021_m_dimu,    ],
                               'BGM_dimu'    : [whd_021_BGM_dimu,  obs_021_BGM_dimu,  ],
                               'BGM_01'      : [whd_021_BGM_01,    obs_021_BGM_01,    ],
                               'BGM_02'      : [whd_021_BGM_02,    obs_021_BGM_02,    ],
                               'm_triL'      : [whd_021_m_triL,    obs_021_m_triL,    ]}

            if label == True:

            VARS = {'pt':        [len(b_pt)-1,     b_pt,     'ptcone012'      ],
                    'dr_12':     [len(b_dR)-1,     b_dR,     'hnl_dr_12'      ],
                    '2disp':     [len(b_2d)-1,     b_2d,     'hnl_2d_disp'    ],
                    '2disp_sig': [len(b_2d_sig)-1, b_2d_sig, 'hnl_2d_disp_sig'],
                    'm_dimu':    [len(b_m)-1,      b_m,      'hnl_m_12'       ],
                    'BGM_dimu':  [len(b_M)-1,      b_M,      'hnl_m_12'       ],
                    'BGM_01':    [len(b_M)-1,      b_M,      'hnl_m_01'       ],
                    'BGM_02':    [len(b_M)-1,      b_M,      'hnl_m_02'       ],
                    'm_triL':    [len(b_M)-1,      b_M,      'hnl_w_vis_m'    ]}

                  dft_021_L = {'DYbb' : dftDYbb_021,   'DY50' : dftDY50_021,   'TT' : dftTT_021,   'extConv' : dft_extConv_021,   'intConv' : dft_intConv_021  }
                dflnt_021_L = {'DYbb' : dflntDYbb_021, 'DY50' : dflntDY50_021, 'TT' : dflntTT_021, 'extConv' : dflnt_extConv_021, 'intConv' : dflnt_intConv_021 }

                _H_DFT_021   = OrderedDict()
                _H_DFLNT_021 = OrderedDict()
                H_DFT_021    = OrderedDict()
                H_DFLNT_021  = OrderedDict()

                for v in VARS.keys():
                    _H_DFT_021[v]   : OrderedDict()
                    _H_DFLNT_021[v] : OrderedDict()
                    H_DFT_021[v]    : OrderedDict()
                    H_DFLNT_021[v]  : OrderedDict()

                    for DF in dft_021_L.keys():
                        _H_DFT_021[v][DF]   : dft_021_L[DF]  .Histo1D(('obs_021_%s'%v,'obs_021_%s'%v, VARS[v][0], VARS[v][1]), VARS[v][2]))
                        _H_DFLNT_021[v][DF] : dflnt_021_L[DF].Histo1D(('whd_021_%s'%v,'whd_021_%s'%v, VARS[v][0], VARS[v][1]), VARS[v][2]), 'fover1minusf021')

                for v in VARS.keys():
                    for DF in dft_021_L.keys():
                        print '\n\tDrawing:', v, DF
                        H_DFT_021[v][DF]   : _H_DFT_021[v][DF]  .GetPtr()
                        H_DFLNT_021[v][DF] : _H_DFLNT_021[v][DF].GetPtr()

                    stack = rt.THStack()    
                    c = rt.TCanvas('asd','asd'); c.cd()


        if mode012 == True:

            obs_012_pt         = dft_012.Histo1D(('obs_012_pt',         'obs_012_pt',        len(b_pt)-1,     b_pt),     'ptcone012'      )
            obs_012_dr_12      = dft_012.Histo1D(('obs_012_dr_12',      'obs_012_dr_12',     len(b_dR)-1,     b_dR),     'hnl_dr_12'      )
            obs_012_2disp      = dft_012.Histo1D(('obs_012_2disp',      'obs_012_2disp',     len(b_2d)-1,     b_2d),     'hnl_2d_disp'    )
            obs_012_2disp_sig  = dft_012.Histo1D(('obs_012_2disp_sig',  'obs_012_2disp_sig', len(b_2d_sig)-1, b_2d_sig), 'hnl_2d_disp_sig')
            obs_012_m_dimu     = dft_012.Histo1D(('obs_012_m_dimu',     'obs_012_m_dimu',    len(b_m)-1,      b_m),      'hnl_m_12'       )
            obs_012_BGM_dimu   = dft_012.Histo1D(('obs_012_BGM_dimu',   'obs_012_BGM_dimu',  len(b_M)-1,      b_M),      'hnl_m_12'       )
            obs_012_BGM_01     = dft_012.Histo1D(('obs_012_BGM_01',     'obs_012_BGM_01',    len(b_M)-1,      b_M),      'hnl_m_01'       )
            obs_012_BGM_02     = dft_012.Histo1D(('obs_012_BGM_02',     'obs_012_BGM_02',    len(b_M)-1,      b_M),      'hnl_m_02'       )
            obs_012_m_triL     = dft_012.Histo1D(('obs_012_m_triL',     'obs_012_m_triL',    len(b_M)-1,      b_M),      'hnl_w_vis_m'    )

            whd_012_pt         = dflnt_012.Histo1D(('whd_012_pt',         'whd_012_pt',        len(b_pt)-1,      b_pt),     'ptcone012',         'fover1minusf012')
            whd_012_dr_12      = dflnt_012.Histo1D(('whd_012_dr_12',      'whd_012_dr_12',     len(b_dR)-1,      b_dR),     'hnl_dr_12',         'fover1minusf012')
            whd_012_2disp      = dflnt_012.Histo1D(('whd_012_2disp',      'whd_012_2disp',     len(b_2d)-1,      b_2d),     'hnl_2d_disp',       'fover1minusf012')
            whd_012_2disp_sig  = dflnt_012.Histo1D(('whd_012_2disp_sig',  'whd_012_2disp_sig', len(b_2d_sig)-1,  b_2d_sig), 'hnl_2d_disp_sig',   'fover1minusf012')
            whd_012_m_dimu     = dflnt_012.Histo1D(('whd_012_m_dimu',     'whd_012_m_dimu',    len(b_m)-1,       b_m),      'hnl_m_12',          'fover1minusf012')
            whd_012_BGM_dimu   = dflnt_012.Histo1D(('whd_012_BGM_dimu',   'whd_012_BGM_dimu',  len(b_M)-1,       b_M),      'hnl_m_12',          'fover1minusf012')
            whd_012_BGM_01     = dflnt_012.Histo1D(('whd_012_BGM_01',     'whd_012_BGM_01',    len(b_M)-1,       b_M),      'hnl_m_01',          'fover1minusf012')
            whd_012_BGM_02     = dflnt_012.Histo1D(('whd_012_BGM_02',     'whd_012_BGM_02',    len(b_M)-1,       b_M),      'hnl_m_02',          'fover1minusf012')
            whd_012_m_triL     = dflnt_012.Histo1D(('whd_012_m_triL',     'whd_012_m_triL',    len(b_M)-1,       b_M),      'hnl_w_vis_m',       'fover1minusf012')


            h_list_012 = { 'pt'          : [whd_012_pt,        obs_012_pt,        ],
                           'dr_12'       : [whd_012_dr_12,     obs_012_dr_12,     ],
                           '2disp'       : [whd_012_2disp,     obs_012_2disp,     ],
                           '2disp_sig'   : [whd_012_2disp_sig, obs_012_2disp_sig, ],
                           'm_dimu'      : [whd_012_m_dimu,    obs_012_m_dimu,    ],
                           'BGM_dimu'    : [whd_012_BGM_dimu,  obs_012_BGM_dimu,  ],
                           'BGM_01'      : [whd_012_BGM_01,    obs_012_BGM_01,    ],
                           'BGM_02'      : [whd_012_BGM_02,    obs_012_BGM_02,    ],
                           'm_triL'      : [whd_012_m_triL,    obs_012_m_triL,    ]}

        info  = { 'pt'          : [b_pt,     ';p_{T}^{cone} [GeV]; Counts'], 
                  'dr_12'       : [b_dR,     ';#DeltaR(l_{1},  l_{2}); Counts'], 
                  '2disp'       : [b_2d,     ';2d_disp [cm]; Counts'], 
                  '2disp_sig'   : [b_2d_sig, ';2d_disp_sig ; Counts'], 
                  'm_dimu'      : [b_m,      ';m(l_{1},  l_{2}) [GeV]; Counts'], 
                  'BGM_dimu'    : [b_M,      ';m(l_{1},  l_{2}) [GeV]; Counts'], 
                  'BGM_01'      : [b_M,      ';m(l_{0},  l_{1}) [GeV]; Counts'], 
                  'BGM_02'      : [b_M,      ';m(l_{0},  l_{2}) [GeV]; Counts'], 
                  'm_triL'      : [b_M,      ';m(l_{0},  l_{1},  l_{2}) [GeV]; Counts'], }

        if label == False:
            for k in info.keys():

                print'\n\tdrawing', k 

                whd_021 = rt.TH1F('whd_021_'+k,'whd_021_'+k,len(info[k][0])-1,info[k][0])
                obs_021 = rt.TH1F('obs_021_'+k,'obs_021_'+k,len(info[k][0])-1,info[k][0])

                whd_012 = rt.TH1F('whd_012_'+k,'whd_012_'+k,len(info[k][0])-1,info[k][0])
                obs_012 = rt.TH1F('obs_012_'+k,'obs_012_'+k,len(info[k][0])-1,info[k][0])

                if mode021 == True:
                    whd_021 = h_list_021[k][0].GetPtr()
                    obs_021 = h_list_021[k][1].GetPtr()

                if mode012 == True:
                    whd_012 = h_list_012[k][0].GetPtr()
                    obs_012 = h_list_012[k][1].GetPtr()

                whd_012.Add(whd_021)
                obs_012.Add(obs_021)

                whd = whd_012; obs = obs_012

                if k == 'pt':
                    print '\n\tyields. weighed: %0.2f, observed: %0.2f' %(whd.GetEntries(), obs.GetEntries())

                c = rt.TCanvas(k, k)
                whd.SetLineColor(rt.kGreen+2); whd.SetLineWidth(2); whd.SetMarkerStyle(0)
                whd.SetTitle(info[k][1])
                obs.SetTitle(info[k][1])
                obs.SetMarkerColor(rt.kMagenta+2)
                obs.Draw()
                whd.Draw('histEsame')
                leg = rt.TLegend(0.57, 0.78, 0.80, 0.9)
                leg.AddEntry(obs, 'observed')
                leg.AddEntry(whd, 'expected')
                leg.Draw()
                pf.showlogoprelimsim('CMS')
                pf.showlumi('SFR_'+ch+eta)
                save(c, sample='DDE', ch=ch+eta, DIR=plotDir)

    sys.stderr = sys.__stderr__
    sys.stdout = sys.__stdout__
######################################################################################

######################################################################################
## FIXME TODO PLAN IS TO USE THIS INSTEAD OF REPEATING THE SAME IN EVERY FUNCTION --> PREPARE AND RETURN DFs
def prepareDF(ch='mem'):

    ### PREPARE CUTS AND FILES
    SFR, DFR, dirs = selectCuts(ch)

    l0l1, l0l2, l1_loose, l2_loose, l1_lnt, l2_lnt, l1_tight, l2_tight = SFR 
    LOOSE, TIGHT, LOOSENOTTIGHT = DFR
    DYBB_dir, DY10_dir, DY50_dir, DY50_ext_dir, TT_dir, W_dir, W_ext_dir = dirs   

    dRdefList, sHdefList = selectDefs(ch)

    l0_is_fake, no_fakes, one_fake_xor, two_fakes, twoFakes_sameJet = dRdefList

    ### PREPARE DF
    t = None
    t = rt.TChain('tree')
    t.Add(DYBB_dir + suffix)
    t.Add(DY10_dir + suffix)
    t.Add(DY50_dir + suffix)
    t.Add(DY50_ext_dir + suffix)
    t.Add(TT_dir + suffix)
    t.Add(W_dir + suffix)
#    t.Add(W_ext_dir + suffix)
    df = rdf(t)
    print'\n\tchain made.'
    N_ENTRIES = df.Count()

    if sfr:

        #### GENERAL 
        print '\n\tpreparing single fakes ...'
        mode021 = False; mode012 = False

        cuts_FR = 'hnl_dr_12 > 0.4'

        #### CHANNEL SPECIFIC
        if ch == 'mem':
            mode021 = True
            cuts_FR += ' && abs(l1_gen_match_pdgid) != 22'

        if ch == 'mmm':
           mode012 = True
           mode021 = True

        ### PREPARE DATAFRAMES
        if mode021 == True:
            cuts_l_021 = cuts_FR + ' && l1_jet_flavour_parton != -99 && ' + l0l2 + ' && ' + l1_loose
            f0_021 = df.Filter(cuts_l_021)
            print '\n\tloose 021 defined.'

            dfl_021 = f0_021.Define('ptcone021', PTCONEL1)
            print '\n\tptcone 021: %s\n' %PTCONEL1
            print '\tptcone 021 defined.'

            if fullSplit == False:
                dfl_021_light = dfl_021.Filter('abs(l1_jet_flavour_parton) != 4 && abs(l1_jet_flavour_parton) != 5')
                dfl_021_heavy = dfl_021.Filter('abs(l1_jet_flavour_parton) == 4 || abs(l1_jet_flavour_parton) == 5')

            if fullSplit == True:
                dfl_021_b     = dfl_021.Filter('abs(l1_jet_flavour_parton) == 5')
                dfl_021_c     = dfl_021.Filter('abs(l1_jet_flavour_parton) == 4')
                dfl_021_glu   = dfl_021.Filter('abs(l1_jet_flavour_parton) == 21 || abs(l1_jet_flavour_parton) == 9')
                dfl_021_light = dfl_021.Filter('abs(l1_jet_flavour_parton) == 3 || abs(l1_jet_flavour_parton) == 2 || abs(l1_jet_flavour_parton) == 1')
                dfl_021_other = dfl_021.Filter('abs(l1_jet_flavour_parton) != 1 && abs(l1_jet_flavour_parton) != 2 && abs(l1_jet_flavour_parton) != 3 && abs(l1_jet_flavour_parton) != 4'\
                                               ' && abs(l1_jet_flavour_parton) != 5 && abs(l1_jet_flavour_parton) != 9 && abs(l1_jet_flavour_parton) != 21')
            print '\tflavours 021 defined.'

            if fullSplit == False:
                dfl_021_light_eta0 = dfl_021_light.Filter(l_eta[l_eta.keys()[0]])
                dfl_021_heavy_eta0 = dfl_021_heavy.Filter(l_eta[l_eta.keys()[0]])

                dfl_021_light_eta1 = dfl_021_light.Filter(l_eta[l_eta.keys()[1]])
                dfl_021_heavy_eta1 = dfl_021_heavy.Filter(l_eta[l_eta.keys()[1]])

                dfl_021_light_eta2 = dfl_021_light.Filter(l_eta[l_eta.keys()[2]])
                dfl_021_heavy_eta2 = dfl_021_heavy.Filter(l_eta[l_eta.keys()[2]])

            if fullSplit == True:
                dfl_021_c_eta0     = dfl_021_c    .Filter(l_eta[l_eta.keys()[0]])
                dfl_021_b_eta0     = dfl_021_b    .Filter(l_eta[l_eta.keys()[0]])
                dfl_021_glu_eta0   = dfl_021_glu  .Filter(l_eta[l_eta.keys()[0]])
                dfl_021_light_eta0 = dfl_021_light.Filter(l_eta[l_eta.keys()[0]])
                dfl_021_other_eta0 = dfl_021_other.Filter(l_eta[l_eta.keys()[0]])
     
                dfl_021_c_eta1     = dfl_021_c    .Filter(l_eta[l_eta.keys()[1]])
                dfl_021_b_eta1     = dfl_021_b    .Filter(l_eta[l_eta.keys()[1]])
                dfl_021_glu_eta1   = dfl_021_glu  .Filter(l_eta[l_eta.keys()[1]])
                dfl_021_light_eta1 = dfl_021_light.Filter(l_eta[l_eta.keys()[1]])
                dfl_021_other_eta1 = dfl_021_other.Filter(l_eta[l_eta.keys()[1]])
     
                dfl_021_c_eta2     = dfl_021_c    .Filter(l_eta[l_eta.keys()[2]])
                dfl_021_b_eta2     = dfl_021_b    .Filter(l_eta[l_eta.keys()[2]])
                dfl_021_glu_eta2   = dfl_021_glu  .Filter(l_eta[l_eta.keys()[2]])
                dfl_021_light_eta2 = dfl_021_light.Filter(l_eta[l_eta.keys()[2]])
                dfl_021_other_eta2 = dfl_021_other.Filter(l_eta[l_eta.keys()[2]])
            print '\tloose 021 eta defined.'

            if fullSplit == False:
                dft_021_light_eta0 = dfl_021_light_eta0.Filter(l1_tight)
                dft_021_heavy_eta0 = dfl_021_heavy_eta0.Filter(l1_tight)

                dft_021_light_eta1 = dfl_021_light_eta1.Filter(l1_tight)
                dft_021_heavy_eta1 = dfl_021_heavy_eta1.Filter(l1_tight)

                dft_021_light_eta2 = dfl_021_light_eta2.Filter(l1_tight)
                dft_021_heavy_eta2 = dfl_021_heavy_eta2.Filter(l1_tight)

            if fullSplit == True:
                dft_021_c_eta0     = dfl_021_c_eta0    .Filter(l1_tight)
                dft_021_b_eta0     = dfl_021_b_eta0    .Filter(l1_tight)
                dft_021_glu_eta0   = dfl_021_glu_eta0  .Filter(l1_tight)
                dft_021_light_eta0 = dfl_021_light_eta0.Filter(l1_tight)
                dft_021_other_eta0 = dfl_021_other_eta0.Filter(l1_tight)
    
                dft_021_c_eta1     = dfl_021_c_eta1    .Filter(l1_tight)
                dft_021_b_eta1     = dfl_021_b_eta1    .Filter(l1_tight)
                dft_021_glu_eta1   = dfl_021_glu_eta1  .Filter(l1_tight)
                dft_021_light_eta1 = dfl_021_light_eta1.Filter(l1_tight)
                dft_021_other_eta1 = dfl_021_other_eta1.Filter(l1_tight)
    
                dft_021_c_eta2     = dfl_021_c_eta2    .Filter(l1_tight)
                dft_021_b_eta2     = dfl_021_b_eta2    .Filter(l1_tight)
                dft_021_glu_eta2   = dfl_021_glu_eta2  .Filter(l1_tight)
                dft_021_light_eta2 = dfl_021_light_eta2.Filter(l1_tight)
                dft_021_other_eta2 = dfl_021_other_eta2.Filter(l1_tight)
            print '\ttight 021 defined.'

            if fullSplit == False:
                _dfl_021_light = [dfl_021_light_eta0, dfl_021_light_eta1, dfl_021_light_eta2]
                _dfl_021_heavy = [dfl_021_heavy_eta0, dfl_021_heavy_eta1, dfl_021_heavy_eta2]

                _dft_021_light = [dft_021_light_eta0, dft_021_light_eta1, dft_021_light_eta2]
                _dft_021_heavy = [dft_021_heavy_eta0, dft_021_heavy_eta1, dft_021_heavy_eta2]

            if fullSplit == True:
                _dfl_021_c     = [dfl_021_c_eta0    , dfl_021_c_eta1    , dfl_021_c_eta2    ] 
                _dfl_021_b     = [dfl_021_b_eta0    , dfl_021_b_eta1    , dfl_021_b_eta2    ] 
                _dfl_021_glu   = [dfl_021_glu_eta0  , dfl_021_glu_eta1  , dfl_021_glu_eta2  ]
                _dfl_021_light = [dfl_021_light_eta0, dfl_021_light_eta1, dfl_021_light_eta2]
                _dfl_021_other = [dfl_021_other_eta0, dfl_021_other_eta1, dfl_021_other_eta2]
          
                _dft_021_c     = [dft_021_c_eta0    , dft_021_c_eta1    , dft_021_c_eta2    ] 
                _dft_021_b     = [dft_021_b_eta0    , dft_021_b_eta1    , dft_021_b_eta2    ] 
                _dft_021_glu   = [dft_021_glu_eta0  , dft_021_glu_eta1  , dft_021_glu_eta2  ]
                _dft_021_light = [dft_021_light_eta0, dft_021_light_eta1, dft_021_light_eta2]
                _dft_021_other = [dft_021_other_eta0, dft_021_other_eta1, dft_021_other_eta2]


        if mode012 == True:
            cuts_l_012 = cuts_FR + ' && l2_jet_flavour_parton != -99 && ' + l0l1 + ' && ' + l2_loose 

            f0_012 = df.Filter(cuts_l_012)
            print '\n\tloose 012 defined.'

            dfl_012 = f0_012.Define('ptcone012', PTCONEL2)
            print '\n\tptcone 012: %s\n' %PTCONEL2
            print '\tptcone 012 defined.'

            if fullSplit == False:
                dfl_012_light = dfl_012.Filter('abs(l2_jet_flavour_parton) != 4 && abs(l2_jet_flavour_parton) != 5')
                dfl_012_heavy = dfl_012.Filter('abs(l2_jet_flavour_parton) == 4 || abs(l2_jet_flavour_parton) == 5')

            if fullSplit == True:
                dfl_012_b     = dfl_012.Filter('abs(l2_jet_flavour_parton) == 5')
                dfl_012_c     = dfl_012.Filter('abs(l2_jet_flavour_parton) == 4')
                dfl_012_glu   = dfl_012.Filter('abs(l2_jet_flavour_parton) == 21 || abs(l2_jet_flavour_parton) == 9')
                dfl_012_light = dfl_012.Filter('abs(l2_jet_flavour_parton) == 3 || abs(l2_jet_flavour_parton) == 2 || abs(l2_jet_flavour_parton) == 1')
                dfl_012_other = dfl_012.Filter('abs(l2_jet_flavour_parton) != 1 && abs(l2_jet_flavour_parton) != 2 && abs(l2_jet_flavour_parton) != 3 && abs(l2_jet_flavour_parton) != 4'\
                                               ' && abs(l2_jet_flavour_parton) != 5 && abs(l2_jet_flavour_parton) != 9 && abs(l2_jet_flavour_parton) != 21')
            print '\tflavours 012 defined.'

            if fullSplit == False:
                dfl_012_light_eta0 = dfl_012_light.Filter(re.sub('l1_eta','l2_eta',l_eta[l_eta.keys()[0]]))
                dfl_012_heavy_eta0 = dfl_012_heavy.Filter(re.sub('l1_eta','l2_eta',l_eta[l_eta.keys()[0]]))

                dfl_012_light_eta1 = dfl_012_light.Filter(re.sub('l1_eta','l2_eta',l_eta[l_eta.keys()[1]]))
                dfl_012_heavy_eta1 = dfl_012_heavy.Filter(re.sub('l1_eta','l2_eta',l_eta[l_eta.keys()[1]]))

                dfl_012_light_eta2 = dfl_012_light.Filter(re.sub('l1_eta','l2_eta',l_eta[l_eta.keys()[2]]))
                dfl_012_heavy_eta2 = dfl_012_heavy.Filter(re.sub('l1_eta','l2_eta',l_eta[l_eta.keys()[2]]))

            if fullSplit == True:
                dfl_012_c_eta0     = dfl_012_c    .Filter(re.sub('l1_eta','l2_eta',l_eta[l_eta.keys()[0]]))
                dfl_012_b_eta0     = dfl_012_b    .Filter(re.sub('l1_eta','l2_eta',l_eta[l_eta.keys()[0]]))
                dfl_012_glu_eta0   = dfl_012_glu  .Filter(re.sub('l1_eta','l2_eta',l_eta[l_eta.keys()[0]]))
                dfl_012_light_eta0 = dfl_012_light.Filter(re.sub('l1_eta','l2_eta',l_eta[l_eta.keys()[0]]))
                dfl_012_other_eta0 = dfl_012_other.Filter(re.sub('l1_eta','l2_eta',l_eta[l_eta.keys()[0]]))
     
                dfl_012_c_eta1     = dfl_012_c    .Filter(re.sub('l1_eta','l2_eta',l_eta[l_eta.keys()[1]]))
                dfl_012_b_eta1     = dfl_012_b    .Filter(re.sub('l1_eta','l2_eta',l_eta[l_eta.keys()[1]]))
                dfl_012_glu_eta1   = dfl_012_glu  .Filter(re.sub('l1_eta','l2_eta',l_eta[l_eta.keys()[1]]))
                dfl_012_light_eta1 = dfl_012_light.Filter(re.sub('l1_eta','l2_eta',l_eta[l_eta.keys()[1]]))
                dfl_012_other_eta1 = dfl_012_other.Filter(re.sub('l1_eta','l2_eta',l_eta[l_eta.keys()[1]]))
     
                dfl_012_c_eta2     = dfl_012_c    .Filter(re.sub('l1_eta','l2_eta',l_eta[l_eta.keys()[2]]))
                dfl_012_b_eta2     = dfl_012_b    .Filter(re.sub('l1_eta','l2_eta',l_eta[l_eta.keys()[2]]))
                dfl_012_glu_eta2   = dfl_012_glu  .Filter(re.sub('l1_eta','l2_eta',l_eta[l_eta.keys()[2]]))
                dfl_012_light_eta2 = dfl_012_light.Filter(re.sub('l1_eta','l2_eta',l_eta[l_eta.keys()[2]]))
                dfl_012_other_eta2 = dfl_012_other.Filter(re.sub('l1_eta','l2_eta',l_eta[l_eta.keys()[2]]))
            print '\tloose 012 eta defined.'

            if fullSplit == False:
                dft_012_light_eta0 = dfl_012_light_eta0.Filter(l2_tight)
                dft_012_heavy_eta0 = dfl_012_heavy_eta0.Filter(l2_tight)

                dft_012_light_eta1 = dfl_012_light_eta1.Filter(l2_tight)
                dft_012_heavy_eta1 = dfl_012_heavy_eta1.Filter(l2_tight)

                dft_012_light_eta2 = dfl_012_light_eta2.Filter(l2_tight)
                dft_012_heavy_eta2 = dfl_012_heavy_eta2.Filter(l2_tight)

            if fullSplit == True:
                dft_012_c_eta0     = dfl_012_c_eta0    .Filter(l2_tight)
                dft_012_b_eta0     = dfl_012_b_eta0    .Filter(l2_tight)
                dft_012_glu_eta0   = dfl_012_glu_eta0  .Filter(l2_tight)
                dft_012_light_eta0 = dfl_012_light_eta0.Filter(l2_tight)
                dft_012_other_eta0 = dfl_012_other_eta0.Filter(l2_tight)
     
                dft_012_c_eta1     = dfl_012_c_eta1    .Filter(l2_tight)
                dft_012_b_eta1     = dfl_012_b_eta1    .Filter(l2_tight)
                dft_012_glu_eta1   = dfl_012_glu_eta1  .Filter(l2_tight)
                dft_012_light_eta1 = dfl_012_light_eta1.Filter(l2_tight)
                dft_012_other_eta1 = dfl_012_other_eta1.Filter(l2_tight)
     
                dft_012_c_eta2     = dfl_012_c_eta2    .Filter(l2_tight)
                dft_012_b_eta2     = dfl_012_b_eta2    .Filter(l2_tight)
                dft_012_glu_eta2   = dfl_012_glu_eta2  .Filter(l2_tight)
                dft_012_light_eta2 = dfl_012_light_eta2.Filter(l2_tight)
                dft_012_other_eta2 = dfl_012_other_eta2.Filter(l2_tight)
            print '\ttight 012 defined.'

            if fullSplit == False:
                _dft_012_light = [dft_012_light_eta0, dft_012_light_eta1, dft_012_light_eta2]
                _dft_012_heavy = [dft_012_heavy_eta0, dft_012_heavy_eta1, dft_012_heavy_eta2]

                _dfl_012_light = [dfl_012_light_eta0, dfl_012_light_eta1, dfl_012_light_eta2]
                _dfl_012_heavy = [dfl_012_heavy_eta0, dfl_012_heavy_eta1, dfl_012_heavy_eta2]

            if fullSplit == True:
                _dfl_012_c     = [dfl_012_c_eta0    , dfl_012_c_eta1    , dfl_012_c_eta2    ] 
                _dfl_012_b     = [dfl_012_b_eta0    , dfl_012_b_eta1    , dfl_012_b_eta2    ] 
                _dfl_012_glu   = [dfl_012_glu_eta0  , dfl_012_glu_eta1  , dfl_012_glu_eta2  ]
                _dfl_012_light = [dfl_012_light_eta0, dfl_012_light_eta1, dfl_012_light_eta2]
                _dfl_012_other = [dfl_012_other_eta0, dfl_012_other_eta1, dfl_012_other_eta2]
          
                _dft_012_c     = [dft_012_c_eta0    , dft_012_c_eta1    , dft_012_c_eta2    ] 
                _dft_012_b     = [dft_012_b_eta0    , dft_012_b_eta1    , dft_012_b_eta2    ] 
                _dft_012_glu   = [dft_012_glu_eta0  , dft_012_glu_eta1  , dft_012_glu_eta2  ]
                _dft_012_light = [dft_012_light_eta0, dft_012_light_eta1, dft_012_light_eta2]
                _dft_012_other = [dft_012_other_eta0, dft_012_other_eta1, dft_012_other_eta2]
######################################################################################

######################################################################################
def checkIsoPDF_JetFlavour(ch='mmm',ID='No',eta_split=True,sfr=True,dR='03',fullSplit=False):

    plotDir = makeFolder('checkIsoPDF_%s' %ch)
    print '\n\tplotDir:', plotDir
    sys.stdout = Logger(plotDir + 'checkIsoPDF_%s' %ch)
    l_eta = None
    l_eta  = OrderedDict()
    l_eta['_eta_all'] = '1 == 1'

    if eta_split == True: 

        if ch == 'mem':
            l_eta = None
            l_eta = OrderedDict()
            l_eta ['_eta_00t08'] = 'abs(l1_eta) < 0.8'; l_eta ['_eta_08t15'] = 'abs(l1_eta) > 0.8 && abs(l1_eta) < 1.479'; l_eta ['_eta_15t25'] = 'abs(l1_eta) > 1.479 && abs(l1_eta) < 2.5'

        if ch == 'mmm':
            l_eta = None
            l_eta = OrderedDict()
            l_eta ['_eta_00t12'] = 'abs(l1_eta) < 1.2'; l_eta ['_eta_12t21'] = 'abs(l1_eta) > 1.2 && abs(l1_eta) < 2.1'; l_eta ['_eta_21t24'] = 'abs(l1_eta) > 2.1 && abs(l1_eta) < 2.4'

    ### PREPARE CUTS AND FILES
    SFR, DFR, dirs = selectCuts(ch)

    l0l1, l0l2, l1_loose, l2_loose, l1_lnt, l2_lnt, l1_tight, l2_tight = SFR 
    LOOSE, TIGHT, LOOSENOTTIGHT = DFR
    DYBB_dir, DY10_dir, DY50_dir, DY50_ext_dir, TT_dir, W_dir, W_ext_dir = dirs   

    dRdefList, sHdefList = selectDefs(ch)

    l0_is_fake, no_fakes, one_fake_xor, two_fakes, twoFakes_sameJet = dRdefList

    ### PREPARE TREES
    t = None
#    t = rt.TChain('tree')
#    t.Add(DYBB_dir + suffix)
#    t.Add(DY10_dir + suffix)
#    t.Add(DY50_dir + suffix)
#    t.Add(DY50_ext_dir + suffix)
#    t.Add(TT_dir + suffix)
##    t.Add(W_dir + suffix)
#    t.Add(W_ext_dir + suffix)
    fin = rt.TFile('/afs/cern.ch/work/m/manzoni/public/forVinzenzDavid/mme_tree.root'); t = fin.Get('tree')
    df = rdf(t)
    print'\n\tchain made.'
    N_ENTRIES = df.Count()

    if sfr:

        #### GENERAL 
        print '\n\tdrawing single fakes ...'
        mode021 = False; mode012 = False

        cuts_FR = 'hnl_dr_12 > 0.3'
        L1ID = ''
        L2ID = ''

        #### CHANNEL SPECIFIC
        if ch == 'mem':
            mode021 = True
            cuts_FR += ' && abs(l1_gen_match_pdgid) != 22'
            if ID == 'M':
                L1ID = ' && l1_MediumNoIso == 1'
            if ID == 'L':
                L1ID = ' && l1_LooseNoIso == 1'

        if ch == 'eem':
           mode012 = True
           if ID == 'M':
                L2ID = ' && l2_Medium == 1'

        if ch == 'mmm':
           mode012 = True
           mode021 = True
           if ID == 'M':
                L1ID = ' && l1_Medium == 1'
                L2ID = ' && l2_Medium == 1'

        ### PREPARE DATAFRAMES
        if mode021 == True:
            cuts_l_021 = cuts_FR + ' && l1_jet_flavour_parton != -99 && ' + l0l2 + ' && ' + l1_loose + L1ID 
            cuts_l_021 = re.sub('abs\(l._reliso_rho_0.\) < ... \&\& ', '', cuts_l_021)
            print cuts_l_021

            f0_021 = df.Filter(cuts_l_021)
            print '\n\tloose 021 defined.'

            dfl_021 = f0_021.Define('ptcone021', PTCONEL1)
            print '\n\tptcone 021: %s\n' %PTCONEL1
            print '\tptcone 021 defined.'

            dfl_021_light = dfl_021.Filter('abs(l1_jet_flavour_parton) != 4 && abs(l1_jet_flavour_parton) != 5')
            dfl_021_heavy = dfl_021.Filter('abs(l1_jet_flavour_parton) == 4 || abs(l1_jet_flavour_parton) == 5')

            print '\tflavours 021 defined.'

            dfl_021_light_eta0 = dfl_021_light.Filter(l_eta[l_eta.keys()[0]])
            dfl_021_heavy_eta0 = dfl_021_heavy.Filter(l_eta[l_eta.keys()[0]])

            dfl_021_light_eta1 = dfl_021_light.Filter(l_eta[l_eta.keys()[1]])
            dfl_021_heavy_eta1 = dfl_021_heavy.Filter(l_eta[l_eta.keys()[1]])

            dfl_021_light_eta2 = dfl_021_light.Filter(l_eta[l_eta.keys()[2]])
            dfl_021_heavy_eta2 = dfl_021_heavy.Filter(l_eta[l_eta.keys()[2]])
            print '\tloose 021 eta defined.'

            _dfl_021_light = [dfl_021_light_eta0, dfl_021_light_eta1, dfl_021_light_eta2]
            _dfl_021_heavy = [dfl_021_heavy_eta0, dfl_021_heavy_eta1, dfl_021_heavy_eta2]


        if mode012 == True:
            cuts_l_012 = cuts_FR + ' && l2_jet_flavour_parton != -99 && ' + l0l1 + ' && ' + l2_loose + L2ID
            cuts_l_012 = re.sub('abs\(l._reliso_rho_0.\) < ... \&\& ', '', cuts_l_012)
            print cuts_l_012

            f0_012 = df.Filter(cuts_l_012)
            print '\n\tloose 012 defined.'

            dfl_012 = f0_012.Define('ptcone012', PTCONEL2)
            print '\n\tptcone 012: %s\n' %PTCONEL2
            print '\tptcone 012 defined.'

            dfl_012_light = dfl_012.Filter('abs(l2_jet_flavour_parton) != 4 && abs(l2_jet_flavour_parton) != 5')
            dfl_012_heavy = dfl_012.Filter('abs(l2_jet_flavour_parton) == 4 || abs(l2_jet_flavour_parton) == 5')

            print '\tflavours 012 defined.'

            dfl_012_light_eta0 = dfl_012_light.Filter(re.sub('l1_eta','l2_eta',l_eta[l_eta.keys()[0]]))
            dfl_012_heavy_eta0 = dfl_012_heavy.Filter(re.sub('l1_eta','l2_eta',l_eta[l_eta.keys()[0]]))

            dfl_012_light_eta1 = dfl_012_light.Filter(re.sub('l1_eta','l2_eta',l_eta[l_eta.keys()[1]]))
            dfl_012_heavy_eta1 = dfl_012_heavy.Filter(re.sub('l1_eta','l2_eta',l_eta[l_eta.keys()[1]]))

            dfl_012_light_eta2 = dfl_012_light.Filter(re.sub('l1_eta','l2_eta',l_eta[l_eta.keys()[2]]))
            dfl_012_heavy_eta2 = dfl_012_heavy.Filter(re.sub('l1_eta','l2_eta',l_eta[l_eta.keys()[2]]))
            print '\tloose 012 eta defined.'

            if fullSplit == False:
                _dfl_012_light = [dfl_012_light_eta0, dfl_012_light_eta1, dfl_012_light_eta2]
                _dfl_012_heavy = [dfl_012_heavy_eta0, dfl_012_heavy_eta1, dfl_012_heavy_eta2]
        
        print '\n\t cuts: %s'                %cuts_FR
        if mode012 ==True:
            print '\ttotal 012 loose: %s\n'      %f0_012.Count().GetValue()
        if mode021 ==True:  
            print '\ttotal 021 loose: %s\n'      %f0_021.Count().GetValue()

    vars = {'reliso_rho_%s'%dR:[1500,0.01,15.01]}
    #'pt':[50,0.,102],  'abs_iso_rho': [150,0,150], 'abs_iso_db': [150,0,150]}#,  'l2_pt':[50,2,102], 'l0_pt':[50,2,102], 'abs_dxy':[60,0.05,3.05]}
    
    for var in vars.keys():

        print'\n\tdrawing %s \n'%var
        h_light_021_eta0 = rt.TH1F('l1_'+var+'eta0_light','l1_'+var+'eta0_light',vars[var][0],vars[var][1],vars[var][2])
        h_heavy_021_eta0 = rt.TH1F('l1_'+var+'eta0_heavy','l1_'+var+'eta0_heavy',vars[var][0],vars[var][1],vars[var][2])

        h_light_021_eta1 = rt.TH1F('l1_'+var+'eta1_light','l1_'+var+'eta1_light',vars[var][0],vars[var][1],vars[var][2])
        h_heavy_021_eta1 = rt.TH1F('l1_'+var+'eta1_heavy','l1_'+var+'eta1_heavy',vars[var][0],vars[var][1],vars[var][2])

        h_light_021_eta2 = rt.TH1F('l1_'+var+'eta2_light','l1_'+var+'eta2_light',vars[var][0],vars[var][1],vars[var][2])
        h_heavy_021_eta2 = rt.TH1F('l1_'+var+'eta2_heavy','l1_'+var+'eta2_heavy',vars[var][0],vars[var][1],vars[var][2])

        h_light_012_eta0 = rt.TH1F('l2_'+var+'eta0_light','l2_'+var+'eta0_light',vars[var][0],vars[var][1],vars[var][2])
        h_heavy_012_eta0 = rt.TH1F('l2_'+var+'eta0_heavy','l2_'+var+'eta0_heavy',vars[var][0],vars[var][1],vars[var][2])

        h_light_012_eta1 = rt.TH1F('l2_'+var+'eta1_light','l2_'+var+'eta1_light',vars[var][0],vars[var][1],vars[var][2])
        h_heavy_012_eta1 = rt.TH1F('l2_'+var+'eta1_heavy','l2_'+var+'eta1_heavy',vars[var][0],vars[var][1],vars[var][2])

        h_light_012_eta2 = rt.TH1F('l2_'+var+'eta2_light','l2_'+var+'eta2_light',vars[var][0],vars[var][1],vars[var][2])
        h_heavy_012_eta2 = rt.TH1F('l2_'+var+'eta2_heavy','l2_'+var+'eta2_heavy',vars[var][0],vars[var][1],vars[var][2])

        if ch =='mmm': 
           mode012 = True
           mode021 = True
 
        if mode021 == True:
            _h_light_021_eta0 = _dfl_021_light[0].Histo1D(('l1_'+var+'eta0_light','l1_'+var+'eta0_light',vars[var][0],vars[var][1],vars[var][2]),'l1_'+var)
            _h_heavy_021_eta0 = _dfl_021_heavy[0].Histo1D(('l1_'+var+'eta0_heavy','l1_'+var+'eta0_heavy',vars[var][0],vars[var][1],vars[var][2]),'l1_'+var)

            _h_light_021_eta1 = _dfl_021_light[1].Histo1D(('l1_'+var+'eta1_light','l1_'+var+'eta1_light',vars[var][0],vars[var][1],vars[var][2]),'l1_'+var)
            _h_heavy_021_eta1 = _dfl_021_heavy[1].Histo1D(('l1_'+var+'eta1_heavy','l1_'+var+'eta1_heavy',vars[var][0],vars[var][1],vars[var][2]),'l1_'+var)

            _h_light_021_eta2 = _dfl_021_light[2].Histo1D(('l1_'+var+'eta2_light','l1_'+var+'eta2_light',vars[var][0],vars[var][1],vars[var][2]),'l1_'+var)
            _h_heavy_021_eta2 = _dfl_021_heavy[2].Histo1D(('l1_'+var+'eta2_heavy','l1_'+var+'eta2_heavy',vars[var][0],vars[var][1],vars[var][2]),'l1_'+var)

            h_light_021_eta0 = _h_light_021_eta0.GetPtr()
            h_heavy_021_eta0 = _h_heavy_021_eta0.GetPtr()

            h_light_021_eta1 = _h_light_021_eta1.GetPtr()
            h_heavy_021_eta1 = _h_heavy_021_eta1.GetPtr()

            h_light_021_eta2 = _h_light_021_eta2.GetPtr()
            h_heavy_021_eta2 = _h_heavy_021_eta2.GetPtr()

        if mode012 == True:
            _h_light_012_eta0 = _dfl_012_light[0].Histo1D(('l2_'+var+'eta0_light','l2_'+var+'eta0_light',vars[var][0],vars[var][1],vars[var][2]),'l2_'+var)
            _h_heavy_012_eta0 = _dfl_012_heavy[0].Histo1D(('l2_'+var+'eta0_heavy','l2_'+var+'eta0_heavy',vars[var][0],vars[var][1],vars[var][2]),'l2_'+var)

            _h_light_012_eta1 = _dfl_012_light[1].Histo1D(('l2_'+var+'eta1_light','l2_'+var+'eta1_light',vars[var][0],vars[var][1],vars[var][2]),'l2_'+var)
            _h_heavy_012_eta1 = _dfl_012_heavy[1].Histo1D(('l2_'+var+'eta1_heavy','l2_'+var+'eta1_heavy',vars[var][0],vars[var][1],vars[var][2]),'l2_'+var)

            _h_light_012_eta2 = _dfl_012_light[2].Histo1D(('l2_'+var+'eta2_light','l2_'+var+'eta2_light',vars[var][0],vars[var][1],vars[var][2]),'l2_'+var)
            _h_heavy_012_eta2 = _dfl_012_heavy[2].Histo1D(('l2_'+var+'eta2_heavy','l2_'+var+'eta2_heavy',vars[var][0],vars[var][1],vars[var][2]),'l2_'+var)

            h_light_012_eta0 = _h_light_012_eta0.GetPtr()
            h_heavy_012_eta0 = _h_heavy_012_eta0.GetPtr()

            h_light_012_eta1 = _h_light_012_eta1.GetPtr()
            h_heavy_012_eta1 = _h_heavy_012_eta1.GetPtr()
 
            h_light_012_eta2 = _h_light_012_eta2.GetPtr()
            h_heavy_012_eta2 = _h_heavy_012_eta2.GetPtr()

        h_light_012_eta0.Add(h_light_021_eta0); h_light_eta0 = h_light_012_eta0
        h_heavy_012_eta0.Add(h_heavy_021_eta0); h_heavy_eta0 = h_heavy_012_eta0

        h_light_012_eta1.Add(h_light_021_eta1); h_light_eta1 = h_light_012_eta1
        h_heavy_012_eta1.Add(h_heavy_021_eta1); h_heavy_eta1 = h_heavy_012_eta1

        h_light_012_eta2.Add(h_light_021_eta2); h_light_eta2 = h_light_012_eta2
        h_heavy_012_eta2.Add(h_heavy_021_eta2); h_heavy_eta2 = h_heavy_012_eta2

        h_light_eta0.SetMarkerStyle(1); h_light_eta0.SetMarkerSize(0.7); h_light_eta0.SetMarkerColor(rt.kBlue+2); h_light_eta0.SetLineColor(rt.kBlue+2);  h_light_eta0.SetTitle('light_eta0')
        h_heavy_eta0.SetMarkerStyle(1); h_heavy_eta0.SetMarkerSize(0.7); h_heavy_eta0.SetMarkerColor(rt.kRed+2);  h_heavy_eta0.SetLineColor(rt.kRed+2);   h_heavy_eta0.SetTitle('heavy_eta0')

        h_light_eta1.SetMarkerStyle(1); h_light_eta1.SetMarkerSize(0.7); h_light_eta1.SetMarkerColor(rt.kBlue+2); h_light_eta1.SetLineColor(rt.kBlue+2);  h_light_eta1.SetTitle('light_eta1')
        h_heavy_eta1.SetMarkerStyle(1); h_heavy_eta1.SetMarkerSize(0.7); h_heavy_eta1.SetMarkerColor(rt.kRed+2);  h_heavy_eta1.SetLineColor(rt.kRed+2);   h_heavy_eta1.SetTitle('heavy_eta1')

        h_light_eta2.SetMarkerStyle(1); h_light_eta2.SetMarkerSize(0.7); h_light_eta2.SetMarkerColor(rt.kBlue+2); h_light_eta2.SetLineColor(rt.kBlue+2);  h_light_eta2.SetTitle('light_eta2')
        h_heavy_eta2.SetMarkerStyle(1); h_heavy_eta2.SetMarkerSize(0.7); h_heavy_eta2.SetMarkerColor(rt.kRed+2);  h_heavy_eta2.SetLineColor(rt.kRed+2);   h_heavy_eta2.SetTitle('heavy_eta2')

        _h_light = [h_light_eta0, h_light_eta1, h_light_eta2] 
        _h_heavy = [h_heavy_eta0, h_heavy_eta1, h_heavy_eta2] 

        i = 0
        for i_eta in l_eta.keys():
            print '\n\tcheck if correct:', i_eta, 'eta%d'%i

            h_light = _h_light[i]
            h_heavy = _h_heavy[i]

            h_light.Scale(1./h_light.Integral())
            h_heavy.Scale(1./h_heavy.Integral())

            CH=ch
            if l_eta[i_eta] != '1': CH=ch+i_eta

            c = rt.TCanvas(var,var)
            h_light.Draw()
            h_heavy.Draw('same')
            c.BuildLegend()
            pf.showlogoprelimsim('CMS')
            pf.showlumi(CH+'_'+var)
            save(c, sample='checkIsoPDF_ID'+ID, ch=CH, DIR=plotDir)

            h_light_cdf = h_light.GetCumulative()
            h_heavy_cdf = h_heavy.GetCumulative()

            h_light_cdf.SetMarkerStyle(1); h_light_cdf.SetMarkerSize(0.5); h_light_cdf.SetLineColor(rt.kGreen+2); h_light_cdf.SetMarkerColor(rt.kGreen+2); h_light_cdf.SetTitle('light')
            h_heavy_cdf.SetMarkerStyle(1); h_heavy_cdf.SetMarkerSize(0.5); h_heavy_cdf.SetLineColor(rt.kRed+2);   h_heavy_cdf.SetMarkerColor(rt.kRed+2);   h_heavy_cdf.SetTitle('heavy')

            c = rt.TCanvas('cdf_'+'rho_'+dR,'cdf_'+'rho_'+dR)
            h_light_cdf.Draw()
            h_heavy_cdf.Draw('same')
            c.BuildLegend()
            pf.showlogoprelimsim('CMS')
            pf.showlumi(CH+'cdf_'+'rho_'+dR)
            save(c, sample='checkIsoCDF_ID'+ID, ch=CH, DIR=plotDir)

            h_heavy_over_light = rt.TH1F('cdf_div','cdf_div', vars[var][0], vars[var][1], vars[var][2])
            h_heavy_over_light.Divide(h_heavy_cdf, h_light_cdf)

            c = rt.TCanvas('cdf_div_'+'rho_'+dR,'cdf_div_'+'rho_'+dR)
            h_heavy_over_light.GetXaxis().SetRangeUser(0.01,10)
            h_heavy_over_light.Draw()
            pf.showlogoprelimsim('CMS')
            pf.showlumi(CH+'_cdf_div_'+'rho_'+dR)
            c.SetLogx()
            save(c, sample='checkIsoCDF_ID'+ID, ch=CH, DIR=plotDir)
            i += 1

    sys.stderr = sys.__stderr__
    sys.stdout = sys.__stdout__
###########################################################################################################################################################################################
    #############       UTILS       ###############
###########################################################################################################################################################################################
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

        l0l1           = None
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

#TODO
#    if pairMode == 'mm':
#        no_fakes_dr         = no_fakes_mm_dr
#        one_fake_xor_dr     = one_fake_xor_mm_dr
#        two_fakes_dr        = two_fakes_mm_dr
#        twoFakes_sameJet_dr = twoFakes_sameJet_mm_dr 

    dRdefList = [l0_is_fake_dr, no_fakes_dr, one_fake_xor_dr, two_fakes_dr, twoFakes_sameJet_dr]
    sHdefList = [l0_is_fake_sh, no_fakes_sh, one_fake_xor_sh, two_fakes_sh, twoFakes_sameJet_sh]
 
    return dRdefList, sHdefList 
######################################################################################

######################################################################################
def save(knvs, iso=0, sample='', ch='', eta='', DIR=plotDir):
    if iso == 0: iso_str = '' 
    if iso != 0: iso_str = '_iso' + str(int(iso * 100))
    knvs.GetFrame().SetLineWidth(0)
    knvs.Modified(); knvs.Update()
    if len(eta):
        knvs.SaveAs('{dr}{smpl}_{ch}_{ttl}{iso}_eta{eta}.png' .format(dr=DIR, smpl=sample, ttl=knvs.GetTitle(), ch=ch, iso=iso_str, eta=eta))
        knvs.SaveAs('{dr}{smpl}_{ch}_{ttl}{iso}_eta{eta}.pdf' .format(dr=DIR, smpl=sample, ttl=knvs.GetTitle(), ch=ch, iso=iso_str, eta=eta))
        knvs.SaveAs('{dr}{smpl}_{ch}_{ttl}{iso}_eta{eta}.root'.format(dr=DIR, smpl=sample, ttl=knvs.GetTitle(), ch=ch, iso=iso_str, eta=eta))
    if not len(eta):
        if iso != 0:
            knvs.SaveAs('{dr}{smpl}_{ch}_{ttl}{iso}.png' .format(dr=DIR, smpl=sample, ttl=knvs.GetTitle(), ch=ch, iso=iso_str))
            knvs.SaveAs('{dr}{smpl}_{ch}_{ttl}{iso}.pdf' .format(dr=DIR, smpl=sample, ttl=knvs.GetTitle(), ch=ch, iso=iso_str))
            knvs.SaveAs('{dr}{smpl}_{ch}_{ttl}{iso}.root'.format(dr=DIR, smpl=sample, ttl=knvs.GetTitle(), ch=ch, iso=iso_str))
        if iso == 0:
            knvs.SaveAs('{dr}{smpl}_{ch}_{ttl}.png' .format(dr=DIR, smpl=sample, ttl=knvs.GetTitle(), ch=ch))
            knvs.SaveAs('{dr}{smpl}_{ch}_{ttl}.pdf' .format(dr=DIR, smpl=sample, ttl=knvs.GetTitle(), ch=ch))
            knvs.SaveAs('{dr}{smpl}_{ch}_{ttl}.root'.format(dr=DIR, smpl=sample, ttl=knvs.GetTitle(), ch=ch))
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

def makeFolder(name):

    plotDir = eos+'plots/DDE/'
    today   = datetime.now()
    date    = today.strftime('%d%m%y')
    h       = str(today.hour)
    mn      = str(today.minute)
 
    plotDir = plotDir + name + '_' + date + '_' + h + 'h_' + mn + 'm/'
    os.mkdir(plotDir)
    return plotDir


