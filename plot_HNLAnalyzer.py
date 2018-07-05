import ROOT as rt
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

# option for single file
# tt = rt.TChain('tree')
# tt.Add('/afs/cern.ch/user/d/dezhu/workspace/HNL/CMSSW_8_0_25/src/CMGTools/HNL/0_result/3_ntuples/HN3L_M_2p1_V_0p00316227766017_e_onshell_26/HNLTreeProducer/tree.root')

nentries = tt.GetEntries()
print('number of total entries in chain:\t\t\t%d'%(nentries))

######################################### 
# Produce KPIs
#########################################

n_2OrMoreMuons = tt.GetEntries()
print('number of all events with 2 or more muons:\t\t%d'%(n_2OrMoreMuons))

n_reconstructable = tt.GetEntries('flag_hnl_reconstructable == 1 & abs(l1_pdgId) == 13 & abs(l1_eta) < 2.4 & abs(l2_pdgId) == 13 & abs(l2_eta) < 2.4') 
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

pur_Chi2_tot = float(n_matchedHNLChi2) / float(n_dimuons)
print('Reconstruction purity (min Chi2 method):\t\t%.1f%%'%(100*pur_Chi2_tot))

pur_Dxy_tot = float(n_matchedHNLDxy) / float(n_dimuons)
print('Reconstruction purity (max Dxy method):\t\t\t%.1f%%'%(100*pur_Dxy_tot))

######################################### 
# initializing  histo's
######################################### 

print('Initializing histograms...')

h_eff_Chi2_sMu_enum = rt.TH1F('h_eff_Chi2_sMu_enum','',50,0,600)
h_eff_Chi2_sMu_denom = rt.TH1F('h_eff_Chi2_sMu_denom','',50,0,600)
h_eff_Chi2_enum = rt.TH1F('h_eff_Chi2_enum','',50,0,600)
h_eff_Chi2_denom = rt.TH1F('h_eff_Chi2_denom','',50,0,600)

h_eff_Dxy_sMu_enum = rt.TH1F('h_eff_Dxy_sMu_enum','',50,0,600)
h_eff_Dxy_sMu_denom = rt.TH1F('h_eff_Dxy_sMu_denom','',50,0,600)
h_eff_Dxy_enum = rt.TH1F('h_eff_Dxy_enum','',50,0,600)
h_eff_Dxy_denom = rt.TH1F('h_eff_Dxy_denom','',50,0,600)

h_pur_Chi2_sMu_enum = rt.TH1F('h_pur_Chi2_sMu_enum','',50,0,600)
h_pur_Chi2_sMu_denom = rt.TH1F('h_pur_Chi2_sMu_denom','',50,0,600)
h_pur_Chi2_enum = rt.TH1F('h_pur_Chi2_enum','',50,0,600)
h_pur_Chi2_denom = rt.TH1F('h_pur_Chi2_denom','',50,0,600)

h_pur_Dxy_sMu_enum = rt.TH1F('h_pur_Dxy_sMu_enum','',50,0,600)
h_pur_Dxy_sMu_denom = rt.TH1F('h_pur_Dxy_sMu_denom','',50,0,600)
h_pur_Dxy_enum = rt.TH1F('h_pur_Dxy_enum','',50,0,600)
h_pur_Dxy_denom = rt.TH1F('h_pur_Dxy_denom','',50,0,600)


######################################### 
# Reconstruction Efficiency 
#########################################

print('Making the efficiency plot...')

c_eff = rt.TCanvas('c_eff', 'c_eff')

tt.Draw('hnl_2d_disp >> h_eff_Chi2_sMu_enum','abs(l0_pdgId) == 11 & flag_matchedHNLChi2 == 1 & dMu1Chi2_reco == 1 & dMu2Chi2_reco == 1 & flag_hnl_reconstructable == 1 & abs(l1_pdgId) == 13 & abs(l1_eta) < 2.4 & abs(l2_pdgId) == 13 & abs(l2_eta) < 2.4')
tt.Draw('hnl_2d_disp >> h_eff_Chi2_sMu_denom','abs(l0_pdgId) == 11 & flag_hnl_reconstructable == 1 & abs(l1_pdgId) == 13 & abs(l1_eta) < 2.4 & abs(l2_pdgId) == 13 & abs(l2_eta) < 2.4')
# probably we shouldn't use the dMu flags in the denominator here

tt.Draw('hnl_2d_disp >> h_eff_Chi2_enum','abs(l0_pdgId) == 11 & flag_matchedHNLChi2 == 1 & flag_hnl_reconstructable == 1 & abs(l1_pdgId) == 13 & abs(l1_eta) < 2.4 & abs(l2_pdgId) == 13 & abs(l2_eta) < 2.4')
tt.Draw('hnl_2d_disp >> h_eff_Chi2_denom','abs(l0_pdgId) == 11 & flag_hnl_reconstructable == 1 & abs(l1_pdgId) == 13 & abs(l1_eta) < 2.4 & abs(l2_pdgId) == 13 & abs(l2_eta) < 2.4')

tt.Draw('hnl_2d_disp >> h_eff_Dxy_sMu_enum','abs(l0_pdgId) == 11 & flag_matchedHNLDxy == 1 & dMu1Dxy_reco == 1 & dMu2Dxy_reco == 1 & flag_hnl_reconstructable == 1 & abs(l1_pdgId) == 13 & abs(l1_eta) < 2.4 & abs(l2_pdgId) == 13 & abs(l2_eta) < 2.4')
tt.Draw('hnl_2d_disp >> h_eff_Dxy_sMu_denom','abs(l0_pdgId) == 11 & flag_hnl_reconstructable == 1 & abs(l1_pdgId) == 13 & abs(l1_eta) < 2.4 & abs(l2_pdgId) == 13 & abs(l2_eta) < 2.4')
# probably we shouldn't use the dMu flags in the denominator here

tt.Draw('hnl_2d_disp >> h_eff_Dxy_enum','abs(l0_pdgId) == 11 & flag_matchedHNLDxy == 1 & flag_hnl_reconstructable == 1 & abs(l1_pdgId) == 13 & abs(l1_eta) < 2.4 & abs(l2_pdgId) == 13 & abs(l2_eta) < 2.4')
tt.Draw('hnl_2d_disp >> h_eff_Dxy_denom','abs(l0_pdgId) == 11 & flag_hnl_reconstructable == 1 & abs(l1_pdgId) == 13 & abs(l1_eta) < 2.4 & abs(l2_pdgId) == 13 & abs(l2_eta) < 2.4')

h_eff_Chi2_sMu_enum.Divide(h_eff_Chi2_sMu_denom)
h_eff_Chi2_sMu_enum.SetTitle(';HNL 2D displacement ; HNL reconstruction efficiency')
h_eff_Chi2_sMu_enum.GetYaxis().SetRangeUser(0.,1.05)
h_eff_Chi2_sMu_enum.SetLineColor(rt.kBlack) ; h_eff_Chi2_sMu_enum.SetMarkerColor(rt.kBlack) 

h_eff_Chi2_enum.Divide(h_eff_Chi2_denom)
h_eff_Chi2_enum.SetTitle(';HNL 2D displacement ; HNL reconstruction efficiency')
h_eff_Chi2_enum.GetYaxis().SetRangeUser(0.,1.05)
h_eff_Chi2_enum.SetLineColor(rt.kRed+2) ; h_eff_Chi2_enum.SetMarkerColor(rt.kRed+2) 

h_eff_Dxy_sMu_enum.Divide(h_eff_Dxy_sMu_denom)
h_eff_Dxy_sMu_enum.SetTitle(';HNL 2D displacement ; HNL reconstruction efficiency')
h_eff_Dxy_sMu_enum.GetYaxis().SetRangeUser(0.,1.05)
h_eff_Dxy_sMu_enum.SetLineColor(rt.kBlue+2) ; h_eff_Dxy_sMu_enum.SetMarkerColor(rt.kBlue+2) 

h_eff_Dxy_enum.Divide(h_eff_Dxy_denom)
h_eff_Dxy_enum.SetTitle(';HNL 2D displacement ; HNL reconstruction efficiency')
h_eff_Dxy_enum.GetYaxis().SetRangeUser(0.,1.05)
h_eff_Dxy_enum.SetLineColor(rt.kGreen+2) ; h_eff_Dxy_enum.SetMarkerColor(rt.kGreen+2) 

h_eff_Chi2_sMu_enum.Draw()
h_eff_Chi2_enum.Draw('same')
h_eff_Dxy_sMu_enum.Draw('same')
h_eff_Dxy_enum.Draw('same')

efleg = rt.TLegend(.4,.75,.8,.88)
efleg.AddEntry(h_eff_Chi2_sMu_enum, 'Chi2, sMu'            ,'EP')
efleg.AddEntry(h_eff_Chi2_enum, 'Chi2, sMu && dSAMu'            ,'EP')
efleg.AddEntry(h_eff_Dxy_sMu_enum, 'Dxy, sMu'            ,'EP')
efleg.AddEntry(h_eff_Dxy_enum, 'Dxy, sMu && dSAMu'            ,'EP')
efleg.Draw('apez same')

pf.showlumi('%d entries'%(h_eff_Dxy_enum.GetEntries()))
pf.showlogopreliminary('CMS', 'Simulation Preliminary')

c_eff.Modified()
c_eff.Update()
# c_eff.SaveAs(output_dir + 'c_eff.pdf')
# c_eff.SaveAs(output_dir + 'c_eff.root')

######################################### 
# Reconstruction Purity
#########################################

print('Making the purity plot...')

c_pur = rt.TCanvas('c_pur', 'c_pur')

tt.Draw('hnl_2d_disp >> h_pur_Chi2_sMu_enum','abs(l0_pdgId) == 11 & flag_matchedHNLChi2 == 1 & dMu1Chi2_reco == 1 & dMu2Chi2_reco == 1 & abs(l1_pdgId) == 13 & abs(l1_eta) < 2.4 & abs(l2_pdgId) == 13 & abs(l2_eta) < 2.4')
tt.Draw('hnl_2d_disp >> h_pur_Chi2_sMu_denom','abs(l0_pdgId) == 11 & n_dimuon > 0 & abs(l1_pdgId) == 13 & abs(l1_eta) < 2.4 & abs(l2_pdgId) == 13 & abs(l2_eta) < 2.4')
# probably we shouldn't use the dMu flags in the denominator here

tt.Draw('hnl_2d_disp >> h_pur_Chi2_enum','abs(l0_pdgId) == 11 & flag_matchedHNLChi2 == 1 & abs(l1_pdgId) == 13 & abs(l1_eta) < 2.4 & abs(l2_pdgId) == 13 & abs(l2_eta) < 2.4')
tt.Draw('hnl_2d_disp >> h_pur_Chi2_denom','abs(l0_pdgId) == 11 & n_dimuon > 0 & abs(l1_pdgId) == 13 & abs(l1_eta) < 2.4 & abs(l2_pdgId) == 13 & abs(l2_eta) < 2.4')

tt.Draw('hnl_2d_disp >> h_pur_Dxy_sMu_enum','abs(l0_pdgId) == 11 & flag_matchedHNLDxy == 1 & dMu1Dxy_reco == 1 & dMu2Dxy_reco == 1 & abs(l1_pdgId) == 13 & abs(l1_eta) < 2.4 & abs(l2_pdgId) == 13 & abs(l2_eta) < 2.4')
tt.Draw('hnl_2d_disp >> h_pur_Dxy_sMu_denom','abs(l0_pdgId) == 11 & n_dimuon > 0 & abs(l1_pdgId) == 13 & abs(l1_eta) < 2.4 & abs(l2_pdgId) == 13 & abs(l2_eta) < 2.4')
# probably we shouldn't use the dMu flags in the denominator here

tt.Draw('hnl_2d_disp >> h_pur_Dxy_enum','abs(l0_pdgId) == 11 & flag_matchedHNLDxy == 1 & abs(l1_pdgId) == 13 & abs(l1_eta) < 2.4 & abs(l2_pdgId) == 13 & abs(l2_eta) < 2.4')
tt.Draw('hnl_2d_disp >> h_pur_Dxy_denom','abs(l0_pdgId) == 11 & n_dimuon > 0 & abs(l1_pdgId) == 13 & abs(l1_eta) < 2.4 & abs(l2_pdgId) == 13 & abs(l2_eta) < 2.4')

h_pur_Chi2_sMu_enum.Divide(h_pur_Chi2_sMu_denom)
h_pur_Chi2_sMu_enum.SetTitle(';HNL 2D displacement ; HNL reconstruction purity')
h_pur_Chi2_sMu_enum.GetYaxis().SetRangeUser(0.,1.05)
h_pur_Chi2_sMu_enum.SetLineColor(rt.kBlack) ; h_pur_Chi2_sMu_enum.SetMarkerColor(rt.kBlack) 

h_pur_Chi2_enum.Divide(h_pur_Chi2_denom)
h_pur_Chi2_enum.SetTitle(';HNL 2D displacement ; HNL reconstruction purity')
h_pur_Chi2_enum.GetYaxis().SetRangeUser(0.,1.05)
h_pur_Chi2_enum.SetLineColor(rt.kRed+2) ; h_pur_Chi2_enum.SetMarkerColor(rt.kRed+2) 

h_pur_Dxy_sMu_enum.Divide(h_pur_Dxy_sMu_denom)
h_pur_Dxy_sMu_enum.SetTitle(';HNL 2D displacement ; HNL reconstruction purity')
h_pur_Dxy_sMu_enum.GetYaxis().SetRangeUser(0.,1.05)
h_pur_Dxy_sMu_enum.SetLineColor(rt.kBlue+2) ; h_pur_Dxy_sMu_enum.SetMarkerColor(rt.kBlue+2) 

h_pur_Dxy_enum.Divide(h_pur_Dxy_denom)
h_pur_Dxy_enum.SetTitle(';HNL 2D displacement ; HNL reconstruction purity')
h_pur_Dxy_enum.GetYaxis().SetRangeUser(0.,1.05)
h_pur_Dxy_enum.SetLineColor(rt.kGreen+2) ; h_pur_Dxy_enum.SetMarkerColor(rt.kGreen+2) 

h_pur_Chi2_sMu_enum.Draw()
h_pur_Chi2_enum.Draw('same')
h_pur_Dxy_sMu_enum.Draw('same')
h_pur_Dxy_enum.Draw('same')

puleg = rt.TLegend(.4,.75,.8,.88)
puleg.AddEntry(h_pur_Chi2_sMu_enum, 'Chi2, sMu'            ,'EP')
puleg.AddEntry(h_pur_Chi2_enum, 'Chi2, sMu && dSAMu'            ,'EP')
puleg.AddEntry(h_pur_Dxy_sMu_enum, 'Dxy, sMu'            ,'EP')
puleg.AddEntry(h_pur_Dxy_enum, 'Dxy, sMu && dSAMu'            ,'EP')
puleg.Draw('apez same')

pf.showlumi('%d entries'%(h_pur_Dxy_enum.GetEntries()))
pf.showlogopreliminary('CMS','Simulation Preliminary')

c_pur.Modified()
c_pur.Update()
# c_pur.SaveAs(output_dir + 'c_pur.pdf')
# c_pur.SaveAs(output_dir + 'c_pur.root')

######################################### 
# Vertex Reconstruction
#########################################
print'making vertex reconstruction plots'

c_VtxRes = rt.TCanvas('c_VtxRes', 'c_VtxRes')
h_VtxRes = rt.TH2F('h_VtxRes','',50,0.,100.,50,0.,100.)
tt.Draw('dimuonChi2_dxy:sqrt(sv_reco_x*sv_reco_x + sv_reco_y*sv_reco_y) >> h_VtxRes')
h_VtxRes.SetTitle(';recoSV_dxy [cm] ; recoHNL_dxy [cm]')
h_VtxRes.Draw('colz')


c_VtxResGen = rt.TCanvas('c_VtxResGen', 'c_VtxResGen')
h_VtxResGen = rt.TH2F('h_VtxResGen','',50,0.,100.,50,0.,100.)
tt.Draw('dimuonChi2_dxy:sqrt(sv_x*sv_x + sv_y*sv_y) >> h_VtxResGen','l1_charge!=l2_charge & abs(l1_eta)<2.4 & abs(l2_eta)<2.4 & l1_pt>5 & l2_pt>5')
h_VtxResGen.SetTitle(';GenSV_dxy [cm] ; recoHNL_dxy [cm]')
h_VtxResGen.Draw('colz')


######################################### 
# Reconstruction Efficiency V2
#########################################
print'making more efficiency plots'
c_eff2 = rt.TCanvas('c_eff2','c_eff2')
h_eff2_0 = rt.TH1F('h_eff2_0','',50,0,200)
h_eff2_1 = rt.TH1F('h_eff2_1','',50,0,200)
h_eff2_2 = rt.TH1F('h_eff2_2','',50,0,200)
h_eff2_3 = rt.TH1F('h_eff2_3','',50,0,200)

# selection 0: all gen info should point towards that the HNL is reconstructable
selection0 = 'abs(l1_pdgId)==13 & abs(l2_pdgId)==13 & abs(l1_eta)<2.4 & abs(l2_eta)<2.4 & l1_pt>10 & l2_pt>10'

# selection 1: for l1 and l2 there should exist for each a reco muon
selection1 = '(l1_matched_muon_pt>0 | l1_matched_dsmuon_pt>0) & (l2_matched_muon_pt>0 | l2_matched_dsmuon_pt>0) & ((l1_matched_muon_pt != l2_matched_muon_pt) | (l1_matched_dsmuon_pt != l2_matched_dsmuon_pt))'

# selection 2: HNL Analyzer has selected the correct l1 and l2 
selection2 = '(dMu1Chi2_pt == l1_matched_muon_pt | dMu1Chi2_pt == l1_matched_dsmuon_pt | dMu1Chi2_pt == l2_matched_muon_pt | dMu1Chi2_pt == l2_matched_dsmuon_pt) & (dMu2Chi2_pt == l1_matched_muon_pt | dMu2Chi2_pt == l1_matched_dsmuon_pt | dMu2Chi2_pt == l2_matched_muon_pt | dMu2Chi2_pt == l2_matched_dsmuon_pt)'

# selection 3: The vertex fitter has reconstructed the correct vertex
selection3 = 'abs((sv_reco_x-sv_x)/(sv_x))<0.3 & abs((sv_reco_y-sv_y)/(sv_y))<0.3 & abs((sv_reco_z-sv_z)/(sv_z))<0.3'

# draw the efficiency plots
tt.Draw('hnl_2d_disp >> h_eff2_0',selection0)
tt.Draw('hnl_2d_disp >> h_eff2_1','&'.join([selection0,selection1]))
tt.Draw('hnl_2d_disp >> h_eff2_2','&'.join([selection0,selection1,selection2]))
tt.Draw('hnl_2d_disp >> h_eff2_3','&'.join([selection0,selection1,selection2,selection3]))

# make efficiencies
h_eff2_3.Divide(h_eff2_2)
h_eff2_2.Divide(h_eff2_1)
h_eff2_1.Divide(h_eff2_0)


# plot settings
h_eff2_0.SetTitle(';HNL 2D displacement [cm]; Efficiency')
h_eff2_0.GetYaxis().SetRangeUser(0.,1.05)
h_eff2_0.SetLineColor  (rt.kBlack)
h_eff2_0.SetMarkerColor(rt.kBlack)
h_eff2_1.SetLineColor  (rt.kRed)
h_eff2_1.SetMarkerColor(rt.kRed)
h_eff2_2.SetLineColor  (rt.kGreen)
h_eff2_2.SetMarkerColor(rt.kGreen)
h_eff2_3.SetLineColor  (rt.kBlue)
h_eff2_3.SetMarkerColor(rt.kBlue)

# draw plots
# h_eff2_0.Draw()
h_eff2_1.Draw()
h_eff2_2.Draw('same')
h_eff2_3.Draw('same')

# build legend
l_eff2 = rt.TLegend(.4,.75,.8,.88)
l_eff2.AddEntry(h_eff2_0, 'selection 0: gen','EP')
l_eff2.AddEntry(h_eff2_1, 'selection 1: there is reco','EP')
l_eff2.AddEntry(h_eff2_2, 'selection 2: correct recos were selected','EP')
l_eff2.AddEntry(h_eff2_3, 'selection 3: vertex','EP')
l_eff2.Draw('apez same')

c_eff2.Update()
