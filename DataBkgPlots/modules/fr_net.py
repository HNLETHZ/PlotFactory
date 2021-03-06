'''
Resources:
https://en.wikipedia.org/wiki/Universal_approximation_theorem
http://neuralnetworksanddeeplearning.com/chap4.html
https://github.com/thomberg1/UniversalFunctionApproximation
'''
from pdb import set_trace
from modules.Samples import createSampleLists, setSumWeights
import modules.Selections as Selections 
from modules.Selections import getSelection
from ROOT import ROOT,TChain, RDataFrame, TCanvas, TH2F
import os
from socket import gethostname
from shutil import copyfile
import uproot as ur
from modules.DataMCPlot import DataMCPlot 
import plotfactory as pf
import pickle
import math

import root_pandas

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from itertools import product

from root_numpy import root2array, tree2array

from tensorflow.keras.models import Sequential, Model, load_model
from tensorflow.keras.layers import Dense, Input, Dropout, BatchNormalization
from tensorflow.keras.utils import plot_model
from tensorflow.keras.callbacks import EarlyStopping, Callback, ReduceLROnPlateau, ModelCheckpoint
from tensorflow.keras import backend as K
from tensorflow.keras.activations import softmax
from tensorflow.keras.constraints import unit_norm
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.optimizers import SGD, Adam

from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve, roc_auc_score

import time
import multiprocessing

import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2' #used to deactivate Tensorflow minor warnings

from modules.path_to_NeuralNet import path_to_NeuralNet

import sys

       

ROOT.EnableImplicitMT()
# fix random seed for reproducibility (TODO! check the reproducibility)
# np.random.seed(1986)

def tree2array_process(queue, chain, branches, selection, key):
    print ('converting .root ntuples to numpy arrays... (%s events)'%key)
    array = tree2array(
                    chain,
                    branches = branches,
                    selection = selection
                    )
    print ('nevents from array (%s): '%key+ str(len(array)))
    queue.put([key,array])

def ex():
    q = multiprocessing.Queue()
    result = []
    processes = [multiprocessing.Process(target=f, args=(q,x)) for x in ['pass','fail']]
    for p in processes: p.start()
    for p in processes: 
        result.append(q.get())
    p.join()

def root2array_process(queue, file_in, branches, selection, sample_name, key):
    # print ('computing %s events for %s'%(key,sample_name))
    array = pd.DataFrame(
                root2array(
                    file_in,
                    'tree',
                    branches,
                    selection
                )
            )
    # print ('nevents %s (%s): %d'%(sample_name,key,len(array)))
    queue.put([key,sample_name,array])

def root2array_PoolProcess(input_array):
    file_in     = input_array[0]
    branches    = input_array[1]
    selection   = input_array[2]
    sample_name = input_array[3]
    key         = input_array[4]
    xsec        = input_array[5]
    sumweights  = input_array[6]

    # print ('computing %s events for %s'%(key,sample_name))
    array = pd.DataFrame(
                root2array(
                    file_in,
                    'tree',
                    branches,
                    selection
                )
            )
    print ('nevents %s (%s): %d'%(sample_name,key,len(array)))
    return [key,array,xsec,sumweights]

def createArrays(features, branches, path_to_NeuralNet, faketype = 'DoubleFake', channel = 'mmm', multiprocess = True, dataset = '2017', analysis_dir = '/home/dehuazhu/SESSD/4_production/'):
    #define basic environmental parameters
    hostname        = gethostname()
    channel         = channel
    sample_dict     = {}

    # call samples
    samples_all, samples_singlefake, samples_doublefake, samples_nonprompt, samples_mc, samples_data = createSampleLists(analysis_dir=analysis_dir, server = hostname, channel=channel, dataset = dataset)
    working_samples = samples_data
    # working_samples = samples_nonprompt
    # working_samples = samples_mc

    # necessary if you want to compare data with MC
    working_samples = setSumWeights(working_samples)
    samples_mc      = setSumWeights(samples_mc)

    # make a TChain object by combining all necessary data samples
    print('###########################################################')
    if faketype == 'DoubleFake': print('# measuring doublefakerate...')
    if faketype == 'SingleFake1': print('# measuring singlefakerate for lepton 1...')
    if faketype == 'SingleFake2': print ('# measuring singlefakerate for lepton 2...')
    print('# %d samples to be used:'%(len(working_samples)))
    print('###########################################################')
    for w in working_samples: print('{:<20}{:<20}'.format(*[w.name,('path: '+w.ana_dir)]))


    chain = TChain('tree') #TChain'ing all data samples together
    for i,s in enumerate(working_samples):
        # sample = working_samples[0] #super stupid mistake, I'm keeping it here as a painful reminder
        sample = working_samples[i]
        file_name = '/'.join([sample.ana_dir, sample.dir_name, sample.tree_prod_name, 'tree.root'])
        chain.Add(file_name)

    
    # define the selections
    if faketype == 'SingleFake1':
        region = Selections.Region('MR_SF1',channel,'MR_SF1')
        selection_passing = region.data
        selection_failing = region.SF_LT

    if faketype == 'SingleFake2':
        region = Selections.Region('MR_SF2',channel,'MR_SF2')
        selection_passing = region.data
        selection_failing = region.SF_TL

    if faketype == 'DoubleFake':
        region = Selections.Region('MR_DF',channel,'MR_DF')
        selection_passing = region.data
        selection_failing = region.DF

    if faketype == 'nonprompt':
        region = Selections.Region('MR_nonprompt',channel,'SR')
        selection_passing    = region.data
        selection_failing    = region.nonprompt
        selection_passing_MC = region.MC_contamination_pass
        selection_failing_MC = region.MC_contamination_fail


    # convert TChain object into numpy arrays for the training
    start = time.time()
    if multiprocess == True:
        queue = multiprocessing.Queue()
        result = []
        processes =[]

        for key in ['pass','fail']:
            if key == 'pass': selection = selection_passing
            if key == 'fail': selection = selection_failing
            processes.append(multiprocessing.Process(target=tree2array_process, args=(queue, chain, branches, selection, key)))

        for p in processes: 
            p.start()

        for p in processes: 
            result.append(queue.get())
            p.join()

        for r in result:
            if r[0] == 'pass':
                array_pass = r[1]
            if r[0] == 'fail':
                array_fail = r[1]

    if multiprocess == False:
        print ('converting .root ntuples to numpy arrays... (passed events)')
        array_pass = tree2array(chain, branches = branches, selection = selection_passing)
        print ('nevents from array_pass: '+ str(array_pass.size))

        print ('converting .root ntuples to numpy arrays... (failed events)')
        array_fail = tree2array(chain, branches = branches, selection = selection_failing)
        print ('nevents from array_fail: '+ str(array_fail.size))
    
    delta = time.time() - start
    print ('It took %.2f seconds to create the arrays'%delta)

    df_pass    = pd.DataFrame(array_pass)
    df_fail    = pd.DataFrame(array_fail)
    
    #giving data the contamination weight '1' (i.e. ignore it)
    for array in [df_pass, df_fail]:
        array['contamination_weight'] = array.weight * array.lhe_weight 
        # array['contamination_weight'] = array.weight * array.lhe_weight * lumi *  xsec / sumweights

    # adding MC prompt contamination
    print ('now adding MC prompt contamination to the training')
    lumi = 41530 # all eras
    # lumi = 4792 # only era B

    if multiprocess == True:
        pool = multiprocessing.Pool(len(samples_mc))
        input_array = []

        for i, sample in enumerate(samples_mc):
            for key in ['pass','fail']:
                file_in = '/'.join([sample.ana_dir, sample.dir_name, sample.tree_prod_name, 'tree.root'])
                if key == 'pass': selection = selection_passing_MC
                if key == 'fail': selection = selection_failing_MC
                entry = [file_in,branches,selection,sample.name,key,sample.xsec,sample.sumweights]
                input_array.append(entry)

        result = pool.map(root2array_PoolProcess,input_array)


        for i, sample in enumerate(result): 
            array       = sample[1]
            xsec        = sample[2]
            sumweights  = sample[3]
            try:
                array['contamination_weight'] = array.weight * array.lhe_weight * lumi * (-1) *  xsec / sumweights
                # array['contamination_weight'] = array.weight * array.lhe_weight * lumi *  xsec /sumweights 
                # array['contamination_weight'] = array.weight * array.lhe_weight 
            except:
                set_trace()

            
            if sample[0] == 'pass':
                df_pass = pd.concat([df_pass,array]) 
                # df_fail = pd.concat([df_fail,array])
                # print ('added pass events to df_pass: %d'%len(array))

            if sample[0] == 'fail':
                # df_pass = pd.concat([df_pass,array]) 
                df_fail = pd.concat([df_fail,array])
                # print ('added fail events to df_pass: %d'%len(array))




    if multiprocess == False:
        for i,s in enumerate(samples_mc):
            sample = samples_mc[i]
            print ('computing %s'%sample.name)
            file_in = '/'.join([sample.ana_dir, sample.dir_name, sample.tree_prod_name, 'tree.root'])

            selection_pass = selection_passing_MC
            selection_fail = selection_failing_MC

            passing = pd.DataFrame( root2array(file_in, 'tree', branches=branches, selection = selection_passing_MC) )
            failing = pd.DataFrame( root2array(file_in, 'tree', branches=branches, selection = selection_failing_MC) )

            for array in [passing, failing]:
                array['contamination_weight'] = array.weight * array.lhe_weight * lumi * (-1) *  sample.xsec / sample.sumweights 
                # array['contamination_weight'] = array.weight * array.lhe_weight * lumi *  sample.xsec / sample.sumweights 
            df_pass = pd.concat([df_pass,passing])
            # df_pass = pd.concat([df_fail,failing])
            # df_fail = pd.concat([df_fail,passing])
            df_fail = pd.concat([df_fail,failing])

    print ('array size after including MC: %d(pass); %d(fail)'%(len(df_pass),len(df_fail)))


    # add the target column
    df_pass['target'] = np.ones (df_pass.shape[0]).astype(np.int)
    df_fail['target'] = np.zeros(df_fail.shape[0]).astype(np.int)

    # concatenate the events and shuffle
    data = pd.concat([df_pass, df_fail])
    data = data.sample(frac=1, replace=False, random_state=1986) # shuffle (and DON'T replace the sample)
    data.index = np.array(range(len(data)))

    data.to_pickle(path_to_NeuralNet + 'training_data.pkl')

def train(features,branches,path_to_NeuralNet,newArrays = False, faketype = 'DoubleFake', channel = 'mmm', multiprocess = True, dataset = '2017', analysis_dir = '/home/dehuazhu/SESSD/4_production/'):
    hostname = gethostname()
    if not os.path.exists(path_to_NeuralNet):
        os.mkdir(path_to_NeuralNet)
        print ("Output directory created. ")
        print ("Output directory: %s"%(path_to_NeuralNet))
    else:
        # print ("Output directory: ", path_to_NeuralNet, "already exists, overwriting it!")
        if newArrays == True:
            print ("Output directory already exists, overwriting it! ")
            print ("Output directory: %s"%(path_to_NeuralNet))
            os.system("rm -rf %s"%(path_to_NeuralNet))
            os.system("mkdir %s"%(path_to_NeuralNet))
        if newArrays == False:
            print ("Output directory already exists, using existing .pkl files")
    
    copyfile('modules/fr_net.py', path_to_NeuralNet+'/fr_net.py')
    copyfile('modules/Selections.py', path_to_NeuralNet+'/Selections.py')
    copyfile('modules/Samples.py', path_to_NeuralNet+'/Samples.py')

    print ('cfg files stored in ' + path_to_NeuralNet)

    if newArrays == True:
        createArrays(features, branches, path_to_NeuralNet, faketype, channel, multiprocess, dataset = dataset, analysis_dir = analysis_dir)

    data = pd.read_pickle(path_to_NeuralNet + 'training_data.pkl')

    # #define indirect training variables
    data, features, branches =  add_branches(data,features,branches)
    print ('training features: ')
    for f in features: print (f)
   
    # define X and Y
    X = pd.DataFrame(data, columns=branches)
    Y = pd.DataFrame(data, columns=['target'])

    # define the activation functions
    activation = 'tanh'
    # activation = 'selu'
    # activation = 'sigmoid'
    # activation = 'relu'
    # activation = 'LeakyReLU' #??????

    # define the net
    input  = Input((len(features),))

    # old version
    dense1 = Dense(64, activation='relu'   , name='dense1')(input )
    dropout1 = Dropout(0.5, seed = 123456)(dense1)
    output = Dense( 1, activation='sigmoid', name='output')(dense1)


    # new version
    input  = Input((len(features),))
    layer  = Dense(4096, activation=activation   , name='dense1', kernel_constraint=unit_norm())(input)
    layer  = Dropout(0.4, name='dropout1')(layer)
    layer  = BatchNormalization()(layer)
    layer  = Dense(128, activation=activation   , name='dense2', kernel_constraint=unit_norm())(layer)
    layer  = Dropout(0.4, name='dropout2')(layer)
    layer  = BatchNormalization()(layer)
    # layer  = Dense(16, activation=activation   , name='dense3', kernel_constraint=unit_norm())(layer)
    # layer  = Dropout(0.4, name='dropout3')(layer)
    # layer  = BatchNormalization()(layer)
    # layer  = Dense(16, activation=activation   , name='dense4', kernel_constraint=unit_norm())(layer)
    # layer  = Dropout(0.4, name='dropout4')(layer)
    # layer  = BatchNormalization()(layer)
    layer  = Dense(16, activation=activation   , name='dense5', kernel_constraint=unit_norm())(layer)
    layer  = Dropout(0.2, name='dropout5')(layer)
    layer  = BatchNormalization()(layer)
    output = Dense(  1, activation='sigmoid', name='output', )(layer)

    # Define outputs of your model
    model = Model(input, output)

    # choose your optimizer
    # opt = SGD(lr=0.0001, momentum=0.8)
    # opt = Adam(lr=0.001, decay=0.1, beta_1=0.9, beta_2=0.999, amsgrad=False)
    # opt = Adam(decay=0.1, beta_1=0.9, beta_2=0.999, amsgrad=False)
    opt = 'Adam'

    # compile and choose your loss function (binary cross entropy for a 1-0 classification problem)
    model.compile(optimizer=opt, loss='binary_crossentropy', metrics=['mae','acc'])

    print (model.summary())

    # plot the models
    # https://keras.io/visualization/
    plot_model(model, show_shapes=True, show_layer_names=True, to_file=path_to_NeuralNet + 'model.png')

    # normalize inputs FIXME! do it, but do it wisely # try also standard scaler!
    # https://scikit-learn.org/stable/auto_examples/preprocessing/plot_all_scaling.html#sphx-glr-auto-examples-preprocessing-plot-all-scaling-py

    #Import two different preprocessor
    from sklearn.preprocessing import QuantileTransformer, RobustScaler

    #Choose the preprocessor
    # qt = QuantileTransformer(output_distribution='normal', random_state=1986)
    qt = RobustScaler()

    qt.fit(X[features])
    xx = qt.transform(X[features])
    pickle.dump( qt, open( path_to_NeuralNet + 'input_transformation.pck', 'wb' ) )

    
    # train, give the classifier a head start
    # early stopping
    # monitor = 'val_acc'
    monitor = 'val_loss'
    # monitor = 'val_mae'

    # early stopping
    es = EarlyStopping(monitor=monitor, mode='auto', verbose=1, patience=30, restore_best_weights=True)

    # reduce learning rate when at plateau, fine search the minimum
    reduce_lr = ReduceLROnPlateau(monitor=monitor, mode='auto', factor=0.2, patience=10, min_lr=0.00001, cooldown=10, verbose=True)

    # save the model every now and then
    filepath = path_to_NeuralNet + 'saved-model-{epoch:04d}_val_loss_{val_loss:.4f}_val_acc_{val_acc:.4f}.h5'
    save_model = ModelCheckpoint(filepath, monitor='val_acc', verbose=1, save_best_only=True, save_weights_only=False, mode='auto', period=1)

    # weight the events according to their displacement (favour high displacement)
    weight = np.array(np.power(X['hnl_2d_disp'], 0.2))

    xx = np.asarray(xx)
    Y  = np.asarray(Y)

    # train only the classifier. beta is set at 0 and the discriminator is not trained
    # history = model.fit(X[features], Y, epochs=500, validation_split=0.5, callbacks=[es])  

    # history = model.fit(xx, Y, batch_size = 512, epochs=1000, verbose = 1,  validation_split=0.5, callbacks=[es],sample_weight = np.array(data.contamination_weight))
    history = model.fit(xx, Y, epochs=2000, validation_split=0.5, callbacks=[es, reduce_lr, save_model], batch_size=32, verbose=True, sample_weight=weight)  

    # plot loss function trends for train and validation sample
    plt.clf()
    plt.title('loss')
    plt.plot(history.history['loss'], label='train')
    plt.plot(history.history['val_loss'], label='test')
    plt.legend()
    # plt.yscale('log')
    center = min(history.history['val_loss'] + history.history['loss'])
    plt.ylim((center*0.98, center*1.5))
    plt.grid(True)
    plt.savefig(path_to_NeuralNet + 'loss_function_history_weighted.pdf')
    plt.clf()

    # plot accuracy trends for train and validation sample
    plt.title('accuracy')
    plt.plot(history.history['acc'], label='train')
    plt.plot(history.history['val_acc'], label='test')
    plt.legend()
    center = max(history.history['val_acc'] +  history.history['acc'])
    plt.ylim((center*0.85, center*1.02))
    # plt.yscale('log')
    plt.grid(True)
    plt.savefig(path_to_NeuralNet + 'accuracy_history_weighted.pdf')
    plt.clf()

    # plot mean absolute error 
    plt.title('mean absolute error')
    plt.plot(history.history['mae'], label='train')
    plt.plot(history.history['val_mae'], label='test')
    plt.legend()
    center = min(history.history['val_mae'] + history.history['mae'])
    plt.ylim((center*0.98, center*1.5))
    # plt.yscale('log')
    plt.grid(True)
    plt.savefig(path_to_NeuralNet + 'mean_absolute_error_history_weighted.pdf')
    plt.clf()

    # calculate predictions on the data sample
    print ('predicting on ', data.shape[0], 'events')
    x = pd.DataFrame(data, columns=features)

    # apply the Transformer also for the evaluation process
    qt = pickle.load(open( path_to_NeuralNet + 'input_transformation.pck', 'rb' ))
    xx = qt.transform(x[features])

    y = model.predict(xx)

    # impose norm conservation if you want probabilities
    # compute the overall rescaling factor scale
    scale = 1.
    # scale = np.sum(passing['target']) / np.sum(y)

    # add the score to the data sample
    data.insert(len(data.columns), 'ml_fr', scale * y)

    # let sklearn do the heavy lifting and compute the ROC curves for you
    fpr, tpr, wps = roc_curve(data.target, data.weight) 
    plt.plot(fpr, tpr)
    xy = [i*j for i,j in product([10.**i for i in range(-8, 0)], [1,2,4,8])]+[1]
    plt.plot(xy, xy, color='grey', linestyle='--')
    plt.yscale('linear')
    plt.savefig(path_to_NeuralNet + 'roc.pdf')

    # save model and weights
    model.save(path_to_NeuralNet + 'net.h5')
    print ('Neural Net saved as ' + path_to_NeuralNet + 'net.h5')
    # model.save_weights('net_model_weights.h5')

    # rename branches, if you want
    # data.rename(
    #     index=str, 
    #     columns={'cand_refit_mass12': 'mass12',}, 
    #     inplace=True)

    # save ntuple
    data.to_root(path_to_NeuralNet + 'output_ntuple.root', key='tree', store_index=False)

def make_all_friendtrees(multiprocess,server,analysis_dir,channel,path_to_NeuralNet,overwrite, dataset = '2017'):
    print ('making friendtrees for all datasamples')
    start = time.time()
    # call samples
    samples_all, samples_singlefake, samples_doublefake, samples_nonprompt, samples_mc, samples_data = createSampleLists(analysis_dir=analysis_dir, server = server, channel=channel, dataset = dataset)
    working_samples = samples_nonprompt
    for w in working_samples: print('{:<20}{:<20}'.format(*[w.name,('path: '+w.ana_dir)]))

    if multiprocess == True:
        pool = multiprocessing.Pool(len(working_samples))
        input_array = []

        for i, sample in enumerate(working_samples):
            sample = working_samples[i]
            file_name = '/'.join([sample.ana_dir, sample.dir_name, sample.tree_prod_name, 'tree.root'])
            input_array.append([
                        file_name,
                        sample.name,
                        path_to_NeuralNet + 'net.h5',
                        path_to_NeuralNet,
                        get_branches_nonprompt2(get_features_nonprompt2()),
                        get_features_nonprompt2(),
                        overwrite,
                        ])
        result = pool.map(makeFriendtree_Process,input_array)

    if multiprocess == False:
        for i,s in enumerate(working_samples):
            sample = working_samples[i]
            file_name = '/'.join([sample.ana_dir, sample.dir_name, sample.tree_prod_name, 'tree.root'])
            friend_file_name = makeFriendtree(
                                tree_file_name = file_name,
                                sample_name = sample.name,
                                net_name = path_to_NeuralNet + 'net.h5',
                                path_to_NeuralNet = path_to_NeuralNet,
                                branches = get_branches_nonprompt2(get_features_nonprompt2()),
                                features = get_features_nonprompt2(),
                                overwrite = overwrite,
                                )
    duration = time.time() - start
    print ('It took %.2f seconds to make all friendtrees.'%duration)
        
def makeFriendtree_Process(input_array):
    tree_file_name      = input_array[0]
    sample_name         = input_array[1]
    net_name            = input_array[2]
    path_to_NeuralNet   = input_array[3]
    branches            = input_array[4]
    features            = input_array[5]
    overwrite           = input_array[6]
    path = makeFriendtree(tree_file_name,sample_name,net_name,path_to_NeuralNet,branches,features,overwrite)

def makeFriendtree(tree_file_name,sample_name,net_name,path_to_NeuralNet,branches,features,overwrite):
    path_to_tree = path_to_NeuralNet + 'friendtree_fr_%s.root'%sample_name
    if not overwrite:
        if os.path.isfile(path_to_tree): 
            print ('Using existing friendtree at %s'%path_to_tree)
            return path_to_tree
        else:
            print ('making friendtree for %s'%sample_name)
    else:
        if os.path.isfile(path_to_tree):
            os.system("rm %s"%(path_to_tree))
            print ('remaking friendtree for %s'%sample_name)
        else:
            print ('making friendtree for %s'%sample_name)


    data = pd.DataFrame(root2array(tree_file_name,'tree',branches,''))
    
    # f = ur.open(tree_file_name)
    # t = f['tree']

    # data = t.pandas.df(branches)

    # #define indirect training variables
    data, features, branches = add_branches(data,features,branches)
    try:
        x = pd.DataFrame(data, columns=features)
    except:
        set_trace()

    from sklearn.preprocessing import QuantileTransformer
    # xx = QuantileTransformer(output_distribution='normal').fit_transform(X[features])
    try:
        qt = pickle.load(open( path_to_NeuralNet + 'quantile_transformation.pck', 'rb' ))
    except:
        qt = pickle.load(open( path_to_NeuralNet + 'input_transformation.pck', 'rb' ))
    xx = qt.transform(x[features])

    classifier = load_model(net_name)
    print ('predicting on ' + tree_file_name)
    Y = classifier.predict(xx)
    scale = 1.0
    # add the score to the data_train_l sample
    data.insert(len(data.columns), 'ml_fr', scale * Y)
    data.to_root(path_to_tree, key = 'tree')
    print ('friend tree stored in %s'%path_to_tree)
    return path_to_tree

def add_branches(data,features,branches):
    # #define indirect training variables

    # data['ptcone'] = (( data.hnl_hn_vis_pt * (data.hnl_iso03_rel_rhoArea < 0.2) ) + ( (data.hnl_iso03_rel_rhoArea >= 0.2) * ( data.hnl_hn_vis_pt * (1. + data.hnl_iso03_rel_rhoArea - 0.2))))
    # features += ['ptcone']
    # branches += ['ptcone']

    # data['abs_eta'] = abs(data.hnl_hn_vis_eta)
    # features += ['abs_eta']
    # branches += ['abs_eta']

    # data['ptcone_l1'] = (( data.l1_pt * (data.l1_reliso_rho_03 < 0.2) ) + ( (data.l1_reliso_rho_03 >= 0.2) * ( data.l1_pt * (1. + data.l1_reliso_rho_03 - 0.2))))
    # data['ptcone_l1'] =  (  ( data.l1_pt * (1. + data.l1_reliso_rho_03)))
    # features += ['ptcone_l1']
    # branches += ['ptcone_l1']
    
    # data['ptcone_l2'] = (( data.l2_pt * (data.l2_reliso_rho_03 < 0.2) ) + ( (data.l2_reliso_rho_03 >= 0.2) * ( data.l2_pt * (1. + data.l2_reliso_rho_03 - 0.2))))
    # data['ptcone_l2'] =  (  ( data.l2_pt * (1. + data.l2_reliso_rho_03)))
    # features += ['ptcone_l2']
    # branches += ['ptcone_l2']

    data['log_abs_l0_dxy'] = np.log(abs(data.l0_dxy))
    features += ['log_abs_l0_dxy']
    branches += ['log_abs_l0_dxy']

    data['log_abs_l1_dxy'] = np.log(abs(data.l1_dxy))
    features += ['log_abs_l1_dxy']
    branches += ['log_abs_l1_dxy']

    data['log_abs_l2_dxy'] = np.log(abs(data.l2_dxy))
    features += ['log_abs_l2_dxy']
    branches += ['log_abs_l2_dxy']

    data['log_abs_l0_dz'] = np.log(abs(data.l0_dz))
    features += ['log_abs_l0_dz']
    branches += ['log_abs_l0_dz']

    data['log_abs_l1_dz'] = np.log(abs(data.l1_dz))
    features += ['log_abs_l1_dz']
    branches += ['log_abs_l1_dz']

    data['log_abs_l2_dz'] = np.log(abs(data.l2_dz))
    features += ['log_abs_l2_dz']
    branches += ['log_abs_l2_dz']

    data['log_abs_l0_eta'] = np.log(abs(data.l0_eta))
    features += ['log_abs_l0_eta']
    branches += ['log_abs_l0_eta']

    data['log_abs_l1_eta'] = np.log(abs(data.l1_eta))
    features += ['log_abs_l1_eta']
    branches += ['log_abs_l1_eta']

    data['log_abs_l2_eta'] = np.log(abs(data.l2_eta))
    features += ['log_abs_l2_eta']
    branches += ['log_abs_l2_eta']

    data['abs_dzDiff_12'] = abs(data.l1_dz - data.l2_dz)
    # features += ['abs_dzDiff_12']
    # branches += ['abs_dzDiff_12']

    data['abs_dphi_12'] = abs(data.l1_phi - data.l2_phi)
    # features += ['abs_dphi_12']
    branches += ['abs_dphi_12']

    data['equalJets_12'] = ((data.l1_jet_pt > 0) & (data.l1_jet_pt == data.l2_jet_pt)).astype(np.int)
    # features += ['equalJets_12']
    branches += ['equalJets_12']

    data['eta_hnl_l0'] = abs(data.hnl_hn_vis_eta - data.l0_eta)
    # features += ['eta_hnl_l0']
    branches += ['eta_hnl_l0']

    return data, features, branches

def get_ptCone():
    PTCONE   = '(  ( hnl_hn_vis_pt * (hnl_iso03_rel_rhoArea<0.2) ) + ( (hnl_iso03_rel_rhoArea>=0.2) * ( hnl_hn_vis_pt * (1. + hnl_iso03_rel_rhoArea - 0.2) ) )  )'
    return PTCONE

def get_features_DF():
    features = [
        'l1_eta',
        'l1_phi',
        'l1_pt',
        # 'l1_reliso_rho_03',
        'l2_eta',
        'l2_phi',
        'l2_pt',
        # 'l2_reliso_rho_03',
        'hnl_2d_disp',
        'hnl_dr_12',
        'hnl_m_12',
        'hnl_hn_vis_eta',
        'hnl_hn_vis_pt',
        # 'hnl_iso03_rel_rhoArea',
    ]
    return features

def get_branches_DF(features):
    branches = features + [
        'run',
        'lumi',
        'event',
        'hnl_iso04_rel_rhoArea',
        'l0_pt',
        'l0_eta',
        'l0_dz',
        'l0_dxy',
        'l0_reliso_rho_03',
        'l0_id_m',
        # 'l1_pt',
        # 'l1_eta',
        # 'l2_pt',
        # 'l2_eta',
        'l1_reliso_rho_03',
        'l2_reliso_rho_03',
        'hnl_q_12',
        'hnl_w_vis_m',
        'l1_Medium',
        'l2_Medium',
        'l1_jet_pt',
        'l2_jet_pt',
        # 'hnl_dr_12',
        # 'hnl_m_12',
        # 'hnl_hn_vis_eta',
        'hnl_iso03_rel_rhoArea',
        # 'hnl_hn_vis_pt',
    ]
    return branches

def get_features_SF1():
    features = [
        'l1_eta',
        'l1_phi',
        'l1_pt',
        'l1_dxy',
        'l1_dz',
    ]
    return features

def get_features_SF2():
    features = [
        'l2_eta',
        # 'l2_phi',
        'l2_pt',
        'l2_dxy',
        'l2_dz',
        # 'ptcone_l2',
    ]
    return features

def get_branches_SF1(features):
    branches = features + [
        'run',
        'lumi',
        'event',
        'l0_pt',
        'l0_eta',
        'l0_dz',
        'l0_dxy',
        'l0_reliso_rho_03',
        'l0_id_m',
        'l2_pt',
        'l2_eta',
        'l2_Medium',
        'l2_jet_pt',
        'l2_reliso_rho_03',
        'l1_Medium',
        'l1_jet_pt',
        'hnl_q_12',
        'hnl_w_vis_m',
        'hnl_dr_12',
        'hnl_m_12',
        'hnl_hn_vis_eta',
        'hnl_hn_vis_pt',
        'hnl_iso03_rel_rhoArea',
        'hnl_iso04_rel_rhoArea',
    ]
    return branches

def get_branches_SF2(features):
    branches = features + [
        'run',
        'lumi',
        'event',
        'l0_pt',
        'l0_eta',
        'l0_dz',
        'l0_dxy',
        'l0_reliso_rho_03',
        'l0_id_m',
        'l1_pt',
        'l1_eta',
        'l1_Medium',
        'l1_jet_pt',
        'l1_reliso_rho_03',
        'l2_Medium',
        'l2_jet_pt',
        'hnl_q_12',
        'hnl_w_vis_m',
        'hnl_dr_12',
        'hnl_m_12',
        'hnl_hn_vis_eta',
        'hnl_hn_vis_pt',
        'hnl_iso03_rel_rhoArea',
        'hnl_iso04_rel_rhoArea',
        # 'l2_pt',
        'l2_reliso_rho_03',
    ]
    return branches

def get_features_nonprompt():
    features = [
        'l1_eta',
        'l1_pt',
        'l1_dxy',

        'l2_eta',
        'l2_pt',
        'l2_dxy',

        'hnl_2d_disp',
        'hnl_dr_12',
	'hnl_m_12',
        'sv_prob',

        # 'l1_phi',
        # # 'l1_jet_pt',
        'l1_dz',
        # 'l2_phi',
        # # 'l2_jet_pt',
        'l2_dz',

	# 'hnl_dphi_12',
        # 'hnl_dr_01',
        # 'hnl_dr_02',
        # 'hnl_m_01',
        # 'hnl_m_02',
        # 'hnl_w_vis_m',
        # 'hnl_dphi_hnvis0',
        # 'hnl_2d_disp_sig',

        # 'n_vtx',
        # 'pfmet_pt',
    ]
    return features

def get_branches_nonprompt(features):
    branches = features + [
        'run',
        'lumi',
        'event',
        'weight',
        'lhe_weight',
        'l0_eta',
        'l1_reliso_rho_03',
        'l2_reliso_rho_03',
        # 'hnl_iso03_rel_rhoArea',
        'hnl_hn_vis_eta',
        'hnl_hn_vis_pt',
        'l1_jet_pt',
        'l2_jet_pt',
        # 'l1_pt',
        # 'l2_pt',
        # 'l1_dz',
        # 'l2_dz',
        'l1_phi',
        'l2_phi',
        # 'hnl_m_12',
        # 'l1_dxy',
        # 'l2_dxy',
        # 'l1_eta',
        # 'l2_eta',
    ]
    return branches

def get_features_nonprompt2():
    features = [
        'l0_pt',
        # 'l0_eta',
        # 'l0_dxy',
        # 'l0_dz',

        'l1_pt',
        # 'l1_eta',
        # 'l1_dxy',
        # 'l1_dz',

        'l2_pt',
        # 'l2_eta',
        # 'l2_dxy',
        # 'l2_dz',

        'hnl_2d_disp',
        'hnl_dr_12',
	'hnl_m_12',
        'sv_prob',

        # 'l1_phi',
        # # 'l1_jet_pt',
        # 'l2_phi',
        # # 'l2_jet_pt',

	# 'hnl_dphi_12',
        # 'hnl_dr_01',
        # 'hnl_dr_02',
        # 'hnl_m_01',
        # 'hnl_m_02',
        # 'hnl_w_vis_m',
        # 'hnl_dphi_hnvis0',
        # 'hnl_2d_disp_sig',

        # 'n_vtx',
        # 'pfmet_pt',
    ]
    return features

def get_branches_nonprompt2(features):
    branches = features + [
        'run',
        'lumi',
        'event',
        'weight',
        'lhe_weight',
        'l1_reliso_rho_03',
        'l2_reliso_rho_03',
        # 'hnl_iso03_rel_rhoArea',
        'hnl_hn_vis_eta',
        'hnl_hn_vis_pt',
        'l1_jet_pt',
        'l2_jet_pt',
        # 'l1_pt',
        # 'l2_pt',
        'l0_dz',
        'l1_dz',
        'l2_dz',
        'l1_phi',
        'l2_phi',
        # 'hnl_m_12',
        'l0_dxy',
        'l1_dxy',
        'l2_dxy',
        'l0_eta',
        'l1_eta',
        'l2_eta',
    ]
    return branches

#################################################################################

if __name__ == '__main__':

    ## select here the channel you want to analyze
    channel = 'mmm'    
    # channel = 'eee'    
    # channel = 'eem_OS'
    # channel = 'eem_SS'
    # channel = 'mem_OS'
    # channel = 'mem_SS'


    ## select the dataset 
    # dataset = '2017'
    dataset = '2018'
    
    hostname        = gethostname()

    if dataset == '2017':
        analysis_dir    = '/home/dehuazhu/SESSD/4_production/'
    if dataset == '2018':
        # analysis_dir    = '/mnt/StorageElement1/4_production/2018/'
        # analysis_dir = '/home/dehuazhu/SESSD/4_production/2018/'
        analysis_dir = '/work/dezhu/4_production/2018/'

    pf.setpfstyle()

    # define input parameters
    #The features are the variables your model should depend on
    features_DF  = get_features_DF()
    features_SF1 = get_features_SF1()
    features_SF2 = get_features_SF2()
    features_nonprompt = get_features_nonprompt2()

    #The branches are the variables you want to write in your trees
    branches_DF  = get_branches_DF(get_features_DF())
    branches_SF1 = get_branches_SF1(get_features_SF1())
    branches_SF2 = get_branches_SF2(get_features_SF2())
    branches_nonprompt = get_branches_nonprompt2(get_features_nonprompt2())

    # run train() if you want to train the NeuralNet
    # faketype = 'SingleFake1'
    # faketype = 'SingleFake2'
    # faketype = 'DoubleFake'
    faketype = 'nonprompt'
    

    if faketype == 'SingleFake1':
        features = features_SF1
        branches = branches_SF1
    if faketype == 'SingleFake2':
        features = features_SF2
        branches = branches_SF2
    if faketype == 'DoubleFake':
        features = features_DF
        branches = branches_DF
    if faketype == 'nonprompt':
        features = features_nonprompt
        branches = branches_nonprompt

    path_to_NeuralNet = path_to_NeuralNet(faketype, channel, dataset, hostname) 

    train(
            features,
            branches,
            path_to_NeuralNet,
            newArrays = True,
            faketype = faketype,
            channel = channel,	
            multiprocess = True,
            dataset = dataset,
            analysis_dir = analysis_dir,
            ) 
