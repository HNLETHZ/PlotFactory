import ROOT as rt
import numpy as np
import plotfactory as pf
import sys
from pdb import set_trace
from os.path import normpath, basename

indir = '/afs/cern.ch/work/v/vstampf/public/ntuples/dr_study/'
ver = 'HN3L_M_2p5_V_0p0173205080757_e_onshell_1/'
outdir = '/afs/cern.ch/work/v/vstampf/plots/recontuple/'

ntdr = basename(normpath(ver))

fin = rt.TFile(indir+ver+'HNLTreeProducer/tree.root')

t = fin.Get('tree')

pf.setpfstyle()

b_dr = np.arange(0.,0.18,0.005)
b_pt = np.arange(0.,50,3)

h_recos = rt.TH1F('recos','recos',len(b_dr)-1,b_dr)
h_recos_l1 = rt.TH1F('recos_l1','recos_l1',len(b_dr)-1,b_dr)
h_recos_l2 = rt.TH1F('recos_l2','recos_l2',len(b_dr)-1,b_dr)

h_recos_bar = rt.TH1F('recos_bar','recos_bar',len(b_dr)-1,b_dr)
h_recos_l1_bar = rt.TH1F('recos_l1_bar','recos_l1_bar',len(b_dr)-1,b_dr)
h_recos_l2_bar = rt.TH1F('recos_l2_bar','recos_l2_bar',len(b_dr)-1,b_dr)

h_recos_cap = rt.TH1F('recos_cap','recos_cap',len(b_dr)-1,b_dr)
h_recos_l1_cap = rt.TH1F('recos_l1_cap','recos_l1_cap',len(b_dr)-1,b_dr)
h_recos_l2_cap = rt.TH1F('recos_l2_cap','recos_l2_cap',len(b_dr)-1,b_dr)

t.Draw('dr_recos_l1 >> recos_l1', 'is_in_acc > 0 & dr_recos_l1 > -1 & abs(l1_pdgId) == 13')
t.Draw('dr_recos_l2 >> recos_l2', 'is_in_acc > 0 & dr_recos_l2 > -1 & abs(l2_pdgId) == 13')

t.Draw('dr_recos_l1 >> recos_l1_bar', 'is_in_acc > 0 & dr_recos_l1 > -1 & abs(l1_pdgId) == 13 & abs(l1_eta) < 0.8')
t.Draw('dr_recos_l2 >> recos_l2_bar', 'is_in_acc > 0 & dr_recos_l2 > -1 & abs(l2_pdgId) == 13 & abs(l2_eta) < 0.8')

t.Draw('dr_recos_l1 >> recos_l1_cap', 'is_in_acc > 0 & dr_recos_l1 > -1 & abs(l1_pdgId) == 13 & abs(l1_eta) > 1.2')
t.Draw('dr_recos_l2 >> recos_l2_cap', 'is_in_acc > 0 & dr_recos_l2 > -1 & abs(l2_pdgId) == 13 & abs(l2_eta) > 1.2')

h_recos.Add(h_recos_l1)
h_recos.Add(h_recos_l2)

h_recos_bar.Add(h_recos_l1_bar)
h_recos_bar.Add(h_recos_l2_bar)

h_recos_cap.Add(h_recos_l1_cap)
h_recos_cap.Add(h_recos_l2_cap)

c_recos = rt.TCanvas('dr_recos','dr_recos')
c_recos_bar = rt.TCanvas('dr_recos_bar','dr_recos_bar')
c_recos_cap = rt.TCanvas('dr_recos_cap','dr_recos_cap')

c_recos.cd()
h_recos.Draw()
pf.showlogoprelimsim('CMS')
c_recos.Modified()
c_recos.Update()
c_recos.SaveAs(outdir+c_recos.GetTitle()+'_'+ntdr+'.root')
c_recos.SaveAs(outdir+c_recos.GetTitle()+'_'+ntdr+'.png')

c_recos_bar.cd()
h_recos_bar.Draw()
pf.showlogoprelimsim('CMS')
c_recos_bar.Modified()
c_recos_bar.Update()
c_recos_bar.SaveAs(outdir+c_recos_bar.GetTitle()+'_'+ntdr+'.root')
c_recos_bar.SaveAs(outdir+c_recos_bar.GetTitle()+'_'+ntdr+'.png')

c_recos_cap.cd()
h_recos_cap.Draw()
pf.showlogoprelimsim('CMS')
c_recos_cap.Modified()
c_recos_cap.Update()
c_recos_cap.SaveAs(outdir+c_recos_cap.GetTitle()+'_'+ntdr+'.root')
c_recos_cap.SaveAs(outdir+c_recos_cap.GetTitle()+'_'+ntdr+'.png')
