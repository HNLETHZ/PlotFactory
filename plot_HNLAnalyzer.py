import ROOT as rt
import plotfactory as pf
import numpy as np
import sys
from pdb import set_trace

pf.setpfstyle()
output_dir = 'temp/' 

######################################### 
# Make Chain from selection of samples
#########################################

# # Get the option from the command line, using 'True' as a fallback.
# if len(sys.argv)>1 and sys.argv[1] == 'test':
    # setting = False
    # print('Using a selection of samples')
# else:
    # setting = True
    # print('Using all samples')

# tt = pf.makechain(setting)

# option for single file
tt = rt.TChain('tree')
# tt.Add('/afs/cern.ch/user/d/dezhu/workspace/HNL/CMSSW_8_0_25/src/CMGTools/HNL/0_result/3_ntuples/HN3L_M_2p5_V_0p0173205080757_e_onshell_50/HNLTreeProducer/tree.root')
tt.Add('/afs/cern.ch/user/d/dezhu/workspace/HNL/CMSSW_8_0_25/src/CMGTools/HNL/0_result/3_ntuples/HN3L_M_2p5_V_0p0173205080757_e_onshell_6/HNLTreeProducer/tree.root')

nentries = tt.GetEntries()
print('number of total entries in chain:\t\t\t%d'%(nentries))

######################################### 
# Produce KPIs
#########################################

# selection 0: all gen info should point towards that the HNL is reconstructable
# selection0 = 'abs(l1_pdgId)==13 & abs(l2_pdgId)==13 & abs(l0_eta)<2.4 & abs(l1_eta)<2.4 & abs(l2_eta)<2.4 & abs(l0_pt)<5 & abs(l1_pt)<5 & abs(l2_pt)<5'
selection0 = 'abs(l1_pdgId)==13 & abs(l2_pdgId)==13 & abs(l0_eta)<2.4 & abs(l1_eta)<2.4 & abs(l2_eta)<2.4'

# selection 1: for l1 and l2 there should exist for each a reco muon
selection1 = '(abs(l1_bestmatchtype) == 13 | abs(l1_bestmatchtype) == 26 | abs(l1_bestmatchtype) == 39) & (abs(l2_bestmatchtype) == 13 | abs(l2_bestmatchtype) == 26 | abs(l2_bestmatchtype) == 39)'

# selection 1_0: for the best muons surviving the muon concatenator
selection1_0 = 'flag_MUCOsuccess == 1'

# selection 1_1: for the correct dimuon is within the pool of dimuons
selection1_1 = 'flag_IsThereTHEDimuon == 1'

# selection 2: HNL Analyzer has selected the correct l1 and l2 
# selection2_Chi2 = 'flag_matchedHNLChi2 == 1'
# selection2_Dxy = 'flag_matchedHNLDxy == 1'
# selection2_MaxPt = 'flag_matchedHNLMaxPt == 1'
# selection2_MinDr12 = 'flag_matchedHNLMinDr12 == 1'
# selection2_MaxCosBPA = 'flag_matchedHNLMaxCosBPA == 1'


selection2_MaxCosBPA = '((dMu1MaxCosBPA_pt-l1_pt)/(l1_pt) < 0.2) & ((dMu2MaxCosBPA_pt-l2_pt)/(l2_pt) < 0.2)'
selection2_Chi2 = '((dMu1Chi2_pt-l1_pt)/(l1_pt) < 0.2) & ((dMu2Chi2_pt-l2_pt)/(l2_pt) < 0.2)'
selection2_Dxy = '((dMu1Dxy_pt-l1_pt)/(l1_pt) < 0.2) & ((dMu2Dxy_pt-l2_pt)/(l2_pt) < 0.2)'
selection2_MaxPt = '((dMu1MaxPt_pt-l1_pt)/(l1_pt) < 0.2) & ((dMu2MaxPt_pt-l2_pt)/(l2_pt) < 0.2)'
selection2_MinDr12 = '((dMu1MinDr12_pt-l1_pt)/(l1_pt) < 0.2) & ((dMu2MinDr12_pt-l2_pt)/(l2_pt) < 0.2)'

# selection 3: The vertex fitter has reconstructed the correct vertex
selection3 = 'abs((sv_reco_x-sv_x)/(sv_x))<0.3 & abs((sv_reco_y-sv_y)/(sv_y))<0.3 & abs((sv_reco_z-sv_z)/(sv_z))<0.3'





n_selection0 = tt.GetEntries(selection0) 
eff_selection0 = float(n_selection0)/float(nentries)
print('selection 0 (gen in acceptance region): \t\t%d\t(%.1f%%)'%(n_selection0,100*eff_selection0))

n_selection1 = tt.GetEntries('&'.join([selection0,selection1])) 
eff_selection1= float(n_selection1)/float(n_selection0)
print('selection 1 (l1/2 have bestmatch reco muons): \t\t%d\t(%.1f%%)'%(n_selection1,100*eff_selection1))

n_selection1_0 = tt.GetEntries('&'.join([selection0,selection1,selection1_0])) 
eff_selection1_0= float(n_selection1_0)/float(n_selection1)
print('selection 1_0 best muons survived the MUCO: \t\t%d\t(%.1f%%)'%(n_selection1_0,100*eff_selection1_0))

n_selection1_1 = tt.GetEntries('&'.join([selection0,selection1,selection1_0,selection1_1])) 
eff_selection1_1= float(n_selection1_1)/float(n_selection1_0)
print('selection 1_1 correct dimuon exist as candidate: \t%d\t(%.1f%%)'%(n_selection1_1,100*eff_selection1_1))

n_selection2_Chi2 = tt.GetEntries('&'.join([selection0,selection1,selection1_0,selection1_1,selection2_Chi2])) 
eff_selection2_Chi2= float(n_selection2_Chi2)/float(n_selection1_1)
print('selection 2 (correct l1/2 (Chi2)): \t\t\t%d\t(%.1f%%)'%(n_selection2_Chi2,100*eff_selection2_Chi2))

n_selection2_Dxy = tt.GetEntries('&'.join([selection0,selection1,selection1_0,selection1_1,selection2_Dxy])) 
eff_selection2_Dxy= float(n_selection2_Dxy)/float(n_selection1_1)
print('selection 2 (correct l1/2 (Dxy)): \t\t\t%d\t(%.1f%%)'%(n_selection2_Dxy,100*eff_selection2_Dxy))

n_selection2_MaxPt = tt.GetEntries('&'.join([selection0,selection1,selection1_0,selection1_1,selection2_MaxPt])) 
eff_selection2_MaxPt= float(n_selection2_MaxPt)/float(n_selection1_1)
print('selection 2 (correct l1/2 (MaxPt)): \t\t\t%d\t(%.1f%%)'%(n_selection2_MaxPt,100*eff_selection2_MaxPt))

n_selection2_MinDr12 = tt.GetEntries('&'.join([selection0,selection1,selection1_0,selection1_1,selection2_MinDr12])) 
eff_selection2_MinDr12= float(n_selection2_MinDr12)/float(n_selection1_1)
print('selection 2 (correct l1/2 (MinDr12)): \t\t\t%d\t(%.1f%%)'%(n_selection2_MinDr12,100*eff_selection2_MinDr12))

n_selection2_MaxCosBPA = tt.GetEntries('&'.join([selection0,selection1,selection1_0,selection1_1,selection2_MaxCosBPA])) 
eff_selection2_MaxCosBPA= float(n_selection2_MaxCosBPA)/float(n_selection1_1)
print('selection 2 (correct l1/2 (MaxCosBPA)): \t\t%d\t(%.1f%%)'%(n_selection2_MaxCosBPA,100*eff_selection2_MaxCosBPA))

n_selection3 = tt.GetEntries('&'.join([selection0,selection1,selection2_MaxCosBPA,selection3])) 
eff_selection3= float(n_selection3)/float(n_selection2_Chi2)
print('selection 3 (correct vertex): \t\t\t\t%d\t(%.1f%%)'%(n_selection3,100*eff_selection3))



# ######################################### 
# # Vertex Reconstruction
# #########################################
# print'making vertex reconstruction plots'

# c_VtxRes = rt.TCanvas('c_VtxRes', 'c_VtxRes')
# h_VtxRes = rt.TH2F('h_VtxRes','',50,0.,200.,50,0.,200.)
# tt.Draw('dimuonChi2_dxy:sqrt(sv_reco_x*sv_reco_x + sv_reco_y*sv_reco_y) >> h_VtxRes','sv_reco_x != -99 & sv_reco_y != -99 & sv_reco_z != -99')
# h_VtxRes.SetTitle(';recoSV_dxy [cm] ; recoHNL_dxy [cm]')
# h_VtxRes.Draw('colz')
# pf.showlogopreliminary('CMS','Simulation Preliminary')
# pf.showlumi('%d entries'%(h_VtxRes.GetEntries()))
# c_VtxRes.SetLogz()


# c_VtxResGen = rt.TCanvas('c_VtxResGen', 'c_VtxResGen')
# h_VtxResGen = rt.TH2F('h_VtxResGen','',50,0.,200.,50,0.,200.)
# tt.Draw('dimuonChi2_dxy:sqrt(sv_x*sv_x + sv_y*sv_y) >> h_VtxResGen','l1_charge!=l2_charge & abs(l1_eta)<2.4 & abs(l2_eta)<2.4 & l1_pt>5 & l2_pt>5& sv_reco_x != -99 & sv_reco_y != -99 & sv_reco_z != -99')
# h_VtxResGen.SetTitle(';GenSV_dxy [cm] ; recoHNL_dxy [cm]')
# h_VtxResGen.Draw('colz')
# pf.showlogopreliminary('CMS','Simulation Preliminary')
# pf.showlumi('%d entries'%(h_VtxResGen.GetEntries()))
# c_VtxResGen.SetLogz()

# c_VtxRecoGen = rt.TCanvas('c_VtxRecoGen', 'c_VtxRecoGen')
# h_VtxRecoGen = rt.TH2F('h_VtxRecoGen','',50,0.,200.,50,0.,200.)
# tt.Draw('sqrt(sv_reco_x*sv_reco_x + sv_reco_y*sv_reco_y):sqrt(sv_x*sv_x + sv_y*sv_y) >> h_VtxRecoGen','l1_charge!=l2_charge & abs(l1_eta)<2.4 & abs(l2_eta)<2.4 & l1_pt>5 & l2_pt>5& sv_reco_x != -99 & sv_reco_y != -99 & sv_reco_z != -99')
# h_VtxRecoGen.SetTitle(';GenSV_dxy [cm];RecoSV_dxy [cm] ')
# h_VtxRecoGen.Draw('colz')
# pf.showlogopreliminary('CMS','Simulation Preliminary')
# pf.showlumi('%d entries'%(h_VtxRecoGen.GetEntries()))
# c_VtxRecoGen.SetLogz()

# # vertex reconstruction efficiency
# c_VtxEff = rt.TCanvas('c_VtxEff','c_VtxEff')
# h_VtxEff0 = rt.TH1F('h_VtxEff0','',30,0.,200.)
# h_VtxEff = rt.TH1F('h_VtxEff','',30,0.,200.)
# tt.Draw('hnl_2d_disp >> h_VtxEff','l1_charge!=l2_charge & abs(l0_eta)<2.4 &abs(l1_eta)<2.4 & abs(l2_eta)<2.4 & l0_pt>5 & l1_pt>5 & l2_pt>5 & abs((sv_reco_x-sv_x)/(sv_x))<0.3 & abs((sv_reco_y-sv_y)/(sv_y))<0.3 & abs((sv_reco_z-sv_z)/(sv_z))<0.3& sv_reco_x != -99 & sv_reco_y != -99 & sv_reco_z != -99')
# tt.Draw('hnl_2d_disp >> h_VtxEff0','l1_charge!=l2_charge & abs(l0_eta)<2.4 & abs(l1_eta)<2.4 & abs(l2_eta)<2.4 & l0_pt>5 & l1_pt>5 & l2_pt>5 ')
# h_VtxEff.Divide(h_VtxEff0)
# h_VtxEff.SetTitle(';HNL 2D displacement [cm]; Vtx Reco Eff (within 30 % deviation)')
# h_VtxEff.GetYaxis().SetRangeUser(0.,1.05)
# h_VtxEff.SetLineColor  (rt.kBlack)
# h_VtxEff.SetMarkerColor(rt.kBlack)
# c_VtxEff.cd()
# h_VtxEff.Draw()
# pf.showlogopreliminary('CMS','Simulation Preliminary')
# pf.showlumi('%d entries'%(h_VtxEff.GetEntries()))
# c_VtxEff.Update()

# # vertex resolution recogen
# c_VtxResRecoGen = rt.TCanvas('VtxResRecoGen','VtxResRecoGen')
# h_VtxResRecoGen = rt.TH2F('h_VtxResRecoGen','',40,0.,200.,40,-2.,10.)
# tt.Draw('(sqrt(sv_reco_x*sv_reco_x + sv_reco_y*sv_reco_y)-sqrt(sv_x*sv_x + sv_y*sv_y))/(sqrt(sv_x*sv_x + sv_y*sv_y)):hnl_2d_disp >> h_VtxResRecoGen','abs(l1_eta)<2.4 & abs(l2_eta)<2.4 & l1_pt>5 & l2_pt>5 & sv_reco_x != -99 & sv_reco_y != -99 & sv_reco_z != -99')
# h_VtxResRecoGen.SetTitle(';HNL 2D displacement [cm]; Vtx Resolution #left[#frac{RecoSV_dxy - GenSV_dxy}{GenSV_dxy}#right] ')
# h_VtxResRecoGen.Draw('colz')
# pf.showlogopreliminary('CMS','Simulation Preliminary')
# pf.showlumi('%d entries'%(h_VtxResRecoGen.GetEntries()))
# c_VtxResRecoGen.SetLogz()

# # abundancy SV_x
# c_SV_x = rt.TCanvas('SV_x','SV_x')
# h_SV_x = rt.TH1F('h_SV_x','h_SV_x',50,-200.,200.)
# tt.Draw('sv_reco_x>>h_SV_x','abs(l1_eta)<2.4 & abs(l2_eta)<2.4 & l1_pt>5 & l2_pt>5 & sv_reco_x != -99 & sv_reco_y != -99 & sv_reco_z != -99')
# h_SV_x.SetTitle(';SV_x [cm];entries')
# h_SV_x.Draw()
# pf.showlogopreliminary('CMS','Simulation Preliminary')
# pf.showlumi('%d entries'%(h_SV_x.GetEntries()))

# # abundancy SV_y
# c_SV_y = rt.TCanvas('SV_y','SV_y')
# h_SV_y = rt.TH1F('h_SV_y','h_SV_y',50,-200.,200.)
# tt.Draw('sv_reco_y>>h_SV_y','abs(l1_eta)<2.4 & abs(l2_eta)<2.4 & l1_pt>5 & l2_pt>5 & sv_reco_x != -99 & sv_reco_y != -99 & sv_reco_z != -99')
# h_SV_y.SetTitle(';SV_y [cm];entries')
# h_SV_y.Draw()
# pf.showlogopreliminary('CMS','Simulation Preliminary')
# pf.showlumi('%d entries'%(h_SV_y.GetEntries()))

# # abundancy SV_z
# c_SV_z = rt.TCanvas('SV_z','SV_z')
# h_SV_z = rt.TH1F('h_SV_z','h_SV_z',50,-200.,200.)
# tt.Draw('sv_reco_z>>h_SV_z','abs(l1_eta)<2.4 & abs(l2_eta)<2.4 & l1_pt>5 & l2_pt>5 & sv_reco_x != -99 & sv_reco_y != -99 & sv_reco_z != -99')
# h_SV_z.SetTitle(';SV_z [cm];entries')
# h_SV_z.Draw()
# pf.showlogopreliminary('CMS','Simulation Preliminary')
# pf.showlumi('%d entries'%(h_SV_z.GetEntries()))

# #resolution SV_x
# c_SV_x_res = rt.TCanvas('SV_x_res','SV_x_res')
# h_SV_x_res = rt.TH2F('h_SV_x_res','',40,0.,200.,40,-10.,10.)
# tt.Draw('(sv_reco_x-sv_x)/(sv_x):hnl_2d_disp >> h_SV_x_res','abs(l1_eta)<2.4 & abs(l2_eta)<2.4 & l1_pt>5 & l2_pt>5 & sv_reco_x != -99 & sv_reco_y != -99 & sv_reco_z != -99')
# h_SV_x_res.SetTitle(';HNL 2D displacement [cm]; Vtx Resolution #left[#frac{RecoSV_x - GenSV_x}{GenSV_x}#right] ')
# h_SV_x_res.Draw('colz')
# pf.showlogopreliminary('CMS','Simulation Preliminary')
# pf.showlumi('%d entries'%(h_SV_x_res.GetEntries()))
# c_SV_x_res.SetLogz()

# #resolution SV_y
# c_SV_y_res = rt.TCanvas('SV_y_res','SV_y_res')
# h_SV_y_res = rt.TH2F('h_SV_y_res','',40,0.,200.,40,-10.,10.)
# tt.Draw('(sv_reco_y-sv_y)/(sv_y):hnl_2d_disp >> h_SV_y_res','abs(l1_eta)<2.4 & abs(l2_eta)<2.4 & l1_pt>5 & l2_pt>5 & sv_reco_x != -99 & sv_reco_y != -99 & sv_reco_z != -99')
# h_SV_y_res.SetTitle(';HNL 2D displacement [cm]; Vtx Resolution #left[#frac{RecoSV_y - GenSV_y}{GenSV_y}#right] ')
# h_SV_y_res.Draw('colz')
# pf.showlogopreliminary('CMS','Simulation Preliminary')
# pf.showlumi('%d entries'%(h_SV_y_res.GetEntries()))
# c_SV_y_res.SetLogz()

# #resolution SV_z
# c_SV_z_res = rt.TCanvas('SV_z_res','SV_z_res')
# h_SV_z_res = rt.TH2F('h_SV_z_res','',40,0.,200.,40,-10.,10.)
# tt.Draw('(sv_reco_z-sv_z)/(sv_z):hnl_2d_disp >> h_SV_z_res','abs(l1_eta)<2.4 & abs(l2_eta)<2.4 & l1_pt>5 & l2_pt>5 & sv_reco_x != -99 & sv_reco_y != -99 & sv_reco_z != -99')
# h_SV_z_res.SetTitle(';HNL 2D displacement [cm]; Vtx Resolution #left[#frac{RecoSV_z - GenSV_z}{GenSV_z}#right] ')
# h_SV_z_res.Draw('colz')
# pf.showlogopreliminary('CMS','Simulation Preliminary')
# pf.showlumi('%d entries'%(h_SV_z_res.GetEntries()))
# c_SV_z_res.SetLogz()

#2d_displ 
c_corrx = rt.TCanvas('c_corrx', 'c_corrx')
h_corrx = rt.TH2F('h_corrx','',50,0.,200.,50,0.,200.)
tt.Draw('hnl_2d_disp:dimuonMaxCosBPA_disp2DFromBS >> h_corrx','l1_charge!=l2_charge & abs(l1_eta)<2.4 & abs(l2_eta)<2.4 & l1_pt>5 & l2_pt>5& sv_reco_x != -99 & sv_reco_y != -99 & sv_reco_z != -99')
tt.Draw('dimuonMaxCosBPA_disp2DFromBS:hnl_2d_disp >> h_corrx','l1_charge!=l2_charge & abs(l1_eta)<2.4 & abs(l2_eta)<2.4 & l1_pt>5 & l2_pt>5& sv_reco_x != -99 & sv_reco_y != -99 & sv_reco_z != -99')
h_corrx.SetTitle(';hnl_2d_disp [cm];dimuonMaxCosBPA_disp2DFromBS [cm] ')
h_corrx.Draw('colz')
pf.showlogopreliminary('CMS','Simulation Preliminary')
pf.showlumi('%d entries'%(h_corrx.GetEntries()))
c_corrx.SetLogz()

# #corry 
# c_corry = rt.TCanvas('c_corry', 'c_corry')
# h_corry = rt.TH2F('h_corry','',50,-200.,200.,50,-200.,200.)
# tt.Draw('sv_reco_y:sv_y >> h_corry','l1_charge!=l2_charge & abs(l1_eta)<2.4 & abs(l2_eta)<2.4 & l1_pt>5 & l2_pt>5& sv_reco_x != -99 & sv_reco_y != -99 & sv_reco_z != -99')
# h_corry.SetTitle(';GenSV_y [cm];RecoSV_y [cm] ')
# h_corry.Draw('colz')
# pf.showlogopreliminary('CMS','Simulation Preliminary')
# pf.showlumi('%d entries'%(h_corry.GetEntries()))
# c_corry.SetLogz()

# #corrz 
# c_corrz = rt.TCanvas('c_corrz', 'c_corrz')
# h_corrz = rt.TH2F('h_corrz','',50,-350.,350.,50,-350.,350.)
# tt.Draw('sv_reco_z:sv_z >> h_corrz','l1_charge!=l2_charge & abs(l1_eta)<2.4 & abs(l2_eta)<2.4 & l1_pt>5 & l2_pt>5& sv_reco_x != -99 & sv_reco_y != -99 & sv_reco_z != -99')
# h_corrz.SetTitle(';GenSV_z [cm];RecoSV_z [cm] ')
# h_corrz.Draw('colz')
# pf.showlogopreliminary('CMS','Simulation Preliminary')
# pf.showlumi('%d entries'%(h_corrz.GetEntries()))
# c_corrz.SetLogz()



######################################### 
# Reconstruction Efficiency V2
#########################################
print'making reco efficiency plots'
# a default canvas for buffer storage
c0 = rt.TCanvas('c_buffer','c_buffer')


h_eff2_0 = rt.TH1F('h_eff2_0','',30,0,200)
h_eff2_1 = rt.TH1F('h_eff2_1','',30,0,200)
h_eff2_1_0 = rt.TH1F('h_eff2_1_0','',30,0,200)
h_eff2_1_1 = rt.TH1F('h_eff2_1_1','',30,0,200)

h_eff2_2_chi2 = rt.TH1F('h_eff2_2_chi2','',30,0,200)
h_eff2_2_maxdxy = rt.TH1F('h_eff2_2_maxdxy','',30,0,200)
h_eff2_2_maxpt = rt.TH1F('h_eff2_2_maxpt','',30,0,200)
h_eff2_2_mindr12 = rt.TH1F('h_eff2_2_mindr12','',30,0,200)
h_eff2_2_maxcosbpa = rt.TH1F('h_eff2_2_maxcosbpa','',30,0,200)

h_eff2_3_chi2 = rt.TH1F('h_eff2_3_chi2','',30,0,200)
h_eff2_3_maxdxy = rt.TH1F('h_eff2_3_maxdxy','',30,0,200)
h_eff2_3_maxpt = rt.TH1F('h_eff2_3_maxpt','',30,0,200)
h_eff2_3_mindr12 = rt.TH1F('h_eff2_3_mindr12','',30,0,200)
h_eff2_3_maxcosbpa = rt.TH1F('h_eff2_3_maxcosbpa','',30,0,200)

# draw the efficiency plots
tt.Draw('hnl_2d_disp >> h_eff2_0',selection0)
tt.Draw('hnl_2d_disp >> h_eff2_1','&'.join([selection0,selection1]))
tt.Draw('hnl_2d_disp >> h_eff2_1_0','&'.join([selection0,selection1,selection1_0]))
tt.Draw('hnl_2d_disp >> h_eff2_1_1','&'.join([selection0,selection1,selection1_0,selection1_1]))

tt.Draw('hnl_2d_disp >> h_eff2_2_chi2','&'.join([selection0,selection1,selection1_0,selection1_1,selection2_Chi2]))
tt.Draw('hnl_2d_disp >> h_eff2_2_maxdxy','&'.join([selection0,selection1,selection1_0,selection1_1,selection2_Dxy]))
tt.Draw('hnl_2d_disp >> h_eff2_2_maxpt','&'.join([selection0,selection1,selection1_0,selection1_1,selection2_MaxPt]))
tt.Draw('hnl_2d_disp >> h_eff2_2_mindr12','&'.join([selection0,selection1,selection1_0,selection1_1,selection2_MinDr12]))
tt.Draw('hnl_2d_disp >> h_eff2_2_maxcosbpa','&'.join([selection0,selection1,selection1_0,selection1_1,selection2_MaxCosBPA]))

tt.Draw('hnl_2d_disp >> h_eff2_3_chi2','&'.join([selection0,selection1,selection1_0,selection1_1,selection2_Chi2,selection3]))
tt.Draw('hnl_2d_disp >> h_eff2_3_maxdxy','&'.join([selection0,selection1,selection1_0,selection1_1,selection2_Dxy,selection3]))
tt.Draw('hnl_2d_disp >> h_eff2_3_maxpt','&'.join([selection0,selection1,selection1_0,selection1_1,selection2_MaxPt,selection3]))
tt.Draw('hnl_2d_disp >> h_eff2_3_mindr12','&'.join([selection0,selection1,selection1_0,selection1_1,selection2_MinDr12,selection3]))
tt.Draw('hnl_2d_disp >> h_eff2_3_maxcosbpa','&'.join([selection0,selection1,selection1_0,selection1_1,selection2_MaxCosBPA,selection3]))

# # make efficiencies
h_eff2_3_chi2.Divide(h_eff2_2_chi2)
h_eff2_3_maxdxy.Divide(h_eff2_2_maxdxy)
h_eff2_3_maxpt.Divide(h_eff2_2_maxpt)
h_eff2_3_mindr12.Divide(h_eff2_2_mindr12)
h_eff2_3_maxcosbpa.Divide(h_eff2_2_maxcosbpa)

h_eff2_2_chi2.Divide(h_eff2_1_1)
h_eff2_2_maxdxy.Divide(h_eff2_1_1)
h_eff2_2_maxpt.Divide(h_eff2_1_1)
h_eff2_2_mindr12.Divide(h_eff2_1_1)
h_eff2_2_maxcosbpa.Divide(h_eff2_1_1)

h_eff2_1_1.Divide(h_eff2_1_0)
h_eff2_1_0.Divide(h_eff2_1)
h_eff2_1.Divide(h_eff2_0)


# plot settings
h_eff2_0.SetLineColor  (rt.kBlack)
h_eff2_0.SetMarkerColor(rt.kBlack)
h_eff2_1.SetLineColor  (rt.kRed+2)
h_eff2_1.SetMarkerColor(rt.kRed+2)
h_eff2_1_0.SetLineColor  (rt.kMagenta)
h_eff2_1_0.SetMarkerColor(rt.kMagenta)
h_eff2_1_1.SetLineColor  (rt.kBlack)
h_eff2_1_1.SetMarkerColor(rt.kBlack)

h_eff2_0.SetTitle(';HNL 2D displacement [cm]; Efficiency')
h_eff2_0.GetYaxis().SetRangeUser(0.,1.05)
h_eff2_1.SetTitle(';HNL 2D displacement [cm]; Efficiency')
# h_eff2_1.SetTitle(';HNL 2D displacement [cm];')
h_eff2_1.GetYaxis().SetRangeUser(0.,1.05)
h_eff2_1_1.SetTitle(';HNL 2D displacement [cm]; Efficiency')
h_eff2_1_1.GetYaxis().SetRangeUser(0.,1.05)

h_eff2_2_chi2.SetLineColor  (rt.kGreen+2)
h_eff2_2_chi2.SetMarkerColor(rt.kGreen+2)
h_eff2_2_maxdxy.SetLineColor  (rt.kGreen+2)
h_eff2_2_maxdxy.SetMarkerColor  (rt.kGreen+2)
h_eff2_2_mindr12.SetLineColor  (rt.kGreen+2)
h_eff2_2_mindr12.SetMarkerColor  (rt.kGreen+2)
h_eff2_2_maxpt.SetLineColor(rt.kGreen+2)
h_eff2_2_maxpt.SetMarkerColor(rt.kGreen+2)
h_eff2_2_maxcosbpa.SetLineColor(rt.kGreen+2)
h_eff2_2_maxcosbpa.SetMarkerColor(rt.kGreen+2)
h_eff2_2_maxcosbpa.SetTitle(';HNL 2D displacement [cm]; Efficiency')

h_eff2_3_chi2.SetLineColor  (rt.kBlue+2)
h_eff2_3_chi2.SetMarkerColor(rt.kBlue+2)
h_eff2_3_maxdxy.SetLineColor  (rt.kBlue+2)
h_eff2_3_maxdxy.SetMarkerColor(rt.kBlue+2)
h_eff2_3_mindr12.SetLineColor  (rt.kBlue+2)
h_eff2_3_mindr12.SetMarkerColor(rt.kBlue+2)
h_eff2_3_maxpt.SetLineColor  (rt.kBlue+2)
h_eff2_3_maxpt.SetMarkerColor(rt.kBlue+2)
h_eff2_3_maxcosbpa.SetLineColor  (rt.kBlue+2)
h_eff2_3_maxcosbpa.SetMarkerColor(rt.kBlue+2)

#######################################################################################
# draw plots
c_eff2_maxcosbpa = rt.TCanvas('c_eff2_maxcosbpa','c_eff2_maxcosbpa')
# h_eff2_0.Draw('same')
h_eff2_1.Draw('same')
h_eff2_1_1.Draw('same')
h_eff2_2_maxcosbpa.Draw('same')

# build legend
l_eff2_maxcosbpa = rt.TLegend(.4,.75,.8,.88)
# l_eff2_maxcosbpa.AddEntry(h_eff2_0, 'selection 0: gens in_acc','EP')
l_eff2_maxcosbpa.AddEntry(h_eff2_1, 'selection 1: lepton reco success ','EP')
l_eff2_maxcosbpa.AddEntry(h_eff2_1_1, 'selection 2: vtx fit success','EP')
l_eff2_maxcosbpa.AddEntry(h_eff2_2_maxcosbpa, 'selection 3: dilepton selection success','EP')
l_eff2_maxcosbpa.Draw('apez same')

# pf.showlogopreliminary('CMS','Simulation Preliminary')
pf.showlumi('%d entries'%(h_eff2_0.GetEntries()))
c_eff2_maxcosbpa.Update()

#######################################################################################
# draw plots
c_eff2_mindr12 = rt.TCanvas('c_eff2_mindr12','c_eff2_mindr12')
# h_eff2_0.Draw('same')
h_eff2_1.Draw('same')
h_eff2_1_1.Draw('same')
h_eff2_2_mindr12.Draw('same')

# build legend
l_eff2_mindr12 = rt.TLegend(.4,.75,.8,.88)
# l_eff2_mindr12.AddEntry(h_eff2_0, 'selection 0: gens in_acc','EP')
l_eff2_mindr12.AddEntry(h_eff2_1, 'selection 1: lepton reco success ','EP')
l_eff2_mindr12.AddEntry(h_eff2_1_1, 'selection 2: vtx fit success','EP')
l_eff2_mindr12.AddEntry(h_eff2_2_mindr12, 'selection 3: dilepton selection success','EP')
l_eff2_mindr12.Draw('apez same')

# pf.showlogopreliminary('CMS','Simulation Preliminary')
pf.showlumi('%d entries'%(h_eff2_0.GetEntries()))
c_eff2_mindr12.Update()

# #######################################################################################
# # draw plots
# c_eff2_mindr12 = rt.TCanvas('c_eff2_mindr12','c_eff2_mindr12')
# h_eff2_1.Draw()
# h_eff2_1_0.Draw('same')
# h_eff2_1_1.Draw('same')
# h_eff2_2_mindr12.Draw('same')
# h_eff2_3_mindr12.Draw('same')

# # build legend
# l_eff2_mindr12 = rt.TLegend(.4,.75,.8,.88)
# # l_eff2.AddEntry(h_eff2_0, 'selection 0: gen','EP')
# l_eff2_mindr12.AddEntry(h_eff2_1, 'selection 1: there is reco','EP')
# l_eff2_mindr12.AddEntry(h_eff2_1_0, 'selection 1_0: MUCO success','EP')
# l_eff2_mindr12.AddEntry(h_eff2_1_1, 'selection 1_1: there is THE dimuon','EP')
# l_eff2_mindr12.AddEntry(h_eff2_2_mindr12, 'selection 2: correct recos mindr12','EP')
# l_eff2_mindr12.AddEntry(h_eff2_3_mindr12, 'selection 3: vertex','EP')
# l_eff2_mindr12.Draw('apez same')

# pf.showlogopreliminary('CMS','Simulation Preliminary')
# pf.showlumi('%d entries'%(h_eff2_0.GetEntries()))
# c_eff2_mindr12.Update()

# #######################################################################################
# # draw plots
# c_eff2_chi2 = rt.TCanvas('c_eff2_chi2','c_eff2_chi2')
# c_eff2_chi2.cd()
# h_eff2_1.Draw()
# h_eff2_1_0.Draw('same')
# h_eff2_1_1.Draw('same')
# h_eff2_2_chi2.Draw('same')
# h_eff2_3_chi2.Draw('same')

# # build legend
# l_eff2_chi2 = rt.TLegend(.4,.75,.8,.88)
# # l_eff2.AddEntry(h_eff2_0, 'selection 0: gen','EP')
# l_eff2_chi2.AddEntry(h_eff2_1, 'selection 1: there is reco','EP')
# l_eff2_chi2.AddEntry(h_eff2_1_0, 'selection1_0: MUCO success','EP')
# l_eff2_chi2.AddEntry(h_eff2_1_1, 'selection 1_1: there is THE dimuon','EP')
# l_eff2_chi2.AddEntry(h_eff2_2_chi2, 'selection 2: correct recos minchi2','EP')
# l_eff2_chi2.AddEntry(h_eff2_3_chi2, 'selection 3: vertex','EP')
# l_eff2_chi2.Draw('apez same')

# pf.showlogopreliminary('CMS','Simulation Preliminary')
# pf.showlumi('%d entries'%(h_eff2_0.GetEntries()))
# c_eff2_chi2.Update()


# #######################################################################################
# # draw plots
# c_eff2_maxdxy = rt.TCanvas('c_eff2_maxdxy','c_eff2_maxdxy')
# h_eff2_1.Draw()
# h_eff2_1_0.Draw('same')
# h_eff2_1_1.Draw('same')
# h_eff2_2_maxdxy.Draw('same')
# h_eff2_3_maxdxy.Draw('same')

# # build legend
# l_eff2_maxdxy = rt.TLegend(.4,.75,.8,.88)
# # l_eff2.AddEntry(h_eff2_0, 'selection 0: gen','EP')
# l_eff2_maxdxy.AddEntry(h_eff2_1, 'selection 1: there is reco','EP')
# l_eff2_maxdxy.AddEntry(h_eff2_1_0, 'selection 1_0: MUCO success','EP')
# l_eff2_maxdxy.AddEntry(h_eff2_1_1, 'selection 1_1: there is THE dimuon','EP')
# l_eff2_maxdxy.AddEntry(h_eff2_2_maxdxy, 'selection 2: correct recos maxdxy','EP')
# l_eff2_maxdxy.AddEntry(h_eff2_3_maxdxy, 'selection 3: vertex','EP')
# l_eff2_maxdxy.Draw('apez same')

# pf.showlogopreliminary('CMS','Simulation Preliminary')
# pf.showlumi('%d entries'%(h_eff2_0.GetEntries()))
# c_eff2_maxdxy.Update()


# #######################################################################################
# # draw plots
# c_eff2_maxpt = rt.TCanvas('c_eff2_maxpt','c_eff2_maxpt')
# h_eff2_1.Draw()
# h_eff2_1_0.Draw('same')
# h_eff2_1_1.Draw('same')
# h_eff2_2_maxpt.Draw('same')
# h_eff2_3_maxpt.Draw('same')

# # build legend
# l_eff2_maxpt = rt.TLegend(.4,.75,.8,.88)
# # l_eff2.AddEntry(h_eff2_0, 'selection 0: gen','EP')
# l_eff2_maxpt.AddEntry(h_eff2_1, 'selection 1: there is reco','EP')
# l_eff2_maxpt.AddEntry(h_eff2_1_0, 'selection 1_0: MUCO success','EP')
# l_eff2_maxpt.AddEntry(h_eff2_1_1, 'selection 1_1: there is THE dimuon','EP')
# l_eff2_maxpt.AddEntry(h_eff2_2_maxpt, 'selection 2: correct recos maxpt','EP')
# l_eff2_maxpt.AddEntry(h_eff2_3_maxpt, 'selection 3: vertex','EP')
# l_eff2_maxpt.Draw('apez same')

# pf.showlogopreliminary('CMS','Simulation Preliminary')
# pf.showlumi('%d entries'%(h_eff2_0.GetEntries()))
# c_eff2_maxpt.Update()

#######################################################################################
# compare all reco methods
c_eff2_allmethods = rt.TCanvas('c_eff2_allmethods','c_eff2_allmethods')

h_eff2_2_chi2.SetLineColor  (rt.kGreen+2)
h_eff2_2_chi2.SetMarkerColor(rt.kGreen+2)
h_eff2_2_maxdxy.SetLineColor  (rt.kBlue+2)
h_eff2_2_maxdxy.SetMarkerColor  (rt.kBlue+2)
h_eff2_2_mindr12.SetLineColor  (rt.kBlack)
h_eff2_2_mindr12.SetMarkerColor  (rt.kBlack)
h_eff2_2_maxpt.SetLineColor(rt.kRed+2)
h_eff2_2_maxpt.SetMarkerColor(rt.kRed+2)
h_eff2_2_maxcosbpa.SetLineColor(rt.kMagenta+2)
h_eff2_2_maxcosbpa.SetMarkerColor(rt.kMagenta+2)

h_eff2_2_maxcosbpa.GetYaxis().SetRangeUser(0.,1.05)

h_eff2_2_maxcosbpa .Draw('same')
h_eff2_2_chi2      .Draw('same')
h_eff2_2_maxdxy    .Draw('same')
h_eff2_2_mindr12   .Draw('same')
h_eff2_2_maxpt     .Draw('same')

# build legend
l_eff2_allmethods = rt.TLegend(.4,.75,.8,.88)
l_eff2_allmethods.AddEntry(h_eff2_2_chi2     , 'chi2','EP')
l_eff2_allmethods.AddEntry(h_eff2_2_maxdxy   , 'dxy','EP')
l_eff2_allmethods.AddEntry(h_eff2_2_mindr12  , 'mindr','EP')
l_eff2_allmethods.AddEntry(h_eff2_2_maxpt    , 'maxpt','EP')
l_eff2_allmethods.AddEntry(h_eff2_2_maxcosbpa, 'maxcosbpa','EP')
l_eff2_allmethods.Draw('apez same')

# pf.showlumi('%d entries'%(h_eff2_2_maxcosbpa.GetEntries()))
c_eff2_allmethods.Update()




