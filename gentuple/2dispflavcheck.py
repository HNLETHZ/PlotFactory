import ROOT as rt
import plotfactory as pf
import numpy as np
import sys
rt.gROOT.SetBatch(True)

pf.setpfstyle()
output_dir = '/afs/cern.ch/work/v/vstampf/plots/candidates/gentuple/' 

fout = rt.TFile(output_dir+'histos2dispflav.root', 'recreate')

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

c_2disp_flavors = rt.TCanvas('2disp_flavors', '2disp_flavors')
c_2disp_gen_reco = rt.TCanvas('2disp_gen_reco', '2disp_gen_reco')

print('Initializing histograms')

#dxybins = np.arange(0.,600,50)
dxybins = np.logspace(-1,2.78,15)

h_2disp_mumu = rt.TH1F("2disp_mumu","2disp_mumu",len(dxybins)-1,dxybins)
h_2disp_ee = rt.TH1F("2disp_ee","2disp_ee",len(dxybins)-1,dxybins)
h_2disp_emu = rt.TH1F("2disp_emu","2disp_emu",len(dxybins)-1,dxybins)
h_2disp_mue = rt.TH1F("2disp_mue","2disp_mue",len(dxybins)-1,dxybins)
h_2disp_gen_reco = rt.TH2F("2disp_gen_reco","2disp_gen_reco",len(dxybins)-1,dxybins,len(dxybins)-1,dxybins)

######################################### 
# Filling Histograms 
#########################################

print('Filling histograms')

tt.Draw("hnl_2d_reco_disp:hnl_2d_disp >> 2disp_gen_reco", "abs(l2_pdgId) == 13 & abs(l1_pdgId) == 13 & is_in_acc == 1 & hnl_2d_reco_disp > -90")

tt.Draw("hnl_2d_disp >> 2disp_mumu", "abs(l2_pdgId) == 13 & abs(l1_pdgId) == 13 & is_in_acc == 1")# & hnl_2d_reco_disp > -90")
tt.Draw("hnl_2d_disp >> 2disp_ee", "abs(l2_pdgId) == 11 & abs(l1_pdgId) == 11 & is_in_acc == 1")# & hnl_2d_reco_disp > -90")
tt.Draw("hnl_2d_disp >> 2disp_emu", "abs(l2_pdgId) == 11 & abs(l1_pdgId) == 13 & is_in_acc == 1")# & hnl_2d_reco_disp > -90")
tt.Draw("hnl_2d_disp >> 2disp_mue", "abs(l2_pdgId) == 13 & abs(l1_pdgId) == 11 & is_in_acc == 1")# & hnl_2d_reco_disp > -90")

h_2disp_emu.Add(h_2disp_mue)

c_2disp_gen_reco.cd()
h_2disp_gen_reco.Draw('colztext')

c_2disp_flavors.cd()
h_2disp_mumu.SetMarkerColor(rt.kGreen+2)
h_2disp_emu.SetMarkerColor(rt.kBlue+2)
h_2disp_ee.SetMarkerColor(rt.kRed+2)
h_2disp_emu.Draw()
h_2disp_ee.Draw('same')
h_2disp_mumu.Draw('same')

hupd8lst = [h_2disp_gen_reco,h_2disp_mumu,h_2disp_ee,h_2disp_emu]

h_2disp_gen_reco.GetZaxis().SetTitle('Events (sel: in_acc & hnl_reco)')
h_2disp_gen_reco.GetZaxis().SetTitleOffset(1.4)
h_2disp_gen_reco.GetYaxis().SetRangeUser(0.,605)
h_2disp_gen_reco.GetYaxis().SetTitle('HNL 2D reco displacement')

for hh in hupd8lst:
   hh.GetXaxis().SetTitle('HNL 2D gen displacement')
   hh.GetXaxis().SetTitleOffset(1.2)
   hh.GetYaxis().SetTitleOffset(1.4)
   hh.GetXaxis().SetRangeUser(0.,605)
#   hh.SetAxisRange(1,1e5,"Z")

h_2disp_emu.GetYaxis().SetTitle('Events (sel: in_acc)')
c_2disp_flavors.SetLogz()
c_2disp_flavors.SetLogy()
c_2disp_flavors.BuildLegend()

print('Updating and saving pads')
for cc in [c_2disp_gen_reco,c_2disp_flavors]:
   cc.cd()
   cc.SetLogx()
   pf.showlogoprelimsim('CMS')
#   rt.gStyle.SetOptStat(0)
   cc.Modified()
   cc.Update()
   cc.SaveAs(output_dir+cc.GetTitle()+'.root')
   cc.SaveAs(output_dir+cc.GetTitle()+'.pdf')


fout.Write()

