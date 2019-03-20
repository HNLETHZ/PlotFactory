import ROOT
from itertools import product

'''
WATCH OUT THAT CODE HAS TO BE C++ COMPATIBLE

Linux-2.6.32-754.3.5.el6.x86_64-x86_64-with-redhat-6.6-Carbon         #T3
Linux-3.10.0-957.1.3.el7.x86_64-x86_64-with-centos-7.6.1810-Core      #LX+
'''
eos       = '/eos/user/v/vstampf/'
eos_david = '/eos/user/d/dezhu/HNL/'
if platform.platform() == 'Linux-2.6.32-754.3.5.el6.x86_64-x86_64-with-redhat-6.6-Carbon':
   eos       = '/t3home/vstampf/eos/'
   eos_david = '/t3home/vstampf/eos-david/'

plotDir = eos+'/plots/DDE/'

# f1 = ROOT.TFile.Open('electron_single_fr.root.bkp', 'read')
f1 = ROOT.TFile.Open('electron_single_fr.root', 'read')
f1.cd()

eta_bins = [
    '1p5to2p5' ,
    '0p8to1p5' ,
    '0to0p8'   ,
    'inclusive',
]

e_ids_bins = [
    'NoID'         ,
    'LooseNoIso'   ,
    'MediumNoIso'  ,
    'MediumWithIso',
]

c1 = ROOT.TCanvas('c1', '', 700, 700)


outfile = ROOT.TFile.Open('electron_single_fr_ratios.root', 'recreate')

for ieta, iid in product(eta_bins, e_ids_bins):
    f1.cd()
   
    num = f1.Get('%s/%s/l1_reliso_rho_04#cb'    %(ieta, iid))
    den = f1.Get('%s/%s/l1_reliso_rho_04#udsgx' %(ieta, iid))

    num.Scale(1./num.Integral())
    den.Scale(1./den.Integral())

    numcum = num.GetCumulative()
    dencum = den.GetCumulative()

    ratio = numcum.Clone()
    
    ratio.Divide(dencum)
    
    ratio.SetLineColor(ROOT.kGreen+2)
    
    ratio.GetYaxis().SetTitle('heavy/light')
        
    ratio.SetTitle('%s %s' %(ieta, iid))
    ratio.SetName('%s_%s' %(ieta, iid))
    
    ratio.SetLineWidth(2)
    
    ROOT.gPad.SetGridx(True)
    ROOT.gPad.SetGridy(True)

    ratio.GetXaxis().SetRangeUser(5.e-2, 10.)
    ratio.GetYaxis().SetRangeUser(0.   ,  1.)
    
    ROOT.gPad.SetLogx(True)

    ratio.Draw('hist')
    
    c1.SaveAs(plotDir + 'electron_single_fr_ratios/ratio_%s_%s.pdf'%(ieta, iid))

    outfile.cd()
    ratio.Write()

]
]
