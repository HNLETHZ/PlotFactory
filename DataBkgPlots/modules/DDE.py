from modules.officialStyle import officialStyle
import plotfactory as pf
from modules.Samples import createSampleLists, setSumWeights
from modules.Selections import getSelection
from ROOT import ROOT, RDataFrame, TH1F, TFile, TTree, TTreeFormula, TCanvas, TPaveText, TBox, gStyle,TChain, gROOT, gSystem
import numpy as np
from socket import gethostname

from pdb import set_trace

# Using official CMS Style
# officialStyle(gStyle)
pf.setpfstyle()

# Enable ROOT's implicit multi-threading for all objects that provide an internal parallelisation mechanism
ROOT.EnableImplicitMT()

class DDE(object):

    def __init__(self, analysis_dir, server, channel):
        self.analysis_dir   = analysis_dir
        self.server         = server
        self.channel        = channel

    def ptCone(self):
        # PTCONE = '((l%s_pt*(l%s_reliso_rho_03<0.2))+((l%s_reliso_rho_03>=0.2)*(l%s_pt*(1. + l%s_reliso_rho_03 - 0.2))))'%(lepton,lepton,lepton,lepton,lepton)
        PTCONE   = '(  ( hnl_hn_vis_pt * (hnl_iso03_rel_rhoArea<0.2) ) + ( (hnl_iso03_rel_rhoArea>=0.2) * ( hnl_hn_vis_pt * (1. + hnl_iso03_rel_rhoArea - 0.2) ) )  )'
        return PTCONE

    def makeDataFrame(self):
        sample_dict = {}
        samples_all, samples_singlefake, samples_doublefake = createSampleLists(analysis_dir=self.analysis_dir, server = self.server, channel=self.channel)
        working_samples = samples_doublefake
        working_samples = setSumWeights(working_samples)
        print('###########################################################')
        print'# measuring doublefakerake...'
        print'# %d samples to be used:'%(len(working_samples))
        print('###########################################################')
        for w in working_samples: print('{:<20}{:<20}'.format(*[w.name,('path: '+w.ana_dir)]))
        chain = TChain('tree') #TChain'ing all data samples together
        for i,s in enumerate(working_samples):
            sample = working_samples[0]
            file_name = '/'.join([sample.ana_dir, sample.dir_name, sample.tree_prod_name, 'tree.root'])
            chain.Add(file_name)
            
        dataframe = RDataFrame(chain)
        weight = 'weight * lhe_weight'
        dataframe = dataframe.Define('w',weight)\
                            .Define('ptCone',self.ptCone())\
                            .Define('abs_hnl_hn_vis_eta','abs(hnl_hn_vis_eta)')\
                            .Define('abs_hnl_hn_eta','abs(hnl_hn_eta)')\
                            .Define('abs_l1_eta','abs(l1_eta)')\
                            .Define('abs_l2_eta','abs(l2_eta)')\
                            .Define('abs_l1_jet_flavour_parton','abs(l1_jet_flavour_parton)')\
                            .Define('abs_l2_jet_flavour_parton','abs(l2_jet_flavour_parton)')\

        return dataframe

    # def measureFR(self, analysis_dir,server, channel):
    def measureSFR(self, drawPlot = False):
        sample_dict = {}
        samples_all, samples_singlefake, samples_doublefake = createSampleLists(analysis_dir=self.analysis_dir, server = self.server, channel=self.channel)
        working_samples = samples_singlefake
        working_samples = setSumWeights(working_samples)
        print('###########################################################')
        print'# measuring singlefakerake...'
        print'# %d samples to be used:'%(len(working_samples))
        print('###########################################################')
        for w in working_samples: print('{:<20}{:<20}'.format(*[w.name,('path: '+w.ana_dir)]))
        chain = TChain('tree') #TChain'ing all data samples together
        for i,s in enumerate(working_samples):
            sample = working_samples[0]
            file_name = '/'.join([sample.ana_dir, sample.dir_name, sample.tree_prod_name, 'tree.root'])
            chain.Add(file_name)
            
        dataframe = RDataFrame(chain)
        weight = 'weight * lhe_weight'
        dataframe = dataframe.Define('w',weight)\
                            .Define('ptCone',self.ptCone())\
                            .Define('abs_hnl_hn_vis_eta','abs(hnl_hn_vis_eta)')\
                            .Define('abs_hnl_hn_eta','abs(hnl_hn_eta)')\
                            .Define('abs_l1_eta','abs(l1_eta)')\
                            .Define('abs_l2_eta','abs(l2_eta)')\
                            .Define('abs_l1_jet_flavour_parton','abs(l1_jet_flavour_parton)')\
                            .Define('abs_l2_jet_flavour_parton','abs(l2_jet_flavour_parton)')\

        # bins_ptCone = np.array([5.,10., 20., 30., 40.,70., 2000])
        # bins_eta    = np.array([0., 0.8, 1.2, 2.4]) 
        bins_ptCone = np.array([5.,10., 20., 30., 40.,70.])
        bins_eta    = np.array([0., 0.8, 1.2, 2.4]) 

        selection_baseline      = getSelection(self.channel,'MR_SF')  

        selection_LL_uncorrelated = '(' + ' & '\
                                    .join([\
                                    selection_baseline,\
                                    getSelection(self.channel,'L_L_uncorrelated')\
                                    ]) + ')' 
        selection_TT_uncorrelated = '(' + ' & '\
                                    .join([\
                                    selection_baseline,\
                                    getSelection(self.channel,'L_L_uncorrelated'),\
                                    getSelection(self.channel,'T_T')\
                                    ]) + ')' 

        h_LL_uncorrelated = dataframe\
                .Filter(selection_LL_uncorrelated)\
                .Histo2D(('h_LL_uncorrelated','h_LL_uncorrelated',len(bins_ptCone)-1,bins_ptCone, len(bins_eta)-1, bins_eta),'ptCone','abs_hnl_hn_vis_eta','w')
        #name the axis, also initiate the dataframe call
        h_LL_uncorrelated.SetTitle(';ptCone [GeV]; dimuon #eta')

        h_TT_uncorrelated = dataframe\
                .Filter(selection_TT_uncorrelated)\
                .Histo2D(('h_TT_uncorrelated','h_TT_uncorrelated',len(bins_ptCone)-1,bins_ptCone, len(bins_eta)-1, bins_eta),'ptCone','abs_hnl_hn_vis_eta','w')
        #name the axis, also initiate the dataframe call
        h_TT_uncorrelated.SetTitle(';ptCone [GeV]; dimuon #eta')

        # preparing the histo and save it into a .root file
        sfr_TH2_dir = '/home/dehuazhu/HNL/CMSSW_9_4_6_patch1/src/PlotFactory/DataBkgPlots/modules/DDE_singlefake.root' 
        sfr_hist = h_TT_uncorrelated.Clone()
        # sfr_hist = h_LL_uncorrelated.Clone()
        # sfrhist = h_baseline.Clone()
        # sfr_hist.Divide(h_LL_uncorrelated.Clone())
        # dfr_hist.SaveAs(sfr_TH2_dir) #uncomment this to save the TH2

        # draw the histo if required 
        if drawPlot == True:
            can = TCanvas('can', '')
            # sfr_hist.Draw('colzTextE')
            # sfr_hist.Draw('colz')
            sfr_hist.Draw()
            pf.showlumi('%d entries'%(sfr_hist.GetEntries()))
            # pf.showlogopreliminary()
            can.Update()
            set_trace()

    def measureDFR(self, drawPlot = False):
        sample_dict = {}
        samples_all, samples_singlefake, samples_doublefake = createSampleLists(analysis_dir=self.analysis_dir, server = self.server, channel=self.channel)
        working_samples = samples_doublefake
        working_samples = setSumWeights(working_samples)
        print('###########################################################')
        print'# measuring doublefakerake...'
        print'# %d samples to be used:'%(len(working_samples))
        print('###########################################################')
        for w in working_samples: print('{:<20}{:<20}'.format(*[w.name,('path: '+w.ana_dir)]))
        chain = TChain('tree') #TChain'ing all data samples together
        for i,s in enumerate(working_samples):
            sample = working_samples[0]
            file_name = '/'.join([sample.ana_dir, sample.dir_name, sample.tree_prod_name, 'tree.root'])
            chain.Add(file_name)
            
        dataframe = RDataFrame(chain)
        weight = 'weight * lhe_weight'
        dataframe = dataframe.Define('w',weight)\
                            .Define('ptCone',self.ptCone())\
                            .Define('abs_hnl_hn_vis_eta','abs(hnl_hn_vis_eta)')\
                            .Define('abs_hnl_hn_eta','abs(hnl_hn_eta)')\
                            .Define('abs_l1_eta','abs(l1_eta)')\
                            .Define('abs_l2_eta','abs(l2_eta)')\
                            .Define('abs_l1_jet_flavour_parton','abs(l1_jet_flavour_parton)')\
                            .Define('abs_l2_jet_flavour_parton','abs(l2_jet_flavour_parton)')\

        bins_ptCone = np.array([10., 20., 30., 40.,70., 2000])
        # bins_eta    = np.array([0., 0.8, 1.2, 2.4]) 
        # bins_ptCone = np.array([10., 20., 30., 40.,70.])
        bins_eta    = np.array([0.,1.2, 2.4]) 
        # bins_ptCone   = np.arange(0.,70.,5)
        # bins_eta      = np.arange(0.,2.4,0.2)
        # bins_eta    = np.array([0., 2.4]) 

        selection_baseline      = getSelection(self.channel,'MR_DF')  

        selection_LL_correlated = '(' + ' & '\
                                    .join([\
                                    selection_baseline,\
                                    getSelection(self.channel,'L_L_correlated')\
                                    ]) + ')' 
        selection_TT_correlated = '(' + ' & '\
                                    .join([\
                                    selection_baseline,\
                                    getSelection(self.channel,'L_L_correlated'),\
                                    getSelection(self.channel,'T_T')\
                                    ]) + ')' 

        h_LL_correlated = dataframe\
                .Filter(selection_LL_correlated)\
                .Histo2D(('h_LL_correlated','h_LL_correlated',len(bins_ptCone)-1,bins_ptCone, len(bins_eta)-1, bins_eta),'ptCone','abs_hnl_hn_vis_eta','w')
        #name the axis, also initiate the dataframe call
        h_LL_correlated.SetTitle(';ptCone [GeV]; dimuon #eta')

        h_TT_correlated = dataframe\
                .Filter(selection_TT_correlated)\
                .Histo2D(('h_TT_correlated','h_TT_correlated',len(bins_ptCone)-1,bins_ptCone, len(bins_eta)-1, bins_eta),'ptCone','abs_hnl_hn_vis_eta','w')
        #name the axis, also initiate the dataframe call
        h_TT_correlated.SetTitle(';ptCone [GeV]; dimuon #eta')

        # preparing the histo and save it into a .root file
        dfr_TH2_dir = '/home/dehuazhu/HNL/CMSSW_9_4_6_patch1/src/PlotFactory/DataBkgPlots/modules/DDE_doublefake.root' 
        dfr_hist = h_TT_correlated.Clone()
        # dfr_hist = h_LL_correlated.Clone()
        # hist = h_baseline.Clone()
        dfr_hist.Divide(h_LL_correlated.Clone())
        dfr_hist.SaveAs(dfr_TH2_dir) #uncomment this to save the TH2

        


        # draw the histo if required 
        if drawPlot == True:
            can = TCanvas('can', '')
            # hist.Draw('colzTextE')
            dfr_hist.Draw('colz')
            # hist.Draw()
            pf.showlumi('%d entries'%(dfr_hist.GetEntries()))
            # pf.showlogopreliminary()
            can.Update()

    def measureDFR_4D(self, disp_low, disp_high):
        sample_dict = {}
        samples_all, samples_singlefake, samples_doublefake = createSampleLists(analysis_dir=self.analysis_dir, server = self.server, channel=self.channel)
        working_samples = samples_doublefake
        working_samples = setSumWeights(working_samples)
        print('###########################################################')
        print'# measuring doublefakerake...'
        print'# %d samples to be used:'%(len(working_samples))
        print('###########################################################')
        for w in working_samples: print('{:<20}{:<20}'.format(*[w.name,('path: '+w.ana_dir)]))
        chain = TChain('tree') #TChain'ing all data samples together
        for i,s in enumerate(working_samples):
            sample = working_samples[0]
            file_name = '/'.join([sample.ana_dir, sample.dir_name, sample.tree_prod_name, 'tree.root'])
            chain.Add(file_name)
            
        dataframe = RDataFrame(chain)
        weight = 'weight * lhe_weight'
        dataframe = dataframe.Define('w',weight)\
                            .Define('ptCone',self.ptCone())\
                            .Define('abs_hnl_hn_vis_eta','abs(hnl_hn_vis_eta)')\
                            .Define('abs_hnl_hn_eta','abs(hnl_hn_eta)')\
                            .Define('abs_l1_eta','abs(l1_eta)')\
                            .Define('abs_l2_eta','abs(l2_eta)')\
                            .Define('abs_l1_jet_flavour_parton','abs(l1_jet_flavour_parton)')\
                            .Define('abs_l2_jet_flavour_parton','abs(l2_jet_flavour_parton)')\

        bins_ptCone = np.array([10., 20., 30., 40.,70., 2000])
        # bins_eta    = np.array([0., 0.8, 1.2, 2.4]) 
        # bins_ptCone = np.array([10., 20., 30., 40.,70.])
        bins_eta    = np.array([0., 1.2, 2.4]) 
        # bins_ptCone   = np.arange(0.,70.,5)
        # bins_eta      = np.arange(0.,2.4,0.2)
        # bins_eta    = np.array([0., 2.4]) 
        # bins_dr12    = np.array([0.,0.02, 0.05, 1.]) 
        bins_dr12    = np.array([0.,0.05, 1.]) 

        selection_baseline      = getSelection(self.channel,'MR_DF')  

        selection_LL_correlated = '(' + ' & '\
                                    .join([\
                                    selection_baseline,\
                                    getSelection(self.channel,'L_L_correlated')\
                                    ]) + ')' 
        selection_TT_correlated = '(' + ' & '\
                                    .join([\
                                    selection_baseline,\
                                    getSelection(self.channel,'L_L_correlated'),\
                                    getSelection(self.channel,'T_T')\
                                    ]) + ')' 

        h_LL_correlated = dataframe\
                .Filter(selection_LL_correlated)\
                .Filter('hnl_2d_disp >= %s && hnl_2d_disp < %s'%(disp_low,disp_high))\
                .Histo3D(('h_LL_correlated','h_LL_correlated',len(bins_ptCone)-1,bins_ptCone, len(bins_eta)-1, bins_eta,len(bins_dr12)-1,bins_dr12),'ptCone','abs_hnl_hn_vis_eta','hnl_dr_12','w')
        #name the axis, also initiate the dataframe call
        h_LL_correlated.SetTitle(';ptCone [GeV]; dimuon #eta; #DeltaR_{12}')

        h_TT_correlated = dataframe\
                .Filter(selection_TT_correlated)\
                .Filter('hnl_2d_disp >= %s && hnl_2d_disp < %s'%(disp_low,disp_high))\
                .Histo3D(('h_TT_correlated','h_TT_correlated',len(bins_ptCone)-1,bins_ptCone, len(bins_eta)-1, bins_eta,len(bins_dr12)-1,bins_dr12),'ptCone','abs_hnl_hn_vis_eta','hnl_dr_12','w')
        #name the axis, also initiate the dataframe call
        h_TT_correlated.SetTitle(';ptCone [GeV]; dimuon #eta; #DeltaR_{12}')


        # preparing the histo and save it into a .root file
        dfr_TH2_dir = '/home/dehuazhu/HNL/CMSSW_9_4_6_patch1/src/PlotFactory/DataBkgPlots/modules/DDE_doublefake_%s_%s.root'%(disp_low,disp_high) 
        dfr_hist = h_TT_correlated.Clone()
        # dfr_hist = h_LL_correlated.Clone()
        # hist = h_baseline.Clone()
        dfr_hist.Divide(h_LL_correlated.Clone())
        dfr_hist.SaveAs(dfr_TH2_dir) #uncomment this to save the TH2
        print '.root file saved to %s'%(dfr_TH2_dir)

        can = TCanvas('can', '')
        # hist.Draw('colzTextE')
        dfr_hist.Draw('colz')
        # hist.Draw()
        pf.showlumi('%d entries'%(dfr_hist.GetEntries()))
        # pf.showlogopreliminary()
        can.Update()


    def makeNameSpaceDoubleFakes(self):
            # import dfr_hist
            f = TFile('modules/DDE_doublefake.root')
            dfr_hist = f.Get('h_TT_correlated')

            #prepare a .h file to implement the fakerates into the ROOT namespace
            dfr_namespace_dir = "/home/dehuazhu/HNL/CMSSW_9_4_6_patch1/src/PlotFactory/DataBkgPlots/modules/DDE_doublefake.h"
            with open(dfr_namespace_dir, "w") as dfr_namespace:
                    dfr_namespace.write("// This namespace prepares the doublefakerate measured via DDE.py to be implementable in dataframe for the main plotting tool.\n")
                    dfr_namespace.write("namespace dfr_namespace {\n")
                    dfr_namespace.write("\tdouble getDoubleFakeRate(double ptCone, double eta){\n")
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
            print 'FakeRateNamespace saved in "%s"'%(dfr_namespace_dir)
            gROOT.ProcessLine(".L modules/DDE_doublefake.h+")

    def makeNameSpaceDoubleFakes_4D(self):
            # import dfr_hist
            f1= TFile('modules/DDE_doublefake_0.0_0.3.root')
            f2= TFile('modules/DDE_doublefake_0.3_10.0.root')
            # dfr_hist1= f.Get('h_TT_correlated')
            dfr_hist1= f1.Get('h_TT_correlated')
            dfr_hist2= f2.Get('h_TT_correlated')
            # dfr_hist1= f1.Get('Tight')
            # dfr_hist2= f2.Get('Tight')

            #prepare a .h file to implement the fakerates into the ROOT namespace
            dfr_namespace_dir = "/home/dehuazhu/HNL/CMSSW_9_4_6_patch1/src/PlotFactory/DataBkgPlots/modules/DDE_doublefake.h"
            with open(dfr_namespace_dir, "w") as dfr_namespace:
                    dfr_namespace.write("// This namespace prepares the doublefakerate measured via DDE.py to be implementable in dataframe for the main plotting tool.\n")
                    dfr_namespace.write("// Run the following once before using the namespace: gROOT->ProcessLine(\".L modules/DDE_doublefake.h+\");\n")
                    dfr_namespace.write("namespace dfr_namespace {\n")
                    dfr_namespace.write("\tdouble getDoubleFakeRate(double ptCone, double eta, double dr12, double displacement){\n")
                    dfr_namespace.write("\t\tif (displacement >= 0.0 && displacement < 0.3) {\n")
                    for xbin_i in np.arange(dfr_hist1.GetNbinsX()): 
                        for ybin_i in np.arange(dfr_hist1.GetNbinsY()): 
                            for zbin_i in np.arange(dfr_hist1.GetNbinsZ()): 
                                xbin_low = dfr_hist1.GetXaxis().GetXbins()[xbin_i]
                                xbin_up  = dfr_hist1.GetXaxis().GetXbins()[xbin_i+1]
                                ybin_low = dfr_hist1.GetYaxis().GetXbins()[ybin_i]
                                ybin_up  = dfr_hist1.GetYaxis().GetXbins()[ybin_i+1]
                                zbin_low = dfr_hist1.GetZaxis().GetXbins()[zbin_i]
                                zbin_up  = dfr_hist1.GetZaxis().GetXbins()[zbin_i+1]
                                result   = dfr_hist1.GetBinContent(xbin_i+1, ybin_i+1, zbin_i+1)
                                dfr_namespace.write("\t\t\tif (ptCone >= %f && ptCone < %f && eta >= %f && eta < %f && dr12 >= %f && dr12 < %f) return %f;\n"%(xbin_low,xbin_up,ybin_low,ybin_up,zbin_low,zbin_up,result))
                    dfr_namespace.write("\t\t\treturn 0.;\n")
                    dfr_namespace.write("\t\t}\n")
                    dfr_namespace.write("\t\tif (displacement >= 0.3 && displacement < 10.0) {\n")
                    for xbin_i in np.arange(dfr_hist2.GetNbinsX()): 
                        for ybin_i in np.arange(dfr_hist2.GetNbinsY()): 
                            for zbin_i in np.arange(dfr_hist2.GetNbinsZ()): 
                                xbin_low = dfr_hist2.GetXaxis().GetXbins()[xbin_i]
                                xbin_up  = dfr_hist2.GetXaxis().GetXbins()[xbin_i+1]
                                ybin_low = dfr_hist2.GetYaxis().GetXbins()[ybin_i]
                                ybin_up  = dfr_hist2.GetYaxis().GetXbins()[ybin_i+1]
                                zbin_low = dfr_hist2.GetZaxis().GetXbins()[zbin_i]
                                zbin_up  = dfr_hist2.GetZaxis().GetXbins()[zbin_i+1]
                                result   = dfr_hist2.GetBinContent(xbin_i+1, ybin_i+1, zbin_i+1)
                                dfr_namespace.write("\t\t\tif (ptCone >= %f && ptCone < %f && eta >= %f && eta < %f && dr12 >= %f && dr12 < %f) return %f;\n"%(xbin_low,xbin_up,ybin_low,ybin_up,zbin_low,zbin_up,result))
                    dfr_namespace.write("\t\t\treturn 0.;\n")
                    dfr_namespace.write("\t\t}\n")
                    dfr_namespace.write("\t\treturn 0.;\n")
                    dfr_namespace.write("\t}\n")
                    dfr_namespace.write("}\n")
            print 'FakeRateNamespace saved in %s'%(dfr_namespace_dir)
            gROOT.ProcessLine(".L modules/DDE_doublefake.h+")

    def makeNameSpaceSingleFakes(self):
            # import sfr_hist
            f = TFile('modules/DDE_singlefake.root')
            sfr_hist = f.Get('ptCone_eta').GetPrimitive("pt_eta_T_012")

            #prepare a .h file to implement the fakerates into the ROOT namespace
            sfr_namespace_dir = "/home/dehuazhu/HNL/CMSSW_9_4_6_patch1/src/PlotFactory/DataBkgPlots/modules/DDE_singlefake.h"
            with open(sfr_namespace_dir, "w") as sfr_namespace:
                    sfr_namespace.write("// This namespace prepares the singlefakerate measured via DDE.py to be implementable in dataframe for the main plotting tool.\n")
                    sfr_namespace.write("namespace sfr_namespace {\n")
                    sfr_namespace.write("\tdouble getSingleFakeRate(double ptCone, double eta){\n")
                    for xbin_i in np.arange(sfr_hist.GetNbinsX()): 
                        for ybin_i in np.arange(sfr_hist.GetNbinsY()): 
                            xbin_low = sfr_hist.GetXaxis().GetXbins()[xbin_i]
                            xbin_up  = sfr_hist.GetXaxis().GetXbins()[xbin_i+1]
                            ybin_low = sfr_hist.GetYaxis().GetXbins()[ybin_i]
                            ybin_up  = sfr_hist.GetYaxis().GetXbins()[ybin_i+1]
                            result   = sfr_hist.GetBinContent(xbin_i+1, ybin_i+1)
                            sfr_namespace.write("\t\tif (ptCone >= %f && ptCone < %f && eta >= %f && eta < %f) return %f;\n"%(xbin_low,xbin_up,ybin_low,ybin_up,result))
                    sfr_namespace.write("\t\treturn 0.;\n")
                    sfr_namespace.write("\t}\n")
                    sfr_namespace.write("}\n")
            print 'FakeRateNamespace saved in "%s"'%(sfr_namespace_dir)
            gROOT.ProcessLine(".L modules/DDE_singlefake.h+")

def main():
    # define basic config info
    hostname = gethostname()
    if "lxplus" in hostname:
        analysis_dir = '/eos/user/v/vstampf/ntuples/'
   
    if "t3ui0" in hostname:
        analysis_dir = '/work/dezhu/4_production/'

    if "starseeker" in hostname:
        analysis_dir = '/home/dehuazhu/SESSD/4_production/'

    channel = 'mmm'

    # # import ntuples and measure Fakerate, the output is a 2D histogram fakerate map
    fakes = DDE(analysis_dir,hostname,channel) 
    # dfr   = fakes.makeDataFrame()
    # dfr_hist = fakes.measureDFR()
    # dfr_hist = fakes.measureDFR_4D(0.0,0.3)
    # dfr_hist = fakes.measureDFR_4D(0.3,10.0)
    # dfr_hist = fakes.measureSFR()
    # dfr_hist = fakes.testbench()
    # fakes.makeNameSpaceDoubleFakes_4D()
    # fakes.makeNameSpaceDoubleFakes()
    fakes.makeNameSpaceSingleFakes()
    

if __name__ == '__main__':
    main()
