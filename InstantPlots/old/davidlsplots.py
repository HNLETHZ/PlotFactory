import ROOT
import plotfactory as pf
import numpy as np

pf.setpfstyle()

tt = pf.makechain(True)
nentries = tt.GetEntries()
print('nentries = %d'%(nentries))

binsx = np.arange(5.,75.,5.)

c = ROOT.TCanvas('c','c')

h_smu_l1_cf = ROOT.TH1F('h_smu_l1_cf','h_smu_l1_cf',len(binsx)-1,binsx)
h_smu_l2_cf = ROOT.TH1F('h_smu_l2_cf','h_smu_l2_cf',len(binsx)-1,binsx)
h_smu_l1_nf = ROOT.TH1F('h_smu_l1_nf','h_smu_l1_nf',len(binsx)-1,binsx)
h_smu_l2_nf = ROOT.TH1F('h_smu_l2_nf','h_smu_l2_nf',len(binsx)-1,binsx)
h_smu_sum   = ROOT.TH1F('h_smu_sum'  ,'h_smu_sum'  ,len(binsx)-1,binsx)

h_dsmu_l1_cf = ROOT.TH1F('h_dsmu_l1_cf','h_dsmu_l1_cf',len(binsx)-1,binsx)
h_dsmu_l2_cf = ROOT.TH1F('h_dsmu_l2_cf','h_dsmu_l2_cf',len(binsx)-1,binsx)
h_dsmu_l1_nf = ROOT.TH1F('h_dsmu_l1_nf','h_dsmu_l1_nf',len(binsx)-1,binsx)
h_dsmu_l2_nf = ROOT.TH1F('h_dsmu_l2_nf','h_dsmu_l2_nf',len(binsx)-1,binsx)
h_dsmu_sum   = ROOT.TH1F('h_dsmu_sum'  ,'h_dsmu_sum'  ,len(binsx)-1,binsx)


h_smu_l1_cf.SetLineColor   (ROOT.kBlue+2)
h_smu_l1_cf.SetMarkerColor (ROOT.kBlue+2)
h_dsmu_l1_cf.SetLineColor  (ROOT.kRed+2)
h_dsmu_l1_cf.SetMarkerColor(ROOT.kRed+2)

tt.Draw('l1_pt >> h_smu_l1_cf','abs(l1_eta)<2.4 & abs(l1_pdgId)==13 & l1_matched_muon_pt > 3 & l1_charge != l1_matched_muon_charge')
tt.Draw('l2_pt >> h_smu_l2_cf','abs(l2_eta)<2.4 & abs(l2_pdgId)==13 & l2_matched_muon_pt > 3 & l2_charge != l2_matched_muon_charge')
tt.Draw('l1_pt >> h_smu_l1_nf','abs(l1_eta)<2.4 & abs(l1_pdgId)==13 & l1_matched_muon_pt > 3 & l1_charge == l1_matched_muon_charge')
tt.Draw('l2_pt >> h_smu_l2_nf','abs(l2_eta)<2.4 & abs(l2_pdgId)==13 & l2_matched_muon_pt > 3 & l2_charge == l2_matched_muon_charge')

tt.Draw('l1_pt >> h_dsmu_l1_cf','abs(l1_eta)<2.4 & abs(l1_pdgId)==13 & l1_matched_dsmuon_pt > 3 & l1_charge != l1_matched_dsmuon_charge')
tt.Draw('l2_pt >> h_dsmu_l2_cf','abs(l2_eta)<2.4 & abs(l2_pdgId)==13 & l2_matched_dsmuon_pt > 3 & l2_charge != l2_matched_dsmuon_charge')
tt.Draw('l1_pt >> h_dsmu_l1_nf','abs(l1_eta)<2.4 & abs(l1_pdgId)==13 & l1_matched_dsmuon_pt > 3 & l1_charge == l1_matched_dsmuon_charge')
tt.Draw('l2_pt >> h_dsmu_l2_nf','abs(l2_eta)<2.4 & abs(l2_pdgId)==13 & l2_matched_dsmuon_pt > 3 & l2_charge == l2_matched_dsmuon_charge')

h_smu_l1_cf.Add(h_smu_l2_cf)
h_smu_l1_nf.Add(h_smu_l2_nf)
h_smu_sum.Add(h_smu_l1_cf)
h_smu_sum.Add(h_smu_l1_nf)

h_dsmu_l1_cf.Add(h_dsmu_l2_cf)
h_dsmu_l1_nf.Add(h_dsmu_l2_nf)
h_dsmu_sum.Add(h_dsmu_l1_cf)
h_dsmu_sum.Add(h_dsmu_l1_nf)

h_smu_l1_cf.Divide(h_smu_sum)
h_smu_l1_nf.Divide(h_smu_sum)
h_dsmu_l1_cf.Divide(h_dsmu_sum)
h_dsmu_l1_nf.Divide(h_dsmu_sum)

hs = ROOT.THStack('h','')
hs.Add(h_smu_l1_cf)
hs.Add(h_dsmu_l1_cf)

hs.Draw('nostack')

for hh in [hs]:
    hh.SetTitle(';pt [GeV];Chargeflip ratio')

leg1 = ROOT.TLegend(.2,.65,.5,.85)
leg1.SetBorderSize(0)
leg1.SetFillColor(ROOT.kWhite)
leg1.SetFillStyle(1001)
leg1.SetTextFont(42)
leg1.SetTextSize(0.03)
leg1.AddEntry(h_smu_l1_cf, 'slimmedMuon'            ,'EP')
leg1.AddEntry(h_dsmu_l1_cf, 'displacedStandAloneMuon'            ,'EP')
leg1.Draw('apez same')



pf.showlumi(' l1+l2 / eta<2.4 / alldispl / %.2f M entries'%(nentries / 1000000.))

for cc in [c]:
    cc.Update()

