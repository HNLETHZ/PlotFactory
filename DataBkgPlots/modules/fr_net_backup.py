'''
Resources:
https://en.wikipedia.org/wiki/Universal_approximation_theorem
http://neuralnetworksanddeeplearning.com/chap4.html
https://github.com/thomberg1/UniversalFunctionApproximation
'''

import root_pandas

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from itertools import product

from root_numpy import root2array

from keras.models import Sequential, Model
from keras.layers import Dense, Input
from keras.utils import plot_model
from keras.callbacks import EarlyStopping, Callback
from keras import backend as K
from keras.activations import softmax

from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve, roc_auc_score
       
# fix random seed for reproducibility (FIXME! not really used by Keras)
np.random.seed(1986)

# define input features
features = [
    'ele_pt',
#     'abs(ele_eta)',
#     'abs(ele_dxy)',
#     'abs(ele_dz)',
    'ele_eta',
    'ele_dxy',
#     'ele_dz',
]

branches = features + [
    'ele_genPartFlav',
    'ele_iso',
    'z_eta',
    'z_pt',
    'z_mass',
    'z_phi',
    'ele_dz',
]

filein = 'dy1j_v2.root'

# load dataset including all event, both passing and failing
passing = pd.DataFrame( root2array(filein, 'tree', branches=branches, selection='ele_genPartFlav==0 & ele_iso<2 & ele_iso<0.15') )
failing = pd.DataFrame( root2array(filein, 'tree', branches=branches, selection='ele_genPartFlav==0 & ele_iso<2 & ele_iso>0.15') )

# targets
passing['target'] = np.ones (passing.shape[0]).astype(np.int)
failing['target'] = np.zeros(failing.shape[0]).astype(np.int)

# concatenate the events and shuffle
data = pd.concat([passing, failing])
data = data.sample(frac=1, replace=True, random_state=1986) # shuffle

# X and Y
X = pd.DataFrame(data, columns=branches)
Y = pd.DataFrame(data, columns=['target'])

# define the net
input  = Input((len(features),))
# dense1 = Dense(64, activation='tanh'   , name='dense1')(input )
dense1 = Dense(64, activation='relu'   , name='dense1')(input )
output = Dense( 1, activation='sigmoid', name='output')(dense1)
# output = Dense( 1, activation='softmax', name='output')(dense1)

# Define outputs of your model
model = Model(input, output)

# compile and choose your loss function (binary cross entropy for a 1-0 classification problem)
model.compile('Adam', loss='binary_crossentropy')

# print net summary
print model.summary()

# plot the models
# https://keras.io/visualization/
plot_model(model, show_shapes=True, show_layer_names=True, to_file='model.png')

# normalize inputs FIXME! do it, but do it wisely
# https://scikit-learn.org/stable/auto_examples/preprocessing/plot_all_scaling.html#sphx-glr-auto-examples-preprocessing-plot-all-scaling-py
from sklearn.preprocessing import QuantileTransformer
xx = QuantileTransformer(output_distribution='normal').fit_transform(X[features])
# alternative way to scale the inputs
# https://datascienceplus.com/keras-regression-based-neural-networks/

# train, give the classifier a head start
# early stopping
es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=20, restore_best_weights=True)

# train only the classifier. beta is set at 0 and the discriminator is not trained
# history = model.fit(X[features], Y, epochs=500, validation_split=0.5, callbacks=[es])  
history = model.fit(xx, Y, epochs=1000, validation_split=0.5, callbacks=[es])  

# plot loss function trends for train and validation sample
plt.plot(history.history['loss'], label='train')
plt.plot(history.history['val_loss'], label='test')
plt.legend()
plt.savefig('loss_function_history.pdf')
plt.clf()

# calculate predictions on the data sample
print 'predicting on', data.shape[0], 'events'
x = pd.DataFrame(data, columns=features)
# y = model.predict(x)
xx = QuantileTransformer(output_distribution='normal').fit_transform(x[features])
y = model.predict(xx)

# impose norm conservation if you want probabilities
# compute the overall rescaling factor scale
scale = 1.
# scale = np.sum(passing['target']) / np.sum(y)

# add the score to the data sample
data.insert(len(data.columns), 'weight', scale * y)

# let sklearn do the heavy lifting and compute the ROC curves for you
fpr, tpr, wps = roc_curve(data.target, data.weight) 
plt.plot(fpr, tpr)
plt.savefig('roc.pdf')

# save model and weights
model.save('net_model.h5')
# model.save_weights('net_model_weights.h5')

# rename branches, if you want
# data.rename(
#     index=str, 
#     columns={'cand_refit_mass12': 'mass12',}, 
#     inplace=True)

# save ntuple
data.to_root('output_ntuple.root', key='tree', store_index=False)

