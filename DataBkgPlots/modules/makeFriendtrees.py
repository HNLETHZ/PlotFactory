from modules.fr_net import make_all_friendtrees, path_to_NeuralNet
from socket import gethostname
from pdb import set_trace

hostname        = gethostname()
analysis_dir    = '/home/dehuazhu/SESSD/4_production/'
faketype = 'nonprompt'

## select here the channel you want to analyze
channel = 'mmm'    
# channel = 'eee'    
# channel = 'eem'
# channel = 'mem'

path_to_NeuralNet = path_to_NeuralNet(faketype, channel) 

make_all_friendtrees(
        multiprocess = True,
        server = hostname,
        analysis_dir = analysis_dir,
        channel=channel,
        path_to_NeuralNet = path_to_NeuralNet,
        overwrite = True,
        )
