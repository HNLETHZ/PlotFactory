import ROOT as rt
import numpy as np
import plotfactory as pf
import sys
import ntup_dir as nt
from pdb import set_trace
from os.path import normpath, basename

output_dir = '/afs/cern.ch/work/v/vstampf/plots/recontuple/' 

ntdr = basename(normpath(nt.getntupdir()))

fout = rt.TFile(output_dir+'dimunum_2disp_'+ntdr+'.root', 'recreate')

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

c_dimunum_2disp = rt.TCanvas('dimunum_2disp','dimunum_2disp')

b_dimunum = np.arange(0.,15,1.)
b_2disp   = np.logspace(-1,2.78,15)

h_dimunum_2disp = rt.TH2F('dimunum_2disp','dimunum_2disp',len(b_2disp)-1,b_2disp,len(b_dimunum)-1,b_dimunum)

tt.Draw('n_dimuon : hnl_2d_disp >> dimunum_2disp', 'abs(l2_pdgId) == 13 & abs(l1_pdgId) == 13 & is_in_acc == 1')

fout.Write()

hstupd8lst = [h_dimunum_2disp] 

for hh in hstupd8lst:
   hh.SetTitle('; HNL 2D displacement; #dimuons')
   hh.GetZaxis().SetTitle('Events  #(\mu\mu \land |\eta|<2.4)')
   hh.GetXaxis().SetTitleOffset(1.4)
   hh.GetYaxis().SetTitleOffset(1)
   hh.GetZaxis().SetTitleOffset(1.2)

c_dimunum_2disp.cd()
h_dimunum_2disp.Draw('colztext')

for cc in [c_dimunum_2disp]:
   cc.cd()
   pf.showlogoprelimsim('CMS')
   cc.SetLogx()
   cc.SetLogz()
   cc.Modified()
   cc.Update()
   cc.SaveAs(output_dir+cc.GetTitle()+'_'+ntdr+'.root')
   cc.SaveAs(output_dir+cc.GetTitle()+'_'+ntdr+'.pdf')



