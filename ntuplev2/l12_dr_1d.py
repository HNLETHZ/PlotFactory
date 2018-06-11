import ROOT
import numpy as np
#from pdb import set_trace
from glob import glob
import sys
sys.path.append('/afs/cern.ch/user/v/vstampf/CMSSW_8_0_30/PlotFactory')
import plotfactory as pf

pf.setpfstyle()
bewl = input("Makechain: True or False\n")
tt = pf.makechain(bewl)

output_dir = '/afs/cern.ch/user/v/vstampf/CMSSW_8_0_30/PlotFactory/plots/leptons_cf/'

#file = ROOT.TFile('tree.root')
#tt = file.Get('tree')
ntries = tt.GetEntries()

print('Number of entries: ' + str(ntries))

################# 
# Define x-axes #
#################
drbins = np.arange(0.,4,0.1)

################### 
# Create canvases #
###################
print('Preparing canvas')
c1 = ROOT.TCanvas('c1','c1 smu l1m l2m')
c2 = ROOT.TCanvas('c2','c2 smu l1g l2m')
c3 = ROOT.TCanvas('c3','c3 smu l1m l2g')
c4 = ROOT.TCanvas('c4','c4 dsmu l1m l2m')
c5 = ROOT.TCanvas('c5','c5 dsmu l1g l2m')
c6 = ROOT.TCanvas('c6','c6 dsmu l1m l2g')

smucfl1 = ROOT.TH1F('smucfl1','smucfl1',len(drbins)-1,drbins)
smucfl2 = ROOT.TH1F('smucfl2','smucfl2',len(drbins)-1,drbins)
smunfl1 = ROOT.TH1F('smunfl1','smunfl1',len(drbins)-1,drbins)
smunfl2 = ROOT.TH1F('smunfl2','smunfl2',len(drbins)-1,drbins)

dsmucfl1 = ROOT.TH1F('dsmucfl1','dsmucfl1',len(drbins)-1,drbins)
dsmucfl2 = ROOT.TH1F('dsmucfl2','dsmucfl2',len(drbins)-1,drbins)
dsmunfl1 = ROOT.TH1F('dsmunfl1','dsmunfl1',len(drbins)-1,drbins)
dsmunfl2 = ROOT.TH1F('dsmunfl2','dsmunfl2',len(drbins)-1,drbins)

# smu
tt.Draw("hnl_dr_12 >> smunfl1", "l1_pt > 5 & abs(l1_pdgId) == 13 & l1_matched_muon_charge == l1_charge & abs(l1_eta) < 2.4 & l1_matched_muon_pt > 0")
tt.Draw("hnl_dr_12 >> smunfl2", "l2_pt > 5 & abs(l2_pdgId) == 13 & l2_matched_muon_charge == l2_charge & abs(l2_eta) < 2.4 & l2_matched_muon_pt > 0")
tt.Draw("hnl_dr_12 >> smucfl1", "l1_pt > 5 & abs(l1_pdgId) == 13 & l1_matched_muon_charge != l1_charge & abs(l1_eta) < 2.4 & l1_matched_muon_pt > 0")
tt.Draw("hnl_dr_12 >> smucfl2", "l2_pt > 5 & abs(l2_pdgId) == 13 & l2_matched_muon_charge != l2_charge & abs(l2_eta) < 2.4 & l2_matched_muon_pt > 0")
# dsmu
tt.Draw("hnl_dr_12 >> dsmunfl1", "l1_pt > 5 & abs(l1_pdgId) == 13 & l1_matched_dsmuon_charge == l1_charge & abs(l1_eta) < 2.4 & l1_matched_dsmuon_pt > 0")
tt.Draw("hnl_dr_12 >> dsmunfl2", "l2_pt > 5 & abs(l2_pdgId) == 13 & l2_matched_dsmuon_charge == l2_charge & abs(l2_eta) < 2.4 & l2_matched_dsmuon_pt > 0")
tt.Draw("hnl_dr_12 >> dsmucfl1", "l1_pt > 5 & abs(l1_pdgId) == 13 & l1_matched_dsmuon_charge != l1_charge & abs(l1_eta) < 2.4 & l1_matched_dsmuon_pt > 0")
tt.Draw("hnl_dr_12 >> dsmucfl2", "l2_pt > 5 & abs(l2_pdgId) == 13 & l2_matched_dsmuon_charge != l2_charge & abs(l2_eta) < 2.4 & l2_matched_dsmuon_pt > 0")

smucfl1.SetMarkerColor(2)
smunfl2.SetMarkerColor(4)
smucfl2.SetMarkerColor(6)
smunfl1.SetMarkerColor(8)

for hh in [smucfl1,smunfl1,dsmucfl1,dsmunfl1]:
   hh.SetAxisRange(1000,1000000,"Y")
   hh.SetAxisRange(0.,4.0,"X")
   hh.GetXaxis().SetTitle('dr')
   hh.GetYaxis().SetTitle('Events')

dsmucfl1.SetMarkerColor(2)
dsmunfl2.SetMarkerColor(4)
dsmucfl2.SetMarkerColor(6)
dsmunfl1.SetMarkerColor(8)

#dsmucfl1.SetAxisRange(1,1000000,"Y")
#dsmunfl1.SetAxisRange(1,1000000,"Y")

c1.cd()
smucfl1.Draw()
smucfl2.Draw('same')
c1.BuildLegend()
#c1.SaveAs(output_dir + 'smueta_l1ml2m.root')

c2.cd()
smunfl1.Draw()
smucfl2.Draw('same')
c2.BuildLegend()
#c2.SaveAs(output_dir + 'smueta_l1gl2m.root')

c3.cd()
smucfl1.Draw()
smunfl2.Draw('same')
c3.BuildLegend()
#c3.SaveAs(output_dir + 'smueta_l1ml2g.root')

c4.cd()
dsmucfl1.Draw()
dsmucfl2.Draw('same')
c4.BuildLegend()
#c4.SaveAs(output_dir + 'dsmueta_l1ml2m.root')

c5.cd()
dsmunfl1.Draw()
dsmucfl2.Draw('same')
c5.BuildLegend()
#c5.SaveAs(output_dir + 'dsmueta_l1gl2m.root')

c6.cd()
dsmucfl1.Draw()
dsmunfl2.Draw('same')
c6.BuildLegend()
#c6.SaveAs(output_dir + 'dsmueta_l1ml2g.root')

for cc in [c1,c2,c3,c4,c5,c6]:
   cc.SetLogy()
   cc.Modified()
   cc.Update()

print('all good')
