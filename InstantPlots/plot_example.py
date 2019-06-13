import ROOT
import plotfactory as pf
import numpy as np
import sys

pf.setpfstyle()

######################################### 
# Make Chain from selection of samples
#########################################
# Get the option from the command line, using 'True' as a fallback.
if len(sys.argv)>1 and sys.argv[1] == 'test':
    setting = False
    print('Using a selection of samples')
else:
    setting = True
    print('Using all samples')

tt = pf.makechain(setting)

nentries = tt.GetEntries()
print('number of events: %d'%(nentries))

######################################### 
# Make Plot
#########################################


c = ROOT.TCanvas('c','c')

binsx = np.arange(0.,200.,10.)
binsy = np.arange(0.,600.,30.)

h = ROOT.TH2F('h','',len(binsx)-1,binsx,len(binsy)-1,binsy)
h.SetTitle(';pt [GeV];production radius [cm];entries')
tt.Draw('hnl_2d_disp:l0_pt >> h','abs(l0_eta)<2.4',)
h.Draw('colz')

pf.showlumi('xxx fb^{-1} (xxx TeV)')
pf.showlogopreliminary('CMS','Preliminary')

c.Update()
