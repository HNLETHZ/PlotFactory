################# 
# Configuration #
#################
import ROOT
import numpy as np
import plotfactory as pf
from pdb import set_trace
from glob import glob

pf.setpfstyle()
bewl = input("Makechain: True or False\n")
tt = pf.makechain(bewl)

#file = ROOT.TFile('tree.root')
#tt = file.Get('tree')
ntries = tt.GetEntries()

print('Number of entries: ' + str(ntries))

################# 
# Define x-axes #
#################
pTbins = np.arange(5.,73,5)

################### 
# Create canvases #
###################
print('Preparing canvas')
t = ROOT.TCanvas('t','bar_d3')
c = ROOT.TCanvas('c','bar_d3')
c1 = ROOT.TCanvas('c1','bar_d3')

##################### 
# Create histograms #
#####################

# d in cm
# d1: less than 4 
# d2: 4 - 120
# d3: 120 - 350
# d4: 350 - 600

smunfl1 = ROOT.TH1F('smunfl1','smunfl1',len(pTbins)-1,pTbins)
smunfl2 = ROOT.TH1F('smunfl2','smunfl2',len(pTbins)-1,pTbins)
smucfl1 = ROOT.TH1F('smucfl1','smucfl1',len(pTbins)-1,pTbins)
smucfl2 = ROOT.TH1F('smucfl2','smucfl2',len(pTbins)-1,pTbins)
smusum  = ROOT.TH1F('smusum','smusum',len(pTbins)-1,pTbins)
smucf   = ROOT.TH1F('smucf','chargeflip',len(pTbins)-1,pTbins)
smunf   = ROOT.TH1F('smunf','no chargeflip',len(pTbins)-1,pTbins)

dsmunfl1 = ROOT.TH1F('dsmunfl1','dsmunfl1',len(pTbins)-1,pTbins)
dsmunfl2 = ROOT.TH1F('dsmunfl2','dsmunfl2',len(pTbins)-1,pTbins)
dsmucfl1 = ROOT.TH1F('dsmucfl1','dsmucfl1',len(pTbins)-1,pTbins)
dsmucfl2 = ROOT.TH1F('dsmucfl2','dsmucfl2',len(pTbins)-1,pTbins)
dsmusum  = ROOT.TH1F('dsmusum','dsmusum',len(pTbins)-1,pTbins)
dsmucf   = ROOT.TH1F('dsmucf','chargeflip',len(pTbins)-1,pTbins)
dsmunf   = ROOT.TH1F('dsmunf','no chargeflip',len(pTbins)-1,pTbins)

dsmusuml1= ROOT.TH1F('dsmusum','dsmusum',len(pTbins)-1,pTbins) 
dsmusuml2= ROOT.TH1F('dsmusum','dsmusum',len(pTbins)-1,pTbins)

# final normalized histograms
l1dsmucf = ROOT.TH1F('dsmucf','l1 chargeflip',len(pTbins)-1,pTbins)
l2dsmucf = ROOT.TH1F('dsmunf','l2 chargeflip',len(pTbins)-1,pTbins)

print('Filling histograms for l1 + l2')
#slimmed mu
tt.Draw("l1_pt >> smunfl1", "abs(l1_pdgId) == 13 & l1_matched_muon_charge == l1_charge & l1_matched_muon_pt > 0 & l1_pt > 5 & abs(l1_eta) < 0.8 & hnl_2d_disp > 120 & hnl_2d_disp < 350")
tt.Draw("l2_pt >> smunfl2", "abs(l2_pdgId) == 13 & l2_matched_muon_charge == l2_charge & l2_matched_muon_pt > 0 & l2_pt > 5 & abs(l2_eta) < 0.8 & hnl_2d_disp > 120 & hnl_2d_disp < 350")
tt.Draw("l1_pt >> smucfl1", "abs(l1_pdgId) == 13 & l1_matched_muon_charge != l1_charge & l1_matched_muon_pt > 0 & l1_pt > 5 & abs(l1_eta) < 0.8 & hnl_2d_disp > 120 & hnl_2d_disp < 350")
tt.Draw("l2_pt >> smucfl2", "abs(l2_pdgId) == 13 & l2_matched_muon_charge != l2_charge & l2_matched_muon_pt > 0 & l2_pt > 5 & abs(l2_eta) < 0.8 & hnl_2d_disp > 120 & hnl_2d_disp < 350")
#ds mu 
tt.Draw("l1_pt >> dsmunfl1", "abs(l1_pdgId) == 13 & l1_matched_dsmuon_charge == l1_charge & l1_matched_dsmuon_pt > 0 & l1_pt > 5 & abs(l1_eta) < 0.8 & hnl_2d_disp > 120 & hnl_2d_disp < 350")
tt.Draw("l2_pt >> dsmunfl2", "abs(l2_pdgId) == 13 & l2_matched_dsmuon_charge == l2_charge & l2_matched_dsmuon_pt > 0 & l2_pt > 5 & abs(l2_eta) < 0.8 & hnl_2d_disp > 120 & hnl_2d_disp < 350")
tt.Draw("l1_pt >> dsmucfl1", "abs(l1_pdgId) == 13 & l1_matched_dsmuon_charge != l1_charge & l1_matched_dsmuon_pt > 0 & l1_pt > 5 & abs(l1_eta) < 0.8 & hnl_2d_disp > 120 & hnl_2d_disp < 350")
tt.Draw("l2_pt >> dsmucfl2", "abs(l2_pdgId) == 13 & l2_matched_dsmuon_charge != l2_charge & l2_matched_dsmuon_pt > 0 & l2_pt > 5 & abs(l2_eta) < 0.8 & hnl_2d_disp > 120 & hnl_2d_disp < 350")

print('Adding and drawing histograms')


dsmusuml1.Add(dsmucfl1)
dsmusuml1.Add(dsmunfl1)

l1dsmucf.Divide(dsmucfl1,dsmusuml1)

dsmusuml2.Add(dsmucfl2)
dsmusuml2.Add(dsmunfl2)

l2dsmucf.Divide(dsmucfl2,dsmusuml2)

dsmucfl2.SetMarkerColor(5)
dsmucfl1.SetMarkerColor(6)

#leg = ROOT.TLegend(.18,.76,.4,.9)
#leg.SetBorderSize(0)
#leg.SetFillColor(ROOT.kWhite)
#leg.SetFillStyle(0)
#leg.SetTextFont(42)
#leg.SetTextSize(0.045)
#leg.AddEntry(dsmucf, 'dSA#mu', 'EP')
#leg.AddEntry(smucf, 'S#mu', 'EP')

c.cd()
l1dsmucf.Draw()
t.cd()
l2dsmucf.Draw()
c1.cd()
l1dsmucf.Draw()
l2dsmucf.Draw('same')

set_trace()
t.cd()
smunfl1.Add(smunfl2)
smucfl1.Add(smucfl2)
smusum.Add(smucfl1)
smusum.Add(smunfl1)
smucf.Divide(smucfl1,smusum)
smucf.Draw()
smucf.SetMarkerColor(4)

dsmunfl1.Add(dsmunfl2)
dsmucfl1.Add(dsmucfl2)
dsmusum.Add(dsmucfl1)
dsmusum.Add(dsmunfl1)
dsmucf.Divide(dsmucfl1,dsmusum)
dsmucf.Draw('same')
dsmucf.SetMarkerColor(2)

smucf.GetXaxis().SetTitle('p_{T}[GeV]')
smucf.GetYaxis().SetTitle('Chargeflip Ratio')
smucf.GetXaxis().SetTitleOffset(1.2)
smucf.GetYaxis().SetTitleOffset(1.4)

slim = smusum.GetEntries()
dsa  = dsmusum.GetEntries()

pf.showlumi('dSA#mu: %.2f / S#mu: %.2f M entries'%((slim / 1000000.),dsa / 1000000.))
pf.showlogosim('CMS')

leg = ROOT.TLegend(.18,.76,.4,.9)
leg.SetBorderSize(0)
leg.SetFillColor(ROOT.kWhite)
leg.SetFillStyle(0)
leg.SetTextFont(42)
leg.SetTextSize(0.045)
leg.AddEntry(dsmucf, 'dSA#mu', 'EP')
leg.AddEntry(smucf, 'S#mu', 'EP') 
leg.Draw('apez same')
t.Update()

print('Updating pads')

for tt in [t]:
    tt.Update()

