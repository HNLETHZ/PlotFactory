################# 
# configuration #
#################
from pdb import set_trace
import ROOT
import numpy as np
import sys
sys.path.append('/afs/cern.ch/user/v/vstampf/CMSSW_8_0_30/PlotFactory')
import plotfactory as pf
#from pdb import set_trace
from glob import glob
#ROOT.gROOT.SetBatch(True)    # don't open X11 forwarding (running screen)
################################## 
pf.setpfstyle()
bewl = input("Makechain: True or False\n")
tt = pf.makechain(bewl)
output_dir = '/afs/cern.ch/user/v/vstampf/CMSSW_8_0_30/PlotFactory/plots/ntuplev2/dr/2d/'
################################## 
ntries = tt.GetEntries()
print('Number of entries: ' + str(ntries))
################# 
# define x-axes #
#################
pTbins = np.arange(5.,73,5)
drbins = np.arange(0.,4,0.25)

c1 = ROOT.TCanvas('c1','c1 gen l1',600,500)
c2 = ROOT.TCanvas('c2','c2 gen l2',600,500)

genl1 = ROOT.TH2F('genl1','genl1',len(pTbins)-1,pTbins,len(drbins)-1,drbins)
genl2 = ROOT.TH2F('genl2','genl2',len(pTbins)-1,pTbins,len(drbins)-1,drbins)

tt.Draw("hnl_dr_12:l1_pt >> genl1", "abs(l1_pdgId) == 13 & l1_pt > 5 & abs(l1_eta) < 2.4")
tt.Draw("hnl_dr_12:l2_pt >> genl2", "abs(l2_pdgId) == 13 & l2_pt > 5 & abs(l2_eta) < 2.4")

histupdatelist = [genl1,genl2]

for hh in histupdatelist:
   hh.GetXaxis().SetTitle('p_{T} [GeV]')
   hh.GetYaxis().SetTitle('#Deltar')
   hh.GetZaxis().SetTitle('Events')
   hh.GetXaxis().SetTitleOffset(1.2)
   hh.GetYaxis().SetTitleOffset(1.4)
   hh.GetZaxis().SetTitleOffset(1.4)
   hh.SetAxisRange(1,10000000,"Z")

c1.cd()
genl1.Draw('colz')
c2.cd()
genl2.Draw('colz')

for cc in [c1,c2]:
    cc.cd()
    cc.SetLogz()
    pf.showlogoprelimsim('CMS')
    ROOT.gStyle.SetOptStat(0)
    cc.Modified()
    cc.Update()

c1.SaveAs(output_dir + 'genl1.root')
c1.SaveAs(output_dir + 'genl1.pdf')
c2.SaveAs(output_dir + 'genl2.root')
c2.SaveAs(output_dir + 'genl2.pdf')
