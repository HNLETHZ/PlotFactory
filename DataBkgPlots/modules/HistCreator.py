import hashlib
from multiprocessing import Pool, Process, cpu_count
# from multiprocessing.dummy import Pool, Process, cpu_count

from array import array
import numpy as np
import time
from modules.PlotConfigs import HistogramCfg
from modules.DataMCPlot import DataMCPlot
from modules.DDE import DDE
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
    def __init__(self, hist_cfg, analysis_dir = '/home/dehuazhu/SESSD/4_production/', channel = 'mmm', server = 'starseeker' ):
        self.analysis_dir = analysis_dir
        self.channel = channel
        self.server = server
        self.hist_cfg = hist_cfg
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

    def createHistograms(self, hist_cfg, all_stack=False, verbose=False,  vcfgs=None, multiprocess = True):
        if multiprocess == True:
            #using multiprocess to create the histograms
            pool = Pool(processes=len(self.hist_cfg.cfgs))
            result = pool.map(self.makealltheplots, self.hist_cfg.cfgs) 
       
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
            file_name = '/'.join([cfg.ana_dir, cfg.dir_name, cfg.tree_prod_name, 'tree.root'])

            # attach the trees to the first DataMCPlot
            plot = self.plots[self.vcfgs[0].name]
            try:
                dataframe = plot.makeRootDataFrameFromTree(file_name, cfg.tree_name, verbose=verbose)
            except:
                set_trace()

            if cfg.is_dde == True:
                ttree.AddFriend('tree',cfg.fr_tree_path)
                #to test the friendtree, you can set trace here and do ttree.GetEntries('tree.fover1minusf021 > 0.01')

            #define the cuts for different stackplots
            # if cfg.is_dde == True and cfg.is_singlefake == True:
                # norm_cut  = self.hist_cfg.region.SF
                # shape_cut = self.hist_cfg.region.SF
                # norm_cut = '({c}) * {we}'.format(c=norm_cut, we='tree.fover1minusf021')
                # shape_cut = '({c}) * {we}'.format(c=shape_cut, we='tree.fover1minusf021')

            if cfg.is_singlefake == True:
                norm_cut  = self.hist_cfg.region.SF
                shape_cut = self.hist_cfg.region.SF

            if cfg.is_doublefake == True:
                norm_cut  = self.hist_cfg.region.DF
                shape_cut = self.hist_cfg.region.DF

            if  cfg.is_MC_Conversions == False:
                norm_cut  = self.hist_cfg.region.MC
                shape_cut = self.hist_cfg.region.MC

            if cfg.is_MC_Conversions == True:
                norm_cut  = self.hist_cfg.region.MC_Conversions
                shape_cut = self.hist_cfg.region.MC_Conversions

            if cfg.is_data == True:
                norm_cut  = self.hist_cfg.region.data
                shape_cut = self.hist_cfg.region.data

            if cfg.is_signal == True:
                norm_cut  = self.hist_cfg.region.signal
                shape_cut = self.hist_cfg.region.signal
            
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
                    hist = TH1F(hname, '', len(vcfg.binning)-1, vcfg.binning)

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
                hist = self.makeDataFrameHistograms(vcfg,cfg,weight,dataframe,norm_cut,hists,stack)
                self.plots[vcfg.name].AddHistogram(cfg.name, hist.Clone(), stack=stack)

            # print('Added histograms for %s. It took %.1f secods'%(cfg.name,time.time()-start))
            PLOTS = self.plots
        return PLOTS

    def makeDataFrameHistograms(self,vcfg,cfg,weight,dataframe,norm_cut,hists,stack):
        plot = self.plots[vcfg.name]
        # print 'adding %s with the cut: \t%s'%(cfg.name,norm_cut)
        if (not cfg.is_data) and (not cfg.is_doublefake) and (not cfg.is_singlefake):
            weight = weight + ' * ' + str(self.hist_cfg.lumi*cfg.xsec/cfg.sumweights)
        if cfg.is_doublefake:
            
            # Comment this section out if you want to remeasure the fakerates
            dfr_TH2D_dir = "modules/DDE_doublefake.root"
            dfr_hist = None
            dfr_TH2D = TFile(dfr_TH2D_dir,"RECREATE")
            doublefake = DDE(self.analysis_dir,self.server,self.channel) 
            dfr_hist = doublefake.measureFR()
            dfr_TH2D.Write()
            dfr_namespace_dir = "modules/DDE_doublefake.h"
            if not dfr_hist:
                dfr_hist_file = TFile(dfr_TH2D_dir)
                dfr_hist = dfr_hist_file.Get('h_TT_correlated')
            with open(dfr_namespace_dir, "w") as dfr_namespace:
                    dfr_namespace.write("// This namespace prepares the doublefakerate measured via DDE.py to be implementable in dataframe for the main plotting tool.\n")
                    dfr_namespace.write("namespace dfr_namespace {\n")
                    dfr_namespace.write("\tdouble getFakeRate(double ptCone, double eta){\n")
                    for xbin_i in np.arange(dfr_hist.GetNbinsX()): 
                        for ybin_i in np.arange(dfr_hist.GetNbinsY()): 
                            xbin_low = dfr_hist.GetXaxis().GetXbins()[xbin_i]
                            xbin_up  = dfr_hist.GetXaxis().GetXbins()[xbin_i+1]
                            ybin_low = dfr_hist.GetYaxis().GetXbins()[ybin_i]
                            ybin_up  = dfr_hist.GetYaxis().GetXbins()[ybin_i+1]
                            result   = dfr_hist.GetBinContent(xbin_i+1, ybin_i+1)
                            dfr_namespace.write("\t\tif (ptCone >= %f && ptCone < %f && eta >= %f && eta < %f) return %f;\n"%(xbin_low,xbin_up,ybin_low,ybin_up,result))
                    dfr_namespace.write("\t\treturn 0.;\n")
                    dfr_namespace.write("\t}\n")
                    dfr_namespace.write("}\n")
            print 'FakeRateMap saved in "%s"'%(dfr_TH2D_dir)
            print 'FakeRateNamespace saved in "%s"'%(dfr_namespace_dir)
            gROOT.ProcessLine(".L modules/DDE_doublefake.h+")
            # End the comment here

            gSystem.Load("modules/DDE_doublefake_h.so")
            
            # weight = weight + ' * ' + str('(dfr_namespace::getFakeRate(pt_cone,hnl_hn_eta))/(1.-dfr_namespace::getFakeRate(pt_cone,hnl_hn_eta))')
            # weight = weight + ' * ' + 'doubleFakeWeight'
            # weight = weight + ' * ' + '0.8'
            weight = 'doubleFakeWeight'
            weight = '1.'

        hists[vcfg.name] =   dataframe.Filter(norm_cut)\
                                .Define('norm_count','1.')\
                                .Define('l0_pt_cone','l0_pt * (1 + l0_reliso_rho_03)')\
                                .Define('l1_pt_cone','l0_pt * (1 + l1_reliso_rho_03)')\
                                .Define('l2_pt_cone','l0_pt * (1 + l2_reliso_rho_03)')\
                                .Define('pt_cone','(  ( hnl_hn_vis_pt * (hnl_iso03_rel_rhoArea<0.2) ) + ( (hnl_iso03_rel_rhoArea>=0.2) * ( hnl_hn_vis_pt * (1. + hnl_iso03_rel_rhoArea - 0.2) ) )  )')\
                                .Define('abs_dphi_hnvis0','abs(hnl_dphi_hnvis0)')\
                                .Define('eta_hnl_l0','hnl_hn_eta - l0_eta')\
                                .Define('abs_hnl_hn_eta','abs(hnl_hn_eta)')\
                                .Define('w',weight)\
                                .Histo1D((hists[vcfg.name].GetName(),'',vcfg.binning['nbinsx'],vcfg.binning['xmin'], vcfg.binning['xmax']),vcfg.drawname,'w')
                                # .Define('doubleFakeRate','dfr_namespace::getFakeRate(pt_cone, abs_hnl_hn_eta)')\
                                # .Define('doubleFakeWeight','doubleFakeRate/(1.0-doubleFakeRate)')\

        # if cfg.name in plot:
            # print 'Histogram', cfg.name, 'already exists', cfg.dir_name
        # else:
            # return hists[vcfg.name].Clone()
            # # plot.AddHistogram(cfg.name, hists[vcfg.name].Clone(), stack=stack)
            # print('added histo %s for %s'%(vcfg.name,cfg.name))
        # return hists[vcfg.name].Clone()
        return hists[vcfg.name]

