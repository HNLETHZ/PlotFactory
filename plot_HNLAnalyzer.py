import ROOT
import plotfactory as pf
import numpy as np
import sys

pf.setpfstyle()
output_dir = 'temp/'

######################################### 
# Make Chain from selection of samples
#########################################
# Get the option from the command line, using 'True' as a fallback.
if len(sys.argv)>1 and sys.argv[1] == 'test':
    setting = False
    print('Using a selection of samples')
else:
    setting = True
    print('Using all samples')

tt = pf.makechain(setting)

nentries = tt.GetEntries()
print('number of total entries in chain:\t\t\t%d'%(nentries))

######################################### 
# Produce KPIs
#########################################

n_2OrMoreMuons = tt.GetEntries()
print('number of all events with 2 or more muons:\t\t%d'%(n_2OrMoreMuons))

n_reconstructable = tt.GetEntries('flag_hnl_reconstructable == 1') 
print('number of events with reconstructable HNLs:\t\t%d'%(n_reconstructable))

n_dimuons = tt.GetEntries('n_dimuon > 0') 
print('number of events with reconstructed DiMuons:\t\t%d'%(n_dimuons))

n_matchedHNLChi2 = tt.GetEntries('flag_matchedHNLChi2 == 1') 
print('number of correctly found HNLs using Chi2 method:\t%d'%(n_matchedHNLChi2))

n_matchedHNLDxy = tt.GetEntries('flag_matchedHNLDxy == 1')
print('number of correctly found HNLs using Dxy method:\t%d'%(n_matchedHNLDxy))

eff_Chi2_tot = float(n_matchedHNLChi2) / float(n_reconstructable)
print('Reconstruction efficiency (min Chi2 method):\t\t%.1f%%'%(100*eff_Chi2_tot))

eff_Dxy_tot = float(n_matchedHNLDxy) / float(n_reconstructable)
print('Reconstruction efficiency (max Dxy method):\t\t%.1f%%'%(100*eff_Dxy_tot))

purity_Chi2_tot = float(n_matchedHNLChi2) / float(n_dimuons)
print('Reconstruction purity (min Chi2 method):\t\t%.1f%%'%(100*purity_Chi2_tot))

purity_Dxy_tot = float(n_matchedHNLDxy) / float(n_dimuons)
print('Reconstruction purity (max Dxy method):\t\t\t%.1f%%'%(100*purity_Dxy_tot))

######################################### 
# Reconstruction Efficiency
#########################################
print('Making the efficiency plot...')

c_eff = ROOT.TCanvas('c_eff', 'c_eff')

h_eff_Chi2_sMu_enum = ROOT.TH1F('h_eff_Chi2_sMu_enum','',50,0,600)
tt.Draw('hnl_2d_disp >> h_eff_Chi2_sMu_enum','flag_matchedHNLChi2 == 1 & dMu1Chi2_reco == 1 & dMu2Chi2_reco == 1 & flag_hnl_reconstructable == 1')
h_eff_Chi2_sMu_denom = ROOT.TH1F('h_eff_Chi2_sMu_denom','',50,0,600)
tt.Draw('hnl_2d_disp >> h_eff_Chi2_sMu_denom','dMu1Chi2_reco == 1 & dMu2Chi2_reco == 1 & flag_hnl_reconstructable == 1')
h_eff_Chi2_sMu_enum.Divide(h_eff_Chi2_sMu_denom)
h_eff_Chi2_sMu_enum.SetTitle(';HNL 2D displacement ; HNL reconstruction efficiency')
h_eff_Chi2_sMu_enum.GetYaxis().SetRangeUser(0.,1.05)
h_eff_Chi2_sMu_enum.SetLineColor(ROOT.kBlack) ; h_eff_Chi2_sMu_enum.SetMarkerColor(ROOT.kBlack) 

h_eff_Chi2_enum = ROOT.TH1F('h_eff_Chi2_enum','',50,0,600)
tt.Draw('hnl_2d_disp >> h_eff_Chi2_enum','flag_matchedHNLChi2 == 1 & flag_hnl_reconstructable == 1')
h_eff_Chi2_denom = ROOT.TH1F('h_eff_Chi2_denom','',50,0,600)
tt.Draw('hnl_2d_disp >> h_eff_Chi2_denom','flag_hnl_reconstructable == 1')
h_eff_Chi2_enum.Divide(h_eff_Chi2_denom)
h_eff_Chi2_enum.SetTitle(';HNL 2D displacement ; HNL reconstruction efficiency')
h_eff_Chi2_enum.GetYaxis().SetRangeUser(0.,1.05)
h_eff_Chi2_enum.SetLineColor(ROOT.kRed+2 ) ; h_eff_Chi2_enum.SetMarkerColor(ROOT.kRed+2 ) 

h_eff_Dxy_sMu_enum = ROOT.TH1F('h_eff_Dxy_sMu_enum','',50,0,600)
tt.Draw('hnl_2d_disp >> h_eff_Dxy_sMu_enum','flag_matchedHNLDxy == 1 & dMu1Dxy_reco == 1 & dMu2Dxy_reco == 1 & flag_hnl_reconstructable == 1')
h_eff_Dxy_sMu_denom = ROOT.TH1F('h_eff_Dxy_sMu_denom','',50,0,600)
tt.Draw('hnl_2d_disp >> h_eff_Dxy_sMu_denom','dMu1Dxy_reco == 1 & dMu2Dxy_reco == 1 & flag_hnl_reconstructable == 1')
h_eff_Dxy_sMu_enum.Divide(h_eff_Dxy_sMu_denom)
h_eff_Dxy_sMu_enum.SetTitle(';HNL 2D displacement ; HNL reconstruction efficiency')
h_eff_Dxy_sMu_enum.GetYaxis().SetRangeUser(0.,1.05)
h_eff_Dxy_sMu_enum.SetLineColor(ROOT.kBlue+2) ; h_eff_Dxy_sMu_enum.SetMarkerColor(ROOT.kBlue+2) 

h_eff_Dxy_enum = ROOT.TH1F('h_eff_Dxy_enum','',50,0,600)
tt.Draw('hnl_2d_disp >> h_eff_Dxy_enum','flag_matchedHNLDxy == 1 & flag_hnl_reconstructable == 1')
h_eff_Dxy_denom = ROOT.TH1F('h_eff_Dxy_denom','',50,0,600)
tt.Draw('hnl_2d_disp >> h_eff_Dxy_denom','flag_hnl_reconstructable == 1')
h_eff_Dxy_enum.Divide(h_eff_Dxy_denom)
h_eff_Dxy_enum.SetTitle(';HNL 2D displacement ; HNL reconstruction efficiency')
h_eff_Dxy_enum.GetYaxis().SetRangeUser(0.,1.05)
h_eff_Dxy_enum.SetLineColor(ROOT.kGreen+2 ) ; h_eff_Dxy_enum.SetMarkerColor(ROOT.kGreen+2 ) 

h_eff_Chi2_sMu_enum.Draw()
h_eff_Chi2_enum.Draw('same')
h_eff_Dxy_sMu_enum.Draw('same')
h_eff_Dxy_enum.Draw('same')

leg = ROOT.TLegend(.4,.75,.8,.88)
leg.AddEntry(h_eff_Chi2_sMu_enum, 'Chi2, sMu'            ,'EP')
leg.AddEntry(h_eff_Chi2_enum, 'Chi2, sMu && dSAMu'            ,'EP')
leg.AddEntry(h_eff_Dxy_sMu_enum, 'Dxy, sMu'            ,'EP')
leg.AddEntry(h_eff_Dxy_enum, 'Dxy, sMu && dSAMu'            ,'EP')
leg.Draw('apez same')

pf.showlumi('%d entries'%(h_eff_Dxy_enum.GetEntries()))
pf.showlogopreliminary('CMS','Simulation Preliminary')

c_eff.Update()
c_eff.SaveAs(output_dir + 'c_eff.pdf')
c_eff.SaveAs(output_dir + 'c_eff.root')


######################################### 
# Reconstruction Efficiency
#########################################
print('Making the purity plot...')

c_purity = ROOT.TCanvas('c_purity', 'c_purity')

h_purity_Chi2_sMu_enum = ROOT.TH1F('h_purity_Chi2_sMu_enum','',50,0,600)
tt.Draw('hnl_2d_disp >> h_purity_Chi2_sMu_enum','flag_matchedHNLChi2 == 1 & dMu1Chi2_reco == 1 & dMu2Chi2_reco == 1')
h_purity_Chi2_sMu_denom = ROOT.TH1F('h_purity_Chi2_sMu_denom','',50,0,600)
tt.Draw('hnl_2d_disp >> h_purity_Chi2_sMu_denom','n_dimuon > 0 & dMu2Chi2_reco == 1 & dMu1Chi2_reco == 1')
h_purity_Chi2_sMu_enum.Divide(h_purity_Chi2_sMu_denom)
h_purity_Chi2_sMu_enum.SetTitle(';HNL 2D displacement ; HNL reconstruction purity')
h_purity_Chi2_sMu_enum.GetYaxis().SetRangeUser(0.,1.05)
h_purity_Chi2_sMu_enum.SetLineColor(ROOT.kBlack) ; h_purity_Chi2_sMu_enum.SetMarkerColor(ROOT.kBlack) 

h_purity_Chi2_enum = ROOT.TH1F('h_purity_Chi2_enum','',50,0,600)
tt.Draw('hnl_2d_disp >> h_purity_Chi2_enum','flag_matchedHNLChi2 == 1')
h_purity_Chi2_denom = ROOT.TH1F('h_purity_Chi2_denom','',50,0,600)
tt.Draw('hnl_2d_disp >> h_purity_Chi2_denom','n_dimuon > 0')
h_purity_Chi2_enum.Divide(h_purity_Chi2_denom)
h_purity_Chi2_enum.SetTitle(';HNL 2D displacement ; HNL reconstruction purity')
h_purity_Chi2_enum.GetYaxis().SetRangeUser(0.,1.05)
h_purity_Chi2_enum.SetLineColor(ROOT.kRed+2 ) ; h_purity_Chi2_enum.SetMarkerColor(ROOT.kRed+2 ) 

h_purity_Dxy_sMu_enum = ROOT.TH1F('h_purity_Dxy_sMu_enum','',50,0,600)
tt.Draw('hnl_2d_disp >> h_purity_Dxy_sMu_enum','flag_matchedHNLDxy == 1 & dMu1Dxy_reco == 1 & dMu2Dxy_reco == 1')
h_purity_Dxy_sMu_denom = ROOT.TH1F('h_purity_Dxy_sMu_denom','',50,0,600)
tt.Draw('hnl_2d_disp >> h_purity_Dxy_sMu_denom','n_dimuon > 0 & dMu1Dxy_reco == 1 & dMu2Dxy_reco == 1')
h_purity_Dxy_sMu_enum.Divide(h_purity_Dxy_sMu_denom)
h_purity_Dxy_sMu_enum.SetTitle(';HNL 2D displacement ; HNL reconstruction purity')
h_purity_Dxy_sMu_enum.GetYaxis().SetRangeUser(0.,1.05)
h_purity_Dxy_sMu_enum.SetLineColor(ROOT.kBlue+2) ; h_purity_Dxy_sMu_enum.SetMarkerColor(ROOT.kBlue+2) 

h_purity_Dxy_enum = ROOT.TH1F('h_purity_Dxy_enum','',50,0,600)
tt.Draw('hnl_2d_disp >> h_purity_Dxy_enum','flag_matchedHNLDxy == 1')
h_purity_Dxy_denom = ROOT.TH1F('h_purity_Dxy_denom','',50,0,600)
tt.Draw('hnl_2d_disp >> h_purity_Dxy_denom','n_dimuon > 0')
h_purity_Dxy_enum.Divide(h_purity_Dxy_denom)
h_purity_Dxy_enum.SetTitle(';HNL 2D displacement ; HNL reconstruction purity')
h_purity_Dxy_enum.GetYaxis().SetRangeUser(0.,1.05)
h_purity_Dxy_enum.SetLineColor(ROOT.kGreen+2 ) ; h_purity_Dxy_enum.SetMarkerColor(ROOT.kGreen+2 ) 

h_purity_Chi2_sMu_enum.Draw()
h_purity_Chi2_enum.Draw('same')
h_purity_Dxy_sMu_enum.Draw('same')
h_purity_Dxy_enum.Draw('same')

leg = ROOT.TLegend(.4,.75,.8,.88)
leg.AddEntry(h_purity_Chi2_sMu_enum, 'Chi2, sMu'            ,'EP')
leg.AddEntry(h_purity_Chi2_enum, 'Chi2, sMu && dSAMu'            ,'EP')
leg.AddEntry(h_purity_Dxy_sMu_enum, 'Dxy, sMu'            ,'EP')
leg.AddEntry(h_purity_Dxy_enum, 'Dxy, sMu && dSAMu'            ,'EP')
leg.Draw('apez same')

pf.showlumi('%d entries'%(h_purity_Dxy_enum.GetEntries()))
pf.showlogopreliminary('CMS','Simulation Preliminary')

c_purity.Update()
c_purity.SaveAs(output_dir + 'c_purity.pdf')
c_purity.SaveAs(output_dir + 'c_purity.root')


######################################### 
# Vertex Reconstruction
#########################################





















