from ROOT import RDataFrame as RDF
import os, platform
import ROOT as rt
import numpy as np
from shutil import copyfile
from glob import glob
import pickle
import re, sys
from datetime import datetime
from pdb import set_trace
from copy import deepcopy
from os.path import normpath, basename, split
from collections import OrderedDict
from itertools import product

import root_pandas
import uproot as ur
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from itertools import product

from root_numpy import root2array

from keras.models import Sequential, Model, load_model
from keras.layers import Dense, Input
from keras.utils import plot_model

from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve, roc_auc_score

today   = datetime.now()
date    = today.strftime('%y%m%d')
hour    = str(today.hour)
minit   = str(today.minute)

'''
WATCH OUT THAT CODE HAS TO BE C++ COMPATIBLE

Linux-2.6.32-754.3.5.el6.x86_64-x86_64-with-redhat-6.6-Carbon         #T3
Linux-3.10.0-957.1.3.el7.x86_64-x86_64-with-centos-7.6.1810-Core      #LX+
'''
eos       = '/eos/user/v/vstampf/'
eos_david = '/eos/user/d/dezhu/HNL/'
if platform.platform() in['Linux-2.6.32-754.3.5.el6.x86_64-x86_64-with-redhat-6.6-Carbon', 'Linux-3.10.0-862.14.4.el7.x86_64-x86_64-with-redhat-7.5-Maipo']:
   eos       = '/t3home/vstampf/eos/'
   eos_david = '/t3home/vstampf/eos-david/'

#rt.ROOT.EnableImplicitMT(8)

def produceLightTree(sample='DY',ch='mmm'):
    if ch == 'mmm':
        d17B = data_B_mmm+suffix; d17C = data_C_mmm+suffix; d17D = data_D_mmm+suffix; d17E = data_E_mmm+suffix; d17F = data_F_mmm+suffix; 
        SFR_012_L = SFR_MMM_012_L
        l2_tight = l2_m_tight

    if ch == 'eem':
        d17B = data_B_eem+suffix; d17C = data_C_eem+suffix; d17D = data_D_eem+suffix; d17E = data_E_eem+suffix; d17F = data_F_eem+suffix; 

    t = rt.TChain('tree')

    if sample == 'DY':
        t.Add(DY)
        t.Add(DY_ext)

    if sample == 'data':
        t.Add(d17B)
       #t.Add(d17C)
       #t.Add(d17D)
       #t.Add(d17E)
       #t.Add(d17F)

    print '\n\ttotal entries:', t.GetEntries()

    df = RDF(t)
    df1 = df.Define('LOOSE', '1 * (' + SFR_012_L + ' && hnl_dr_12 > 0.3 && hnl_dr_02 > 0.3 && abs(hnl_m_01 - 91.19) < 10 && hnl_q_01 == 0 )' )
    df2 = df1.Define('TIGHT', '1 * (' + SFR_012_L + ' && hnl_dr_12 > 0.3 && hnl_dr_02 > 0.3 && abs(hnl_m_01 - 91.19) < 10 && hnl_q_01 == 0 && ' + l2_tight + ')' )

    num_L = df2.Filter('LOOSE == 1').Count().GetValue()
    print '\n\tloose entries in MR:', num_L 

    num_T = df2.Filter('TIGHT == 1').Count().GetValue()
    print '\n\ttight entries in MR:', num_T

    df2 = df2.Define('ptcone', PTCONEL2)

    branchList = rt.vector('string')()
    for br in ['event', 'lumi', 'run', 'LOOSE', 'TIGHT', 'l2_reliso_rho_03', 'l2_Medium', 'l2_eta', 'l2_pt', 'l2_dxy', 'l2_dz', 'ptcone']:
        branchList.push_back(br)
    df2.Snapshot('tree', saveDir+'/%s_%s_6_24B_Lcut_29_4.root'%(sample,ch), branchList)

def split(file_name): #without.root
    tfile = rt.TFile(file_name+'.root')
    tree = tfile.Get('tree')

    df = RDF(tree)
    n = tree.GetEntries()
    df1 = df.Range(0,int(n/2))
    df2 = df.Range(int(n/2),0)
    df1.Snapshot('tree', '%s_training_half.root'%file_name)
    df2.Snapshot('tree', '%s_untouched_half.root'%file_name)


def run_nn(tree_file_name,sample_name):
    # calculate predictions on sample
    print 'Engaging Neural Network for %s'%sample_name
    # tree_file_name='/home/dehuazhu/SESSD/4_production/production_20190411_Data_mmm/ntuples/Single_mu_2017B/HNLTreeProducer/tree.root'
    # path_to_tree = file_name + 'sfr_weights.root'
    path_to_tree = 'modules/%s_sfr_weights.root'%sample_name
    if os.path.isfile(path_to_tree): 
        print 'Using existing friendtree at %s'%path_to_tree
        return path_to_tree

    features = ['l2_abs_dxy', 'l2_abs_eta', 'l2_ptcone']
    branches = ['event', 'lumi', 'l2_pt', 'l2_dxy', 'l2_eta', 'l2_dz', 'l2_reliso_rho_03'] 

    f = ur.open(tree_file_name)
    t = f['tree']
    df = t.pandas.df(branches)

    
    df['l2_abs_dxy'] = np.abs(df.l2_dxy)
    df['l2_abs_eta'] = np.abs(df.l2_eta)
    df['l2_ptcone']  = df.l2_pt * (1 + np.maximum(0, df.l2_reliso_rho_03 - 0.2) )

    X = pd.DataFrame(df, columns=features)

    classifier = load_model('modules/net.h5')
    print 'predicting on' + tree_file_name
    Y = classifier.predict(X)

   #self.data_train.insert(len(self.data_train.columns), 'score', self.y1)
   #k = np.sum(self.data_train.score)
   #T = np.count_nonzero(self.data_train.TIGHT)
   #K = T/k 
   #print(k, T, K)

    K = 1.0

    # add the score to the data_train_l sample
    df.insert(len(df.columns), 'ml_fr', K * Y)
    df.to_root(path_to_tree, key = 'tree')
    print 'friend tree stored in %s'%path_to_tree
    return path_to_tree

   # def checkFakeRate(self,file_name='data_6_24'):

   #     tfile1 = rt.TFile(saveDir+'data_6_18_training_half_output.root')
   #     #tfile2 = rt.TFilesaveDir+''%s_untouched_half_output.root'%file_name)
   #     tfile2 = rt.TFile(saveDir+'data_eem_6_19_output.root')

   #     tree1 = tfile1.Get('tree')
   #     tree2 = tfile2.Get('tree')

   #     tree1.Draw('score>>SCORE_T_trained(100,0,1)',   'TIGHT==1')
   #     tree1.Draw('score>>SCORE_LNT_trained(100,0,1)', 'TIGHT==0')
   #     tree2.Draw('score>>SCORE_T_free(100,0,1)',   'TIGHT==1')
   #     tree2.Draw('score>>SCORE_LNT_free(100,0,1)', 'TIGHT==0')

   #     h_T_trained   = rt.gDirectory.Get('SCORE_T_trained')
   #     h_LNT_trained = rt.gDirectory.Get('SCORE_LNT_trained')
   #     h_T_free   = rt.gDirectory.Get('SCORE_T_free')
   #     h_LNT_free = rt.gDirectory.Get('SCORE_LNT_free')

   #     h_T_trained.SetLineColor(rt.kRed+2)
   #     h_LNT_trained.SetLineColor(rt.kGreen+2)
   #     h_T_free.SetLineColor(rt.kRed+2)
   #     h_LNT_free.SetLineColor(rt.kGreen+2)

   #     c1 = rt.TCanvas('training_half','training_half'); c1.cd()
   #     h_LNT_trained.SetAxisRange(0.0,0.3,'X')
   #     h_LNT_trained.SetTitle('')
   #     h_T_trained.SetTitle('')
   #     h_LNT_trained.DrawNormalized()
   #     h_T_trained.DrawNormalized('same')
   #     c1.BuildLegend(0.5,0.5,0.9,0.75)
   #     c1.SaveAs(saveDir+'training_half.root')
   #     c1.SaveAs(saveDir+'training_half.pdf')

   #     c2 = rt.TCanvas('untouched_half','untouched_half'); c2.cd()
   #     h_LNT_free.SetAxisRange(0.0,0.3,'X')
   #     h_LNT_free.SetTitle('')
   #     h_T_free.SetTitle('')
   #     h_LNT_free.DrawNormalized()
   #     h_T_free.DrawNormalized('same')
   #     c2.BuildLegend(0.5,0.5,0.9,0.75)
   #     c2.SaveAs(saveDir+'untouched_half.root')
   #     c2.SaveAs(saveDir+'untouched_half.pdf')

######################################################################################

######################################################################################
# https://stackoverflow.com/questions/616645/how-to-duplicate-sys-stdout-to-a-log-file
#class Logger(object):
#    def __init__(self, fileName):
#        self.terminal = sys.stdout
#        self.log = open(fileName+'.log', 'a')
#
#    def write(self, message):
#        self.terminal.write(message)
#        self.log.write(message) 
#
#def makeFolder(name):
#
#    plotDir = eos+'plots/DDE/'
#    today = datetime.now(); date = today.strftime('%y%m%d'); hour = str(today.hour); minit = str(today.minute)
#    plotDir = plotDir + name + '_' + date + '_' + hour + 'h_' + minit + 'm/'
#    os.mkdir(plotDir)
#    return plotDir
#
#def makeLabel(sample_dir, ch='mmm', lbl='1',era='B'):
#    '''create a label (friend) tree for a respective sample
#       use the following: data: 0, DY: 1, TT: 2, WJ: 3''' 
#    if lbl != '0': era = ''
#    fin = rt.TFile(sample_dir+suffix)
#    tr = fin.Get('tree')
#    ldf = rdf(tr)
#    df = ldf.Define('label', lbl)
#    bL = rt.vector('string')()
#    for br in ['event', 'lumi', 'label']:
#        bL.push_back(br)
#    df.Snapshot('tree', plotDir + 'friend_tree_label_%s_%s%s.root'%(ch,lbl,era), bL)

############################################################################################################################################################################
#class nn(object):
#
#    def __init__(self):
#        self.netDir = ''
#        np.random.seed(1986)
#        self.branches = [
#        #     'event',        
#        #     'lumi',        
#        #     'run',        
#        #     'TIGHT',        
#             'l2_abs_eta',        
#             'l2_ptcone',        
#             'l2_abs_dxy',        
#        #     'l2_dz',        
#        ]

#    def train(self):
#
#        print ('training classifier')
#        self.classifier.fit(self.X[self.features], self.Y, epochs=10, validation_split=0.3)  
#        self.classifier.save(self.netDir + 'net_6_24B_Lcut_29_4.h5')
#
#        self.features = self.branches
#
#        classifier_input  = Input((len(self.branches),))
#        #classifier_dense1 = Dense(64, activation='tanh'   )(classifier_input )
#        #classifier_dense2 = Dense(64, activation='relu'   )(classifier_dense1)
#        classifier_dense1 = Dense(128, activation='tanh'  )(classifier_input)
#        classifier_output = Dense( 1, activation='sigmoid')(classifier_dense1)
#
#        self.classifier = Model(classifier_input, classifier_output)
#        self.classifier.compile('Adam', loss='binary_crossentropy', loss_weights=[1])        
#        plot_model(self.classifier, show_shapes=True, show_layer_names=True, to_file=saveDir+'classifier.png')
#
#        self.ndf_training_half_LOOSE  = root2array(saveDir+'data_mmm_6_24B_Lcut_29_4.root' , 'tree', selection='LOOSE == 1')
#
#        self.data_train_l = pd.DataFrame( self.ndf_training_half_LOOSE )
##
#        self.data_train_l['l2_ptcone']  = self.data_train_l.l2_pt * (1 + np.maximum(0, self.data_train_l.l2_reliso_rho_03 - 0.2) )
#        self.data_train_l['l2_abs_eta'] = np.abs(self.data_train_l.l2_eta) 
#        self.data_train_l['l2_abs_dxy'] = np.abs(self.data_train_l.l2_dxy)
#        self.data_train_l = self.data_train_l.sample(frac=1, replace=True, random_state=1986)
#
#        self.X = pd.DataFrame(self.data_train_l, columns=self.branches)
#        self.Y = pd.DataFrame(self.data_train_l, columns=['TIGHT'])
