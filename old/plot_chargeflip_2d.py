################# 
# Configuration #
#################
import ROOT
import numpy as np
import plotfactory as pf
from glob import glob

pf.setpfstyle()
tt = pf.makechain(False)

#file = ROOT.TFile('tree.root')
#tt = file.Get('tree')
ntries = tt.GetEntries()

print('Number of entries: ' + str(ntries))

################# 
# Define x-axes #
#################
pTbins = np.arange(3.,65, 1)
dxybins= np.arange(0.,600,10)


################### 
# Create canvases #
###################
print('Preparing canvas')
t = ROOT.TCanvas('t','d')
t1 = ROOT.TCanvas('t1','d1')
t2 = ROOT.TCanvas('t2','d2')
t3 = ROOT.TCanvas('t3','d3')

##################### 
# Create histograms #
#####################

# selection: abs(pId) == 13, pT > 3, eta < 2.4 
# d in cm
# d1: less than 10 
# d2: 10 - 100
# d3: 100 - 600

#d4nfl0 = ROOT.TH1F('#d4nfl0','#d4nfl0',len(pTbins)-1,pTbins)
#d4nfl1 = ROOT.TH1F('#d4nfl1','#d4nfl1',len(pTbins)-1,pTbins)
#d4nfl2 = ROOT.TH1F('#d4nfl2','#d4nfl2',len(pTbins)-1,pTbins)
#d4cfl0 = ROOT.TH1F('#d4cfl0','#d4cfl0',len(pTbins)-1,pTbins)
#d4cfl1 = ROOT.TH1F('#d4cfl1','#d4cfl1',len(pTbins)-1,pTbins)
#d4cfl2 = ROOT.TH1F('#d4cfl2','#d4cfl2',len(pTbins)-1,pTbins)
#d4sum  = ROOT.TH1F('#d4sum','#d4sum',len(pTbins)-1,pTbins)

nfl0 = ROOT.TH2F('nfl0','nfl0',len(pTbins)-1,pTbins,len(dxybins)-1,dxybins)
nfl1 = ROOT.TH2F('nfl1','nfl1',len(pTbins)-1,pTbins,len(dxybins)-1,dxybins)
nfl2 = ROOT.TH2F('nfl2','nfl2',len(pTbins)-1,pTbins,len(dxybins)-1,dxybins)
cfl0 = ROOT.TH2F('cfl0','cfl0',len(pTbins)-1,pTbins,len(dxybins)-1,dxybins)
cfl1 = ROOT.TH2F('cfl1','cfl1',len(pTbins)-1,pTbins,len(dxybins)-1,dxybins)
cfl2 = ROOT.TH2F('cfl2','cfl2',len(pTbins)-1,pTbins,len(dxybins)-1,dxybins)


print('Filling histograms for l1 + l2')
#Filling TH1
print('Filling d')
# Filling TH2
#tt.Draw("l0_pt:hnl_2d_disp>>nfl0", "abs(l0_pdgId) == 13 & l0_matched_muon_charge == l0_charge & l0_matched_muon_pt > 3 & abs(l0_eta) < 2.4")
t.cd()
tt.Draw("l1_pt:hnl_2d_disp>>nfl1", "abs(l1_pdgId) == 13 & l1_matched_muon_charge == l1_charge & l1_matched_muon_pt > 3 & abs(l1_eta) < 2.4")
t1.cd()
tt.Draw("l2_pt:hnl_2d_disp>>nfl2", "abs(l2_pdgId) == 13 & l2_matched_muon_charge == l2_charge & l2_matched_muon_pt > 3 & abs(l2_eta) < 2.4")
#tt.Draw("l0_pt:hnl_2d_disp>>cfl0", "abs(l0_pdgId) == 13 & l0_matched_muon_charge != l0_charge & l0_matched_muon_pt > 3 & abs(l0_eta) < 2.4")
t2.cd()
tt.Draw("l1_pt:hnl_2d_disp>>cfl1", "abs(l1_pdgId) == 13 & l1_matched_muon_charge != l1_charge & l1_matched_muon_pt > 3 & abs(l1_eta) < 2.4")
t3.cd()
tt.Draw("l2_pt:hnl_2d_disp>>cfl2", "abs(l2_pdgId) == 13 & l2_matched_muon_charge != l2_charge & l2_matched_muon_pt > 3 & abs(l2_eta) < 2.4")

t3.cd()
cfl2.Draw("candle")

print('Updating pads')

for tt in [t,t1,t2,t3]:
    tt.Update()
