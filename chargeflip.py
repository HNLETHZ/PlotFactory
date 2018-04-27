########################## 
# Configuration
##########################
import ROOT
import numpy as np
import plotfactory as pf
from glob import glob

pf.setpfstyle()

file = ROOT.TFile('tree.root')
tt = file.Get('tree')
ntries = tt.GetEntriesFast()

print('number of entries: ' + str(ntries))

########################## 
# Define x-axis
##########################
pTbins = np.arange(0.,65, 1)
dxybins= np.arange(0.,600,10)


########################## 
# Create canvases 
##########################
print('preparing canvas')
t1 = ROOT.TCanvas('t1','t1')
t2 = ROOT.TCanvas('t2','t2')
t3 = ROOT.TCanvas('t3','t3')
t4 = ROOT.TCanvas('t4','t4')

########################## 
# 4) Create histograms
##########################
dcf0l0 = ROOT.TH1F('dcf0l0','dcf0l0',len(dxybins)-1,dxybins)
dcf0l1 = ROOT.TH1F('dcf0l1','dcf0l1',len(dxybins)-1,dxybins)
dcf0l2 = ROOT.TH1F('dcf0l2','dcf0l2',len(dxybins)-1,dxybins)
dcf1l0 = ROOT.TH1F('dcf1l0','dcf1l0',len(dxybins)-1,dxybins)
dcf1l1 = ROOT.TH1F('dcf1l1','dcf1l1',len(dxybins)-1,dxybins)
dcf1l2 = ROOT.TH1F('dcf1l2','dcf1l2',len(dxybins)-1,dxybins)

cf0l0 = ROOT.TH2F('cf0l0','cf0l0',len(pTbins)-1,pTbins,len(dxybins)-1,dxybins)
cf0l1 = ROOT.TH2F('cf0l1','cf0l1',len(pTbins)-1,pTbins,len(dxybins)-1,dxybins) 
cf0l2 = ROOT.TH2F('cf0l2','cf0l2',len(pTbins)-1,pTbins,len(dxybins)-1,dxybins) 
cf1l0 = ROOT.TH2F('cf1l0','cf1l0',len(pTbins)-1,pTbins,len(dxybins)-1,dxybins) 
cf1l1 = ROOT.TH2F('cf1l1','cf1l1',len(pTbins)-1,pTbins,len(dxybins)-1,dxybins) 
cf1l2 = ROOT.TH2F('cf1l2','cf1l2',len(pTbins)-1,pTbins,len(dxybins)-1,dxybins) 

print('Filling histograms for l0, l1, l2')

t1.cd()
tt.Draw("l0_matched_muon_dxy >> dcf0l0", "abs(l0_pdgId) == 13 & l0_matched_muon_charge == l0_charge & l0_matched_muon_pt > 5 & abs(l0_eta) < 0.8")
tt.Draw("l1_matched_muon_dxy >> dcf0l1", "abs(l1_pdgId) == 13 & l1_matched_muon_charge == l1_charge & l1_matched_muon_pt > 5 & abs(l1_eta) < 0.8")
tt.Draw("l2_matched_muon_dxy >> dcf0l2", "abs(l2_pdgId) == 13 & l2_matched_muon_charge == l2_charge & l2_matched_muon_pt > 5 & abs(l2_eta) < 0.8")
t2.cd()
tt.Draw("l0_matched_muon_dxy >> dcf1l0", "abs(l0_pdgId) == 13 & l0_matched_muon_charge != l0_charge & l0_matched_muon_pt > 5 & abs(l0_eta) < 0.8")
tt.Draw("l1_matched_muon_dxy >> dcf1l1", "abs(l1_pdgId) == 13 & l1_matched_muon_charge != l1_charge & l1_matched_muon_pt > 5 & abs(l1_eta) < 0.8")
tt.Draw("l2_matched_muon_dxy >> dcf1l2", "abs(l2_pdgId) == 13 & l2_matched_muon_charge != l2_charge & l2_matched_muon_pt > 5 & abs(l2_eta) < 0.8")

t3.cd()
tt.Draw("l0_pt:l0_matched_muon_dxy>>cf0l0", "abs(l0_pdgId) == 13 & l0_matched_muon_charge == l0_charge & l0_matched_muon_pt > 5 & abs(l0_eta) < 0.8")
tt.Draw("l1_pt:l1_matched_muon_dxy>>cf0l1", "abs(l1_pdgId) == 13 & l1_matched_muon_charge == l1_charge & l1_matched_muon_pt > 5 & abs(l1_eta) < 0.8")
tt.Draw("l2_pt:l2_matched_muon_dxy>>cf0l2", "abs(l2_pdgId) == 13 & l2_matched_muon_charge == l2_charge & l2_matched_muon_pt > 5 & abs(l2_eta) < 0.8")
t4.cd()
tt.Draw("l0_pt:l0_matched_muon_dxy>>cf1l0", "abs(l0_pdgId) == 13 & l0_matched_muon_charge != l0_charge & l0_matched_muon_pt > 5 & abs(l0_eta) < 0.8")
tt.Draw("l1_pt:l1_matched_muon_dxy>>cf1l1", "abs(l1_pdgId) == 13 & l1_matched_muon_charge != l1_charge & l1_matched_muon_pt > 5 & abs(l1_eta) < 0.8")
tt.Draw("l2_pt:l2_matched_muon_dxy>>cf1l2", "abs(l2_pdgId) == 13 & l2_matched_muon_charge != l2_charge & l2_matched_muon_pt > 5 & abs(l2_eta) < 0.8")

print('Adding and drawing histograms')

dcf0l0.Add(dcf0l1)
dcf0l0.Add(dcf0l2)
dcf1l0.Add(dcf1l1)
dcf1l0.Add(dcf1l2)

t1.cd()
dcf0l0.Draw()
t2.cd()
dcf1l0.Draw()

cf0l0.Add(cf0l1)
cf0l0.Add(cf0l2)
cf1l0.Add(cf1l1)
cf1l0.Add(cf1l2)

t3.cd()
cf0l0.Draw()
t4.cd()
cf1l0.Draw()

for t in [t1,t2,t3,t4]:
    t.Update()

# selection: abs(pId) == 13, pT > 0
# d in cm
# d1: less than 4
# d2:  4 - 120
# d3: 120 - 350
# d4: 350 - 600
