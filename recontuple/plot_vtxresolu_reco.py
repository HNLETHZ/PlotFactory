import ROOT as rt
import plotfactory as pf
import numpy as np
import sys

pf.setpfstyle()
output_dir = '/afs/cern.ch/work/v/vstampf/plots/' 

fout = rt.TFile('histosvtxresolu.root', 'recreate')

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

n_reconstructable = tt.GetEntries('flag_hnl_reconstructable == 1 & abs(l1_pdgId) == 13 & abs(l1_eta) < 2.4 & abs(l2_pdgId) == 13 & abs(l2_eta) < 2.4') 
print('number of events with reconstructable HNLs:\t\t%d'%(n_reconstructable))

n_dimuons = tt.GetEntries('n_dimuon > 0 & abs(l1_pdgId) == 13 & abs(l1_eta) < 2.4 & abs(l2_pdgId) == 13 & abs(l2_eta) < 2.4') 
print('number of events with reconstructed DiMuons:\t\t%d'%(n_dimuons))

n_matchedHNLChi2 = tt.GetEntries('flag_matchedHNLChi2 == 1 & abs(l1_pdgId) == 13 & abs(l1_eta) < 2.4 & abs(l2_pdgId) == 13 & abs(l2_eta) < 2.4') 
print('number of correctly found HNLs using Chi2 method:\t%d'%(n_matchedHNLChi2))

n_matchedHNLDxy = tt.GetEntries('flag_matchedHNLDxy == 1 & abs(l1_pdgId) == 13 & abs(l1_eta) < 2.4 & abs(l2_pdgId) == 13 & abs(l2_eta) < 2.4')
print('number of correctly found HNLs using Dxy method:\t%d'%(n_matchedHNLDxy))

#n_matchedHNLChi2_and_recable = tt.GetEntries('flag_matchedHNLChi2 == 1 & flag_hnl_reconstructable ==1')
eff_Chi2_tot = float(n_matchedHNLChi2) / float(n_reconstructable)
# here it should be n_matchedHNL && n_reconstructable in the numerator
print('Reconstruction efficiency (min Chi2 method):\t\t%.1f%%'%(100*eff_Chi2_tot))

eff_Dxy_tot = float(n_matchedHNLDxy) / float(n_reconstructable)
# here it should be n_matchedHNL && n_reconstructable in the numerator
print('Reconstruction efficiency (max Dxy method):\t\t%.1f%%'%(100*eff_Dxy_tot))

pur_Chi2_tot = float(n_matchedHNLChi2) / float(n_dimuons)
print('Reconstruction purity (min Chi2 method):\t\t%.1f%%'%(100*pur_Chi2_tot))

pur_Dxy_tot = float(n_matchedHNLDxy) / float(n_dimuons)
print('Reconstruction purity (max Dxy method):\t\t\t%.1f%%'%(100*pur_Dxy_tot))

######################################### 
# initializing  histo's
######################################### 

c_vtx_reldiff_chi = rt.TCanvas('c_vtx_reldiff_chi', 'c_vtx_reldiff_chi')
c_vtx_reldiff_dxy = rt.TCanvas('c_vtx_reldiff_dxy', 'c_vtx_reldiff_dxy')
c_vtx_diff_chi = rt.TCanvas('c_vtx_diff_chi', 'c_vtx_diff_chi')
c_vtx_diff_dxy = rt.TCanvas('c_vtx_diff_dxy', 'c_vtx_diff_dxy')

print('Initializing histograms')

diffdxybins = np.arange(-40.,300,25)
reldiffdxybins = np.arange(-3.,1.5,0.25)
dxybins = np.arange(0.,600,50)

dxy_diff_chifit = rt.TH2F("dxy_diff_chifit","dxy_diff_chifit",len(dxybins)-1,dxybins,len(diffdxybins)-1,diffdxybins)
dxy_diff_dxyfit = rt.TH2F("dxy_diff_dxyfit","dxy_diff_dxyfit",len(dxybins)-1,dxybins,len(diffdxybins)-1,diffdxybins)
dxy_reldiff_chifit = rt.TH2F("dxy_reldiff_chifit","dxy_reldiff_chifit",len(dxybins)-1,dxybins,len(reldiffdxybins)-1,reldiffdxybins)
dxy_reldiff_dxyfit = rt.TH2F("dxy_reldiff_dxyfit","dxy_reldiff_dxyfit",len(dxybins)-1,dxybins,len(reldiffdxybins)-1,reldiffdxybins)

######################################### 
# Reconstruction Efficiency 
#########################################

print('Filling vertex resolution histograms')

tt.Draw("hnl_2d_disp - dimuonDxy_dxy:hnl_2d_disp >> dxy_diff_dxyfit", "abs(l0_pdgId) == 11 & flag_matchedHNLDxy == 1 & abs(l1_pdgId) == 13 & abs(l2_pdgId) == 13 & abs(l1_eta) < 2.4 & abs(l2_eta) < 2.4")
tt.Draw("hnl_2d_disp - dimuonChi2_dxy:hnl_2d_disp >> dxy_diff_chifit", "abs(l0_pdgId) == 11 & flag_matchedHNLChi2 == 1 & abs(l1_pdgId) == 13 & abs(l2_pdgId) == 13 & abs(l1_eta) < 2.4 & abs(l2_eta) < 2.4")

tt.Draw("(hnl_2d_disp - dimuonDxy_dxy)/hnl_2d_disp:hnl_2d_disp >> dxy_reldiff_dxyfit", "abs(l0_pdgId) == 11 & flag_matchedHNLDxy == 1 & abs(l1_pdgId) == 13 & abs(l2_pdgId) == 13 & abs(l1_eta) < 2.4 & abs(l2_eta) < 2.4")
tt.Draw("(hnl_2d_disp - dimuonChi2_dxy)/hnl_2d_disp:hnl_2d_disp >> dxy_reldiff_chifit", "abs(l0_pdgId) == 11 & flag_matchedHNLChi2 == 1 & abs(l1_pdgId) == 13 & abs(l2_pdgId) == 13 & abs(l1_eta) < 2.4 & abs(l2_eta) < 2.4")

c_vtx_diff_dxy.cd()
dxy_diff_dxyfit.Draw('colz')

c_vtx_diff_chi.cd()
dxy_diff_chifit.Draw('colz')

c_vtx_reldiff_dxy.cd()
dxy_reldiff_dxyfit.Draw('colz')

c_vtx_reldiff_chi.cd()
dxy_reldiff_chifit.Draw('colz')

hupd8lst = [dxy_diff_chifit,dxy_diff_dxyfit,dxy_reldiff_chifit,dxy_reldiff_dxyfit]

for hh in hupd8lst:
   hh.GetXaxis().SetTitle('HNL 2D displacement')
   hh.GetZaxis().SetTitle('Events')
   hh.GetXaxis().SetTitleOffset(1.2)
   hh.GetYaxis().SetTitleOffset(1.4)
   hh.GetZaxis().SetTitleOffset(1.4)
   hh.GetXaxis().SetRangeUser(0.,605)
#   hh.SetAxisRange(1,1e5,"Z")
for hh in [dxy_diff_chifit,dxy_diff_dxyfit]:
   hh.GetYaxis().SetTitle('vtx_{xy,gen}-vtx_{xy,reco}')
   hh.GetYaxis().SetRangeUser(-40.,305)

for hh in [dxy_reldiff_chifit,dxy_reldiff_dxyfit]:
   hh.GetYaxis().SetTitle('#frac{vtx_{xy,gen}-vtx_{xy,reco}}{vtx_{xy,gen}}')
   hh.GetYaxis().SetRangeUser(-3.,1.5)

print('Updating and saving pads')
for cc in [c_vtx_diff_dxy,c_vtx_diff_chi,c_vtx_reldiff_dxy,c_vtx_reldiff_chi]:
   cc.cd()
#   cc.SetLogz()
   pf.showlogoprelimsim('CMS')
#   rt.gStyle.SetOptStat(0)
   cc.Modified()
   cc.Update()
#   cc.SaveAs(output_dir+cc.GetTitle()+'.root')
#   cc.SaveAs(output_dir+cc.GetTitle()+'.pdf')


fout.Write()
#fout.Close()
















