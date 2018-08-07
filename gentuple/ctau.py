import ROOT as rt
import numpy as np
import plotfactory as pf
import ntup_dir as nt
from glob import glob
import sys
from pdb import set_trace
from os.path import normpath, basename
import CMGTools.HNL.samples.signal as signal
####################################################################################################
outdir = '/afs/cern.ch/work/v/vstampf/plots/gentuple/'
indir = '/afs/cern.ch/work/v/vstampf/public/ntuples/gen_v1_refurbshd/' 
####################################################################################################
ntdr = basename(normpath(indir))
####################################################################################################
chain = []

all_files = glob(indir + 'HN3L_*/HNLGenTreeProducer/tree.root')

mass = []

ctau = [] # make list of ctaus with same ordering as all_files

m = 0 
for i in all_files:
    j = i.replace('/HNLGenTreeProducer/tree.root','')
    n = basename(normpath(j))
    f = [s for s in signal.all_signals if s.name == n][0]
    ctau.append(f.ctau)
    chain.append( rt.TChain('tree') )
    chain[m].Add(i)
    mass.append(f.mass)
    print(all_files[m], n, f.ctau, ctau[m])
    m += 1

pf.setpfstyle()

b_m = np.arange(0.,10.,0.1)

lghtspd = 299792458.0

# now write ctau reso; ie. rel diff of gen ctau fitted with expo and ctau provided as sample info

# step 0: getting data
i = 0

# let's have 30 bins from 0 to 3*ctau
#b_dxyz =0 np.linspace(0.,2*ctau[i]/10,30)
#h_temp = rt.TH1F('temp','temp',len(b_dxyz)-1,b_dxyz)
#chain[i].Draw('hnl_3d_disp >> temp')
# 'automatic binning'
c = rt.TCanvas('c','c')
chain[i].Draw('(hnl_2d_disp/hnl_hn_pt)*%d'%(mass[i]))
h = c.GetPrimitive('htemp')

# step 1: fitting
fit = []
func = rt.TF1('func','[0]*exp(-[0]*x)',0,ctau[i])
FIT = h.Fit('func','S')

# step 2: plotting

#pf.showlogopreliminary('CMS','Simulation Preliminary')

#c_acc1.Modified()
#c_acc1.Update()

