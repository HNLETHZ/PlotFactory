#Set the location where all ntuples are stored. Adapt the location to your path
def getntupdir():
    # ntup_dir = '/afs/cern.ch/user/d/dezhu/workspace/public/ntuples/201804_HNL/' # location on lxplus
    # ntup_dir = '/afs/cern.ch/user/d/dezhu/workspace/public/ntuples/201805_HNL/' # location on lxplus
    # ntup_dir = '/eos/user/m/manzoni/HNL/gentuple_050318_v4/' # first version from riccardo
    # ntup_dir = '/Users/dehuazhu/Dropbox/PhD/5_Projects/analysis/180419_NTuples/201804_HN3L/' # location on local machine
    # ntup_dir = '/eos/user/d/dezhu/HNL/ntuple/20180608_HNLreco/ntuple/' # global
    # ntup_dir = '/afs/cern.ch/work/v/vstampf/public/ntuples/cherry1/' # around 700k evts cherry1
    # ntup_dir = '/eos/user/v/vstampf/public/ntuples/reco_v613/' # latest (6/14) ntuples
    ntup_dir = '/afs/cern.ch/work/v/vstampf/public/ntuples/gen_v1_refurbshd/' # latest (6/21) ntuples
    # ntup_dir = '/afs/cern.ch/work/v/vstampf/public/ntuples/gen_v622/' # latest (6/22) new update
    return ntup_dir
