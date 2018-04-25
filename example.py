import ROOT
import plotfactory as pf

pfstyle = pf.makestyle()
ROOT.gROOT.SetStyle('pfstyle')

tt = pf.makechain(False)
tt.Draw('l0_pt')
