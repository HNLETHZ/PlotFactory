import ROOT as rt
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
# Make Canvas and Histograms
#########################################
c_acc1 = rt.TCanvas('c_acc1','c_acc2')

binsx = np.arange(0.,100.,2.)

h_denom = rt.TH1F('h_denom','',len(binsx)-1,binsx)
h_allmass = rt.TH1F('h_allmass','',len(binsx)-1,binsx)
h_allmass.SetTitle(';promt electron pt cut [GeV]; acceptance')
h_allmass.GetYaxis().SetRangeUser(0.,1.04)

sel0 = 'abs(l0_pdgId)==13 & is_in_acc==1'
n_sel0 = tt.GetEntries(sel0)

tt.Draw('l0_pt>>h_denom',sel0)

for ibin in range(len(binsx)):
    ipt = binsx[ibin]
    # iacc = float(h_denom.Integral(ibin,len(binsx)))/float(h_denom.Integral()) 
    int_tot = float(h_denom.Integral())
    int_sub = float(h_denom.Integral(ibin,len(binsx)))
    iacc = int_sub/int_tot
    # print('%d    %d    %d    %d    %.2f'%(ibin,ipt,int_tot,int_sub,iacc))
    h_allmass.SetBinContent(ibin,iacc)

h_allmass.Draw()

c_acc1.Update()
