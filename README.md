# PlotFactory
PlotFactory is a framework made to quickly generate stadarn plots from HNL NTuples. 
Import plotfactory.py into your python module to use it. 
In plotfactory.py adapt the location you are collecting your Ntuples. 
Don't forget 'HNLGenTreeProducer' & 'HNLTreeProducer'

## setting up the plotting tool

log on the new CentOS 7  machine on the T3
`ssh -XY <USER>@t3ui07.psi.ch`

source a root version > 6.14 (the newer the better and stable)
better write this in your bashscript, WARNING, ONLY WORKS ON CentOS (ie. t3ui07)
`source /cvmfs/sft.cern.ch/lcg/views/LCG_95rc2/x86_64-centos7-gcc8-opt/setup.sh`

mount your eos drive from LXplus
`mkdir ~/eos`
`fusermount -u ~/eos; sshfs -o allow_other,reconnect <USER>@lxplus.cern.ch:/eos/user/<U>/<USER>/ /eos`
DON’T FORGET ANY slashes at the beginning or end!

(if working on t3ui2, use 
`source /cvmfs/sft.cern.ch/lcg/views/LCG_94/x86_64-slc6-gcc8-opt/setup.sh`)

install plotting tool
please install to your home folder! (there will be errors otherweise)
`cd ~; git clone -o ML https://github.com/vinzenzstampf/PlotFactory.git -b dz PlotFactory`
`cd PlotFactory/DataBkgPlots`

compiling root namespaces (for single & double FR weights & cone corrected mass)
run in root:
`.L modules/DDE_doublefake.h+`
`.L modules/DDE_singlefake.h+`
`.L modules/pt_ConeCorrection.h+`
exit root

run the tool
`ipython -i 0_cfg_hn3l_mmm.py`

(if you have to install python modules, to that with 
`pip install <PACKAGE> --user`)
