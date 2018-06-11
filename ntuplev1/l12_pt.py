import ROOT
import numpy as np
import plotfactory as pf
#from pdb import set_trace
from glob import glob

pf.setpfstyle()
bewl = input("Makechain: True or False\n")
tt = pf.makechain(bewl)
ntries = tt.GetEntries()

print('Number of entries: ' + str(ntries))

pTbins = np.arange(5.,73,5)

print('Preparing canvas')

c1 = ROOT.TCanvas('c1','smu')
c2 = ROOT.TCanvas('c2','dsmu')

smucfl1 = ROOT.TH1F('smucfl1','smucfl1',len(pTbins)-1,pTbins)
smunfl1 = ROOT.TH1F('smunfl1','smunfl1',len(pTbins)-1,pTbins)
smucfl2 = ROOT.TH1F('smucfl2','smucfl2',len(pTbins)-1,pTbins)
smunfl2 = ROOT.TH1F('smunfl2','smunfl2',len(pTbins)-1,pTbins)

smusuml1 = ROOT.TH1F('smusuml1','smusuml1',len(pTbins)-1,pTbins)
smusuml2 = ROOT.TH1F('smusuml2','smusuml2',len(pTbins)-1,pTbins)
smucfl1R= ROOT.TH1F('smucfl1R','smucfl1R',len(pTbins)-1,pTbins)
smucfl2R= ROOT.TH1F('smucfl2R','smucfl2R',len(pTbins)-1,pTbins)

dsmusuml1 = ROOT.TH1F('dsmusuml1','dsmusuml1',len(pTbins)-1,pTbins)
dsmusuml2 = ROOT.TH1F('dsmusuml2','dsmusuml2',len(pTbins)-1,pTbins)
dsmucfl1R= ROOT.TH1F('dsmucfl1R','dsmucfl1R',len(pTbins)-1,pTbins)
dsmucfl2R= ROOT.TH1F('dsmucfl2R','dsmucfl2R',len(pTbins)-1,pTbins)

dsmucfl1 = ROOT.TH1F('dsmucfl1','dsmucfl1',len(pTbins)-1,pTbins)
dsmunfl1 = ROOT.TH1F('dsmunfl1','dsmunfl1',len(pTbins)-1,pTbins)
dsmucfl2 = ROOT.TH1F('dsmucfl2','dsmucfl2',len(pTbins)-1,pTbins)
dsmunfl2 = ROOT.TH1F('dsmunfl2','dsmunfl2',len(pTbins)-1,pTbins)

tt.Draw('l1_pt >> smucfl1', 'l1_pt > 5 & abs(l1_pdgId) == 13 & abs(l1_eta) < 2.4 & l1_matched_muon_pt > 0 & l1_matched_muon_charge != l1_charge')
tt.Draw('l2_pt >> smunfl2', 'l2_pt > 5 & abs(l2_pdgId) == 13 & abs(l2_eta) < 2.4 & l2_matched_muon_pt > 0 & l2_matched_muon_charge == l2_charge')
tt.Draw('l1_pt >> smunfl1', 'l1_pt > 5 & abs(l1_pdgId) == 13 & abs(l1_eta) < 2.4 & l1_matched_muon_pt > 0 & l1_matched_muon_charge == l1_charge')
tt.Draw('l2_pt >> smucfl2', 'l2_pt > 5 & abs(l2_pdgId) == 13 & abs(l2_eta) < 2.4 & l2_matched_muon_pt > 0 & l2_matched_muon_charge != l2_charge')

tt.Draw('l1_pt >> dsmucfl1', 'l1_pt > 5 & abs(l1_pdgId) == 13 & abs(l1_eta) < 2.4 & l1_matched_dsmuon_pt > 0 & l1_matched_dsmuon_charge != l1_charge')
tt.Draw('l2_pt >> dsmunfl2', 'l2_pt > 5 & abs(l2_pdgId) == 13 & abs(l2_eta) < 2.4 & l2_matched_dsmuon_pt > 0 & l2_matched_dsmuon_charge == l2_charge')
tt.Draw('l1_pt >> dsmunfl1', 'l1_pt > 5 & abs(l1_pdgId) == 13 & abs(l1_eta) < 2.4 & l1_matched_dsmuon_pt > 0 & l1_matched_dsmuon_charge == l1_charge')
tt.Draw('l2_pt >> dsmucfl2', 'l2_pt > 5 & abs(l2_pdgId) == 13 & abs(l2_eta) < 2.4 & l2_matched_dsmuon_pt > 0 & l2_matched_dsmuon_charge != l2_charge')

smusuml1.Add(smucfl1)
smusuml1.Add(smunfl1)
smusuml2.Add(smucfl2)
smusuml2.Add(smunfl2)

smucfl1R.Divide(smucfl1,smusuml1)
smucfl2R.Divide(smucfl2,smusuml2)

dsmusuml1.Add(dsmucfl1)
dsmusuml1.Add(dsmunfl1)
dsmusuml2.Add(dsmucfl2)
dsmusuml2.Add(dsmunfl2)

dsmucfl1R.Divide(dsmucfl1,dsmusuml1)
dsmucfl2R.Divide(dsmucfl2,dsmusuml2)

c1.cd()
smucfl1R.Draw()
smucfl2R.Draw('same')
smucfl1R.SetMarkerColor(4)
smucfl2R.SetMarkerColor(2)
smucfl2R.SetAxisRange(0,1,"Y")
c1.BuildLegend()

c2.cd()
dsmucfl1R.Draw()
dsmucfl2R.Draw('same')
dsmucfl1R.SetMarkerColor(4)
dsmucfl2R.SetMarkerColor(2)
dsmucfl2R.SetAxisRange(0,1,"Y")
c2.BuildLegend()

for cc in [c1,c2]:
    cc.Modified()
    cc.Update()

