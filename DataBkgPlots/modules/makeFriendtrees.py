from modules.fr_net import make_all_friendtrees, path_to_NeuralNet
from socket import gethostname
from pdb import set_trace

hostname        = gethostname()
faketype = 'nonprompt'

## select here the channel you want to analyze
channel = 'mmm'    
# channel = 'eee'    
# channel = 'eem_OS'
# channel = 'eem_SS'
# channel = 'mem_OS'
# channel = 'mem_SS'

# dataset = '2017'
dataset = '2018'

if dataset == '2017':
    analysis_dir    = '/home/dehuazhu/SESSD/4_production/'
if dataset == '2018':
    # analysis_dir    = '/mnt/StorageElement1/4_production/2018/'
    # analysis_dir = '/home/dehuazhu/SESSD/4_production/2018/'
    analysis_dir = '/work/dezhu/4_production/2018/'


path_to_NeuralNet = path_to_NeuralNet(faketype, channel, dataset) 

make_all_friendtrees(
        multiprocess = False,
        server = hostname,
        analysis_dir = analysis_dir,
        channel=channel,
        path_to_NeuralNet = path_to_NeuralNet,
        overwrite = False,
        dataset = dataset,
        )
