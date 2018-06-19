import ROOT as rt
import numpy as np
import plotfactory as pf
import sys
from pdb import set_trace

output_dir = '/afs/cern.ch/work/v/vstampf/plots/candidates/gentuple/' 

######################################### 
# Make Chain from selection of samples
#########################################

fout = rt.TFile(output_dir+'flavcheckM_tr_sl.root', 'recreate')

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

c_flavors = rt.TCanvas('flavors_tr_sl','flavors_tr_sl')
c_eos = rt.TCanvas('flavors_eos_tr_sl','flavors_eos_tr_sl')
c_mos = rt.TCanvas('flavors_mos_tr_sl','flavors_mos_tr_sl')
c_m1 = rt.TCanvas('flavors_m1_tr_sl','flavors_m1_tr_sl')
c_m2 = rt.TCanvas('flavors_m2_tr_sl','flavors_m2_tr_sl')
c_m3 = rt.TCanvas('flavors_m3_tr_sl','flavors_m3_tr_sl')

b_flavor = np.arange(11.,15,1.5)

h_flavors_l1 = rt.TH2F('flavors_l1','flavors_l1',len(b_flavor)-1,b_flavor,len(b_flavor)-1,b_flavor)
h_flavors_l2 = rt.TH2F('flavors_l2','flavors_l2',len(b_flavor)-1,b_flavor,len(b_flavor)-1,b_flavor)
h_eos_l1 = rt.TH2F('eos_l1','eos_l1',len(b_flavor)-1,b_flavor,len(b_flavor)-1,b_flavor)
h_eos_l2 = rt.TH2F('eos_l2','eos_l2',len(b_flavor)-1,b_flavor,len(b_flavor)-1,b_flavor)
h_mos_l1 = rt.TH2F('mos_l1','mos_l1',len(b_flavor)-1,b_flavor,len(b_flavor)-1,b_flavor)
h_mos_l2 = rt.TH2F('mos_l2','mos_l2',len(b_flavor)-1,b_flavor,len(b_flavor)-1,b_flavor)
h_m1_l1 = rt.TH2F('m1_l1','m1_l1',len(b_flavor)-1,b_flavor,len(b_flavor)-1,b_flavor)
h_m1_l2 = rt.TH2F('m1_l2','m1_l2',len(b_flavor)-1,b_flavor,len(b_flavor)-1,b_flavor)
h_m2_l1 = rt.TH2F('m2_l1','m2_l1',len(b_flavor)-1,b_flavor,len(b_flavor)-1,b_flavor)
h_m2_l2 = rt.TH2F('m2_l2','m2_l2',len(b_flavor)-1,b_flavor,len(b_flavor)-1,b_flavor)
h_m3_l1 = rt.TH2F('m3_l1','m3_l1',len(b_flavor)-1,b_flavor,len(b_flavor)-1,b_flavor)
h_m3_l2 = rt.TH2F('m3_l2','m3_l2',len(b_flavor)-1,b_flavor,len(b_flavor)-1,b_flavor)

tt.Draw('abs(l2_pdgId) : abs(l1_pdgId) >> flavors_l1', 'abs(l1_pdgId) == abs(n_pdgId) - 1') # l1 trailing
tt.Draw('abs(l1_pdgId) : abs(l2_pdgId) >> flavors_l2', 'abs(l2_pdgId) == abs(n_pdgId) - 1') # l2 trailing
tt.Draw('abs(l2_pdgId) : abs(l1_pdgId) >> eos_l1', 'abs(l0_pdgId) == 11 & abs(l1_pdgId) == abs(n_pdgId) - 1')
tt.Draw('abs(l1_pdgId) : abs(l2_pdgId) >> eos_l2', 'abs(l0_pdgId) == 11 & abs(l2_pdgId) == abs(n_pdgId) - 1')
tt.Draw('abs(l2_pdgId) : abs(l1_pdgId) >> mos_l1', 'abs(l0_pdgId) == 13 & abs(l1_pdgId) == abs(n_pdgId) - 1')
tt.Draw('abs(l1_pdgId) : abs(l2_pdgId) >> mos_l2', 'abs(l0_pdgId) == 13 & abs(l2_pdgId) == abs(n_pdgId) - 1')
tt.Draw('abs(l2_pdgId) : abs(l1_pdgId) >> m1_l1', 'hnl_hn_m < 3 & abs(l1_pdgId) == abs(n_pdgId) - 1')
tt.Draw('abs(l1_pdgId) : abs(l2_pdgId) >> m1_l2', 'hnl_hn_m < 3 & abs(l2_pdgId) == abs(n_pdgId) - 1')
tt.Draw('abs(l2_pdgId) : abs(l1_pdgId) >> m2_l1', 'hnl_hn_m > 3 & hnl_hn_m < 7 & abs(l1_pdgId) == abs(n_pdgId) - 1')
tt.Draw('abs(l1_pdgId) : abs(l2_pdgId) >> m2_l2', 'hnl_hn_m > 3 & hnl_hn_m < 7 & abs(l2_pdgId) == abs(n_pdgId) - 1')
tt.Draw('abs(l2_pdgId) : abs(l1_pdgId) >> m3_l1', 'hnl_hn_m > 7 & abs(l1_pdgId) == abs(n_pdgId) - 1')
tt.Draw('abs(l1_pdgId) : abs(l2_pdgId) >> m3_l2', 'hnl_hn_m > 7 & abs(l2_pdgId) == abs(n_pdgId) - 1')

fout.Write()

h_flavors_l1.Add(h_flavors_l2)
h_mos_l1.Add(h_mos_l2)
h_eos_l1.Add(h_eos_l2)
h_m1_l1.Add(h_m1_l2)
h_m2_l1.Add(h_m2_l2)
h_m3_l1.Add(h_m3_l2)

hstupd8lst = [h_mos_l1,h_eos_l1,h_flavors_l1,h_m1_l1,h_m2_l1,h_m3_l1]

for hh in hstupd8lst:
   hh.SetTitle(';l_subleading_pdgId ; l_trailing_pdgId')
   hh.GetZaxis().SetTitle('Events')
   hh.GetXaxis().SetTitleOffset(1.2)
   hh.GetYaxis().SetTitleOffset(1.4)
   hh.GetZaxis().SetTitleOffset(1.4)
   hh.SetMarkerSize(3)

c_flavors.cd()
h_flavors_l1.Draw('colztext')

c_eos.cd()
h_eos_l1.Draw('colztext')

c_mos.cd()
h_mos_l1.Draw('colztext')

c_m1.cd()
h_m1_l1.Draw('colztext')

c_m2.cd()
h_m2_l1.Draw('colztext')

c_m3.cd()
h_m3_l1.Draw('colztext')

for cc in [c_flavors,c_eos,c_mos,c_m1,c_m2,c_m3]:
   cc.cd()
   pf.showlogoprelimsim('CMS')
   cc.Modified()
   cc.Update()
   cc.SaveAs(output_dir+cc.GetTitle()+'.root')
   cc.SaveAs(output_dir+cc.GetTitle()+'.pdf')



