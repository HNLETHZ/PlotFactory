import ROOT
import numpy as np
import root_pandas
import pandas
from copy import deepcopy as dc
from root_numpy import tree2array, array2root
from collections import OrderedDict

ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch(True)

class Var(object):
    '''
    '''
    def __init__(self, var, bins, xtitle, ytitle, label):
        self.var    = var
        self.bins   = bins
        self.xtitle = xtitle
        self.ytitle = ytitle
        self.label  = label
        self.histo  = ROOT.TH1F(self.label, '', len(self.bins)-1, bins)
        self.histo.GetXaxis().SetTitle(self.xtitle)
        self.histo.GetYaxis().SetTitle(self.ytitle)


class Flavours(object):
    def __init__(self, keys, selections, colours, labels):
        self.keys       = keys
        self.selections = selections
        self.colours    = colours
        self.labels     = labels
    
    def GetKeys(self):
        return self.keys    

    def GetSelections(self):
        return OrderedDict(zip(self.keys, self.selections))    

    def GetColours(self):
        return OrderedDict(zip(self.keys, self.colours))    

    def GetLabels(self):
        return OrderedDict(zip(self.keys, self.labels))    


class Distributions(object):
    '''
    '''
    def __init__(self, tree, common_selection, flavours, variables, treename='tree'):
        self.tree               = tree
        self.common_selection   = common_selection   
        self.flavours           = flavours 
        self.variables          = variables
#         print 'skimming tree based on selection\n', common_selection
#         import pdb ; pdb.set_trace()
#         self.skimmed_tree       = array2root(tree2array(tree, selection=self.common_selection))             
#         print '... done'
    
    def ProducePlots(self):
        histos = OrderedDict()
        for ivar in self.variables:
            print 'plotting', ivar.label
            histos[ivar.label] = OrderedDict()
            for ii in self.flavours.keys:
                selection = '&'.join([self.common_selection, self.flavours.GetSelections()[ii]])
#                 hist_name = str(hash(ivar.label + '#' + selection))
                hist_name = ivar.label + '#' + ii
                hist = ivar.histo.Clone()
                hist.SetName(str(hist_name))
                hist.SetLineColor(self.flavours.GetColours()[ii])
                print '\t', ii, '\t', hist_name
                tree.Draw(ivar.var + '>>' + hist_name, selection)
                histos[ivar.label][ii] = hist
        return histos

class Plotter(object):
    '''
    '''
    def __init__(self, histos, name, labels, legpos='topright'):
        self.histos = histos
        self.name = name
        self.labels = labels
        self.legpos = legpos
        self.c1 = ROOT.TCanvas('c1', '', 700, 700)
        self.c1.SetLeftMargin(0.15)
        self.c1.SetBottomMargin(0.15)
    
    def CreateLegend(self, legpos=None):
        position = legpos if legpos else self.legpos
        if position=='topright'   : self.legend = ROOT.TLegend(.7,.7,.88,.8 )
        if position=='topleft'    : self.legend = ROOT.TLegend(.6,.6,.88,.88) # FIXME!
        if position=='bottomright': self.legend = ROOT.TLegend(.6,.3,.88,.4 ) # FIXME!
        if position=='bottomleft' : self.legend = ROOT.TLegend(.6,.6,.88,.88) # FIXME!
        self.legend.SetBorderSize(0)

    def Plots(self, norm=False, cdf=False, savepdf=True):
        toreturn = [] 
        self.c1.Draw()
        self.CreateLegend()
        jj = 0
        for k, v in self.histos.iteritems():
            vv = v # decouple from original histogram
            self.legend.AddEntry(vv, self.labels[k], 'L')
            if norm: vv.Scale(1./vv.Integral())
            if cdf: vv = vv.GetCumulative() 
            vv.SetMinimum(0.)
            vv.Draw('hist' + (jj>0)*'same')
            jj += 1
            toreturn.append(vv)
        self.legend.Draw('same')   
        plotname = self.name 
        if norm: plotname += '_norm'
        if cdf : plotname += '_cdf'
        plotname += '.pdf'
        if savepdf: self.c1.SaveAs(plotname)
        return toreturn
            
    def PlotsCDFRatio(self, logx=False):
        self.c1.Draw()
        self.CreateLegend()
        
        reference_key   = self.histos.keys  ()[0]
        reference_histo = self.histos.values()[0]

        jj = 0
        for k, v in self.histos.iteritems():
            if reference_histo.GetName() == v.GetName(): continue
            num = v.GetCumulative()
            den = reference_histo.GetCumulative()

            ratio = num.Clone()
            
            ratio.Divide(num, den)
            
            ratio.GetYaxis().SetTitle('1/%s' %k)
            
            if logx: ROOT.gPad.SetLogx(True)
            else: ROOT.gPad.SetLogx(False)

            self.legend.AddEntry(ratio, self.labels[k], 'L')
            ratio.Draw('hist' + (jj>0)*'same')
            jj += 1
                
        self.legend.Draw('same')   
        plotname = self.name 
        plotname += '_cdf_ratio'
        plotname += '.pdf'
        self.c1.SaveAs(plotname)
#         return h1, h2


                    
                

##########################################################################################
##########################################################################################
##########################################################################################

if __name__ == '__main__':

    tree = ROOT.TChain('tree')
    tree.Add('/work/dezhu/4_production/production_20190306_BkgMC/mem/ntuples/DYBB/HNLTreeProducer/tree.root'              )
    tree.Add('/work/dezhu/4_production/production_20190306_BkgMC/mem/ntuples/DYJetsToLL_M50/HNLTreeProducer/tree.root'    )
    tree.Add('/work/dezhu/4_production/production_20190306_BkgMC/mem/ntuples/DYJetsToLL_M50_ext/HNLTreeProducer/tree.root')
    tree.Add('/work/dezhu/4_production/production_20190306_BkgMC/mem/ntuples/TTJets/HNLTreeProducer/tree.root'            )

    ######################################################################################
    baseline_selection = '&'.join([
        'l0_pt>27 & abs(l0_eta)<2.4 & l0_id_t & l0_dz<0.2 & l0_dxy<0.05 & l0_reliso_rho_04<0.2', # l0 genuine
        'l2_pt>15 & abs(l2_eta)<2.4 & l2_id_t & l2_dz<0.2 & l2_dxy<0.05 & l2_reliso_rho_04<0.2', # l2 genuine 
        'hnl_q_02==0'                                                                          , # opposite charge
        'l1_pt>5 & abs(l1_eta)<2.5 & l1_dz<0.2 & l1_dxy>0.05'                                  , # l1 kinematics and impact parameter
        'l1_gen_match_pdgid!=22'                                                               , # no conversions 
        'hnl_dr_01>0.3 & hnl_dr_12>0.3'                                                        , # distance from genuine leptons
#         'l1_MediumNoIso==1'                                                                    , # medium iso
    ])

    ######################################################################################
    flavours = Flavours(
        keys = [
            'udsgx', 
            'cb'   , 
        ],
        selections = [
            '(abs(l1_jet_flavour_parton)!=4 & abs(l1_jet_flavour_parton)!=5 & abs(l1_jet_flavour_parton)>-99)' ,
            '(abs(l1_jet_flavour_parton)==4 | abs(l1_jet_flavour_parton)==5)' ,
        ],
        colours = [    
            ROOT.kRed       ,
            ROOT.kBlue      ,
        ],
        labels = [
            'light, gluon and other',
            'c and b',
        ]
    )

    ######################################################################################
    variables = [
        Var(var='l1_pt * (1. + l0_reliso_rho_04)', bins=np.linspace( 0  , 100  ,  41), xtitle='p_{T} cone [GeV]'                    , ytitle='a.u.', label='l1_pt_cone'           ),
        Var(var='l1_eta'                         , bins=np.linspace(-2.5,   2.5,  21), xtitle='#eta'                                , ytitle='a.u.', label='l1_eta'               ),
        Var(var='l1_reliso_rho_04'               , bins=np.linspace( 0  ,  10  , 201), xtitle='#rho-corrected I^{rel} #DeltaR = 0.4', ytitle='a.u.', label='l1_reliso_rho_04'     ),
        Var(var='l1_jet_flavour_parton'          , bins=np.linspace(-100,  25  , 126), xtitle='parton flavour'                      , ytitle='a.u.', label='l1_jet_flavour_parton'),
    ]


    ######################################################################################
    #      CHECK DIFFERENT ETA BINS
    ######################################################################################
    eta_bins = OrderedDict()
    eta_bins['1p5to2p5' ] = 'abs(l1_eta)>1.5'
    eta_bins['0p8to1p5' ] = 'abs(l1_eta)>0.8 & abs(l1_eta)<=1.5'
    eta_bins['0to0p8'   ] = 'abs(l1_eta)<=0.8'
    eta_bins['inclusive'] = '1'

    e_ids_bins = OrderedDict()
    e_ids_bins['NoID'         ] = '1'
    e_ids_bins['LooseNoIso'   ] = 'l1_LooseNoIso'
    e_ids_bins['MediumNoIso'  ] = 'l1_MediumNoIso'
    e_ids_bins['MediumWithIso'] = 'l1_MediumWithIso'


    # save histograms
    outfile = ROOT.TFile.Open('electron_single_fr.root', 'recreate')
    outfile.cd()
    
    for k, v in eta_bins.iteritems():
    
        outfile.mkdir(k)
        outfile.cd(k)
        
    
        for kk, vv in e_ids_bins.iteritems():

            outfile.mkdir('/'.join([k,kk]))
            outfile.cd('/'.join([k,kk]))

            print 'now plotting eta:', k, '\telectron ID', kk
            ######################################################################################
            distro = Distributions(
                tree             = tree,
                common_selection = baseline_selection + '&' + v + '&' + vv,
                flavours         = flavours,
                variables        = variables,
            )

            ######################################################################################
            histos = distro.ProducePlots()

            ######################################################################################    
            for ivar in variables:
                # produce plots
                plotter   = Plotter(histos[ivar.label], '%s_light_vs_heavy_mediumNoIso_eta_%s_id_%s' %(ivar.label, k, kk), flavours.GetLabels(), legpos='topright')
                plots     = plotter.Plots(savepdf=False)    
                for iplot in plots:
                    iplot.SetName(iplot.GetName())
                    iplot.Write()

                if ivar.label == 'l1_reliso_rho_04':
                    plotscdf  = plotter.Plots(norm=True, cdf=True, savepdf=False) 
                    for iplot in plotscdf:
                        iplot.SetName(iplot.GetName().replace('_cumulative', '_cdf'))
                        iplot.Write()
            
#             plotter.PlotsCDFRatio(logx=True)   


            outfile.cd('..')
        outfile.cd('..')

    outfile.Close()

