import ROOT as rt
import numpy as np
import plotfactory as pf
import ntup_dir as nt
from glob import glob
import sys
from pdb import set_trace
from os.path import normpath, basename
####################################################################################################
outdir = '/afs/cern.ch/work/v/vstampf/plots/recontuple/'
indir = nt.getntupdir()
####################################################################################################
ntdr = basename(normpath(indir))
####################################################################################################
t = pf.makechain(True)
####################################################################################################
####################################################################################################
pf.setpfstyle()
####################################################################################################
####################################################################################################
####################################################################################################
b_m = np.arange(0.,11,0.1)
####################################################################################################
####################################################################################################
####################################################################################################
h_m_maxcos_eff_d = rt.TH1F('m_maxcos_eff_d','m_maxcos_eff_d',len(b_m)-1,b_m)
h_m_maxcos_eff_n = rt.TH1F('m_maxcos_eff_n','m_maxcos_eff_n',len(b_m)-1,b_m)
####################################################################################################
h_m_maxcos_pur_d = rt.TH1F('m_maxcos_pur_d','m_maxcos_pur_d',len(b_m)-1,b_m)
h_m_maxcos_pur_n = rt.TH1F('m_maxcos_pur_n','m_maxcos_pur_n',len(b_m)-1,b_m)
####################################################################################################
####################################################################################################
h_m_maxdxy_eff_d = rt.TH1F('m_maxdxy_eff_d','m_maxdxy_eff_d',len(b_m)-1,b_m)
h_m_maxdxy_eff_n = rt.TH1F('m_maxdxy_eff_n','m_maxdxy_eff_n',len(b_m)-1,b_m)
####################################################################################################
h_m_maxdxy_pur_d = rt.TH1F('m_maxdxy_pur_d','m_maxdxy_pur_d',len(b_m)-1,b_m)
h_m_maxdxy_pur_n = rt.TH1F('m_maxdxy_pur_n','m_maxdxy_pur_n',len(b_m)-1,b_m)
####################################################################################################
####################################################################################################
h_m_mindr_eff_d = rt.TH1F('m_mindr_eff_d','m_mindr_eff_d',len(b_m)-1,b_m)
h_m_mindr_eff_n = rt.TH1F('m_mindr_eff_n','m_mindr_eff_n',len(b_m)-1,b_m)
####################################################################################################
h_m_mindr_pur_d = rt.TH1F('m_mindr_pur_d','m_mindr_pur_d',len(b_m)-1,b_m)
h_m_mindr_pur_n = rt.TH1F('m_mindr_pur_n','m_mindr_pur_n',len(b_m)-1,b_m)
####################################################################################################
####################################################################################################
h_m_maxpt_eff_d = rt.TH1F('m_maxpt_eff_d','m_maxpt_eff_d',len(b_m)-1,b_m)
h_m_maxpt_eff_n = rt.TH1F('m_maxpt_eff_n','m_maxpt_eff_n',len(b_m)-1,b_m)
####################################################################################################
h_m_maxpt_pur_d = rt.TH1F('m_maxpt_pur_d','m_maxpt_pur_d',len(b_m)-1,b_m)
h_m_maxpt_pur_n = rt.TH1F('m_maxpt_pur_n','m_maxpt_pur_n',len(b_m)-1,b_m)
####################################################################################################
####################################################################################################
h_m_minchi2_eff_d = rt.TH1F('m_minchi2_eff_d','m_minchi2_eff_d',len(b_m)-1,b_m)
h_m_minchi2_eff_n = rt.TH1F('m_minchi2_eff_n','m_minchi2_eff_n',len(b_m)-1,b_m)
####################################################################################################
h_m_minchi2_pur_d = rt.TH1F('m_minchi2_pur_d','m_minchi2_pur_d',len(b_m)-1,b_m)
h_m_minchi2_pur_n = rt.TH1F('m_minchi2_pur_n','m_minchi2_pur_n',len(b_m)-1,b_m)
####################################################################################################
####################################################################################################
####################################################################################################
t.Draw('hnl_hn_MASS >> m_maxcos_eff_n','flag_IsThereTHEDimuon == 1 & flag_matchedHNLMaxCosBPA == 1')
t.Draw('hnl_hn_MASS >> m_maxcos_eff_d','flag_IsThereTHEDimuon == 1')
####################################################################################################
t.Draw('hnl_hn_MASS >> m_maxcos_pur_n','flag_matchedHNLMaxCosBPA == 1')
t.Draw('hnl_hn_MASS >> m_maxcos_pur_d','flag_matchedHNLMaxCosBPA == 1 | flag_matchedHNLMaxCosBPA == 0')
####################################################################################################
####################################################################################################
t.Draw('hnl_hn_MASS >> m_maxdxy_eff_n','flag_IsThereTHEDimuon == 1 & flag_matchedHNLDxy == 1')
t.Draw('hnl_hn_MASS >> m_maxdxy_eff_d','flag_IsThereTHEDimuon == 1')
####################################################################################################
t.Draw('hnl_hn_MASS >> m_maxdxy_pur_n','flag_matchedHNLDxy == 1')
t.Draw('hnl_hn_MASS >> m_maxdxy_pur_d','flag_matchedHNLDxy == 1 | flag_matchedHNLDxy == 0')
####################################################################################################
####################################################################################################
t.Draw('hnl_hn_MASS >> m_mindr_eff_n','flag_IsThereTHEDimuon == 1 & flag_matchedHNLMinDr12 == 1')
t.Draw('hnl_hn_MASS >> m_mindr_eff_d','flag_IsThereTHEDimuon == 1')
####################################################################################################
t.Draw('hnl_hn_MASS >> m_mindr_pur_n','flag_matchedHNLMinDr12 == 1')
t.Draw('hnl_hn_MASS >> m_mindr_pur_d','flag_matchedHNLMinDr12 == 1 | flag_matchedHNLMinDr12 == 0')
####################################################################################################
####################################################################################################
t.Draw('hnl_hn_MASS >> m_maxpt_eff_n','flag_IsThereTHEDimuon == 1 & flag_matchedHNLMaxPt == 1')
t.Draw('hnl_hn_MASS >> m_maxpt_eff_d','flag_IsThereTHEDimuon == 1')
####################################################################################################
t.Draw('hnl_hn_MASS >> m_maxpt_pur_n','flag_matchedHNLMaxPt == 1')
t.Draw('hnl_hn_MASS >> m_maxpt_pur_d','flag_matchedHNLMaxPt == 1 | flag_matchedHNLMaxPt == 0')
####################################################################################################
####################################################################################################
t.Draw('hnl_hn_MASS >> m_minchi2_eff_n','flag_IsThereTHEDimuon == 1 & flag_matchedHNLChi2 == 1')
t.Draw('hnl_hn_MASS >> m_minchi2_eff_d','flag_IsThereTHEDimuon == 1')
####################################################################################################
t.Draw('hnl_hn_MASS >> m_minchi2_pur_n','flag_matchedHNLChi2 == 1')
t.Draw('hnl_hn_MASS >> m_minchi2_pur_d','flag_matchedHNLChi2 == 1 | flag_matchedHNLChi2 == 0')
####################################################################################################
####################################################################################################
####################################################################################################
h_m_maxcos_pur_n.Divide(h_m_maxcos_pur_d)
h_m_maxcos_eff_n.Divide(h_m_maxcos_eff_d)
h_m_maxcos_pur_n.SetMarkerColor(rt.kBlue+2)
h_m_maxcos_eff_n.SetMarkerColor(rt.kBlue+2)
h_m_maxcos_eff_n.SetTitle('MaxCosBPA')
h_m_maxcos_pur_n.SetTitle('MaxCosBPA')
####################################################################################################
h_m_maxdxy_pur_n.Divide(h_m_maxdxy_pur_d)
h_m_maxdxy_eff_n.Divide(h_m_maxdxy_eff_d)
h_m_maxdxy_pur_n.SetMarkerColor(rt.kYellow+2)
h_m_maxdxy_eff_n.SetMarkerColor(rt.kYellow+2)
h_m_maxdxy_pur_n.SetTitle('Max D_{xy}') 
h_m_maxdxy_eff_n.SetTitle('Max D_{xy}')
####################################################################################################
h_m_mindr_pur_n.Divide(h_m_mindr_pur_d)
h_m_mindr_eff_n.Divide(h_m_mindr_eff_d)
h_m_mindr_pur_n.SetMarkerColor(rt.kCyan+2)
h_m_mindr_eff_n.SetMarkerColor(rt.kCyan+2)
h_m_mindr_pur_n.SetTitle('Min #Deltar(l_{1},l_{2})') 
h_m_mindr_eff_n.SetTitle('Min #Deltar(l_{1},l_{2})')
####################################################################################################
h_m_maxpt_pur_n.Divide(h_m_maxpt_pur_d)
h_m_maxpt_eff_n.Divide(h_m_maxpt_eff_d)
h_m_maxpt_pur_n.SetMarkerColor(rt.kGreen+2)
h_m_maxpt_eff_n.SetMarkerColor(rt.kGreen+2)
h_m_maxpt_pur_n.SetTitle('Max p_{T}')
h_m_maxpt_eff_n.SetTitle('Max p_{T}')
####################################################################################################
h_m_minchi2_pur_n.Divide(h_m_minchi2_pur_d)
h_m_minchi2_eff_n.Divide(h_m_minchi2_eff_d)
h_m_minchi2_pur_n.SetMarkerColor(rt.kRed+2)
h_m_minchi2_eff_n.SetMarkerColor(rt.kRed+2)
h_m_minchi2_pur_n.SetTitle('Min #chi^{2}')
h_m_minchi2_eff_n.SetTitle('Min #chi^{2}')
####################################################################################################
####################################################################################################
lst_pur = [h_m_maxpt_pur_n,h_m_maxdxy_pur_n,h_m_maxcos_pur_n,h_m_mindr_pur_n,h_m_minchi2_pur_n]
lst_eff = [h_m_maxpt_eff_n,h_m_maxdxy_eff_n,h_m_maxcos_eff_n,h_m_mindr_eff_n,h_m_minchi2_eff_n]
####################################################################################################
####################################################################################################
for h in lst_pur+lst_eff:
    h.GetXaxis().SetTitle('HNL Mass [GeV]')
    h.SetMarkerSize(0.3)
for h in lst_eff:
    h.SetAxisRange(0.92,1.005,'Y')
    h.GetYaxis().SetTitle('Efficiency')
for h in lst_pur:
    h.GetYaxis().SetTitle('Purity')
    h.SetAxisRange(0.3,0.905,'Y')
####################################################################################################
####################################################################################################
####################################################################################################
c_m_eff = rt.TCanvas('m_eff','m_eff')
c_m_pur = rt.TCanvas('m_pur','m_pur')
####################################################################################################
####################################################################################################
clist = [c_m_pur,c_m_eff]
####################################################################################################
####################################################################################################
c_m_eff.cd()
for h in lst_eff: h.Draw('epsame')
c_m_eff.BuildLegend()
####################################################################################################
####################################################################################################
c_m_pur.cd()
for h in lst_pur: h.Draw('epsame')
c_m_pur.BuildLegend()
####################################################################################################
####################################################################################################
for c in clist:
    c.cd()
    pf.showlogoprelimsim('CMS')
#    rt.gStyle.SetOptStat()
    c.Modified()
    c.Update()
    c.SaveAs(outdir+c.GetTitle()+'_'+ntdr+'.root')
    c.SaveAs(outdir+c.GetTitle()+'_'+ntdr+'.png')
