import os
from glob import glob
import ROOT
import numpy as np
import pandas, root_numpy
import root_pandas
from itertools import product

## get FR(eta, pt)
ff = ROOT.TFile('/eos/user/v/vstampf/plots/DDE/TTL_partial_ptCone_eta_iso15_eta.root')
cc = ff.Get('ptCone_eta')
hh = cc.GetPrimitive('pt_cone_eta_n')

# convert into a numpy array
frs = root_numpy.hist2array(hh)
xbins = np.array([hh.GetXaxis().GetBinUpEdge(i) for i in range(hh.GetNbinsX()+1)])
ybins = np.array([hh.GetYaxis().GetBinUpEdge(i) for i in range(hh.GetNbinsY()+1)])

@np.vectorize
def fakeRate(pt, eta): #, frs, xbins, ybins):
    ipt  = min(max(np.where(pt >=xbins)[0]), len(xbins)-2) # if overflow, just stick to the last bin
    ieta = min(max(np.where(eta>=ybins)[0]), len(ybins)-2)
    return frs[ipt][ieta]

# some validation
# ipts  = np.linspace(0., 100., 20)
# ietas = np.linspace(0., 3.  , 6 )
# 
# for ipt, ieta in product(ipts, ietas):
#     print 'pt = %.1f \teta = %.1f \t\t fake rate = %.5f' %(ipt, ieta, fakeRate(ipt, ieta))
# https://github.com/vinzenzstampf/PlotFactory/blob/master/DDE/countingFakes.py#L646-L677

ifile = '/eos/user/v/vstampf/ntuples/DDE_v2/prompt_m/TTJets/HNLTreeProducer/tree.root'

myfile = ROOT.TFile.Open(ifile, 'read')
myfile.cd()
mytree = myfile.Get('tree')
nevents = mytree.GetEntries()
isocut = 0.15
apop = 100000

# proceed 200k events a pop
nslices = nevents/apop + 1
for islice in range(nslices)[:3]:
    
    start =  islice      * apop
    stop  = (islice + 1) * apop
    
    print 'loading dataset...'
    dataset = pandas.DataFrame(root_numpy.root2array(ifile, 'tree', start=start, stop=stop))
    dataset['aux_index'] = np.arange(start,stop)
    print '\t...done'

    dataset_iso    = dataset.iloc[np.where(dataset.hnl_iso04_rel_rhoArea< isocut)[0], :]
    dataset_noniso = dataset.iloc[np.where(dataset.hnl_iso04_rel_rhoArea>=isocut)[0], :]

    dataset_iso   ['weight_fr'] = fakeRate(dataset_iso   .hnl_hn_vis_pt                                                       , np.abs(dataset_iso   .hnl_hn_vis_eta))
    dataset_noniso['weight_fr'] = fakeRate(dataset_noniso.hnl_hn_vis_pt * (1. + dataset_noniso.hnl_iso04_rel_rhoArea - isocut), np.abs(dataset_noniso.hnl_hn_vis_eta))

    frames = [dataset_iso, dataset_noniso]

    out_dataset = pandas.concat(frames)
    out_dataset.sort_values(['aux_index'], inplace=True)

    print 'staging out...'
    out_dataset.to_root('test_tree_slice%d.root' %islice, key='tree')
    print '\t...done'

# tree->Scan("hnl_iso04_rel_rhoArea:weight_fr:(hnl_hn_vis_pt*(hnl_iso04_rel_rhoArea<0.15)) + ((hnl_iso04_rel_rhoArea>=0.15)*(hnl_hn_vis_pt*(1. + hnl_iso04_rel_rhoArea - 0.15))):abs(hnl_hn_vis_eta):__index__:aux_index","", "colsize=15")

tomerge = glob('test_tree_slice*.root')

command = 'hadd tree_fr.root'
for imerge in tomerge:
    command += ' ' + imerge

os.system(command)

