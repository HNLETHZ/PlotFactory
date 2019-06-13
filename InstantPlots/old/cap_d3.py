################# 
# Configuration #
#################
import ROOT
import numpy as np
import plotfactory as pf
#from pdb import set_trace
from glob import glob

pf.setpfstyle()
bewl = input("Makechain: True or False\n")
tt = pf.makechain(bewl)

output_dir = '/afs/cern.ch/user/v/vstampf/CMSSW_8_0_30/PlotFactory/plots/4_reg/genpt5/debugging/'

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
c1 = ROOT.TCanvas('c1','cap_d3')
c2 = ROOT.TCanvas('c2','cap_d3')
c3 = ROOT.TCanvas('c3','cap_d3')
#c4 = ROOT.TCanvas('c4','bar_d3')

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

smusuml1= ROOT.TH1F('smusuml1','smusuml1',len(pTbins)-1,pTbins) 
smusuml2= ROOT.TH1F('smusuml2','smusuml2',len(pTbins)-1,pTbins)
smucfl1R= ROOT.TH1F('smucfl1R','smucfl1R',len(pTbins)-1,pTbins)
smucfl2R= ROOT.TH1F('smucfl2R','smucfl2R',len(pTbins)-1,pTbins)

dsmunfl1 = ROOT.TH1F('dsmunfl1','dsmunfl1',len(pTbins)-1,pTbins)
dsmunfl2 = ROOT.TH1F('dsmunfl2','dsmunfl2',len(pTbins)-1,pTbins)
dsmucfl1 = ROOT.TH1F('dsmucfl1','dsmucfl1',len(pTbins)-1,pTbins)
dsmucfl2 = ROOT.TH1F('dsmucfl2','dsmucfl2',len(pTbins)-1,pTbins)
dsmusum  = ROOT.TH1F('dsmusum','dsmusum',len(pTbins)-1,pTbins)
dsmucf   = ROOT.TH1F('dsmucf','chargeflip',len(pTbins)-1,pTbins)
dsmunf   = ROOT.TH1F('dsmunf','no chargeflip',len(pTbins)-1,pTbins)

dsmusuml1= ROOT.TH1F('dsmusum11','dsmusuml1',len(pTbins)-1,pTbins) 
dsmusuml2= ROOT.TH1F('dsmusuml2','dsmusuml2',len(pTbins)-1,pTbins)
dsmucfl1R= ROOT.TH1F('dsmucfl1R','dsmucfl1R',len(pTbins)-1,pTbins)
dsmucfl2R= ROOT.TH1F('dsmucfl2R','dsmucfl2R',len(pTbins)-1,pTbins)


print('Filling histograms for l1 + l2')
#slimmed mu
tt.Draw("l1_pt >> smunfl1", "abs(l1_pdgId) == 13 & l1_matched_muon_charge == l1_charge & l1_matched_muon_pt > 0 & l1_pt > 5 & abs(l1_eta) < 2.4 & abs(l1_eta) > 1.2 & hnl_2d_disp < 350 & hnl_2d_disp > 120")
tt.Draw("l2_pt >> smunfl2", "abs(l2_pdgId) == 13 & l2_matched_muon_charge == l2_charge & l2_matched_muon_pt > 0 & l2_pt > 5 & abs(l2_eta) < 2.4 & abs(l2_eta) > 1.2 & hnl_2d_disp < 350 & hnl_2d_disp > 120")
tt.Draw("l1_pt >> smucfl1", "abs(l1_pdgId) == 13 & l1_matched_muon_charge != l1_charge & l1_matched_muon_pt > 0 & l1_pt > 5 & abs(l1_eta) < 2.4 & abs(l1_eta) > 1.2 & hnl_2d_disp < 350 & hnl_2d_disp > 120")
tt.Draw("l2_pt >> smucfl2", "abs(l2_pdgId) == 13 & l2_matched_muon_charge != l2_charge & l2_matched_muon_pt > 0 & l2_pt > 5 & abs(l2_eta) < 2.4 & abs(l2_eta) > 1.2 & hnl_2d_disp < 350 & hnl_2d_disp > 120")
#ds mu 
tt.Draw("l1_pt >> dsmunfl1", "abs(l1_pdgId) == 13 & l1_matched_dsmuon_charge == l1_charge & l1_matched_dsmuon_pt > 0 & l1_pt > 5 & abs(l1_eta) < 2.4 & abs(l1_eta) > 1.2 & hnl_2d_disp < 350 & hnl_2d_disp > 120")
tt.Draw("l2_pt >> dsmunfl2", "abs(l2_pdgId) == 13 & l2_matched_dsmuon_charge == l2_charge & l2_matched_dsmuon_pt > 0 & l2_pt > 5 & abs(l2_eta) < 2.4 & abs(l2_eta) > 1.2 & hnl_2d_disp < 350 & hnl_2d_disp > 120")
tt.Draw("l1_pt >> dsmucfl1", "abs(l1_pdgId) == 13 & l1_matched_dsmuon_charge != l1_charge & l1_matched_dsmuon_pt > 0 & l1_pt > 5 & abs(l1_eta) < 2.4 & abs(l1_eta) > 1.2 & hnl_2d_disp < 350 & hnl_2d_disp > 120")
tt.Draw("l2_pt >> dsmucfl2", "abs(l2_pdgId) == 13 & l2_matched_dsmuon_charge != l2_charge & l2_matched_dsmuon_pt > 0 & l2_pt > 5 & abs(l2_eta) < 2.4 & abs(l2_eta) > 1.2 & hnl_2d_disp < 350 & hnl_2d_disp > 120")

print('Adding and drawing histograms')

# slimmed mu
smusuml1.Add(smucfl1)
smusuml1.Add(smunfl1)
smucfl1R.Divide(smucfl1,smusuml1)

smusuml2.Add(smucfl2)
smusuml2.Add(smunfl2)
smucfl2R.Divide(smucfl2,smusuml2)

smucfl2R.SetMarkerColor(7)
smucfl1R.SetMarkerColor(8)

c1.cd()
smucfl1R.Draw()
smucfl2R.Draw('same')
c1.BuildLegend()
c1.SaveAs(output_dir + 'cap_d3_smu_l12.root')

# dsa mu
dsmusuml1.Add(dsmucfl1)
dsmusuml1.Add(dsmunfl1)
dsmucfl1R.Divide(dsmucfl1,dsmusuml1)

dsmusuml2.Add(dsmucfl2)
dsmusuml2.Add(dsmunfl2)
dsmucfl2R.Divide(dsmucfl2,dsmusuml2)

dsmucfl2R.SetMarkerColor(5)
dsmucfl1R.SetMarkerColor(6)

c2.cd()
dsmucfl1R.Draw()
dsmucfl2R.Draw('same')
c2.BuildLegend()
c2.SaveAs(output_dir + 'cap_d3_dsmu_l12.root')

#set_trace()
c3.cd()
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

#pf.showlumi('dSA#mu: %.2f / S#mu: %.2f M entries'%((slim / 1000000.),dsa / 1000000.))
pf.showlogoprelimsim('CMS')

leg = ROOT.TLegend(.18,.76,.4,.9)
leg.SetBorderSize(0)
leg.SetFillColor(ROOT.kWhite)
leg.SetFillStyle(0)
leg.SetTextFont(42)
leg.SetTextSize(0.045)
leg.AddEntry(dsmucf, 'dSA#mu', 'EP')
leg.AddEntry(smucf, 'S#mu', 'EP') 
leg.Draw('apez same')
c3.Update()
c3.SaveAs(output_dir + 'cap_d3.root')

print('Updating pads')

for c in [c1,c2,c3]:
    c.Modified()
    c.Update()

print('dSA#mu: %.2f / S#mu: %.2f M entries'%((slim / 1000000.),dsa / 1000000.))

