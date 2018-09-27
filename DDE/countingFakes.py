from __future__ import division
from ROOT import gROOT as gr
import ROOT as rt
import numpy as np
import plotfactory as pf
from glob import glob
import sys
from pdb import set_trace
from os.path import normpath, basename, split
from collections import OrderedDict
from multiprocessing import Pool
gr.SetBatch(True) # NEEDS TO BE SET FOR MULTIPROCESSING OF plot.Draw()
pf.setpfstyle()
####################################################################################################
outdir = '/eos/user/v/vstampf/plots/DDE/tight_to_loose/'
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
                '  && l0_reliso05_03 < 0.1 && l1_reliso05_03 < 0.1 && l2_reliso05_03 < 0.1 '\
                '  && hnl_dr_01 > 0.05 && hnl_dr_02 > 0.05 && hnl_dr_12 > 0.05 '
####################################################################################################
threeMu         =   'l1_pt > 20  &&  l2_pt > 10  &&  l0_pt > 27'\
                '  &&  abs(l0_dz) < 0.2 &&  abs(l1_dz) < 0.2 &&  abs(l2_dz) < 0.2 '\
                '  &&  abs(l0_dxy) < 0.045 &&  abs(l1_dxy) < 0.045 &&  abs(l2_dxy) < 0.045 '\
                '  && l0_id_m && l1_id_m && l2_id_m '\
                '  && abs(l0_eta) < 2.4 && abs(l1_eta) < 2.4 && abs(l2_eta) < 2.4 '\
                '  && l0_reliso05_03 < 0.1 && l1_reliso05_03 < 0.1 && l2_reliso05_03 < 0.1 '\
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
            [DY10to50_ext_dir_m, threeMu_pt_rlxd],
        ]
####################################################################################################
## FAKES / PROMPT ##
####################################################################################################
in_acc = 'abs(l0_eta) < 2.4  &&  abs(l2_eta) < 2.4  &&  abs(l2_eta) < 2.4'

l0_prompt_m_dr = '( (l0_gen_match_fromHardProcessFinalState == 1 || l0_gen_match_isPromptFinalState == 1) && abs(l0_gen_match_pdgid) == 13 )'
l0_prompt_e_dr = '( (l0_gen_match_fromHardProcessFinalState == 1 || l0_gen_match_isPromptFinalState == 1) && abs(l0_gen_match_pdgid) == 11 )'
l1_prompt_dr   = '( (l1_gen_match_fromHardProcessFinalState == 1 || l1_gen_match_isPromptFinalState == 1) && abs(l0_gen_match_pdgid) == 13 )'
l2_prompt_dr   = '( (l2_gen_match_fromHardProcessFinalState == 1 || l2_gen_match_isPromptFinalState == 1) && abs(l0_gen_match_pdgid) == 13 )'

l0_fake_m_dr = '( !' + l0_prompt_m_dr + ')'  #'( (l0_gen_match_fromHardProcessFinalState == 0 && l0_gen_match_isPromptFinalState == 0) || abs(l0_gen_match_pdgid) != 13 )'
l0_fake_e_dr = '( !' + l0_prompt_e_dr + ')'  #'( (l0_gen_match_fromHardProcessFinalState == 0 && l0_gen_match_isPromptFinalState == 0) || abs(l0_gen_match_pdgid) != 11 )'
l1_fake_dr   = '( !' + l1_prompt_dr   + ')' 
l2_fake_dr   = '( !' + l2_prompt_dr   + ')' 

#at_least_one_prompt_dr = '(' + l1_prompt_dr + ')  ||  (' + l2_prompt_dr + ')'
#two_prompt_dr = '(' + l1_prompt_dr + ')  &&  (' + l2_prompt_dr + ')'

l0_prompt = '( l0_simType == 4 || (l0_simType == 3 && l0_simFlavour == 15) )'
l1_prompt = '( l1_simType == 4 || (l1_simType == 3 && l1_simFlavour == 15) )'
l2_prompt = '( l2_simType == 4 || (l2_simType == 3 && l2_simFlavour == 15) )'

l0_fake = '( ! ' + l0_prompt + ' )' #(l0_simType != 4)'# & abs(l0_simType) < 1001)'
l1_fake = '( ! ' + l1_prompt + ' )' #'(l1_simType != 4)'# & abs(l1_simType) < 1001)'
l2_fake = '( ! ' + l2_prompt + ' )' #'(l2_simType != 4)'# & abs(l2_simType) < 1001)'

l1_heavyfake = 'l1_simType == 3'
l2_heavyfake = 'l2_simType == 3'

l1f_l2p     = '(' + l1_fake    + ' && ' + l2_prompt    + ')'
l2f_l1p     = '(' + l2_fake    + ' && ' + l1_prompt    + ')'
l1f_l2p_dr  = '(' + l1_fake_dr + ' && ' + l2_prompt_dr + ')'
l2f_l1p_dr  = '(' + l2_fake_dr + ' && ' + l1_prompt_dr + ')'
l1f_l2p_l0p = '(' + l1f_l2p    + ' && ' + l0_prompt    + ')'
l2f_l1p_l0p = '(' + l2f_l1p    + ' && ' + l0_prompt    + ')'

l1hf_l2p     = '(' + l1_heavyfake + ' && ' + l2_prompt + ')'
l2hf_l1p     = '(' + l2_heavyfake + ' && ' + l1_prompt + ')'
l1hf_l2p_l0p = '(' + l1hf_l2p     + ' && ' + l0_prompt + ')'
l2hf_l1p_l0p = '(' + l2hf_l1p     + ' && ' + l0_prompt + ')'

l1_LVtx_dr  = '( abs(l1_gen_match_vtx_x) + abs(l1_gen_match_vtx_y) + abs(l1_gen_match_vtx_z) )'
l2_LVtx_dr  = '( abs(l2_gen_match_vtx_x) + abs(l2_gen_match_vtx_y) + abs(l2_gen_match_vtx_z) )'

DeltaLVtx = '( ' + l1_LVtx_dr + ' - ' + l2_LVtx_dr + ' )' 
SumLVtx   = '( ' + l1_LVtx_dr + ' + ' + l2_LVtx_dr + ' )'

#sameVtx_dr = '( ( 2 *( ' + l1_vtx_dr + ' - ' + l2_vtx_dr + ' ) / ( ' + l1_vtx_dr + ' + ' + l2_vtx_dr + ' ) ) < 0.01 )'
#sameVtx_dr = '( ( ' + DeltaLVtx + ' / ' + SumLVtx + ' ) < 0.005 )'
sameVtx_dr = '( ' + DeltaLVtx + ' == 0 )'

two_prompt            = '(' + l1_prompt     + ' && ' + l2_prompt      +  ')'
two_prompt_dr         = '(' + l1_prompt_dr  + ' && ' + l2_prompt_dr   +  ')'
one_fake_xor          = '(' + l1f_l2p       + ' || ' + l2f_l1p        +  ')' 
one_fake_xor_dr       = '(' + l1f_l2p_dr    + ' || ' + l2f_l1p_dr     +  ')' 
two_fakes             = '(' + l1_fake       + ' && ' + l2_fake        +  ')'  
two_fakes_dr          = '(' + l1_fake_dr    + ' && ' + l2_fake_dr     +  ')'  
twoHeavyFakes         = '(' + l1_heavyfake  + ' && ' + l2_heavyfake   +  ')'  
twoFakes_sameVtx      = '(' + two_fakes     + ' && l2_simProdZ == l1_simProdZ && l1_simProdZ != 0)'  
twoFakes_sameVtx_dr   = '(' + two_fakes_dr  + ' && ' + sameVtx_dr     +  ')'
twoHeavyFakes_sameVtx = '(' + twoHeavyFakes + ' && l2_simProdZ == l1_simProdZ && l1_simProdZ != 0)'  

no_fakes    = two_prompt
no_fakes_dr = two_prompt_dr
sameJet     = '( l1_jet_pt == l2_jet_pt)'
twoFakes_sameVtx_sameJet        = '(' + twoFakes_sameVtx    + ' & ' + sameJet + ')' 
twoFakes_sameVtx_sameJet_l0p    = '(' + twoFakes_sameVtx    + ' & ' + sameJet + ' & ' + l0_prompt      + ')'
twoFakes_sameVtx_sameJet_l0p_dr = '(' + twoFakes_sameVtx_dr + ' & ' + sameJet + ' & ' + l0_prompt_m_dr + ')'

eta_0to1p2   = '( abs(l1_eta) < 1.2 & abs(l2_eta) < 1.2 )'
eta_1p2to2p1 = '( abs(l1_eta) > 1.2 & abs(l2_eta) > 1.2 & abs(l1_eta) < 2.1 & abs(l2_eta) < 2.1)'
eta_2p1to2p4 = '( abs(l1_eta) > 2.1 & abs(l2_eta) > 2.1 & abs(l1_eta) < 2.4 & abs(l2_eta) < 2.4)'

eta_bins = [['0_to_1p2'  , eta_0to1p2],
            ['1p2_to_2p1', eta_1p2to2p1],
            ['2p1_to_2p4', eta_2p1to2p4]]
####################################################################################################
def countFakesWithoutCuts(sample_dir):
    ch = basename(split(normpath(sample_dir))[0]) 
    name = basename(normpath(sample_dir))
    fin = rt.TFile(indir + sample_dir + suffix)
    t = fin.Get('tree')
    n_entries            = t.GetEntriesFast() 
    n_one_fake_xor       = t.GetEntries(one_fake_xor)
    n_two_fakes          = t.GetEntries(two_fakes)
    n_twoFakes_sameVtx = t.GetEntries(twoFakes_sameVtx)
    print name + '_%s\n\t entries \t\t'%ch, '100.0% \t'                                        , n_entries 
    print '\t one_fake_xor \t\t'          , '{:.1%} \t'.format(n_one_fake_xor/n_entries)       , n_one_fake_xor      
    print '\t two_fakes \t\t'             , '{:.1%} \t'.format(n_two_fakes/n_entries)          , n_two_fakes         
    print '\t twoFakes_sameVtx \t'        , '{:.1%} \t'.format(n_twoFakes_sameVtx/n_entries)   , n_twoFakes_sameVtx
    print ''
        
def countFakes(tupel):
    sample_dir, cuts = tupel
    ch = basename(split(normpath(sample_dir))[0]) 
    name = basename(normpath(sample_dir))
    fin = rt.TFile(indir + sample_dir + suffix)
    t = fin.Get('tree')
    n_entries             = t.GetEntries(cuts) 
    print name, n_entries
    if ch == 'prompt_m':
        n_l0_is_fake      = t.GetEntries(cuts + ' && ' + l0_fake)
        n_l0_is_fake_dr   = t.GetEntries(cuts + ' && ' + l0_fake_m_dr)
    if ch == 'prompt_e':
        n_l0_is_fake      = 0
        n_l0_is_fake_dr   = t.GetEntries(cuts + ' && ' + l0_fake_e_dr)
    print '\t l0_is_fake \t\t'            , '{:.1%} \t'.format(n_l0_is_fake/n_entries)                 , n_l0_is_fake     
    print '\t l0_is_fake_dr \t\t'         , '{:.1%} \t'.format(n_l0_is_fake_dr/n_entries)              , n_l0_is_fake_dr     
    n_no_fakes            = t.GetEntries(cuts + ' && ' + no_fakes)
    print '\t no_fakes \t\t'              , '{:.1%} \t'.format(n_no_fakes/n_entries)                   , n_no_fakes      
    n_no_fakes_dr         = t.GetEntries(cuts + ' && ' + no_fakes_dr)
    print '\t no_fakes_dr \t\t'           , '{:.1%} \t'.format(n_no_fakes_dr/n_entries)                , n_no_fakes_dr      
    n_one_fake_xor        = t.GetEntries(cuts + ' && ' + one_fake_xor)
    print '\t one_fake_xor \t\t'          , '{:.1%} \t'.format(n_one_fake_xor/n_entries)               , n_one_fake_xor      
    n_one_fake_xor_dr     = t.GetEntries(cuts + ' && ' + one_fake_xor_dr)
    print '\t one_fake_xor_dr \t'         , '{:.1%} \t'.format(n_one_fake_xor_dr/n_entries)            , n_one_fake_xor_dr      
    n_two_fakes           = t.GetEntries(cuts + ' && ' + two_fakes)
    print '\t two_fakes \t\t'             , '{:.1%} \t'.format(n_two_fakes/n_entries)                  , n_two_fakes         
    n_two_fakes_dr        = t.GetEntries(cuts + ' && ' + two_fakes_dr)
    print '\t two_fakes_dr\t\t'           , '{:.1%} \t'.format(n_two_fakes_dr/n_entries)               , n_two_fakes_dr         
    n_twoFakes_sameVtx    = t.GetEntries(cuts + ' && ' + twoFakes_sameVtx)
    print '\t twoFakes_sameVtx \t'        , '{:.1%} \t'.format(n_twoFakes_sameVtx/n_two_fakes)         , n_twoFakes_sameVtx   , '\t({:.1%})'.format(n_twoFakes_sameVtx/n_entries)
    n_twoFakes_sameVtx_dr = t.GetEntries(cuts + ' && ' + twoFakes_sameVtx_dr)
    print '\t twoFakes_sameVtx_dr\t'      , '{:.1%} \t'.format(n_twoFakes_sameVtx_dr/n_two_fakes_dr)   , n_twoFakes_sameVtx_dr, '\t({:.1%})'.format(n_twoFakes_sameVtx_dr/n_entries)

    if len(cuts) > 2: name += '_' + cuts[0:3]
    sys.stdout = open(outdir + name + '_%s'%ch + '.py', 'w+')

    print name + '_%s \ncuts:\t%s '%(ch, cuts)
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
    print '\t twoFakes_sameVtx_dr\t'      , '{:.1%} \t'.format(n_twoFakes_sameVtx_dr/n_two_fakes_dr)   , n_twoFakes_sameVtx_dr, '\t({:.1%})'.format(n_twoFakes_sameVtx_dr/n_entries)
    print ''
    
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__
    
    print name + '_%s\t\t done'%ch

def checkTTLratio(eta_bin):
    eta, eta_cut = eta_bin
    tupels = [[DY50_dir_m, '1'], [TT_dir_m, '1']] 
    h_pt_1f = []; i = 0
    for tupel in tupels: 
        iso_cut = 0.13
        sample_dir, cuts = tupel
        iso_str = str(int(iso_cut * 100))
    #    iso_str += '_stf=3'
        ch = basename(split(normpath(sample_dir))[0]) 
        name = basename(normpath(sample_dir))
        fin = rt.TFile(indir + sample_dir + suffix)
        t = fin.Get('tree')

        b_pt  = np.arange(5.,100,5)

        h_pt_l2_d  = rt.TH1F('pt_cone_l2_d', 'pt_cone_l2_d',len(b_pt)-1,b_pt)
        h_pt_l1_d  = rt.TH1F('pt_cone_l1_d', 'pt_cone_l1_d',len(b_pt)-1,b_pt)
        h_pt_2f_d  = rt.TH1F('pt_cone_2f_d', 'pt_cone_2f_d',len(b_pt)-1,b_pt)

        h_pt_l2_n  = rt.TH1F('pt_cone_l2_n', 'pt_cone_l2_n',len(b_pt)-1,b_pt)
        h_pt_l1_n  = rt.TH1F('pt_cone_l1_n', 'pt_cone_l1_n',len(b_pt)-1,b_pt)
        h_pt_2f_n  = rt.TH1F('pt_cone_2f_n', 'pt_cone_2f_n',len(b_pt)-1,b_pt)

        h_pt       = rt.TH1F('pt_cone'     , 'pt_cone'     ,len(b_pt)-1,b_pt)

        print 'drawing %s iso%s eta: %s ...'%(name, iso_str, eta)

        t.Draw(                              'l1_pt >> pt_cone_l1_n'        , l1hf_l2p_l0p + ' & l1_id_t & l1_reliso05_03 < %f & '%iso_cut + eta_cut)
        t.Draw('(l1_pt) * (1 + l1_reliso05_03 - %f) >> pt_cone_l1_d'%iso_cut, l1hf_l2p_l0p + ' & l1_id_t & l1_reliso05_03 > %f & l1_reliso05_03 < 1 & '%iso_cut + eta_cut)
    #    t.Draw(                          'l1_jet_pt >> pt_cone_l1_d'        , l1hf_l2p_l0p + ' & l1_id_t & l1_reliso05_03 > %f & l1_reliso05_03 < 1'%iso_cut)
        print '%s iso%s eta: %s ... l1 done'%(name, iso_str, eta)

        t.Draw(                              'l2_pt >> pt_cone_l2_n'        , l2hf_l1p_l0p + ' & l2_id_t & l2_reliso05_03 < %f & '%iso_cut + eta_cut)
        t.Draw('(l2_pt) * (1 + l2_reliso05_03 - %f) >> pt_cone_l2_d'%iso_cut, l2hf_l1p_l0p + ' & l2_id_t & l2_reliso05_03 > %f & l2_reliso05_03 < 1 & '%iso_cut + eta_cut)
    #    t.Draw(                          'l2_jet_pt >> pt_cone_l2_d'        , l2hf_l1p_l0p + ' & l2_id_t & l2_reliso05_03 > %f & l2_reliso05_03 < 1'%iso_cut)
        print '%s iso%s eta: %s ... l2 done'%(name, iso_str, eta)

        ## two fakes same vertex same jet
    #    t.Draw(      'l1_pt + l2_pt >> pt_cone_2f_n' , twoFakes_sameVtx_sameJet_l0p + ' & l1_id_t & l1_reliso05_03 < %f'%iso_cut)
    #    t.Draw(          'l1_jet_pt >> pt_cone_2f_d' , twoFakes_sameVtx_sameJet_l0p + ' & l1_id_t & l1_reliso05_03 > %f & l1_reliso05_03 < 1'%iso_cut)
    #    print 'iso%s eta: %s ... two fakes done'%(iso_str, eta)

        h_pt_l1_d.Add(h_pt_l1_n)
        h_pt_l2_d.Add(h_pt_l2_n)

        h_pt_l1_d.Add(h_pt_l2_d)
        h_pt_l1_n.Add(h_pt_l2_n)

        h_pt_2f_d.Add(h_pt_2f_n)

        h_pt_1f.append(rt.TEfficiency(h_pt_l1_n, h_pt_l1_d))
        h_pt_1f[i].SetTitle('%s ; p_{T}^{Cone} [GeV]; tigh-to-loose ratio (one fake)'%name)
        h_pt_1f[i].SetMarkerColor(rt.kGreen+i*2)

        c_pt_1f = rt.TCanvas('ptCone_1f', 'ptCone_1f')
        h_pt_1f[i].Draw()
        pf.showlogoprelimsim('CMS')
    #    pf.showTitle('iso_cut = 0.%s'%iso_str)
        pf.showTitle('eta: %s'%eta)
        c_pt_1f.Modified; c_pt_1f.Update()

        c_pt_1f.SaveAs(outdir + name + '_' + c_pt_1f.GetTitle() + '_%s_iso%s_eta%s.png' %(ch, iso_str, eta))
        c_pt_1f.SaveAs(outdir + name + '_' + c_pt_1f.GetTitle() + '_%s_iso%s_eta%s.pdf' %(ch, iso_str, eta))
        c_pt_1f.SaveAs(outdir + name + '_' + c_pt_1f.GetTitle() + '_%s_iso%s_eta%s.root'%(ch, iso_str, eta))

        i += 1

#    c_pt_n = rt.TCanvas('ptCone_n', 'ptCone_n')
#    c_pt_n.cd()
#    h_pt_l1_n.Draw('ep')
#    h_pt_l1_n.SetTitle('; p_{T}^{Cone} [GeV]; numerator')
#    pf.showlogoprelimsim('CMS')
#    pf.showTitle('iso_cut = 0.%s'%iso_str)
#    c_pt_n.Modified; c_pt_n.Update()
#    c_pt_n.SaveAs(outdir + c_pt_n.GetTitle() + '_' + name + '_%s_iso%s.png' %(ch, iso_str))
#    c_pt_n.SaveAs(outdir + c_pt_n.GetTitle() + '_' + name + '_%s_iso%s.pdf' %(ch, iso_str))
#    c_pt_n.SaveAs(outdir + c_pt_n.GetTitle() + '_' + name + '_%s_iso%s.root'%(ch, iso_str))

#    c_pt_d = rt.TCanvas('ptCone_d', 'ptCone_d')
#    h_pt_l1_d.Draw('ep')
#    h_pt_l1_d.SetTitle('; p_{T}^{Cone} [GeV]; denominator')
#    pf.showlogoprelimsim('CMS')
#    pf.showTitle('iso_cut = 0.%s'%iso_str)
#    c_pt_d.Modified; c_pt_d.Update()
#    c_pt_d.SaveAs(outdir + c_pt_d.GetTitle() + '_' + name + '_%s_iso%s.png' %(ch, iso_str))
#    c_pt_d.SaveAs(outdir + c_pt_d.GetTitle() + '_' + name + '_%s_iso%s.pdf' %(ch, iso_str))
#    c_pt_d.SaveAs(outdir + c_pt_d.GetTitle() + '_' + name + '_%s_iso%s.root'%(ch, iso_str))

    c_pt_1f = rt.TCanvas('ptCone_1f', 'ptCone_1f')
    h_pt_1f[0].Draw()
    h_pt_1f[1].Draw('same')
    c_pt_1f.BuildLegend(0.18, 0.78, 0.41, 0.9)
#    c_pt_1f.SetLogz()
    pf.showlogoprelimsim('CMS')
#    pf.showTitle('iso_cut = 0.%s'%iso_str)
    pf.showTitle('eta: %s'%eta)
    c_pt_1f.Modified; c_pt_1f.Update()

    c_pt_1f.SaveAs(outdir + 'cmbnd_' + c_pt_1f.GetTitle() + '_%s_iso%s_eta%s.png' %(ch, iso_str, eta))
    c_pt_1f.SaveAs(outdir + 'cmbnd_' + c_pt_1f.GetTitle() + '_%s_iso%s_eta%s.pdf' %(ch, iso_str, eta))
    c_pt_1f.SaveAs(outdir + 'cmbnd_' + c_pt_1f.GetTitle() + '_%s_iso%s_eta%s.root'%(ch, iso_str, eta))

#    c_pt_2f = rt.TCanvas('ptCone_2f', 'ptCone_2f')
#    h_pt_2f = rt.TEfficiency(h_pt_2f_n, h_pt_2f_d)
#    h_pt_2f.Draw()
#    h_pt_2f.SetTitle('; p_{T}^{Cone} [GeV]; tigh-to-loose ratio (two fakes same vtx & jet)')
#    c_pt_2f.SetLogz()
#    pf.showlogoprelimsim('CMS')
#    pf.showTitle('iso_cut = 0.%s'%iso_str)
#    pf.showTitle('eta: %s'%eta)
#    c_pt_2f.Modified; c_pt_2f.Update()
    
#    c_pt_2f.SaveAs(outdir + name + '_' + c_pt_2f.GetTitle() + '_%s_iso%s_eta%s.png' %(ch, iso_str, eta))
#    c_pt_2f.SaveAs(outdir + name + '_' + c_pt_2f.GetTitle() + '_%s_iso%s_eta%s.pdf' %(ch, iso_str, eta))
#    c_pt_2f.SaveAs(outdir + name + '_' + c_pt_2f.GetTitle() + '_%s_iso%s_eta%s.root'%(ch, iso_str, eta))

    print name + '_%s_iso%s\t\t done'%(ch,iso_str)
####################################################################################################


if 1 == 2:
    for sample_dir in [TT_dir_e, TT_dir_m]:
        ch = basename(split(normpath(sample_dir))[0]) 
        fin = rt.TFile(indir + sample_dir + suffix)
        t = fin.Get('tree')

        b_rho = np.arange(-100.,100,4)
        b_r   = np.arange(0.,6,0.05)
        b_z   = np.arange(-1.5,1.5,0.04)
        b_st  = np.arange(-20,20,1)

        h_rho  = rt.TH1F('delta_rho', 'delta_rho',len(b_rho)-1,b_rho)
        h_z    = rt.TH1F('delta_z', 'delta_z',len(b_z)-1,b_z)
        h_dR_z = rt.TH2F('twoD_plot', 'twoD_plot',len(b_z)-1,b_z,len(b_r)-1,b_r)
        h_dVtx = rt.TH2F('simType_diffVtx', 'simType_diffVtx',len(b_st)-1,b_st,len(b_st)-1,b_st)
        h_sVtx = rt.TH2F('simType_sameVtx', 'simType_sameVtx',len(b_st)-1,b_st,len(b_st)-1,b_st)

        reasonable_sim = '(abs(l1_simType) < 100 & abs(l2_simType) < 100)'
      
        set_trace()

        t.Draw('l2_simProdRho - l1_simProdRho >> delta_rho', two_fakes)
        t.Draw('l2_simProdZ - l1_simProdZ >> delta_z', two_fakes)
        t.Draw('sqrt((l2_simPhi - l1_simPhi)^2 + (l2_simEta - l1_simEta)^2 ) : l2_simProdZ - l1_simProdZ >> twoD_plot', two_fakes)
        t.Draw('l2_simType:l1_simType >> simType_diffVtx', two_fakes + '  &  !' + twoFakes_sameVtx + '  &&  ' + reasonable_sim)
        t.Draw('l2_simType:l1_simType >> simType_sameVtx', two_fakes + '  &&  ' + twoFakes_sameVtx + '  &&  ' + reasonable_sim)

        c_sVtx = rt.TCanvas('sVtx', 'sVtx')
        h_sVtx.Draw('colz')
        h_sVtx.SetTitle('; l_{1} simType; l_{2} simType')
    #    c_sVtx.SetLogz()
        pf.showlogoprelimsim('CMS')
        c_sVtx.Modified; c_sVtx.Update()

        c_dVtx = rt.TCanvas('dVtx', 'dVtx')
        h_dVtx.Draw('colz')
        h_dVtx.SetTitle('; l_{1} simType; l_{2} simType')
    #    c_dVtx.SetLogz()
        pf.showlogoprelimsim('CMS')
        c_dVtx.Modified; c_dVtx.Update()

        c_rho = rt.TCanvas('rho', 'rho')
        h_rho.Draw('ep')
        h_rho.SetTitle('; #Delta#rho (l_{1}, l_{2}); Entries')
        pf.showlogoprelimsim('CMS')
        c_rho.SetLogy()
        c_rho.Modified; c_rho.Update()

        c_z = rt.TCanvas('z', 'z')
        h_z.Draw('ep')
        h_z.SetTitle('; #DeltaZ (l_{1}, l_{2}); Entries')
        pf.showlogoprelimsim('CMS')
        c_z.SetLogy()
        c_z.Modified; c_z.Update()

        c_dR_z = rt.TCanvas('dR_z', 'dR_z')
        h_dR_z.Draw('colz')
        h_dR_z.SetTitle('; #DeltaZ (l_{1}, l_{2}); #DeltaR (l_{1}, l_{2})')
        c_dR_z.SetLogz()
        pf.showlogoprelimsim('CMS')
        c_dR_z.Modified; c_dR_z.Update()


        for c in [c_dVtx, c_sVtx, c_rho, c_z, c_dR_z]:
            c.SaveAs(outdir + 'delta_' + c.GetTitle() + '_' + ch + '.png')
            c.SaveAs(outdir + 'delta_' + c.GetTitle() + '_' + ch + '.pdf')
            c.SaveAs(outdir + 'delta_' + c.GetTitle() + '_' + ch + '.root')

isolst = [0.10,0.11,0.12,0.13,0.14,0.15,0.16,0.17,0.18,0.19,0.20]

#print '\n'
#pool = Pool(processes=len(isolst))
#print('number of processes (ie. samples): %i'%len(isolst))
#pool.map(checkTTLratio, isolst)

print '\n'
pool = Pool(processes=len(eta_bins))
print('number of processes (ie. samples): %i'%len(eta_bins))
pool.map(checkTTLratio, eta_bins)
#checkTTLratio(['0-to-2.4', l0_prompt])

print '\n'
#pool = Pool(processes=len(mltlst))
#print('number of processes (ie. samples): %i'%len(mltlst))
#pool.map(countFakes, mltlst) 
#countFakes([TT_dir_m          , '1'])

def TDraw(tupel):
    tree, hist, strng, options = tupel
    tree.Draw('{s} >> {h}'.format(s=strng,h=hist), options)
####################################################################################################
