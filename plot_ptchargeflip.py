################# 
# Configuration #
#################
import ROOT
import numpy as np
from glob import glob
import plotfactory as pf

pf.setpfstyle()
tt = pf.makechain(False)

#file = ROOT.TFile('tree.root')
#tt = file.Get('tree')
ntries = tt.GetEntries()

print('number of entries: ' + str(ntries))

binsx = np.arange(5.,65, 1)  # THE COMMA IS SUPER IMPORTANT!

h0_smu_cf0_pT = ROOT.TH1F('h0_smu_cf0_pT','h0_smu_cf0_pT',len(binsx)-1,binsx)
h0_smu_cf1_pT = ROOT.TH1F('h0_smu_cf1_pT','h0_smu_cf1_pT',len(binsx)-1,binsx)
h1_smu_cf0_pT = ROOT.TH1F('h1_smu_cf0_pT','h1_smu_cf0_pT',len(binsx)-1,binsx)
h1_smu_cf1_pT = ROOT.TH1F('h1_smu_cf1_pT','h1_smu_cf1_pT',len(binsx)-1,binsx)
h2_smu_cf0_pT = ROOT.TH1F('h2_smu_cf0_pT','h2_smu_cf0_pT',len(binsx)-1,binsx)
h2_smu_cf1_pT = ROOT.TH1F('h2_smu_cf1_pT','h2_smu_cf1_pT',len(binsx)-1,binsx)
div0 = ROOT.TH1F("smu_cf0_pT","no chargeflip",len(binsx)-1,binsx)
div1 = ROOT.TH1F("smu_cf1_pT","chargeflip",len(binsx)-1,binsx)
hs1 = ROOT.THStack("hs","Stacked 1D histograms")
hs2 = ROOT.THStack("hs","slimmed muons")
hs_ns = ROOT.THStack("hs","not scaled")

print('setting canvas')
c00 = ROOT.TCanvas('c00', 'c00', 500, 500)      #nomenclature: c00 = 'l=l_0', 'cf=No'
c01 = ROOT.TCanvas('c01', 'c01', 500, 500)
c10 = ROOT.TCanvas('c10', 'c10', 500, 500)
c11 = ROOT.TCanvas('c11', 'c11', 500, 500)
c20 = ROOT.TCanvas('c20', 'c20', 500, 500)
c21 = ROOT.TCanvas('c21', 'c21', 500, 500)
c3  = ROOT.TCanvas('c30', 'c30', 500, 500)
c4  = ROOT.TCanvas('c31', 'c31', 500, 500)
c32 = ROOT.TCanvas('c32', 'c32')

print('creating histograms for l0, l1, l2')

c00.cd()
tt.Draw("l0_pt >> h0_smu_cf0_pT", "abs(l0_pdgId) == 13 & l0_matched_muon_charge == l0_charge & l0_matched_muon_pt > 5 & abs(l0_eta) < 0.8")
c01.cd()
tt.Draw("l0_pt >> h0_smu_cf1_pT", "abs(l0_pdgId) == 13 & l0_matched_muon_charge != l0_charge & l0_matched_muon_pt > 5 & abs(l0_eta) < 0.8")
c10.cd()
tt.Draw("l1_pt >> h1_smu_cf0_pT", "abs(l1_pdgId) == 13 & l1_matched_muon_charge == l1_charge & l1_matched_muon_pt > 5 & abs(l1_eta) < 0.8")
c11.cd()
tt.Draw("l1_pt >> h1_smu_cf1_pT", "abs(l1_pdgId) == 13 & l1_matched_muon_charge != l1_charge & l1_matched_muon_pt > 5 & abs(l1_eta) < 0.8")
c20.cd()
tt.Draw("l2_pt >> h2_smu_cf0_pT", "abs(l2_pdgId) == 13 & l2_matched_muon_charge == l2_charge & l2_matched_muon_pt > 5 & abs(l2_eta) < 0.8")
c21.cd()
tt.Draw("l2_pt >> h2_smu_cf1_pT", "abs(l2_pdgId) == 13 & l2_matched_muon_charge != l2_charge & l2_matched_muon_pt > 5 & abs(l2_eta) < 0.8")


h0_smu_cf0_pT.Add(h1_smu_cf0_pT)
h0_smu_cf0_pT.Add(h2_smu_cf0_pT)

h0_smu_cf1_pT.Add(h1_smu_cf1_pT)
h0_smu_cf1_pT.Add(h2_smu_cf1_pT)

div1.Divide(h0_smu_cf1_pT,(h0_smu_cf0_pT+h0_smu_cf1_pT))
div0.Divide(h0_smu_cf0_pT,(h0_smu_cf0_pT+h0_smu_cf1_pT))

div0.SetFillColor(4)
div0.SetMarkerStyle(4)
div0.SetMarkerColor(4)
hs2.Add(div0)

div1.SetFillColor(2)
div1.SetMarkerStyle(2)
div1.SetMarkerColor(2)
hs2.Add(div1)

hs_ns.Add(h0_smu_cf0_pT)
hs_ns.Add(h0_smu_cf1_pT)
c32.cd()
hs_ns.Draw('hist')

c3.cd()
hs2.Draw("hist")
hs2.GetXaxis().SetTitle('(p_{T})[GeV]')
hs2.GetYaxis().SetTitle('Entries (normalized)')
ROOT.gPad.BuildLegend(0.6,0.21,0.85,0.36,"")

print('scaling histograms')

for hh in [h0_smu_cf0_pT,h0_smu_cf1_pT]:
    scale = 1.0/hh.Integral()
    hh.Scale(scale)

h0_smu_cf1_pT.SetFillColor(21)
h0_smu_cf1_pT.SetMarkerStyle(21)
h0_smu_cf1_pT.SetMarkerColor(21)
hs1.Add(h0_smu_cf1_pT)

h0_smu_cf0_pT.SetFillColor(40)
h0_smu_cf0_pT.SetMarkerStyle(40)
h0_smu_cf0_pT.SetMarkerColor(40)
hs1.Add(h0_smu_cf0_pT)

leg1 = ROOT.TLegend(0.7,.7,.88,.88)
leg1.SetBorderSize(0)
leg1.SetFillColor(0)
leg1.SetFillStyle(0)
leg1.SetTextFont(42)
leg1.SetTextSize(0.03)

leg1.AddEntry(h0_smu_cf0_pT, 'no chargeflip','EP')
leg1.AddEntry(h0_smu_cf1_pT, 'chargeflip','EP')

c4.cd()
hs1.Draw("nostack")
leg1.Draw('apez same')

c32.cd()
leg1.Draw()

print('Updating pads')

for cc in [c00,c01,c10,c11,c20,c21,c3,c4,c32]:
    cc.Update()

