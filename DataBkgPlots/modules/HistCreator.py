import hashlib
from multiprocessing import Pool, Process, cpu_count
# from multiprocessing.dummy import Pool, Process, cpu_count

from array import array
import numpy as np
import time
from modules.PlotConfigs import HistogramCfg
from modules.DataMCPlot import DataMCPlot
from modules.DDE import DDE
from modules.binning import binning_dimuonmass
from modules.nn import run_nn 
import modules.fr_net as fr_net
# from CMGTools.RootTools.DataMC.Histogram import Histogram
from pdb import set_trace

from ROOT import ROOT, RDataFrame, TH1F, TFile, TTree, TTreeFormula, gInterpreter, gROOT, gSystem

# Enable ROOT's implicit multi-threading for all objects that provide an internal parallelisation mechanism
ROOT.EnableImplicitMT()

def initHist(hist, vcfg):
    hist.Sumw2()
    xtitle = vcfg.xtitle
    if vcfg.unit:
        xtitle += ' ({})'.format(vcfg.unit)
    hist.GetXaxis().SetTitle(xtitle)
    hist.SetStats(False)

class CreateHists(object):
    def __init__(self, hist_cfg, analysis_dir = '/home/dehuazhu/SESSD/4_production/', channel = 'mmm', server = 'starseeker', useNeuralNetwork=False):
        self.analysis_dir = analysis_dir
        self.channel = channel
        self.server = server
        self.hist_cfg = hist_cfg
        self.useNeuralNetwork = useNeuralNetwork
        if self.hist_cfg.vars:
            self.vcfgs = hist_cfg.vars

        if not self.vcfgs:
            print 'ERROR in createHistograms: No variable configs passed', self.hist_cfg.name

        self.plots = {}

        for vcfg in self.vcfgs:
            plot = DataMCPlot(vcfg.name,vcfg.xtitle)
            plot.lumi = hist_cfg.lumi
            if vcfg.name in self.plots:
                print 'Adding variable with same name twice', vcfg.name, 'not yet foreseen; taking the last'
            self.plots[vcfg.name] = plot

    def createHistograms(self, hist_cfg, all_stack=False, verbose=False,  vcfgs=None, multiprocess = True, useNeuralNetwork = False):
        if multiprocess == True:
            #using multiprocess to create the histograms
            pool = Pool(processes=len(self.hist_cfg.cfgs))
            results = pool.map(self.makealltheplots, self.hist_cfg.cfgs) 
            pool.terminate()

            for vcfg in self.vcfgs:
                for result in results: 
                    self.plots[vcfg.name].AddHistogram(\
                            result[vcfg.name].histos[0].name\
                            ,result[vcfg.name].histos[0].obj\
                            ,stack=result[vcfg.name].histos[0].stack)

       
        # DO NOT USE IT FOR PRODUCTION, ONLY FOR DEBUGGING: if we don't use multiprocess, we compute the histos one by one - good for debugging.
        if multiprocess == False:
            for i, cfg in enumerate(self.hist_cfg.cfgs):
                # result = self.makealltheplots(self.hist_cfg.cfgs[i]) 
                try:
                    result = self.makealltheplots(self.hist_cfg.cfgs[i]) 
                except:
                    set_trace()

        procs = []
        for i, plot in enumerate(self.plots.itervalues()):
            proc = Process(target=plot.Draw, args=())
            procs.append(proc)
            proc.start()
     
        for proc in procs:
            proc.join()       

        # for plot in self.plots.itervalues():
            # plot.Draw()

        return self.plots

    def makealltheplots(self, cfg):
        verbose=False
        all_stack=False
    #    for cfg in [hist_cfg.cfgs[0]]:
    #    for cfg in hist_cfg.cfgs:
            # First check whether it's a sub-histo or not
        if isinstance(cfg, HistogramCfg):
            hists = createHistograms(cfg, all_stack=True, vcfgs=self.vcfgs)
            for h in hists: print(h)
            for vcfg in self.vcfgs:
                hist = hists[vcfg.name]
                plot = self.plots[vcfg.name]
                hist._BuildStack(hist._SortedHistograms(), ytitle='Events')
                print('stack built')
                total_hist = plot.AddHistogram(cfg.name, hist.stack.totalHist.weighted, stack=True)

                if cfg.norm_cfg is not None:
                    norm_hist = createHistogram(cfg.norm_cfg, all_stack=True)
                    norm_hist._BuildStack(norm_hist._SortedHistograms(), ytitle='Events')
                    total_hist.Scale(hist.stack.integral/total_hist.Yield())

                if cfg.total_scale is not None:
                    total_hist.Scale(cfg.total_scale)
                    # print 'Scaling total', hist_cfg.name, 'by', cfg.total_scale
        else:
            # print('building histgrams for %s'%cfg.name)
            # It's a sample cfg

            # Now read the tree
            tree_file_name = '/'.join([cfg.ana_dir, cfg.dir_name, cfg.tree_prod_name, 'tree.root'])

            # attach the trees to the first DataMCPlot
            plot = self.plots[self.vcfgs[0].name]
            try:
                if self.useNeuralNetwork:
                    if cfg.is_singlefake:
                        # friend_file_name = fr_net.makeFriendtree(
                                            # tree_file_name = tree_file_name,
                                            # sample_name = cfg.name,
                                            # net_name = fr_net.path_to_NeuralNet('SingleFake1') + 'net.h5',
                                            # path_to_NeuralNet = fr_net.path_to_NeuralNet('SingleFake1'),
                                            # branches = fr_net.branches_SF1(fr_net.features_SF1()),
                                            # features = fr_net.features_SF1(),
                                            # overwrite = False,
                                            # )
                        # dataframe = plot.makeRootDataFrameFromTree(tree_file_name, cfg.tree_name, verbose=verbose, friend_name='SF1', friend_file_name=friend_file_name)
                        friend_file_name = fr_net.makeFriendtree(
                                            tree_file_name = tree_file_name,
                                            sample_name = cfg.name,
                                            net_name = fr_net.path_to_NeuralNet('SingleFake2') + 'net.h5',
                                            path_to_NeuralNet = fr_net.path_to_NeuralNet('SingleFake2'),
                                            branches = fr_net.get_branches_SF2(fr_net.get_features_SF2()),
                                            features = fr_net.get_features_SF2(),
                                            overwrite = False,
                                            )
                        dataframe = plot.makeRootDataFrameFromTree(tree_file_name, cfg.tree_name, verbose=verbose, friend_name='SF2', friend_file_name=friend_file_name)
                        dataframe = plot.makeRootDataFrameFromTree(tree_file_name, cfg.tree_name, verbose=verbose, friend_name='SF1', friend_file_name=friend_file_name)
                    if cfg.is_doublefake:
                        friend_file_name = fr_net.makeFriendtree(
                                            tree_file_name = tree_file_name,
                                            sample_name = cfg.name,
                                            net_name = fr_net.path_to_NeuralNet('DoubleFake') + 'net.h5',
                                            path_to_NeuralNet = fr_net.path_to_NeuralNet('DoubleFake'),
                                            branches = fr_net.get_branches_DF(fr_net.get_features_DF()),
                                            features = fr_net.get_features_DF(),
                                            overwrite = False,
                                            )
                        dataframe = plot.makeRootDataFrameFromTree(tree_file_name, cfg.tree_name, verbose=verbose, friend_name='DF', friend_file_name=friend_file_name)
                    if cfg.is_nonprompt:
                        friend_file_name = fr_net.makeFriendtree(
                                            tree_file_name = tree_file_name,
                                            sample_name = cfg.name,
                                            net_name = fr_net.path_to_NeuralNet('nonprompt') + 'net.h5',
                                            path_to_NeuralNet = fr_net.path_to_NeuralNet('nonprompt'),
                                            branches = fr_net.get_branches_nonprompt(fr_net.get_features_nonprompt()),
                                            features = fr_net.get_features_nonprompt(),
                                            overwrite = False,
                                            )
                        dataframe = plot.makeRootDataFrameFromTree(tree_file_name, cfg.tree_name, verbose=verbose, friend_name='nonprompt', friend_file_name=friend_file_name)
                    if cfg.is_contamination:
                        friend_file_name = fr_net.makeFriendtree(
                                            tree_file_name = tree_file_name,
                                            sample_name = cfg.name,
                                            net_name = fr_net.path_to_NeuralNet('nonprompt') + 'net.h5',
                                            path_to_NeuralNet = fr_net.path_to_NeuralNet('nonprompt'),
                                            branches = fr_net.get_branches_nonprompt(fr_net.get_features_nonprompt()),
                                            features = fr_net.get_features_nonprompt(),
                                            overwrite = False,
                                            )
                        dataframe = plot.makeRootDataFrameFromTree(tree_file_name, cfg.tree_name, verbose=verbose, friend_name='contamination', friend_file_name=friend_file_name)
                    else:
                        dataframe = plot.makeRootDataFrameFromTree(tree_file_name, cfg.tree_name, verbose=verbose)
                else:
                    dataframe = plot.makeRootDataFrameFromTree(tree_file_name, cfg.tree_name, verbose=verbose)

            except:
                #This is for debugging
                set_trace()

            # set_trace()
            if cfg.is_singlefake == True:
                norm_cut  = self.hist_cfg.region.SF_LL
                self.norm_cut_LL  = self.hist_cfg.region.SF_LL
                self.norm_cut_LT  = self.hist_cfg.region.SF_LT
                self.norm_cut_TL  = self.hist_cfg.region.SF_TL

            if cfg.is_doublefake == True:
                norm_cut  = self.hist_cfg.region.DF
            
            if cfg.is_nonprompt == True:
                norm_cut  = self.hist_cfg.region.nonprompt

            if cfg.is_MC == True:
                # norm_cut  = self.hist_cfg.region.MC
                norm_cut  = self.hist_cfg.region.MC_contamination_pass

            if cfg.is_SingleConversions == True:
                # norm_cut  = self.hist_cfg.region.MC_SingleConversions
                norm_cut  = self.hist_cfg.region.MC_contamination_pass

            if cfg.is_DoubleConversions == True:
                # norm_cut  = self.hist_cfg.region.MC_DoubleConversions
                norm_cut  = self.hist_cfg.region.MC_contamination_pass

            if cfg.is_Conversions == True:
                # norm_cut  = self.hist_cfg.region.MC_Conversions
                norm_cut  = self.hist_cfg.region.MC_contamination_pass

            if cfg.is_DY == True:
                # norm_cut  = self.hist_cfg.region.MC_DY
                norm_cut  = self.hist_cfg.region.MC_contamination_pass

            if cfg.is_data == True:
                norm_cut  = self.hist_cfg.region.data

            if cfg.is_signal == True:
                norm_cut  = self.hist_cfg.region.signal

            if cfg.is_contamination == True:
                # norm_cut = self.hist_cfg.region.nonprompt + " && (l1_gen_match_isPromptFinalState==1 && l2_gen_match_isPromptFinalState==1)"
                # norm_cut = self.hist_cfg.region.nonprompt
                # norm_cut  = self.hist_cfg.region.MC
                norm_cut  = self.hist_cfg.region.MC_contamination_pass
            
            weight = self.hist_cfg.weight
            if cfg.weight_expr:
                weight = '*'.join([weight, cfg.weight_expr])

            # print '#### FULL CUT ####', norm_cut

            # Initialise all hists before the multidraw
            hists = {}

            for vcfg in self.vcfgs:
                # hname = '_'.join([self.hist_cfg.name, hashlib.md5(self.hist_cfg.cut).hexdigest(), cfg.name, vcfg.name, cfg.dir_name])
                hname = '_'.join([self.hist_cfg.name, hashlib.md5(norm_cut).hexdigest(), cfg.name, vcfg.name, cfg.dir_name])
                if any(str(b) == 'xmin' for b in vcfg.binning):
                    hist = TH1F(hname, '', vcfg.binning['nbinsx'],
                                vcfg.binning['xmin'], vcfg.binning['xmax'])
                else:
                    hist = TH1F(hname, '', len(vcfg.binning['bins'])-1, vcfg.binning['bins'])

                initHist(hist, vcfg)
                hists[vcfg.name] = hist


            var_hist_tuples = []

            for vcfg in self.vcfgs:
                var_hist_tuples.append('{var} >> {hist}'.format(var=vcfg.drawname, hist=hists[vcfg.name].GetName()))

            stack = all_stack or (not cfg.is_data and not cfg.is_signal)


            # Produce all histograms using the RootDataFrame FW and add them to self.plots
            # print 'preparing %s with the following cut: '%(cfg.name) + norm_cut
            start = time.time()

            for vcfg in self.vcfgs:
                # self.makeDataFrameHistograms(vcfg,cfg,weight,dataframe,norm_cut,hists,stack)
                hist = self.makeDataFrameHistograms(vcfg,cfg,weight,dataframe,norm_cut,hists,stack,self.useNeuralNetwork)
                self.plots[vcfg.name].AddHistogram(cfg.name, hist.Clone(), stack=stack)

            # print('Added histograms for %s. It took %.1f secods'%(cfg.name,time.time()-start))
            PLOTS = self.plots
        return PLOTS

    def makeDataFrameHistograms(self,vcfg,cfg,weight,dataframe,norm_cut,hists,stack,useNeuralNetwork):
        plot = self.plots[vcfg.name]

        if (not cfg.is_data) and (not cfg.is_doublefake) and (not cfg.is_singlefake) and (not cfg.is_nonprompt):
            weight = weight + ' * ' + str(self.hist_cfg.lumi*cfg.xsec/cfg.sumweights)

        gSystem.Load("modules/DDE_doublefake_h.so")
        gSystem.Load("modules/DDE_singlefake_h.so")

        dataframe =   dataframe\
                                .Define('norm_count','1.')\
                                .Define('l0_pt_cone','l0_pt * (1 + l0_reliso_rho_03)')\
                                .Define('pt_cone','(  ( hnl_hn_vis_pt * (hnl_iso03_rel_rhoArea<0.2) ) + ( (hnl_iso03_rel_rhoArea>=0.2) * ( hnl_hn_vis_pt * (1. + hnl_iso03_rel_rhoArea - 0.2) ) )  )')\
                                # .Define('eta_hnl_l0','hnl_hn_eta - l0_eta')\
                                # .Define('abs_dphi_hnvis0','abs(hnl_dphi_hnvis0)')\
                                # .Define('abs_hnl_hn_eta','abs(hnl_hn_eta)')\
                                # .Define('abs_hnl_hn_vis_eta','abs(hnl_hn_vis_eta)')
                                # .Define('abs_l1_eta','abs(l1_eta)')\
                                # .Define('abs_l2_eta','abs(l2_eta)')\
                                # .Define('l1_pt_cone','((l1_pt * (l1_reliso_rho_03<0.2)) + ((l1_reliso_rho_03>=0.2) * (l1_pt * (1. + l1_reliso_rho_03 - 0.2))))')\
                                # .Define('l2_pt_cone','((l2_pt * (l2_reliso_rho_03<0.2)) + ((l2_reliso_rho_03>=0.2) * (l2_pt * (1. + l2_reliso_rho_03 - 0.2))))')\
                                # .Define('abs_l2_dxy','abs(l2_dxy)')\
                                # .Define('abs_l2_dz','abs(l2_dz)')\
                                # .Define('doubleFakeRate','dfr_namespace::getDoubleFakeRate(pt_cone, abs_hnl_hn_eta)')\
                                # .Define('doubleFakeRate','dfr_namespace::getDoubleFakeRate(pt_cone, abs_hnl_hn_eta, hnl_dr_12, hnl_2d_disp)')\
                                # .Define('singleFakeRate','sfr_namespace::getSingleFakeRate(pt_cone, abs_hnl_hn_eta)')\
        
        # define some extra columns for custom calculations
        if useNeuralNetwork == True:     
            if cfg.is_singlefake:
                dataframe =   dataframe\
                                        .Define('singleFakeRate1','SF1.ml_fr')\
                                        .Define('singleFakeWeight1','singleFakeRate1/(1.0-singleFakeRate1)')\
                                        .Define('singleFakeRate2','SF2.ml_fr')\
                                        .Define('singleFakeWeight2','singleFakeRate2/(1.0-singleFakeRate2)')
            if cfg.is_doublefake:
                dataframe =   dataframe\
                                        .Define('doubleFakeRate','DF.ml_fr')\
                                        .Define('doubleFakeWeight','doubleFakeRate/(1.0-doubleFakeRate)')
                                        # .Filter('doubleFakeRate != 1')\

            if cfg.is_nonprompt:
                dataframe =   dataframe\
                                        .Define('nonprompt_FakeRate','nonprompt.ml_fr')\
                                        .Define('nonprompt_FakeWeight','nonprompt_FakeRate/(1.0-nonprompt_FakeRate)')
            
        else:
            dataframe =   dataframe\
                                    .Define('singleFakeRate','sfr_namespace::getSingleFakeRate(pt_cone, abs_hnl_hn_eta)')\
                                    .Define('singleFakeWeight','singleFakeRate/(1.0-singleFakeRate)')\
                                    .Define('doubleFakeRate','dfr_namespace::getDoubleFakeRate(pt_cone, abs_hnl_hn_eta, hnl_dr_12, hnl_2d_disp)')\
                                    .Define('doubleFakeWeight','doubleFakeRate/(1.0-doubleFakeRate)')

        # define additional columns for the ptcone correction
        gSystem.Load("modules/pt_ConeCorrection_h.so")
        dataframe =   dataframe\
                                .Define('l0_px_ConeCorrected','pt_ConeCorrection::pCone(l0_px, l0_reliso_rho_03)')\
                                .Define('l0_py_ConeCorrected','pt_ConeCorrection::pCone(l0_py, l0_reliso_rho_03)')\
                                .Define('l0_pz_ConeCorrected','pt_ConeCorrection::pCone(l0_pz, l0_reliso_rho_03)')\
                                .Define('l0_e_ConeCorrected' ,'pt_ConeCorrection::pCone(l0_e , l0_reliso_rho_03)')\
                                .Define('l1_px_ConeCorrected','pt_ConeCorrection::pCone(l1_px, l1_reliso_rho_03)')\
                                .Define('l1_py_ConeCorrected','pt_ConeCorrection::pCone(l1_py, l1_reliso_rho_03)')\
                                .Define('l1_pz_ConeCorrected','pt_ConeCorrection::pCone(l1_pz, l1_reliso_rho_03)')\
                                .Define('l1_e_ConeCorrected' ,'pt_ConeCorrection::pCone(l1_e , l1_reliso_rho_03)')\
                                .Define('l2_px_ConeCorrected','pt_ConeCorrection::pCone(l2_px, l2_reliso_rho_03)')\
                                .Define('l2_py_ConeCorrected','pt_ConeCorrection::pCone(l2_py, l2_reliso_rho_03)')\
                                .Define('l2_pz_ConeCorrected','pt_ConeCorrection::pCone(l2_pz, l2_reliso_rho_03)')\
                                .Define('l2_e_ConeCorrected' ,'pt_ConeCorrection::pCone(l2_e , l2_reliso_rho_03)')\
                                .Define('hnl_m_12_ConeCorrected','pt_ConeCorrection::dimass(\
                                        l1_px_ConeCorrected,\
                                        l1_py_ConeCorrected,\
                                        l1_pz_ConeCorrected,\
                                        l1_e_ConeCorrected,\
                                        l2_px_ConeCorrected,\
                                        l2_py_ConeCorrected,\
                                        l2_pz_ConeCorrected,\
                                        l2_e_ConeCorrected\
                                        )')\
                                .Define('hnl_m_12_ConeCorrected_test','pt_ConeCorrection::dimass(\
                                        l1_px,\
                                        l1_py,\
                                        l1_pz,\
                                        l1_e,\
                                        l2_px,\
                                        l2_py,\
                                        l2_pz,\
                                        l2_e\
                                        )')
                                


        if cfg.is_singlefake:
            '''
            in this section we introduce singlefakes, which is made of the following components:
            1. tight prompt lepton + tight displaced lepton + loose-not-tight displaced lepton 
            - an application region for single fakes (SFR), these events are weighted 
            by SFR/(1-SFR) where SFR is taken for loose-not-tight displaced lepton;
            2. tight prompt lepton + two loose-not-tight displaced leptons where these displaced 
            leptons are not clustered into a single jet 
            - an application region for single FR, these events are weighted 
            by -SFR1/(1-SFR1)*SFR2/(1-SFR2).
            Note "-" sign: this contribution is subtracted from the contribution above (#2)
            '''

            dataframe =   dataframe\
                            .Define('weight_LL','(singleFakeWeight1 * singleFakeWeight2)')\
                            .Define('weight_LT','singleFakeWeight1')\
                            .Define('weight_TL','singleFakeWeight2')

            # dataframe =   dataframe\
                            # .Define('weight_LL','1')\
                            # .Define('weight_LT','1')\
                            # .Define('weight_TL','1')

            # # implement ptCone correction to the single fakes
            # if 'hnl_m_12' in vcfg.drawname:
                # vcfg.drawname = 'hnl_m_12_ConeCorrected'


            hist_sf_LL = dataframe\
                            .Filter(self.norm_cut_LL)\
                            .Histo1D((hists[vcfg.name].GetName(),'',vcfg.binning['nbinsx'],vcfg.binning['xmin'], vcfg.binning['xmax']),vcfg.drawname,'weight_LL')
            hist_sf_LL = hist_sf_LL.Clone() # convert the ROOT.ROOT::RDF::RResultPtr<TH1D> object into a ROOT.TH1D object

            hist_sf_LT = dataframe\
                            .Filter(self.norm_cut_LT)\
                            .Histo1D((hists[vcfg.name].GetName(),'',vcfg.binning['nbinsx'],vcfg.binning['xmin'], vcfg.binning['xmax']),vcfg.drawname,'weight_LT')
            hist_sf_LT = hist_sf_LT.Clone() # convert the ROOT.ROOT::RDF::RResultPtr<TH1D> object into a ROOT.TH1D object
        
            hist_sf_TL = dataframe\
                            .Filter(self.norm_cut_TL)\
                            .Histo1D((hists[vcfg.name].GetName(),'',vcfg.binning['nbinsx'],vcfg.binning['xmin'], vcfg.binning['xmax']),vcfg.drawname,'weight_TL')
            hist_sf_TL = hist_sf_TL.Clone() # convert the ROOT.ROOT::RDF::RResultPtr<TH1D> object into a ROOT.TH1D object


            hist_sf_TL.Add(hist_sf_LT)       
            hist_sf_TL.Add(hist_sf_LL,-1)       
            hists[vcfg.name] = hist_sf_TL      
            
            # hists[vcfg.name] = hist_sf_TL      
            # hists[vcfg.name] = hist_sf_LT      
            # hists[vcfg.name] = hist_sf_LL      
        
        if cfg.is_doublefake:
            '''
            in this section, we introduce the double fakes compoment:
            ==> tight prompt lepton + two loose-not-tight displaced leptons where these displaced 
            leptons are clustered into a single jet 
            - an application region for double FR, these events are weighted by DFR/(1-DFR) 
            where DFR is picked up as a function of a dilepton properties (pt-corr, eta, flavor).
            '''
            weight = 'doubleFakeWeight'

            is_corrupt = dataframe.Define('is_same','DF.hnl_hn_vis_pt - hnl_hn_vis_pt').Filter('is_same != 0').Count().GetValue()
            if is_corrupt > 0:
                print '%s: main tree and friend tree do not match'%(cfg.name)
                set_trace()

        if cfg.is_nonprompt:
            '''
            This is a crazy attempt to have a single fake rate substituting both SF and DF.
            '''
            weight = 'nonprompt_FakeWeight'
            # is_corrupt = dataframe.Define('is_same','nonprompt.l2_pt - l2_pt').Filter('is_same != 0').Count().GetValue()
            # if is_corrupt > 0:
                # print '%s: main tree and friend tree do not match'%(cfg.name)
                # set_trace()
    
        if cfg.is_contamination:
            '''
            Eventually, the very same procedure of DDE should be applied to the MC samples,
            in order to remove prompt contamination from the application region. 
            In events taken from MC samples MC-truth matching should be always on
            (we need to pick up only prompt leptons from MC), and there the very
            same algorithm applies, but the sign of the contribution will be inverted:

            event weight for single FR: -SFR/(1-SFR)
            event weight for single FR with two fakes: SFR1/(1-SFR1)*SFR2/(1-SFR2)
            event weight for double FR: -DFR/(1-DFR)
            
            This signs inversion corresponds to the fact that we subtract from the data
            application region the prompt contamination (with MC truth matching and
            all the data/MC scale-factors applied).
            '''

            weight = weight + ' * (-1)'
            # weight = weight 
            # weight = '(-1)'
            # weight = 'contamination_FakeWeight'
            # dataframe =   dataframe\
                                    # .Define('contamination_FakeRate','-1')\
                                    # # .Define('contamination_FakeRate','contamination.ml_fr')\
                                    # # .Define('contamination_FakeWeight','(contamination_FakeRate/(1.0-contamination_FakeRate))')
                                    # # .Define('contamination_FakeWeight','-(contamination_FakeRate/(1.0-contamination_FakeRate))')

        
        if not cfg.is_singlefake:
            if 'nbinsx' in vcfg.binning.keys():
                hists[vcfg.name] =   dataframe\
                                        .Define('w',weight)\
                                        .Filter(norm_cut)\
                                        .Histo1D((hists[vcfg.name].GetName(),'',vcfg.binning['nbinsx'],vcfg.binning['xmin'], vcfg.binning['xmax']),vcfg.drawname,'w')
            else: 
                hists[vcfg.name] =   dataframe\
                                        .Define('w',weight)\
                                        .Filter(norm_cut)\
                                        .Histo1D((hists[vcfg.name].GetName(),'',len(vcfg.binning['bins'])-1,vcfg.binning['bins']),vcfg.drawname,'w')

            histo = hists[vcfg.name]
        return hists[vcfg.name]

