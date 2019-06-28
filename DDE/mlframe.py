from __future__ import division
from ROOT import gROOT as gr
from ROOT import RDataFrame as RDF
import os, platform
import ROOT as rt
import numpy as np
import plotfactory as pf
from shutil import copyfile
from glob import glob
import pickle
import re, sys
from datetime import datetime
from pdb import set_trace
from copy import deepcopy
from os.path import normpath, basename, split
from collections import OrderedDict
from multiprocessing import Pool
from multiprocessing.dummy import Pool
from itertools import product

import root_pandas
import uproot as ur
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from itertools import product

from root_numpy import root2array

from keras.models import Sequential, Model, load_model
from keras.layers import Dense, Input
from keras.utils import plot_model

from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve, roc_auc_score

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
if platform.platform() in['Linux-2.6.32-754.3.5.el6.x86_64-x86_64-with-redhat-6.6-Carbon', 'Linux-3.10.0-862.14.4.el7.x86_64-x86_64-with-redhat-7.5-Maipo']:
   eos       = '/t3home/vstampf/eos/'
   eos_david = '/t3home/vstampf/eos-david/'

pf.setpfstyle()
#rt.TStyle.SetOptStat(0)
#BATCH MODE
gr.SetBatch(True)

#rt.ROOT.EnableImplicitMT(8)

pi = rt.TMath.Pi()
###########################################################################################################################################################################################
saveDir = eos+'ML_FR/from_R/'
skimDir = eos+'ntuples/skimmed_trees/'
plotDir = eos+'plots/DDE/'
suffix  = 'HNLTreeProducer/tree.root'
###########################################################################################################################################################################################
DYBBDir_mem     = eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_mem/DYBB/'
DY50Dir_mem     = eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_mem/DYJetsToLL_M50/'
DY50_extDir_mem = eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_mem/DYJetsToLL_M50_ext/'
DY10Dir_mem     = eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_mem/DYJetsToLL_M10to50/'
TT_dir_mem      = eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_mem/TTJets/'  
W_dir_mem       = eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_mem/WJetsToLNu/'
W_ext_dir_mem   = eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_mem/WJetsToLNu_ext/'
#data_B_mem      = eos+'ntuples/HN3Lv2.0/data/mem/2017B/Single_mu_2017B/'
data_B_mem      = '/work/dezhu/4_production/production_20190429_Data_mem/ntuples/Single_mu_2017B/'
data_C_mem      = '/work/dezhu/4_production/production_20190429_Data_mem/ntuples/Single_mu_2017C/'
data_D_mem      = '/work/dezhu/4_production/production_20190429_Data_mem/ntuples/Single_mu_2017D/'
data_E_mem      = '/work/dezhu/4_production/production_20190429_Data_mem/ntuples/Single_mu_2017E/'
data_F_mem      = '/work/dezhu/4_production/production_20190429_Data_mem/ntuples/Single_mu_2017F/'
###########################################################################################################################################################################################
DYBBDir_mmm     = '/work/dezhu/4_production/production_20190411_Bkg_mmm/ntuples/DYBB/'
DY50Dir_mmm     = '/work/dezhu/4_production/production_20190411_Bkg_mmm/ntuples/DYJetsToLL_M50/'
DY50_extDir_mmm = '/work/dezhu/4_production/production_20190411_Bkg_mmm/ntuples/DYJetsToLL_M50_ext/'
DY10Dir_mmm     = '/work/dezhu/4_production/production_20190411_Bkg_mmm/ntuples/DYJetsToLL_M10to50/'
TT_dir_mmm      = '/work/dezhu/4_production/production_20190411_Bkg_mmm/ntuples/TTJets/'  
W_dir_mmm       = '/work/dezhu/4_production/production_20190411_Bkg_mmm/ntuples/WJetsToLNu/'
W_ext_dir_mmm   = '/work/dezhu/4_production/production_20190411_Bkg_mmm/ntuples/WJetsToLNu_ext/'
data_B_mmm      = '/work/dezhu/4_production/production_20190411_Data_mmm/ntuples/Single_mu_2017B/'
data_C_mmm      = '/work/dezhu/4_production/production_20190411_Data_mmm/ntuples/Single_mu_2017C/'
data_D_mmm      = '/work/dezhu/4_production/production_20190411_Data_mmm/ntuples/Single_mu_2017D/'
data_E_mmm      = '/work/dezhu/4_production/production_20190411_Data_mmm/ntuples/Single_mu_2017E/'
data_F_mmm      = '/work/dezhu/4_production/production_20190411_Data_mmm/ntuples/Single_mu_2017F/'
###########################################################################################################################################################################################
DYBBDir_eee     = eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_eee/partial/DYBB/'
DY50Dir_eee     = eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_eee/partial/DYJetsToLL_M50/'
DY50_extDir_eee = eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_eee/partial/DYJetsToLL_M50_ext/'
DY10Dir_eee     = eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_eee/partial/DYJetsToLL_M10to50/'
TT_dir_eee      = eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_eee/partial/TTJets_amcat/'  
W_dir_eee       = eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_eee/partial/WJetsToLNu/'
W_ext_dir_eee   = eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_eee/partial/WJetsToLNu_ext/'
data_B_eee      = '/work/dezhu/4_production/production_20190502_Data_eee/ntuples/Single_ele_2017B/'
data_C_eee      = '/work/dezhu/4_production/production_20190502_Data_eee/ntuples/Single_ele_2017C/'
data_D_eee      = '/work/dezhu/4_production/production_20190502_Data_eee/ntuples/Single_ele_2017D/'
data_E_eee      = '/work/dezhu/4_production/production_20190502_Data_eee/ntuples/Single_ele_2017E/'
data_F_eee      = '/work/dezhu/4_production/production_20190502_Data_eee/ntuples/Single_ele_2017F/'
###########################################################################################################################################################################################
DYBBDir_eem     = eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_eem/DYBB/'
DY50Dir_eem     = eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_eem/DYJetsToLL_M50/'
DY50_extDir_eem = eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_eem/DYJetsToLL_M50_ext/'
DY10Dir_eem     = eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_eem/DYJetsToLL_M10to50/'
TT_dir_eem      = eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_eem/TTJets_amcat/'  
W_dir_eem       = eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_eem/WJetsToLNu/'
W_ext_dir_eem   = eos+'ntuples/HN3Lv2.0/background/montecarlo/mc_eem/WJetsToLNu_ext/'
data_B_eem      = '/work/dezhu/4_production/production_20190511_Data_eem/ntuples/Single_ele_2017B/'
data_C_eem      = '/work/dezhu/4_production/production_20190511_Data_eem/ntuples/Single_ele_2017C/'
data_D_eem      = '/work/dezhu/4_production/production_20190511_Data_eem/ntuples/Single_ele_2017D/'
data_E_eem      = '/work/dezhu/4_production/production_20190511_Data_eem/ntuples/Single_ele_2017E/'
data_F_eem      = '/work/dezhu/4_production/production_20190511_Data_eem/ntuples/Single_ele_2017F/'
###########################################################################################################################################################################################

###########################################################################################################################################################################################
### FAKEABLE OBJECTS AND PROMPT LEPTON DEFINITIONS
###########################################################################################################################################################################################
charge_01 = ' && hnl_q_01 == 0'
charge_02 = ' && hnl_q_02 == 0'
###########################################################################################################################################################################################
### PROMPT LEPTONS
###########################################################################################################################################################################################
l0_m = 'l0_pt > 25 && abs(l0_eta) < 2.4 && abs(l0_dz) < 0.2 && abs(l0_dxy) < 0.05 && l0_reliso_rho_03 < 0.2 && l0_id_m == 1'                  # l0 genuine muon
l1_m = 'l1_pt > 10 && abs(l1_eta) < 2.4 && abs(l1_dz) < 0.2 && abs(l1_dxy) < 0.05 && l1_reliso_rho_03 < 0.2 && l1_id_m == 1'                  # l1 genuine muon 
l2_m = 'l2_pt > 10 && abs(l2_eta) < 2.4 && abs(l2_dz) < 0.2 && abs(l2_dxy) < 0.05 && l2_reliso_rho_03 < 0.2 && l2_id_m == 1'                  # l2 genuine muon 

l0_e = 'l0_pt > 25 && abs(l0_eta) < 2.5 && abs(l0_dz) < 0.2 && abs(l0_dxy) < 0.05 && l0_reliso_rho_03 < 0.2 && l0_eid_mva_iso_wp90 == 1'      # l0 genuine electron
l1_e = 'l1_pt > 10 && abs(l1_eta) < 2.5 && abs(l1_dz) < 0.2 && abs(l1_dxy) < 0.05 && l1_reliso_rho_03 < 0.2 && l1_eid_mva_iso_wp90 == 1'      # l1 genuine electron 
l2_e = 'l2_pt > 10 && abs(l2_eta) < 2.5 && abs(l2_dz) < 0.2 && abs(l2_dxy) < 0.05 && l2_reliso_rho_03 < 0.2 && l2_eid_mva_iso_wp90 == 1'      # l2 genuine electron 

###########################################################################################################################################################################################
### FAKEABLE OBJECTS
###########################################################################################################################################################################################
l1_m_loose  = 'l1_pt > 5 && abs(l1_eta) < 2.4 && abs(l1_dz) < 2 && abs(l1_dxy) > 0.01'                                              # l1 kinematics and impact parameter
l1_m_tight  = l1_m_loose + ' &&  l1_Medium == 1 && l1_reliso_rho_03 < 0.2'
l1_m_lnt    = l1_m_loose + ' && (l1_Medium == 0 || l1_reliso_rho_03 > 0.2)'

l2_m_loose  = 'l2_pt > 5 && abs(l2_eta) < 2.4 && abs(l2_dz) < 2 && abs(l2_dxy) > 0.01'                                              # l2 kinematics and impact parameter
l2_m_tight  = l2_m_loose + ' &&  l2_Medium == 1 && l2_reliso_rho_03 < 0.2'
l2_m_lnt    = l2_m_loose + ' && (l2_Medium == 0 || l2_reliso_rho_03 > 0.2)'

l1_e_loose  = 'l1_pt > 5 && abs(l1_eta) < 2.5 && abs(l1_dz) < 2 && abs(l1_dxy) > 0.05'                                              # l1 kinematics and impact parameter
l1_e_tight  = l1_e_loose + ' &&  l1_MediumNoIso == 1 && l1_reliso_rho_03 < 0.2'
l1_e_lnt    = l1_e_loose + ' && (l1_MediumNoIso == 0 || l1_reliso_rho_03 > 0.2)'

l2_e_loose  = 'l2_pt > 5 && abs(l2_eta) < 2.5 && abs(l2_dz) < 2 && abs(l2_dxy) > 0.05'                                              # l2 kinematics and impact parameter
l2_e_tight  = l2_e_loose + ' &&  l2_MediumNoIso == 1 && l2_reliso_rho_03 < 0.2'
l2_e_lnt    = l2_e_loose + ' && (l2_MediumNoIso == 0 || l2_reliso_rho_03 > 0.2)'
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
SFR_EEE_L_CUT = ''
#SFR_MMM_L_CUT = ' && ( (l1_reliso_rho_03 < 0.42 && abs(l1_eta) < 1.2) || (l1_reliso_rho_03 < 0.35 && abs(l1_eta) > 1.2) )'  # dR 03
#SFR_MMM_L_CUT = ' && ( (l1_reliso_rho_03 < 0.6 && abs(l1_eta) < 1.2) || (l1_reliso_rho_03 < 0.95 && abs(l1_eta) > 1.2 && abs(l1_eta) < 2.1) || (l1_reliso_rho_03 < 0.4 && abs(l1_eta) > 2.1) )'  # dR 03 (29.4.19)
#SFR_MMM_L_CUT = '' #try to see what happens...
SFR_MMM_L_CUT = ' && ( (l1_reliso_rho_03 < 0.38 && abs(l1_eta) < 1.2) || (l1_reliso_rho_03 < 0.29 && abs(l1_eta) > 1.2 && abs(l1_eta) < 2.1) || (l1_reliso_rho_03 < 0.19 && abs(l1_eta) > 2.1) )'  #dR 03 (6.5.19 incl cross dR veto)
#SFR_MEM_L_CUT = ' && ( (l1_reliso_rho_03 < 0.6  && abs(l1_eta) < 0.8) || (l1_reliso_rho_03 < 0.35 && abs(l1_eta) > 0.8) )'  # dR 03
#SFR_MEM_L_CUT = ' && ( (l1_reliso_rho_03 < 0.93  && abs(l1_eta) < 0.8) || (l1_reliso_rho_03 < 0.63 && abs(l1_eta) > 0.8 && abs(l1_eta) < 1.479) || (l1_reliso_rho_03 < 0.41 && abs(l1_eta) > 1.479) )' #dR 03 (7.5.19 incl cross dR veto)
#SFR_MEM_L_CUT = ' && ( (l1_reliso_rho_04 < 0.4  && abs(l1_eta) < 0.8) || (l1_reliso_rho_04 < 0.7 && abs(l1_eta) > 0.8 && abs(l1_eta) < 1.479) || (l1_reliso_rho_04 < 0.3 && abs(l1_eta) > 1.479) )'  # dR 04

### DY - SELECTION
### SFR::MMM 
SFR_EEE_021_L   =  l0_e + ' && ' + l2_e + ' && ' + l1_e_loose 
SFR_EEE_021_L   += charge_02                                        # opposite charge 
#SFR_EEE_021_L   += SFR_EEE_L_CUT                                    # reliso bound for LOOSE cf. checkIso_mmm_220319 
SFR_EEE_021_LNT =  SFR_EEE_021_L + ' && ' + l1_e_lnt
SFR_EEE_021_T   =  SFR_EEE_021_L + ' && ' + l1_e_tight 

SFR_EEE_012_L   =  l0_e + ' && ' + l1_e + ' && ' + l2_e_loose 
SFR_EEE_012_L   += re.sub('02', '01', charge_02)                    # opposite charge 
#SFR_EEE_012_L   += re.sub('l1', 'l2', SFR_EEE_L_CUT)                # reliso bound for LOOSE cf. checkIso_mmm_220319 
SFR_EEE_012_LNT =  SFR_EEE_012_L + ' && ' + l2_e_lnt
SFR_EEE_012_T   =  SFR_EEE_012_L + ' && ' + l2_e_tight 

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
#SFR_MEM_021_L   += SFR_MEM_L_CUT                                    # reliso bound for LOOSE cf. checkIso_mmm_220319 
SFR_MEM_021_LNT =  SFR_MEM_021_L + ' && ' + l1_e_lnt
SFR_MEM_021_T   =  SFR_MEM_021_L + ' && ' + l1_e_tight 

'''study TT'''
### TT - SELECTION
### SFR::MEM 
SFR_MEM_012_L   =  l0_m + ' && ' + l1_e + ' && ' + l2_m_loose 
SFR_MEM_012_L   += charge_01                                        # opposite charge 
SFR_MEM_012_L   += ' && nbj > 0 && abs(hnl_m_02 - 91.19) > 10'
SFR_MEM_012_LNT =  SFR_MEM_012_L + ' && ' + l2_m_lnt
SFR_MEM_012_T   =  SFR_MEM_012_L + ' && ' + l2_m_tight 

#SFR_MEM_012_L   += ' && nbj > 0'#
SFR_EEM_012_L   =  l0_e + ' && ' + l1_e + ' && ' + l2_m_loose 
SFR_EEM_012_L   += ' && hnl_q_01 == 0'                                  # opposite charge 
#SFR_EEM_012_L   += re.sub('l1', 'l2', SFR_MMM_L_CUT)                # reliso bound for LOOSE cf. checkIso_mmm_220319 
SFR_EEM_012_LNT =  SFR_EEM_012_L + ' && ' + l2_m_lnt
SFR_EEM_012_T   =  SFR_EEM_012_L + ' && ' + l2_m_tight 
###########################################################################################################################################################################################
### ENERGY-IN-CONE CORRECTED PT
###########################################################################################################################################################################################
PTCONE   = '(  ( hnl_hn_vis_pt * (hnl_iso03_rel_rhoArea<0.2) ) + ( (hnl_iso03_rel_rhoArea>=0.2) * ( hnl_hn_vis_pt * (1. + hnl_iso03_rel_rhoArea - 0.2) ) )  )'
PTCONEL1 = '(  ( l1_pt         * (l1_reliso_rho_03<0.2) )      + ( (l1_reliso_rho_03>=0.2)      * ( l1_pt         * (1. + l1_reliso_rho_03 - 0.2) ) )  )'
PTCONEL2 = '(  ( l2_pt         * (l2_reliso_rho_03<0.2) )      + ( (l2_reliso_rho_03>=0.2)      * ( l2_pt         * (1. + l2_reliso_rho_03 - 0.2) ) )  )'
###########################################################################################################################################################################################
### BINNING FOR CLOSURE TEST 
###########################################################################################################################################################################################
b_nbj       = np.arange(0., 10, 1)
b_N         = np.arange(-0.5, 3.5,1)
b_pt_std    = np.arange(5.,105,5)
b_pt        = np.array([ 0., 5., 10., 15., 20., 25., 35., 50., 70.])
b_pt_mu_sfr = np.array([ 0., 5., 10., 20., 70.])
b_2d        = np.arange(0., 11, 1)
b_2d_sig    = np.arange(0., 105, 5)
b_m         = np.arange(0.,11,1)
b_M         = np.arange(0.,204,4)
b_eta_mu    = np.array([0., 1.2, 2.1, 2.4]) 
b_eta_ele   = np.array([0., 0.8, 1.479, 2.5]) 
b_rho       = np.arange(0.,15,0.25)
b_dphi      = np.arange(-3.142,3.142,0.3)
b_dR        = np.arange(0.,0.85,0.05)
b_dR_coarse = np.arange(0.,6,0.2)
b_dR_Coarse = np.arange(0.,6,0.4)
b_z         = np.arange(-1.5,1.5,0.06)
b_abs_z     = np.arange(0.,2,0.05)
b_z_fine    = np.arange(-0.02,0.02,0.0001)
b_st        = np.arange(-20,20,1)
b_sf        = np.arange(-20,20,1)
b_y         = np.arange(0.,1.,0.1)
b_dxy       = np.arange(0.,0.51,0.01)
b_chi2      = np.arange(0.,1.05,0.05)

'''framer for TEfficiency plots'''
framer = rt.TH2F('','',len(b_pt)-1,b_pt,len(b_y)-1,b_y)
framer.GetYaxis().SetRangeUser(0.,1.0)
framer.GetYaxis().SetRangeUser(0.,0.5)
#framer.GetYaxis().SetRangeUser(0.01,0.5)
############################################################################################################################################################################

############################################################################################################################################################################
def produceLightTree(sample='DY',ch='mmm'):

    if ch == 'mmm':
        d17B = data_B_mmm+suffix; d17C = data_C_mmm+suffix; d17D = data_D_mmm+suffix; d17E = data_E_mmm+suffix; d17F = data_F_mmm+suffix; 
        SFR_012_L = SFR_MMM_012_L
        l2_tight = l2_m_tight

    if ch == 'eem':
        d17B = data_B_eem+suffix; d17C = data_C_eem+suffix; d17D = data_D_eem+suffix; d17E = data_E_eem+suffix; d17F = data_F_eem+suffix; 

    t = rt.TChain('tree')

    if sample == 'DY':
        t.Add(DY)
        t.Add(DY_ext)

    if sample == 'data':
        t.Add(d17B)
       #t.Add(d17C)
       #t.Add(d17D)
       #t.Add(d17E)
       #t.Add(d17F)

    print '\n\ttotal entries:', t.GetEntries()

    df = RDF(t)
    df1 = df.Define('LOOSE', '1 * (' + SFR_012_L + ' && hnl_dr_12 > 0.3 && hnl_dr_02 > 0.3 && abs(hnl_m_01 - 91.19) < 10 && hnl_q_01 == 0 )' )
    df2 = df1.Define('TIGHT', '1 * (' + SFR_012_L + ' && hnl_dr_12 > 0.3 && hnl_dr_02 > 0.3 && abs(hnl_m_01 - 91.19) < 10 && hnl_q_01 == 0 && ' + l2_tight + ')' )

    num_L = df2.Filter('LOOSE == 1').Count().GetValue()
    print '\n\tloose entries in MR:', num_L 

    num_T = df2.Filter('TIGHT == 1').Count().GetValue()
    print '\n\ttight entries in MR:', num_T

    df2 = df2.Define('ptcone', PTCONEL2)

    branchList = rt.vector('string')()
    for br in ['event', 'lumi', 'run', 'LOOSE', 'TIGHT', 'l2_reliso_rho_03', 'l2_Medium', 'l2_eta', 'l2_pt', 'l2_dxy', 'l2_dz', 'ptcone']:
        branchList.push_back(br)
    df2.Snapshot('tree', saveDir+'/%s_%s_6_26B_Lcut_06_5.root'%(sample,ch), branchList)

def split(file_name): #without.root

    tfile = rt.TFile(file_name+'.root')
    tree = tfile.Get('tree')

    df = RDF(tree)
    n = tree.GetEntries()
    df1 = df.Range(0,int(n/2))
    df2 = df.Range(int(n/2),0)
    df1.Snapshot('tree', '%s_training_half.root'%file_name)
    df2.Snapshot('tree', '%s_untouched_half.root'%file_name)
############################################################################################################################################################################

############################################################################################################################################################################
def closureTest(ch='mmm', mode='sfr', isData=True, CONV=True, subtract=True, verbose=True, output=False, fr=False, full=False):
    
    input = 'MC' if isData == False else 'DATA'

    oldPlotDir = eos+'plots/DDE/'
    plotDir = makeFolder('closureTest_%s'%ch)
    sys.stdout = Logger(plotDir + 'closureTest_%s' %ch)
    print '\n\tplotDir:', plotDir

    print '\n\tcopy from: %s' %oldPlotDir
    sfr = False; dfr = False; print '\n\tmode: %s, \tch: %s, \tisData: %s, \tCONV: %s, \tsubtract: %s' %(mode, ch, isData, CONV, subtract)
    if mode == 'sfr': sfr = True
    if mode == 'dfr': dfr = True

    ### PREPARE CUTS AND FILES
    SFR, DFR, dirs = selectCuts(ch)

    SFR_021_L, SFR_012_L, SFR_021_LNT, SFR_012_LNT, SFR_021_T, SFR_012_T = SFR 
    DFR_L, DFR_T, DFR_LNT = DFR
    DYBB_dir, DY10_dir, DY50_dir, DY50_ext_dir, TT_dir, W_dir, W_ext_dir, DATA = dirs   

    if full == False: DATA = DATA[:1]

    ### APPLICATION REGION
    appReg = 'hnl_w_vis_m < 80'
    appReg = 'hnl_w_vis_m > 95'
    appReg = '1 == 1'

    mReg   = '1 == 1'

    cuts_FR = appReg # 27_3 FOR CLOSURE TEST LEAVE DR_12 < 0.3 TO SEE WHAT HAPPENS
    #cuts_FR = appReg + ' && hnl_dr_12 > 0.3'
    #cuts_FR = appReg + ' && hnl_dr_12 > 0.3 && abs(hnl_m_01 - 91.19) < 10'

    cuts_FR_021 = '1 == 1';    cuts_FR_012 = '1 == 1';    tight_021   = '1 == 1';    tight_012   = '1 == 1'
    lnt_021     = '1 == 1';    lnt_012     = '1 == 1';    ptconel1    = PTCONEL1;    ptconel2    = PTCONEL2

    if sfr:

        #### GENERAL 
        print '\n\tdrawing single fakes ...'
        mode021 = False; mode012 = False

        if ch == 'mmm':
            b_eta = b_eta_mu
            cuts_FR_012 = cuts_FR + ' && hnl_dr_02 > 0.3 && hnl_dr_12 > 0.3 && ' + SFR_MMM_012_L
            cuts_FR_021 = cuts_FR + ' && hnl_dr_01 > 0.3 && hnl_dr_12 > 0.3 && ' + SFR_MMM_021_L + ' && nbj > 500'
            lnt_021 = SFR_MMM_021_LNT
            lnt_012 = SFR_MMM_012_LNT
            tight_021 = SFR_MMM_021_T
            tight_012 = SFR_MMM_012_T
            mode012 = True
            mode021 = True 

        if ch == 'eem':
            b_eta = b_eta_mu
            cuts_FR_012 = cuts_FR + ' && hnl_dr_02 > 0.3 && hnl_dr_12 > 0.3 && ' + SFR_EEM_012_L
            cuts_FR_021 = cuts_FR + ' && nbj > 50'
            lnt_012 = SFR_EEM_012_LNT
            lnt_021 = SFR_EEM_012_LNT
            tight_012 = SFR_EEM_012_T
            tight_021 = SFR_EEM_012_T
            mode012 = True
            mode021 = True


    ### PREPARE TREES
    t = None
    t = rt.TChain('tree')
    t.Add(data_B_mmm+suffix)
    #t.Add(data_C_mmm+suffix)
    #t.Add(data_D_mmm+suffix)
    #t.Add(data_E_mmm+suffix)
    #t.Add(data_F_mmm+suffix) 
    #t.Add(eos+'ML_FR/DY/DY_6_18_half1_output.root')
    #t.AddFriend('DY = tree',      DY50Dir_mmm    +suffix)
    #t.AddFriend('DY_ext = tree',  DY50_extDir_mmm+suffix)

    #try: t.AddFriend('ml_fr = tree', eos+'plost/DDE/closureTest_190624_15h_35m/data_weights.root')
    #sys.stdout = sys.__stdout__; sys.stderr = sys.__stderr__; set_trace()
    try: 
        print (eos+'ML_FR/repr_6_19/data_mmm_6_26B_Lcut_06_5_Keq1_training_half_output.root')
        t.AddFriend('ML = tree', eos+'ML_FR/repr_6_19/data_mmm_6_26B_Lcut_06_5_Keq1_training_half_output.root')
        #t.AddFriend('ML = tree', eos+'ML_FR/data_geq0p01dxy/data_6_18_training_half_weights.root')
   #     t.AddFriend('ML = tree', 'data_weights.root')
   #     #try: t.AddFriend('ML = tree', eos+'ML_FR/data_geq0p01dxy/data_weights.root')
    except:
        sys.stdout = sys.__stdout__; sys.stderr = sys.__stderr__; set_trace()
        #uf_dataB = ur.open(eos+'ML_FR/data_geq0p01dxy/data_6_18_training_half.root')
        uf_dataB = ur.open(data_B_mmm+suffix)
        #uf_dataC = ur.open(data_C_mmm+suffix)
        #uf_dataD = ur.open(data_D_mmm+suffix)
        #uf_dataE = ur.open(data_E_mmm+suffix)
        #uf_dataF = ur.open(data_F_mmm+suffix)

        ut_dataB = uf_dataB['tree']
        #ut_dataC = uf_dataC['tree']
        #ut_dataD = uf_dataD['tree']
        #ut_dataE = uf_dataE['tree']
        #ut_dataF = uf_dataF['tree']

        pdf_dataB = ut_dataB.pandas.df(['event','lumi','run','l2_pt','l2_dxy','l2_eta', 'l2_reliso_rho_03'])
        #pdf_dataC = ut_dataC.pandas.df(['event','lumi','run','l2_pt','l2_dxy','l2_eta'])
        #pdf_dataD = ut_dataD.pandas.df(['event','lumi','run','l2_pt','l2_dxy','l2_eta'])
        #pdf_dataE = ut_dataE.pandas.df(['event','lumi','run','l2_pt','l2_dxy','l2_eta'])
        #pdf_dataF = ut_dataF.pandas.df(['event','lumi','run','l2_pt','l2_dxy','l2_eta'])

        # https://pandas.pydata.org/pandas-docs/stable/user_guide/merging.html
        pdf_data = pd.concat([pdf_dataB])#,pdf_dataC, pdf_dataD, pdf_dataE, pdf_dataF]
        pdf_data['l2_abs_dxy'] = np.abs(pdf_data.l2_dxy)
        pdf_data['l2_abs_eta'] = np.abs(pdf_data.l2_eta)
        pdf_data['l2_ptcone']  = pdf_data.l2_pt * (1 + np.maximum(0, pdf_data.l2_reliso_rho_03 - 0.2) )

        # RUN CLASSIFIER HERE
        features = ['l2_ptcone','l2_abs_dxy','l2_abs_eta']

        classifier = load_model('net.h5')
        print '\n\tpredicting on', pdf_data.shape[0], 'events'
        x  = pd.DataFrame(pdf_data, columns=features)
        y = classifier.predict(x)

        # add the score to the data_train_l sample
        #pdf_data.insert(len(pdf_data.columns), 'score', y)
        #k = np.sum(pdf_data.score)
        #T = np.count_nonzero(pdf_data.TIGHT)
        #K = T/k 
        #print(k, T, K)

        pdf_data.insert(len(pdf_data.columns), 'ml_fr_weight', y)
        #pdf_data.to_root(eos+'ML_FR/data_geq0p01dxy/data_weights.root','tree')
        pdf_data.to_root(eos+'ML_FR/data_geq0p01dxy/data_6_18_training_half_weights.root','tree')
        #t.AddFriend('ML = tree', eos+'ML_FR/data_geq0p01dxy/data_weights.root')
        t.AddFriend('ML = tree', eos+'ML_FR/data_geq0p01dxy/data_6_18_training_half_weights.root')

    sys.stdout = sys.__stdout__; sys.stderr = sys.__stderr__; set_trace()

    df0 = RDF(t)
    n = df0.Count().GetValue()
    print '\n\tentries:', n 
    #for validation with first half of dataset
    df0 = df0.Range(0,int(n/2))
    df  = df0.Define('_norm_', '1')
    df  = df.Define('abs_l1_eta', 'abs(l1_eta)')
    df  = df.Define('abs_l2_eta', 'abs(l2_eta)')
    df  = df.Define('abs_l1_dxy', 'abs(l1_dxy)')
    df  = df.Define('abs_l2_dxy', 'abs(l2_dxy)')
    print'\n\tchain made.'
    sys.stdout = sys.__stdout__; sys.stderr = sys.__stderr__; set_trace()

    ## VALIDATIO OF FRIEND TREE
    print '\n\t: VALIDATION                      :'
    vld_evt = df.Filter('ML.event - event != 0').Count().GetValue()
    print '\t: ML.event - event != 0: %d events :'%vld_evt
    vld_pt = df.Filter('ML.l2_pt - l2_pt != 0').Count().GetValue()
    print '\t: ML.l2_pt - l2_pt != 0: %d events :'%vld_pt
    if vld_pt != 0 or vld_evt != 0: sys.stdout = sys.__stdout__; sys.stderr = sys.__stderr__; set_trace()

    ''' SCALE MC #TODO PUT THIS IN A FUNCTION
    ### lumi = 4792.0 /pb data B
    ### lumi = 41530.0 /pb data 2017 full golden JSON -->  https://twiki.cern.ch/twiki/bin/viewauth/CMS/PdmV2017Analysis'''
    lumi = 4792.0 if full == False else 41530.0 

   ### DY
   #pckfile_dy = DY50_ext_dir+'SkimAnalyzerCount/SkimReport.pck'
   #xsec_dy    = DYJetsToLL_M50_ext.xSection

   #pckobj_dy     = pickle.load(open(pckfile_dy, 'r'))
   #counters_dy   = dict(pckobj_dy)
   #sumweights_dy = counters_dy['Sum Norm Weights']

   ### TT
   #pckfile_tt = TT_dir+'SkimAnalyzerCount/SkimReport.pck'
   #xsec_tt    = TTJets.xSection

   #pckobj_tt     = pickle.load(open(pckfile_tt, 'r'))
   #counters_tt   = dict(pckobj_tt)
   #sumweights_tt = counters_tt['Sum Norm Weights']

   #DY_SCALE = lumi * xsec_dy / sumweights_dy
   #print '\n\tlumi: %0.2f, DY: xsec: %0.2f, sumweights: %0.2f, SCALE: %0.2f' %(lumi, xsec_dy, sumweights_dy, DY_SCALE)
   #TT_SCALE = lumi * xsec_tt / sumweights_tt
   #print '\n\tlumi: %0.2f, TT: xsec: %0.2f, sumweights: %0.2f, SCALE: %0.2f' %(lumi, xsec_tt, sumweights_tt, TT_SCALE)

    ### initialize DF placeholders to avoid empty calls
    dfLNT_021 = None; dfLNTConv_021 = None; dfT_021 = None; dfTdata_021 = None; dfTConv_021 = None
    dfLNT_012 = None; dfLNTConv_012 = None; dfT_012 = None; dfTdata_012 = None; dfTConv_012 = None

    '''PREPARE DATAFRAMES'''

    '''MODE 021
       l0 and l2 prompt, l1 is tested'''
    cuts_l_021 = cuts_FR_021
    f0_021 = df.Filter(cuts_l_021)
    if mode021 == True:
        print '\n\tloose df 021 defined.'
        print '\n\tloose df 021 events:', f0_021.Count().GetValue()
    #    print '\n\tTIGHT df 021 events:', f0_021.Filter('ML.TIGHT==1').Count().GetValue()

    f1_021    = f0_021.Define('ptcone021', ptconel1)
    dfL_021   = f1_021#.Define('abs_l1_eta', 'abs(l1_eta)')

    dfLNT0_021 = dfL_021.Filter(lnt_021)
    dfLNT1_021 = dfLNT0_021.Define('fover1minusf021', '2.32 * ML.ml_fr/(1-ML.ml_fr)')
    dfLNT2_021 = dfLNT1_021.Define('lnt_021_evt_wht', 'fover1minusf021 * weight * lhe_weight')
    if isData == False: 
        dfLNT_021 = dfLNT2_021 
        if mode021 == True: print '\n\tfr mc 021 defined.'
    if isData == True: 
        dfLNTdata_021 = dfLNT2_021#.Filter('ftdata.label == 0')
        if mode021 == True: print '\n\tfr data 021 defined.'
    if mode021 == True: print '\n\tweight f/(1-f)  021 defined.'

    if subtract == True: dfLNTConv_021 = dfLNT2_021.Filter('ftdy.label == 1 && ( (abs(l1_gen_match_pdgid) != 22 && l1_gen_match_isPrompt == 1) ||  abs(l1_gen_match_pdgid) == 22 )') 
    if mode021 == True:  print '\n\tlnt df 021 defined.'

    if mode021 == True: print '\n\tlnt df 021 events:', dfLNT0_021.Count().GetValue()

    dfT0_021  = dfL_021.Filter(tight_021)
    dfT_021   = dfT0_021.Define('t_021_evt_wht', 'weight * lhe_weight')
    #dfTTT_021 = dfT_021.Filter('fttt.label == 2')
    if isData == False and mode021 == True: print '\n\ttight mc 021 defined.'
    if isData == True: 
        dfTdata_021 = dfT_021#.Filter('ftdata.label == 0')
        if mode021 == True: print '\n\ttight data 021 defined.'
    if CONV == True: dfTConv_021 = dfT_021.Filter('ftdy.label == 1 && ( (abs(l1_gen_match_pdgid) != 22 && l1_gen_match_isPrompt == 1) ||  abs(l1_gen_match_pdgid) == 22 )') 

    if mode021 == True: print '\n\ttight df 021 events:', dfT_021.Count().GetValue()

    '''MODE 012
       l0 and l1 prompt, l2 is tested'''
    cuts_l_012 = cuts_FR_012
    f0_012 = df.Filter(cuts_l_012)
    if mode012 == True: print '\n\tloose df 012 defined.'

    if mode012 == True: print '\n\tloose df 012 events:', f0_012.Count().GetValue()

    f1_012    = f0_012.Define('ptcone012', ptconel2)
    dfL_012   = f1_012#.Define('abs_l2_eta', 'abs(l2_eta)')

    #print '\n\t: VALIDATION                      :'
    #vld_ptc = dfL_012.Filter('ML.ptcone012 - l2_ptcone != 0').Count().GetValue()
    #print '\t: ML.ptcone - ptcone != 0: %d events :'%vld_ptc

    dfLNT0_012 = dfL_012.Filter(lnt_012)
    dfLNT1_012 = dfLNT0_012.Define('fover1minusf012', '2.32 * ML.ml_fr/(1-ML.ml_fr)')
    dfLNT2_012 = dfLNT1_012.Define('lnt_012_evt_wht', 'fover1minusf012 * weight * lhe_weight')
    if isData == False: 
        dfLNT_012 = dfLNT2_012 
        if mode012 == True: print '\n\tlnt mc 012 defined.'
    if isData == True:  
        dfLNTdata_012 = dfLNT2_012#.Filter('ftdata.label == 0')
        if mode012 == True: print '\n\tlnt data 012 defined.'

    if subtract == True: dfLNTConv_012 = dfLNT2_012.Filter('ftdy.label == 1 && ( (abs(l2_gen_match_pdgid) != 22 && l2_gen_match_isPrompt == 1) ||  abs(l2_gen_match_pdgid) == 22 )') 
    if mode012 == True:  print '\n\tweight f/(1-f)  012 defined. (without lumi/data normalization)'

    if mode012 == True: print '\n\tlnt df 012 events:', dfLNT0_012.Count().GetValue()

    dfT0_012 = dfL_012.Filter(tight_012)
    dfT_012 = dfT0_012.Define('t_012_evt_wht', 'weight * lhe_weight')
    #dfTTT_012 = dfT_012.Filter('fttt.label == 2')
    if isData == False and mode012 == True: print '\n\ttight mc 012 defined.'
    if isData == True: 
        dfTdata_012 = dfT_012#.Filter('ftdata.label == 0')
        if mode012 == True: print '\n\ttight data 012 defined.'
    if CONV == True: dfTConv_012 = dfT_012.Filter('ftdy.label == 1 && ( (abs(l2_gen_match_pdgid) != 22 && l2_gen_match_isPrompt == 1) || abs(l2_gen_match_pdgid) == 22 )') 

    if mode012 == True: print '\n\ttight df 012 events:', dfT_012.Count().GetValue()

    print '\n\t cuts: %s'                   %cuts_FR
    if mode012 ==True:
        print '\n\tloose 012: %s\n'         %(cuts_FR_012)
        print '\n\ttight 012: %s\n'         %(tight_012)
        print '\ttotal loose 012: %s\n'     %f0_012.Count().GetValue()
    if mode021 ==True:
        print '\n\tloose 021: %s\n'         %(cuts_FR_021)
        print '\n\ttight 021: %s\n'         %(tight_021)
        print '\ttotal loose 021: %s\n'     %f0_021.Count().GetValue()
    
    ## SAVE FR OUTPUT BRANCH IN TREE
    if output == True:
        branchList_021 = rt.vector('string')(); branchList_012 = rt.vector('string')()
        for br in ['event', 'lumi']:
            branchList_021.push_back(br)
            branchList_012.push_back(br)
        if CONV == True: branchList_021.push_back('label'); branchList_012.push_back('label')
        time_string = ch + '_' + mode + '_' + date + '_' + hour + '_' + minit
        if mode021 == True:
            branchList_021.push_back('fover1minusf021')
            dfLNT_021.Snapshot('tree', plotDir + 'fr_021_%s.root'%time_string, branchList_021)
        if mode012 == True:
            branchList_012.push_back('fover1minusf012')
            dfLNT_012.Snapshot('tree', plotDir + 'fr_012_%s.root'%time_string, branchList_012)

    sys.stdout = sys.__stdout__; sys.stderr = sys.__stderr__; set_trace()

    VARS = OrderedDict()
    VARS ['pt']          =  None
    VARS ['eta']         =  None
    VARS ['norm']        = [len(b_N)-1,        b_N,            '_norm_'         ,   ';Normalisation; Counts'] 
    VARS ['m_triL']      = [len(b_M)-1,        b_M,            'hnl_w_vis_m'    ,   ';m(prompt_{1},  prompt_{2},  FO) [GeV]; Counts']
    VARS ['BGM_01']      = [len(b_M)-1,        b_M,            'hnl_m_01'       ,   ';m(prompt_{1},  prompt_{2}) [GeV]; Counts'] 
    VARS ['BGM_02']      = [len(b_M)-1,        b_M,            'hnl_m_02'       ,   ';m(prompt_{1},  FO) [GeV]; Counts']
    VARS ['m_dilep']     = [len(b_m)-1,        b_m,            'hnl_m_12'       ,   ';m(prompt_{2},  FO) [GeV]; Counts'] 
    VARS ['dr_12']       = [len(b_dR)-1,       b_dR,           'hnl_dr_12'      ,   ';#DeltaR(prompt_{2},  FO); Counts'] 
    VARS ['BGM_dilep']   = [len(b_M)-1,        b_M,            'hnl_m_12'       ,   ';m(prompt_{2},  FO) [GeV]; Counts'] 
    VARS ['nbj']         = [len(b_nbj)-1,      b_nbj,          'nbj'            ,   ';Number of b-jets; Counts'] 
    VARS ['2disp']       = [len(b_2d)-1,       b_2d,           'hnl_2d_disp'    ,   ';2d_disp [cm]; Counts'] 
    VARS [ 'dr_01']      = [len(b_dR)-1,       b_dR_coarse,    'hnl_dr_01'      ,   ';#DeltaR(prompt_{1},  prompt_{2}); Counts'] 
    VARS [ 'dr_02']      = [len(b_dR)-1,       b_dR_coarse,    'hnl_dr_02'      ,   ';#DeltaR(prompt_{1},  FO); Counts'] 
    VARS [ '2disp_sig']  = [len(b_2d_sig)-1,   b_2d_sig,       'hnl_2d_disp_sig',   ';2d_disp_sig ; Counts'] 
    VARS ['dphi_0dilep'] = [len(b_dphi)-1,     b_dphi,         'hnl_dphi_hnvis0',   ';#Delta#Phi(l_{0}, di-lep); Counts']
    VARS ['FO_dxy']      = [len(b_dxy)-1,      b_dxy,          'abs_l2_dxy'     ,   ';|d_{xy}|(FO); Counts']

    _H_OBS_012 = OrderedDict();   _H_OBS_021 = OrderedDict();   dfT_021_L  = OrderedDict()
    _H_WHD_012 = OrderedDict();   _H_WHD_021 = OrderedDict();   dfT_012_L  = OrderedDict()   
    H_OBS_012  = OrderedDict();   H_OBS_021  = OrderedDict();   dfLNT_021_L = OrderedDict()
    H_WHD_012  = OrderedDict();   H_WHD_021  = OrderedDict();   dfLNT_012_L = OrderedDict()  

    for v in VARS.keys():
        _H_OBS_021[v] = OrderedDict();  _H_OBS_012[v] = OrderedDict()
        H_OBS_021[v]  = OrderedDict();  H_OBS_012[v]  = OrderedDict()
        _H_WHD_021[v] = OrderedDict();  _H_WHD_012[v] = OrderedDict()
        H_WHD_021[v]  = OrderedDict();  H_WHD_012[v]  = OrderedDict()
    
    if mode021 == True:
        VARS ['pt']  = [len(b_pt)-1,     b_pt,     'ptcone021'      , ';p_{T}^{cone}(FO) [GeV]; Counts']
        VARS ['eta'] = [len(b_eta)-1,    b_eta,    'abs_l1_eta'     , ';|#eta(FO)|; Counts']

        if fr == True:       dfLNT_021_L ['FR']   = dfLNT_021
        if subtract == True: dfLNT_021_L ['Conv'] = dfLNTConv_021
        if isData == False:  dfT_021_L['DY50']    = dfT_021  
        if isData == True:  
            dfT_021_L ['data'] = dfTdata_021
            if fr == True: dfLNT_021_L ['FR'] = dfLNTdata_021
        if CONV == True:  dfT_021_L['Conv'] = dfTConv_021
        #dfT_021_L ['TT'] = dfTTT_021
        KEYS = dfT_021_L.keys(); keys = dfLNT_021_L.keys()
        print '\n\tKEYS 021: %s, keys 021: %s' %(KEYS, keys)

        for v in VARS.keys():
            if fr == True:       _H_WHD_021[v]['FR']   = dfLNT_021_L['FR'].Histo1D(('whd_021_%s_FR'%v,'whd_021_%s_FR'%v, VARS[v][0], VARS[v][1]), VARS[v][2], 'lnt_021_evt_wht')

            if subtract == True: _H_WHD_021[v]['Conv'] = dfLNTConv_021.Histo1D(('whd_021_%s_Conv'%v,'whd_021_%s_Conv'%v, VARS[v][0], VARS[v][1]), VARS[v][2], 'lnt_021_evt_wht')
            if len(KEYS) == 1:   _H_OBS_021[v]['data'] = dfT_021.Histo1D(('obs_021_%s'%v,'obs_021_%s'%v, VARS[v][0], VARS[v][1]), VARS[v][2], 't_021_evt_wht')

            if len(KEYS) > 1:
                for DF in dfT_021_L.keys():
                    _H_OBS_021[v][DF] = dfT_021_L[DF].Histo1D(('obs_021_%s_%s'%(v,DF),'obs_021_%s_%s'%(v,DF), VARS[v][0], VARS[v][1]), VARS[v][2], 't_021_evt_wht')

    if mode012 == True:
        VARS ['pt']  = [len(b_pt)-1,     b_pt,     'ptcone012'      , ';p_{T}^{cone}(FO) [GeV]; Counts']
        VARS ['eta'] = [len(b_eta)-1,    b_eta,    'abs_l2_eta'     , ';|#eta(FO)|; Counts']

        if fr == True:       dfLNT_012_L ['FR']   = dfLNT_012
        if subtract == True: dfLNT_012_L ['Conv'] = dfLNTConv_012
        if isData == False:  dfT_012_L['DY50']    = dfT_012  
        if isData == True:  
            dfT_012_L ['data'] = dfTdata_012
            if fr == True: dfLNT_012_L ['FR'] = dfLNTdata_012
        if CONV == True:  dfT_012_L['Conv'] = dfTConv_012
        #dfT_012_L ['TT'] = dfTTT_012
        KEYS = dfT_012_L.keys(); keys = dfLNT_012_L.keys()
        print '\n\tKEYS 012: %s, keys 012: %s' %(KEYS, keys)

        for v in VARS.keys():
            if fr == True:       _H_WHD_012[v]['FR']   = dfLNT_012_L['FR'].Histo1D(('whd_012_%s_FR'%v,'whd_012_%s_FR'%v, VARS[v][0], VARS[v][1]), VARS[v][2], 'lnt_012_evt_wht')

            if subtract == True: _H_WHD_012[v]['Conv'] = dfLNTConv_012.Histo1D(('whd_012_%s_Conv'%v,'whd_012_%s_Conv'%v, VARS[v][0], VARS[v][1]), VARS[v][2], 'lnt_012_evt_wht')
            if len(KEYS) == 1:   _H_OBS_012[v]['data'] = dfT_012.Histo1D(('obs_012_%s'%v,'obs_012_%s'%v, VARS[v][0], VARS[v][1]), VARS[v][2], 't_012_evt_wht')

            if len(KEYS) > 1:
                for DF in dfT_012_L.keys():
                    _H_OBS_012[v][DF] = dfT_012_L[DF].Histo1D(('obs_012_%s_%s'%(v,DF),'obs_012_%s_%s'%(v,DF), VARS[v][0], VARS[v][1]), VARS[v][2], 't_012_evt_wht')

    for v in VARS.keys():
#        if v not in ['BGM_01', 'BGM_02', 'dr_01', 'dr_02']: continue
        for df in keys:
            H_WHD_012[v][df] = rt.TH1F('whd_012_%s_%s'%(v,df),'whd_012_%s_%s'%(v,df), VARS[v][0], VARS[v][1])
            H_WHD_021[v][df] = rt.TH1F('whd_021_%s_%s'%(v,df),'whd_021_%s_%s'%(v,df), VARS[v][0], VARS[v][1])

        for DF in KEYS:
            H_OBS_012[v][DF] = rt.TH1F('obs_012_%s_%s'%(v,DF),'obs_012_%s_%s'%(v,DF), VARS[v][0], VARS[v][1])           
            H_OBS_021[v][DF] = rt.TH1F('obs_021_%s_%s'%(v,DF),'obs_021_%s_%s'%(v,DF), VARS[v][0], VARS[v][1])           
        
        if mode012 == True:
            VARS ['pt'] = [len(b_pt)-1,     b_pt,     'ptcone012'      , ';p_{T}^{cone} [GeV]; Counts']
            if fr == True: 
                print '\n\tDrawing: 012', v, 'weighted FR'
                H_WHD_012[v]['FR']   = _H_WHD_012[v]['FR'].GetPtr()
            if len(keys) > 1:
                print '\n\tDrawing: 012', v, 'weighted Conv'
                H_WHD_012[v]['Conv'] = _H_WHD_012[v]['Conv'].GetPtr()
            for DF in dfT_012_L.keys():
                _H_OBS_012[v][DF] = dfT_012_L[DF].Histo1D(('obs_012_%s_%s'%(v,DF),'obs_012_%s_%s'%(v,DF), VARS[v][0], VARS[v][1]), VARS[v][2], 't_012_evt_wht')
                print '\n\tDrawing: 012', v, DF
                H_OBS_012[v][DF]  = _H_OBS_012[v][DF].GetPtr()

        if mode021 == True:
            VARS ['pt'] = [len(b_pt)-1,     b_pt,     'ptcone021'      , ';p_{T}^{cone} [GeV]; Counts']
            if v not in ['BGM_01', 'BGM_02', 'dr_01', 'dr_02']: V = v
            if v == 'BGM_01': V = 'BGM_02'
            if v == 'BGM_02': V = 'BGM_01'
            if v == 'dr_01':  V = 'dr_02'
            if v == 'dr_02':  V = 'dr_01'
            if fr == True: 
                print '\n\tDrawing: 021', V, 'weighted FR'
                H_WHD_021[V]['FR']   = _H_WHD_021[V]['FR'].GetPtr()
            if len(keys) > 1:
                print '\n\tDrawing: 021', V, 'weighted Conv'
                H_WHD_021[V]['Conv'] = _H_WHD_021[V]['Conv'].GetPtr()
            for DF in dfT_021_L.keys():
                try: _H_OBS_021[v][DF] = dfT_021_L[DF].Histo1D(('obs_021_%s_%s'%(V,DF),'obs_021_%s_%s'%(V,DF), VARS[V][0], VARS[V][1]), VARS[V][2], 't_021_evt_wht')
                except: sys.stdout = sys.__stdout__; sys.stderr = sys.__stderr__; set_trace()
                print '\n\tDrawing: 021', V, DF
                H_OBS_021[V][DF]  = _H_OBS_021[V][DF].GetPtr()

    #for v in VARS.keys():
        # STACK COLORS            
        col = OrderedDict() 
        col['data']    = rt.kBlack;        col['IntConv'] = rt.kRed+1
        col['TT']      = rt.kBlue+1;       col['ExtConv'] = rt.kCyan+1  
        col['DYbb']    = rt.kRed+1;        col['Conv']    = rt.kCyan+1
        col['DY50']    = rt.kYellow+1;     col['whd']     = rt.kGreen+1 
        
        if fr == True:
            if v not in ['BGM_01', 'BGM_02', 'dr_01', 'dr_02']: H_WHD_012[v]['FR'].Add(H_WHD_021[v]['FR'])
            if v == 'BGM_01':                                   H_WHD_012['BGM_01']['FR'].Add(H_WHD_021['BGM_02']['FR'])
            if v == 'BGM_02':                                   H_WHD_012['BGM_02']['FR'].Add(H_WHD_021['BGM_01']['FR'])
            if v == 'dr_01':                                    H_WHD_012['dr_01']['FR'].Add(H_WHD_021['dr_02']['FR'])
            if v == 'dr_02':                                    H_WHD_012['dr_02']['FR'].Add(H_WHD_021['dr_01']['FR'])
            H_WHD_012[v]['FR'].SetFillColor(col['whd'])
            H_WHD_012[v]['FR'].SetLineColor(rt.kBlack)
            H_WHD_012[v]['FR'].SetMarkerSize(0)
            H_WHD_012[v]['FR'].SetMarkerColor(rt.kBlack)

        if isData == False: obs = H_OBS_012[v]['DY50'] 
        if isData == True:  obs = H_OBS_012[v]['data'] 

        if subtract == True:
            if v not in ['BGM_01', 'BGM_02', 'dr_01', 'dr_02']: H_WHD_012[v]['Conv'].Add(H_WHD_021[v]['Conv'])
            if v == 'BGM_01':                                   H_WHD_012['BGM_01']['Conv'].Add(H_WHD_021['BGM_02']['Conv'])
            if v == 'BGM_02':                                   H_WHD_012['BGM_02']['Conv'].Add(H_WHD_021['BGM_01']['Conv'])
            if v == 'dr_01':                                    H_WHD_012['dr_01']['Conv'].Add(H_WHD_021['dr_02']['Conv'])
            if v == 'dr_02':                                    H_WHD_012['dr_02']['Conv'].Add(H_WHD_021['dr_01']['Conv'])
            if verbose: print '\n\tConv whd entries b4 weighting:', H_WHD_012[v]['Conv'].GetEntries()
            H_WHD_012[v]['Conv'].Scale(DY_SCALE)      ## SCALING MC
            if verbose: print '\n\tConv whd entries after weighting:', H_WHD_012[v]['Conv'].GetEntries()
            if verbose: print '\n\tFR whd entries b4 subtracting:', H_WHD_012[v]['FR'].GetEntries()
            H_WHD_012[v]['FR'].Add(H_WHD_012[v]['Conv'], -1.)
            if verbose: print '\n\tFR whd entries after subtracting:', H_WHD_012[v]['FR'].GetEntries()

        whd = rt.THStack('whd_%s'%v,'whd_%s'%v)
        
        for DF in KEYS:
            if dfr:
                H_OBS_012[v][DF].Add(H_OBS_021[v][DF])
            if sfr:
                if v not in ['BGM_01', 'BGM_02', 'dr_01', 'dr_02']: H_OBS_012[v][DF].Add(H_OBS_021[v][DF])
                if v == 'BGM_01':                                   H_OBS_012['BGM_01'][DF].Add(H_OBS_021['BGM_02'][DF])
                if v == 'BGM_02':                                   H_OBS_012['BGM_02'][DF].Add(H_OBS_021['BGM_01'][DF])
                if v == 'dr_01':                                    H_OBS_012['dr_01'][DF].Add(H_OBS_021['dr_02'][DF])
                if v == 'dr_02':                                    H_OBS_012['dr_02'][DF].Add(H_OBS_021['dr_01'][DF])
            if not DF == 'DY50' and not DF == 'data':
                H_OBS_012[v][DF].SetFillColor(col[DF])
                H_OBS_012[v][DF].SetLineColor(rt.kBlack)
                H_OBS_012[v][DF].SetMarkerSize(0)
                H_OBS_012[v][DF].SetMarkerColor(rt.kBlack)
        #H_OBS_012[v]['TT'].Scale(TT_SCALE)  ## SCALING MC
        #whd.Add(H_OBS_012[v]['TT'])

        if CONV == True: 
            H_OBS_012[v]['Conv'].Scale(DY_SCALE)  ## SCALING MC
            whd.Add(H_OBS_012[v]['Conv'])

        if fr == True:
            whd.Add(H_WHD_012[v]['FR'])

        if v == 'pt':
            n_obs = 0; n_whd = 0
            for DF in KEYS: 
                print '\n\t', DF, H_OBS_012[v][DF].GetEntries() 
                n_obs += H_OBS_012[v][DF].GetEntries()
            for df in keys: 
                print '\n\t', df, H_WHD_012[v][df].GetEntries() 
                n_whd += H_WHD_012[v][df].GetEntries()
            print '\n\tyields. weighted: %0.2f, not weighted: %0.2f' %(n_whd, n_obs)

        ##SCALING CANVAS
        ymax = whd.GetMaximum()
        if obs.GetMaximum() > ymax: ymax = obs.GetMaximum()
        ymax *= 1.4; obs.GetYaxis().SetRangeUser(0.01, ymax)
 
        c = rt.TCanvas(v, v); c.cd()
        whd.SetTitle(VARS[v][3])
        obs.SetTitle(VARS[v][3])
        if isData == False: obs.SetMarkerColor(rt.kMagenta+2)
        obs.Draw()
        whd.Draw('histEsame')
        obs.Draw('same')
        leg = rt.TLegend(0.57, 0.78, 0.80, 0.9)
        if CONV == False: 
            leg.AddEntry(obs, 'observed')
        if CONV == True: 
            for DF in KEYS:
                if not DF == 'DY50' and not DF == 'data': leg.AddEntry(H_OBS_012[v][DF], DF)
                if isData == False:
                    if DF == 'DY50': leg.AddEntry(H_OBS_012[v][DF], 'observed')
                if isData == True:
                    if DF == 'data': leg.AddEntry(H_OBS_012[v][DF], 'observed')
        if fr == True: 
            leg.AddEntry(H_WHD_012[v]['FR'], 'expected SFR')
        leg.Draw()
        pf.showlogoprelimsim('CMS')
        pf.showlumi('SFR_'+ch)
        save(knvs=c, sample='DDE', ch=ch, DIR=plotDir)

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
        data           =   [data_B_eee, data_C_eee, data_D_eee, data_E_eee, data_F_eee]

        DFR_T          =   ''
        DFR_L          =   ''
        DFR_LNT        =   ''

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
        data           =   [data_B_eem, data_C_eem, data_D_eem, data_E_eem, data_F_eem]

        DFR_T          =   ''
        DFR_L          =   ''
        DFR_LNT        =   ''

        SFR_012_L       =  SFR_EEM_012_L  
        SFR_012_LNT     =  SFR_EEM_012_LNT
        SFR_012_T       =  SFR_EEM_012_T  
        SFR_021_L       =  ''
        SFR_021_LNT     =  ''
        SFR_021_T       =  ''


    if channel == 'mem':
        DYBB_dir       =   DYBBDir_mem     
        DY10_dir       =   DY10Dir_mem      
        DY50_dir       =   DY50Dir_mem      
        DY50_ext_dir   =   DY50_extDir_mem 
        W_dir          =   W_dir_mem
        W_ext_dir      =   W_ext_dir_mem
        TT_dir         =   TT_dir_mem
        data           =   [data_B_mem, data_C_mem, data_D_mem, data_E_mem, data_F_mem]

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
        data           =   [data_B_mmm, data_C_mmm, data_D_mmm, data_E_mmm, data_F_mmm]

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
    dirs = [DYBB_dir, DY10_dir, DY50_dir, DY50_ext_dir, TT_dir, W_dir, W_ext_dir, data] 

    return SFR, DFR, dirs 
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
    knvs.SetLogy()
    knvs.SaveAs('{dr}{smpl}_{ch}_{ttl}_log.png' .format(dr=DIR, smpl=sample, ttl=knvs.GetTitle(), ch=ch))
    knvs.SaveAs('{dr}{smpl}_{ch}_{ttl}_log.pdf' .format(dr=DIR, smpl=sample, ttl=knvs.GetTitle(), ch=ch))

######################################################################################

######################################################################################
class nn(object):

    def __init__(self):
        np.random.seed(1986)
        self.branches = [
        #     'event',        
        #     'lumi',        
        #     'run',        
        #     'TIGHT',        
             'l2_abs_eta',        
             'l2_ptcone',        
             'l2_abs_dxy',        
        #     'l2_dz',        
        ]

        self.features = self.branches

        classifier_input  = Input((len(self.branches),))
        #classifier_dense1 = Dense(64, activation='tanh'   )(classifier_input )
        #classifier_dense2 = Dense(64, activation='relu'   )(classifier_dense1)
        classifier_dense1 = Dense(128, activation='tanh'  )(classifier_input)
        # R: use 64 and relu --> should get K = 1
        classifier_output = Dense( 1, activation='sigmoid')(classifier_dense1)

        self.classifier = Model(classifier_input, classifier_output)
        self.classifier.compile('Adam', loss='binary_crossentropy', loss_weights=[1])        
        plot_model(self.classifier, show_shapes=True, show_layer_names=True, to_file=saveDir+'classifier.png')

        self.ndf_training_half        = root2array(saveDir+'data_mmm_6_24B_training_half.root' , 'tree')
        self.ndf_training_half_LOOSE  = root2array(saveDir+'data_mmm_6_24B_training_half.root' , 'tree', selection='LOOSE == 1')
        self.ndf_untouched_half       = root2array(saveDir+'data_mmm_6_24B_untouched_half.root', 'tree')

        self.data_train_l = pd.DataFrame( self.ndf_training_half_LOOSE )
        self.data_train   = pd.DataFrame( self.ndf_training_half       )
        self.data_untouch = pd.DataFrame( self.ndf_untouched_half      )
 
        self.data_untouch['l2_ptcone']  = self.data_untouch.l2_pt * (1 + np.maximum(0, self.data_untouch.l2_reliso_rho_03 - 0.2) )
        self.data_untouch['l2_abs_eta'] = np.abs(self.data_untouch.l2_eta) 
        self.data_untouch['l2_abs_dxy'] = np.abs(self.data_untouch.l2_dxy)

        self.data_train_l['l2_ptcone']  = self.data_train_l.l2_pt * (1 + np.maximum(0, self.data_train_l.l2_reliso_rho_03 - 0.2) )
        self.data_train_l['l2_abs_eta'] = np.abs(self.data_train_l.l2_eta) 
        self.data_train_l['l2_abs_dxy'] = np.abs(self.data_train_l.l2_dxy)
        
        self.data_train['l2_ptcone']  = self.data_train.l2_pt * (1 + np.maximum(0, self.data_train.l2_reliso_rho_03 - 0.2) )
        self.data_train['l2_abs_eta'] = np.abs(self.data_train.l2_eta) 
        self.data_train['l2_abs_dxy'] = np.abs(self.data_train.l2_dxy)

        self.data_train_l = self.data_train_l.sample(frac=1, replace=True, random_state=1986)

        self.X = pd.DataFrame(self.data_train_l, columns=self.branches)
        self.Y = pd.DataFrame(self.data_train_l, columns=['TIGHT'])


    def train(self):
        print ('training classifier')
        self.classifier.fit(self.X, self.Y, epochs=10, validation_split=0.3)  
        self.classifier.save(saveDir+'net_6_26B_Lcut_06_5.h5')

        # add the score to the data_train_l sample
        print ('normalizing...')
        set_trace()
        Y = self.classifier.predict(self.X)
        self.data_train_l.insert(len(self.data_train_l.columns), 'score', Y)
        k = np.sum(self.data_train_l.score)
        T = np.count_nonzero(self.data_train_l.TIGHT)
        self.K = T/k 
        print(k, T, self.K)


    def predict(self):
    # calculate predictions on the data_train_l sample
        print ('predicting on', self.data_train.shape[0], 'events')
        x_train   = pd.DataFrame(self.data_train,   columns=self.features)
        x_untouch = pd.DataFrame(self.data_untouch, columns=self.features)
        y_train   = self.classifier.predict(x_train  )
        y_untouch = self.classifier.predict(x_untouch)

        self.K = 1

        self.data_train  .insert(len(self.data_train.columns),   'ml_fr', self.K * y_train  )
        self.data_untouch.insert(len(self.data_untouch.columns), 'ml_fr', self.K * y_untouch)

        roc = False
        if roc == True:
            fpr, tpr, wps = roc_curve(self.data_train.TIGHT, self.data_train.score)

            plt.xscale('log')
            plt.plot(fpr, tpr, color='m', label=r'Z=$\mathcal{N}(0, 1)$')
            xy = [i*j for i,j in product([10.**i for i in range(-2, 0)], [1,2,4,8])]+[1]
            plt.plot(xy, xy, color='grey', linestyle='--')

            plt.xlabel(r'Loose')
            plt.ylabel(r'Tight')
            plt.xlim([0.0, 1.0])
            plt.ylim([0.0, 1.0])

            plt.grid(True)
            plt.legend(loc='lower right')
            plt.savefig('roc.pdf')
            plt.clf()

        self.data_train  .to_root(saveDir+'data_mmm_6_26B_Lcut_06_5_Keq1_training_half_output.root',  key = 'tree')
        self.data_untouch.to_root(saveDir+'data_mmm_6_26B_Lcut_06_5_Keq1_untouched_half_output.root', key = 'tree')

    def checkFakeRate(self,file_name='data_6_24'):

        tfile1 = rt.TFile(saveDir+'data_6_18_training_half_output.root')
        #tfile2 = rt.TFilesaveDir+''%s_untouched_half_output.root'%file_name)
        tfile2 = rt.TFile(saveDir+'data_eem_6_19_output.root')

        tree1 = tfile1.Get('tree')
        tree2 = tfile2.Get('tree')

        tree1.Draw('score>>SCORE_T_trained(100,0,1)',   'TIGHT==1')
        tree1.Draw('score>>SCORE_LNT_trained(100,0,1)', 'TIGHT==0')
        tree2.Draw('score>>SCORE_T_free(100,0,1)',   'TIGHT==1')
        tree2.Draw('score>>SCORE_LNT_free(100,0,1)', 'TIGHT==0')

        h_T_trained   = rt.gDirectory.Get('SCORE_T_trained')
        h_LNT_trained = rt.gDirectory.Get('SCORE_LNT_trained')
        h_T_free   = rt.gDirectory.Get('SCORE_T_free')
        h_LNT_free = rt.gDirectory.Get('SCORE_LNT_free')

        h_T_trained.SetLineColor(rt.kRed+2)
        h_LNT_trained.SetLineColor(rt.kGreen+2)
        h_T_free.SetLineColor(rt.kRed+2)
        h_LNT_free.SetLineColor(rt.kGreen+2)

        c1 = rt.TCanvas('training_half','training_half'); c1.cd()
        h_LNT_trained.SetAxisRange(0.0,0.3,'X')
        h_LNT_trained.SetTitle('')
        h_T_trained.SetTitle('')
        h_LNT_trained.DrawNormalized()
        h_T_trained.DrawNormalized('same')
        c1.BuildLegend(0.5,0.5,0.9,0.75)
        c1.SaveAs(saveDir+'training_half.root')
        c1.SaveAs(saveDir+'training_half.pdf')

        c2 = rt.TCanvas('untouched_half','untouched_half'); c2.cd()
        h_LNT_free.SetAxisRange(0.0,0.3,'X')
        h_LNT_free.SetTitle('')
        h_T_free.SetTitle('')
        h_LNT_free.DrawNormalized()
        h_T_free.DrawNormalized('same')
        c2.BuildLegend(0.5,0.5,0.9,0.75)
        c2.SaveAs(saveDir+'untouched_half.root')
        c2.SaveAs(saveDir+'untouched_half.pdf')

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
    today = datetime.now(); date = today.strftime('%y%m%d'); hour = str(today.hour); minit = str(today.minute)
    plotDir = plotDir + name + '_' + date + '_' + hour + 'h_' + minit + 'm/'
    os.mkdir(plotDir)
    return plotDir

def makeLabel(sample_dir, ch='mmm', lbl='1',era='B'):
    '''create a label (friend) tree for a respective sample
       use the following: data: 0, DY: 1, TT: 2, WJ: 3''' 
    if lbl != '0': era = ''
    fin = rt.TFile(sample_dir+suffix)
    tr = fin.Get('tree')
    ldf = rdf(tr)
    df = ldf.Define('label', lbl)
    bL = rt.vector('string')()
    for br in ['event', 'lumi', 'label']:
        bL.push_back(br)
    df.Snapshot('tree', plotDir + 'friend_tree_label_%s_%s%s.root'%(ch,lbl,era), bL)

