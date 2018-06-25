import ROOT as rt
import numpy as np
import plotfactory as pf
import sys
from pdb import set_trace

output_dir = '/afs/cern.ch/work/v/vstampf/plots/candidates/gentuple/' 

######################################### 
# Make Chain from selection of samples
#########################################

fout = rt.TFile(output_dir+'signcheckM.root', 'recreate')

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

pf.setpfstyle()

c_signs_l01 = rt.TCanvas('signs_l01', 'signs_l01')
c_signs_l12 = rt.TCanvas('signs_l12', 'signs_l12')
c_signs_l02 = rt.TCanvas('signs_l02', 'signs_l02')
c_eos_l01 = rt.TCanvas('signs_eos_l01', 'eos_l01')
c_eos_l12 = rt.TCanvas('signs_eos_l12', 'eos_l12')
c_eos_l02 = rt.TCanvas('signs_eos_l02', 'eos_l02')
c_mos_l01 = rt.TCanvas('signs_mos_l01', 'mos_l01')
c_mos_l12 = rt.TCanvas('signs_mos_l12', 'mos_l12')
c_mos_l02 = rt.TCanvas('signs_mos_l02', 'mos_l02')
c_m1_l01 = rt.TCanvas('signs_m1_l01', 'm1_l01')
c_m1_l12 = rt.TCanvas('signs_m1_l12', 'm1_l12')
c_m1_l02 = rt.TCanvas('signs_m1_l02', 'm1_l02')
c_m2_l01 = rt.TCanvas('signs_m2_l01', 'm2_l01')
c_m2_l12 = rt.TCanvas('signs_m2_l12', 'm2_l12')
c_m2_l02 = rt.TCanvas('signs_m2_l02', 'm2_l02')
c_m3_l01 = rt.TCanvas('signs_m3_l01', 'm3_l01')
c_m3_l12 = rt.TCanvas('signs_m3_l12', 'm3_l12')
c_m3_l02 = rt.TCanvas('signs_m3_l02', 'm3_l02')


b_signs = np.arange(-1.,3,1.5)

h_signs_l01 = rt.TH2F('h_signs_l01','h_signs_l01',len(b_signs)-1,b_signs,len(b_signs)-1,b_signs)
h_signs_l12 = rt.TH2F('h_signs_l12','h_signs_l12',len(b_signs)-1,b_signs,len(b_signs)-1,b_signs)
h_signs_l02 = rt.TH2F('h_signs_l02','h_signs_l02',len(b_signs)-1,b_signs,len(b_signs)-1,b_signs)
h_eos_l01 = rt.TH2F('h_eos_l01','h_eos_l01',len(b_signs)-1,b_signs,len(b_signs)-1,b_signs)
h_eos_l12 = rt.TH2F('h_eos_l12','h_eos_l12',len(b_signs)-1,b_signs,len(b_signs)-1,b_signs)
h_eos_l02 = rt.TH2F('h_eos_l02','h_eos_l02',len(b_signs)-1,b_signs,len(b_signs)-1,b_signs)
h_mos_l01 = rt.TH2F('h_mos_l01','h_mos_l01',len(b_signs)-1,b_signs,len(b_signs)-1,b_signs)
h_mos_l12 = rt.TH2F('h_mos_l12','h_mos_l12',len(b_signs)-1,b_signs,len(b_signs)-1,b_signs)
h_mos_l02 = rt.TH2F('h_mos_l02','h_mos_l02',len(b_signs)-1,b_signs,len(b_signs)-1,b_signs)
h_m1_l01 = rt.TH2F('h_m1_l01','h_m1_l01',len(b_signs)-1,b_signs,len(b_signs)-1,b_signs)
h_m1_l12 = rt.TH2F('h_m1_l12','h_m1_l12',len(b_signs)-1,b_signs,len(b_signs)-1,b_signs)
h_m1_l02 = rt.TH2F('h_m1_l02','h_m1_l02',len(b_signs)-1,b_signs,len(b_signs)-1,b_signs)
h_m2_l01 = rt.TH2F('h_m2_l01','h_m2_l01',len(b_signs)-1,b_signs,len(b_signs)-1,b_signs)
h_m2_l12 = rt.TH2F('h_m2_l12','h_m2_l12',len(b_signs)-1,b_signs,len(b_signs)-1,b_signs)
h_m2_l02 = rt.TH2F('h_m2_l02','h_m2_l02',len(b_signs)-1,b_signs,len(b_signs)-1,b_signs)
h_m3_l01 = rt.TH2F('h_m3_l01','h_m3_l01',len(b_signs)-1,b_signs,len(b_signs)-1,b_signs)
h_m3_l12 = rt.TH2F('h_m3_l12','h_m3_l12',len(b_signs)-1,b_signs,len(b_signs)-1,b_signs)
h_m3_l02 = rt.TH2F('h_m3_l02','h_m3_l02',len(b_signs)-1,b_signs,len(b_signs)-1,b_signs)

tt.Draw('l1_charge : l0_charge >> h_signs_l01')
tt.Draw('l2_charge : l1_charge >> h_signs_l12')
tt.Draw('l2_charge : l0_charge >> h_signs_l02') 
tt.Draw('l1_charge : l0_charge >> h_eos_l01', 'abs(l0_pdgId) == 11')
tt.Draw('l2_charge : l1_charge >> h_eos_l12', 'abs(l0_pdgId) == 11')
tt.Draw('l2_charge : l0_charge >> h_eos_l02', 'abs(l0_pdgId) == 11')
tt.Draw('l1_charge : l0_charge >> h_mos_l01', 'abs(l0_pdgId) == 13')
tt.Draw('l2_charge : l1_charge >> h_mos_l12', 'abs(l0_pdgId) == 13')
tt.Draw('l2_charge : l0_charge >> h_mos_l02', 'abs(l0_pdgId) == 13')
#tt.Draw('l1_charge : l0_charge >> h_m1_l01', 'hnl_hn_m < 3')
#tt.Draw('l2_charge : l1_charge >> h_m1_l12', 'hnl_hn_m < 3')
#tt.Draw('l2_charge : l0_charge >> h_m1_l02', 'hnl_hn_m < 3')
#tt.Draw('l1_charge : l0_charge >> h_m2_l01', 'hnl_hn_m > 3 & hnl_hn_m < 7')
#tt.Draw('l2_charge : l1_charge >> h_m2_l12', 'hnl_hn_m > 3 & hnl_hn_m < 7')
#tt.Draw('l2_charge : l0_charge >> h_m2_l02', 'hnl_hn_m > 3 & hnl_hn_m < 7')
#tt.Draw('l1_charge : l0_charge >> h_m3_l01', 'hnl_hn_m > 7')
#tt.Draw('l2_charge : l1_charge >> h_m3_l12', 'hnl_hn_m > 7')
#tt.Draw('l2_charge : l0_charge >> h_m3_l02', 'hnl_hn_m > 7')
#set_trace()

hstupd8lst = [h_mos_l01,h_mos_l12,h_mos_l02,h_eos_l01,h_eos_l12,h_eos_l02,h_signs_l01,h_signs_l12,h_signs_l02,h_m1_l01,h_m1_l12,h_m1_l02,h_m2_l01,h_m2_l12,h_m2_l02,h_m3_l01,h_m3_l12,h_m3_l02]

for hh in hstupd8lst:
   if 'l01' in hh.GetTitle():
      hh.SetTitle('; l0_sign; l1_sign')
   if 'l12' in hh.GetTitle():
      hh.SetTitle('; l1_sign; l2_sign')
   if 'l02' in hh.GetTitle():
      hh.SetTitle('; l0_sign; l2_sign')
   hh.GetZaxis().SetTitle('Events')
   hh.GetXaxis().SetTitleOffset(1.2)
   hh.GetYaxis().SetTitleOffset(1.4)
   hh.GetZaxis().SetTitleOffset(1.4)
   hh.SetMarkerSize(3)


c_signs_l01.cd()
h_signs_l01.Draw('colztext')
c_signs_l12.cd()
h_signs_l12.Draw('colztext')
c_signs_l02.cd()
h_signs_l02.Draw('colztext')

c_eos_l01.cd()
h_eos_l01.Draw('colztext')
c_eos_l12.cd()
h_eos_l12.Draw('colztext')
c_eos_l02.cd()
h_eos_l02.Draw('colztext')

c_mos_l01.cd()
h_mos_l01.Draw('colztext')
c_mos_l12.cd()
h_mos_l12.Draw('colztext')
c_mos_l02.cd()
h_mos_l02.Draw('colztext')

c_m1_l01.cd()
h_m1_l01.Draw('colztext')
c_m1_l12.cd()
h_m1_l12.Draw('colztext')
c_m1_l02.cd()
h_m1_l02.Draw('colztext')

c_m2_l01.cd()
h_m2_l01.Draw('colztext')
c_m2_l12.cd()
h_m2_l12.Draw('colztext')
c_m2_l02.cd()
h_m2_l02.Draw('colztext')

c_m3_l01.cd()
h_m3_l01.Draw('colztext')
c_m3_l12.cd()
h_m3_l12.Draw('colztext')
c_m3_l02.cd()
h_m3_l02.Draw('colztext')

for cc in [c_signs_l01,c_signs_l12,c_signs_l02,c_eos_l01,c_eos_l12,c_eos_l02,c_mos_l01,c_mos_l12,c_mos_l02,c_m1_l01,c_m1_l12,c_m1_l02,c_m2_l01,c_m2_l12,c_m2_l02,c_m3_l01,c_m3_l12,c_m3_l02,]:
   cc.cd()
   pf.showlogoprelimsim('CMS')
   cc.Modified()
   cc.Update()
   cc.SaveAs(output_dir+cc.GetTitle()+'.root')
   cc.SaveAs(output_dir+cc.GetTitle()+'.pdf')

fout.Write()

