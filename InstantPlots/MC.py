import ROOT as rt
import plotfactory as pf
import numpy as np

plotDir = '/eos/user/v/vstampf/plots/'

# look at emm events

cut_denom   = 'abs(l0_gen_pdgid) == 11  &  abs(l1_gen_pdgid) == 13  &  abs(l2_gen_pdgid) == 13'
cut_num = cut_denom
cut_num += '  &  l0_eid_mva_iso_wp90  &  l1_id_l  &  l2_id_l  &  l1_q + l2_q == 0  &  hnl_w_vis_m < 80.4' 
cut_num += '  &  hnl_iso04_rel_rhoArea < 0.25  &  hnl_2d_disp > 0.5  &  hnl_2d_disp_sig > 5  &  nbj == 0  &  abs(hnl_dphi_hnvis0) > 2  &  sv_cos > 0.9' 

cut_tot = ''

fin = rt.TFile('/afs/cern.ch/work/v/vstampf/public/ntuples/sig_mc_e/HN3L_M_2_V_0p00707106781187_e_massiveAndCKM_LO/HNLTreeProducer/tree.root')
t=fin.Get('tree')

pf.setpfstyle()

#def checkflavor():

b_pdgid = np.arange(11.,15,1.5)

num = rt.TH2F('num','num',len(b_pdgid)-1,b_pdgid,len(b_pdgid)-1,b_pdgid)
denom = rt.TH2F('denom','denom',len(b_pdgid)-1,b_pdgid,len(b_pdgid)-1,b_pdgid)

tot = rt.TH2F('tot','tot',len(b_pdgid)-1,b_pdgid,len(b_pdgid)-1,b_pdgid)

t.Draw('abs(l2_gen_pdgid):abs(l1_gen_pdgid) >> num', cut_num)
t.Draw('abs(l2_gen_pdgid):abs(l1_gen_pdgid) >> denom', cut_denom)

t.Draw('abs(l2_gen_pdgid):abs(l1_gen_pdgid) >> tot', cut_tot)

print(num.GetEntries())
print(denom.GetEntries())

num.Divide(denom)

c= rt.TCanvas('flavor','flavor')
c.cd()
pf.showlogoprelimsim('CMS')
#num.Draw('colztext')
tot.Draw('colztext')
c.Modified(); c.Update()
c.SaveAs(plotDir+'flavor.root')
c.SaveAs(plotDir+'flavor.pdf')
c.SaveAs(plotDir+'flavor.png')
