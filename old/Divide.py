import ROOT
import numpy as np
import plotfactory as pf
from glob import glob

#pf.setpfstyle()

pTbins = np.arange(0.,6,1)

print('Preparing canvas')
t = ROOT.TCanvas('t','t')
#u = ROOT.TCanvas('u','u')
c1 = ROOT.TCanvas('c1','c1')
c2 = ROOT.TCanvas('c2','c2')


a = ROOT.TH1F('a','a',len(pTbins)-1,pTbins)
b = ROOT.TH1F('b','b',len(pTbins)-1,pTbins)
c = ROOT.TH1F('c','c',len(pTbins)-1,pTbins)

for i in range(10000):
    a.Fill(3) 
    b.Fill(2)

#t.cd()
#c.Draw()

c1.cd()
a.Draw()

c2.cd()
b.Draw()

t.cd()
a.Add(b)
a.Draw()

#u.cd()
#print(a.Divide(b))
#a.Draw('same')

#for tt in [t,c1,c2]:
#    tt.Update()
