import ROOT
from itertools import product

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
    
    c1.SaveAs('electron_single_fr_ratios/ratio_%s_%s.pdf'%(ieta, iid))

    outfile.cd()
    ratio.Write()

]
]
