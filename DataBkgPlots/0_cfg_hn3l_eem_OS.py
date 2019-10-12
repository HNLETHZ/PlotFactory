from master.plot_cfg_hn3l import *

dataset          = '2017'
# dataset          = '2018'

promptLeptonType = "ele" # do "ele" or "mu"
L1L2LeptonType   = "em" # do "mm", "me", "ee"
dataset          = '2017'
option           = "OS"

producePlots(promptLeptonType, L1L2LeptonType, dataset, option)
