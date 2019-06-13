################# 
# Configuration #
#################
import ROOT
import numpy as np
import plotfactory as pf
from glob import glob

pf.setpfstyle()
tt = pf.makechain(True)
output_dir = '/afs/cern.ch/user/v/vstampf/CMSSW_8_0_30/PlotFactory/plots/4_reg/'

#file = ROOT.TFile('tree.root')
#tt = file.Get('tree')
ntries = tt.GetEntries()

print('Number of entries: ' + str(ntries))

################# 
# Define x-axes #
#################
pTbins = np.arange(5.,71, 5)
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
# d1: < 4 
# d2: 4 - 120
# d3: 120 - 350
# d4: 350 - 600

smudnfl1 = ROOT.TH1F('smudnfl1','smudnfl1',len(pTbins)-1,pTbins)
smudnfl2 = ROOT.TH1F('smudnfl2','smudnfl2',len(pTbins)-1,pTbins)
smudcfl1 = ROOT.TH1F('smudcfl1','smudcfl1',len(pTbins)-1,pTbins)
smudcfl2 = ROOT.TH1F('smudcfl2','smudcfl2',len(pTbins)-1,pTbins)
smudsum  = ROOT.TH1F('smudsum','smudsum',len(pTbins)-1,pTbins)
smudcf   = ROOT.TH1F('smudcf','slimmedMuon',len(pTbins)-1,pTbins)

dsmudnfl1 = ROOT.TH1F('dsmudnfl1','dsmudnfl1',len(pTbins)-1,pTbins)
dsmudnfl2 = ROOT.TH1F('dsmudnfl2','dsmudnfl2',len(pTbins)-1,pTbins)
dsmudcfl1 = ROOT.TH1F('dsmudcfl1','dsmudcfl1',len(pTbins)-1,pTbins)
dsmudcfl2 = ROOT.TH1F('dsmudcfl2','dsmudcfl2',len(pTbins)-1,pTbins)
dsmudsum  = ROOT.TH1F('dsmudsum','dsmudsum',len(pTbins)-1,pTbins)
dsmudcf   = ROOT.TH1F('dsmudcf','displacedStandAloneMuon',len(pTbins)-1,pTbins)


d1nfl0 = ROOT.TH1F('d1nfl0','d1nfl0',len(pTbins)-1,pTbins)
d1nfl1 = ROOT.TH1F('d1nfl1','d1nfl1',len(pTbins)-1,pTbins)
d1nfl2 = ROOT.TH1F('d1nfl2','d1nfl2',len(pTbins)-1,pTbins)
d1cfl0 = ROOT.TH1F('d1cfl0','d1cfl0',len(pTbins)-1,pTbins)
d1cfl1 = ROOT.TH1F('d1cfl1','d1cfl1',len(pTbins)-1,pTbins)
d1cfl2 = ROOT.TH1F('d1cfl2','d1cfl2',len(pTbins)-1,pTbins)
d1sum  = ROOT.TH1F('d1sum','d1sum',len(pTbins)-1,pTbins)
d1cf   = ROOT.TH1F('d1cf','chargeflip',len(pTbins)-1,pTbins)
d1nf   = ROOT.TH1F('d1nf','no chargeflip',len(pTbins)-1,pTbins)
d1stack= ROOT.THStack("d1stack","slimmed muons, d1")

d2nfl0 = ROOT.TH1F('d2nfl0','d2nfl0',len(pTbins)-1,pTbins)
d2nfl1 = ROOT.TH1F('d2nfl1','d2nfl1',len(pTbins)-1,pTbins)
d2nfl2 = ROOT.TH1F('d2nfl2','d2nfl2',len(pTbins)-1,pTbins)
d2cfl0 = ROOT.TH1F('d2cfl0','d2cfl0',len(pTbins)-1,pTbins)
d2cfl1 = ROOT.TH1F('d2cfl1','d2cfl1',len(pTbins)-1,pTbins)
d2cfl2 = ROOT.TH1F('d2cfl2','d2cfl2',len(pTbins)-1,pTbins)
d2sum  = ROOT.TH1F('d2sum','d2sum',len(pTbins)-1,pTbins)
d2cf   = ROOT.TH1F('d2cf','chargeflip',len(pTbins)-1,pTbins)
d2nf   = ROOT.TH1F('d2nf','no chargeflip',len(pTbins)-1,pTbins)
d2stack= ROOT.THStack("d2stack","slimmed muons, d2")

d3nfl0 = ROOT.TH1F('d3nfl0','d3nfl0',len(pTbins)-1,pTbins)
d3nfl1 = ROOT.TH1F('d3nfl1','d3nfl1',len(pTbins)-1,pTbins)
d3nfl2 = ROOT.TH1F('d3nfl2','d3nfl2',len(pTbins)-1,pTbins)
d3cfl0 = ROOT.TH1F('d3cfl0','d3cfl0',len(pTbins)-1,pTbins)
d3cfl1 = ROOT.TH1F('d3cfl1','d3cfl1',len(pTbins)-1,pTbins)
d3cfl2 = ROOT.TH1F('d3cfl2','d3cfl2',len(pTbins)-1,pTbins)
d3sum  = ROOT.TH1F('d3sum','d3sum',len(pTbins)-1,pTbins)
d3cf   = ROOT.TH1F('d3cf','chargeflip',len(pTbins)-1,pTbins)
d3nf   = ROOT.TH1F('d3nf','no chargeflip',len(pTbins)-1,pTbins)
d3stack= ROOT.THStack("d3stack","slimmed muons, d3")

d4nfl0 = ROOT.TH1F('d4nfl0','d4nfl0',len(pTbins)-1,pTbins)
d4nfl1 = ROOT.TH1F('d4nfl1','d4nfl1',len(pTbins)-1,pTbins)
d4nfl2 = ROOT.TH1F('d4nfl2','d4nfl2',len(pTbins)-1,pTbins)
d4cfl0 = ROOT.TH1F('d4cfl0','d4cfl0',len(pTbins)-1,pTbins)
d4cfl1 = ROOT.TH1F('d4cfl1','d4cfl1',len(pTbins)-1,pTbins)
d4cfl2 = ROOT.TH1F('d4cfl2','d4cfl2',len(pTbins)-1,pTbins)
d4sum  = ROOT.TH1F('d4sum','d4sum',len(pTbins)-1,pTbins)

print('Filling histograms for l1 + l2')
#d,reco=smu
print('Filling d') 
tt.Draw("l1_pt >> smudnfl1", "abs(l1_pdgId) == 13 & l1_matched_muon_charge == l1_charge & l1_matched_muon_pt > 3 & abs(l1_eta) < 2.4")
tt.Draw("l2_pt >> smudnfl2", "abs(l2_pdgId) == 13 & l2_matched_muon_charge == l2_charge & l2_matched_muon_pt > 3 & abs(l2_eta) < 2.4")
tt.Draw("l1_pt >> smudcfl1", "abs(l1_pdgId) == 13 & l1_matched_muon_charge != l1_charge & l1_matched_muon_pt > 3 & abs(l1_eta) < 2.4")
tt.Draw("l2_pt >> smudcfl2", "abs(l2_pdgId) == 13 & l2_matched_muon_charge != l2_charge & l2_matched_muon_pt > 3 & abs(l2_eta) < 2.4")
#d,reco=dsmu
tt.Draw("l1_pt >> dsmudnfl1", "abs(l1_pdgId) == 13 & l1_matched_dsmuon_charge == l1_charge & l1_matched_dsmuon_pt > 3 & abs(l1_eta) < 2.4")
tt.Draw("l2_pt >> dsmudnfl2", "abs(l2_pdgId) == 13 & l2_matched_dsmuon_charge == l2_charge & l2_matched_dsmuon_pt > 3 & abs(l2_eta) < 2.4")
tt.Draw("l1_pt >> dsmudcfl1", "abs(l1_pdgId) == 13 & l1_matched_dsmuon_charge != l1_charge & l1_matched_dsmuon_pt > 3 & abs(l1_eta) < 2.4")
tt.Draw("l2_pt >> dsmudcfl2", "abs(l2_pdgId) == 13 & l2_matched_dsmuon_charge != l2_charge & l2_matched_dsmuon_pt > 3 & abs(l2_eta) < 2.4")

##d1
#print('Filling d1') 
#tt.Draw("l0_pt >> d1nfl0", "abs(l0_pdgId) == 13 & l0_matched_muon_charge == l0_charge & l0_matched_muon_pt > 3 & abs(l0_eta) < 2.4 & hnl_2d_disp < 10")
#tt.Draw("l1_pt >> d1nfl1", "abs(l1_pdgId) == 13 & l1_matched_muon_charge == l1_charge & l1_matched_muon_pt > 3 & abs(l1_eta) < 2.4 & hnl_2d_disp < 10")
#tt.Draw("l2_pt >> d1nfl2", "abs(l2_pdgId) == 13 & l2_matched_muon_charge == l2_charge & l2_matched_muon_pt > 3 & abs(l2_eta) < 2.4 & hnl_2d_disp < 10")
#tt.Draw("l0_pt >> d1cfl0", "abs(l0_pdgId) == 13 & l0_matched_muon_charge != l0_charge & l0_matched_muon_pt > 3 & abs(l0_eta) < 2.4 & hnl_2d_disp < 10")
#tt.Draw("l1_pt >> d1cfl1", "abs(l1_pdgId) == 13 & l1_matched_muon_charge != l1_charge & l1_matched_muon_pt > 3 & abs(l1_eta) < 2.4 & hnl_2d_disp < 10")
#tt.Draw("l2_pt >> d1cfl2", "abs(l2_pdgId) == 13 & l2_matched_muon_charge != l2_charge & l2_matched_muon_pt > 3 & abs(l2_eta) < 2.4 & hnl_2d_disp < 10")
##d2 
#print('Filling d2') 
#tt.Draw("l0_pt >> d2nfl0", "abs(l0_pdgId) == 13 & l0_matched_muon_charge == l0_charge & l0_matched_muon_pt > 3 & abs(l0_eta) < 2.4 & hnl_2d_disp < 100 & hnl_2d_disp > 10")
#tt.Draw("l1_pt >> d2nfl1", "abs(l1_pdgId) == 13 & l1_matched_muon_charge == l1_charge & l1_matched_muon_pt > 3 & abs(l1_eta) < 2.4 & hnl_2d_disp < 100 & hnl_2d_disp > 10")
#tt.Draw("l2_pt >> d2nfl2", "abs(l2_pdgId) == 13 & l2_matched_muon_charge == l2_charge & l2_matched_muon_pt > 3 & abs(l2_eta) < 2.4 & hnl_2d_disp < 100 & hnl_2d_disp > 10")
#tt.Draw("l0_pt >> d2cfl0", "abs(l0_pdgId) == 13 & l0_matched_muon_charge != l0_charge & l0_matched_muon_pt > 3 & abs(l0_eta) < 2.4 & hnl_2d_disp < 100 & hnl_2d_disp > 10")
#tt.Draw("l1_pt >> d2cfl1", "abs(l1_pdgId) == 13 & l1_matched_muon_charge != l1_charge & l1_matched_muon_pt > 3 & abs(l1_eta) < 2.4 & hnl_2d_disp < 100 & hnl_2d_disp > 10")
#tt.Draw("l2_pt >> d2cfl2", "abs(l2_pdgId) == 13 & l2_matched_muon_charge != l2_charge & l2_matched_muon_pt > 3 & abs(l2_eta) < 2.4 & hnl_2d_disp < 100 & hnl_2d_disp > 10")
##d3
#print('Filling d3') 
#tt.Draw("l0_pt >> d3nfl0", "abs(l0_pdgId) == 13 & l0_matched_muon_charge == l0_charge & l0_matched_muon_pt > 3 & abs(l0_eta) < 2.4 & hnl_2d_disp < 600 & hnl_2d_disp > 100")
#tt.Draw("l1_pt >> d3nfl1", "abs(l1_pdgId) == 13 & l1_matched_muon_charge == l1_charge & l1_matched_muon_pt > 3 & abs(l1_eta) < 2.4 & hnl_2d_disp < 600 & hnl_2d_disp > 100")
#tt.Draw("l2_pt >> d3nfl2", "abs(l2_pdgId) == 13 & l2_matched_muon_charge == l2_charge & l2_matched_muon_pt > 3 & abs(l2_eta) < 2.4 & hnl_2d_disp < 600 & hnl_2d_disp > 100")
#tt.Draw("l0_pt >> d3cfl0", "abs(l0_pdgId) == 13 & l0_matched_muon_charge != l0_charge & l0_matched_muon_pt > 3 & abs(l0_eta) < 2.4 & hnl_2d_disp < 600 & hnl_2d_disp > 100")
#tt.Draw("l1_pt >> d3cfl1", "abs(l1_pdgId) == 13 & l1_matched_muon_charge != l1_charge & l1_matched_muon_pt > 3 & abs(l1_eta) < 2.4 & hnl_2d_disp < 600 & hnl_2d_disp > 100")
#tt.Draw("l2_pt >> d3cfl2", "abs(l2_pdgId) == 13 & l2_matched_muon_charge != l2_charge & l2_matched_muon_pt > 3 & abs(l2_eta) < 2.4 & hnl_2d_disp < 600 & hnl_2d_disp > 100")


print('Adding and drawing histograms')

t.cd()
smudnfl1.Add(smudnfl2)
smudcfl1.Add(smudcfl2)
smudsum.Add(smudcfl1)
smudsum.Add(smudnfl1)
smudcf.Divide(smudcfl1,smudsum)

dsmudnfl1.Add(dsmudnfl2)
dsmudcfl1.Add(dsmudcfl2)
dsmudsum.Add(dsmudcfl1)
dsmudsum.Add(dsmudnfl1)
dsmudcf.Divide(dsmudcfl1,dsmudsum)

dsmudcf.Draw()
smudcf.Draw('same')

smudcf.SetMarkerColor(4)
dsmudcf.SetMarkerColor(2)
dsmudcf.GetXaxis().SetTitle('p_{T}[GeV]')
dsmudcf.GetYaxis().SetTitle('Entries (normalized)')
dsmudcf.GetXaxis().SetTitleOffset(1.2)
dsmudcf.GetYaxis().SetTitleOffset(1.4)

leg = ROOT.TLegend(.18,.76,.4,.9)
leg.SetBorderSize(0)
#leg.SetFillColor(ROOT.kWhite)
leg.SetFillStyle(0)
leg.SetTextFont(42)
leg.SetTextSize(0.03)
leg.AddEntry(dsmudcf, 'dSA#mu', 'EP')
leg.AddEntry(smudcf , 'S#mu', 'EP')
leg.Draw('apez same')

pf.showlogoprelimsim('CMS')

print('Updating pads and saving outputs')

for tt in [t,t1,t2,t3]:
    tt.Update()

t.SaveAs(output_dir + 'alld.pdf')
