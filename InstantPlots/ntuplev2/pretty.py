import ROOT as rt
import numpy as np
#import sys
#sys.path.append('/afs/cern.ch/user/v/vstampf/CMSSW_8_0_30/PlotFactory')
import plotfactory as pf

pf.setpfstyle()

c0 = rt.TCanvas('c0','c0',500,500)

for plt in ['bar','cap']:
   for dd in ['d1','d2','d3','d4']:

      filegl = rt.TFile('%s_%s_gl.root'%(plt,dd))
      filesa = rt.TFile('%s_%s_sa.root'%(plt,dd))

      gmucf = filegl.c10.GetPrimitive('gmucf')
      dgmucf = filegl.c10.GetPrimitive('dgmucf')

      samucf = filesa.c5.GetPrimitive('samucf')
      dsmucf = filesa.c5.GetPrimitive('dsmucf')

      c0.cd()
      gmucf.Draw()
      dgmucf.Draw('same')
      samucf.Draw('same')
      dsmucf.Draw('same')

      histupdatelist = [dsmucf,samucf,gmucf,dgmucf]

      for hh in histupdatelist:
         hh.GetXaxis().SetTitle('p_{T}[GeV]')
         hh.GetYaxis().SetTitle('Chargeflip Ratio')
         hh.GetXaxis().SetTitleOffset(1.2)
         hh.GetYaxis().SetTitleOffset(1.4)

      dgmucf.SetMarkerColor(rt.kGreen+2)
      gmucf.SetMarkerColor(rt.kCyan+2)
      dsmucf.SetMarkerColor(rt.kRed+2)
      samucf.SetMarkerColor(rt.kMagenta+2)

      if (dd == 'd1' or dd == 'd2'):
         leg = rt.TLegend(.18,.70,.4,.86)
      else:
         leg = rt.TLegend(.18,.16,.4,.3)
      leg.SetBorderSize(0)
      leg.SetFillColor(rt.kWhite)
      leg.SetFillStyle(0)
      leg.SetTextFont(42)
      leg.SetTextSize(0.045)
      leg.AddEntry(dsmucf, 'dSA#mu', 'EP')
      leg.AddEntry(samucf, 'SA#mu', 'EP')
      leg.AddEntry(dgmucf, 'dG#mu', 'EP')
      leg.AddEntry(gmucf, 'G#mu', 'EP')
      leg.Draw('apez same')
      pf.showlogoprelimsim('CMS')

      gmucf.SetAxisRange(0.001,1,"Y")

      c0.SetLogy()

      c0.Modified()
      c0.Update()

      c0.SaveAs('%s_%s_total.root'%(plt,dd))
      c0.SaveAs('%s_%s_total.pdf'%(plt,dd))

      filesa.Close()
      filegl.Close()
      c0.Clear()

      print('%s_%s_total.pdf generated'%(plt,dd))
