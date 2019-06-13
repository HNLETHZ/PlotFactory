import ROOT
import numpy as np
import plotfactory as pf
from glob import glob

pf.setpfstyle()
work_dir = '/afs/cern.ch/user/v/vstampf/CMSSW_8_0_30/PlotFactory/plots/4_reg/'

file = ROOT.TFile('plots/4_reg/hist_notfull.root')

pTbins = np.arange(3.,75, 5)

smucfbar = file.Get('dsmul1barcf')
smunfbar = file.Get('dsmul1barnf')

t = ROOT.TCanvas('t','t')

smubar  = ROOT.TH1F('alld','alld',len(pTbins)-1,pTbins)

#print(sum.GetName())

t.cd()
#cf.Draw()
smubar.Add(smucfbar)
smubar.Add(smunfbar)
buf = ROOT.TH1F('alld','alld',len(pTbins)-1,pTbins)
buf.Divide(smucfbar,smubar)

buf.Draw()

#pf.showlumi(' l1+l2 / eta<0.8 / alld')# / %.2f M entries'%(ntries / 1000000.))
buf.SetMarkerColor(4)
#dbuf.SetMarkerColor(2)
buf.GetXaxis().SetTitle('p_{T}[GeV]')
buf.GetYaxis().SetTitle('Entries (normalized)')
buf.GetXaxis().SetTitleOffset(1.2)
buf.GetYaxis().SetTitleOffset(1.4)
pf.showlogoprelimsim('CMS')

leg = ROOT.TLegend(.18,.76,.4,.9)
leg.SetBorderSize(0)
leg.SetFillColor(ROOT.kWhite)
leg.SetFillStyle(0)
leg.SetTextFont(42)
leg.SetTextSize(0.03)
#leg.AddEntry(dbuf, 'dSA#mu', 'EP')
leg.AddEntry(buf , 'S#mu', 'EP')
leg.Draw('apez same')
t.Update()
