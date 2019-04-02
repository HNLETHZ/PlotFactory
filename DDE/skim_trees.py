import ROOT
import root_pandas
#from root_pandas import to_root
import numpy as np
import pandas as pd
import root_numpy

outDir = '/eos/user/v/vstampf/ntuples/'

def makeFiles(self, ch='mmm'):
    if ch == 'mem':
        files = [(0, '/work/dezhu/4_production/production_20190306_BkgMC/mem/ntuples/DYBB/HNLTreeProducer/tree.root'              ),
                 (1, '/work/dezhu/4_production/production_20190306_BkgMC/mem/ntuples/DYJetsToLL_M50/HNLTreeProducer/tree.root'    ),
                 (1, '/work/dezhu/4_production/production_20190306_BkgMC/mem/ntuples/DYJetsToLL_M50_ext/HNLTreeProducer/tree.root'),
                 (2, '/work/dezhu/4_production/production_20190306_BkgMC/mem/ntuples/TTJets/HNLTreeProducer/tree.root'            ),
                ]

    if ch == 'mmm':
        files = [(0, '/eos/user/d/dezhu/HNL/ntuples/HN3Lv2.0/background/montecarlo/production20190318/mmm/ntuples/DYBB/HNLTreeProducer/tree.root'              ),
                 (1, '/eos/user/d/dezhu/HNL/ntuples/HN3Lv2.0/background/montecarlo/production20190318/mmm/ntuples/DYJetsToLL_M50/HNLTreeProducer/tree.root'    ),
                 (1, '/eos/user/d/dezhu/HNL/ntuples/HN3Lv2.0/background/montecarlo/production20190318/mmm/ntuples/DYJetsToLL_M50_ext/HNLTreeProducer/tree.root'),
                 (2, '/eos/user/d/dezhu/HNL/ntuples/HN3Lv2.0/background/montecarlo/production20190318/mmm/ntuples/TTJets/HNLTreeProducer/tree.root'            ),
                ]

    return files

def baseCuts(ch='mmm'):
    if ch == 'mem':
        cuts = ' && '.join(['l0_pt > 25 && abs(l0_eta) < 2.4 && l0_id_m == 1 && abs(l0_dz) < 0.2 && abs(l0_dxy) < 0.05 && l0_reliso_rho_03 < 0.2', # l0 genuine
                            'l2_pt > 10 && abs(l2_eta) < 2.4 && l2_id_m == 1 && abs(l2_dz) < 0.2 && abs(l2_dxy) < 0.05 && l2_reliso_rho_03 < 0.2', # l2 genuine 
                            'hnl_q_02 == 0'                                                                                                      , # opposite charge
                            'l1_pt > 5 && abs(l1_eta) < 2.5 && abs(l1_dz) < 2. && abs(l1_dxy) > 0.05'                                            , # l1 kinematics and impact par
                           ])

    if ch == 'mmm':
        cuts = ' && '.join(['l0_pt > 25 && abs(l0_eta) < 2.4 && l0_id_m == 1 && abs(l0_dz) < 0.2 && abs(l0_dxy) < 0.05 && l0_reliso_rho_03 < 0.2', # l0 genuine
                            'l1_pt > 5 && abs(l1_eta) < 2.4 && abs(l1_dz) < 2',
                            'l2_pt > 5 && abs(l2_eta) < 2.4 && abs(l2_dz) < 2', 
                           ])

    return cuts


def skim(ch='mmm'):

    files = makeFiles(ch)
    baseline  = baseCuts(ch)

    print '\n\tloading datasets...\n'

    datasets =[]
    for ilabel, ifile in files:
        print 'importing', ifile
        dataset = pd.DataFrame(root_numpy.root2array(ifile, 'tree', selection=baseline))
        dataset['label'] = ilabel
        datasets.append(dataset)

    print '\n\tconcatenating...'
    result = pd.concat(datasets)
    print '\n\t...loading done'


    nevents = result.shape[0]
    aPop = 100000
    nslices = int(nevents/aPop) + 1
    print '\n\tnumber of slices:', nslices 

    RANGE = range(nslices)
    for islice in RANGE:#[:3]:

        print '\n\tslice:', islice
        sub_result = result[islice * aPop : (islice+1)*aPop]
        
        print '\tstaging...'
        sub_result.to_root(outDir + '%s_tree_slice_%d.root'%(ch,islice), key='tree')
        print '\t...slice', (islice + 1), 'done'

    print '\n\t...done'
