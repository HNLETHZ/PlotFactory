import ROOT as rt
import plotfactory as pf
import numpy as np

pf.setpfstyle()

tt = pf.makechain(True)

pf.setpfstyle()

c0 = rt.TCanvas('c0','c0')

b_dxy = np.arange(-5.,200,20)

h_gen_2disp = rt.TH1F('gen_2disp','gen_2disp',len(b_dxy)-1,b_dxy)
h_reco_2disp = rt.TH1F('reco_2disp','reco_2disp',len(b_dxy)-1,b_dxy)

tt.Draw('hnl_2d_disp >> gen_2disp','','hist')
tt.Draw('hnl_2d_reco_disp >> reco_2disp' ,'hnl_2d_reco_disp > -90','hist')

h_gen_2disp.SetMarkerColor(rt.kBlue+2)
h_reco_2disp.SetMarkerColor(rt.kGreen+2)

for hh in [h_gen_2disp,h_reco_2disp]:
   hh.SetTitle(';hnl 2d displacement; Events')

c0.cd()
h_gen_2disp.Draw()
h_reco_2disp.Draw('same')
pf.showlogoprelimsim('CMS')
c0.SetLogy()
c0.Modified()
c0.Update()

