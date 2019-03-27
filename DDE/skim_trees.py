import ROOT
import root_pandas
import numpy as np
import pandas as pd
import pandas, root_numpy

files = [
    (0, '/work/dezhu/4_production/production_20190306_BkgMC/mem/ntuples/DYBB/HNLTreeProducer/tree.root'              ),
    (1, '/work/dezhu/4_production/production_20190306_BkgMC/mem/ntuples/DYJetsToLL_M50/HNLTreeProducer/tree.root'    ),
    (1, '/work/dezhu/4_production/production_20190306_BkgMC/mem/ntuples/DYJetsToLL_M50_ext/HNLTreeProducer/tree.root'),
    (2, '/work/dezhu/4_production/production_20190306_BkgMC/mem/ntuples/TTJets/HNLTreeProducer/tree.root'            ),
]

baseline_selection = '&'.join([
    'l0_pt>25 & abs(l0_eta)<2.4 & l0_id_m & abs(l0_dz)<0.2 & abs(l0_dxy)<0.05 & l0_reliso_rho_03<0.2', # l0 genuine
    'l2_pt>10 & abs(l2_eta)<2.4 & l2_id_m & abs(l2_dz)<0.2 & abs(l2_dxy)<0.05 & l2_reliso_rho_03<0.2', # l2 genuine 
    'hnl_q_02==0'                                                                                    , # opposite charge
    'l1_pt>5 & abs(l1_eta)<2.5 & abs(l1_dz)<2. & abs(l1_dxy)>0.05'                                   , # l1 kinematics and impact parameter
])

datasets =[]

for ilabel, ifile in files:
    print 'importing', ifile
    dataset = pandas.DataFrame(root_numpy.root2array(ifile, 'tree', selection=baseline_selection))
    dataset['label'] = ilabel
    datasets.append(dataset)

print 'concatenating...'
result = pd.concat(datasets)
print '...done'

print 'staging...'
result.to_root('mme_tree.root', key='tree', store_index=False)
print '...done'

