################# 
# configuration #
#################
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
output_dir = '/afs/cern.ch/user/v/vstampf/CMSSW_8_0_30/PlotFactory/plots/ntuplev2/dr/1d/'
################################## 
ntries = tt.GetEntries()
print('Number of entries: ' + str(ntries))
################# 
# define x-axes #
#################
drbins = np.arange(0.,4.,0.25)
################### 
# create canvases #
###################
print('Preparing canvas')
c1 = ROOT.TCanvas('c1','c1 bar_d2_dr sa')
c2 = ROOT.TCanvas('c2','c2 bar_d2_dr ds')
c3 = ROOT.TCanvas('c3','c3 bar_d2_dr sa')
c4 = ROOT.TCanvas('c4','c4 bar_d2_dr ds')
c5 = ROOT.TCanvas('c5','c5 bar_d2_dr sa / ds')
c6 = ROOT.TCanvas('c6','c6 bar_d2_dr g')
c7 = ROOT.TCanvas('c7','c7 bar_d2_dr dg')
c8 = ROOT.TCanvas('c8','c8 bar_d2_dr g')
c9 = ROOT.TCanvas('c9','c9 bar_d2_dr dg')
c10= ROOT.TCanvas('c10','c10 bar_d2_dr g / dg')
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
samul0 = ROOT.TH1F('samul0','samul0',len(drbins)-1,drbins)
samunfl1 = ROOT.TH1F('samunfl1','samunfl1',len(drbins)-1,drbins)
samunfl2 = ROOT.TH1F('samunfl2','samunfl2',len(drbins)-1,drbins)
samucfl1 = ROOT.TH1F('samucfl1','samucfl1',len(drbins)-1,drbins)
samucfl2 = ROOT.TH1F('samucfl2','samucfl2',len(drbins)-1,drbins)
samusum  = ROOT.TH1F('samusum','samusum',len(drbins)-1,drbins)
samucf   = ROOT.TH1F('samucf','chargeflip',len(drbins)-1,drbins)
samunf   = ROOT.TH1F('samunf','no chargeflip',len(drbins)-1,drbins)
###################################################################  
samusuml1= ROOT.TH1F('samusuml1','samusuml1',len(drbins)-1,drbins) 
samusuml2= ROOT.TH1F('samusuml2','samusuml2',len(drbins)-1,drbins)
samucfl1R= ROOT.TH1F('samucfl1R','samucfl1R',len(drbins)-1,drbins)
samucfl2R= ROOT.TH1F('samucfl2R','samucfl2R',len(drbins)-1,drbins)
###################################################################    
dsmul0 = ROOT.TH1F('dsmul0','dsmul0',len(drbins)-1,drbins)
dsmunfl1 = ROOT.TH1F('dsmunfl1','dsmunfl1',len(drbins)-1,drbins)
dsmunfl2 = ROOT.TH1F('dsmunfl2','dsmunfl2',len(drbins)-1,drbins)
dsmucfl1 = ROOT.TH1F('dsmucfl1','dsmucfl1',len(drbins)-1,drbins)
dsmucfl2 = ROOT.TH1F('dsmucfl2','dsmucfl2',len(drbins)-1,drbins)
dsmusum  = ROOT.TH1F('dsmusum','dsmusum',len(drbins)-1,drbins)
dsmucf   = ROOT.TH1F('dsmucf','chargeflip',len(drbins)-1,drbins)
dsmunf   = ROOT.TH1F('dsmunf','no chargeflip',len(drbins)-1,drbins)
###################################################################    
dsmusuml1= ROOT.TH1F('dsmusum11','dsmusuml1',len(drbins)-1,drbins) 
dsmusuml2= ROOT.TH1F('dsmusuml2','dsmusuml2',len(drbins)-1,drbins)
dsmucfl1R= ROOT.TH1F('dsmucfl1R','dsmucfl1R',len(drbins)-1,drbins)
dsmucfl2R= ROOT.TH1F('dsmucfl2R','dsmucfl2R',len(drbins)-1,drbins)
###################################################################   
samuledr = ROOT.THStack('samuledr', 'samuledr; #Deltar; Events')
dsmuledr = ROOT.THStack('dsmuledr', 'dsmuledr; #Deltar; Events')
################# 
# global        #
################# 
gmul0 = ROOT.TH1F('gmul0','gmul0',len(drbins)-1,drbins)
gmunfl1 = ROOT.TH1F('gmunfl1','gmunfl1',len(drbins)-1,drbins)
gmunfl2 = ROOT.TH1F('gmunfl2','gmunfl2',len(drbins)-1,drbins)
gmucfl1 = ROOT.TH1F('gmucfl1','gmucfl1',len(drbins)-1,drbins)
gmucfl2 = ROOT.TH1F('gmucfl2','gmucfl2',len(drbins)-1,drbins)
gmusum  = ROOT.TH1F('gmusum','gmusum',len(drbins)-1,drbins)
gmucf   = ROOT.TH1F('gmucf','chargeflip',len(drbins)-1,drbins)
gmunf   = ROOT.TH1F('gmunf','no chargeflip',len(drbins)-1,drbins)
###################################################################   
gmusuml1= ROOT.TH1F('gmusuml1','gmusuml1',len(drbins)-1,drbins) 
gmusuml2= ROOT.TH1F('gmusuml2','gmusuml2',len(drbins)-1,drbins)
gmucfl1R= ROOT.TH1F('gmucfl1R','gmucfl1R',len(drbins)-1,drbins)
gmucfl2R= ROOT.TH1F('gmucfl2R','gmucfl2R',len(drbins)-1,drbins)
###################################################################   
dgmul0 = ROOT.TH1F('dgmul0','dgmul0',len(drbins)-1,drbins)
dgmunfl1 = ROOT.TH1F('dgmunfl1','dgmunfl1',len(drbins)-1,drbins)
dgmunfl2 = ROOT.TH1F('dgmunfl2','dgmunfl2',len(drbins)-1,drbins)
dgmucfl1 = ROOT.TH1F('dgmucfl1','dgmucfl1',len(drbins)-1,drbins)
dgmucfl2 = ROOT.TH1F('dgmucfl2','dgmucfl2',len(drbins)-1,drbins)
dgmusum  = ROOT.TH1F('dgmusum','dgmusum',len(drbins)-1,drbins)
dgmucf   = ROOT.TH1F('dgmucf','chargeflip',len(drbins)-1,drbins)
dgmunf   = ROOT.TH1F('dgmunf','no chargeflip',len(drbins)-1,drbins)
###################################################################    
dgmusuml1= ROOT.TH1F('dgmusum11','dgmusuml1',len(drbins)-1,drbins) 
dgmusuml2= ROOT.TH1F('dgmusuml2','dgmusuml2',len(drbins)-1,drbins)
dgmucfl1R= ROOT.TH1F('dgmucfl1R','dgmucfl1R',len(drbins)-1,drbins)
dgmucfl2R= ROOT.TH1F('dgmucfl2R','dgmucfl2R',len(drbins)-1,drbins)
###################################################################    
gmuledr = ROOT.THStack('gmuledr', 'gmuledr; #Deltar; Events')
dgmuledr = ROOT.THStack('dgmuledr', 'dgmuledr; #Deltar; Events')
###################################################################
# Filling histos #
##################     
print('Filling histograms') 
###################### 
# slimmed standalone #
###################### 
tt.Draw("hnl_dr_12 >> samunfl1", "abs(l1_pdgId) == 13 & l1_matched_muon_is_sa == 1 & l1_matched_muon_charge == l1_charge & l1_matched_muon_pt > 0  & l1_pt > 5 & abs(l1_eta) < 0.8 & hnl_2d_disp > 4 & hnl_2d_disp < 120")
tt.Draw("hnl_dr_12 >> samunfl2", "abs(l2_pdgId) == 13 & l2_matched_muon_is_sa == 1 & l2_matched_muon_charge == l2_charge & l2_matched_muon_pt > 0  & l2_pt > 5 & abs(l2_eta) < 0.8 & hnl_2d_disp > 4 & hnl_2d_disp < 120")
tt.Draw("hnl_dr_12 >> samucfl1", "abs(l1_pdgId) == 13 & l1_matched_muon_is_sa == 1 & l1_matched_muon_charge != l1_charge & l1_matched_muon_pt > 0  & l1_pt > 5 & abs(l1_eta) < 0.8 & hnl_2d_disp > 4 & hnl_2d_disp < 120")
tt.Draw("hnl_dr_12 >> samucfl2", "abs(l2_pdgId) == 13 & l2_matched_muon_is_sa == 1 & l2_matched_muon_charge != l2_charge & l2_matched_muon_pt > 0  & l2_pt > 5 & abs(l2_eta) < 0.8 & hnl_2d_disp > 4 & hnl_2d_disp < 120")
######################## 
# displaced standalone #
######################## 
tt.Draw("hnl_dr_12 >> dsmunfl1", "abs(l1_pdgId) == 13 & l1_matched_dsmuon_charge == l1_charge & l1_matched_dsmuon_pt > 0  & l1_pt > 5 & abs(l1_eta) < 0.8 & hnl_2d_disp > 4 & hnl_2d_disp < 120")
tt.Draw("hnl_dr_12 >> dsmunfl2", "abs(l2_pdgId) == 13 & l2_matched_dsmuon_charge == l2_charge & l2_matched_dsmuon_pt > 0  & l2_pt > 5 & abs(l2_eta) < 0.8 & hnl_2d_disp > 4 & hnl_2d_disp < 120")
tt.Draw("hnl_dr_12 >> dsmucfl1", "abs(l1_pdgId) == 13 & l1_matched_dsmuon_charge != l1_charge & l1_matched_dsmuon_pt > 0  & l1_pt > 5 & abs(l1_eta) < 0.8 & hnl_2d_disp > 4 & hnl_2d_disp < 120")
tt.Draw("hnl_dr_12 >> dsmucfl2", "abs(l2_pdgId) == 13 & l2_matched_dsmuon_charge != l2_charge & l2_matched_dsmuon_pt > 0  & l2_pt > 5 & abs(l2_eta) < 0.8 & hnl_2d_disp > 4 & hnl_2d_disp < 120")
################## 
# slimmed global #
################## 
tt.Draw("hnl_dr_12 >> gmunfl1", "abs(l1_pdgId) == 13 & l1_matched_muon_is_gl == 1 & l1_matched_muon_charge == l1_charge & l1_matched_muon_pt > 0  & l1_pt > 5 & abs(l1_eta) < 0.8 & hnl_2d_disp > 4 & hnl_2d_disp < 120")
tt.Draw("hnl_dr_12 >> gmunfl2", "abs(l2_pdgId) == 13 & l2_matched_muon_is_gl == 1 & l2_matched_muon_charge == l2_charge & l2_matched_muon_pt > 0  & l2_pt > 5 & abs(l2_eta) < 0.8 & hnl_2d_disp > 4 & hnl_2d_disp < 120")
tt.Draw("hnl_dr_12 >> gmucfl1", "abs(l1_pdgId) == 13 & l1_matched_muon_is_gl == 1 & l1_matched_muon_charge != l1_charge & l1_matched_muon_pt > 0  & l1_pt > 5 & abs(l1_eta) < 0.8 & hnl_2d_disp > 4 & hnl_2d_disp < 120")
tt.Draw("hnl_dr_12 >> gmucfl2", "abs(l2_pdgId) == 13 & l2_matched_muon_is_gl == 1 & l2_matched_muon_charge != l2_charge & l2_matched_muon_pt > 0  & l2_pt > 5 & abs(l2_eta) < 0.8 & hnl_2d_disp > 4 & hnl_2d_disp < 120")
#################### 
# displaced global #
####################
tt.Draw("hnl_dr_12 >> dgmunfl1", "abs(l1_pdgId) == 13 & l1_matched_dgmuon_charge == l1_charge & l1_matched_dgmuon_pt > 0  & l1_pt > 5 & abs(l1_eta) < 0.8 & hnl_2d_disp > 4 & hnl_2d_disp < 120")
tt.Draw("hnl_dr_12 >> dgmunfl2", "abs(l2_pdgId) == 13 & l2_matched_dgmuon_charge == l2_charge & l2_matched_dgmuon_pt > 0  & l2_pt > 5 & abs(l2_eta) < 0.8 & hnl_2d_disp > 4 & hnl_2d_disp < 120")
tt.Draw("hnl_dr_12 >> dgmucfl1", "abs(l1_pdgId) == 13 & l1_matched_dgmuon_charge != l1_charge & l1_matched_dgmuon_pt > 0  & l1_pt > 5 & abs(l1_eta) < 0.8 & hnl_2d_disp > 4 & hnl_2d_disp < 120")
tt.Draw("hnl_dr_12 >> dgmucfl2", "abs(l2_pdgId) == 13 & l2_matched_dgmuon_charge != l2_charge & l2_matched_dgmuon_pt > 0  & l2_pt > 5 & abs(l2_eta) < 0.8 & hnl_2d_disp > 4 & hnl_2d_disp < 120")
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
samucfl1R.SetMarkerColor(ROOT.kBlue+1)
samucfl2R.SetMarkerColor(ROOT.kRed+1)
##################################  
c1.cd()
samucfl2R.Draw()
samucfl1R.Draw('same')
c1.BuildLegend()
##################################  
c3.cd()
samusuml2.SetFillColor(ROOT.kRed+1)
samusuml1.SetFillColor(ROOT.kBlue+1)
samuledr.Add(samusuml1)
samuledr.Add(samusuml2)
samuledr.Draw('hist,nostack')
c3.BuildLegend()
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
dsmucfl1R.SetMarkerColor(ROOT.kBlue+1)
dsmucfl2R.SetMarkerColor(ROOT.kRed+1)
##################################  
c2.cd()
dsmucfl2R.Draw()
dsmucfl1R.Draw('same')
c2.BuildLegend()
##################################  
c4.cd()
dsmusuml2.SetFillColor(ROOT.kRed+1)
dsmusuml1.SetFillColor(ROOT.kBlue+1)
dsmuledr.Add(dsmusuml1)
dsmuledr.Add(dsmusuml2)
dsmuledr.Draw('hist,nostack')
c4.BuildLegend()
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
gmucfl1R.SetMarkerColor(ROOT.kBlue+1)
gmucfl2R.SetMarkerColor(ROOT.kRed+1)
##################################  
c6.cd()
gmucfl2R.Draw()
gmucfl1R.Draw('same')
c6.BuildLegend()
##################################  
c8.cd()
gmusuml2.SetFillColor(ROOT.kRed+1)
gmusuml1.SetFillColor(ROOT.kBlue+1)
gmuledr.Add(gmusuml1)
gmuledr.Add(gmusuml2)
gmuledr.Draw('hist,nostack')
c8.BuildLegend()
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
dgmucfl1R.SetMarkerColor(ROOT.kBlue+1)
dgmucfl2R.SetMarkerColor(ROOT.kRed+1)
##################################  
c7.cd()
dgmucfl2R.Draw()
dgmucfl1R.Draw('same')
c7.BuildLegend()
##################################  
c9.cd()
dgmusuml2.SetFillColor(ROOT.kRed+1)
dgmusuml1.SetFillColor(ROOT.kBlue+1)
dgmuledr.Add(dgmusuml1)
dgmuledr.Add(dgmusuml2)
dgmuledr.Draw('hist,nostack')
c9.BuildLegend()
################  
# total ratios #
################ 
c5.cd()
samunfl1.Add(samunfl2)
samucfl1.Add(samucfl2)
samusum.Add(samucfl1)
samusum.Add(samunfl1)
samucf.Divide(samucfl1,samusum)
samucf.Draw()
samucf.SetMarkerColor(ROOT.kMagenta+2)
##################################  
dsmunfl1.Add(dsmunfl2)
dsmucfl1.Add(dsmucfl2)
dsmusum.Add(dsmucfl1)
dsmusum.Add(dsmunfl1)
dsmucf.Divide(dsmucfl1,dsmusum)
dsmucf.Draw('same')
dsmucf.SetMarkerColor(ROOT.kRed+2)
##################################  
c10.cd()
gmunfl1.Add(gmunfl2)
gmucfl1.Add(gmucfl2)
gmusum.Add(gmucfl1)
gmusum.Add(gmunfl1)
gmucf.Divide(gmucfl1,gmusum)
gmucf.Draw()
gmucf.SetMarkerColor(ROOT.kCyan+2)
##################################  
dgmunfl1.Add(dgmunfl2)
dgmucfl1.Add(dgmucfl2)
dgmusum.Add(dgmucfl1)
dgmusum.Add(dgmunfl1)
dgmucf.Divide(dgmucfl1,dgmusum)
dgmucf.Draw('same')
dgmucf.SetMarkerColor(ROOT.kGreen+2)
########### 
# make-up # 
###########
histupdatelist = [samucf,samucfl2R,dsmucfl2R,dsmucfl1R,samucfl1R,gmucf,gmucfl2R,dgmucfl2R,dgmucfl1R,gmucfl1R]
##################################   
for hh in histupdatelist:
   hh.GetXaxis().SetTitle('#Deltar')
   hh.GetYaxis().SetTitle('Chargeflip Ratio')
   hh.GetXaxis().SetTitleOffset(1.2)
   hh.GetYaxis().SetTitleOffset(1.4)
##################################  
samu  = samusum.GetEntries()
dsamu = dsmusum.GetEntries()
gmu   = gmusum.GetEntries()
dgmu  = dgmusum.GetEntries()
##################################  
c5.cd()
leg5 = ROOT.TLegend(.18,.76,.4,.9)
leg5.SetBorderSize(0)
leg5.SetFillColor(ROOT.kWhite)
leg5.SetFillStyle(0)
leg5.SetTextFont(42)
leg5.SetTextSize(0.045)
leg5.AddEntry(dsmucf, 'dSA#mu', 'EP')
leg5.AddEntry(samucf, 'SA#mu', 'EP') 
leg5.Draw('apez same')
pf.showlogoprelimsim('CMS')
##################################  
c10.cd()
leg10 = ROOT.TLegend(.18,.76,.4,.9)
leg10.SetBorderSize(0)
leg10.SetFillColor(ROOT.kWhite)
leg10.SetFillStyle(0)
leg10.SetTextFont(42)
leg10.SetTextSize(0.045)
leg10.AddEntry(dgmucf, 'dG#mu', 'EP')
leg10.AddEntry(gmucf, 'G#mu', 'EP') 
leg10.Draw('apez same')
pf.showlogoprelimsim('CMS')
#######################
# updating and saving # 
####################### 
print('Updating and saving pads')
##################################  
for cc in [c1,c2,c3,c4,c5,c6,c7,c8,c9,c10]:
    cc.Modified()
    cc.Update()
####################################################  
c1.SaveAs(output_dir + 'bar_d2_cf_dr_samu_l12.root')
c2.SaveAs(output_dir + 'bar_d2_cf_dr_dsmu_l12.root')
c3.SaveAs(output_dir + 'bar_d2_dr_samu_l12.root')
c4.SaveAs(output_dir + 'bar_d2_dr_dsmu_l12.root')
c5.SaveAs(output_dir + 'bar_d2_cf_dr_sa.root')
c6.SaveAs(output_dir + 'bar_d2_cf_dr_gmu_l12.root')
c7.SaveAs(output_dir + 'bar_d2_cf_dr_dgmu_l12.root')
c8.SaveAs(output_dir + 'bar_d2_cf_dr_gmu_l12.root')
c9.SaveAs(output_dir + 'bar_d2_dr_dgmu_l12.root')
c10.SaveAs(output_dir + 'bar_d2_cf_dr_gl.root')
################################################### 
print('dSA#mu: %.2f / SA#mu: %.2f M entries'%((samu / 1000000.),dsamu / 1000000.))
print('dG#mu: %.2f / G#mu: %.2f M entries'%((gmu / 1000000.),dgmu / 1000000.))
