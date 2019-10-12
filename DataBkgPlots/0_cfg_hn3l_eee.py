from master.plot_cfg_hn3l import *

dataset          = '2017'
# dataset          = '2018'

promptLeptonType = "ele" # do "ele" or "mu"
L1L2LeptonType   = "ee" # do "mm", "me", "ee"

producePlots(promptLeptonType, L1L2LeptonType, dataset)
