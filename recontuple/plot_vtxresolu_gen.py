import ROOT as rt
import plotfactory as pf
import numpy as np
import sys

pf.setpfstyle()
output_dir = '/afs/cern.ch/work/v/vstampf/plots/candidates/recontuple/' 

fout = rt.TFile(output_dir+'histosvtxresolu.root', 'recreate')

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

fin = rt.TFile('/afs/cern.ch/work/v/vstampf/ntuples/gen/HN3L_M_3_V_0p00707106781187_e_onshell_1/HNLGenTreeProducer/tree.root')
tt = fin.Get('tree') 

nentries = tt.GetEntries()
print('number of total entries in chain:\t\t\t%d'%(nentries))

######################################### 
# Produce KPIs
#########################################

# n_2OrMoreMuons = tt.GetEntries()
# print('number of all events with 2 or more muons:\t\t%d'%(n_2OrMoreMuons))
# 
# n_reconstructable = tt.GetEntries('flag_hnl_reconstructable == 1 & abs(l1_pdgId) == 13 & abs(l1_eta) < 2.4 & abs(l2_pdgId) == 13 & abs(l2_eta) < 2.4') 
# print('number of events with reconstructable HNLs:\t\t%d'%(n_reconstructable))
# 
# n_dimuons = tt.GetEntries('n_dimuon > 0 & abs(l1_pdgId) == 13 & abs(l1_eta) < 2.4 & abs(l2_pdgId) == 13 & abs(l2_eta) < 2.4') 
# print('number of events with reconstructed DiMuons:\t\t%d'%(n_dimuons))
# 
# n_matchedHNLChi2 = tt.GetEntries('flag_matchedHNLChi2 == 1 & abs(l1_pdgId) == 13 & abs(l1_eta) < 2.4 & abs(l2_pdgId) == 13 & abs(l2_eta) < 2.4') 
# print('number of correctly found HNLs using Chi2 method:\t%d'%(n_matchedHNLChi2))
# 
# n_matchedHNLDxy = tt.GetEntries('abs(l1_pdgId) == 13 & abs(l1_eta) < 2.4 & abs(l2_pdgId) == 13 & abs(l2_eta) < 2.4')
# print('number of correctly found HNLs using Dxy method:\t%d'%(n_matchedHNLDxy))
# 
# #n_matchedHNLChi2_and_recable = tt.GetEntries('flag_matchedHNLChi2 == 1 & flag_hnl_reconstructable ==1')
# eff_Chi2_tot = float(n_matchedHNLChi2) / float(n_reconstructable)
# # here it should be n_matchedHNL && n_reconstructable in the numerator
# print('Reconstruction efficiency (min Chi2 method):\t\t%.1f%%'%(100*eff_Chi2_tot))
# 
# eff_Dxy_tot = float(n_matchedHNLDxy) / float(n_reconstructable)
# # here it should be n_matchedHNL && n_reconstructable in the numerator
# print('Reconstruction efficiency (max Dxy method):\t\t%.1f%%'%(100*eff_Dxy_tot))
# 
# pur_Chi2_tot = float(n_matchedHNLChi2) / float(n_dimuons)
# print('Reconstruction purity (min Chi2 method):\t\t%.1f%%'%(100*pur_Chi2_tot))
# 
# pur_Dxy_tot = float(n_matchedHNLDxy) / float(n_dimuons)
# print('Reconstruction purity (max Dxy method):\t\t\t%.1f%%'%(100*pur_Dxy_tot))

######################################### 
# initializing  histo's
######################################### 

c_vtx_reldiff = rt.TCanvas('c_vtx_reldiff', 'c_vtx_reldiff')
c_vtx_diff = rt.TCanvas('c_vtx_diff', 'c_vtx_diff')

print('Initializing histograms')

diffdxybins = np.arange(-40.,300,25)
reldiffdxybins = np.arange(-3.,1.5,0.25)
dxybins = np.arange(0.,600,50)

dxy_diff = rt.TH2F("dxy_diff","dxy_diff",len(dxybins)-1,dxybins,len(diffdxybins)-1,diffdxybins)
dxy_reldiff = rt.TH2F("dxy_reldiff","dxy_reldiff",len(dxybins)-1,dxybins,len(reldiffdxybins)-1,reldiffdxybins)

######################################### 
# Reconstruction Efficiency 
#########################################

print('Filling vertex resolution histograms')

tt.Draw("hnl_2d_disp - hnl_2d_reco_disp:hnl_2d_disp >> dxy_diff", "abs(l2_pdgId) == 13 & abs(l1_pdgId) == 13")# & is_in_acc == 1")# & hnl_2d_reco_disp > -90")

tt.Draw("(hnl_2d_disp - hnl_2d_reco_disp)/hnl_2d_disp:hnl_2d_disp >> dxy_reldiff", "abs(l2_pdgId) == 13 & abs(l1_pdgId) == 13")# & is_in_acc == 1")# & hnl_2d_reco_disp > -90")

c_vtx_diff.cd()
dxy_diff.Draw('colz')

c_vtx_diff.cd()
dxy_diff.Draw('colz')

c_vtx_reldiff.cd()
dxy_reldiff.Draw('colz')

c_vtx_reldiff.cd()
dxy_reldiff.Draw('colz')

hupd8lst = [dxy_diff,dxy_reldiff]

for hh in hupd8lst:
   hh.GetXaxis().SetTitle('HNL 2D displacement')
   hh.GetZaxis().SetTitle('Events')
   hh.GetXaxis().SetTitleOffset(1.2)
   hh.GetYaxis().SetTitleOffset(1.4)
   hh.GetZaxis().SetTitleOffset(1.4)
   hh.GetXaxis().SetRangeUser(0.,605)
#   hh.SetAxisRange(1,1e5,"Z")
for hh in [dxy_diff,dxy_diff]:
   hh.GetYaxis().SetTitle('vtx_{xy,gen}-vtx_{xy,reco}')
   hh.GetYaxis().SetRangeUser(-40.,305)

for hh in [dxy_reldiff,dxy_reldiff]:
   hh.GetYaxis().SetTitle('#frac{vtx_{xy,gen}-vtx_{xy,reco}}{vtx_{xy,gen}}')
   hh.GetYaxis().SetRangeUser(-3.,1.5)

print('Updating and saving pads')
for cc in [c_vtx_diff,c_vtx_reldiff]:
   cc.cd()
#   cc.SetLogz()
   pf.showlogoprelimsim('CMS')
#   rt.gStyle.SetOptStat(0)
   cc.Modified()
   cc.Update()
#   cc.SaveAs(output_dir+cc.GetTitle()+'.root')
#   cc.SaveAs(output_dir+cc.GetTitle()+'.pdf')


#fout.Write()
#fout.Close()
















