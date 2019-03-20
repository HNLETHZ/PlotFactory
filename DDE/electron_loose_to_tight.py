import ROOT
import pickle
import numpy as np
from root_numpy import hist2array
from collections import OrderedDict

ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch(True)
ROOT.TH1.SetDefaultSumw2()

tree = ROOT.TChain('tree')
tree.Add('/work/dezhu/4_production/production_20190306_BkgMC/mem/ntuples/DYBB/HNLTreeProducer/tree.root'              )
tree.Add('/work/dezhu/4_production/production_20190306_BkgMC/mem/ntuples/DYJetsToLL_M50/HNLTreeProducer/tree.root'    )
tree.Add('/work/dezhu/4_production/production_20190306_BkgMC/mem/ntuples/DYJetsToLL_M50_ext/HNLTreeProducer/tree.root')
tree.Add('/work/dezhu/4_production/production_20190306_BkgMC/mem/ntuples/TTJets/HNLTreeProducer/tree.root'            )

outfile = ROOT.TFile.Open('electron_single_fr_tight_to_loose.root', 'recreate')

baseline_selection = '&'.join([
    'l0_pt>27 & abs(l0_eta)<2.4 & l0_id_t & l0_dz<0.2 & l0_dxy<0.05 & l0_reliso_rho_04<0.2', # l0 genuine
    'l2_pt>15 & abs(l2_eta)<2.4 & l2_id_t & l2_dz<0.2 & l2_dxy<0.05 & l2_reliso_rho_04<0.2', # l2 genuine 
    'hnl_q_02==0'                                                                          , # opposite charge
    'l1_pt>5 & abs(l1_eta)<2.5 & l1_dz<0.2 & l1_dxy>0.05'                                  , # l1 kinematics and impact parameter
    'l1_gen_match_pdgid!=22'                                                               , # no conversions 
    'hnl_dr_01>0.3 & hnl_dr_12>0.3'                                                        , # distance from genuine leptons
])

tight_selection = '&'.join([
    'l1_MediumNoIso==1'   , # medium ID
    'l1_reliso_rho_04<0.2', # electron iso
])

no_tight_selection = '!(%s)' %tight_selection

flavour_selections = OrderedDict()
flavour_selections['heavy'] = '(abs(l1_jet_flavour_parton)==4 | abs(l1_jet_flavour_parton)==5)'
flavour_selections['light'] = '(abs(l1_jet_flavour_parton)!=4 & abs(l1_jet_flavour_parton)!=5 & abs(l1_jet_flavour_parton)>-99)'

eta_bins = OrderedDict()
eta_bins['0to0p8'   ] = ['l1_reliso_rho_04<0.45', 'abs(l1_eta)<=0.8'                  ]
eta_bins['0p8to1p5' ] = ['l1_reliso_rho_04<0.60', 'abs(l1_eta)>0.8 & abs(l1_eta)<=1.5']
eta_bins['1p5to2p5' ] = ['l1_reliso_rho_04<0.50', 'abs(l1_eta)>1.5'                   ]

bins = np.array([0., 5., 10., 15., 40., 100.])
c1 = ROOT.TCanvas('c1', '', 700, 700)

weights = OrderedDict()

for k, v in eta_bins.iteritems():
    histos = OrderedDict()
    histos['tight'      ] = ROOT.TH1F('ptcone_tight'      , '', len(bins)-1, bins)
    histos['loose'      ] = ROOT.TH1F('ptcone_loose'      , '', len(bins)-1, bins)

    histos['tight_heavy'] = ROOT.TH1F('ptcone_tight_heavy', '', len(bins)-1, bins)
    histos['loose_heavy'] = ROOT.TH1F('ptcone_loose_heavy', '', len(bins)-1, bins)

    histos['tight_light'] = ROOT.TH1F('ptcone_tight_light', '', len(bins)-1, bins)
    histos['loose_light'] = ROOT.TH1F('ptcone_loose_light', '', len(bins)-1, bins)
    
    sel_t   = '&'.join([baseline_selection, tight_selection   , v[1]      ])
    sel_l   = '&'.join([baseline_selection, no_tight_selection, v[0], v[1]])

    sel_t_h = '&'.join([baseline_selection, tight_selection   , v[1]      , flavour_selections['heavy']])
    sel_l_h = '&'.join([baseline_selection, no_tight_selection, v[0], v[1], flavour_selections['heavy']])

    sel_t_l = '&'.join([baseline_selection, tight_selection   , v[1]      , flavour_selections['light']])
    sel_l_l = '&'.join([baseline_selection, no_tight_selection, v[0], v[1], flavour_selections['light']])
    
    tree.Draw('l1_pt * (1. + l0_reliso_rho_04) >> ptcone_tight', sel_t)
    tree.Draw('l1_pt * (1. + l0_reliso_rho_04) >> ptcone_loose', sel_l)

    tree.Draw('l1_pt * (1. + l0_reliso_rho_04) >> ptcone_tight_heavy', sel_t_h)
    tree.Draw('l1_pt * (1. + l0_reliso_rho_04) >> ptcone_loose_heavy', sel_l_h)

    tree.Draw('l1_pt * (1. + l0_reliso_rho_04) >> ptcone_tight_light', sel_t_l)
    tree.Draw('l1_pt * (1. + l0_reliso_rho_04) >> ptcone_loose_light', sel_l_l)
    
    ratio = histos['tight'].Clone()
    ratio.Divide(histos['tight'], histos['loose'])

    ratio_h = histos['tight_heavy'].Clone()
    ratio_h.Divide(histos['tight_heavy'], histos['loose_heavy'])

    ratio_l = histos['tight_light'].Clone()
    ratio_l.Divide(histos['tight_light'], histos['loose_light'])

    ratio.SetTitle(k)
    
    for iratio in [ratio, ratio_l, ratio_h]:
        iratio.SetMinimum(0.)
        iratio.SetMaximum(0.25)
        iratio.GetXaxis().SetTitle('p_{T} cone [GeV]')
        iratio.GetYaxis().SetTitle('tight/loose ratio')
        iratio.GetYaxis().SetTitleOffset(0.9)
    ratio.SetMarkerStyle(8)
    ratio.SetLineColor(ROOT.kBlack)
    ratio.Draw('ep')

    ratio_l.SetMarkerStyle(21)
    ratio_h.SetMarkerStyle(22)

    ratio_l.SetMarkerColor(ROOT.kRed)
    ratio_h.SetMarkerColor(ROOT.kBlue)

    ratio_l.SetLineColor(ROOT.kRed)
    ratio_h.SetLineColor(ROOT.kBlue)
    
    ratio_l.Draw('ep same')
    ratio_h.Draw('ep same')

    ROOT.gPad.SetGridx(True)
    ROOT.gPad.SetGridy(True)
    ROOT.gPad.Update()
    ROOT.gPad.SaveAs('tight_to_loose_%s.pdf' %k)

    ratio  .SetName('tight_to_loose_%s' %k)
    ratio_l.SetName('tight_to_loose_light_%s' %k)
    ratio_h.SetName('tight_to_loose_heavy_%s' %k)

    outfile.cd()

    ratio  .Write()
    ratio_l.Write()
    ratio_h.Write()

    weights[k] = OrderedDict()
    weights[k]['inclusive'] = hist2array(ratio)
    weights[k]['heavy'    ] = hist2array(ratio_h)
    weights[k]['light'    ] = hist2array(ratio_l)

outfile.Close()    

with open('electron_single_fr_tight_to_loose.pck', 'w+') as weight_file:
    pickle.dump(weights, weight_file)


## READ WEIGHTS with
# import pickle
# 
# with open('electron_single_fr_tight_to_loose.pck') as f1:
#     weights = pickle.load(f1)

]
]
