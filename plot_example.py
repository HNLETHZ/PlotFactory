import ROOT
import plotfactory as pf
import numpy as np

pf.setpfstyle()
tt = pf.makechain(True)

c = ROOT.TCanvas('c','c')

binsx = np.arange(0.,200.,10.)
binsy = np.arange(0.,600.,30.)

h = ROOT.TH2F('h','',len(binsx)-1,binsx,len(binsy)-1,binsy)
h.SetTitle(';pt [GeV];production radius [cm];entries')
tt.Draw('hnl_2d_disp:l0_pt >> h','abs(l0_eta)<2.4',)
h.Draw('colz')

pf.showlumi('xxx fb^{-1} (xxx TeV)')
pf.showlogopreliminary()

c.Update()
