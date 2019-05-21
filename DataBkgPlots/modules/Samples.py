import os
import pickle

import ROOT
from ROOT import gSystem, gROOT
from collections import OrderedDict

from pdb import set_trace

from modules.PlotConfigs import SampleCfg, HistogramCfg

# from modules.samples_mc_2017_noskim   import TTJets, WJetsToLNu, WJetsToLNu_ext, ZZZ, WZZ, WWZ, WWW, WWTo2L2Nu, WGGJets, TTWJetsToLNu, TTZToLL_M10, TTZToLL_M1to10, ST_sch_lep, STbar_tch_inc, ST_tch_inc, STbar_tW_inc, ST_tW_inc, DYBB, DYJetsToLL_M10to50,DYJetsToLL_M50, DYJetsToLL_M50_ext, DY1JetsToLL_M50, DY2JetsToLL_M50, DY2JetsToLL_M50_ext, DY3JetsToLL_M50, DY3JetsToLL_M50_ext, WW, WZ, ZZ, QCD_pt_15to20_mu, QCD_pt_20to30_mu, QCD_pt_30to50_mu, QCD_pt_50to80_mu, QCD_pt_80to120_mu

# from modules.samples_data_2017_noskim import Single_ele_2017B, Single_ele_2017C, Single_ele_2017D, Single_ele_2017E, Single_ele_2017F, Single_mu_2017B,  Single_mu_2017C,  Single_mu_2017D,  Single_mu_2017E,  Single_mu_2017F



def createSampleLists(analysis_dir='', 
                      server='t3',
                      channel='mmm',
                      signal_scale=0.09,#27.0,#200.0,#0.09,
                      no_data=True,
                      tree_prod_name='HNLTreeProducer', 
                      add_data_cut=None,
                      add_mc_cut=None):
    
    if channel == 'emm':
#        data_dir = '/eos/user/m/manzoni/HNL/singleele_e_23_08_2018/'              # first version
        # data_dir = '/eos/user/v/vstampf/ntuples/data_2017_e_noskim/partial_hadd/'  # 9/13 production including met filters and masses between vetoing leps and 3l
        if server == 'lxplus':
            data_dir = '/eos/user/v/vstampf/ntuples/data_2017_e_noskim/'
            bkg_dir = 'bkg_mc_e/'
            sig_dir = 'sig_mc_e/ntuples/'
            DY_dir  = '/eos/user/v/vstampf/ntuples/DDE_v0/prompt_e/'
        if server == 't3':
            data_dir = analysis_dir + 'data/'
            bkg_dir = 'background'
            sig_dir = 'signal'
            # DY_dir  = '/eos/user/v/vstampf/ntuples/DDE_v0/prompt_e/'
        dataB_name = 'Single_ele_2017B'; dataC_name = 'Single_ele_2017C'; dataD_name = 'Single_ele_2017D'; dataE_name = 'Single_ele_2017E'; dataF_name = 'Single_ele_2017F'; 

    if channel == 'mmm':
        if server == 'lxplus':
            data_dir = '/eos/user/v/vstampf/ntuples/data_2017_m_noskim/'
            bkg_dir = 'bkg_mc_m/'
            sig_dir = 'sig_mc_m/ntuples/'
            DY_dir = analysis_dir + bkg_dir
        if server == 't3':
            # data_dir = analysis_dir + 'data/'
            # data_dir = 'root://t3dcachedb.psi.ch:1094///pnfs/psi.ch/cms/trivcat/store/user/dezhu/2_ntuples/HN3Lv2.0/mmm/data/'
            data_dir = analysis_dir + 'production_20190411_Data_mmm/ntuples'
            bkg_dir = 'production_20190411_Bkg_mmm/ntuples/'
            sig_dir = 'signal/ntuples'
            DY_dir = analysis_dir + bkg_dir
        if server == 'starseeker':
            data_dir = analysis_dir+'production_20190411_Data_mmm/ntuples'
            bkg_dir = 'production_20190411_Bkg_mmm/ntuples/'
            # bkg_dir = 'production_20190306_BkgMC/mmm/ntuples/'
            sig_dir = 'signal/ntuples'
            DY_dir = analysis_dir + bkg_dir
        dataB_name = 'Single_mu_2017B'; dataC_name = 'Single_mu_2017C'; dataD_name = 'Single_mu_2017D'; dataE_name = 'Single_mu_2017E'; dataF_name = 'Single_mu_2017F'; 

    if channel == 'mem':
        if server == 'lxplus':
            data_dir = '/eos/user/v/vstampf/ntuples/data_2017_m_noskim/'
            bkg_dir = 'bkg_mc_m/'
            sig_dir = 'sig_mc_m/ntuples/'
            DY_dir = analysis_dir + bkg_dir
        if server == 't3':
            # data_dir = analysis_dir + 'data/'
            # data_dir = 'root://t3dcachedb.psi.ch:1094///pnfs/psi.ch/cms/trivcat/store/user/dezhu/2_ntuples/HN3Lv2.0/mmm/data/'
            data_dir = '/work/dezhu/4_production/vinz'
            bkg_dir = 'vinz/'
            # bkg_dir = 'production_20190306_BkgMC/mmm/ntuples/'
            sig_dir = 'signal/ntuples'
            DY_dir = analysis_dir + bkg_dir
        if server == 'starseeker':
            # data_dir = '/mnt/StorageElement1/4_production/production_20190411_Data_mmm/ntuples'
            data_dir = '/mnt/StorageElement1/4_production/vinz/'
            bkg_dir = 'vinz/'
            sig_dir = 'signal/ntuples'
            DY_dir = analysis_dir + bkg_dir
        dataB_name = 'Single_mu_2017B'; dataC_name = 'Single_mu_2017C'; dataD_name = 'Single_mu_2017D'; dataE_name = 'Single_mu_2017E'; dataF_name = 'Single_mu_2017F'; 

   
    #Temporal data 
    samples_data = [
        SampleCfg(name='data_2017B', dir_name=dataB_name, ana_dir=data_dir, tree_prod_name=tree_prod_name, is_data=True, norm_cut=add_data_cut),                                         #nevents =  5265969 
        SampleCfg(name='data_2017C', dir_name=dataC_name, ana_dir=data_dir, tree_prod_name=tree_prod_name, is_data=True, norm_cut=add_data_cut),                                         #nevents = 10522062 
        SampleCfg(name='data_2017D', dir_name=dataD_name, ana_dir=data_dir, tree_prod_name=tree_prod_name, is_data=True, norm_cut=add_data_cut),                                           #nevents =  3829353
        SampleCfg(name='data_2017E', dir_name=dataE_name, ana_dir=data_dir, tree_prod_name=tree_prod_name, is_data=True, norm_cut=add_data_cut),                                         #nevents = 10926946 
        SampleCfg(name='data_2017F', dir_name=dataF_name, ana_dir=data_dir, tree_prod_name=tree_prod_name, is_data=True, norm_cut=add_data_cut),                                         #nevents = 19122658 ; SUM of BCDEF = 49'666'988
    ]

    samples_dataF = [
        SampleCfg(name='data_2017F', dir_name=dataF_name, ana_dir=data_dir, tree_prod_name=tree_prod_name, is_data=True, norm_cut=add_data_cut),                                         #nevents = 19122658 ; SUM of BCDEF = 49'666'988
    ]

    samples_TTJets = [
            SampleCfg(name='TTJets', 
                dir_name='TTJets', 
                ana_dir=analysis_dir+bkg_dir, 
                tree_prod_name=tree_prod_name, 
                xsec=831.76, 
                # sumweights=TTJets.nGenEvents, 
                sumweights=None, 
                is_MC=True),
            ]

    samples_WJets = [
            SampleCfg(name='WJetsToLNu', 
                dir_name='WJetsToLNu', 
                ana_dir=analysis_dir+bkg_dir, 
                tree_prod_name=tree_prod_name, 
                xsec=59850, 
                sumweights=None, 
                is_MC=True),
            SampleCfg(name='WJetsToLNu_ext', 
                dir_name='WJetsToLNu_ext', 
                ana_dir=analysis_dir+bkg_dir, 
                tree_prod_name=tree_prod_name, 
                xsec=59850, 
                sumweights=76666716, 
                is_MC=True),
            ]

    samples_DYBB = [
            SampleCfg(name='DYBB', 
                dir_name='DYBB', 
                ana_dir='/work/dezhu/4_production/production_20190306_BkgMC/mmm/ntuples/', 
                tree_prod_name=tree_prod_name, 
                xsec=1.459e+01, 
                sumweights=None, 
                is_DY=True),
            ]

    samples_DY = [
            SampleCfg(name='DYJetsToLL_M10to50',
                dir_name='DYJetsToLL_M10to50', 
                ana_dir=analysis_dir+bkg_dir, 
                tree_prod_name=tree_prod_name, 
                xsec=18610.0, 
                sumweights=None, 
                is_MC=True,
                is_DY=True),
            SampleCfg(name='DYJets_M50', 
                dir_name='DYJetsToLL_M50', 
                ana_dir=analysis_dir+bkg_dir, 
                tree_prod_name=tree_prod_name, 
                xsec=2075.14*3, 
                sumweights=None, 
                is_MC=True,
                is_DY=True),
            SampleCfg(name='DYJets_M50_ext', 
                dir_name='DYJetsToLL_M50_ext', 
                ana_dir=analysis_dir+bkg_dir, 
                tree_prod_name=tree_prod_name, 
                xsec=2075.14*3, 
                sumweights=None, 
                is_MC=True,
                is_DY=True),
            ]

    samples_Diboson = [
            SampleCfg(name='ZZ', 
                dir_name='ZZ', 
                ana_dir=analysis_dir+bkg_dir, 
                tree_prod_name=tree_prod_name, 
                xsec=12.14, 
                sumweights=None, 
                is_MC=True),
            SampleCfg(name='WZ', 
                dir_name='WZ', 
                ana_dir=analysis_dir+bkg_dir, 
                tree_prod_name=tree_prod_name, 
                xsec=27.6, 
                sumweights=None, 
                is_MC=True),
            SampleCfg(name='WW', 
                dir_name='WW', 
                ana_dir=analysis_dir+bkg_dir, 
                tree_prod_name=tree_prod_name, 
                xsec=75.88, 
                sumweights=None, 
                is_MC=True),
            ]

    samples_SingleTop = [
            SampleCfg(name='ST_sch_lep', 
                dir_name='ST_sch_lep', 
                ana_dir=analysis_dir+bkg_dir, 
                tree_prod_name=tree_prod_name, 
                xsec=3.68, 
                sumweights=None, 
                is_MC=True),
            SampleCfg(name='ST_tch_inc', 
                dir_name='ST_tch_inc', 
                ana_dir=analysis_dir+bkg_dir, 
                tree_prod_name=tree_prod_name, 
                xsec=44.07, 
                sumweights=None, 
                is_MC=True),
            SampleCfg(name='STbar_tch_inc', 
                dir_name='STbar_tch_inc', 
                ana_dir=analysis_dir+bkg_dir, 
                tree_prod_name=tree_prod_name, 
                xsec=26.23, 
                sumweights=None, 
                is_MC=True),
            ]

    samples_conversion = [
            SampleCfg(name='Conversion_DYJets_M50_ext', 
                dir_name='DYJetsToLL_M50_ext', 
                ana_dir=analysis_dir+bkg_dir, 
                # ana_dir='/work/dezhu/4_production/production_20190411_Bkg_mmm/ntuples', 
                # ana_dir='root://t3dcachedb.psi.ch:1094///pnfs/psi.ch/cms/trivcat/store/user/dezhu/2_ntuples/HN3Lv2.0/mmm/background/montecarlo/production_20190318_BkgMC', 
                tree_prod_name=tree_prod_name, 
                xsec=2075.14*3, 
                # sumweights=DYJetsToLL_M50_ext.nGenEvents, 
                # sumweights=133395135, 
                sumweights=None, 
                is_MC=True,
                is_MC_Conversions=True),
            ]

    samples_Triboson = [
            SampleCfg(name='ZZZ', 
                dir_name='ZZZ', 
                ana_dir=analysis_dir+bkg_dir, 
                tree_prod_name=tree_prod_name, 
                xsec=0.01398, 
                sumweights=None, 
                is_MC=True),
            SampleCfg(name='WZZ', 
                dir_name='WZZ', 
                ana_dir=analysis_dir+bkg_dir, 
                tree_prod_name=tree_prod_name, 
                xsec=0.05565, 
                sumweights=None, 
                is_MC=True),
            SampleCfg(name='WWZ', 
                dir_name='WWZ', 
                ana_dir=analysis_dir+bkg_dir, 
                tree_prod_name=tree_prod_name, 
                xsec=0.1651, 
                sumweights=None, 
                is_MC=True),
            SampleCfg(name='WWW', 
                dir_name='WWW', 
                ana_dir=analysis_dir+bkg_dir, 
                tree_prod_name=tree_prod_name, 
                xsec=0.2086, 
                sumweights=None, 
                is_MC=True),
            ]
    
    samples_QCD = [
            SampleCfg(name='QCD_pt_15to20_mu', 
                dir_name='QCD_pt_15to20_mu', 
                ana_dir=analysis_dir+bkg_dir, 
                tree_prod_name=tree_prod_name, 
                xsec=2.798e+06, 
                sumweights=None, 
                is_MC=True),
            SampleCfg(name='QCD_pt_20to30_mu', 
                dir_name='QCD_pt_20to30_mu', 
                ana_dir=analysis_dir+bkg_dir, 
                tree_prod_name=tree_prod_name, 
                xsec=2.533e+06, 
                sumweights=None, 
                is_MC=True),
            SampleCfg(name='QCD_pt_30to50_mu', 
                dir_name='QCD_pt_30to50_mu', 
                ana_dir=analysis_dir+bkg_dir, 
                tree_prod_name=tree_prod_name, 
                xsec=1.375e+06, 
                sumweights=None, 
                is_MC=True),
            SampleCfg(name='QCD_pt_50to80_mu', 
                dir_name='QCD_pt_50to80_mu', 
                ana_dir=analysis_dir+bkg_dir, 
                tree_prod_name=tree_prod_name, 
                xsec=3.770e+05, 
                sumweights=None, 
                is_MC=True),
            SampleCfg(name='QCD_pt_80to120_mu', 
                dir_name='QCD_pt_80to120_mu', 
                ana_dir=analysis_dir+bkg_dir, 
                tree_prod_name=tree_prod_name, 
                xsec=8.880e+04, 
                sumweights=None, 
                is_MC=True),
            ]

    samples_singlefake = [
        SampleCfg(name='singlefake_B', dir_name=dataB_name, ana_dir=data_dir, tree_prod_name=tree_prod_name, is_data=False, is_singlefake=True, norm_cut=add_data_cut),                                         #nevents =  5265969 
        # SampleCfg(name='singlefake_C', dir_name=dataC_name, ana_dir=data_dir, tree_prod_name=tree_prod_name, is_data=False, is_singlefake=True, norm_cut=add_data_cut),                                         #nevents = 10522062 
        # SampleCfg(name='singlefake_D', dir_name=dataD_name, ana_dir=data_dir, tree_prod_name=tree_prod_name, is_data=False, is_singlefake=True, norm_cut=add_data_cut),                                           #nevents =  3829353
        # SampleCfg(name='singlefake_E', dir_name=dataE_name, ana_dir=data_dir, tree_prod_name=tree_prod_name, is_data=False, is_singlefake=True, norm_cut=add_data_cut),                                         #nevents = 10926946 
        # SampleCfg(name='singlefake_F', dir_name=dataF_name, ana_dir=data_dir, tree_prod_name=tree_prod_name, is_data=False, is_singlefake=True, norm_cut=add_data_cut),                                         #nevents = 19122658 ; SUM of BCDEF = 49'666'988
    ]

    samples_doublefake = [
        SampleCfg(name='doublefake_B', dir_name=dataB_name, ana_dir=data_dir, tree_prod_name=tree_prod_name, is_data=False, is_doublefake=True, norm_cut=add_data_cut),                                         #nevents =  5265969 
        SampleCfg(name='doublefake_C', dir_name=dataC_name, ana_dir=data_dir, tree_prod_name=tree_prod_name, is_data=False, is_doublefake=True, norm_cut=add_data_cut),                                         #nevents = 10522062 
        SampleCfg(name='doublefake_D', dir_name=dataD_name, ana_dir=data_dir, tree_prod_name=tree_prod_name, is_data=False, is_doublefake=True, norm_cut=add_data_cut),                                           #nevents =  3829353
        SampleCfg(name='doublefake_E', dir_name=dataE_name, ana_dir=data_dir, tree_prod_name=tree_prod_name, is_data=False, is_doublefake=True, norm_cut=add_data_cut),                                         #nevents = 10926946 
        SampleCfg(name='doublefake_F', dir_name=dataF_name, ana_dir=data_dir, tree_prod_name=tree_prod_name, is_data=False, is_doublefake=True, norm_cut=add_data_cut),                                         #nevents = 19122658 ; SUM of BCDEF = 49'666'988
    ]




    samples_mc =  samples_DY + samples_WJets + samples_TTJets + samples_Diboson + samples_SingleTop
    # samples_bkg = samples_mc + samples_singlefake + samples_doublefake 
    # samples_bkg = samples_doublefake
    samples_bkg = samples_mc 
    samples_all = samples_bkg + samples_data
    # samples_all = samples_TTJets
    # samples_all = samples_DY + samples_TTJets 

    return samples_all, samples_singlefake, samples_doublefake


def getSumWeight(sample, weight_dir='SkimAnalyzerCount', norm=True):
    sumNormWeights_file_dir = '/'.join([sample.ana_dir, sample.dir_name, weight_dir, 'SkimReport.txt'])
    try:
        sumNormWeights_file = open(sumNormWeights_file_dir,'rt')
        if sumNormWeights_file.mode == 'rt':
            f1 = sumNormWeights_file.readlines()
            for i,l in enumerate(f1):
                if f1[i].find('Sum Norm Weights') != -1: 
                    return float(f1[i].split()[3])
    except:
        print 'Warning: could not find sum weights information or the following file does not even exist: %s'%(sumNormWeights_file_dir)
        set_trace()

def setSumWeights(samples, weight_dir='SkimAnalyzerCount', norm=True):
    print '###########################################################'
    print '# setting sum weights for the samples...'
    print '###########################################################'
    print ''

    
    for sample in samples:
        try:
            if isinstance(sample, HistogramCfg) or sample.is_data:
                continue
        except:
            set_trace()

        if sample.name == 'DYJets_M50' or sample.name == 'DYJets_M50_ext':
            sample_DYJets_M50        = [s for s in samples if s.name == 'DYJets_M50'    ][0]
            sample_DYJets_M50_ext    = [s for s in samples if s.name == 'DYJets_M50_ext'][0]
            sumweight_DYJets_M50     = getSumWeight(sample_DYJets_M50)
            sumweight_DYJets_M50_ext = getSumWeight(sample_DYJets_M50_ext) 
            sample.sumweights = sumweight_DYJets_M50 + sumweight_DYJets_M50_ext 

        elif sample.name == 'WJetsToLNu' or sample.name == 'WJetsToLNu_ext':
            sample_WJetsToLNu        = [s for s in samples if s.name == 'WJetsToLNu'    ][0]
            sample_WJetsToLNu_ext    = [s for s in samples if s.name == 'WJetsToLNu_ext'][0]
            sumweight_WJetsToLNu     = getSumWeight(sample_WJetsToLNu)
            sumweight_WJetsToLNu_ext = getSumWeight(sample_WJetsToLNu_ext) 
            sample.sumweights = sumweight_WJetsToLNu + sumweight_WJetsToLNu_ext 

        else:
            sample.sumweights = getSumWeight(sample, weight_dir, norm)

        print 'Sum weights from sample',sample.name, 'taken from SkimReport.txt file. Setting it to', sample.sumweights

    return samples
