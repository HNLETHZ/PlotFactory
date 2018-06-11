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
ROOT.gROOT.SetBatch(True)    # don't open X11 forwarding (running screen)
################################## 
pf.setpfstyle()
bewl = input("Makechain: True or False\n")
tt = pf.makechain(bewl)
output_dir = '/afs/cern.ch/user/v/vstampf/CMSSW_8_0_30/PlotFactory/plots/ntuplev2/'
################################## 
ntries = tt.GetEntries()
print('Number of entries: ' + str(ntries))
################# 
# define x-axes #
#################
pTbins = np.arange(5.,73,5)
################### 
# create canvases #
###################
print('Preparing canvas')
c1 = ROOT.TCanvas('c1','c1 cap_d2 sa')
c2 = ROOT.TCanvas('c2','c2 cap_d2 ds')
c3 = ROOT.TCanvas('c3','c3 cap_d2 sa')
c4 = ROOT.TCanvas('c4','c4 cap_d2 ds')
c5 = ROOT.TCanvas('c5','c5 cap_d2 sa / ds')
c6 = ROOT.TCanvas('c6','c6 cap_d2 g')
c7 = ROOT.TCanvas('c7','c7 cap_d2 dg')
c8 = ROOT.TCanvas('c8','c8 cap_d2 g')
c9 = ROOT.TCanvas('c9','c9 cap_d2 dg')
c10= ROOT.TCanvas('c10','c10 cap_d2 g / dg')
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
samul0 = ROOT.TH1F('samul0','samul0',len(pTbins)-1,pTbins)
samunfl1 = ROOT.TH1F('samunfl1','samunfl1',len(pTbins)-1,pTbins)
samunfl2 = ROOT.TH1F('samunfl2','samunfl2',len(pTbins)-1,pTbins)
samucfl1 = ROOT.TH1F('samucfl1','samucfl1',len(pTbins)-1,pTbins)
samucfl2 = ROOT.TH1F('samucfl2','samucfl2',len(pTbins)-1,pTbins)
samusum  = ROOT.TH1F('samusum','samusum',len(pTbins)-1,pTbins)
samucf   = ROOT.TH1F('samucf','chargeflip',len(pTbins)-1,pTbins)
samunf   = ROOT.TH1F('samunf','no chargeflip',len(pTbins)-1,pTbins)
###################################################################  
samusuml1= ROOT.TH1F('samusuml1','samusuml1',len(pTbins)-1,pTbins) 
samusuml2= ROOT.TH1F('samusuml2','samusuml2',len(pTbins)-1,pTbins)
samucfl1R= ROOT.TH1F('samucfl1R','samucfl1R',len(pTbins)-1,pTbins)
samucfl2R= ROOT.TH1F('samucfl2R','samucfl2R',len(pTbins)-1,pTbins)
###################################################################    
dsmul0 = ROOT.TH1F('dsmul0','dsmul0',len(pTbins)-1,pTbins)
dsmunfl1 = ROOT.TH1F('dsmunfl1','dsmunfl1',len(pTbins)-1,pTbins)
dsmunfl2 = ROOT.TH1F('dsmunfl2','dsmunfl2',len(pTbins)-1,pTbins)
dsmucfl1 = ROOT.TH1F('dsmucfl1','dsmucfl1',len(pTbins)-1,pTbins)
dsmucfl2 = ROOT.TH1F('dsmucfl2','dsmucfl2',len(pTbins)-1,pTbins)
dsmusum  = ROOT.TH1F('dsmusum','dsmusum',len(pTbins)-1,pTbins)
dsmucf   = ROOT.TH1F('dsmucf','chargeflip',len(pTbins)-1,pTbins)
dsmunf   = ROOT.TH1F('dsmunf','no chargeflip',len(pTbins)-1,pTbins)
###################################################################    
dsmusuml1= ROOT.TH1F('dsmusum11','dsmusuml1',len(pTbins)-1,pTbins) 
dsmusuml2= ROOT.TH1F('dsmusuml2','dsmusuml2',len(pTbins)-1,pTbins)
dsmucfl1R= ROOT.TH1F('dsmucfl1R','dsmucfl1R',len(pTbins)-1,pTbins)
dsmucfl2R= ROOT.TH1F('dsmucfl2R','dsmucfl2R',len(pTbins)-1,pTbins)
###################################################################   
samulepT = ROOT.THStack('samulepT', 'samulepT; p_{T}[GeV]; Events')
dsmulepT = ROOT.THStack('dsmulepT', 'dsmulepT; p_{T}[GeV]; Events')
################# 
# global        #
################# 
gmul0 = ROOT.TH1F('gmul0','gmul0',len(pTbins)-1,pTbins)
gmunfl1 = ROOT.TH1F('gmunfl1','gmunfl1',len(pTbins)-1,pTbins)
gmunfl2 = ROOT.TH1F('gmunfl2','gmunfl2',len(pTbins)-1,pTbins)
gmucfl1 = ROOT.TH1F('gmucfl1','gmucfl1',len(pTbins)-1,pTbins)
gmucfl2 = ROOT.TH1F('gmucfl2','gmucfl2',len(pTbins)-1,pTbins)
gmusum  = ROOT.TH1F('gmusum','gmusum',len(pTbins)-1,pTbins)
gmucf   = ROOT.TH1F('gmucf','chargeflip',len(pTbins)-1,pTbins)
gmunf   = ROOT.TH1F('gmunf','no chargeflip',len(pTbins)-1,pTbins)
###################################################################   
gmusuml1= ROOT.TH1F('gmusuml1','gmusuml1',len(pTbins)-1,pTbins) 
gmusuml2= ROOT.TH1F('gmusuml2','gmusuml2',len(pTbins)-1,pTbins)
gmucfl1R= ROOT.TH1F('gmucfl1R','gmucfl1R',len(pTbins)-1,pTbins)
gmucfl2R= ROOT.TH1F('gmucfl2R','gmucfl2R',len(pTbins)-1,pTbins)
###################################################################   
dgmul0 = ROOT.TH1F('dgmul0','dgmul0',len(pTbins)-1,pTbins)
dgmunfl1 = ROOT.TH1F('dgmunfl1','dgmunfl1',len(pTbins)-1,pTbins)
dgmunfl2 = ROOT.TH1F('dgmunfl2','dgmunfl2',len(pTbins)-1,pTbins)
dgmucfl1 = ROOT.TH1F('dgmucfl1','dgmucfl1',len(pTbins)-1,pTbins)
dgmucfl2 = ROOT.TH1F('dgmucfl2','dgmucfl2',len(pTbins)-1,pTbins)
dgmusum  = ROOT.TH1F('dgmusum','dgmusum',len(pTbins)-1,pTbins)
dgmucf   = ROOT.TH1F('dgmucf','chargeflip',len(pTbins)-1,pTbins)
dgmunf   = ROOT.TH1F('dgmunf','no chargeflip',len(pTbins)-1,pTbins)
###################################################################    
dgmusuml1= ROOT.TH1F('dgmusum11','dgmusuml1',len(pTbins)-1,pTbins) 
dgmusuml2= ROOT.TH1F('dgmusuml2','dgmusuml2',len(pTbins)-1,pTbins)
dgmucfl1R= ROOT.TH1F('dgmucfl1R','dgmucfl1R',len(pTbins)-1,pTbins)
dgmucfl2R= ROOT.TH1F('dgmucfl2R','dgmucfl2R',len(pTbins)-1,pTbins)
###################################################################    
gmulepT = ROOT.THStack('gmulepT', 'gmulepT; p_{T}[GeV]; Events')
dgmulepT = ROOT.THStack('dgmulepT', 'dgmulepT; p_{T}[GeV]; Events')
###################################################################
# Filling histos #
##################     
print('Filling histograms') 
###################### 
# slimmed standalone #
###################### 
tt.Draw("l0_pt >> samul0", "abs(l0_pdgId) == 13 & l0_matched_muon_is_sa == 1 & l0_matched_muon_pt > 0 & l0_pt > 5 & abs(l0_eta) > 1.2 & abs(l0_eta) < 2.4 & hnl_2d_disp > 4 & hnl_2d_disp < 120")
tt.Draw("l1_pt >> samunfl1", "abs(l1_pdgId) == 13 & l1_matched_muon_is_sa == 1 & l1_matched_muon_charge == l1_charge & l1_matched_muon_pt > 0  & l1_pt > 5 & abs(l1_eta) > 1.2 & abs(l1_eta) < 2.4 & hnl_2d_disp > 4 & hnl_2d_disp < 120")
tt.Draw("l2_pt >> samunfl2", "abs(l2_pdgId) == 13 & l2_matched_muon_is_sa == 1 & l2_matched_muon_charge == l2_charge & l2_matched_muon_pt > 0  & l2_pt > 5 & abs(l2_eta) > 1.2 & abs(l2_eta) < 2.4 & hnl_2d_disp > 4 & hnl_2d_disp < 120")
tt.Draw("l1_pt >> samucfl1", "abs(l1_pdgId) == 13 & l1_matched_muon_is_sa == 1 & l1_matched_muon_charge != l1_charge & l1_matched_muon_pt > 0  & l1_pt > 5 & abs(l1_eta) > 1.2 & abs(l1_eta) < 2.4 & hnl_2d_disp > 4 & hnl_2d_disp < 120")
tt.Draw("l2_pt >> samucfl2", "abs(l2_pdgId) == 13 & l2_matched_muon_is_sa == 1 & l2_matched_muon_charge != l2_charge & l2_matched_muon_pt > 0  & l2_pt > 5 & abs(l2_eta) > 1.2 & abs(l2_eta) < 2.4 & hnl_2d_disp > 4 & hnl_2d_disp < 120")
######################## 
# displaced standalone #
######################## 
tt.Draw("l0_pt >> dsmul0", "abs(l0_pdgId) == 13 & l0_matched_dsmuon_pt > 0 & l0_pt > 5 & abs(l0_eta) > 1.2 & abs(l0_eta) < 2.4 & hnl_2d_disp > 4 & hnl_2d_disp < 120")
tt.Draw("l1_pt >> dsmunfl1", "abs(l1_pdgId) == 13 & l1_matched_dsmuon_charge == l1_charge & l1_matched_dsmuon_pt > 0  & l1_pt > 5 & abs(l1_eta) > 1.2 & abs(l1_eta) < 2.4 & hnl_2d_disp > 4 & hnl_2d_disp < 120")
tt.Draw("l2_pt >> dsmunfl2", "abs(l2_pdgId) == 13 & l2_matched_dsmuon_charge == l2_charge & l2_matched_dsmuon_pt > 0  & l2_pt > 5 & abs(l2_eta) > 1.2 & abs(l2_eta) < 2.4 & hnl_2d_disp > 4 & hnl_2d_disp < 120")
tt.Draw("l1_pt >> dsmucfl1", "abs(l1_pdgId) == 13 & l1_matched_dsmuon_charge != l1_charge & l1_matched_dsmuon_pt > 0  & l1_pt > 5 & abs(l1_eta) > 1.2 & abs(l1_eta) < 2.4 & hnl_2d_disp > 4 & hnl_2d_disp < 120")
tt.Draw("l2_pt >> dsmucfl2", "abs(l2_pdgId) == 13 & l2_matched_dsmuon_charge != l2_charge & l2_matched_dsmuon_pt > 0  & l2_pt > 5 & abs(l2_eta) > 1.2 & abs(l2_eta) < 2.4 & hnl_2d_disp > 4 & hnl_2d_disp < 120")
################## 
# slimmed global #
################## 
tt.Draw("l0_pt >> gmul0", "abs(l0_pdgId) == 13 & l0_matched_muon_is_gl == 1 & l0_matched_muon_pt > 0 & l0_pt > 5 & abs(l0_eta) > 1.2 & abs(l0_eta) < 2.4 & hnl_2d_disp > 4 & hnl_2d_disp < 120")
tt.Draw("l1_pt >> gmunfl1", "abs(l1_pdgId) == 13 & l1_matched_muon_is_gl == 1 & l1_matched_muon_charge == l1_charge & l1_matched_muon_pt > 0  & l1_pt > 5 & abs(l1_eta) > 1.2 & abs(l1_eta) < 2.4 & hnl_2d_disp > 4 & hnl_2d_disp < 120")
tt.Draw("l2_pt >> gmunfl2", "abs(l2_pdgId) == 13 & l2_matched_muon_is_gl == 1 & l2_matched_muon_charge == l2_charge & l2_matched_muon_pt > 0  & l2_pt > 5 & abs(l2_eta) > 1.2 & abs(l2_eta) < 2.4 & hnl_2d_disp > 4 & hnl_2d_disp < 120")
tt.Draw("l1_pt >> gmucfl1", "abs(l1_pdgId) == 13 & l1_matched_muon_is_gl == 1 & l1_matched_muon_charge != l1_charge & l1_matched_muon_pt > 0  & l1_pt > 5 & abs(l1_eta) > 1.2 & abs(l1_eta) < 2.4 & hnl_2d_disp > 4 & hnl_2d_disp < 120")
tt.Draw("l2_pt >> gmucfl2", "abs(l2_pdgId) == 13 & l2_matched_muon_is_gl == 1 & l2_matched_muon_charge != l2_charge & l2_matched_muon_pt > 0  & l2_pt > 5 & abs(l2_eta) > 1.2 & abs(l2_eta) < 2.4 & hnl_2d_disp > 4 & hnl_2d_disp < 120")
#################### 
# displaced global #
####################
tt.Draw("l0_pt >> dgmul0", "abs(l0_pdgId) == 13 & l0_matched_dgmuon_pt > 0 & l0_pt > 5 & abs(l0_eta) > 1.2 & abs(l0_eta) < 2.4 & hnl_2d_disp > 4 & hnl_2d_disp < 120")
tt.Draw("l1_pt >> dgmunfl1", "abs(l1_pdgId) == 13 & l1_matched_dgmuon_charge == l1_charge & l1_matched_dgmuon_pt > 0  & l1_pt > 5 & abs(l1_eta) > 1.2 & abs(l1_eta) < 2.4 & hnl_2d_disp > 4 & hnl_2d_disp < 120")
tt.Draw("l2_pt >> dgmunfl2", "abs(l2_pdgId) == 13 & l2_matched_dgmuon_charge == l2_charge & l2_matched_dgmuon_pt > 0  & l2_pt > 5 & abs(l2_eta) > 1.2 & abs(l2_eta) < 2.4 & hnl_2d_disp > 4 & hnl_2d_disp < 120")
tt.Draw("l1_pt >> dgmucfl1", "abs(l1_pdgId) == 13 & l1_matched_dgmuon_charge != l1_charge & l1_matched_dgmuon_pt > 0  & l1_pt > 5 & abs(l1_eta) > 1.2 & abs(l1_eta) < 2.4 & hnl_2d_disp > 4 & hnl_2d_disp < 120")
tt.Draw("l2_pt >> dgmucfl2", "abs(l2_pdgId) == 13 & l2_matched_dgmuon_charge != l2_charge & l2_matched_dgmuon_pt > 0  & l2_pt > 5 & abs(l2_eta) > 1.2 & abs(l2_eta) < 2.4 & hnl_2d_disp > 4 & hnl_2d_disp < 120")
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
samucfl2R.SetMarkerColor(7)
samucfl1R.SetMarkerColor(8)
##################################  
c1.cd()
samucfl1R.Draw()
samucfl2R.Draw('same')
c1.BuildLegend()
##################################  
c3.cd()
samusuml2.SetFillColor(2)
samusuml1.SetFillColor(6)
samul0.SetFillColor(4)
samulepT.Add(samul0)
samulepT.Add(samusuml1)
samulepT.Add(samusuml2)
samulepT.Draw('hist,nostack')
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
dsmucfl2R.SetMarkerColor(5)
dsmucfl1R.SetMarkerColor(6)
##################################  
c2.cd()
dsmucfl1R.Draw()
dsmucfl2R.Draw('same')
c2.BuildLegend()
##################################  
c4.cd()
dsmusuml2.SetFillColor(2)
dsmusuml1.SetFillColor(6)
dsmul0.SetFillColor(4)
dsmulepT.Add(dsmul0)
dsmulepT.Add(dsmusuml1)
dsmulepT.Add(dsmusuml2)
dsmulepT.Draw('hist,nostack')
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
gmucfl2R.SetMarkerColor(7)
gmucfl1R.SetMarkerColor(8)
##################################  
c6.cd()
gmucfl1R.Draw()
gmucfl2R.Draw('same')
c6.BuildLegend()
##################################  
c8.cd()
gmusuml2.SetFillColor(2)
gmusuml1.SetFillColor(6)
gmul0.SetFillColor(4)
gmulepT.Add(gmul0)
gmulepT.Add(gmusuml1)
gmulepT.Add(gmusuml2)
gmulepT.Draw('hist,nostack')
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
dgmucfl2R.SetMarkerColor(5)
dgmucfl1R.SetMarkerColor(6)
##################################  
c7.cd()
dgmucfl1R.Draw()
dgmucfl2R.Draw('same')
c7.BuildLegend()
##################################  
c9.cd()
dgmusuml2.SetFillColor(2)
dgmusuml1.SetFillColor(6)
dgmul0.SetFillColor(4)
dgmulepT.Add(dgmul0)
dgmulepT.Add(dgmusuml1)
dgmulepT.Add(dgmusuml2)
dgmulepT.Draw('hist,nostack')
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
samucf.SetMarkerColor(4)
##################################  
dsmunfl1.Add(dsmunfl2)
dsmucfl1.Add(dsmucfl2)
dsmusum.Add(dsmucfl1)
dsmusum.Add(dsmunfl1)
dsmucf.Divide(dsmucfl1,dsmusum)
dsmucf.Draw('same')
dsmucf.SetMarkerColor(2)
##################################  
c10.cd()
gmunfl1.Add(gmunfl2)
gmucfl1.Add(gmucfl2)
gmusum.Add(gmucfl1)
gmusum.Add(gmunfl1)
gmucf.Divide(gmucfl1,gmusum)
gmucf.Draw()
gmucf.SetMarkerColor(4)
##################################  
dgmunfl1.Add(dgmunfl2)
dgmucfl1.Add(dgmucfl2)
dgmusum.Add(dgmucfl1)
dgmusum.Add(dgmunfl1)
dgmucf.Divide(dgmucfl1,dgmusum)
dgmucf.Draw('same')
dgmucf.SetMarkerColor(2)
########### 
# make-up # 
###########
histupdatelist = [samucf,dsmul0,samul0,samucfl2R,dsmucfl2R,dsmucfl1R,samucfl1R,gmucf,dgmul0,gmul0,gmucfl2R,dgmucfl2R,dgmucfl1R,gmucfl1R]
##################################   
for hh in histupdatelist:
   hh.GetXaxis().SetTitle('p_{T}[GeV]')
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
###################################################  
c1.SaveAs(output_dir + 'cap_d2_samu_l12.root')
c2.SaveAs(output_dir + 'cap_d2_dsmu_l12.root')
c3.SaveAs(output_dir + 'cap_d2_samu_l012pt.root')
c4.SaveAs(output_dir + 'cap_d2_dsmu_l012pt.root')
c5.SaveAs(output_dir + 'cap_d2_sa.root')
c6.SaveAs(output_dir + 'cap_d2_gmu_l12.root')
c7.SaveAs(output_dir + 'cap_d2_dgmu_l12.root')
c8.SaveAs(output_dir + 'cap_d2_gmu_l012pt.root')
c9.SaveAs(output_dir + 'cap_d2_dgmu_l012pt.root')
c10.SaveAs(output_dir + 'cap_d2_gl.root')
################################################### 
print('dSA#mu: %.2f / SA#mu: %.2f M entries'%((samu / 1000000.),dsamu / 1000000.))
print('dG#mu: %.2f / G#mu: %.2f M entries'%((gmu / 1000000.),dgmu / 1000000.))
