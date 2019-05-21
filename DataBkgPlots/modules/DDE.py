from modules.officialStyle import officialStyle
import plotfactory as pf
from modules.Samples import createSampleLists, setSumWeights
from modules.Selections import getSelection
from ROOT import ROOT, RDataFrame, TH1F, TFile, TTree, TTreeFormula, TCanvas, TPaveText, TBox, gStyle,TChain, gROOT, gSystem
import numpy as np

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

    # def measureFR(self, analysis_dir,server, channel):
    def measureFR(self, drawPlot = False):
        sample_dict = {}
        samples_all, samples_singlefake, samples_doublefake = createSampleLists(analysis_dir=self.analysis_dir, server = self.server, channel=self.channel)
        working_samples = samples_doublefake
        working_samples = setSumWeights(working_samples)
        print('###########################################################')
        print'# measuring doublefakerake...'
        print'# %d samples to be used:'%(len(working_samples))
        print('###########################################################')
        for w in working_samples: print('{:<20}{:<20}'.format(*[w.name,('path: '+w.ana_dir)]))
        #TChain'ing all data samples together
        chain = TChain('tree')
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
        bins_eta    = np.array([0., 0.8, 1.2, 2.4]) 
        # bins_ptCone   = np.arange(0.,70.,1)
        # bins_eta      = np.arange(0.,2.4,0.03)

        selection_baseline      = getSelection(self.channel,'baseline')  
        selection_ttbar         = getSelection(self.channel,'CR_ttbar')  
        selection_DY            = getSelection(self.channel,'CR_DY')  

        selection_LL_correlated = '(' + ' & '\
                                    .join([\
                                    selection_baseline,\
                                    getSelection(self.channel,'LL_correlated')\
                                    ]) + ')' 
        selection_TT_correlated = '(' + ' & '\
                                    .join([\
                                    selection_baseline,\
                                    getSelection(self.channel,'LL_correlated'),\
                                    getSelection(self.channel,'TT')\
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

        ########################################
        # This section is for tinkering, comment everythig out if you want to do normal mode
        # h_baseline = dataframe\
                # .Filter(selection_baseline)\
                # .Histo2D(('h_baseline','h_baseline',20,10.,100.,20,0.,1.),'hnl_hn_vis_pt','hnl_dr_12')
                # .Histo2D(('h_TT_correlated','h_TT_correlated',len(bins_ptCone)-1,bins_ptCone, len(bins_eta)-1, bins_eta),'l1_ptCone','l1_eta')
        # h_baseline = dataframe\
                # .Histo2D(('h_TT_correlated','h_TT_correlated',len(bins_ptCone)-1,bins_ptCone, len(bins_eta)-1, bins_eta),'ptCone','abs_hnl_hn_vis_eta')
                # .Histo2D(('h_baseline','h_baseline',20,10.,100.,20,0.01,.8),'hnl_hn_vis_pt','l1_reliso_rho_03')
                # .Histo2D(('h_baseline','h_baseline',20,10.,100.,20,0.01,.8),'hnl_hn_vis_pt','hnl_dr_12')
        # h_baseline.SetTitle(';DiMuon p_T [GeV]; #DeltaR(#mu1, #mu2)')
        # h_baseline.SetTitle(';DiMuon p_T [GeV]; l1_reliso_rho_03')
        # h_baseline.SetTitle(';ptCone [GeV]; dimuon #eta')


        # h_LL_correlated = dataframe\
                # .Filter(selection_LL_correlated)\
                # .Histo1D(('h_LL_correlated','h_LL_correlated',10,0.,5.),'hnl_2d_disp','w')
                # .Histo1D(('h_LL_correlated','h_LL_correlated',10,0.,10.),'abs_l1_jet_flavour_parton','w')
                # .Histo1D(('h_LL_correlated','h_LL_correlated',10,0.,10.),'nbj','w')
                # .Histo1D(('h_LL_correlated','h_LL_correlated',10,-3.14,3.14),'hnl_hn_vis_phi','w')
                # .Histo1D(('h_LL_correlated','h_LL_correlated',20,0.,100.),'hnl_hn_vis_pt','w')
                # .Histo1D(('h_LL_correlated','h_LL_correlated',10,0.,10.),'nj','w')
                # .Histo1D(('h_LL_correlated','h_LL_correlated',20,0.,100.),'ptCone','w')
                # .Histo1D(('h_LL_correlated','h_LL_correlated',10,0.,4.),'abs_l1_eta','w')
                # .Histo1D(('h_LL_correlated','h_LL_correlated',10,0.,4.),'abs_l2_eta','w')
                # .Histo1D(('h_LL_correlated','h_LL_correlated',10,0.,4.),'abs_hnl_hn_eta','w')
                # .Histo1D(('h_LL_correlated','h_LL_correlated',10,0.,4.0),'abs_hnl_hn_vis_eta','w')

        # h_TT_correlated = dataframe\
                # .Filter(selection_TT_correlated)\
                # .Histo1D(('h_TT_correlated','h_TT_correlated',10,0.,5.),'hnl_2d_disp','w')
                # .Histo1D(('h_TT_correlated','h_TT_correlated',10,0.,10.),'abs_l1_jet_flavour_parton','w')
                # .Histo1D(('h_TT_correlated','h_TT_correlated',10,0.,10.),'nbj','w')
                # .Histo1D(('h_TT_correlated','h_TT_correlated',10,-3.14,3.14),'hnl_hn_vis_phi','w')
                # .Histo1D(('h_TT_correlated','h_TT_correlated',20,0.,100.),'hnl_hn_vis_pt','w')
                # .Histo1D(('h_TT_correlated','h_TT_correlated',10,0.,10.),'nj','w')
                # .Histo1D(('h_TT_correlated','h_TT_correlated',20,0.,100.),'ptCone','w')
                # .Histo1D(('h_LL_correlated','h_LL_correlated',10,0.,4.),'abs_l1_eta','w')
                # .Histo1D(('h_LL_correlated','h_LL_correlated',10,0.,4.),'abs_l2_eta','w')
                # .Histo1D(('h_LL_correlated','h_LL_correlated',10,0.,4.),'abs_hnl_hn_eta','w')
                # .Histo1D(('h_LL_correlated','h_LL_correlated',10,0.,4.0),'abs_hnl_hn_vis_eta','w')
        #name the axis, also initiate the dataframe call
        # h_TT_correlated.SetTitle(';abs_l2_eta; fakerate (TTL)')
        # h_TT_correlated.SetTitle(';abs_l1_eta; fakerate (TTL)')
        # h_TT_correlated.SetTitle(';abs_hnl_hn_eta; fakerate (TTL)')
        # h_TT_correlated.SetTitle(';abs_hnl_hn_vis_eta; fakerate (TTL)')
        # h_TT_correlated.SetTitle(';ptCone [GeV]; fakerate (TTL)')
        # h_TT_correlated.SetTitle(';nj; fakerate (TTL)')
        # h_TT_correlated.SetTitle(';nbj; fakerate (TTL)')
        # h_TT_correlated.SetTitle(';hnl_hn_vis_pt; fakerate (TTL)')
        # h_TT_correlated.SetTitle(';hnl_hn_vis_phi; fakerate (TTL)')
        # h_TT_correlated.SetTitle(';abs_l1_jet_flavour_parton; fakerate (TTL)')
        # h_TT_correlated.SetTitle(';hnl_2d_disp; fakerate (TTL)')


        # h_LL_correlated = dataframe\
                # .Filter(selection_LL_correlated)\
                # .Histo2D(('h_LL_correlated','h_LL_correlated',6,0.,3.,6,10.,70.),'hnl_2d_disp','ptCone','w')
        # h_TT_correlated = dataframe\
                # .Filter(selection_TT_correlated)\
                # .Histo2D(('h_TT_correlated','h_TT_correlated',6,0.,3.,6,10.,70.),'hnl_2d_disp','ptCone','w')
        #name the axis, also initiate the dataframe call
        # h_LL_correlated.SetTitle(';l1_eta; dimuon #eta')
        # h_TT_correlated.SetTitle(';hnl_2d_disp; ptCone')
        ########################################

        # preparing the histo and save it into a .root file
        dfr_TH2_dir = '/home/dehuazhu/HNL/CMSSW_9_4_6_patch1/src/PlotFactory/DataBkgPlots/modules/DDE_doublefake.root' 
        dfr_hist = h_TT_correlated.Clone()
        # hist = h_LL_correlated.Clone()
        # hist = h_baseline.Clone()
        dfr_hist.Divide(h_LL_correlated.Clone())
        dfr_hist.SaveAs(dfr_TH2_dir)

        #prepare a .h file to implement the fakerates into the ROOT namespace
        dfr_namespace_dir = "/home/dehuazhu/HNL/CMSSW_9_4_6_patch1/src/PlotFactory/DataBkgPlots/modules/DDE_doublefake.h"
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
        print 'FakeRateMap saved in "%s"'%(dfr_TH2_dir)
        print 'FakeRateNamespace saved in "%s"'%(dfr_namespace_dir)
        gROOT.ProcessLine(".L modules/DDE_doublefake.h+")

        # draw the histo if required 
        if drawPlot == True:
            can = TCanvas('can', '')
            # hist.Draw('colzTextE')
            dfr_hist.Draw('colz')
            # hist.Draw()
            pf.showlumi('%d entries'%(dfr_hist.GetEntries()))
            # pf.showlogopreliminary()
            can.Update()
            set_trace()

        return hist


def main():
    # define basic config into
    analysis_dir = '/home/dehuazhu/SESSD/4_production/'
    server = 'starseeker'
    channel = 'mmm'

    # import ntuples and measure Fakerate, the output is a 2D histogram fakerate map
    doublefake = DDE(analysis_dir,server,channel) 
    dfr_hist = doublefake.measureFR(drawPlot = False)
    

if __name__ == '__main__':
    main()
