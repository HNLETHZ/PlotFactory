#################
DEFINITION
################

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

############################################
3mu at Z: l1_pt > 20  &&  l2_pt > 10  &&  l0_pt > 27  &&  abs(l0_dz) < 0.2 &&  abs(l1_dz) < 0.2 &&  abs(l2_dz) < 0.2   &&  abs(l0_dxy) < 0.045 &&  abs(l1_dxy) < 0.045 &&  abs(l2_dxy) < 0.045   && l0_id_m && l1_id_m && l2_id_m   && abs(l0_eta) < 2.4 && abs(l1_eta) < 2.4 && abs(l2_eta) < 2.4   && l0_reliso05 < 0.1 && l1_reliso05 < 0.1 && l2_reliso05 < 0.1   && hnl_dr_01 > 0.05 && hnl_dr_02 > 0.05 && hnl_dr_12 > 0.05

3mu at Z PT relaxed: l1_pt > 20  &&  l2_pt > 4  &&  l0_pt > 4  &&  abs(l0_dz) < 0.2 &&  abs(l1_dz) < 0.2 &&  abs(l2_dz) < 0.2   &&  abs(l0_dxy) < 0.045 &&  abs(l1_dxy) < 0.045 &&  abs(l2_dxy) < 0.045   && l0_id_m && l1_id_m && l2_id_m   && abs(l0_eta) < 2.4 && abs(l1_eta) < 2.4 && abs(l2_eta) < 2.4   && l0_reliso05 < 0.1 && l1_reliso05 < 0.1 && l2_reliso05 < 0.1   && hnl_dr_01 > 0.05 && hnl_dr_02 > 0.05 && hnl_dr_12 > 0.05
############################################

WJetsToLNu_prompt_e
     entries        100.0%  145081
     one_fake_xor       0.1%    108
     two_fakes      99.9%   144935
     two_fakes_same_vtx     92.5%   134149

WJetsToLNu_ext_prompt_e
     entries        100.0%  196151
     one_fake_xor       0.1%    144
     two_fakes      99.9%   195956
     two_fakes_same_vtx     92.4%   181339

TTJets_prompt_e
     entries        100.0%  4032890
     one_fake_xor       18.8%   757176
     two_fakes      81.2%   3274225
     two_fakes_same_vtx     26.3%   1061065

DYBB_prompt_e
     entries        100.0%  83512
     one_fake_xor       0.1%    93
     two_fakes      99.6%   83192
     two_fakes_same_vtx     44.2%   36913

DYJetsToLL_M10to50_ext_prompt_e
     entries        100.0%  1556
     one_fake_xor       0.1%    2
     two_fakes      99.5%   1548
     two_fakes_same_vtx     81.1%   1262

DYJetsToLL_M50_prompt_e
     entries        100.0%  257422
     one_fake_xor       0.1%    324
     two_fakes      99.6%   256288
     two_fakes_same_vtx     85.8%   220920

################################################################

WJetsToLNu_prompt_m
     entries        100.0%  290366
     one_fake_xor       0.3%    800
     two_fakes      99.7%   289483
     two_fakes_same_vtx     88.8%   257741

WJetsToLNu_ext_prompt_m
     entries        100.0%  394905
     one_fake_xor       0.3%    1126
     two_fakes      99.7%   393677
     two_fakes_same_vtx     88.6%   350057

TTJets_prompt_m
     entries        100.0%  5664221
     one_fake_xor       12.7%   718716
     two_fakes      87.2%   4940107
     two_fakes_same_vtx     30.2%   1709113

DYBB_prompt_m
     entries        100.0%  270437
     one_fake_xor       80.5%   217781
     two_fakes      19.3%   52105
     two_fakes_same_vtx     9.8%    26434

DYJetsToLL_M10to50_ext_prompt_m
     entries        100.0%  10525
     one_fake_xor       75.4%   7931
     two_fakes      24.5%   2580
     two_fakes_same_vtx     19.2%   2017

DYJetsToLL_M10to50_prompt_m
     entries        100.0%  29840
     one_fake_xor       76.2%   22728
     two_fakes      23.7%   7080
     two_fakes_same_vtx     18.8%   5605

DYJetsToLL_M50_prompt_m
     entries        100.0%  1093216
     one_fake_xor       76.8%   839588
     two_fakes      23.1%   252259
     two_fakes_same_vtx     18.7%   203943

################################################################

DYJetsToLL_M50_prompt_m
(3mu at Z)
     entries        100.0%  358
     no_fakes       16.8%   60
     one_fake_xor       82.4%   295
     two_fakes      0.8%    3
     two_fakes_same_vtx     0.0%    0

DYJetsToLL_M10to50_prompt_m
(3mu at Z PT relaxed)
     entries        100.0%  13
     no_fakes       7.7%    1
     one_fake_xor       92.3%   12
     two_fakes      0.0%    0
     two_fakes_same_vtx     0.0%    0

DYJetsToLL_M10to50_ext_prompt_m
(3mu at Z PT relaxed)
     entries        100.0%  3
     no_fakes       0.0%    0
     one_fake_xor       100.0%  3
     two_fakes      0.0%    0
     two_fakes_same_vtx     0.0%    0

###############################################################

TTJets_prompt_e
cuts:   hnl_2d_disp > 0.5  &&  nbj > 0
     entries        100.0%  595071
     no_fakes       0.0%    13
     one_fake_xor       7.7%    45862
     two_fakes      92.3%   549196
     two_fakes_same_vtx     39.6%   235576

TTJets_prompt_m
cuts:   hnl_2d_disp > 0.5  &&  nbj > 0
     entries        100.0%  1054882
     no_fakes       0.0%    98
     one_fake_xor       5.4%    57437
     two_fakes      94.5%   997347
     two_fakes_same_vtx     44.9%   473453
