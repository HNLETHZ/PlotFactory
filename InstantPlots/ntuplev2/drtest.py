import ROOT as rt
import numpy as np
import sys
sys.path.append('/afs/cern.ch/user/v/vstampf/CMSSW_8_0_30/PlotFactory')
import plotfactory as pf

tt = pf.makechain(False)
ntries = tt.GetEntries()
print('Number of entries: ' + str(ntries))

pTbins = np.arange(5.,73.,5)
drbins = np.arange(0.,4.,0.25)

c = rt.TCanvas('c','c',500,500)

h = rt.TH2F('h','',len(pTbins)-1,pTbins,len(drbins)-1,drbins)

tt.Draw("hnl_dr_12:l1_pt >> h", "abs(l1_pdgId) == 13 & l1_pt > 5")

h.Draw('colz')

print('success')
