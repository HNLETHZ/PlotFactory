import ROOT as rt
import plotfactory as pf
import numpy as np
import sys

pf.setpfstyle()
output_dir = '/afs/cern.ch/work/v/vstampf/plots/candidates/gentuple/' 

fout = rt.TFile(output_dir+'histos3dispflav.root', 'recreate')

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
# initializing  histo's
######################################### 

c_3disp_flavors = rt.TCanvas('3disp_flavors', '3disp_flavors')
c_3disp_gen_reco = rt.TCanvas('3disp_gen_reco', '3disp_gen_reco')

print('Initializing histograms')

dxybins = np.logspace(-1,2.78,15)

h_3disp_mumu = rt.TH1F("3disp_mumu","3disp_mumu",len(dxybins)-1,dxybins)
h_3disp_ee = rt.TH1F("3disp_ee","3disp_ee",len(dxybins)-1,dxybins)
h_3disp_emu = rt.TH1F("3disp_emu","3disp_emu",len(dxybins)-1,dxybins)
h_3disp_mue = rt.TH1F("3disp_mue","3disp_mue",len(dxybins)-1,dxybins)
h_3disp_gen_reco = rt.TH2F("3disp_gen_reco","3disp_gen_reco",len(dxybins)-1,dxybins,len(dxybins)-1,dxybins)

######################################### 
# Filling Histograms 
#########################################

print('Filling histograms')

tt.Draw("hnl_3d_reco_disp:hnl_3d_disp >> 3disp_gen_reco", "abs(l2_pdgId) == 13 & abs(l1_pdgId) == 13 & is_in_acc == 1 & hnl_3d_reco_disp > -90")

tt.Draw("hnl_3d_disp >> 3disp_mumu", "abs(l2_pdgId) == 13 & abs(l1_pdgId) == 13 & is_in_acc == 1")# & hnl_3d_reco_disp > -90")
tt.Draw("hnl_3d_disp >> 3disp_ee", "abs(l2_pdgId) == 11 & abs(l1_pdgId) == 11 & is_in_acc == 1")# & hnl_3d_reco_disp > -90")
tt.Draw("hnl_3d_disp >> 3disp_emu", "abs(l2_pdgId) == 11 & abs(l1_pdgId) == 13 & is_in_acc == 1")# & hnl_3d_reco_disp > -90")
tt.Draw("hnl_3d_disp >> 3disp_mue", "abs(l2_pdgId) == 13 & abs(l1_pdgId) == 11 & is_in_acc == 1")# & hnl_3d_reco_disp > -90")

h_3disp_emu.Add(h_3disp_mue)

c_3disp_gen_reco.cd()
h_3disp_gen_reco.Draw('colztext')

c_3disp_flavors.cd()
h_3disp_mumu.SetMarkerColor(rt.kGreen+2)
h_3disp_emu.SetMarkerColor(rt.kBlue+2)
h_3disp_ee.SetMarkerColor(rt.kRed+2)
h_3disp_emu.Draw()
h_3disp_ee.Draw('same')
h_3disp_mumu.Draw('same')

hupd8lst = [h_3disp_gen_reco,h_3disp_mumu,h_3disp_ee,h_3disp_emu]

h_3disp_gen_reco.GetZaxis().SetTitle('Events (sel: in_acc & hnl_reco)')
h_3disp_gen_reco.GetZaxis().SetTitleOffset(1.4)
h_3disp_gen_reco.GetYaxis().SetRangeUser(0.,605)
h_3disp_gen_reco.GetYaxis().SetTitle('HNL 3D reco displacement')

for hh in hupd8lst:
   hh.GetXaxis().SetTitle('HNL 3D gen displacement')
   hh.GetXaxis().SetTitleOffset(1.2)
   hh.GetYaxis().SetTitleOffset(1.4)
   hh.GetXaxis().SetRangeUser(0.,605)
#   hh.SetAxisRange(1,1e5,"Z")

h_3disp_emu.GetYaxis().SetTitle('Events (sel: in_acc)')
c_3disp_flavors.SetLogz()
c_3disp_flavors.SetLogy()
c_3disp_flavors.BuildLegend()

print('Updating and saving pads')
for cc in [c_3disp_gen_reco,c_3disp_flavors]:
   cc.cd()
   cc.SetLogx()
   pf.showlogoprelimsim('CMS')
#   rt.gStyle.SetOptStat(0)
   cc.Modified()
   cc.Update()
   cc.SaveAs(output_dir+cc.GetTitle()+'.root')
   cc.SaveAs(output_dir+cc.GetTitle()+'.pdf')

fout.Write()

