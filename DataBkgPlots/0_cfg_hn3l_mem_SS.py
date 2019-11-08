from master.plot_cfg_hn3l import *

dataset          = '2017'
# dataset          = '2018'

promptLeptonType = "mu" # do "ele" or "mu"
L1L2LeptonType   = "em" # do "mm", "me", "ee"
option           = "SS"

producePlots(promptLeptonType, L1L2LeptonType, dataset, option)
