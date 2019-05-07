from master.plot_cfg_hn3l import *

promptLeptonType = "mu" # do "ele" or "mu"
L1L2LeptonType   = "em" # do "mm", "me", "ee"
server           = "starseeker" # do "t3" or "lxplus" or "starseeker"
multiprocess     = True

# producePlots(promptLeptonType = promptLeptonType, L1L2LeptonType = L1L2LeptonType)
producePlots(promptLeptonType, L1L2LeptonType, server)
