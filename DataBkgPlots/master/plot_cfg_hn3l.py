import copy
import os
from collections import namedtuple
from operator import itemgetter
from ROOT import gROOT as gr
from multiprocessing import Pool, Process, cpu_count

from shutil import copyfile, copytree
from numpy import array
from getpass import getuser
import time

from copy_reg import pickle       # to pickle methods for multiprocessing
from types    import MethodType   # to pickle methods for multiprocessing

from modules.PlotConfigs import HistogramCfg, VariableCfg
# from modules.HistCreator import CreateHists
from modules.HistCreator_df import CreateHists
from modules.HistDrawer import HistDrawer
from modules.Variables import hnl_vars, test_vars, getVars,dde_vars
from modules.Selections import getSelection, Region
from modules.Samples import createSampleLists, setSumWeights
from pdb import set_trace
# from CMGTools.HNL.plotter.qcdEstimationMSSMltau import estimateQCDWMSSM, createQCDWHistograms



def _pickle_method(method): 
    func_name = method.im_func.__name__
    obj = method.im_self
    cls = method.im_class
    return _unpickle_method, (func_name, obj, cls)

def _unpickle_method(func_name, obj, cls):
    for cls in cls.mro():
        try:
            func = cls.__dict__[func_name]
        except KeyError:
            pass
        else:
            break
    return func.__get__(obj, cls)

pickle(MethodType, _pickle_method, _unpickle_method)

gr.SetBatch(True) # NEEDS TO BE SET FOR MULTIPROCESSING OF plot.Draw()

# get the lumis from here: https://twiki.cern.ch/twiki/bin/viewauth/CMS/PdmV2017Analysis
int_lumi = 41530.0 # pb ### (all eras), Golden JSON Int.Lumi: from https://twiki.cern.ch/twiki/bin/viewauth/CMS/PdmVAnalysisSummaryTable 
# int_lumi =  4792.0 # pb (era B)



def prepareRegions(channel):
    regions = []
    # regions.append(Region('SR','mmm','SR'))
    regions.append(Region('DY','mmm','CR_DY'))
    # regions.append(Region('ttbar','mem','CR_ttbar'))

    print('###########################################################')
    print('# setting analysis regions')
    print('###########################################################')
   

    for region in regions: 
        print 'region: %s; channel: %s'%(region.name,region.channel)
        print 'baseline: %s\n'%(region.baseline)

    return regions

def createSamples(channel, analysis_dir, total_weight, server, add_data_cut=None):
    sample_dict = {}
    # print "creating samples from %s"%(analysis_dir)
    samples_all = createSampleLists(analysis_dir=analysis_dir, server = server, channel=channel, add_data_cut=add_data_cut)

    #select here the samples you wish to use
    # working_samples = samples_data_dde
    working_samples = samples_all
    working_samples = setSumWeights(working_samples)
    sample_dict['working_samples'] = working_samples
    print ''

    #TODO implement a code to print the samples
    print('###########################################################')
    print'# %d samples to be used:'%(len(working_samples))
    print('###########################################################')
    for w in working_samples: print('{:<20}{:<20}'.format(*[w.name,('path: '+w.ana_dir)]))

    return sample_dict

def createVariables(rebin=None):
    # Taken from Variables.py; can get subset with e.g. getVars(['mt', 'mvis'])
#    variables = CR_vars
    DoNotRebin = ['_norm_', 'n_vtx', 'nj', 'nbj',] 
    variables = hnl_vars
    # variables = dde_vars
    variables = test_vars
    if rebin>0:
        for ivar in hnl_vars:
            if ivar.name in DoNotRebin: continue
            ivar.binning['nbinsx'] = int(ivar.binning['nbinsx']/rebin)

    return variables

def makePlots(plotDir,channel_name,variables, regions, total_weight, sample_dict, make_plots=True, create_trees=False, multiprocess=False, dataframe=True):
    ams_dict = {}
    sample_names = set()
    for region in regions:
        regionDir = plotDir+region.name
        if not os.path.exists(regionDir):
            os.mkdir(regionDir)
            print "Output directory created. "
            print "Output directory: %s"%(regionDir)
        else:
            # print "Output directory: ", regionDir, "already exists, overwriting it!"
            print "Output directory already exists, overwriting it! "
            print "Output directory: %s"%(regionDir)
            os.system("rm -rf %s"%(regionDir))
            os.system("mkdir %s"%(regionDir))

        cfg_main = HistogramCfg(name=region.name, var=None, cfgs=sample_dict['working_samples'], region=region, lumi=int_lumi, weight=total_weight)

        print('\n###########################################################')
        print('# creating plots for %i sample(s) and %i variable(s)...'%(len(sample_dict['working_samples']),len(variables),))
        print('# using %d CPUs'%(cpu_count()))
        print('###########################################################')
        
        i_var = 0
        start_plots = time.time()
        for var in variables:
            i_var += 1
            print '\nPlotting variable \'%s\' (%d of %d; total time passed: %.1f s)...'%(var.name,i_var,len(variables),time.time()-start_plots)
            start_plot = time.time()
            cfg_main.vars = [var]
            HISTS = CreateHists(cfg_main)
            plots = HISTS.createHistograms(cfg_main, verbose=False, multiprocess = multiprocess)
            plot = plots[var.name]
            plot.Group('data_obs', ['data_2017B', 'data_2017C', 'data_2017D', 'data_2017E', 'data_2017F'])
            plot.Group('Diboson', ['WZTo3LNu','ZZTo4L','WW','WZ','ZZ'])
            plot.Group('Single t', ['STbar_tch_inc','ST_tch_inc','ST_sch_lep'])
            plot.Group('DY', ['DYJets_M50_ext','DYJets_M50','DYJetsToLL_M10to50'])
            # plot.Group('Conversions', ['Conversion_DYJets_M50_ext','Conversion_DYJets_M50','Conversion_DYJetsToLL_M10to50'])
            plot.Group('QCD',['QCD_pt_15to20_mu', 'QCD_pt_20to30_mu', 'QCD_pt_30to50_mu', 'QCD_pt_50to80_mu', 'QCD_pt_80to120_mu'])
            plot.Group('WJets', ['WJetsToLNu','WJetsToLNu_ext','W1JetsToLNu', 'W2JetsToLNu', 'W3JetsToLNu', 'W4JetsToLNu'])
            if make_plots:
                HistDrawer.draw(plot, channel = channel_name, plot_dir = plotDir+region.name)
            print'\tThis plot took %.1f s to compute.'%(time.time()-start_plot)


def producePlots(promptLeptonType, L1L2LeptonType, server, multiprocess = False, dataframe = True):
    start_time = time.time()

    usr = getuser()

    if server == 't3':
        if usr == 'dezhu':   plotDirBase = '/work/dezhu/3_figures/1_DataMC/FinalStates/'
        if usr == 'vstampf': plotDirBase = '/t3home/vstampf/eos/plots/'

    if server == 'lxplus':
        if usr == 'dezhu':   plotDirBase = '/eos/user/d/dezhu/HNL/plots/FinalStates/'
        if usr == 'vstampf': plotDirBase = '/eos/user/v/vstampf/plots/'

    if server == 'starseeker':
        if usr == 'dehuazhu': plotDirBase = '/mnt/StorageElement1/3_figures/1_DataMC/FinalStates/'

    if promptLeptonType == "ele":
        channel_name = 'e'
        if L1L2LeptonType == "ee":
            plotDir = plotDirBase + 'eee/'
            channel_name += 'ee'
            channel = 'eee'
        if L1L2LeptonType == "em":
            plotDir = plotDirBase + 'eem/'
            channel_name += 'e#mu'
            channel = 'eem'
        if L1L2LeptonType == "mm":
            plotDir = plotDirBase + 'emm/'
            channel_name += '#mu#mu'
            channel = 'emm'
    if promptLeptonType == "mu":
        channel_name = '#mu'
        if L1L2LeptonType == "ee":
            plotDir = plotDirBase + 'mee/'
            channel_name += 'ee'
            channel = 'mee'
        if L1L2LeptonType == "em":
            plotDir = plotDirBase + 'mem/'
            channel_name += 'e#mu'
            channel = 'mem'
        if L1L2LeptonType == "mm":
            plotDir = plotDirBase + 'mmm/'
            channel_name += '#mu#mu'
            channel = 'mmm'
    
    if server == "lxplus":
        analysis_dir = '/eos/user/v/vstampf/ntuples/'
   
    if server == "t3":
        # analysis_dir = 'root://t3dcachedb.psi.ch:1094///pnfs/psi.ch/cms/trivcat/store/user/dezhu/2_ntuples/HN3Lv1.0/' + channel + '/'
        analysis_dir = '/work/dezhu/4_production/'

    if server == "starseeker":
        # analysis_dir = '/mnt/StorageElement1/4_production/'
        analysis_dir = '/home/dehuazhu/SESSD/4_production/'

    total_weight = 'weight * lhe_weight'
    # total_weight = '1'


    regions = prepareRegions(channel)
    

    # variables = createVariables(rebin = 2.5)
    variables = createVariables()

    sample_dict = createSamples(channel,analysis_dir, total_weight, server=server)

    handle = os.popen('echo $CMSSW_BASE')
    line = handle.read()
    handle.close()
    cmsBaseDir = line.strip('\n')

    
    makePlots(
        plotDir,
        channel_name,
        variables, 
        regions, 
        total_weight, 
        sample_dict, 
        make_plots=True,
        multiprocess=multiprocess,
        dataframe=dataframe
    )


    for i in regions:
        copyfile(cmsBaseDir+'/src/CMGTools/HNL/PlotFactory/DataBkgPlots/0_cfg_hn3l_'+channel+'.py', plotDir+i.name+'/plot_cfg.py')
        copyfile(cmsBaseDir+'/src/CMGTools/HNL/PlotFactory/DataBkgPlots/master/plot_cfg_hn3l.py', plotDir+i.name+'/plot_cfg_base.py')
        copyfile(cmsBaseDir+'/src/CMGTools/HNL/PlotFactory/DataBkgPlots/modules/Selections.py', plotDir+i.name+'/Selections.py')
        print '\ncfg file stored in "', plotDir + i.name + '/plot_cfg.py"'
        print 'cfg_base file stored in "', plotDir + i.name + '/plot_cfg_base.py"'
        # os.system("cp -rf %s %s"%(plotDir+i.name,'/home/dehuazhu/t3work/3_figures/1_DataMC/FinalStates/mmm/'+i.name)) 
        if server == "starseeker":
            print 'copying the plots from starseeker to T3'
            os.system("cp -rf %s %s"%(plotDir+i.name,'/home/dehuazhu/t3work/3_figures/1_DataMC/FinalStates/'+channel+'/'))
            print 'directory %s copied to /t3home/dezhu/eos/t3/figures/1_DataMC/FinalStates/%s!'%(i.name,channel)

    end_time = time.time()
    print('This job took %.1f seconds to compute.'%(end_time-start_time))
