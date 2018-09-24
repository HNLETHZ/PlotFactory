from __future__ import division
import ROOT as rt
import numpy as np
import plotfactory as pf
from glob import glob
import sys
from pdb import set_trace
from os.path import normpath, basename, split
from collections import OrderedDict
from multiprocessing import Pool
#from CMGTools.HNL.plotting.plot_cfg_mu import threeMuAtZ
####################################################################################################
outdir = '/eos/user/v/vstampf/plots/DDE/'
indir  = '/afs/cern.ch/work/v/vstampf/public/ntuples/DD_estimates/'
m_dir  = 'prompt_m/'
e_dir  = 'prompt_e/'
suffix = 'HNLTreeProducer/tree.root'
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
W_dir_m              = 'prompt_m/WJetsToLNu/'
W_ext_dir_m          = 'prompt_m/WJetsToLNu_ext/'
####################################################################################################
samples =  [W_dir_e, W_ext_dir_e, TT_dir_e, DYBB_dir_e, DY50_dir_e, DY10to50_ext_dir_e,]# DY10to50_dir_e,] <-- # TODO SOME ERROR # DY50_ext_dir_e] #NOT YET PROCESSED
samples += [W_dir_m, W_ext_dir_m, TT_dir_m, DYBB_dir_m, DY50_dir_m, DY10to50_ext_dir_m, DY10to50_dir_m,]# DY50_ext_dir_m]
####################################################################################################
## CUTS ##
####################################################################################################
disp0p5     = 'hnl_2d_disp > 0.5'
disp1       = 'hnl_2d_disp > 1'
M10         = 'hnl_m_01 > 10  &&  hnl_m_02 > 10  &&  hnl_m_12 > 10'
tt_disp_bj1 = disp0p5 + '  &&  nbj > 0'
####################################################################################################
threeMu_pt_rlxd =   'l1_pt > 20  &&  l2_pt > 4  &&  l0_pt > 4'\
                '  &&  abs(l0_dz) < 0.2 &&  abs(l1_dz) < 0.2 &&  abs(l2_dz) < 0.2 '\
                '  &&  abs(l0_dxy) < 0.045 &&  abs(l1_dxy) < 0.045 &&  abs(l2_dxy) < 0.045 '\
                '  && l0_id_m && l1_id_m && l2_id_m '\
                '  && abs(l0_eta) < 2.4 && abs(l1_eta) < 2.4 && abs(l2_eta) < 2.4 '\
                '  && l0_reliso05 < 0.1 && l1_reliso05 < 0.1 && l2_reliso05 < 0.1 '\
                '  && hnl_dr_01 > 0.05 && hnl_dr_02 > 0.05 && hnl_dr_12 > 0.05 '
####################################################################################################
threeMu         =   'l1_pt > 20  &&  l2_pt > 10  &&  l0_pt > 27'\
                '  &&  abs(l0_dz) < 0.2 &&  abs(l1_dz) < 0.2 &&  abs(l2_dz) < 0.2 '\
                '  &&  abs(l0_dxy) < 0.045 &&  abs(l1_dxy) < 0.045 &&  abs(l2_dxy) < 0.045 '\
                '  && l0_id_m && l1_id_m && l2_id_m '\
                '  && abs(l0_eta) < 2.4 && abs(l1_eta) < 2.4 && abs(l2_eta) < 2.4 '\
                '  && l0_reliso05 < 0.1 && l1_reliso05 < 0.1 && l2_reliso05 < 0.1 '\
                '  && hnl_dr_01 > 0.05 && hnl_dr_02 > 0.05 && hnl_dr_12 > 0.05 '
####################################################################################################
mltlst = [ ##  sample          , cuts 
            [W_dir_e           , '1'],
            [W_ext_dir_e       , '1'],
            [TT_dir_e          , '1'], 
            [DYBB_dir_e        , '1'],
            [DY50_dir_e        , '1'], 
            [DY10to50_ext_dir_e, '1'],
            [W_dir_m           , '1'],
            [W_ext_dir_m       , '1'],
            [TT_dir_m          , '1'], 
            [DYBB_dir_m        , '1'],
            [DY50_dir_m        , '1'], 
            [DY10to50_ext_dir_m, '1'],
            [DY10to50_dir_m    , '1'],
            [TT_dir_e          , tt_disp_bj1], 
            [TT_dir_m          , tt_disp_bj1], 
            [DY50_dir_m        , threeMu],
            [DY10to50_dir_m    , threeMu_pt_rlxd],
            [DY10to50_ext_dir_m, threeMu_pt_rlxd],]
####################################################################################################
## FAKES / PROMPT ##
####################################################################################################
in_acc = 'prompt_e/abs(l0_eta) < 2.4  &&  abs(l2_eta) < 2.4  &&  abs(l2_eta) < 2.4'

#l1_prompt_dr = 'prompt_e/l1_gen_match_fromHardProcessFinalState == 1  ||  l1_gen_match_isPromptFinalState == 1'
#l2_prompt_dr = 'prompt_e/l2_gen_match_fromHardProcessFinalState == 1  ||  l2_gen_match_isPromptFinalState == 1'
#at_least_one_prompt_dr = 'prompt_e/(' + l1_prompt_dr + ')  ||  (' + l2_prompt_dr + ')'
#two_prompt_dr = 'prompt_e/(' + l1_prompt_dr + ')  &&  (' + l2_prompt_dr + ')'

l1_prompt = 'l1_simType == 4'
l2_prompt = 'l2_simType == 4'

l1_fake = 'l1_simType != 4'
l2_fake = 'l2_simType != 4'

l1f_l2p = l1_fake + ' && ' + l2_prompt 
l2f_l1p = l2_fake + ' && ' + l1_prompt 

two_prompt         = '(' + l1_prompt + ' && ' + l2_prompt + ')'
one_fake_xor       = '(' + l1f_l2p   + ' || ' + l2f_l1p   + ')' 
two_fakes          = '(' + l1_fake   + ' && ' + l2_fake   + ')'  
two_fakes_same_vtx = '(' + two_fakes + ' && l2_simProdZ == l1_simProdZ)'  

no_fakes = two_prompt
####################################################################################################
def countFakesWithoutCuts(sample_dir):
    ch = basename(split(normpath(sample_dir))[0]) 
    name = basename(normpath(sample_dir))
    fin = rt.TFile(indir + sample_dir + suffix)
    t = fin.Get('tree')
    n_entries            = t.GetEntriesFast() 
    n_one_fake_xor       = t.GetEntries(one_fake_xor)
    n_two_fakes          = t.GetEntries(two_fakes)
    n_two_fakes_same_vtx = t.GetEntries(two_fakes_same_vtx)
    print name + '_%s\n\t entries \t\t'%ch, '100.0% \t'                                        , n_entries 
    print '\t one_fake_xor \t\t'          , '{:.1%} \t'.format(n_one_fake_xor/n_entries)       , n_one_fake_xor      
    print '\t two_fakes \t\t'             , '{:.1%} \t'.format(n_two_fakes/n_entries)          , n_two_fakes         
    print '\t two_fakes_same_vtx \t'      , '{:.1%} \t'.format(n_two_fakes_same_vtx/n_entries) , n_two_fakes_same_vtx
    print ''
        
def countFakes(tupel):
    sample_dir, cuts = tupel
    ch = basename(split(normpath(sample_dir))[0]) 
    name = basename(normpath(sample_dir))
    fin = rt.TFile(indir + sample_dir + suffix)
    t = fin.Get('tree')
    n_entries            = t.GetEntries(cuts) 
    n_no_fakes           = t.GetEntries(cuts + ' && ' + no_fakes)
    n_one_fake_xor       = t.GetEntries(cuts + ' && ' + one_fake_xor)
    n_two_fakes          = t.GetEntries(cuts + ' && ' + two_fakes)
    n_two_fakes_same_vtx = t.GetEntries(cuts + ' && ' + two_fakes_same_vtx)

    if len(cuts) > 2: name += '_' + cuts[0:3]
    sys.stdout = open(outdir + name + '_%s'%ch + '.py', 'w+')

    print name + '_%s \ncuts:\t%s '%(ch, cuts)
    print '\t entries \t\t'               , '100.0% \t'                                        , n_entries 
    print '\t no_fakes \t\t'              , '{:.1%} \t'.format(n_no_fakes/n_entries)           , n_no_fakes      
    print '\t one_fake_xor \t\t'          , '{:.1%} \t'.format(n_one_fake_xor/n_entries)       , n_one_fake_xor      
    print '\t two_fakes \t\t'             , '{:.1%} \t'.format(n_two_fakes/n_entries)          , n_two_fakes         
    print '\t two_fakes_same_vtx \t'      , '{:.1%} \t'.format(n_two_fakes_same_vtx/n_entries) , n_two_fakes_same_vtx
    print ''
    
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__
    
    print name + '_%s\t\t done'%ch
####################################################################################################
pf.setpfstyle()

print '\n'
pool = Pool(processes=len(mltlst))
print('number of processes for filling histos (ie. samples): %i'%len(mltlst))
pool.map(countFakes, mltlst) 
####################################################################################################
