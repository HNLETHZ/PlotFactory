################# 
# configuration #
#################
from pdb import set_trace
import ROOT
import numpy as np
import sys
sys.path.append('/afs/cern.ch/user/v/vstampf/CMSSW_8_0_30/PlotFactory')
import plotfactory as pf
#from pdb import set_trace
from glob import glob
#ROOT.gROOT.SetBatch(True)    # don't open X11 forwarding (running screen)
################################## 
pf.setpfstyle()
bewl = input("Makechain: True or False\n")
tt = pf.makechain(bewl)
output_dir = '/afs/cern.ch/user/v/vstampf/CMSSW_8_0_30/PlotFactory/plots/ntuplev2/dr/2d/'
################################## 
ntries = tt.GetEntries()
print('Number of entries: ' + str(ntries))
################# 
# define x-axes #
#################
pTbins = np.arange(5.,73,5)
drbins = np.arange(0.,4,0.25)
################### 
# create canvases #
###################
print('Preparing canvas')
c1 = ROOT.TCanvas('c1','c1 sa l1',600,500)
c2 = ROOT.TCanvas('c2','c2 sa l2',600,500)
c3 = ROOT.TCanvas('c3','c3 ds l1',600,500)
c4 = ROOT.TCanvas('c4','c4 ds l2',600,500)
c5 = ROOT.TCanvas('c5','c5 g l1',600,500)
c6 = ROOT.TCanvas('c6','c6 g l2',600,500)
c7 = ROOT.TCanvas('c7','c7 dg l1',600,500)
c8 = ROOT.TCanvas('c8','c8 dg l2',600,500)
##################### 
# create histograms #
#####################
# d in cm           #
# d1: less than 4   #
# d2: 4 - 120       #
# d3: 120 - 350     #
# d4: 350 - 600     #
#####################  
# standalone        #
##################### 
samul0 = ROOT.TH2F('samul0','samul0',len(pTbins)-1,pTbins,len(drbins)-1,drbins)
samunfl1 = ROOT.TH2F('samunfl1','samunfl1',len(pTbins)-1,pTbins,len(drbins)-1,drbins)
samunfl2 = ROOT.TH2F('samunfl2','samunfl2',len(pTbins)-1,pTbins,len(drbins)-1,drbins)
samucfl1 = ROOT.TH2F('samucfl1','samucfl1',len(pTbins)-1,pTbins,len(drbins)-1,drbins)
samucfl2 = ROOT.TH2F('samucfl2','samucfl2',len(pTbins)-1,pTbins,len(drbins)-1,drbins)
#######################################################################################  
samusuml1= ROOT.TH2F('samusuml1','samusuml1',len(pTbins)-1,pTbins,len(drbins)-1,drbins) 
samusuml2= ROOT.TH2F('samusuml2','samusuml2',len(pTbins)-1,pTbins,len(drbins)-1,drbins)
samucfl1R= ROOT.TH2F('samucfl1R','samucfl1R',len(pTbins)-1,pTbins,len(drbins)-1,drbins)
samucfl2R= ROOT.TH2F('samucfl2R','samucfl2R',len(pTbins)-1,pTbins,len(drbins)-1,drbins)
#######################################################################################  
dsmul0 = ROOT.TH2F('dsmul0','dsmul0',len(pTbins)-1,pTbins,len(drbins)-1,drbins)
dsmunfl1 = ROOT.TH2F('dsmunfl1','dsmunfl1',len(pTbins)-1,pTbins,len(drbins)-1,drbins)
dsmunfl2 = ROOT.TH2F('dsmunfl2','dsmunfl2',len(pTbins)-1,pTbins,len(drbins)-1,drbins)
dsmucfl1 = ROOT.TH2F('dsmucfl1','dsmucfl1',len(pTbins)-1,pTbins,len(drbins)-1,drbins)
dsmucfl2 = ROOT.TH2F('dsmucfl2','dsmucfl2',len(pTbins)-1,pTbins,len(drbins)-1,drbins)
#######################################################################################  
dsmusuml1= ROOT.TH2F('dsmusum11','dsmusuml1',len(pTbins)-1,pTbins,len(drbins)-1,drbins) 
dsmusuml2= ROOT.TH2F('dsmusuml2','dsmusuml2',len(pTbins)-1,pTbins,len(drbins)-1,drbins)
dsmucfl1R= ROOT.TH2F('dsmucfl1R','dsmucfl1R',len(pTbins)-1,pTbins,len(drbins)-1,drbins)
dsmucfl2R= ROOT.TH2F('dsmucfl2R','dsmucfl2R',len(pTbins)-1,pTbins,len(drbins)-1,drbins)
################# 
# global        #
################# 
gmul0 = ROOT.TH2F('gmul0','gmul0',len(pTbins)-1,pTbins,len(drbins)-1,drbins)
gmunfl1 = ROOT.TH2F('gmunfl1','gmunfl1',len(pTbins)-1,pTbins,len(drbins)-1,drbins)
gmunfl2 = ROOT.TH2F('gmunfl2','gmunfl2',len(pTbins)-1,pTbins,len(drbins)-1,drbins)
gmucfl1 = ROOT.TH2F('gmucfl1','gmucfl1',len(pTbins)-1,pTbins,len(drbins)-1,drbins)
gmucfl2 = ROOT.TH2F('gmucfl2','gmucfl2',len(pTbins)-1,pTbins,len(drbins)-1,drbins)
#######################################################################################  
gmusuml1= ROOT.TH2F('gmusuml1','gmusuml1',len(pTbins)-1,pTbins,len(drbins)-1,drbins) 
gmusuml2= ROOT.TH2F('gmusuml2','gmusuml2',len(pTbins)-1,pTbins,len(drbins)-1,drbins)
gmucfl1R= ROOT.TH2F('gmucfl1R','gmucfl1R',len(pTbins)-1,pTbins,len(drbins)-1,drbins)
gmucfl2R= ROOT.TH2F('gmucfl2R','gmucfl2R',len(pTbins)-1,pTbins,len(drbins)-1,drbins)
#######################################################################################  
dgmul0 = ROOT.TH2F('dgmul0','dgmul0',len(pTbins)-1,pTbins,len(drbins)-1,drbins)
dgmunfl1 = ROOT.TH2F('dgmunfl1','dgmunfl1',len(pTbins)-1,pTbins,len(drbins)-1,drbins)
dgmunfl2 = ROOT.TH2F('dgmunfl2','dgmunfl2',len(pTbins)-1,pTbins,len(drbins)-1,drbins)
dgmucfl1 = ROOT.TH2F('dgmucfl1','dgmucfl1',len(pTbins)-1,pTbins,len(drbins)-1,drbins)
dgmucfl2 = ROOT.TH2F('dgmucfl2','dgmucfl2',len(pTbins)-1,pTbins,len(drbins)-1,drbins)
#######################################################################################  
dgmusuml1= ROOT.TH2F('dgmusum11','dgmusuml1',len(pTbins)-1,pTbins,len(drbins)-1,drbins) 
dgmusuml2= ROOT.TH2F('dgmusuml2','dgmusuml2',len(pTbins)-1,pTbins,len(drbins)-1,drbins)
dgmucfl1R= ROOT.TH2F('dgmucfl1R','dgmucfl1R',len(pTbins)-1,pTbins,len(drbins)-1,drbins)
dgmucfl2R= ROOT.TH2F('dgmucfl2R','dgmucfl2R',len(pTbins)-1,pTbins,len(drbins)-1,drbins)
##################     
# Filling histos #
##################     
print('Filling histograms') 
###################### 
# slimmed standalone #
###################### 
tt.Draw("hnl_dr_12:l0_pt >> samul0")#, "abs(l0_pdgId) == 13 & l0_matched_muon_is_sa == 1 & l0_matched_muon_pt > 0 & l0_pt > 5 & abs(l0_eta) < 2.4")# & hnl_2d_disp < 4")
tt.Draw("hnl_dr_12:l1_pt >> samunfl1", "abs(l1_pdgId) == 13 & l1_matched_muon_is_sa == 1 & l1_matched_muon_charge == l1_charge & l1_matched_muon_pt > 0  & l1_pt > 5 & abs(l1_eta) < 2.4")# & hnl_2d_disp < 4")
tt.Draw("hnl_dr_12:l2_pt >> samunfl2", "abs(l2_pdgId) == 13 & l2_matched_muon_is_sa == 1 & l2_matched_muon_charge == l2_charge & l2_matched_muon_pt > 0  & l2_pt > 5 & abs(l2_eta) < 2.4")# & hnl_2d_disp < 4")
tt.Draw("hnl_dr_12:l1_pt >> samucfl1", "abs(l1_pdgId) == 13 & l1_matched_muon_is_sa == 1 & l1_matched_muon_charge != l1_charge & l1_matched_muon_pt > 0  & l1_pt > 5 & abs(l1_eta) < 2.4")# & hnl_2d_disp < 4")
tt.Draw("hnl_dr_12:l2_pt >> samucfl2", "abs(l2_pdgId) == 13 & l2_matched_muon_is_sa == 1 & l2_matched_muon_charge != l2_charge & l2_matched_muon_pt > 0  & l2_pt > 5 & abs(l2_eta) < 2.4")# & hnl_2d_disp < 4")
######################## 
# displaced standalone #
######################## 
tt.Draw("hnl_dr_12:l0_pt >> dsmul0", "abs(l0_pdgId) == 13 & l0_matched_dsmuon_pt > 0 & l0_pt > 5 & abs(l0_eta) < 2.4")# & hnl_2d_disp < 4")
tt.Draw("hnl_dr_12:l1_pt >> dsmunfl1", "abs(l1_pdgId) == 13 & l1_matched_dsmuon_charge == l1_charge & l1_matched_dsmuon_pt > 0  & l1_pt > 5 & abs(l1_eta) < 2.4")# & hnl_2d_disp < 4")
tt.Draw("hnl_dr_12:l2_pt >> dsmunfl2", "abs(l2_pdgId) == 13 & l2_matched_dsmuon_charge == l2_charge & l2_matched_dsmuon_pt > 0  & l2_pt > 5 & abs(l2_eta) < 2.4")# & hnl_2d_disp < 4")
tt.Draw("hnl_dr_12:l1_pt >> dsmucfl1", "abs(l1_pdgId) == 13 & l1_matched_dsmuon_charge != l1_charge & l1_matched_dsmuon_pt > 0  & l1_pt > 5 & abs(l1_eta) < 2.4")# & hnl_2d_disp < 4")
tt.Draw("hnl_dr_12:l2_pt >> dsmucfl2", "abs(l2_pdgId) == 13 & l2_matched_dsmuon_charge != l2_charge & l2_matched_dsmuon_pt > 0  & l2_pt > 5 & abs(l2_eta) < 2.4")# & hnl_2d_disp < 4")
################## 
# slimmed global #
################## 
tt.Draw("hnl_dr_12:l0_pt >> gmul0", "abs(l0_pdgId) == 13 & l0_matched_muon_is_gl == 1 & l0_matched_muon_pt > 0 & l0_pt > 5 & abs(l0_eta) < 2.4")# & hnl_2d_disp < 4")
tt.Draw("hnl_dr_12:l1_pt >> gmunfl1", "abs(l1_pdgId) == 13 & l1_matched_muon_is_gl == 1 & l1_matched_muon_charge == l1_charge & l1_matched_muon_pt > 0  & l1_pt > 5 & abs(l1_eta) < 2.4")# & hnl_2d_disp < 4")
tt.Draw("hnl_dr_12:l2_pt >> gmunfl2", "abs(l2_pdgId) == 13 & l2_matched_muon_is_gl == 1 & l2_matched_muon_charge == l2_charge & l2_matched_muon_pt > 0  & l2_pt > 5 & abs(l2_eta) < 2.4")# & hnl_2d_disp < 4")
tt.Draw("hnl_dr_12:l1_pt >> gmucfl1", "abs(l1_pdgId) == 13 & l1_matched_muon_is_gl == 1 & l1_matched_muon_charge != l1_charge & l1_matched_muon_pt > 0  & l1_pt > 5 & abs(l1_eta) < 2.4")# & hnl_2d_disp < 4")
tt.Draw("hnl_dr_12:l2_pt >> gmucfl2", "abs(l2_pdgId) == 13 & l2_matched_muon_is_gl == 1 & l2_matched_muon_charge != l2_charge & l2_matched_muon_pt > 0  & l2_pt > 5 & abs(l2_eta) < 2.4")# & hnl_2d_disp < 4")
#################### 
# displaced global #
####################
tt.Draw("hnl_dr_12:l0_pt >> dgmul0", "abs(l0_pdgId) == 13 & l0_matched_dgmuon_pt > 0 & l0_pt > 5 & abs(l0_eta) < 2.4")# & hnl_2d_disp < 4")
tt.Draw("hnl_dr_12:l1_pt >> dgmunfl1", "abs(l1_pdgId) == 13 & l1_matched_dgmuon_charge == l1_charge & l1_matched_dgmuon_pt > 0  & l1_pt > 5 & abs(l1_eta) < 2.4")# & hnl_2d_disp < 4")
tt.Draw("hnl_dr_12:l2_pt >> dgmunfl2", "abs(l2_pdgId) == 13 & l2_matched_dgmuon_charge == l2_charge & l2_matched_dgmuon_pt > 0  & l2_pt > 5 & abs(l2_eta) < 2.4")# & hnl_2d_disp < 4")
tt.Draw("hnl_dr_12:l1_pt >> dgmucfl1", "abs(l1_pdgId) == 13 & l1_matched_dgmuon_charge != l1_charge & l1_matched_dgmuon_pt > 0  & l1_pt > 5 & abs(l1_eta) < 2.4")# & hnl_2d_disp < 4")
tt.Draw("hnl_dr_12:l2_pt >> dgmucfl2", "abs(l2_pdgId) == 13 & l2_matched_dgmuon_charge != l2_charge & l2_matched_dgmuon_pt > 0  & l2_pt > 5 & abs(l2_eta) < 2.4")# & hnl_2d_disp < 4")
#################### 
# Computing histos #
#################### 
print('Adding and drawing histograms')
######################  
# slimmed standalone #
###################### 
samusuml1.Add(samucfl1)
samusuml1.Add(samunfl1)
samucfl1R.Divide(samucfl1,samusuml1)
##################################  
samusuml2.Add(samucfl2)
samusuml2.Add(samunfl2)
samucfl2R.Divide(samucfl2,samusuml2)
##################################  
c1.cd()
samucfl1R.Draw('colz')
c2.cd()
samucfl2R.Draw('colz')
########################  
# displaced standalone #
######################## 
dsmusuml1.Add(dsmucfl1)
dsmusuml1.Add(dsmunfl1)
dsmucfl1R.Divide(dsmucfl1,dsmusuml1)
##################################  
dsmusuml2.Add(dsmucfl2)
dsmusuml2.Add(dsmunfl2)
dsmucfl2R.Divide(dsmucfl2,dsmusuml2)
##################################  
c3.cd()
dsmucfl1R.Draw('colz')
c4.cd()
dsmucfl2R.Draw('colz')
##################  
# slimmed global #
################## 
gmusuml1.Add(gmucfl1)
gmusuml1.Add(gmunfl1)
gmucfl1R.Divide(gmucfl1,gmusuml1)
##################################  
gmusuml2.Add(gmucfl2)
gmusuml2.Add(gmunfl2)
gmucfl2R.Divide(gmucfl2,gmusuml2)
##################################  
c5.cd()
gmucfl1R.Draw('colz')
c6.cd()
gmucfl2R.Draw('colz')
####################  
# displaced global #
#################### 
dgmusuml1.Add(dgmucfl1)
dgmusuml1.Add(dgmunfl1)
dgmucfl1R.Divide(dgmucfl1,dgmusuml1)
##################################  
dgmusuml2.Add(dgmucfl2)
dgmusuml2.Add(dgmunfl2)
dgmucfl2R.Divide(dgmucfl2,dgmusuml2)
##################################  
c7.cd()
dgmucfl1R.Draw('colz')
c8.cd()
dgmucfl2R.Draw('colz')
########### 
# make-up # 
###########
histupdatelist = [dsmul0,samul0,samucfl2R,dsmucfl2R,dsmucfl1R,samucfl1R,dgmul0,gmul0,gmucfl2R,dgmucfl2R,dgmucfl1R,gmucfl1R]
##################################   
for hh in histupdatelist:
   hh.GetXaxis().SetTitle('p_{T} [GeV]')
   hh.GetYaxis().SetTitle('#Deltar')
   hh.GetZaxis().SetTitle('Chargeflip Ratio')
   hh.GetXaxis().SetTitleOffset(1.2)
   hh.GetYaxis().SetTitleOffset(1.4)
   hh.GetZaxis().SetTitleOffset(1.4)
   hh.SetAxisRange(0.001,1,"Z")
#######################
# updating and saving # 
####################### 
print('Updating and saving pads')
##################################  
for cc in [c1,c2,c3,c4,c5,c6,c7,c8]:
    cc.cd()
    cc.SetLogz()
    pf.showlogoprelimsim('CMS')
    ROOT.gStyle.SetOptStat(0)
    cc.Modified()
    cc.Update()
###################################################  
c1.SaveAs(output_dir + 'l1_samu_cf_dr_pt.root')
c1.SaveAs(output_dir + 'l1_samu_cf_dr_pt.pdf')
c2.SaveAs(output_dir + 'l2_samu_cf_dr_pt.root')
c2.SaveAs(output_dir + 'l2_samu_cf_dr_pt.pdf')
###################################################  
c3.SaveAs(output_dir + 'l1_dsmu_cf_dr_pt.root')
c3.SaveAs(output_dir + 'l1_dsmu_cf_dr_pt.pdf')
c4.SaveAs(output_dir + 'l2_dsmu_cf_dr_pt.root')
c4.SaveAs(output_dir + 'l2_dsmu_cf_dr_pt.pdf')
###################################################  
c5.SaveAs(output_dir + 'l1_gmu_cf_dr_pt.root')
c5.SaveAs(output_dir + 'l1_gmu_cf_dr_pt.pdf')
c6.SaveAs(output_dir + 'l2_gmu_cf_dr_pt.root')
c6.SaveAs(output_dir + 'l2_gmu_cf_dr_pt.pdf')
###################################################  
c7.SaveAs(output_dir + 'l1_dgmu_cf_dr_pt.root')
c7.SaveAs(output_dir + 'l1_dgmu_cf_dr_pt.pdf')
c8.SaveAs(output_dir + 'l2_dgmu_cf_dr_pt.root')
c8.SaveAs(output_dir + 'l2_dgmu_cf_dr_pt.pdf')
################################################### 
