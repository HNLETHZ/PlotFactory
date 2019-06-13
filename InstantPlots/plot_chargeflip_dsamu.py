################# 
# Configuration #
#################
import ROOT
import numpy as np
import plotfactory as pf
from glob import glob

pf.setpfstyle()
tt = pf.makechain(True)

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

dnfl0 = ROOT.TH1F('dnfl0','dnfl0',len(pTbins)-1,pTbins)
dnfl1 = ROOT.TH1F('dnfl1','dnfl1',len(pTbins)-1,pTbins)
dnfl2 = ROOT.TH1F('dnfl2','dnfl2',len(pTbins)-1,pTbins)
dcfl0 = ROOT.TH1F('dcfl0','dcfl0',len(pTbins)-1,pTbins)
dcfl1 = ROOT.TH1F('dcfl1','dcfl1',len(pTbins)-1,pTbins)
dcfl2 = ROOT.TH1F('dcfl2','dcfl2',len(pTbins)-1,pTbins)
dsum  = ROOT.TH1F('dsum','dsum',len(pTbins)-1,pTbins)
dcf   = ROOT.TH1F('dcf','chargeflip',len(pTbins)-1,pTbins)
dnf   = ROOT.TH1F('dnf','no chargeflip',len(pTbins)-1,pTbins)
dstack= ROOT.THStack("dstack","dSA muons")

d1nfl0 = ROOT.TH1F('d1nfl0','d1nfl0',len(pTbins)-1,pTbins)
d1nfl1 = ROOT.TH1F('d1nfl1','d1nfl1',len(pTbins)-1,pTbins)
d1nfl2 = ROOT.TH1F('d1nfl2','d1nfl2',len(pTbins)-1,pTbins)
d1cfl0 = ROOT.TH1F('d1cfl0','d1cfl0',len(pTbins)-1,pTbins)
d1cfl1 = ROOT.TH1F('d1cfl1','d1cfl1',len(pTbins)-1,pTbins)
d1cfl2 = ROOT.TH1F('d1cfl2','d1cfl2',len(pTbins)-1,pTbins)
d1sum  = ROOT.TH1F('d1sum','d1sum',len(pTbins)-1,pTbins)
d1cf   = ROOT.TH1F('d1cf','chargeflip',len(pTbins)-1,pTbins)
d1nf   = ROOT.TH1F('d1nf','no chargeflip',len(pTbins)-1,pTbins)
d1stack= ROOT.THStack("d1stack","dSA muons, d1")

d2nfl0 = ROOT.TH1F('d2nfl0','d2nfl0',len(pTbins)-1,pTbins)
d2nfl1 = ROOT.TH1F('d2nfl1','d2nfl1',len(pTbins)-1,pTbins)
d2nfl2 = ROOT.TH1F('d2nfl2','d2nfl2',len(pTbins)-1,pTbins)
d2cfl0 = ROOT.TH1F('d2cfl0','d2cfl0',len(pTbins)-1,pTbins)
d2cfl1 = ROOT.TH1F('d2cfl1','d2cfl1',len(pTbins)-1,pTbins)
d2cfl2 = ROOT.TH1F('d2cfl2','d2cfl2',len(pTbins)-1,pTbins)
d2sum  = ROOT.TH1F('d2sum','d2sum',len(pTbins)-1,pTbins)
d2cf   = ROOT.TH1F('d2cf','chargeflip',len(pTbins)-1,pTbins)
d2nf   = ROOT.TH1F('d2nf','no chargeflip',len(pTbins)-1,pTbins)
d2stack= ROOT.THStack("d2stack","dSA muons, d2")

d3nfl0 = ROOT.TH1F('d3nfl0','d3nfl0',len(pTbins)-1,pTbins)
d3nfl1 = ROOT.TH1F('d3nfl1','d3nfl1',len(pTbins)-1,pTbins)
d3nfl2 = ROOT.TH1F('d3nfl2','d3nfl2',len(pTbins)-1,pTbins)
d3cfl0 = ROOT.TH1F('d3cfl0','d3cfl0',len(pTbins)-1,pTbins)
d3cfl1 = ROOT.TH1F('d3cfl1','d3cfl1',len(pTbins)-1,pTbins)
d3cfl2 = ROOT.TH1F('d3cfl2','d3cfl2',len(pTbins)-1,pTbins)
d3sum  = ROOT.TH1F('d3sum','d3sum',len(pTbins)-1,pTbins)
d3cf   = ROOT.TH1F('d3cf','chargeflip',len(pTbins)-1,pTbins)
d3nf   = ROOT.TH1F('d3nf','no chargeflip',len(pTbins)-1,pTbins)
d3stack= ROOT.THStack("d3stack","dSA muons, d3")

#d4nfl0 = ROOT.TH1F('d4nfl0','d4nfl0',len(pTbins)-1,pTbins)
#d4nfl1 = ROOT.TH1F('d4nfl1','d4nfl1',len(pTbins)-1,pTbins)
#d4nfl2 = ROOT.TH1F('d4nfl2','d4nfl2',len(pTbins)-1,pTbins)
#d4cfl0 = ROOT.TH1F('d4cfl0','d4cfl0',len(pTbins)-1,pTbins)
#d4cfl1 = ROOT.TH1F('d4cfl1','d4cfl1',len(pTbins)-1,pTbins)
#d4cfl2 = ROOT.TH1F('d4cfl2','d4cfl2',len(pTbins)-1,pTbins)
#d4sum  = ROOT.TH1F('d4sum','d4sum',len(pTbins)-1,pTbins)

nfl0 = ROOT.TH2F('nfl0','nfl0',len(pTbins)-1,pTbins,len(dxybins)-1,dxybins)
nfl1 = ROOT.TH2F('nfl1','nfl1',len(pTbins)-1,pTbins,len(dxybins)-1,dxybins) 
nfl2 = ROOT.TH2F('nfl2','nfl2',len(pTbins)-1,pTbins,len(dxybins)-1,dxybins) 
cfl0 = ROOT.TH2F('cfl0','cfl0',len(pTbins)-1,pTbins,len(dxybins)-1,dxybins) 
cfl1 = ROOT.TH2F('cfl1','cfl1',len(pTbins)-1,pTbins,len(dxybins)-1,dxybins) 
cfl2 = ROOT.TH2F('cfl2','cfl2',len(pTbins)-1,pTbins,len(dxybins)-1,dxybins) 

print('Filling histograms for l1 + l2')
#Filling TH1
#d
print('Filling d') 
#tt.Draw("l0_pt >> dnfl0", "abs(l0_pdgId) == 13 & l0_matched_dsmuon_charge == l0_charge & l0_matched_dsmuon_pt > 3 & abs(l0_eta) < 2.4")
tt.Draw("l1_pt >> dnfl1", "abs(l1_pdgId) == 13 & l1_matched_dsmuon_charge == l1_charge & l1_matched_dsmuon_pt > 3 & abs(l1_eta) < 2.4")
tt.Draw("l2_pt >> dnfl2", "abs(l2_pdgId) == 13 & l2_matched_dsmuon_charge == l2_charge & l2_matched_dsmuon_pt > 3 & abs(l2_eta) < 2.4")
#tt.Draw("l0_pt >> dcfl0", "abs(l0_pdgId) == 13 & l0_matched_dsmuon_charge != l0_charge & l0_matched_dsmuon_pt > 3 & abs(l0_eta) < 2.4")
tt.Draw("l1_pt >> dcfl1", "abs(l1_pdgId) == 13 & l1_matched_dsmuon_charge != l1_charge & l1_matched_dsmuon_pt > 3 & abs(l1_eta) < 2.4")
tt.Draw("l2_pt >> dcfl2", "abs(l2_pdgId) == 13 & l2_matched_dsmuon_charge != l2_charge & l2_matched_dsmuon_pt > 3 & abs(l2_eta) < 2.4")
##d1
print('Filling d1') 
#tt.Draw("l0_pt >> d1nfl0", "abs(l0_pdgId) == 13 & l0_matched_dsmuon_charge == l0_charge & l0_matched_dsmuon_pt > 3 & abs(l0_eta) < 2.4 & hnl_2d_disp < 10")
tt.Draw("l1_pt >> d1nfl1", "abs(l1_pdgId) == 13 & l1_matched_dsmuon_charge == l1_charge & l1_matched_dsmuon_pt > 3 & abs(l1_eta) < 2.4 & hnl_2d_disp < 10")
tt.Draw("l2_pt >> d1nfl2", "abs(l2_pdgId) == 13 & l2_matched_dsmuon_charge == l2_charge & l2_matched_dsmuon_pt > 3 & abs(l2_eta) < 2.4 & hnl_2d_disp < 10")
#tt.Draw("l0_pt >> d1cfl0", "abs(l0_pdgId) == 13 & l0_matched_dsmuon_charge != l0_charge & l0_matched_dsmuon_pt > 3 & abs(l0_eta) < 2.4 & hnl_2d_disp < 10")
tt.Draw("l1_pt >> d1cfl1", "abs(l1_pdgId) == 13 & l1_matched_dsmuon_charge != l1_charge & l1_matched_dsmuon_pt > 3 & abs(l1_eta) < 2.4 & hnl_2d_disp < 10")
tt.Draw("l2_pt >> d1cfl2", "abs(l2_pdgId) == 13 & l2_matched_dsmuon_charge != l2_charge & l2_matched_dsmuon_pt > 3 & abs(l2_eta) < 2.4 & hnl_2d_disp < 10")
##d2 
print('Filling d2') 
#tt.Draw("l0_pt >> d2nfl0", "abs(l0_pdgId) == 13 & l0_matched_dsmuon_charge == l0_charge & l0_matched_dsmuon_pt > 3 & abs(l0_eta) < 2.4 & hnl_2d_disp < 100 & hnl_2d_disp > 10")
tt.Draw("l1_pt >> d2nfl1", "abs(l1_pdgId) == 13 & l1_matched_dsmuon_charge == l1_charge & l1_matched_dsmuon_pt > 3 & abs(l1_eta) < 2.4 & hnl_2d_disp < 100 & hnl_2d_disp > 10")
tt.Draw("l2_pt >> d2nfl2", "abs(l2_pdgId) == 13 & l2_matched_dsmuon_charge == l2_charge & l2_matched_dsmuon_pt > 3 & abs(l2_eta) < 2.4 & hnl_2d_disp < 100 & hnl_2d_disp > 10")
#tt.Draw("l0_pt >> d2cfl0", "abs(l0_pdgId) == 13 & l0_matched_dsmuon_charge != l0_charge & l0_matched_dsmuon_pt > 3 & abs(l0_eta) < 2.4 & hnl_2d_disp < 100 & hnl_2d_disp > 10")
tt.Draw("l1_pt >> d2cfl1", "abs(l1_pdgId) == 13 & l1_matched_dsmuon_charge != l1_charge & l1_matched_dsmuon_pt > 3 & abs(l1_eta) < 2.4 & hnl_2d_disp < 100 & hnl_2d_disp > 10")
tt.Draw("l2_pt >> d2cfl2", "abs(l2_pdgId) == 13 & l2_matched_dsmuon_charge != l2_charge & l2_matched_dsmuon_pt > 3 & abs(l2_eta) < 2.4 & hnl_2d_disp < 100 & hnl_2d_disp > 10")
##d3
print('Filling d3') 
#tt.Draw("l0_pt >> d3nfl0", "abs(l0_pdgId) == 13 & l0_matched_dsmuon_charge == l0_charge & l0_matched_dsmuon_pt > 3 & abs(l0_eta) < 2.4 & hnl_2d_disp < 600 & hnl_2d_disp > 100")
tt.Draw("l1_pt >> d3nfl1", "abs(l1_pdgId) == 13 & l1_matched_dsmuon_charge == l1_charge & l1_matched_dsmuon_pt > 3 & abs(l1_eta) < 2.4 & hnl_2d_disp < 600 & hnl_2d_disp > 100")
tt.Draw("l2_pt >> d3nfl2", "abs(l2_pdgId) == 13 & l2_matched_dsmuon_charge == l2_charge & l2_matched_dsmuon_pt > 3 & abs(l2_eta) < 2.4 & hnl_2d_disp < 600 & hnl_2d_disp > 100")
#tt.Draw("l0_pt >> d3cfl0", "abs(l0_pdgId) == 13 & l0_matched_dsmuon_charge != l0_charge & l0_matched_dsmuon_pt > 3 & abs(l0_eta) < 2.4 & hnl_2d_disp < 600 & hnl_2d_disp > 100")
tt.Draw("l1_pt >> d3cfl1", "abs(l1_pdgId) == 13 & l1_matched_dsmuon_charge != l1_charge & l1_matched_dsmuon_pt > 3 & abs(l1_eta) < 2.4 & hnl_2d_disp < 600 & hnl_2d_disp > 100")
tt.Draw("l2_pt >> d3cfl2", "abs(l2_pdgId) == 13 & l2_matched_dsmuon_charge != l2_charge & l2_matched_dsmuon_pt > 3 & abs(l2_eta) < 2.4 & hnl_2d_disp < 600 & hnl_2d_disp > 100")

# Filling TH2
#tt.Draw("l0_pt:l0_matched_dsmuon_dxy>>nfl0", "abs(l0_pdgId) == 13 & l0_matched_dsmuon_charge == l0_charge & l0_matched_dsmuon_pt > 3 & abs(l0_eta) < 2.4")
#tt.Draw("l1_pt:l1_matched_dsmuon_dxy>>nfl1", "abs(l1_pdgId) == 13 & l1_matched_dsmuon_charge == l1_charge & l1_matched_dsmuon_pt > 3 & abs(l1_eta) < 2.4")
#tt.Draw("l2_pt:l2_matched_dsmuon_dxy>>nfl2", "abs(l2_pdgId) == 13 & l2_matched_dsmuon_charge == l2_charge & l2_matched_dsmuon_pt > 3 & abs(l2_eta) < 2.4")
#tt.Draw("l0_pt:l0_matched_dsmuon_dxy>>cfl0", "abs(l0_pdgId) == 13 & l0_matched_dsmuon_charge != l0_charge & l0_matched_dsmuon_pt > 3 & abs(l0_eta) < 2.4")
#tt.Draw("l1_pt:l1_matched_dsmuon_dxy>>cfl1", "abs(l1_pdgId) == 13 & l1_matched_dsmuon_charge != l1_charge & l1_matched_dsmuon_pt > 3 & abs(l1_eta) < 2.4")
#tt.Draw("l2_pt:l2_matched_dsmuon_dxy>>cfl2", "abs(l2_pdgId) == 13 & l2_matched_dsmuon_charge != l2_charge & l2_matched_dsmuon_pt > 3 & abs(l2_eta) < 2.4")

print('Adding and drawing histograms')

t.cd()
dnfl0.Add(dnfl1)
dnfl0.Add(dnfl2)
dcfl0.Add(dcfl1)
dcfl0.Add(dcfl2)
dsum.Add(dcfl0)
dsum.Add(dnfl0)
dcf.Divide(dcfl0,dsum)
dnf.Divide(dnfl0,dsum)
dcf.SetFillColor(2)
dnf.SetFillColor(4)
dstack.Add(dnf)
dstack.Add(dcf)
dstack.Draw("hist")
dstack.GetXaxis().SetTitle('p_{T}[GeV]')
dstack.GetYaxis().SetTitle('Entries (normalized)')
ROOT.gPad.BuildLegend(0.6,0.21,0.85,0.36,"")
pf.showlumi(' l1+l2 / eta<2.4 / alldispl / %.2f M entries'%(ntries / 1000000.))

#print('no error until d1')

t1.cd()
d1nfl0.Add(d1nfl1)
d1nfl0.Add(d1nfl2)
d1cfl0.Add(d1cfl1)
d1cfl0.Add(d1cfl2)
d1sum.Add(d1cfl0)
d1sum.Add(d1nfl0)
d1cf.Divide(d1cfl0,d1sum)
d1nf.Divide(d1nfl0,d1sum)
d1cf.SetFillColor(2)
d1nf.SetFillColor(4)
d1stack.Add(d1nf)
d1stack.Add(d1cf)
d1stack.Draw("hist")
d1stack.GetXaxis().SetTitle('p_{T}[GeV]')
d1stack.GetYaxis().SetTitle('Entries (normalized)')
ROOT.gPad.BuildLegend(0.6,0.21,0.85,0.36,"")
pf.showlumi(' l1+l2 / eta<2.4 / <10cm / %.2f M entries'%(ntries / 1000000.))

#print('no error until d2')

t2.cd()
d2nfl0.Add(d2nfl1)
d2nfl0.Add(d2nfl2)
d2cfl0.Add(d2cfl1)
d2cfl0.Add(d2cfl2)
d2sum.Add(d2cfl0)
d2sum.Add(d2nfl0)
d2cf.Divide(d2cfl0,d2sum)
d2nf.Divide(d2nfl0,d2sum)
d2cf.SetFillColor(2)
d2nf.SetFillColor(4)
d2stack.Add(d2nf)
d2stack.Add(d2cf)
d2stack.Draw("hist")
d2stack.GetXaxis().SetTitle('p_{T}[GeV]')
d2stack.GetYaxis().SetTitle('Entries (normalized)')
ROOT.gPad.BuildLegend(0.6,0.21,0.85,0.36,"")
pf.showlumi(' l1+l2 / eta<2.4 / 10 - 100cm / %.2f M entries'%(ntries / 1000000.))


#print('no error until d3')

t3.cd()
d3nfl0.Add(d3nfl1)
d3nfl0.Add(d3nfl2)
d3cfl0.Add(d3cfl1)
d3cfl0.Add(d3cfl2)
d3sum.Add(d3cfl0)
d3sum.Add(d3nfl0)
d3cf.Divide(d3cfl0,d3sum)
d3nf.Divide(d3nfl0,d3sum)
d3cf.SetFillColor(2)
d3nf.SetFillColor(4)
d3stack.Add(d3nf)
d3stack.Add(d3cf)
d3stack.Draw("hist")
d3stack.GetXaxis().SetTitle('p_{T}[GeV]')
d3stack.GetYaxis().SetTitle('Entries (normalized)')
ROOT.gPad.BuildLegend(0.6,0.21,0.85,0.36,"")
pf.showlumi(' l1+l2 / eta<2.4 / 100 - 600cm / %.2f M entries'%(ntries / 1000000.))

print('Updating pads')

for tt in [t,t1,t2,t3]:
    tt.Update()

