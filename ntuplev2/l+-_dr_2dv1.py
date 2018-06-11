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
c1 = ROOT.TCanvas('c1','c1 sa lp',600,500)
c2 = ROOT.TCanvas('c2','c2 sa lm',600,500)
c3 = ROOT.TCanvas('c3','c3 ds lp',600,500)
c4 = ROOT.TCanvas('c4','c4 ds lm',600,500)
c5 = ROOT.TCanvas('c5','c5 g lp',600,500)
c6 = ROOT.TCanvas('c6','c6 g lm',600,500)
c7 = ROOT.TCanvas('c7','c7 dg lp',600,500)
c8 = ROOT.TCanvas('c8','c8 dg lm',600,500)
##################### 
# create histograms #
#####################
# lp = '+'          #
# lm = '-'          #
#####################  
# standalone        #
##################### 
samunflp = ROOT.TH2F('samunflp','samunflp',len(pTbins)-1,pTbins,len(drbins)-1,drbins)
samunflm = ROOT.TH2F('samunflm','samunflm',len(pTbins)-1,pTbins,len(drbins)-1,drbins)
samucflp = ROOT.TH2F('samucflp','samucflp',len(pTbins)-1,pTbins,len(drbins)-1,drbins)
samucflm = ROOT.TH2F('samucflm','samucflm',len(pTbins)-1,pTbins,len(drbins)-1,drbins)
#######################################################################################  
samusumlp= ROOT.TH2F('samusumlp','samusumlp',len(pTbins)-1,pTbins,len(drbins)-1,drbins) 
samusumlm= ROOT.TH2F('samusumlm','samusumlm',len(pTbins)-1,pTbins,len(drbins)-1,drbins)
samucflpR= ROOT.TH2F('samucflpR','samucflpR',len(pTbins)-1,pTbins,len(drbins)-1,drbins)
samucflmR= ROOT.TH2F('samucflmR','samucflmR',len(pTbins)-1,pTbins,len(drbins)-1,drbins)
#######################################################################################  
dsmunflp = ROOT.TH2F('dsmunflp','dsmunflp',len(pTbins)-1,pTbins,len(drbins)-1,drbins)
dsmunflm = ROOT.TH2F('dsmunflm','dsmunflm',len(pTbins)-1,pTbins,len(drbins)-1,drbins)
dsmucflp = ROOT.TH2F('dsmucflp','dsmucflp',len(pTbins)-1,pTbins,len(drbins)-1,drbins)
dsmucflm = ROOT.TH2F('dsmucflm','dsmucflm',len(pTbins)-1,pTbins,len(drbins)-1,drbins)
#######################################################################################  
dsmusumlp= ROOT.TH2F('dsmusum11','dsmusumlp',len(pTbins)-1,pTbins,len(drbins)-1,drbins) 
dsmusumlm= ROOT.TH2F('dsmusumlm','dsmusumlm',len(pTbins)-1,pTbins,len(drbins)-1,drbins)
dsmucflpR= ROOT.TH2F('dsmucflpR','dsmucflpR',len(pTbins)-1,pTbins,len(drbins)-1,drbins)
dsmucflmR= ROOT.TH2F('dsmucflmR','dsmucflmR',len(pTbins)-1,pTbins,len(drbins)-1,drbins)
################# 
# global        #
################# 
gmunflp = ROOT.TH2F('gmunflp','gmunflp',len(pTbins)-1,pTbins,len(drbins)-1,drbins)
gmunflm = ROOT.TH2F('gmunflm','gmunflm',len(pTbins)-1,pTbins,len(drbins)-1,drbins)
gmucflp = ROOT.TH2F('gmucflp','gmucflp',len(pTbins)-1,pTbins,len(drbins)-1,drbins)
gmucflm = ROOT.TH2F('gmucflm','gmucflm',len(pTbins)-1,pTbins,len(drbins)-1,drbins)
#######################################################################################  
gmusumlp= ROOT.TH2F('gmusumlp','gmusumlp',len(pTbins)-1,pTbins,len(drbins)-1,drbins) 
gmusumlm= ROOT.TH2F('gmusumlm','gmusumlm',len(pTbins)-1,pTbins,len(drbins)-1,drbins)
gmucflpR= ROOT.TH2F('gmucflpR','gmucflpR',len(pTbins)-1,pTbins,len(drbins)-1,drbins)
gmucflmR= ROOT.TH2F('gmucflmR','gmucflmR',len(pTbins)-1,pTbins,len(drbins)-1,drbins)
#######################################################################################  
dgmunflp = ROOT.TH2F('dgmunflp','dgmunflp',len(pTbins)-1,pTbins,len(drbins)-1,drbins)
dgmunflm = ROOT.TH2F('dgmunflm','dgmunflm',len(pTbins)-1,pTbins,len(drbins)-1,drbins)
dgmucflp = ROOT.TH2F('dgmucflp','dgmucflp',len(pTbins)-1,pTbins,len(drbins)-1,drbins)
dgmucflm = ROOT.TH2F('dgmucflm','dgmucflm',len(pTbins)-1,pTbins,len(drbins)-1,drbins)
#######################################################################################  
dgmusumlp= ROOT.TH2F('dgmusum11','dgmusumlp',len(pTbins)-1,pTbins,len(drbins)-1,drbins) 
dgmusumlm= ROOT.TH2F('dgmusumlm','dgmusumlm',len(pTbins)-1,pTbins,len(drbins)-1,drbins)
dgmucflpR= ROOT.TH2F('dgmucflpR','dgmucflpR',len(pTbins)-1,pTbins,len(drbins)-1,drbins)
dgmucflmR= ROOT.TH2F('dgmucflmR','dgmucflmR',len(pTbins)-1,pTbins,len(drbins)-1,drbins)
##################     
# Filling histos #
##################     
print('Filling histograms') 
###################### 
# slimmed standalone #
###################### 
tt.Draw("hnl_dr_12:l1_pt >> samunflp", "abs(l1_pdgId) == 13 & l1_matched_muon_is_sa == 1 & l1_matched_muon_charge == l1_charge & l1_charge == 1 & l1_matched_muon_pt > 0  & l1_pt > 5 & abs(l1_eta) < 2.4")# & hnl_2d_disp < 4")
tt.Draw("hnl_dr_12:l2_pt >> samunflm", "abs(l2_pdgId) == 13 & l2_matched_muon_is_sa == 1 & l2_matched_muon_charge == l2_charge & l2_charge == -1 & l2_matched_muon_pt > 0  & l2_pt > 5 & abs(l2_eta) < 2.4")# & hnl_2d_disp < 4")
tt.Draw("hnl_dr_12:l1_pt >> samucflp", "abs(l1_pdgId) == 13 & l1_matched_muon_is_sa == 1 & l1_matched_muon_charge != l1_charge & l1_charge == 1 & l1_matched_muon_pt > 0  & l1_pt > 5 & abs(l1_eta) < 2.4")# & hnl_2d_disp < 4")
tt.Draw("hnl_dr_12:l2_pt >> samucflm", "abs(l2_pdgId) == 13 & l2_matched_muon_is_sa == 1 & l2_matched_muon_charge != l2_charge & l2_charge == -1 & l2_matched_muon_pt > 0  & l2_pt > 5 & abs(l2_eta) < 2.4")# & hnl_2d_disp < 4")
######################## 
# displaced standalone #
######################## 
tt.Draw("hnl_dr_12:l1_pt >> dsmunflp", "abs(l1_pdgId) == 13 & l1_matched_dsmuon_charge == l1_charge & l1_charge == 1 & l1_matched_dsmuon_pt > 0  & l1_pt > 5 & abs(l1_eta) < 2.4")# & hnl_2d_disp < 4")
tt.Draw("hnl_dr_12:l2_pt >> dsmunflm", "abs(l2_pdgId) == 13 & l2_matched_dsmuon_charge == l2_charge & l2_charge == -1 & l2_matched_dsmuon_pt > 0  & l2_pt > 5 & abs(l2_eta) < 2.4")# & hnl_2d_disp < 4")
tt.Draw("hnl_dr_12:l1_pt >> dsmucflp", "abs(l1_pdgId) == 13 & l1_matched_dsmuon_charge != l1_charge & l1_charge == 1 & l1_matched_dsmuon_pt > 0  & l1_pt > 5 & abs(l1_eta) < 2.4")# & hnl_2d_disp < 4")
tt.Draw("hnl_dr_12:l2_pt >> dsmucflm", "abs(l2_pdgId) == 13 & l2_matched_dsmuon_charge != l2_charge & l2_charge == -1 & l2_matched_dsmuon_pt > 0  & l2_pt > 5 & abs(l2_eta) < 2.4")# & hnl_2d_disp < 4")
################## 
# slimmed global #
################## 
tt.Draw("hnl_dr_12:l1_pt >> gmunflp", "abs(l1_pdgId) == 13 & l1_matched_muon_is_gl == 1 & l1_matched_muon_charge == l1_charge & l1_charge == 1 & l1_matched_muon_pt > 0  & l1_pt > 5 & abs(l1_eta) < 2.4")# & hnl_2d_disp < 4")
tt.Draw("hnl_dr_12:l2_pt >> gmunflm", "abs(l2_pdgId) == 13 & l2_matched_muon_is_gl == 1 & l2_matched_muon_charge == l2_charge & l2_charge == -1 & l2_matched_muon_pt > 0  & l2_pt > 5 & abs(l2_eta) < 2.4")# & hnl_2d_disp < 4")
tt.Draw("hnl_dr_12:l1_pt >> gmucflp", "abs(l1_pdgId) == 13 & l1_matched_muon_is_gl == 1 & l1_matched_muon_charge != l1_charge & l1_charge == 1 & l1_matched_muon_pt > 0  & l1_pt > 5 & abs(l1_eta) < 2.4")# & hnl_2d_disp < 4")
tt.Draw("hnl_dr_12:l2_pt >> gmucflm", "abs(l2_pdgId) == 13 & l2_matched_muon_is_gl == 1 & l2_matched_muon_charge != l2_charge & l2_charge == -1 & l2_matched_muon_pt > 0  & l2_pt > 5 & abs(l2_eta) < 2.4")# & hnl_2d_disp < 4")
#################### 
# displaced global #
####################
tt.Draw("hnl_dr_12:l1_pt >> dgmunflp", "abs(l1_pdgId) == 13 & l1_matched_dgmuon_charge == l1_charge & l1_charge == 1 & l1_matched_dgmuon_pt > 0  & l1_pt > 5 & abs(l1_eta) < 2.4")# & hnl_2d_disp < 4")
tt.Draw("hnl_dr_12:l2_pt >> dgmunflm", "abs(l2_pdgId) == 13 & l2_matched_dgmuon_charge == l2_charge & l2_charge == -1 & l2_matched_dgmuon_pt > 0  & l2_pt > 5 & abs(l2_eta) < 2.4")# & hnl_2d_disp < 4")
tt.Draw("hnl_dr_12:l1_pt >> dgmucflp", "abs(l1_pdgId) == 13 & l1_matched_dgmuon_charge != l1_charge & l1_charge == 1 & l1_matched_dgmuon_pt > 0  & l1_pt > 5 & abs(l1_eta) < 2.4")# & hnl_2d_disp < 4")
tt.Draw("hnl_dr_12:l2_pt >> dgmucflm", "abs(l2_pdgId) == 13 & l2_matched_dgmuon_charge != l2_charge & l2_charge == -1 & l2_matched_dgmuon_pt > 0  & l2_pt > 5 & abs(l2_eta) < 2.4")# & hnl_2d_disp < 4")
#################### 
# Computing histos #
#################### 
print('Adding and drawing histograms')
######################  
# slimmed standalone #
###################### 
samusumlp.Add(samucflp)
samusumlp.Add(samunflp)
samucflpR.Divide(samucflp,samusumlp)
##################################  
samusumlm.Add(samucflm)
samusumlm.Add(samunflm)
samucflmR.Divide(samucflm,samusumlm)
##################################  
c1.cd()
samucflpR.Draw('colz')
c2.cd()
samucflmR.Draw('colz')
########################  
# displaced standalone #
######################## 
dsmusumlp.Add(dsmucflp)
dsmusumlp.Add(dsmunflp)
dsmucflpR.Divide(dsmucflp,dsmusumlp)
##################################  
dsmusumlm.Add(dsmucflm)
dsmusumlm.Add(dsmunflm)
dsmucflmR.Divide(dsmucflm,dsmusumlm)
##################################  
c3.cd()
dsmucflpR.Draw('colz')
c4.cd()
dsmucflmR.Draw('colz')
##################  
# slimmed global #
################## 
gmusumlp.Add(gmucflp)
gmusumlp.Add(gmunflp)
gmucflpR.Divide(gmucflp,gmusumlp)
##################################  
gmusumlm.Add(gmucflm)
gmusumlm.Add(gmunflm)
gmucflmR.Divide(gmucflm,gmusumlm)
##################################  
c5.cd()
gmucflpR.Draw('colz')
c6.cd()
gmucflmR.Draw('colz')
####################  
# displaced global #
#################### 
dgmusumlp.Add(dgmucflp)
dgmusumlp.Add(dgmunflp)
dgmucflpR.Divide(dgmucflp,dgmusumlp)
##################################  
dgmusumlm.Add(dgmucflm)
dgmusumlm.Add(dgmunflm)
dgmucflmR.Divide(dgmucflm,dgmusumlm)
##################################  
c7.cd()
dgmucflpR.Draw('colz')
c8.cd()
dgmucflmR.Draw('colz')
########### 
# make-up # 
###########
histupdatelist = [samucflmR,dsmucflmR,dsmucflpR,samucflpR,gmucflmR,dgmucflmR,dgmucflpR,gmucflpR]
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
c1.SaveAs(output_dir + 'lp_samu_cf_dr_pt.root')
c1.SaveAs(output_dir + 'lp_samu_cf_dr_pt.pdf')
c2.SaveAs(output_dir + 'lm_samu_cf_dr_pt.root')
c2.SaveAs(output_dir + 'lm_samu_cf_dr_pt.pdf')
###################################################  
c3.SaveAs(output_dir + 'lp_dsmu_cf_dr_pt.root')
c3.SaveAs(output_dir + 'lp_dsmu_cf_dr_pt.pdf')
c4.SaveAs(output_dir + 'lm_dsmu_cf_dr_pt.root')
c4.SaveAs(output_dir + 'lm_dsmu_cf_dr_pt.pdf')
###################################################  
c5.SaveAs(output_dir + 'lp_gmu_cf_dr_pt.root')
c5.SaveAs(output_dir + 'lp_gmu_cf_dr_pt.pdf')
c6.SaveAs(output_dir + 'lm_gmu_cf_dr_pt.root')
c6.SaveAs(output_dir + 'lm_gmu_cf_dr_pt.pdf')
###################################################  
c7.SaveAs(output_dir + 'lp_dgmu_cf_dr_pt.root')
c7.SaveAs(output_dir + 'lp_dgmu_cf_dr_pt.pdf')
c8.SaveAs(output_dir + 'lm_dgmu_cf_dr_pt.root')
c8.SaveAs(output_dir + 'lm_dgmu_cf_dr_pt.pdf')
################################################### 
