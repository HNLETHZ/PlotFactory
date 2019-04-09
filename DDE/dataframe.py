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

today   = datetime.now()
date    = today.strftime('%y%m%d')
hour    = str(today.hour)
minit   = str(today.minute)

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
#rt.TStyle.SetOptStat(0)

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
DYBBDir_mem     = eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_mem/DYBB/'
DY50Dir_mem     = eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_mem/DYJetsToLL_M50/'
DY50_extDir_mem = eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_mem/DYJetsToLL_M50_ext/'
DY10Dir_mem     = eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_mem/DYJetsToLL_M10to50/'
TT_dir_mem      = eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_mem/TTJets/'  
W_dir_mem       = eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_mem/WJetsToLNu/'
W_ext_dir_mem   = eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_mem/WJetsToLNu_ext/'
data_B_mem      = eos+'ntuples/HN3Lv2.0/data/mem/2017B/Single_mu_2017B/HNLTreeProducer/tree.root'
###########################################################################################################################################################################################
DYBBDir_mmm     = eos_david+'ntuples/HN3Lv2.0/background/montecarlo/production20190318/mmm/ntuples/DYBB/'
DY50Dir_mmm     = eos_david+'ntuples/HN3Lv2.0/background/montecarlo/production20190318/mmm/ntuples/DYJetsToLL_M50/'
DY50_extDir_mmm = eos_david+'ntuples/HN3Lv2.0/background/montecarlo/production20190318/mmm/ntuples/DYJetsToLL_M50_ext/'
DY10Dir_mmm     = eos_david+'ntuples/HN3Lv2.0/background/montecarlo/production20190318/mmm/ntuples/DYJetsToLL_M10to50/'
TT_dir_mmm      = eos_david+'ntuples/HN3Lv2.0/background/montecarlo/production20190318/mmm/ntuples/TTJets/'  
W_dir_mmm       = eos_david+'ntuples/HN3Lv2.0/background/montecarlo/production20190318/mmm/ntuples/WJetsToLNu/'
W_ext_dir_mmm   = eos_david+'ntuples/HN3Lv2.0/background/montecarlo/production20190318/mmm/ntuples/WJetsToLNu_ext/'
data_B_mmm      = 'root://cms-xrd-transit.cern.ch//store/user/dezhu/2_ntuples/HN3Lv2.0/mmm/data/Single_mu_2017B/HNLTreeProducer/tree.root'
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
#######
## SKIMMED TREES
####
skim_mem = eos+'ntuples/mme_tree.root'
skim_mmm = eos+'ntuples/mmm_merged.root'
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
charge_02 = ' && hnl_q_02 == 0'
###########################################################################################################################################################################################
### FAKEABLE OBJECTS AND PROMPT LEPTON DEFINITIONS
###########################################################################################################################################################################################
### PROMPT LEPTONS
l0_m = 'l0_pt > 25 && abs(l0_eta) < 2.4 && abs(l0_dz) < 0.2 && abs(l0_dxy) < 0.05 && l0_reliso_rho_04 < 0.2 && l0_id_m == 1'                  # l0 genuine muon
l1_m = 'l1_pt > 10 && abs(l1_eta) < 2.4 && abs(l1_dz) < 0.2 && abs(l1_dxy) < 0.05 && l1_reliso_rho_04 < 0.2 && l1_id_m == 1'                  # l1 genuine muon 
l2_m = 'l2_pt > 10 && abs(l2_eta) < 2.4 && abs(l2_dz) < 0.2 && abs(l2_dxy) < 0.05 && l2_reliso_rho_04 < 0.2 && l2_id_m == 1'                  # l2 genuine muon 

l0_e = 'l0_pt > 25 && abs(l0_eta) < 2.5 && abs(l0_dz) < 0.2 && abs(l0_dxy) < 0.05 && l0_reliso_rho_04 < 0.2 && l0_eid_mva_iso_wp90 == 1'      # l0 genuine electron
l1_e = 'l1_pt > 10 && abs(l1_eta) < 2.5 && abs(l1_dz) < 0.2 && abs(l1_dxy) < 0.05 && l1_reliso_rho_04 < 0.2 && l1_eid_mva_iso_wp90 == 1'      # l1 genuine electron 
l2_e = 'l2_pt > 10 && abs(l2_eta) < 2.5 && abs(l2_dz) < 0.2 && abs(l2_dxy) < 0.05 && l2_reliso_rho_04 < 0.2 && l2_eid_mva_iso_wp90 == 1'      # l2 genuine electron 

### FAKEABLE OBJECTS
l1_m_loose  = 'l1_pt > 5 && abs(l1_eta) < 2.4 && abs(l1_dz) < 2 && abs(l1_dxy) > 0.05'                                              # l1 kinematics and impact parameter
l1_m_tight  = l1_m_loose + ' &&  l1_Medium == 1 && l1_reliso_rho_04 < 0.2'
l1_m_lnt    = l1_m_loose + ' && (l1_Medium == 0 || l1_reliso_rho_04 > 0.2)'

l2_m_loose  = 'l2_pt > 5 && abs(l2_eta) < 2.4 && abs(l2_dz) < 2 && abs(l2_dxy) > 0.05'                                              # l2 kinematics and impact parameter
l2_m_tight  = l2_m_loose + ' &&  l2_Medium == 1 && l2_reliso_rho_04 < 0.2'
l2_m_lnt    = l2_m_loose + ' && (l2_Medium == 0 || l2_reliso_rho_04 > 0.2)'

l1_e_loose  = 'l1_pt > 5 && abs(l1_eta) < 2.5 && abs(l1_dz) < 2 && abs(l1_dxy) > 0.05'                                              # l1 kinematics and impact parameter
l1_e_tight  = l1_e_loose + ' &&  l1_MediumNoIso == 1 && l1_reliso_rho_04 < 0.2'
l1_e_lnt    = l1_e_loose + ' && (l1_MediumNoIso == 0 || l1_reliso_rho_04 > 0.2)'

l2_e_loose  = 'l2_pt > 5 && abs(l2_eta) < 2.5 && abs(l2_dz) < 2 && abs(l2_dxy) > 0.05'                                              # l2 kinematics and impact parameter
l2_e_tight  = l2_e_loose + ' &&  l2_MediumNoIso == 1 && l2_reliso_rho_04 < 0.2'
l2_e_lnt    = l2_e_loose + ' && (l2_MediumNoIso == 0 || l2_reliso_rho_04 > 0.2)'
###########################################################################################################################################################################################
              ##                 DOUBLE FAKE RATE                   ##  
###########################################################################################################################################################################################
### DFR:: LOOSE CUTS OBTAINED THROUGH CDF HEAVY/LIGHT COMPARISON 
DFR_MMM_L_CUT = ''
DFR_MEM_L_CUT = ' && hnl_iso04_rel_rhoArea < 0.6'

### DFR::MMM 
DFR_MMM_L   =  l0_m + ' && ' + l1_m_loose + ' && ' + l2_m_loose 
DFR_MMM_L   += ' && hnl_q_12 == 0'                                  # opposite charge 
DFR_MMM_L   += DFR_MMM_L_CUT                                        # reliso bound for LOOSE cf. checkIso_mmm_220319
DFR_MMM_LNT =  DFR_MMM_L + ' && '  # FIXME                          
DFR_MMM_T   =  DFR_MMM_L + ' && ' + l1_m_tight + ' && ' + l2_m_tight 

### DFR::MMM 
DFR_MEM_L   =  l0_m + ' && ' + l1_e_loose + ' && ' + l2_m_loose 
DFR_MEM_L   += ' && hnl_q_12 == 0'                                  # opposite charge 
DFR_MEM_L   += DFR_MEM_L_CUT                                        # reliso bound for LOOSE cf. checkIso_mmm_220319
DFR_MEM_LNT =  DFR_MEM_L + ' && '  # FIXME                          
DFR_MEM_T   =  DFR_MEM_L + ' && ' + l1_e_tight + ' && ' + l2_m_tight 
###########################################################################################################################################################################################
              ##                 SINGLE FAKE RATE                   ##  
###########################################################################################################################################################################################
### SFR:: LOOSE CUTS OBTAINED THROUGH CDF HEAVY/LIGHT COMPARISON 
SFR_MMM_L_CUT = ' && ( (l1_reliso_rho_03 < 0.42 && abs(l1_eta) < 1.2) || (l1_reliso_rho_03 < 0.35 && abs(l1_eta) > 1.2) )'  # dR 03
#SFR_MEM_L_CUT = ' && ( (l1_reliso_rho_03 < 0.6  && abs(l1_eta) < 0.8) || (l1_reliso_rho_03 < 0.35 && abs(l1_eta) > 0.8) )'  # dR 03
SFR_MEM_L_CUT = ' && ( (l1_reliso_rho_04 < 0.4  && abs(l1_eta) < 0.8) || (l1_reliso_rho_04 < 0.7 && abs(l1_eta) > 0.8 && abs(l1_eta) < 1.479) || (l1_reliso_rho_04 < 0.3 && abs(l1_eta) > 1.479) )'  # dR 04

### SFR::MMM 
SFR_MMM_021_L   =  l0_m + ' && ' + l2_m + ' && ' + l1_m_loose 
SFR_MMM_021_L   += charge_02                                        # opposite charge 
SFR_MMM_021_L   += SFR_MMM_L_CUT                                    # reliso bound for LOOSE cf. checkIso_mmm_220319 
SFR_MMM_021_LNT =  SFR_MMM_021_L + ' && ' + l1_m_lnt
SFR_MMM_021_T   =  SFR_MMM_021_L + ' && ' + l1_m_tight 

SFR_MMM_012_L   =  l0_m + ' && ' + l1_m + ' && ' + l2_m_loose 
SFR_MMM_012_L   += re.sub('02', '01', charge_02)                    # opposite charge 
SFR_MMM_012_L   += re.sub('l1', 'l2', SFR_MMM_L_CUT)                # reliso bound for LOOSE cf. checkIso_mmm_220319 
SFR_MMM_012_LNT =  SFR_MMM_012_L + ' && ' + l2_m_lnt
SFR_MMM_012_T   =  SFR_MMM_012_L + ' && ' + l2_m_tight 

### SFR::MEM 
SFR_MEM_021_L   =  l0_m + ' && ' + l2_m + ' && ' + l1_e_loose 
SFR_MEM_021_L   += charge_02                                        # opposite charge 
#SFR_MEM_021_L   += SFR_MMM_L_CUT                                    # reliso bound for LOOSE cf. checkIso_mmm_220319 
SFR_MEM_021_LNT =  SFR_MEM_021_L + ' && ' + l1_e_lnt
SFR_MEM_021_T   =  SFR_MEM_021_L + ' && ' + l1_e_tight 

###########################################################################################################################################################################################
### ENERGY-IN-CONE CORRECTED PT
###########################################################################################################################################################################################
PTCONE   = '(  ( hnl_hn_vis_pt * (hnl_iso04_rel_rhoArea<0.2) ) + ( (hnl_iso04_rel_rhoArea>=0.2) * ( hnl_hn_vis_pt * (1. + hnl_iso04_rel_rhoArea - 0.2) ) )  )'
PTCONEL1 = '(  ( l1_pt         * (l1_reliso_rho_04<0.2) )      + ( (l1_reliso_rho_04>=0.2)      * ( l1_pt         * (1. + l1_reliso_rho_04 - 0.2) ) )  )'
PTCONEL2 = '(  ( l2_pt         * (l2_reliso_rho_04<0.2) )      + ( (l2_reliso_rho_04>=0.2)      * ( l2_pt         * (1. + l2_reliso_rho_04 - 0.2) ) )  )'
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
b_M         = np.arange(0.,204,4)
b_eta_mu    = np.array([0., 1.2, 2.1, 2.4]) 
b_eta_ele   = np.array([0., 0.8, 1.479, 2.5]) 
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
framer.GetYaxis().SetRangeUser(0.,1.0)
framer.GetYaxis().SetRangeUser(0.,0.5)
#framer.GetYaxis().SetRangeUser(0.01,0.5)
############################################################################################################################################################################

############################################################################################################################################################################
def selectBins(ch='mem', lep=1, isData=False):

    input = 'MC'
    if isData == True: input = 'DATA'

    l_pt   = { '_pt0t5'   : 'ptcone < 5',                  '_pt5t10' : 'ptcone > 5 && ptcone < 10',  '_pt10t15' : 'ptcone > 10 && ptcone < 15', '_pt15t20' : 'ptcone > 15 && ptcone < 20',
               '_pt20t25' : 'ptcone > 20 && ptcone < 25', '_pt25t35' : 'ptcone > 25 && ptcone < 35', '_pt35t50' : 'ptcone > 35 && ptcone < 50', '_pt50t70' : 'ptcone > 50'}# && ptcone < 70'}
    for i in l_pt.keys(): 
        l_pt[i] = re.sub('ptcone','ptcone021',l_pt[i])

    if ch == 'mem':
        f_in = rt.TFile(plotDir+'%s_T2Lratio_mem_ptCone_eta.root'%input)
    
        l_eta = {'eta_bin_0' : 'abs(l1_eta) < 0.8', 'eta_bin_1' : 'abs(l1_eta) > 0.8 && abs(l1_eta) < 1.479', 'eta_bin_2' : 'abs(l1_eta) > 1.479 && abs(l1_eta) < 2.5'}

    if ch == 'mmm':
        f_in = rt.TFile(plotDir+'%s_T2Lratio_mmm_ptCone_eta.root'%input)
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
############################################################################################################################################################################

######################################################################################
def map_FR(ch='mem',mode='sfr',isData=True):

    sfr = False; dfr = False; print '\n\tmode: %s, \tch: %s' %(mode, ch)
    if mode == 'sfr': sfr = True
    if mode == 'dfr': dfr = True

    plotDir = makeFolder('map_FR_%s'%ch)
    print '\n\tplotDir:', plotDir
    sys.stdout = Logger(plotDir + 'map_FR_%s' %ch)

    mode021 = False; mode012 = False; mshReg = ''
    cuts_FR_021 = ''; cuts_FR_012 = ''
    input = 'MC'
    if isData == True: input = 'DATA'

    ### PREPARE CUTS AND FILES
    SFR, DFR, dirs = selectCuts(ch)

    SFR_021_L, SFR_012_L, SFR_021_LNT, SFR_012_LNT, SFR_021_T, SFR_012_T = SFR 
    DFR_L, DFR_T, DFR_LNT = DFR
    DYBB_dir, DY10_dir, DY50_dir, DY50_ext_dir, TT_dir, W_dir, W_ext_dir = dirs   

    dRdefList, sHdefList = selectDefs(ch)

    l0_is_fake, no_fakes, one_fake_xor, two_fakes, twoFakes_sameJet = dRdefList
    
    mshReg  = 'hnl_w_vis_m > 80'
    mshReg  = '1 == 1'

    if sfr:

        #### GENERAL 
        ptconel1 = PTCONEL1
        ptconel2 = PTCONEL2
        print '\n\tdrawing single fakes ...'

        cuts_FR = mshReg + ' && hnl_dr_12 > 0.3'

        #### CHANNEL SPECIFIC
        if ch == 'eem':
            mode012 = True
            cuts_FR_012 = cuts_FR + ' && ' + SFR_EEM_012_L
            tight_021 = SFR_EEM_021_T

        if ch == 'mmm':
            cuts_FR_012 = cuts_FR + ' && ' + SFR_MMM_012_L
            cuts_FR_021 = cuts_FR + ' && ' + SFR_MMM_021_L
            tight_021 = SFR_MMM_021_T
            tight_012 = SFR_MMM_012_T
            mode012 = True
            mode021 = True

        if ch == 'mem':

            mode021 = True
            b_eta = b_eta_ele

            cuts_FR_021 =  cuts_FR + ' && ' + SFR_MEM_021_L 
            cuts_FR_021 += ' && hnl_dr_01 > 0.3'                                                        # no conversions, only use this to measure t2l ratio 
            tight_021   = SFR_MEM_021_T

            if isData == False:
                cuts_FR_021  += ' && l1_gen_match_pdgid != 22 && label == 1'  # DY50 only

        if ch == 'mmm':
            mode021 = True
            mode012 = True
            b_eta = b_eta_mu

            if isData == False:
                cuts_FR_021  += ' && l1_gen_match_pdgid != 22'# && label == 1' # DY50 only
                cuts_FR_012  += ' && l2_gen_match_pdgid != 22'# && label == 1' # DY50 only

            cuts_FR_012 = cuts_FR + ' && ' + SFR_MMM_012_L 
            cuts_FR_021 = cuts_FR + ' && ' + SFR_MMM_021_L 

            cuts_FR_021 += ' && hnl_dr_01 > 0.3'                                                        # no conversions, only use this to measure t2l ratio 
            cuts_FR_012 += ' && hnl_dr_02 > 0.3'                                                        # no conversions, only use this to measure t2l ratio 

            tight_012   = SFR_MMM_012_T
            tight_021   = SFR_MMM_021_T

    if dfr:

        #### GENERAL 
        ptconel1 = PTCONE
        print '\n\tdrawing double fakes ...'
        cuts_FR = 'hnl_dr_12 < 0.3'

        #### CHANNEL SPECIFIC
        if ch == 'mem':
            mode021 = True

            cuts_FR_021 = cuts_FR + ' && ' + DFR_MEM_L
            tight_021 = DFR_MEM_T
            b_eta = b_eta_mu

            if isData == False:
                cuts_FR_021  += ' && l1_gen_match_pdgid != 22 && label == 1'  # DY50 only

    h_pt_eta_T_012  = rt.TH2F('pt_eta_T_012','pt_eta_T_012',len(b_pt)-1,b_pt,len(b_eta)-1,b_eta)
    h_pt_eta_T_021  = rt.TH2F('pt_eta_T_021','pt_eta_T_021',len(b_pt)-1,b_pt,len(b_eta)-1,b_eta)
    h_pt_eta_L_012  = rt.TH2F('pt_eta_L_012','pt_eta_L_012',len(b_pt)-1,b_pt,len(b_eta)-1,b_eta)
    h_pt_eta_L_021  = rt.TH2F('pt_eta_L_021','pt_eta_L_021',len(b_pt)-1,b_pt,len(b_eta)-1,b_eta)

    ### PREPARE TREES
    t = None
#    t = rt.TChain('tree')
#    t.Add(data_B_mmm)
#    t.Add(DYBB_dir + suffix)
#    t.Add(DY10_dir + suffix)
#    t.Add(DY50_dir + suffix)
#    t.Add(DY50_ext_dir + suffix)
#    t.Add(TT_dir + suffix)
#    t.Add(W_dir + suffix)
#    t.Add(W_ext_dir + suffix)
    fin = rt.TFile(skim_mem); t = fin.Get('tree')
    df = rdf(t)
    print'\n\tchain made.'
    N_ENTRIES = df.Count()

    if mode021 == True:

        f0_021 = df.Filter(cuts_FR_021)

        print '\n\tf0_021 entries:', f0_021.Count().GetValue()

        df0_021 = f0_021.Define('ptcone021', ptconel1)
        print '\n\tptcone021 defined.'

        dfL_021 = df0_021.Define('abs_l1_eta', 'abs(l1_eta)')
        print '\n\tabs_l1_eta defined.'

        dfT_021 = dfL_021.Filter(tight_021)
        print '\n\ttight df_021 defined.'

        _pt_eta_T_021 = dfT_021.Histo2D(('pt_eta_T_021','pt_eta_T_021',len(b_pt)-1,b_pt,len(b_eta)-1,b_eta),'ptcone021','abs_l1_eta')
        _pt_eta_L_021 = dfL_021.Histo2D(('pt_eta_L_021','pt_eta_L_021',len(b_pt)-1,b_pt,len(b_eta)-1,b_eta),'ptcone021','abs_l1_eta')

        h_pt_eta_T_021 = _pt_eta_T_021.GetPtr()
        h_pt_eta_L_021 = _pt_eta_L_021.GetPtr()

    if mode012 == True:

        f0_012 = df.Filter(cuts_FR_012)

        print '\n\tf0_012 entries:', f0_012.Count().GetValue()

        df0_012 = f0_012.Define('ptcone012', ptconel2)
        print '\n\tptcone012 defined.'

        dfL_012 = df0_012.Define('abs_l2_eta', 'abs(l2_eta)')
        print '\n\tabs_l2_eta defined.'

        dfT_012 = dfL_012.Filter(tight_012)
        print '\n\ttight df_012 defined.'

        _pt_eta_T_012 = dfT_012.Histo2D(('pt_eta_T_012','pt_eta_T_012',len(b_pt)-1,b_pt,len(b_eta)-1,b_eta),'ptcone012','abs_l2_eta')
        _pt_eta_L_012 = dfL_012.Histo2D(('pt_eta_L_012','pt_eta_L_012',len(b_pt)-1,b_pt,len(b_eta)-1,b_eta),'ptcone012','abs_l2_eta')

        h_pt_eta_T_012 = _pt_eta_T_012.GetPtr()
        h_pt_eta_L_012 = _pt_eta_L_012.GetPtr()

    h_pt_eta_T_012.Add(h_pt_eta_T_021)
    h_pt_eta_L_012.Add(h_pt_eta_L_021)

    print '\n\t cuts: %s'                    %cuts_FR
    if mode012 ==True:
        print '\n\t loose 012: %s\n'         %(cuts_FR_012)
        print '\n\t tight 012: %s\n'         %(tight_012)
        print '\ttotal loose 012: %s\n'      %f0_012.Count().GetValue()
    if mode021 ==True:
        print '\n\t loose 021: %s\n'         %(cuts_FR_021)
        print '\n\t tight 021: %s\n'         %(tight_021)
        print '\ttotal loose 021: %s\n'      %f0_021.Count().GetValue()

    print '\n\tentries T && L: ', h_pt_eta_T_012.GetEntries(), h_pt_eta_L_012.GetEntries()

    c_pt_eta = rt.TCanvas('ptCone_eta', 'ptCone_eta')
    h_pt_eta_T_012.Divide(h_pt_eta_L_012)
    h_pt_eta_T_012.Draw('colztextE')
    h_pt_eta_T_012.SetTitle('; p_{T}^{cone} [GeV]; DiMuon |#eta|; tight-to-loose ratio')
    pf.showlogoprelimsim('CMS')
    pf.showlumi('SFR_'+ch)
    save(knvs=c_pt_eta, sample='%s_T2Lratio'%input, ch=ch, DIR=plotDir)

    sys.stderr = sys.__stderr__
    sys.stdout = sys.__stdout__
    # DO AGAIN WITH THREE DIFFERENT TEFFS TO GET ERROR
###########################################################################################################################################################################################

###########################################################################################################################################################################################
def happyTreeFriends(ch='mmm', mode='sfr', isData=True, label=True):
    
    sfr = False; dfr = False
    if mode == 'sfr': sfr = True
    if mode == 'dfr': dfr = True

    plotDir = makeFolder('friendTree_%s'%ch)
    print '\n\tplotDir:', plotDir
    sys.stdout = Logger(plotDir + 'friendTree_%s' %ch)

    print '\n\tmode: %s\n'%ch

    ### PREPARE DATAFRAMES
    t = None
    t = rt.TChain('tree')
    t.Add('root://cms-xrd-transit.cern.ch//store/user/dezhu/2_ntuples/HN3Lv2.0/mmm/data/Single_mu_2017B/HNLTreeProducer/tree.root')
    df = rdf(t)
    print'\n\tchain made.'

    if sfr: 

        ptconel1 = PTCONEL1; ptconel2 = PTCONEL2
        if ch == 'mem': mode021 = True
        if ch == 'mmm': 
            mode021 = True; mode012 = True

    if dfr: ptconel1 = PTCONE

    if mode021 == True:
        df_021   = df.Define('ptcone021', ptconel1)

        print '\n\tlnt df 021 events:', df_021.Count().GetValue()

        df_021 = df_021.Define('fover1minusf021', selectBins(ch=ch,lep=1,isData=isData))
        print '\n\tweight f/(1-f)  021 defined.'

    if mode012 == True:
        df_012   = df.Define('ptcone012', ptconel2)

        print '\n\tlnt df 012 events:', df_012.Count().GetValue()

        df_012 = df_012.Define('fover1minusf012', selectBins(ch=ch,lep=2,isData=isData))
        print '\n\tweight f/(1-f)  012 defined.'

    ## SAVE FR OUTPUT BRANCH IN TREE
    branchList_021 = rt.vector('string')(); branchList_012 = rt.vector('string')()
    for br in ['event', 'lumi']:
        branchList_021.push_back(br)
        branchList_012.push_back(br)
    if label == True: branchList_021.push_back('label'); branchList_012.push_back('label')
    time_string = ch + '_' + mode + '_' + date + '_' + hour + 'h_' + minit + 'm'
    if mode021 == True:
        branchList_021.push_back('fover1minusf021')
        df_021.Snapshot('tree', plotDir + 'fr_021_%s.root'%time_string, branchList_021)
    if mode012 == True:
        branchList_012.push_back('fover1minusf012')
        df_012.Snapshot('tree', plotDir + 'fr_012_%s.root'%time_string, branchList_012)
###########################################################################################################################################################################################

###########################################################################################################################################################################################
def checkTTLratio(ch='mmm',eta_split=True,mode='sfr',dbg=False):

    sfr = False; dfr = False; print '\n\tmode: %s, \tch: %s' %(mode, ch)
    if mode == 'sfr': sfr = True
    if mode == 'dfr': dfr = True

    plotDir = makeFolder('checkTTLratio_%s'%ch)
    print '\n\tplotDir:', plotDir
    sys.stdout = Logger(plotDir + 'checkTTLratio_%s' %ch)

    l_eta = None; l_eta  = OrderedDict()
    l_eta['_eta_all'] = '1 == 1'

    if eta_split == True: 

        if ch == 'mem' or ch == 'eee':
            l_eta = None; l_eta = OrderedDict()
            l_eta ['_eta_00t08'] = 'abs(l1_eta) < 0.8'; l_eta ['_eta_08t15'] = 'abs(l1_eta) > 0.8 && abs(l1_eta) < 1.479'; l_eta ['_eta_15t25'] = 'abs(l1_eta) > 1.479 && abs(l1_eta) < 2.5'

        if ch == 'mmm' or ch == 'eem':
            l_eta = None; l_eta = OrderedDict()
            l_eta ['_eta_00t12'] = 'abs(l1_eta) < 1.2'; l_eta ['_eta_12t21'] = 'abs(l1_eta) > 1.2 && abs(l1_eta) < 2.1'; l_eta ['_eta_21t24'] = 'abs(l1_eta) > 2.1 && abs(l1_eta) < 2.4'

        if dfr: 
            l_eta = None; l_eta = OrderedDict()
            l_eta ['_eta_00t12'] = 'abs(l1_eta) < 1.2'; l_eta ['_eta_12t21'] = 'abs(l1_eta) > 1.2 && abs(l1_eta) < 2.1'; l_eta ['_eta_21t24'] = 'abs(l1_eta) > 2.1 && abs(l1_eta) < 2.4'
            for i in l_eta.keys(): l_eta[i] = re.sub('l1', 'hnl_hn_vis', l_eta[i])


    ### PREPARE CUTS AND FILES
    SFR, DFR, dirs = selectCuts(ch)

    SFR_021_L, SFR_012_L, SFR_021_LNT, SFR_012_LNT, SFR_021_T, SFR_012_T = SFR 
    DFR_L, DFR_T, DFR_LNT = DFR
    DYBB_dir, DY10_dir, DY50_dir, DY50_ext_dir, TT_dir, W_dir, W_ext_dir = dirs   

    dRdefList, sHdefList = selectDefs(ch)

    l0_is_fake, no_fakes, one_fake_xor, two_fakes, twoFakes_sameJet = dRdefList
    
    if sfr:

        #### GENERAL 
        ptconel1 = PTCONEL1
        ptconel2 = PTCONEL2
        print '\n\tdrawing single fakes ...'
        mode021 = False; mode012 = False

        cuts_FR = 'hnl_dr_12 > 0.3'

        #### CHANNEL SPECIFIC
        if ch == 'mem':
            mode021 = True
            cuts_FR += ' && abs(l1_gen_match_pdgid) != 22'
            cuts_FR_021 = cuts_FR + ' && ' + SFR_MEM_021_L
            tight_021 = SFR_MEM_021_T

        if ch == 'eem':
            mode012 = True
            cuts_FR_012 = cuts_FR + ' && ' + SFR_EEM_012_L
            tight_021 = SFR_EEM_021_T

        if ch == 'mmm':
            cuts_FR_012 = cuts_FR + ' && ' + SFR_MMM_012_L
            cuts_FR_021 = cuts_FR + ' && ' + SFR_MMM_021_L
            tight_021 = SFR_MMM_021_T
            tight_012 = SFR_MMM_021_T
            mode012 = True
            mode021 = True

    if dfr: ## FOR DFR NO L1 < -- > L2 IS NEEDED => DRAW EVERYTHING WITH MODE021

        #### GENERAL 
        ptconel1 = PTCONE
        print '\n\tdrawing double fakes ...'
        mode021 = False; mode012 = False

        cuts_FR = 'hnl_dr_12 < 0.3'
        #### CHANNEL SPECIFIC
        if ch == 'mem':
            mode021 = True
            cuts_FR += ' && abs(l1_gen_match_pdgid) != 22'
            cuts_FR_021 = cuts_FR + ' && ' + DFR_MEM_L
            tight_021 = DFR_MEM_T

    ### PREPARE TREES
    t = None
#    t = rt.TChain('tree')
#    t.Add(DYBB_dir + suffix)
#    t.Add(DY10_dir + suffix)
#    t.Add(DY50_dir + suffix)
#    t.Add(DY50_ext_dir + suffix)
#    t.Add(TT_dir + suffix)
#    t.Add(W_dir + suffix)
#    t.Add(W_ext_dir + suffix)
    fin = rt.TFile(skim_mem); t = fin.Get('tree')
    df = rdf(t)
    print'\n\tchain made.'
    N_ENTRIES = df.Count()

    flavors = ['all', 'heavy', 'light']


    ### PREPARE DATAFRAMES
    if mode021 == True:
        cuts_l_021 = cuts_FR_021 + ' && l1_jet_flavour_parton != -99'
        f0_021 = df.Filter(cuts_l_021)
        print '\n\tloose 021 defined.'

        dfL_021 = f0_021.Define('ptcone021', ptconel1)
        print '\n\tptcone 021: %s\n' %ptconel1
        print '\tptcone 021 defined.'

        dfL_021_flvr = OrderedDict()
        for flvr in ['light', 'heavy']:
            dfL_021_flvr['light'] = dfL_021.Filter('abs(l1_jet_flavour_parton) != 4 && abs(l1_jet_flavour_parton) != 5')
            dfL_021_flvr['heavy'] = dfL_021.Filter('abs(l1_jet_flavour_parton) == 4 || abs(l1_jet_flavour_parton) == 5')
        print '\tflavours 021 defined.'

        dfL_021_flvr_ita = OrderedDict()
        dfT_021_flvr_ita = OrderedDict()
        for flvr in ['light', 'heavy']:
            dfL_021_flvr_ita[flvr] = OrderedDict()
            dfT_021_flvr_ita[flvr] = OrderedDict()
            for ita in l_eta.keys():
                dfL_021_flvr_ita[flvr][ita] = dfL_021_flvr[flvr].Filter(l_eta[ita])
                dfT_021_flvr_ita[flvr][ita] = dfL_021_flvr_ita[flvr][ita].Filter(tight_021)
        print '\tloose 021 eta defined.'
        print '\ttight 021 eta defined.'


    if mode012 == True:
        cuts_l_021 = cuts_FR_021 + ' && l1_jet_flavour_parton != -99'

        f0_012 = df.Filter(cuts_l_012)
        print '\n\tloose 012 defined.'

        dfL_012 = f0_012.Define('ptcone012', ptconel2)
        print '\n\tptcone 012: %s\n' %ptconel2
        print '\tptcone 012 defined.'

        dfL_012_flvr = OrderedDict()
        for flvr in ['light', 'heavy']:
            dfL_012_flvr['light'] = dfL_012.Filter('abs(l1_jet_flavour_parton) != 4 && abs(l1_jet_flavour_parton) != 5')
            dfL_012_flvr['heavy'] = dfL_012.Filter('abs(l1_jet_flavour_parton) == 4 || abs(l1_jet_flavour_parton) == 5')
        print '\tflavours 012 defined.'

        dfL_012_flvr_ita = OrderedDict()
        dfT_012_flvr_ita = OrderedDict()
        for flvr in ['light', 'heavy']:
            dfL_012_flvr_ita[flvr] = OrderedDict()
            dfT_012_flvr_ita[flvr] = OrderedDict()
            for ita in l_eta.keys():
                dfL_012_flvr_ita[flvr][ita] = dfL_012_flvr[flvr].Filter(l_eta[ita])
                dfT_012_flvr_ita[flvr][ita] = dfL_012_flvr_ita[flvr][ita].Filter(tight_012)
        print '\tloose 012 eta defined.'
        print '\ttight 012 defined.'


    print '\n\t cuts: %s'                    %cuts_FR
    if mode012 ==True:
        print '\n\t loose 012: %s\n'         %(cuts_FR_012)
        print '\n\t tight 012: %s\n'         %(tight_012)
        print '\ttotal loose 012: %s\n'      %f0_012.Count().GetValue()
    if mode021 ==True:
        print '\n\t loose 021: %s\n'         %(cuts_FR_021)
        print '\n\t tight 021: %s\n'         %(tight_021)
        print '\ttotal loose 021: %s\n'      %f0_021.Count().GetValue()

    i = 0
    for ita in l_eta.keys():
        print '\n\teta:', ita
        print '\n\teta cut:', l_eta[ita]

        if mode012 == True:
            print'\n\t','df 012 sum loose:',   dfL_012_flvr_ita['heavy'][ita].Count().GetValue() + dfL_012_flvr_ita['light'][ita].Count().GetValue()
            print'\t','df 012 entries loose:', dfL_012_flvr_ita['heavy'][ita].Count().GetValue(),  dfL_012_flvr_ita['light'][ita].Count().GetValue()
            print'\t','df 012 sum tight:',     dfT_012_flvr_ita['heavy'][ita].Count().GetValue() + dfT_012_flvr_ita['light'][ita].Count().GetValue()
            print'\t','df 012 entries tight:', dfT_012_flvr_ita['heavy'][ita].Count().GetValue(),  dfT_012_flvr_ita['light'][ita].Count().GetValue()
        if mode021 == True:
            print'\n\t','df 021 sum loose:',   dfL_021_flvr_ita['heavy'][ita].Count().GetValue() + dfL_021_flvr_ita['light'][ita].Count().GetValue()
            print'\t','df 021 entries loose:', dfL_021_flvr_ita['heavy'][ita].Count().GetValue(),  dfL_021_flvr_ita['light'][ita].Count().GetValue()
            print'\t','df 021 sum tight:',     dfT_021_flvr_ita['heavy'][ita].Count().GetValue() + dfT_021_flvr_ita['light'][ita].Count().GetValue()
            print'\t','df 021 entries tight:', dfT_021_flvr_ita['heavy'][ita].Count().GetValue(),  dfT_021_flvr_ita['light'][ita].Count().GetValue()

        h_pt = OrderedDict()
        for flvr in flavors:
            h_pt[flvr] = OrderedDict()
            for lbl in ['T_012','T_021','L_012','L_021']: 
                h_pt[flvr][lbl]   = rt.TH1F('pt_%s_%s'%(lbl,flvr),    'pt_%s_%s'%(lbl,flvr), len(b_pt)-1,b_pt)

        ### FILLING
        if mode021 ==True:

            _h_pt_L_021 = OrderedDict(); _h_pt_T_021 = OrderedDict()
            for flvr in ['heavy','light']:
                _h_pt_L_021[flvr] = dfL_021_flvr_ita[flvr][ita].Histo1D(('pt_L_021_%s'%flvr, 'pt_L_021_%s'%flvr, len(b_pt)-1, b_pt), 'ptcone021')
                _h_pt_T_021[flvr] = dfT_021_flvr_ita[flvr][ita].Histo1D(('pt_T_021_%s'%flvr, 'pt_T_021_%s'%flvr, len(b_pt)-1, b_pt), 'ptcone021')

                h_pt[flvr]['L_021']  = _h_pt_L_021[flvr].GetPtr()
                h_pt[flvr]['T_021']  = _h_pt_T_021[flvr].GetPtr()
            print '\n\tfilling 021 done.'

        if mode012 ==True:

            _h_pt_L_012 = OrderedDict(); _h_pt_T_012 = OrderedDict()
            for flvr in ['heavy','light']:
                _h_pt_L_012[flvr] = dfL_012_flvr_ita[flvr][ita].Histo1D(('pt_L_012_%s'%flvr, 'pt_L_012_%s'%flvr, len(b_pt)-1, b_pt), 'ptcone012')
                _h_pt_T_012[flvr] = dfT_012_flvr_ita[flvr][ita].Histo1D(('pt_T_012_%s'%flvr, 'pt_T_012_%s'%flvr, len(b_pt)-1, b_pt), 'ptcone012')

                h_pt[flvr]['L_012']  = _h_pt_L_012[flvr].GetPtr()
                h_pt[flvr]['T_012']  = _h_pt_T_012[flvr].GetPtr()
            print '\n\tfilling 012 done.'


        ### ADDING 012 + 021
        h_pt['light']['T_012'].Add(h_pt['light']['T_021'])
        h_pt['heavy']['T_012'].Add(h_pt['heavy']['T_021'])
        print '\n\th entries tight:', h_pt['heavy']['T_012'].GetEntries(), h_pt['light']['T_012'].GetEntries()
        print '\th sum tight:', h_pt['heavy']['T_012'].GetEntries() + h_pt['light']['T_012'].GetEntries()

        h_pt['all']['T_012'].Add(h_pt['light']['T_012'])  
        h_pt['all']['T_012'].Add(h_pt['heavy']['T_012'])  
        print '\th entries tight:', h_pt['all']['T_012'].GetEntries()

        h_pt['light']['L_012'].Add(h_pt['light']['L_021'])
        h_pt['heavy']['L_012'].Add(h_pt['heavy']['L_021'])
        print '\n\th entries  loose:', h_pt['heavy']['L_012'].GetEntries(), h_pt['light']['L_012'].GetEntries()
        print '\th sum loose:', h_pt['heavy']['L_012'].GetEntries() + h_pt['light']['L_012'].GetEntries()

        h_pt['all']['L_012'].Add(h_pt['light']['L_012'])  
        h_pt['all']['L_012'].Add(h_pt['heavy']['L_012'])  
        print '\th entries loose:', h_pt['all']['L_012'].GetEntries()


        ### EFFICIENCIES
        h_fr_pt = OrderedDict()
        for flvr in flavors:
            h_fr_pt[flvr] = rt.TEfficiency(h_pt[flvr]['T_012'], h_pt[flvr]['L_012'])
            h_fr_pt[flvr].SetTitle('%s; p_{T} [GeV]; tight-to-loose ratio'%flvr)
            h_fr_pt[flvr].SetFillColor(rt.kWhite)

        h_fr_pt['all']  .SetMarkerColor(rt.kBlack)
        h_fr_pt['light'].SetMarkerColor(rt.kBlue)
        h_fr_pt['heavy'].SetMarkerColor(rt.kBlack+1)

        ### PLOTTING
        if sfr:

            c_fr_pt = rt.TCanvas('ptCone_1f', 'ptCone_1f')
            framer.Draw()
            framer.GetYaxis().SetTitle('tight-to-loose ratio (SFR)')
            framer.GetXaxis().SetTitle('p_{T}^{cone} [GeV]')
            leg = rt.TLegend(0.57, 0.78, 0.80, 0.9)
            for flvr in flavors:
                h_fr_pt[flvr].Draw('same')
                leg.AddEntry(h_fr_pt[flvr], h_fr_pt[flvr].GetTitle())
            leg.Draw()
            pf.showlogoprelimsim('CMS')
            pf.showlumi(ch+ita)
            save(knvs=c_fr_pt, sample='TT_DY_WJ', ch=ch+ita, DIR=plotDir)
 
        if dfr:

            c_pt_2f = rt.TCanvas('ptCone_2f', 'ptCone_2f')
            framer.Draw()
            framer.GetYaxis().SetTitle('tight-to-loose ratio (DFR)')
            framer.GetXaxis().SetTitle('p_{T}^{cone} [GeV]')
            leg = rt.TLegend(0.57, 0.78, 0.80, 0.9)
            for flvr in flavors:
                h_fr_pt[flvr].Draw('same')
                leg.AddEntry(h_fr_pt[flvr], h_fr_pt[flvr].GetTitle())
            leg.Draw()
            pf.showlogoprelimsim('CMS')
            pf.showlumi(ch+ita)
            save(knvs=c_pt_2f, sample='TT_DY_WJ', ch=ch+ita, DIR=plotDir)

        i += 1
        print '\n\t %s done'%ita

    print '\n\t %s %s done'%(mode, ch)
    sys.stderr = sys.__stderr__
    sys.stdout = sys.__stdout__
###########################################################################################################################################################################################

###########################################################################################################################################################################################
def closureTest(ch='mmm', mode='sfr', isData=True, label=True, output=False):
    
    sfr = False; dfr = False; print '\n\tmode: %s, \tch: %s' %(mode, ch)
    if mode == 'sfr': sfr = True
    if mode == 'dfr': dfr = True

    plotDir = makeFolder('closureTest_%s'%ch)
    print '\n\tplotDir:', plotDir
    sys.stdout = Logger(plotDir + 'closureTest_%s' %ch)

    ### PREPARE CUTS AND FILES
    SFR, DFR, dirs = selectCuts(ch)

    SFR_021_L, SFR_012_L, SFR_021_LNT, SFR_012_LNT, SFR_021_T, SFR_012_T = SFR 
    DFR_L, DFR_T, DFR_LNT = DFR
    DYBB_dir, DY10_dir, DY50_dir, DY50_ext_dir, TT_dir, W_dir, W_ext_dir = dirs   

    dRdefList, sHdefList = selectDefs(ch)

    l0_is_fake, no_fakes, one_fake_xor, two_fakes, twoFakes_sameJet = dRdefList

    ### APPLICATION REGION
    appReg = 'hnl_w_vis_m < 80'
    appReg = '1 == 1' # RIC: FIRST DO VALIDITY TEST OF THE METHOD (26_03)
#    appReg = 'hnl_w_vis_m > 100' # RIC: Make me happy (27_03)
    flavors = ['all', 'heavy', 'light']

#        cuts_FR = 'hnl_dr_12 > 0.4 && abs(91.19 - hnl_m_01) > 10 && abs(91.19 - hnl_m_02) > 10 && ' + l_eta[eta]
    cuts_FR = appReg + ' && hnl_dr_12 > 0.3' 
    cuts_FR = appReg # 27_3 FOR CLOSURE TEST LEAVE DR_12 < 0.3 TO SEE WHAT HAPPENS

    if sfr:

        #### GENERAL 
        ptconel1 = PTCONEL1
        ptconel2 = PTCONEL2
        print '\n\tdrawing single fakes ...'
        mode021 = False; mode012 = False

        #### CHANNEL SPECIFIC
        if ch == 'mem':
            mode021 = True
            cuts_FR_021 = cuts_FR + ' && ' + SFR_MEM_021_L
            lnt_021     = SFR_MEM_021_LNT
            tight_021   = SFR_MEM_021_T

        if ch == 'eem':
            mode012 = True
            cuts_FR_012 = cuts_FR + ' && ' + SFR_EEM_012_L
            tight_021 = SFR_EEM_021_T
            if ID == 'M':
                L2ID = ' && l2_Medium == 1'

        if ch == 'mmm':
            cuts_FR_012 = cuts_FR + ' && ' + SFR_MMM_012_L
            cuts_FR_021 = cuts_FR + ' && ' + SFR_MMM_021_L
            tight_021 = SFR_MMM_021_T
            tight_012 = SFR_MMM_021_T
            mode012 = True
            mode021 = True

    if dfr: ## FOR DFR NO L1 < -- > L2 IS NEEDED => DRAW EVERYTHING WITH MODE021

        #### GENERAL 
        ptconel1 = PTCONE
        print '\n\tdrawing double fakes ...'
        mode021 = False; mode012 = False

        #### CHANNEL SPECIFIC
        if ch == 'mem':
            mode021 = True
            cuts_FR += ' && abs(l1_gen_match_pdgid) != 22'
            cuts_FR_021 = cuts_FR + ' && ' + DFR_MEM_L
            tight_021 = DFR_MEM_T

    ### PREPARE TREES
    t = None
    t = rt.TChain('tree')
#    t.Add(DYBB_dir + suffix)
#    t.Add(DY10_dir + suffix)
#    t.Add(DY50_dir + suffix)
#    t.Add(DY50_ext_dir + suffix)
#    t.Add(TT_dir + suffix)
##    t.Add(W_dir + suffix)
#    t.Add(W_ext_dir + suffix)
#    fin = rt.TFile(skim_mem); t = fin.Get('tree')
#    fin = rt.TFile(data_B_mmm); t = fin.Get('tree')
    t.Add(skim_mem); t.Add(data_B_mem)
    df = rdf(t)
    print'\n\tchain made.'

    # TODO SCALE MC
    # data B lumi = 4 792 /pb

    ### PREPARE DATAFRAMES
    if mode021 == True:

        cuts_l_021 = cuts_FR_021
        f0_021 = df.Filter(cuts_l_021)
        print '\n\tloose df 021 defined.'

        dfL_021   = f0_021.Define('ptcone021', ptconel1)

        if isData == True: 
            dfL0_021  = dfL_021.Filter(lnt_021 + ' && run > 1')
        if isData == False:
            dfL0_021  = dfL_021.Filter(lnt_021)
        print '\n\tlnt df 021 defined.'

        dfLNT_021 = dfL0_021.Define('fover1minusf021', selectBins(ch=ch,lep=1,isData=isData))
        print '\n\tweight f/(1-f)  021 defined. (without lumi/data normalization)'

        print '\n\tlnt df 021 events:', dfL0_021.Count().GetValue()

        dfT_021     = dfL_021.Filter(tight_021)
        if isData == True: 
            dfTdata_021      = dfT_021.Filter('run > 1')
        if label == True:
            dfTDYbb_021      = dfT_021.Filter('label == 0')# && abs(l1_gen_match_pdgid) != 22 && l1_gen_match_isPromptFinalState == 0')
            dfTDY50_021      = dfT_021.Filter('label == 1')# && abs(l1_gen_match_pdgid) != 22 && l1_gen_match_isPromptFinalState != 1')
            dfTTT_021        = dfT_021.Filter('label == 2')# && abs(l1_gen_match_pdgid) != 22 && l1_gen_match_isPromptFinalState == 0')
            dfTExtConv_021   = dfT_021.Filter('label == 1 && abs(l1_gen_match_pdgid) == 22') 
            dfTIntConv_021   = dfT_021.Filter('label == 1 && abs(l1_gen_match_pdgid) != 22 && l1_gen_match_isPromptFinalState == 1') 
        print '\n\ttight df 021 defined.'

        print '\n\ttight df 021 events:', dfT_021.Count().GetValue()

    if mode012 == True:

        print '\n\t l0l1: %s\n'       %(l0l1)
        print '\n\t l2_loose: %s\n'   %(l2_loose)
        print '\n\t l2_lnt: %s\n'     %(l2_lnt)
        print '\n\t l2_tight: %s\n'   %(l2_tight)

        f0_012 = df.Filter(cuts_FR + ' && ' + l0l1 + ' && ' + l2_loose)
        print '\n\tloose df 012 defined.'

        dfL_012   = f0_012.Define('ptcone012', ptconlel2)

        if isData == True: 
            dfL0_012  = dfL_012.Filter(lnt_012 + ' && run > 1')
        if isData == False:
            dfL0_012  = dfL_012.Filter(lnt_012)
        print '\n\tlnt df 012 defined.'

        dfLNT_012 = dfL0_012.Define('fover1minusf012', selectBins(ch=ch,lep=1,isData=isData))
        print '\n\tweight f/(1-f)  012 defined. (without lumi/data normalization)'

        print '\n\tlnt df 012 events:', dfL0_012.Count().GetValue()

        dfT_012   = dfL_012.Filter(tight_012)
        if isData == True: 
            dfTdata_012      = dfT_012.Filter('run > 1')
        if label == True:
            dfTDYbb_012      = dfT_012.Filter('label == 0')# && abs(l1_gen_match_pdgid) != 22 && l1_gen_match_isPromptFinalState == 0')
            dfTDY50_012      = dfT_012.Filter('label == 1')# && abs(l2_gen_match_pdgid) != 22 && l2_gen_match_isPromptFinalState != 1')
            dfTTT_012        = dfT_012.Filter('label == 2')# && abs(l1_gen_match_pdgid) != 22 && l1_gen_match_isPromptFinalState == 0')
            dfTExtConv_012   = dfT_012.Filter('label == 1 && abs(l2_gen_match_pdgid) == 22') 
            dfTIntConv_012   = dfT_012.Filter('label == 1 && abs(l2_gen_match_pdgid) != 22 && l2_gen_match_isPromptFinalState == 1') 
        print '\n\ttight df 012 defined.'

        print '\n\ttight df 012 events:', dfT_012.Count().GetValue()

    print '\n\t cuts: %s'                    %cuts_FR
    if mode012 ==True:
        print '\n\t loose 012: %s\n'         %(cuts_FR_012)
        print '\n\t tight 012: %s\n'         %(tight_012)
        print '\ttotal loose 012: %s\n'      %f0_012.Count().GetValue()
    if mode021 ==True:
        print '\n\t loose 021: %s\n'         %(cuts_FR_021)
        print '\n\t tight 021: %s\n'         %(tight_021)
        print '\ttotal loose 021: %s\n'      %f0_021.Count().GetValue()
    
    ## SAVE FR OUTPUT BRANCH IN TREE
    if output == True:
        branchList_021 = rt.vector('string')(); branchList_012 = rt.vector('string')()
        for br in ['event', 'lumi']:
            branchList_021.push_back(br)
            branchList_012.push_back(br)
        if label == True: branchList_021.push_back('label'); branchList_012.push_back('label')
        time_string = ch + '_' + mode + '_' + date + '_' + hour + '_' + minit
        if mode021 == True:
            branchList_021.push_back('fover1minusf021')
            set_trace()
            dfLNT_021.Snapshot('tree', plotDir + 'fr_021_%s.root'%time_string, branchList_021)
        if mode012 == True:
            branchList_012.push_back('fover1minusf012')
            dfLNT_012.Snapshot('tree', plotDir + 'fr_012_%s.root'%time_string, branchList_012)


    VARS = {'dr_12':     [len(b_dR)-1,     b_dR,     'hnl_dr_12'      , ';#DeltaR(l_{1},  l_{2}); Counts'], 
            '2disp':     [len(b_2d)-1,     b_2d,     'hnl_2d_disp'    , ';2d_disp [cm]; Counts'], 
            '2disp_sig': [len(b_2d_sig)-1, b_2d_sig, 'hnl_2d_disp_sig', ';2d_disp_sig ; Counts'], 
            'm_dimu':    [len(b_m)-1,      b_m,      'hnl_m_12'       , ';m(l_{1},  l_{2}) [GeV]; Counts'], 
            'BGM_dimu':  [len(b_M)-1,      b_M,      'hnl_m_12'       , ';m(l_{1},  l_{2}) [GeV]; Counts'], 
            'BGM_01':    [len(b_M)-1,      b_M,      'hnl_m_01'       , ';m(l_{0},  l_{1}) [GeV]; Counts'], 
            'BGM_02':    [len(b_M)-1,      b_M,      'hnl_m_02'       , ';m(l_{0},  l_{2}) [GeV]; Counts'], 
            'm_triL':    [len(b_M)-1,      b_M,      'hnl_w_vis_m'    , ';m(l_{0},  l_{1},  l_{2}) [GeV]; Counts'],
            'pt' : None}

    _H_OBS_012   = OrderedDict()
    _H_WHD_012 = OrderedDict()
    H_OBS_012    = OrderedDict()
    H_WHD_012  = OrderedDict()

    _H_OBS_021   = OrderedDict()
    _H_WHD_021 = OrderedDict()
    H_OBS_021    = OrderedDict()
    H_WHD_021  = OrderedDict()

    for v in VARS.keys():
        _H_OBS_021[v] = OrderedDict()
        H_OBS_021[v]  = OrderedDict()
        _H_WHD_021[v] = OrderedDict()
        H_WHD_021[v]  = OrderedDict()

        _H_OBS_012[v] = OrderedDict()
        H_OBS_012[v]  = OrderedDict()
        _H_WHD_012[v] = OrderedDict()
        H_WHD_012[v]  = OrderedDict()

    if mode021 == True:

        VARS ['pt'] = [len(b_pt)-1,     b_pt,     'ptcone021'      , ';p_{T}^{cone} [GeV]; Counts']

        dfT_021_L = OrderedDict()
        if isData == True:
            dfT_021_L ['data'] = dfTdata_021
        if label == True:
            dfT_021_L ['DY50'] = dfTDY50_021;  dfT_021_L['IntConv'] = dfTIntConv_021; dfT_021_L['ExtConv'] = dfTExtConv_021#, 'DYbb' : dfTDYbb_021,   'TT' : dfTTT_021    }
        KEYS = dfT_021_L.keys()

        for v in VARS.keys():

            _H_WHD_021[v]   = dfLNT_021.Histo1D(('whd_021_%s'%v,'whd_021_%s'%v, VARS[v][0], VARS[v][1]), VARS[v][2], 'fover1minusf021')
            if label == False and isData == False:
                _H_OBS_021[v] = dfT_021.Histo1D(('obs_021_%s'%v,'obs_021_%s'%v, VARS[v][0], VARS[v][1]), VARS[v][2])

            if label == True or isData == True:
                for DF in dfT_021_L.keys():
                    _H_OBS_021[v][DF] = dfT_021_L[DF].Histo1D(('obs_021_%s_%s'%(v,DF),'obs_021_%s_%s'%(v,DF), VARS[v][0], VARS[v][1]), VARS[v][2])

    if mode012 == True:

        VARS ['pt'] = [len(b_pt)-1,     b_pt,     'ptcone012'      , ';p_{T}^{cone} [GeV]; Counts']

        dfT_012_L = OrderedDict()
        if isData == True:
            dfT_012_L ['data'] = dfTdata_012
        if label == True:
            dfT_012_L ['DY50'] = dfTDY50_012;  dfT_012_L['IntConv'] = dfTIntConv_012; dfT_012_L['ExtConv'] = dfTExtConv_012#, 'DYbb' : dfTDYbb_012,   'TT' : dfTTT_012    }
        KEYS = dfT_012_L.keys()

        for v in VARS.keys():

            _H_WHD_012[v]   = dfLNT_012.Histo1D(('whd_012_%s'%v,'whd_012_%s'%v, VARS[v][0], VARS[v][1]), VARS[v][2], 'fover1minusf012')
            if label == False and isData == False:
                _H_OBS_012[v] = dfT_012.Histo1D(('obs_012_%s'%v,'obs_012_%s'%v, VARS[v][0], VARS[v][1]), VARS[v][2])

            if label == True or isData == True:
                for DF in dfT_021_L.keys():
                    _H_OBS_012[v][DF] = dfT_012_L[DF].Histo1D(('obs_012_%s_%s'%(v,DF),'obs_012_%s_%s'%(v,DF), VARS[v][0], VARS[v][1]), VARS[v][2])

    for v in VARS.keys():

        H_WHD_012[v] = rt.TH1F('whd_012_%s_'%(v),'whd_012_%s'%(v), VARS[v][0], VARS[v][1])
        H_WHD_021[v] = rt.TH1F('whd_021_%s_'%(v),'whd_021_%s'%(v), VARS[v][0], VARS[v][1])
        if label == False and isData == False:
            H_OBS_012[v] = rt.TH1F('obs_012_%s'%(v),'obs_012_%s'%(v), VARS[v][0], VARS[v][1])           
            H_OBS_021[v] = rt.TH1F('obs_021_%s'%(v),'obs_021_%s'%(v), VARS[v][0], VARS[v][1])           

        if label == True or isData == True:
            for DF in KEYS:
                H_OBS_012[v][DF] = rt.TH1F('obs_012_%s_%s'%(v,DF),'obs_012_%s_%s'%(v,DF), VARS[v][0], VARS[v][1])           
                H_OBS_021[v][DF] = rt.TH1F('obs_021_%s_%s'%(v,DF),'obs_021_%s_%s'%(v,DF), VARS[v][0], VARS[v][1])           

        if mode021 == True:
            VARS ['pt'] = [len(b_pt)-1,     b_pt,     'ptcone021'      , ';p_{T}^{cone} [GeV]; Counts']
            H_WHD_021[v] = _H_WHD_021[v].GetPtr()
            if label == False and isData == False:
                H_OBS_021[v] = _H_OBS_021[v].GetPtr()
            if label == True or isData == True:
                for DF in dfT_021_L.keys():
                    _H_OBS_021[v][DF] = dfT_021_L[DF].Histo1D(('obs_021_%s_%s'%(v,DF),'obs_021_%s_%s'%(v,DF), VARS[v][0], VARS[v][1]), VARS[v][2])
                    print '\n\tDrawing:', v, DF
                    H_OBS_021[v][DF]  = _H_OBS_021[v][DF].GetPtr()
        
        if mode012 == True:
            VARS ['pt'] = [len(b_pt)-1,     b_pt,     'ptcone012'      , ';p_{T}^{cone} [GeV]; Counts']
            H_WHD_012[v] = _H_WHD_012[v].GetPtr()
            if label == False and isData == False:
                H_OBS_012[v] = _H_OBS_012[v].GetPtr()
            if label == True or isData == True:
                for DF in dfT_012_L.keys():
                    _H_OBS_012[v][DF] = dfT_012_L[DF].Histo1D(('obs_012_%s_%s'%(v,DF),'obs_012_%s_%s'%(v,DF), VARS[v][0], VARS[v][1]), VARS[v][2])
                    print '\n\tDrawing:', v, DF
                    H_OBS_012[v][DF]  = _H_OBS_012[v][DF].GetPtr()

        # STACK COLORS            
        col = OrderedDict() 
        col['data']    = rt.kBlack
        col['TT']      = rt.kBlue+1
        col['DYbb']    = rt.kRed+1
        col['DY50']    = rt.kYellow+1
        col['IntConv'] = rt.kRed+1
        col['ExtConv'] = rt.kCyan+1
        col['whd']     = rt.kGreen+1

        H_WHD_012[v].Add(H_WHD_021[v]); H_WHD_012[v].SetFillColor(col['whd']); H_WHD_012[v].SetLineColor(rt.kBlack); H_WHD_012[v].SetMarkerSize(0); H_WHD_012[v].SetMarkerColor(rt.kBlack)
        whd = H_WHD_012[v]

        if label == True:
            obs = rt.THStack('obs_%s'%v,'obs_%s'%v)
            whd = rt.THStack('whd_%s'%v,'whd_%s'%v)
            
            for DF in KEYS:
                H_OBS_012[v][DF].Add(H_OBS_021[v][DF])
                if not DF == 'DY50':
                    H_OBS_012[v][DF].SetFillColor(col[DF])
                    H_OBS_012[v][DF].SetLineColor(rt.kBlack)
                    H_OBS_012[v][DF].SetMarkerSize(0)
                    H_OBS_012[v][DF].SetMarkerColor(rt.kBlack)
#                    obs.Add(H_OBS_012[v][DF])

            # WHD = SFR + INT & EXT CONVs // OBS = IS ONLY DY FOR NOW (27_03)
            if isData == False:
                obs = H_OBS_012[v]['DY50'] 
            if isData == True:
                obs = H_OBS_012[v]['data'] 

            whd.Add(H_WHD_012[v])
            whd.Add(H_OBS_012[v]['IntConv'])
            whd.Add(H_OBS_012[v]['ExtConv'])

        if label == False:
            H_OBS_012[v].Add(H_OBS_021[v])
            obs = H_OBS_012[v]

        if v == 'pt':
            if label == False: n_obs = obs.GetEntries(); n_whd = whd.GetEntries()
            if label == True: 
                n_obs = 0
                for DF in KEYS: 
                    print '\n\t', H_OBS_012[v][DF].GetEntries() 
                    n_obs += H_OBS_012[v][DF].GetEntries()
                    n_whd = H_WHD_012[v].GetEntries()
            print '\n\tyields. weighed: %0.2f, observed: %0.2f' %(n_whd, n_obs)

        c = rt.TCanvas(v, v); c.cd()
#            whd.SetLineColor(rt.kGreen+2); whd.SetLineWidth(2); whd.SetMarkerStyle(0)
        obs.SetTitle(VARS[v][3])
        obs.SetMarkerColor(rt.kMagenta+2)
        whd.Draw('histE')
        whd.SetTitle(VARS[v][3])
        obs.Draw('same')
        leg = rt.TLegend(0.57, 0.78, 0.80, 0.9)
        if label == False: 
            leg.AddEntry(obs, 'observed')
        if label == True: 
            for DF in KEYS:
                if not DF == 'DY50' and not DF == 'data': leg.AddEntry(H_OBS_012[v][DF], DF)
                if isData == False:
                    if DF == 'DY50': leg.AddEntry(H_OBS_012[v][DF], 'observed')
                if isData == True:
                    if DF == 'data': leg.AddEntry(H_OBS_012[v][DF], 'observed')
        leg.AddEntry(H_WHD_012[v], 'expected SFR')
        leg.Draw()
        pf.showlogoprelimsim('CMS')
        pf.showlumi('SFR_'+ch)
        save(knvs=c, sample='DDE', ch=ch, DIR=plotDir)

    sys.stderr = sys.__stderr__
    sys.stdout = sys.__stdout__
######################################################################################

######################################################################################
## FIXME TODO PLAN IS TO USE THIS INSTEAD OF REPEATING THE SAME IN EVERY FUNCTION --> PREPARE AND RETURN DFs
## TODO make a class out of this
class FakeRate(object):

    def prepareDF(self, ch='mem'):

        ### PREPARE CUTS AND FILES
        SFR, DFR, dirs = selectCuts(ch)

        SFR_021_L, SFR_012_L, SFR_021_LNT, SFR_012_LNT, SFR_021_T, SFR_012_T = SFR 
        DFR_L, DFR_T, DFR_LNT = DFR
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

            cuts_FR = 'hnl_dr_12 > 0.3'

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

                dfL_021 = f0_021.Define('ptcone021', PTCONEL1)
                print '\n\tptcone 021: %s\n' %PTCONEL1
                print '\tptcone 021 defined.'

                dfL_021_light = dfL_021.Filter('abs(l1_jet_flavour_parton) != 4 && abs(l1_jet_flavour_parton) != 5')
                dfL_021_heavy = dfL_021.Filter('abs(l1_jet_flavour_parton) == 4 || abs(l1_jet_flavour_parton) == 5')
                print '\tflavours 021 defined.'

                dfL_021_light_eta0 = dfL_021_light.Filter(l_eta[l_eta.keys()[0]])
                dfL_021_heavy_eta0 = dfL_021_heavy.Filter(l_eta[l_eta.keys()[0]])

                dfL_021_light_eta1 = dfL_021_light.Filter(l_eta[l_eta.keys()[1]])
                dfL_021_heavy_eta1 = dfL_021_heavy.Filter(l_eta[l_eta.keys()[1]])

                dfL_021_light_eta2 = dfL_021_light.Filter(l_eta[l_eta.keys()[2]])
                dfL_021_heavy_eta2 = dfL_021_heavy.Filter(l_eta[l_eta.keys()[2]])
                print '\tloose 021 eta defined.'

                dfT_021_light_eta0 = dfL_021_light_eta0.Filter(l1_tight)
                dfT_021_heavy_eta0 = dfL_021_heavy_eta0.Filter(l1_tight)

                dfT_021_light_eta1 = dfL_021_light_eta1.Filter(l1_tight)
                dfT_021_heavy_eta1 = dfL_021_heavy_eta1.Filter(l1_tight)

                dfT_021_light_eta2 = dfL_021_light_eta2.Filter(l1_tight)
                dfT_021_heavy_eta2 = dfL_021_heavy_eta2.Filter(l1_tight)
                print '\ttight 021 defined.'

                _dfL_021_light = [dfL_021_light_eta0, dfL_021_light_eta1, dfL_021_light_eta2]
                _dfL_021_heavy = [dfL_021_heavy_eta0, dfL_021_heavy_eta1, dfL_021_heavy_eta2]

                _dfT_021_light = [dfT_021_light_eta0, dfT_021_light_eta1, dfT_021_light_eta2]
                _dfT_021_heavy = [dfT_021_heavy_eta0, dfT_021_heavy_eta1, dfT_021_heavy_eta2]

            if mode012 == True:
                cuts_l_012 = cuts_FR + ' && l2_jet_flavour_parton != -99 && ' + l0l1 + ' && ' + l2_loose 

                f0_012 = df.Filter(cuts_l_012)
                print '\n\tloose 012 defined.'

                dfL_012 = f0_012.Define('ptcone012', PTCONEL2)
                print '\n\tptcone 012: %s\n' %PTCONEL2
                print '\tptcone 012 defined.'

                dfL_012_light = dfL_012.Filter('abs(l2_jet_flavour_parton) != 4 && abs(l2_jet_flavour_parton) != 5')
                dfL_012_heavy = dfL_012.Filter('abs(l2_jet_flavour_parton) == 4 || abs(l2_jet_flavour_parton) == 5')
                print '\tflavours 012 defined.'

                dfL_012_light_eta0 = dfL_012_light.Filter(re.sub('l1_eta','l2_eta',l_eta[l_eta.keys()[0]]))
                dfL_012_heavy_eta0 = dfL_012_heavy.Filter(re.sub('l1_eta','l2_eta',l_eta[l_eta.keys()[0]]))

                dfL_012_light_eta1 = dfL_012_light.Filter(re.sub('l1_eta','l2_eta',l_eta[l_eta.keys()[1]]))
                dfL_012_heavy_eta1 = dfL_012_heavy.Filter(re.sub('l1_eta','l2_eta',l_eta[l_eta.keys()[1]]))

                dfL_012_light_eta2 = dfL_012_light.Filter(re.sub('l1_eta','l2_eta',l_eta[l_eta.keys()[2]]))
                dfL_012_heavy_eta2 = dfL_012_heavy.Filter(re.sub('l1_eta','l2_eta',l_eta[l_eta.keys()[2]]))
                print '\tloose 012 eta defined.'

                dfT_012_light_eta0 = dfL_012_light_eta0.Filter(l2_tight)
                dfT_012_heavy_eta0 = dfL_012_heavy_eta0.Filter(l2_tight)

                dfT_012_light_eta1 = dfL_012_light_eta1.Filter(l2_tight)
                dfT_012_heavy_eta1 = dfL_012_heavy_eta1.Filter(l2_tight)

                dfT_012_light_eta2 = dfL_012_light_eta2.Filter(l2_tight)
                dfT_012_heavy_eta2 = dfL_012_heavy_eta2.Filter(l2_tight)
                print '\ttight 012 defined.'

                _dfT_012_light = [dfT_012_light_eta0, dfT_012_light_eta1, dfT_012_light_eta2]
                _dfT_012_heavy = [dfT_012_heavy_eta0, dfT_012_heavy_eta1, dfT_012_heavy_eta2]

                _dfL_012_light = [dfL_012_light_eta0, dfL_012_light_eta1, dfL_012_light_eta2]
                _dfL_012_heavy = [dfL_012_heavy_eta0, dfL_012_heavy_eta1, dfL_012_heavy_eta2]
######################################################################################

######################################################################################
def checkIsoPDF(ch='mmm',ID='No',eta_split=True,mode='sfr',dR='04',fullSplit=False):

    sfr = False; dfr = False; print '\n\tmode: %s, \tch: %s' %(mode, ch)
    if mode == 'sfr': sfr = True
    if mode == 'dfr': dfr = True

    plotDir = makeFolder('checkIsoPDF_%s' %ch)
    print '\n\tplotDir:', plotDir
    sys.stdout = Logger(plotDir + 'checkIsoPDF_%s' %ch)

    l_eta = None; l_eta = OrderedDict()
    l_eta['_eta_all'] = '1 == 1'

    if eta_split == True: 

        if ch == 'mem':
            l_eta = None; l_eta = OrderedDict()
            l_eta ['_eta_00t08'] = 'abs(l1_eta) < 0.8'; l_eta ['_eta_08t15'] = 'abs(l1_eta) > 0.8 && abs(l1_eta) < 1.479'; l_eta ['_eta_15t25'] = 'abs(l1_eta) > 1.479 && abs(l1_eta) < 2.5'


        if ch == 'mmm':
            l_eta = None; l_eta = OrderedDict()
            l_eta ['_eta_00t12'] = 'abs(l1_eta) < 1.2'; l_eta ['_eta_12t21'] = 'abs(l1_eta) > 1.2 && abs(l1_eta) < 2.1'; l_eta ['_eta_21t24'] = 'abs(l1_eta) > 2.1 && abs(l1_eta) < 2.4'

        if dfr: 
            l_eta = None; l_eta = OrderedDict()
            l_eta ['_eta_00t12'] = 'abs(l1_eta) < 1.2'; l_eta ['_eta_12t21'] = 'abs(l1_eta) > 1.2 && abs(l1_eta) < 2.1'; l_eta ['_eta_21t24'] = 'abs(l1_eta) > 2.1 && abs(l1_eta) < 2.4'
            for i in l_eta.keys(): l_eta[i] = re.sub('l1', 'hnl_hn_vis', l_eta[i])

    print '\n\teta:', l_eta

    ### PREPARE CUTS AND FILES
    SFR, DFR, dirs = selectCuts(ch)

    SFR_021_L, SFR_012_L, SFR_021_LNT, SFR_012_LNT, SFR_021_T, SFR_012_T = SFR 
    DFR_L, DFR_T, DFR_LNT = DFR
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
        ptconel1 = PTCONEL1
        ptconel2 = PTCONEL2
        print '\n\tdrawing single fakes ...'
        mode021 = False; mode012 = False

        cuts_FR = 'hnl_dr_12 > 0.3'
        L1ID = ''
        L2ID = ''

        #### CHANNEL SPECIFIC
        if ch == 'mem':
            mode021 = True
            cuts_FR += ' && abs(l1_gen_match_pdgid) != 22'
            cuts_FR_021 = cuts_FR + ' && ' + SFR_MEM_021_L
            if ID == 'M':
                L1ID = ' && l1_MediumNoIso == 1'
            if ID == 'L':
                L1ID = ' && l1_LooseNoIso == 1'

        if ch == 'eem':
           mode012 = True
           cuts_FR_012 = cuts_FR + ' && ' + SFR_EEM_012_L
           if ID == 'M':
                L2ID = ' && l2_Medium == 1'

        if ch == 'mmm':
           cuts_FR_012 = cuts_FR + ' && ' + SFR_MMM_012_L
           cuts_FR_021 = cuts_FR + ' && ' + SFR_MMM_021_L
           mode012 = True
           mode021 = True
           if ID == 'M':
                L1ID = ' && l1_Medium == 1'
                L2ID = ' && l2_Medium == 1'

    if dfr: ## FOR DFR NO L1 < -- > L2 IS NEEDED => DRAW EVERYTHING WITH MODE021

        #### GENERAL 
        print '\n\tdrawing double fakes ...'
        mode021 = False; mode012 = False
        ptconel1 = PTCONE

        cuts_FR = 'hnl_dr_12 < 0.3'
        L1ID = ''
        #### CHANNEL SPECIFIC
        if ch == 'mem':
            mode021 = True
            cuts_FR += ' && abs(l1_gen_match_pdgid) != 22'
            cuts_FR_021 = cuts_FR + ' && ' + DFR_MEM_L
            if ID == 'M':
                L1ID = ' && l1_MediumNoIso == 1 && l2_Medium == 1'
            if ID == 'L':
                L1ID = ' && l1_LooseNoIso == 1 && l2_id_l == 1'


    ### PREPARE DATAFRAMES
    if mode021 == True:
        cuts_l_021 = cuts_FR_021 + ' && l1_jet_flavour_parton != -99' + L1ID 
        cuts_l_021 = re.sub('abs\(l._reliso_rho_0.\) < ... \&\& ', '', cuts_l_021)
        print cuts_l_021

        f0_021 = df.Filter(cuts_l_021)
        print '\n\tloose 021 defined.'

        dfL_021 = f0_021.Define('ptcone021', ptconel1)
        print '\n\tptcone 021: %s\n' %ptconel1
        print '\tptcone 021 defined.'

        dfL_021_light = dfL_021.Filter('abs(l1_jet_flavour_parton) != 4 && abs(l1_jet_flavour_parton) != 5')
        dfL_021_heavy = dfL_021.Filter('abs(l1_jet_flavour_parton) == 4 || abs(l1_jet_flavour_parton) == 5')
        print '\tflavours 021 defined.'

        dfL_021_light_eta0 = dfL_021_light.Filter(l_eta[l_eta.keys()[0]])
        dfL_021_heavy_eta0 = dfL_021_heavy.Filter(l_eta[l_eta.keys()[0]])

        dfL_021_light_eta1 = dfL_021_light.Filter(l_eta[l_eta.keys()[1]])
        dfL_021_heavy_eta1 = dfL_021_heavy.Filter(l_eta[l_eta.keys()[1]])

        dfL_021_light_eta2 = dfL_021_light.Filter(l_eta[l_eta.keys()[2]])
        dfL_021_heavy_eta2 = dfL_021_heavy.Filter(l_eta[l_eta.keys()[2]])
        print '\tloose 021 eta defined.'

        _dfL_021_light = [dfL_021_light_eta0, dfL_021_light_eta1, dfL_021_light_eta2]
        _dfL_021_heavy = [dfL_021_heavy_eta0, dfL_021_heavy_eta1, dfL_021_heavy_eta2]


    if mode012 == True:
        cuts_l_012 = cuts_FR_012 + ' && l2_jet_flavour_parton != -99' + L2ID
        cuts_l_012 = re.sub('abs\(l._reliso_rho_0.\) < ... \&\& ', '', cuts_l_012)
        print cuts_l_012

        f0_012 = df.Filter(cuts_l_012)
        print '\n\tloose 012 defined.'

        dfL_012 = f0_012.Define('ptcone012', ptconel2)
        print '\n\tptcone 012: %s\n' %ptconel2
        print '\tptcone 012 defined.'

        dfL_012_light = dfL_012.Filter('abs(l2_jet_flavour_parton) != 4 && abs(l2_jet_flavour_parton) != 5')
        dfL_012_heavy = dfL_012.Filter('abs(l2_jet_flavour_parton) == 4 || abs(l2_jet_flavour_parton) == 5')
        print '\tflavours 012 defined.'

        dfL_012_light_eta0 = dfL_012_light.Filter(re.sub('l1_eta','l2_eta',l_eta[l_eta.keys()[0]]))
        dfL_012_heavy_eta0 = dfL_012_heavy.Filter(re.sub('l1_eta','l2_eta',l_eta[l_eta.keys()[0]]))

        dfL_012_light_eta1 = dfL_012_light.Filter(re.sub('l1_eta','l2_eta',l_eta[l_eta.keys()[1]]))
        dfL_012_heavy_eta1 = dfL_012_heavy.Filter(re.sub('l1_eta','l2_eta',l_eta[l_eta.keys()[1]]))

        dfL_012_light_eta2 = dfL_012_light.Filter(re.sub('l1_eta','l2_eta',l_eta[l_eta.keys()[2]]))
        dfL_012_heavy_eta2 = dfL_012_heavy.Filter(re.sub('l1_eta','l2_eta',l_eta[l_eta.keys()[2]]))
        print '\tloose 012 eta defined.'

        if fullSplit == False:
            _dfL_012_light = [dfL_012_light_eta0, dfL_012_light_eta1, dfL_012_light_eta2]
            _dfL_012_heavy = [dfL_012_heavy_eta0, dfL_012_heavy_eta1, dfL_012_heavy_eta2]
    
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
            _h_light_021_eta0 = _dfL_021_light[0].Histo1D(('l1_'+var+'eta0_light','l1_'+var+'eta0_light',vars[var][0],vars[var][1],vars[var][2]),'l1_'+var)
            _h_heavy_021_eta0 = _dfL_021_heavy[0].Histo1D(('l1_'+var+'eta0_heavy','l1_'+var+'eta0_heavy',vars[var][0],vars[var][1],vars[var][2]),'l1_'+var)

            _h_light_021_eta1 = _dfL_021_light[1].Histo1D(('l1_'+var+'eta1_light','l1_'+var+'eta1_light',vars[var][0],vars[var][1],vars[var][2]),'l1_'+var)
            _h_heavy_021_eta1 = _dfL_021_heavy[1].Histo1D(('l1_'+var+'eta1_heavy','l1_'+var+'eta1_heavy',vars[var][0],vars[var][1],vars[var][2]),'l1_'+var)

            _h_light_021_eta2 = _dfL_021_light[2].Histo1D(('l1_'+var+'eta2_light','l1_'+var+'eta2_light',vars[var][0],vars[var][1],vars[var][2]),'l1_'+var)
            _h_heavy_021_eta2 = _dfL_021_heavy[2].Histo1D(('l1_'+var+'eta2_heavy','l1_'+var+'eta2_heavy',vars[var][0],vars[var][1],vars[var][2]),'l1_'+var)

            h_light_021_eta0 = _h_light_021_eta0.GetPtr()
            h_heavy_021_eta0 = _h_heavy_021_eta0.GetPtr()

            h_light_021_eta1 = _h_light_021_eta1.GetPtr()
            h_heavy_021_eta1 = _h_heavy_021_eta1.GetPtr()

            h_light_021_eta2 = _h_light_021_eta2.GetPtr()
            h_heavy_021_eta2 = _h_heavy_021_eta2.GetPtr()

        if mode012 == True:
            _h_light_012_eta0 = _dfL_012_light[0].Histo1D(('l2_'+var+'eta0_light','l2_'+var+'eta0_light',vars[var][0],vars[var][1],vars[var][2]),'l2_'+var)
            _h_heavy_012_eta0 = _dfL_012_heavy[0].Histo1D(('l2_'+var+'eta0_heavy','l2_'+var+'eta0_heavy',vars[var][0],vars[var][1],vars[var][2]),'l2_'+var)

            _h_light_012_eta1 = _dfL_012_light[1].Histo1D(('l2_'+var+'eta1_light','l2_'+var+'eta1_light',vars[var][0],vars[var][1],vars[var][2]),'l2_'+var)
            _h_heavy_012_eta1 = _dfL_012_heavy[1].Histo1D(('l2_'+var+'eta1_heavy','l2_'+var+'eta1_heavy',vars[var][0],vars[var][1],vars[var][2]),'l2_'+var)

            _h_light_012_eta2 = _dfL_012_light[2].Histo1D(('l2_'+var+'eta2_light','l2_'+var+'eta2_light',vars[var][0],vars[var][1],vars[var][2]),'l2_'+var)
            _h_heavy_012_eta2 = _dfL_012_heavy[2].Histo1D(('l2_'+var+'eta2_heavy','l2_'+var+'eta2_heavy',vars[var][0],vars[var][1],vars[var][2]),'l2_'+var)

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

            print '\n\tevents:', h_light.Integral(), h_heavy.Integral()
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

        DFR_T          =   DFR_EEE_T
        DFR_L          =   DFR_EEE_L
        DFR_LNT        =   DFR_EEE_LNT

        SFR_012_L       =  SFR_EEE_012_L  
        SFR_012_LNT     =  SFR_EEE_012_LNT
        SFR_012_T       =  SFR_EEE_012_T  
        SFR_021_L       =  SFR_EEE_021_L  
        SFR_021_LNT     =  SFR_EEE_021_LNT
        SFR_021_T       =  SFR_EEE_021_T  


    if channel == 'eem':
        DYBB_dir       =   DYBBDir_eem     
        DY10_dir       =   DY10Dir_eem      
        DY50_dir       =   DY50Dir_eem      
        DY50_ext_dir   =   DY50_extDir_eem 
        W_dir          =   W_dir_eem
        W_ext_dir      =   W_ext_dir_eem
        TT_dir         =   TT_dir_eem

        DFR_T          =   DFR_EMM_T
        DFR_L          =   DFR_EMM_L
        DFR_LNT        =   DFR_EMM_LNT

        SFR_012_L       =  SFR_EEM_012_L  
        SFR_012_LNT     =  SFR_EEM_012_LNT
        SFR_012_T       =  SFR_EEM_012_T  
        SFR_021_L       =  ''
        SFR_021_LNT     =  ''
        SFR_021_T       =  ''


    if channel == 'emm':
        DYBB_dir       =   DYBBDir_emm     
        DY10_dir       =   DY10Dir_emm      
        DY50_dir       =   DY50Dir_emm      
        DY50_ext_dir   =   DY50_extDir_emm 
        W_dir          =   W_dir_emm
        W_ext_dir      =   W_ext_dir_emm
        TT_dir         =   TT_dir_emm

        DFR_T          =   DFR_EMM_T
        DFR_L          =   DFR_EMM_L
        DFR_LNT        =   DFR_EMM_LNT

        SFR_012_L       =  SFR_EMM_012_L  
        SFR_012_LNT     =  SFR_EMM_012_LNT
        SFR_012_T       =  SFR_EMM_012_T  
        SFR_021_L       =  SFR_EMM_021_L  
        SFR_021_LNT     =  SFR_EMM_021_LNT
        SFR_021_T       =  SFR_EMM_021_T  


    if channel == 'mee':
        DYBB_dir       =   DYBBDir_mee     
        DY10_dir       =   DY10Dir_mee      
        DY50_dir       =   DY50Dir_mee      
        DY50_ext_dir   =   DY50_extDir_mee 
        W_dir          =   W_dir_mee
        W_ext_dir      =   W_ext_dir_mee
        TT_dir         =   TT_dir_mee

        DFR_T          =   DFR_MEE_T
        DFR_L          =   DFR_MEE_L
        DFR_LNT        =   DFR_MEE_LNT

        SFR_012_L       =  SFR_MEE_012_L  
        SFR_012_LNT     =  SFR_MEE_012_LNT
        SFR_012_T       =  SFR_MEE_012_T  
        SFR_021_L       =  SFR_MEE_021_L  
        SFR_021_LNT     =  SFR_MEE_021_LNT
        SFR_021_T       =  SFR_MEE_021_T  


    if channel == 'mem':
        DYBB_dir       =   DYBBDir_mem     
        DY10_dir       =   DY10Dir_mem      
        DY50_dir       =   DY50Dir_mem      
        DY50_ext_dir   =   DY50_extDir_mem 
        W_dir          =   W_dir_mem
        W_ext_dir      =   W_ext_dir_mem
        TT_dir         =   TT_dir_mem

        DFR_T          =   DFR_MEM_T
        DFR_L          =   DFR_MEM_L
        DFR_LNT        =   DFR_MEM_LNT

        SFR_012_L       =  ''
        SFR_012_LNT     =  ''
        SFR_012_T       =  ''
        SFR_021_L       =  SFR_MEM_021_L  
        SFR_021_LNT     =  SFR_MEM_021_LNT
        SFR_021_T       =  SFR_MEM_021_T  

    if channel == 'mmm':
        DYBB_dir       =   DYBBDir_mmm     
        DY10_dir       =   DY10Dir_mmm      
        DY50_dir       =   DY50Dir_mmm      
        DY50_ext_dir   =   DY50_extDir_mmm 
        W_dir          =   W_dir_mmm
        W_ext_dir      =   W_ext_dir_mmm
        TT_dir         =   TT_dir_mmm

        DFR_T          =   DFR_MMM_T
        DFR_L          =   DFR_MMM_L
        DFR_LNT        =   DFR_MMM_LNT

        SFR_012_L       =  SFR_MMM_012_L  
        SFR_012_LNT     =  SFR_MMM_012_LNT
        SFR_012_T       =  SFR_MMM_012_T  
        SFR_021_L       =  SFR_MMM_021_L  
        SFR_021_LNT     =  SFR_MMM_021_LNT
        SFR_021_T       =  SFR_MMM_021_T  

    SFR  = [SFR_021_L, SFR_012_L, SFR_021_LNT, SFR_012_LNT, SFR_021_T, SFR_012_T] 
    DFR  = [DFR_L, DFR_T, DFR_LNT] 
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
 
    plotDir = plotDir + name + '_' + date + '_' + hour + 'h_' + minit + 'm/'
    os.mkdir(plotDir)
    return plotDir


