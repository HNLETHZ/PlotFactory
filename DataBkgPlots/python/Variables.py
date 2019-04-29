from math import pi

from CMGTools.HNL.plotter.PlotConfigs import VariableCfg as VCfg

from CMGTools.HNL.plotter.binning import binning_svfitMass_finer, binning_mttotal, binning_mttotal_fine

generic_vars = [
    VCfg(name='_norm_', drawname='1.', binning={'nbinsx':5, 'xmin':-1.5, 'xmax':3.5}, unit='', xtitle='Normalisation'),
    VCfg(name='svfit_mass', binning=binning_svfitMass_finer, unit='GeV', xtitle='m_{#tau#tau}'),
    VCfg(name='svfit_transverse_mass', binning={'nbinsx':40, 'xmin':0., 'xmax':300.}, unit='GeV', xtitle='M_{T}^{SVFit}'),
    VCfg(name='mt_total', binning={'nbinsx':40, 'xmin':0., 'xmax':800.}, unit='GeV', xtitle='M_{T}^{total}'),
    VCfg(name='mt_total_mssm', drawname='mt_total', binning=binning_mttotal, unit='GeV', xtitle='M_{T}^{total}'),
    VCfg(name='mt_total_mssm_fine', drawname='mt_total', binning=binning_mttotal_fine, unit='GeV', xtitle='M_{T}^{total}'),
    VCfg(name='max_mt', drawname='max(mt, mt_leg2)', binning={'nbinsx':60, 'xmin':0., 'xmax':600.}, unit='GeV', xtitle='max(M_{T} (leg 1), M_{T} (leg 2))'),
    VCfg(name='mvis', binning=binning_svfitMass_finer, unit='GeV', xtitle='m_{vis}'),
    VCfg(name='mvis_fine', drawname='mvis', binning={'nbinsx':200, 'xmin':0., 'xmax':200.}, unit='GeV', xtitle='m_{vis}'),
    VCfg(name='mvis_extended', drawname='mvis', binning={'nbinsx':50, 'xmin':0., 'xmax':1000.}, unit='GeV', xtitle='m_{vis}'),
    VCfg(name='mt', binning={'nbinsx':60, 'xmin':0., 'xmax':300.}, unit='GeV', xtitle='m_{T}'),
    VCfg(name='pfmet_mt1', binning={'nbinsx':50, 'xmin':0., 'xmax':200.}, unit='GeV', xtitle='m_{T} (PF)'),
    VCfg(name='puppimet_mt1', binning={'nbinsx':50, 'xmin':0., 'xmax':200.}, unit='GeV', xtitle='m_{T} (Puppet)'),
    VCfg(name='mt_leg2', binning={'nbinsx':60, 'xmin':0., 'xmax':300.}, unit='GeV', xtitle='m_{T} leg 2'),
    VCfg(name='pfmet_mt2', binning={'nbinsx':50, 'xmin':0., 'xmax':200.}, unit='GeV', xtitle='m_{T} leg 2 (PF)'),
    VCfg(name='puppimet_mt2', binning={'nbinsx':50, 'xmin':0., 'xmax':200.}, unit='GeV', xtitle='m_{T} leg 2(Puppet)'),
    VCfg(name='mt_sum', drawname='mt + mt_leg2', binning={'nbinsx':60, 'xmin':0., 'xmax':1000.}, unit='GeV', xtitle='Sum m_{T} (MET-leg1, MET-leg2)'),
    VCfg(name='n_vertices', binning={'nbinsx':51, 'xmin':-0.5, 'xmax':50.5}, unit=None, xtitle='N_{vertices}'),
    VCfg(name='rho', binning={'nbinsx':50, 'xmin':0., 'xmax':50.}, unit='GeV', xtitle='#rho'),
    VCfg(name='n_jets', binning={'nbinsx':12, 'xmin':-0.5, 'xmax':11.5}, unit=None, xtitle='N_{jets}'),
    VCfg(name='n_jets_20', binning={'nbinsx':12, 'xmin':-0.5, 'xmax':11.5}, unit=None, xtitle='N_{jets} (20 GeV)'),
    VCfg(name='n_jets_puid', binning={'nbinsx':12, 'xmin':-0.5, 'xmax':11.5}, unit=None, xtitle='N_{jets} (PU ID)'),
    VCfg(name='n_jets_csvl', binning={'nbinsx':12, 'xmin':-0.5, 'xmax':11.5}, unit=None, xtitle='N_{jets} (CSV loose; no SF)'),
    VCfg(name='n_bjets', binning={'nbinsx':12, 'xmin':-0.5, 'xmax':11.5}, unit=None, xtitle='N_{b jets}'),
    VCfg(name='met_phi', binning={'nbinsx':40, 'xmin':-3.141593, 'xmax':3.141593}, unit=None, xtitle='E_{T}^{miss} #Phi'),
    VCfg(name='pthiggs', binning={'nbinsx':50, 'xmin':0., 'xmax':300.}, unit='GeV', xtitle='Higgs boson p_{T}'),
    VCfg(name='met_pt', binning={'nbinsx':60, 'xmin':0., 'xmax':300.}, unit='GeV', xtitle='E_{T}^{miss}'),
    VCfg(name='pfmet_pt', binning={'nbinsx':60, 'xmin':0., 'xmax':300.}, unit='GeV', xtitle='E_{T}^{miss} (PF)'),
    VCfg(name='puppimet_pt', binning={'nbinsx':60, 'xmin':0., 'xmax':300.}, unit='GeV', xtitle='E_{T}^{miss} (Puppet)'),
    VCfg(name='met_sig', drawname='met_pt/sqrt(met_cov00 + met_cov11)', binning={'nbinsx':50, 'xmin':0., 'xmax':15.}, unit='GeV', xtitle='MVA E_{T}^{miss} significance'),
    
    VCfg(name='vbf_mjj', binning={'nbinsx':40, 'xmin':0, 'xmax':1000.}, unit='GeV', xtitle='m_{jj}'),
    VCfg(name='vbf_deta', binning={'nbinsx':40, 'xmin':-7., 'xmax':7.}, unit=None, xtitle='#Delta#eta (VBF)'),
    VCfg(name='vbf_n_central', binning={'nbinsx':4, 'xmin':-0.5, 'xmax':3.5}, unit=None, xtitle='N_{central jets}'),
    VCfg(name='vbf_dphidijethiggs', binning={'nbinsx':40, 'xmin':-3.1415927, 'xmax':3.1415927}, unit=None, xtitle='#Delta#Phi(dijet, Higgs)'),
    VCfg(name='vbf_mindetajetvis', binning={'nbinsx':40, 'xmin':0, 'xmax':10.}, unit=None, xtitle='Min(#Delta#eta jet, visible system)'),
    VCfg(name='vbf_dijetpt', binning={'nbinsx':50, 'xmin':0, 'xmax':1000.}, unit='GeV', xtitle='Dijet p_{T}'),
    VCfg(name='vbf_jdphi', binning={'nbinsx':40, 'xmin':-3.1415927, 'xmax':3.1415927}, unit=None, xtitle='#Delta#Phi(leading jets)'),
    VCfg(name='jet1_pt', binning={'nbinsx':60, 'xmin':0., 'xmax':300.}, unit='GeV', xtitle='jet 1 p_{T}'),
    VCfg(name='jet1_flavour_parton', binning={'nbinsx':27, 'xmin':-5.5, 'xmax':21.5}, unit='', xtitle='jet 1 parton flavour'),
    VCfg(name='jet2_pt', binning={'nbinsx':40, 'xmin':0., 'xmax':200.}, unit='GeV', xtitle='jet 2 p_{T}'),
    VCfg(name='jet1_eta', binning={'nbinsx':50, 'xmin':-5., 'xmax':5.}, unit=None, xtitle='jet 1 #eta'),
    VCfg(name='jet1_eta_puid', drawname='jet1_eta - 100*(!jet1_id_pu)', binning={'nbinsx':50, 'xmin':-5., 'xmax':5.}, unit=None, xtitle='jet 1 #eta (PU ID)'),
    VCfg(name='jet1_eta_pu', drawname='jet1_eta - 100*(jet1_id_pu)', binning={'nbinsx':50, 'xmin':-5., 'xmax':5.}, unit=None, xtitle='jet 1 #eta (PU)'),
    VCfg(name='jet1_eta_puid_medium', drawname='jet1_eta - 100*(jet1_id_pu<1.5)', binning={'nbinsx':50, 'xmin':-5., 'xmax':5.}, unit=None, xtitle='jet 1 #eta (PU medium)'),
    VCfg(name='jet1_eta_puid_tight', drawname='jet1_eta - 100*(jet1_id_pu<2.5)', binning={'nbinsx':50, 'xmin':-5., 'xmax':5.}, unit=None, xtitle='jet 1 #eta (PU tight)'),
    VCfg(name='jet2_eta', binning={'nbinsx':40, 'xmin':-5., 'xmax':5.}, unit=None, xtitle='jet 2 #eta'),
    VCfg(name='jet2_eta_puid', drawname='jet2_eta - 100*(!jet2_id_pu)', binning={'nbinsx':40, 'xmin':-5., 'xmax':5.}, unit=None, xtitle='jet 2 #eta (PU ID)'),
    VCfg(name='jet2_eta_pu', drawname='jet2_eta - 100*(jet2_id_pu)', binning={'nbinsx':40, 'xmin':-5., 'xmax':5.}, unit=None, xtitle='jet 2 #eta (PU)'),
    VCfg(name='bjet1_pt', binning={'nbinsx':60, 'xmin':0., 'xmax':300.}, unit='GeV', xtitle='b jet 1 p_{T}'),
    VCfg(name='bjet2_pt', binning={'nbinsx':40, 'xmin':0., 'xmax':200.}, unit='GeV', xtitle='b jet 2 p_{T}'),
    VCfg(name='bjet1_eta', binning={'nbinsx':40, 'xmin':-5., 'xmax':5.}, unit=None, xtitle='b jet 1 #eta'),
    VCfg(name='bjet2_eta', binning={'nbinsx':40, 'xmin':-5., 'xmax':5.}, unit=None, xtitle='b jet 2 #eta'),
    VCfg(name='jet1_csv', binning={'nbinsx':40, 'xmin':0., 'xmax':1.00001}, unit=None, xtitle='jet 1 CSV'),
    VCfg(name='jet2_csv', binning={'nbinsx':40, 'xmin':0., 'xmax':1.00001}, unit=None, xtitle='jet 2 CSV'),
    VCfg(name='bjet1_csv', binning={'nbinsx':40, 'xmin':0., 'xmax':1.00001}, unit=None, xtitle='b jet 1 CSV'),
    VCfg(name='bjet2_csv', binning={'nbinsx':40, 'xmin':0., 'xmax':1.00001}, unit=None, xtitle='b jet 2 CSV'),
    VCfg(name='pzeta_vis', binning={'nbinsx':50, 'xmin':0., 'xmax':250.}, unit=None, xtitle='p^{#zeta}_{vis} (GeV)'),
    VCfg(name='pzeta_met', binning={'nbinsx':50, 'xmin':-150., 'xmax':250.}, unit=None, xtitle='p^{#zeta}_{MET} (GeV)'),
    VCfg(name='pzeta_disc', binning={'nbinsx':40, 'xmin':-200., 'xmax':200.}, unit=None, xtitle='p^{#zeta}_{disc} (GeV)'),

    VCfg(name='delta_phi_j1_met', drawname='abs(TVector2::Phi_mpi_pi(met_phi - jet1_phi))+ 20*(jet1_phi<-50)', binning={'nbinsx':40, 'xmin':0, 'xmax':3.141593}, unit=None, xtitle='#Delta#Phi(E_{T}^{miss}, jet1) '),
    VCfg(name='delta_phi_j2_met', drawname='abs(TVector2::Phi_mpi_pi(met_phi - jet2_phi)) + 20*(jet2_phi<-50)', binning={'nbinsx':40, 'xmin':0, 'xmax':3.141593}, unit=None, xtitle='#Delta#Phi(E_{T}^{miss}, jet2)'),
    # VCfg(name='min_delta_phi_j1j2_met', drawname='min(abs(TVector2::Phi_mpi_pi(met_phi - jet2_phi)) + 20*(jet2_phi<-50), abs(TVector2::Phi_mpi_pi(met_phi - jet1_phi))+ 20*(jet1_phi<-50))', binning={'nbinsx':40, 'xmin':0, 'xmax':3.141593}, unit=None, xtitle='min(#Delta#Phi(E_{T}^{miss}, jet1/2)'),
    VCfg(name='delta_phi_l1l2_met', drawname="abs(TVector2::Phi_mpi_pi(TMath::ATan((l1_pt*sin(l1_phi) + l2_pt*sin(l2_phi))/(l1_pt*cos(l1_phi) + l2_pt*cos(l2_phi))) - met_phi))", binning={'nbinsx':40, 'xmin':0, 'xmax':3.141593}, unit=None, xtitle='#Delta#Phi(E_{T}^{miss}, l1+l2)'),
    # VCfg(name='pt_l1l2_div_pt_l1', drawname="sqrt(l1_pt**2 + l2_pt**2 + 2*l1_pt*l2_pt*(cos(l1_phi - l2_phi)))/l1_pt", binning={'nbinsx':40, 'xmin':0, 'xmax':2.}, unit=None, xtitle='p_{T}^{l1+l2}/p_{T}^{l1}'),
    # VCfg(name='pt_l1l2_div_pt_l2', drawname="sqrt(l1_pt**2 + l2_pt**2 + 2*l1_pt*l2_pt*(cos(l1_phi - l2_phi)))/l2_pt", binning={'nbinsx':50, 'xmin':0, 'xmax':10.}, unit=None, xtitle='p_{T}^{l1+l2}/p_{T}^{l2}'),
    VCfg(name='dil_pt', drawname="dil_pt", binning={'nbinsx':50, 'xmin':0, 'xmax':250.}, unit='GeV', xtitle='p_{T}^{l1+l2}'),

    VCfg(name='geninfo_nup', binning={'nbinsx':10, 'xmin':-0.5, 'xmax':9.5}, unit=None, xtitle='N_{partons}'),
    
    VCfg(name='min_delta_phi_tau1tau2_met', drawname='min(min(abs(TVector2::Phi_mpi_pi(met_phi - l1_phi)), abs(TVector2::Phi_mpi_pi(met_phi - l2_phi))),min(abs(TVector2::Phi_mpi_pi(met_phi - jet1_phi))+100*(jet1_pt>40), abs(TVector2::Phi_mpi_pi(met_phi - jet2_phi))+100*(jet2_pt>40)))', binning={'nbinsx':32, 'xmin':0, 'xmax':3.2}, unit=None, xtitle='min(#Delta#Phi(E_{T}^{miss}, tau1/tau2)'),

    # VCfg(name='jet1_chargedHadronMultiplicity', binning={'nbinsx':40, 'xmin':-0.5, 'xmax':39.5}, unit=None, xtitle='jet 1 N_{CH}'),
    # VCfg(name='jet1_chargedMultiplicity', binning={'nbinsx':40, 'xmin':-0.5, 'xmax':39.5}, unit='', xtitle='jet 1 N_{charged}'),
    # VCfg(name='jet1_neutralMultiplicity', binning={'nbinsx':40, 'xmin':-0.5, 'xmax':39.5}, unit='', xtitle='jet 1 N_{neutral}'),
]

muon_l1_vars = [
    VCfg(name='l1_pt', binning={'nbinsx':40, 'xmin':0., 'xmax':100.}, unit='GeV', xtitle='muon p_{T}'),
    VCfg(name='l1_eta', binning={'nbinsx':20, 'xmin':-2.5, 'xmax':2.5}, unit=None, xtitle='muon #eta'),
    VCfg(name='l1_phi', binning={'nbinsx':40, 'xmin':-3.141593, 'xmax':3.141593}, unit=None, xtitle='muon #phi'),
    VCfg(name='l1_reliso05_03', drawname='log(abs(l1_reliso05_03)+0.004)', binning={'nbinsx':40, 'xmin':-6., 'xmax':0.}, unit='', xtitle='log(muon relative isolation cone 0.3)'),
    VCfg(name='l1_reliso05', drawname='log(abs(l1_reliso05)+0.004)', binning={'nbinsx':40, 'xmin':-6., 'xmax':0.}, unit='', xtitle='log(muon relative isolation cone 0.4)'),
#    VCfg(name='l1_gen_pdgId', binning={'nbinsx':40, 'xmin':-17.5, 'xmax':22.5}, unit=None, xtitle='muon gen match PDG ID'),
#    VCfg(name='l1_log_dxy', drawname='log(abs(l1_dxy))', binning={'nbinsx':40, 'xmin':-18., 'xmax':-2.}, unit='log(cm)', xtitle='log(muon d_{xy})'),
#    VCfg(name='l1_dxy_sig', drawname='log(abs(l1_dxy/l1_dxy_error))', binning={'nbinsx':100, 'xmin':-20., 'xmax':20.}, unit=None, xtitle='muon log(d_{xy}/#sigma(d_{xy}))'),
#    VCfg(name='l1_log_dz', drawname='log(abs(l1_dz))', binning={'nbinsx':40, 'xmin':-18., 'xmax':-2.}, unit='log(cm)', xtitle='log(muon d_{z})'),
#    VCfg(name='l1_dz_sig', drawname='log(abs(l1_dz/l1_dz_error))', binning={'nbinsx':100, 'xmin':-20., 'xmax':20.}, unit=None, xtitle='muon log(d_{z}/#sigma(d_{z}))'),
#    VCfg(name='delta_phi_l1_met', drawname='abs(TVector2::Phi_mpi_pi(l1_phi-met_phi))', binning={'nbinsx':40, 'xmin':-3.141593, 'xmax':3.141593}, unit=None, xtitle='#Delta #phi (muon, MET)'),
]

electron_l1_vars = [
    VCfg(name='l1_pt', binning={'nbinsx':40, 'xmin':0., 'xmax':100.}, unit='GeV', xtitle='electron p_{T}'),
    VCfg(name='l1_eta', binning={'nbinsx':20, 'xmin':-2.5, 'xmax':2.5}, unit=None, xtitle='electron #eta'),
    VCfg(name='l1_phi', binning={'nbinsx':40, 'xmin':-3.141593, 'xmax':3.141593}, unit=None, xtitle='electron #phi'),
    VCfg(name='l1_reliso05_04', drawname='log(abs(l1_reliso05_04)+0.004)', binning={'nbinsx':40, 'xmin':-6., 'xmax':0.}, unit='', xtitle='log(electron relative isolation cone 0.4)'),
    VCfg(name='l1_reliso05', drawname='log(abs(l1_reliso05)+0.004)', binning={'nbinsx':40, 'xmin':-6., 'xmax':0.}, unit='', xtitle='log(electron relative isolation cone 0.3)'),
    VCfg(name='l1_gen_pdgId', binning={'nbinsx':40, 'xmin':-17.5, 'xmax':22.5}, unit=None, xtitle='electron gen match PDG ID'),
    VCfg(name='l1_log_dxy', drawname='log(abs(l1_dxy))', binning={'nbinsx':40, 'xmin':-18., 'xmax':-2.}, unit='log(cm)', xtitle='log(electron d_{xy})'),
    VCfg(name='l1_dxy_sig', drawname='log(abs(l1_dxy/l1_dxy_error))', binning={'nbinsx':100, 'xmin':-20., 'xmax':20.}, unit=None, xtitle='electron log(d_{xy}/#sigma(d_{xy}))'),
    VCfg(name='l1_log_dz', drawname='log(abs(l1_dz))', binning={'nbinsx':40, 'xmin':-18., 'xmax':-2.}, unit='log(cm)', xtitle='log(electron d_{z})'),
    VCfg(name='l1_dz_sig', drawname='log(abs(l1_dz/l1_dz_error))', binning={'nbinsx':100, 'xmin':-20., 'xmax':20.}, unit=None, xtitle='electron log(d_{z}/#sigma(d_{z}))'),
    VCfg(name='delta_phi_l1_met', binning={'nbinsx':40, 'xmin':-3.141593, 'xmax':3.141593}, unit=None, xtitle='#Delta #phi (electron, MET)'),
    VCfg(name='l1_nhits_missing', binning={'nbinsx':4, 'xmin':-0.5, 'xmax':3.5}, unit=None, xtitle='electron N(missing hits)'),
    VCfg(name='l1_eid_nontrigmva_loose', binning={'nbinsx':50, 'xmin':0.5, 'xmax':1.001}, unit=None, xtitle='electron non-triggering MVA'),
    VCfg(name='l1_eid', drawname='l1_eid_loose+l1_eid_medium+l1_eid_tight', binning={'nbinsx':4, 'xmin':-0.5, 'xmax':3.5}, unit=None, xtitle='cut-based ID'),
    
]

tau_l1_vars = [
    VCfg(name='l1_pt', binning={'nbinsx':50, 'xmin':0., 'xmax':400.}, unit='GeV', xtitle='tau_{1} p_{T}'),
    VCfg(name='l1_eta', binning={'nbinsx':20, 'xmin':-2.5, 'xmax':2.5}, unit=None, xtitle='tau_{1} #eta'),
    VCfg(name='l1_phi', binning={'nbinsx':40, 'xmin':-3.141593, 'xmax':3.141593}, unit=None, xtitle='tau_{1} #phi'),
    VCfg(name='l1_mt', drawname='mt', binning={'nbinsx':50, 'xmin':0., 'xmax':200.}, unit='GeV', xtitle='m_{T} #tau_{1}'),
    VCfg(name='l1_decayMode', binning={'nbinsx':12, 'xmin':-0.5, 'xmax':11.5}, unit=None, xtitle='tau_{1} decay mode'),
    VCfg(name='l1_mass', binning={'nbinsx':40, 'xmin':0., 'xmax':3.}, unit='GeV', xtitle='tau_{1} mass'),
    VCfg(name='l1_gen_pdgId', binning={'nbinsx':40, 'xmin':-17.5, 'xmax':22.5}, unit=None, xtitle='tau_{1} gen match PDG ID'),
    VCfg(name='l1_log_dxy', drawname='log(abs(l1_dxy)+0.00001)', binning={'nbinsx':40, 'xmin':-18., 'xmax':0.5}, unit='log(cm)', xtitle='log(tau_{1} d_{xy})'),
    VCfg(name='l1_dxy_sig', drawname='log(abs(l1_dxy/l1_dxy_error))', binning={'nbinsx':100, 'xmin':-20., 'xmax':20.}, unit=None, xtitle='tau_{1} log(d_{xy}/#sigma(d_{xy}))'),
    VCfg(name='l1_log_dz', drawname='log(abs(l1_dz)+0.00001)', binning={'nbinsx':40, 'xmin':-18., 'xmax':0.5}, unit='log(cm)', xtitle='log(tau_{1} d_{z})'),
    VCfg(name='l1_dz_sig', drawname='log(abs(l1_dz/l1_dz_error))', binning={'nbinsx':100, 'xmin':-20., 'xmax':20.}, unit=None, xtitle='tau_{1} log(d_{z}/#sigma(d_{z}))'),
    VCfg(name='l1_byCombinedIsolationDeltaBetaCorrRaw3Hits', binning={'nbinsx':100, 'xmin':0., 'xmax':100.}, unit='GeV', xtitle='tau_{1} delta-beta corr. 3-hit isolation'),
    VCfg(name='l1_byIsolationMVArun2v1DBoldDMwLTraw', binning={'nbinsx':40, 'xmin':0.6, 'xmax':1.}, unit='', xtitle='tau_{1} isolation MVA (old DM w/LT)'),
    VCfg(name='l1_byIsolationMVArun2v1DBdR03oldDMwLTraw', binning={'nbinsx':40, 'xmin':0.6, 'xmax':1.}, unit='', xtitle='tau_{1} isolation MVA (old DM w/LT cone 0.3)'),
    VCfg(name='l1_chargedIsoPtSum', binning={'nbinsx':50, 'xmin':0., 'xmax':25.}, unit='GeV', xtitle='tau_{1} charged isolation'),
    VCfg(name='l1_neutralIsoPtSum', binning={'nbinsx':50, 'xmin':0., 'xmax':25.}, unit='GeV', xtitle='tau_{1} neutral isolation'),
    VCfg(name='l1_puCorrPtSum', binning={'nbinsx':50, 'xmin':0., 'xmax':25.}, unit='GeV', xtitle='tau_{1} charged PU isolation'),
    VCfg(name='l1_photonPtSumOutsideSignalCone', binning={'nbinsx':50, 'xmin':0., 'xmax':25.}, unit='GeV', xtitle='tau_{1} #Sigma photon p_{T} outside signal cone'),
    VCfg(name='l1_zImpact', binning={'nbinsx':30, 'xmin':-600., 'xmax':600.}, unit='', xtitle='tau_{1} z impact'),
    VCfg(name='l1_jet_charge', binning={'nbinsx':31, 'xmin':-15.5, 'xmax':15.5}, unit='', xtitle='tau_{1} jet charge'),
    VCfg(name='l1_jet_pt_div_l1_pt', drawname='l1_pt/l1_jet_pt', binning={'nbinsx':30, 'xmin':-0.5, 'xmax':1.5}, unit='', xtitle='tau_{1} p_{T}/jet p_{T}'),
    VCfg(name='delta_phi_l1_met', drawname='abs(TVector2::Phi_mpi_pi(l1_phi - met_phi))', binning={'nbinsx':40, 'xmin':0, 'xmax':3.141593}, unit=None, xtitle='#Delta #phi (tau_{1}, MET)'),
    VCfg(name='mt_div_l1_pt', drawname='mt/l1_pt', binning={'nbinsx':40, 'xmin':0, 'xmax':7}, unit=None, xtitle='M_{T}/tau_{1} p_{T}'),
]

tau_l2_vars = [
    VCfg(name='l2_pt', binning={'nbinsx':50, 'xmin':0., 'xmax':250.}, unit='GeV', xtitle='tau p_{T}'),
    VCfg(name='l2_eta', binning={'nbinsx':20, 'xmin':-2.5, 'xmax':2.5}, unit=None, xtitle='tau #eta'),
    VCfg(name='l2_phi', binning={'nbinsx':40, 'xmin':-3.141593, 'xmax':3.141593}, unit=None, xtitle='tau #phi'),
    VCfg(name='l2_mt', drawname='mt_leg2', binning={'nbinsx':50, 'xmin':0., 'xmax':200.}, unit='GeV', xtitle='m_{T} #tau'),
    VCfg(name='l2_decayMode', binning={'nbinsx':12, 'xmin':-0.5, 'xmax':11.5}, unit=None, xtitle='tau decay mode'),
    VCfg(name='l2_mass', binning={'nbinsx':40, 'xmin':0., 'xmax':3.}, unit='GeV', xtitle='tau mass'),
    VCfg(name='l2_jet_pt', binning={'nbinsx':40, 'xmin':0., 'xmax':240.}, unit='GeV', xtitle='tau jet p_{T}'),
    VCfg(name='l2_gen_pdgId', binning={'nbinsx':40, 'xmin':-17.5, 'xmax':22.5}, unit=None, xtitle='tau gen match PDG ID'),
    VCfg(name='l2_log_dxy', drawname='log(abs(l2_dxy)+0.00001)', binning={'nbinsx':40, 'xmin':-18., 'xmax':0.5}, unit='log(cm)', xtitle='log(tau d_{xy})'),
    VCfg(name='l2_dxy_sig', drawname='log(abs(l2_dxy/l2_dxy_error))', binning={'nbinsx':100, 'xmin':-20., 'xmax':20.}, unit=None, xtitle='tau log(d_{xy}/#sigma(d_{xy}))'),
    VCfg(name='l2_log_dz', drawname='log(abs(l2_dz)+0.00001)', binning={'nbinsx':40, 'xmin':-18., 'xmax':0.5}, unit='log(cm)', xtitle='log(tau d_{z})'),
    VCfg(name='l2_dz_sig', drawname='log(abs(l2_dz/l2_dz_error))', binning={'nbinsx':100, 'xmin':-20., 'xmax':20.}, unit=None, xtitle='tau log(d_{z}/#sigma(d_{z}))'),
    VCfg(name='l2_byCombinedIsolationDeltaBetaCorrRaw3Hits', binning={'nbinsx':100, 'xmin':0., 'xmax':100.}, unit='GeV', xtitle='tau delta-beta corr. 3-hit isolation'),
    VCfg(name='l2_byIsolationMVArun2v1DBoldDMwLTraw', binning={'nbinsx':100, 'xmin':-1., 'xmax':1.}, unit='', xtitle='tau isolation MVA (old DM w/LT)'),
    VCfg(name='l2_byIsolationMVArun2v1DBdR03oldDMwLTraw', binning={'nbinsx':100, 'xmin':0., 'xmax':1.}, unit='', xtitle='tau isolation MVA (old DM w/LT cone 0.3)'),
    # VCfg(name='l2_nc_ratio', binning={'nbinsx':20, 'xmin':-1., 'xmax':1.}, unit='GeV', xtitle='tau neutral-charged asymmetry'),
    # VCfg(name='l2_gen_nc_ratio', binning={'nbinsx':20, 'xmin':-1., 'xmax':1.}, unit='GeV', xtitle='tau gen neutral-charged asymmetry'),
    VCfg(name='delta_phi_l2_met', drawname='abs(TVector2::Phi_mpi_pi(l2_phi-met_phi))', binning={'nbinsx':40, 'xmin':0., 'xmax':3.141593}, unit=None, xtitle='#Delta #phi (tau, MET)'),
]

muon_l2_vars = [
    VCfg(name='l2_pt', binning={'nbinsx':40, 'xmin':0., 'xmax':100.}, unit='GeV', xtitle='2nd muon p_{T}'),
    VCfg(name='l2_eta', binning={'nbinsx':20, 'xmin':-2.5, 'xmax':2.5}, unit=None, xtitle='2nd muon #eta'),
    VCfg(name='l2_phi', binning={'nbinsx':40, 'xmin':-3.141593, 'xmax':3.141593}, unit=None, xtitle='2nd muon #phi'),
#    VCfg(name='l2_reliso05_03', drawname='log(abs(l2_reliso05_03)+0.004)', binning={'nbinsx':40, 'xmin':-6., 'xmax':0.}, unit='', xtitle='log(2nd muon relative isolation cone 0.3)'),
#    VCfg(name='l2_reliso05', drawname='log(abs(l2_reliso05)+0.004)', binning={'nbinsx':40, 'xmin':-6., 'xmax':0.}, unit='', xtitle='log(2nd muon relative isolation cone 0.4)'),
#    VCfg(name='l2_gen_pdgId', binning={'nbinsx':40, 'xmin':-17.5, 'xmax':22.5}, unit=None, xtitle='muon gen match PDG ID'),
#    VCfg(name='l2_log_dxy', drawname='log(abs(l2_dxy))', binning={'nbinsx':40, 'xmin':-18., 'xmax':-2.}, unit='log(cm)', xtitle='log(2nd muon d_{xy})'),
#    VCfg(name='l2_dxy_sig', drawname='log(abs(l2_dxy/l1_dxy_error))', binning={'nbinsx':100, 'xmin':-20., 'xmax':20.}, unit=None, xtitle='2nd muon log(d_{xy}/#sigma(d_{xy}))'),
#    VCfg(name='l2_log_dz', drawname='log(abs(l2_dz))', binning={'nbinsx':40, 'xmin':-18., 'xmax':-2.}, unit='log(cm)', xtitle='log(2nd muon d_{z})'),
#    VCfg(name='l2_dz_sig', drawname='log(abs(l2_dz/l2_dz_error))', binning={'nbinsx':100, 'xmin':-20., 'xmax':20.}, unit=None, xtitle='2nd muon log(d_{z}/#sigma(d_{z}))'),
#    VCfg(name='delta_phi_l2_met', binning={'nbinsx':40, 'xmin':-3.141593, 'xmax':3.141593}, unit=None, xtitle='#Delta #phi (2nd muon, MET'),
]

tau_mu_special_vars = [
    VCfg(name='delta_eta_l1_l2', drawname='abs(l1_eta - l2_eta)', binning={'nbinsx':40, 'xmin':0, 'xmax':4.5}, unit=None, xtitle='#Delta#eta(#tau, #mu)'),
    VCfg(name='delta_r_l1_l2', binning={'nbinsx':40, 'xmin':0, 'xmax':4.5}, unit=None, xtitle='#Delta R(#tau, #mu)'),
    VCfg(name='delta_phi_l1_l2', drawname='abs(TVector2::Phi_mpi_pi(l1_phi - l2_phi))', binning={'nbinsx':40, 'xmin':0, 'xmax':3.1415927}, unit=None, xtitle='#Delta #phi(#tau, #mu)'),
    VCfg(name='dil_pt', binning={'nbinsx':40, 'xmin':0, 'xmax':300.}, unit='GeV', xtitle='Dilepton p_{T}'),
    VCfg(name='delta_phi_dil_l1', drawname='abs(TVector2::Phi_mpi_pi(dil_phi - l1_phi))', binning={'nbinsx':40, 'xmin':0, 'xmax':3.1415927}, unit=None, xtitle='#Delta #phi(dilepton, #mu)'),
    VCfg(name='delta_phi_dil_l2', drawname='abs(TVector2::Phi_mpi_pi(dil_phi - l2_phi))', binning={'nbinsx':40, 'xmin':0, 'xmax':3.1415927}, unit=None, xtitle='#Delta #phi(dilepton, #tau)'),
    VCfg(name='delta_eta_dil_l1', drawname='abs(dil_eta - l1_eta)', binning={'nbinsx':40, 'xmin':0, 'xmax':4.5}, unit=None, xtitle='#Delta#eta(dilepton, #mu)'),
    VCfg(name='delta_eta_dil_l2', drawname='abs(dil_eta - l2_eta)', binning={'nbinsx':40, 'xmin':0, 'xmax':4.5}, unit=None, xtitle='#Delta#eta(dilepton, #tau)'),
]

tau_tau_special_vars = [
    VCfg(name='mt2', binning={'nbinsx':50, 'xmin':0., 'xmax':500.}, unit='GeV', xtitle='m_{T2}'),
    VCfg(name='delta_eta_l1_l2', drawname='abs(l1_eta - l2_eta)', binning={'nbinsx':40, 'xmin':0, 'xmax':4.5}, unit=None, xtitle='#Delta#eta(#tau_{1}, #tau_{2})'),
    VCfg(name='delta_r_l1_l2', binning={'nbinsx':40, 'xmin':0, 'xmax':4.5}, unit=None, xtitle='#Delta R(#tau_{1}, #tau_{2})'),
    VCfg(name='delta_phi_l1_l2', drawname='abs(TVector2::Phi_mpi_pi(l1_phi - l2_phi))', binning={'nbinsx':40, 'xmin':0., 'xmax':3.141593}, unit=None, xtitle='#Delta #phi (#tau_{1}, #tau_{2})'),
]

mu_mu_special_vars = [
    VCfg(name='delta_eta_l1_l2', drawname='abs(l1_eta - l2_eta)', binning={'nbinsx':40, 'xmin':0, 'xmax':4.5}, unit=None, xtitle='#Delta#eta(#mu, #mu)'),
    VCfg(name='delta_r_l1_l2', binning={'nbinsx':40, 'xmin':0, 'xmax':4.5}, unit=None, xtitle='#Delta R(#mu, #mu)'),
    VCfg(name='delta_phi_l1_l2', drawname='abs(TVector2::Phi_mpi_pi(l1_phi - l2_phi))', binning={'nbinsx':40, 'xmin':0, 'xmax':3.1415927}, unit=None, xtitle='#Delta #phi(#mu, #mu)'),
]

additional_tau_vars = [
    VCfg(name='tau1_pt', binning={'nbinsx':40, 'xmin':0., 'xmax':100.}, unit='GeV', xtitle='tau p_{T}'),
    VCfg(name='tau1_eta', binning={'nbinsx':20, 'xmin':-2.5, 'xmax':2.5}, unit=None, xtitle='tau #eta'),
    VCfg(name='tau1_decayMode', binning={'nbinsx':12, 'xmin':-0.5, 'xmax':11.5}, unit=None, xtitle='tau decay mode'),
    VCfg(name='tau1_mass', binning={'nbinsx':40, 'xmin':0., 'xmax':3.}, unit='GeV', xtitle='tau mass'),
    VCfg(name='tau1_gen_pdgId', binning={'nbinsx':40, 'xmin':-17.5, 'xmax':22.5}, unit=None, xtitle='tau gen match PDG ID'),
    VCfg(name='tau1_log_dxy', drawname='log(abs(tau1_dxy)+0.00001)', binning={'nbinsx':40, 'xmin':-18., 'xmax':0.5}, unit='log(cm)', xtitle='log(tau d_{xy})'),
    VCfg(name='tau1_dxy_sig', drawname='log(abs(tau1_dxy/tau1_dxy_error))', binning={'nbinsx':100, 'xmin':-20., 'xmax':20.}, unit=None, xtitle='tau log(d_{xy}/#sigma(d_{xy}))'),
    VCfg(name='tau1_byCombinedIsolationDeltaBetaCorrRaw3Hits', binning={'nbinsx':100, 'xmin':0., 'xmax':100.}, unit='GeV', xtitle='tau delta-beta corr. 3-hit isolation'),
    VCfg(name='tau1_chargedIsoPtSum', binning={'nbinsx':50, 'xmin':0., 'xmax':50.}, unit='', xtitle='charged isolation (GeV)'),
    VCfg(name='tau1_neutralIsoPtSum', binning={'nbinsx':50, 'xmin':0., 'xmax':50.}, unit='', xtitle='neutral isolation (GeV)'),
    VCfg(name='tau1_photonPtSumOutsideSignalCone', binning={'nbinsx':50, 'xmin':0., 'xmax':30.}, unit='GeV', xtitle='tau photon p_{T} outer'),
    VCfg(name='tau1_photonPtSumOutsideSignalCone_div_tau_pt', drawname='tau1_photonPtSumOutsideSignalCone/tau1_pt',  binning={'nbinsx':50, 'xmin':0., 'xmax':1.}, unit='', xtitle='tau photon p_{T} outer/tau p_{T}'),
    VCfg(name='tau1_byCombinedIsolationDeltaBetaCorr3Hits', binning={'nbinsx':7, 'xmin':-0.5, 'xmax':6.5}, unit='', xtitle='delta-beta corr. 3-hit isolation'),
    VCfg(name='tau1_byIsolationMVArun2v1DBoldDMwLT', binning={'nbinsx':7, 'xmin':-0.5, 'xmax':6.5}, unit='', xtitle='isolation MVA (old DM w/LT)'),
    VCfg(name='tau1_byIsolationMVArun2v1DBdR03oldDMwLT', binning={'nbinsx':7, 'xmin':-0.5, 'xmax':6.5}, unit='', xtitle='isolation MVA (old DM w/LT cone 0.3)'),
    VCfg(name='tau1_puCorrPtSum', binning={'nbinsx':50, 'xmin':0., 'xmax':50.}, unit='GeV', xtitle='Pileup correction p_{T} sum'),
    VCfg(name='tau1_footprintCorrection', binning={'nbinsx':50, 'xmin':0., 'xmax':50.}, unit='GeV', xtitle='Footprint correction'),
    VCfg(name='tau1_againstElectronMVA6', binning={'nbinsx':9, 'xmin':-0.5, 'xmax':8.5}, unit='', xtitle='Anti-electron MVA6'),
    VCfg(name='tau1_againstMuon3', binning={'nbinsx':4, 'xmin':-0.5, 'xmax':3.5}, unit='', xtitle='Anti-muon discriminator 3'),
    VCfg(name='tau1_pt_div_jet_pt', drawname='tau1_pt/tau1_jet_pt', binning={'nbinsx':50, 'xmin':0., 'xmax':1.5}, unit='', xtitle='p_{T}/jet p_{T}'),
    VCfg(name='tau1_log_zimpact', drawname='log(abs(tau1_zImpact))', binning={'nbinsx':50, 'xmin':-5., 'xmax':8.}, unit='cm', xtitle='z impact'),
    VCfg(name='tau1_own_vertexz', drawname='tau1_dz_selfvertex>0', binning={'nbinsx':2, 'xmin':-0.5, 'xmax':1.5}, unit='', xtitle='Is own z vertex'),
    VCfg(name='tau1_jet_mass', binning={'nbinsx':50, 'xmin':0., 'xmax':50.}, unit='GeV', xtitle='Jet mass'),
    VCfg(name='tau1_eta_min_jet_eta', drawname='tau1_eta - tau1_jet_eta', binning={'nbinsx':50, 'xmin':-0.15, 'xmax':0.15}, unit='', xtitle='#eta - jet #eta'),
]

additional_extra_tau_vars = [
    VCfg(name='tau1_iso_n_ch', binning={'nbinsx':41, 'xmin':-0.5, 'xmax':40.5}, unit='', xtitle='tau isolation N_{charged hadrons}'),
    VCfg(name='tau1_iso_n_gamma', binning={'nbinsx':41, 'xmin':-0.5, 'xmax':40.5}, unit='', xtitle='tau isolation N_{photons}'),
    VCfg(name='tau1_lead_ch_pt', drawname='log(abs(tau_lead_ch_pt)) - 999*(tau_lead_ch_pt<0)', binning={'nbinsx':40, 'xmin':-0.1, 'xmax':6.}, unit='GeV', xtitle='log(tau iso leading CH p_{T})'),
    VCfg(name='tau1_lead_ch_dxy', drawname='log(abs(tau_lead_ch_dxy))', binning={'nbinsx':40, 'xmin':-12., 'xmax':-2.}, unit='cm', xtitle='log(tau iso leading CH d_{xy})'),
    VCfg(name='tau1_lead_ch_dz', drawname='log(abs(tau_lead_ch_dz))', binning={'nbinsx':40, 'xmin':-12., 'xmax':3.}, unit='cm', xtitle='log(tau iso leading CH d_{z})'),
    VCfg(name='tau1_lead_ch_ndof', binning={'nbinsx':34, 'xmin':-0.5, 'xmax':33.5}, unit='', xtitle='tau iso leading CH ndof'),
    VCfg(name='tau1_lead_ch_normchi2', binning={'nbinsx':100, 'xmin':-0., 'xmax':49.5}, unit='', xtitle='tau iso leading CH normalized chi2'),
    VCfg(name='tau1_lead_ch_chi2', binning={'nbinsx':100, 'xmin':-0., 'xmax':49.5}, unit='', xtitle='tau iso leading CH  chi2'),
    VCfg(name='tau1_lead_ch_n_layers_pixel', binning={'nbinsx':6, 'xmin':-0.5, 'xmax':5.5}, unit='', xtitle='tau iso leading CH N_{pixel layers}'),
    VCfg(name='tau1_lead_ch_n_hits_pixel', binning={'nbinsx':9, 'xmin':-0.5, 'xmax':8.5}, unit='', xtitle='tau iso leading CH N_{pixel hits}'),
    VCfg(name='tau1_lead_ch_n_layers_tracker', binning={'nbinsx':6, 'xmin':-0.5, 'xmax':5.5}, unit='', xtitle='tau iso leading CH N_{tracker layers}'),
    VCfg(name='tau1_lead_ch_n_hits', binning={'nbinsx':32, 'xmin':-0.5, 'xmax':31.5}, unit='', xtitle='tau iso leading CH N_{hits}'),
    VCfg(name='tau1_lead_ch_n_missing_inner', binning={'nbinsx':4, 'xmin':-0.5, 'xmax':3.5}, unit='', xtitle='tau iso leading CH N_{missing inner hits}'),

    VCfg(name='tau1_leadiso_ch_pt', drawname='log(abs(tau_leadiso_ch_pt)) - 999*(tau_leadiso_ch_pt<0)', binning={'nbinsx':40, 'xmin':-0.1, 'xmax':6.}, unit='GeV', xtitle='log(tau iso leading CH p_{T})'),
    VCfg(name='tau1_leadiso_ch_dxy', drawname='log(abs(tau_leadiso_ch_dxy))', binning={'nbinsx':40, 'xmin':-12., 'xmax':-2.}, unit='cm', xtitle='log(tau iso leading CH d_{xy})'),
    VCfg(name='tau1_leadiso_ch_dz', drawname='log(abs(tau_leadiso_ch_dz))', binning={'nbinsx':40, 'xmin':-12., 'xmax':3.}, unit='cm', xtitle='log(tau iso leading CH d_{z})'),
    VCfg(name='tau1_leadiso_ch_ndof', binning={'nbinsx':34, 'xmin':-0.5, 'xmax':33.5}, unit='', xtitle='tau iso leading CH ndof'),
    VCfg(name='tau1_leadiso_ch_normchi2', binning={'nbinsx':100, 'xmin':-0., 'xmax':49.5}, unit='', xtitle='tau iso leading CH normalized chi2'),
    VCfg(name='tau1_leadiso_ch_chi2', binning={'nbinsx':100, 'xmin':-0., 'xmax':49.5}, unit='', xtitle='tau iso leading CH  chi2'),
    VCfg(name='tau1_leadiso_ch_n_layers_pixel', binning={'nbinsx':6, 'xmin':-0.5, 'xmax':5.5}, unit='', xtitle='tau iso leading CH N_{pixel layers}'),
    VCfg(name='tau1_leadiso_ch_n_hits_pixel', binning={'nbinsx':9, 'xmin':-0.5, 'xmax':8.5}, unit='', xtitle='tau iso leading CH N_{pixel hits}'),
    VCfg(name='tau1_leadiso_ch_n_layers_tracker', binning={'nbinsx':6, 'xmin':-0.5, 'xmax':5.5}, unit='', xtitle='tau iso leading CH N_{tracker layers}'),
    VCfg(name='tau1_leadiso_ch_n_hits', binning={'nbinsx':32, 'xmin':-0.5, 'xmax':31.5}, unit='', xtitle='tau iso leading CH N_{hits}'),
    VCfg(name='tau1_leadiso_ch_n_missing_inner', binning={'nbinsx':4, 'xmin':-0.5, 'xmax':3.5}, unit='', xtitle='tau iso leading CH N_{missing inner hits}'),

]

hnl_vars = [
    VCfg(name='CR_l0_pt_cone' , drawname='l0_pt * (1 + l0_reliso_rho_03)'  , binning={'nbinsx':16, 'xmin':0.  , 'xmax':200.}, unit='GeV', xtitle='p_{T}^{Cone} (leading)'),
    VCfg(name='CR_l2_pt_cone' , drawname='l2_pt * (1 + l2_reliso_rho_03)'  , binning={'nbinsx':16, 'xmin':0.  , 'xmax':200.}, unit='GeV', xtitle='p_{T}^{Cone} (trailing)'),
    VCfg(name='CR_hnl_mt_0'   , drawname='hnl_mt_0'   , binning={'nbinsx':16, 'xmin':0   , 'xmax':200 }, unit='GeV', xtitle='M_{T} (leading)'),
    VCfg(name='hnl_w_vis_m', binning={'nbinsx':40, 'xmin':0   , 'xmax':250 }, unit='GeV', xtitle='3 lepton mass'),
    VCfg(name='CR_hnl_w_vis_m_wide', drawname='hnl_w_vis_m', binning={'nbinsx':24, 'xmin':0  , 'xmax':300 }, unit='GeV', xtitle='3 lepton mass'),
    VCfg(name='CR_hnl_w_vis_m_z', drawname='hnl_w_vis_m', binning={'nbinsx':40, 'xmin':70  , 'xmax':110 }, unit='GeV', xtitle='3 lepton mass'),

    VCfg(name='_norm_'     , drawname='1.', binning={'nbinsx':5, 'xmin':-1.5, 'xmax':3.5}, unit='', xtitle='Normalisation'),

    VCfg(name='n_vtx', binning={'nbinsx':101, 'xmin':-0.5, 'xmax':100.5}, unit=None, xtitle='N_{vertices}'),

    VCfg(name='l0_pt'      , binning={'nbinsx':40, 'xmin':0.  , 'xmax':100.}, unit='GeV', xtitle='prompt lepton p_{T}'),
    VCfg(name='l0_eta'     , binning={'nbinsx':20, 'xmin':-2.5, 'xmax':2.5 }, unit=None , xtitle='prompt lepton #eta'),
    VCfg(name='l0_phi'     , binning={'nbinsx':40, 'xmin':-pi , 'xmax':pi  }, unit='rad', xtitle='prompt lepton #phi'),
    VCfg(name='l1_pt'      , binning={'nbinsx':40, 'xmin':0.  , 'xmax':100.}, unit='GeV', xtitle='1st muon p_{T}'),
    VCfg(name='l1_eta'     , binning={'nbinsx':20, 'xmin':-2.5, 'xmax':2.5 }, unit=None , xtitle='1st muon #eta'),
    VCfg(name='l1_phi'     , binning={'nbinsx':40, 'xmin':-pi , 'xmax':pi  }, unit='rad', xtitle='1st muon #phi'),
    VCfg(name='l2_pt'      , binning={'nbinsx':40, 'xmin':0.  , 'xmax':100.}, unit='GeV', xtitle='2nd muon p_{T}'),
    VCfg(name='l2_eta'     , binning={'nbinsx':20, 'xmin':-2.5, 'xmax':2.5 }, unit=None , xtitle='2nd muon #eta'),
    VCfg(name='l2_phi'     , binning={'nbinsx':40, 'xmin':-pi , 'xmax':pi  }, unit='rad', xtitle='2nd muon #phi'),

    VCfg(name='l0_dxy', binning={'nbinsx':100, 'xmin':-2. , 'xmax':2. }, unit='cm', xtitle='prompt lepton d_{xy}'),
    VCfg(name='l0_dz' , binning={'nbinsx':100, 'xmin':-3. , 'xmax':3. }, unit='cm', xtitle='prompt lepton d_{z}'),
    VCfg(name='l1_dxy', binning={'nbinsx':100, 'xmin':-4. , 'xmax':4. }, unit='cm', xtitle='1st muon d_{xy}'),
    VCfg(name='l1_dxy_coarse', drawname='l1_dxy', binning={'nbinsx':40, 'xmin':-1. , 'xmax':1. }, unit='cm', xtitle='1st muon d_{xy}'),
    VCfg(name='l1_dz' , binning={'nbinsx':100, 'xmin':-20., 'xmax':20.}, unit='cm', xtitle='1st muon d_{z}'),
    VCfg(name='l2_dxy', binning={'nbinsx':100, 'xmin':-4. , 'xmax':4. }, unit='cm', xtitle='2nd muon d_{xy}'),
    VCfg(name='l2_dxy_coarse', drawname='l2_dxy', binning={'nbinsx':40, 'xmin':-1. , 'xmax':1. }, unit='cm', xtitle='2nd muon d_{xy}'),
    VCfg(name='l2_dz' , binning={'nbinsx':100, 'xmin':-20., 'xmax':20.}, unit='cm', xtitle='2nd muon d_{z}'),

    VCfg(name='l0_reliso_rho_03', binning={'nbinsx':20, 'xmin':0., 'xmax':0.5}, unit=None, xtitle='prompt lepton relative isolation cone 0.3'),
    VCfg(name='l1_reliso_rho_03', binning={'nbinsx':20, 'xmin':0., 'xmax':0.5}, unit=None, xtitle='1st muon relative isolation cone 0.3'),
    VCfg(name='l2_reliso_rho_03', binning={'nbinsx':20, 'xmin':0., 'xmax':0.5}, unit=None, xtitle='2nd muon relative isolation cone 0.3'),

    VCfg(name='hnl_m_01', binning={'nbinsx':40, 'xmin':0   , 'xmax':200 }, unit='GeV', xtitle='mass(l_{0},#mu_{1})'),
    VCfg(name='hnl_m_01_Z', drawname = 'hnl_m_01', binning={'nbinsx':40, 'xmin':70.   , 'xmax':110 }, unit='GeV', xtitle='mass(l_{0},#mu_{1})'),
    VCfg(name='hnl_m_01_wide', drawname = 'hnl_m_01', binning={'nbinsx':80, 'xmin':0.   , 'xmax':110 }, unit='GeV', xtitle='mass(l_{0},#mu_{1})'),
    VCfg(name='hnl_m_02', binning={'nbinsx':40, 'xmin':0   , 'xmax':200 }, unit='GeV', xtitle='mass(l_{0},#mu_{2})'),

    VCfg(name='hnl_m_12_wide', drawname='hnl_m_12', binning={'nbinsx':80, 'xmin':0   , 'xmax':200 }, unit='GeV', xtitle='dimuon mass'),
    VCfg(name='hnl_m_12_z'   , drawname='hnl_m_12', binning={'nbinsx':40, 'xmin':70  , 'xmax':110 }, unit='GeV', xtitle='dimuon mass'),
    VCfg(name='hnl_m_12_jpsi', drawname='hnl_m_12', binning={'nbinsx':50, 'xmin':2.5 , 'xmax':3.5 }, unit='GeV', xtitle='dimuon mass'),
    VCfg(name='hnl_m_12_low' , drawname='hnl_m_12', binning={'nbinsx':40, 'xmin':0   , 'xmax':10  }, unit='GeV', xtitle='dimuon mass'),

    VCfg(name='hnl_hn_pt'    , binning={'nbinsx':80, 'xmin':0   , 'xmax':200 }, unit='GeV', xtitle='dimuon p_{T} (MET)'),
    VCfg(name='hnl_hn_vis_pt', binning={'nbinsx':80, 'xmin':0   , 'xmax':200 }, unit='GeV', xtitle='dimuon p_{T} (no MET)'),
    VCfg(name='hnl_hn_eta'   , binning={'nbinsx':40, 'xmin':-2.5, 'xmax':2.5 }, unit=None , xtitle='dimuon #eta'),
    VCfg(name='hnl_hn_phi'   , binning={'nbinsx':40, 'xmin':-pi , 'xmax':pi  }, unit='rad', xtitle='dimuon #phi'),

    VCfg(name='hnl_dr_01'        , binning={'nbinsx':40, 'xmin':0   , 'xmax':6 }, unit=None, xtitle='#DeltaR (l_{0}, #mu_{1})'),
    VCfg(name='hnl_dr_02'        , binning={'nbinsx':40, 'xmin':0   , 'xmax':6 }, unit=None, xtitle='#DeltaR (l_{0}, #mu_{2})'),
    VCfg(name='hnl_dr_12'        , binning={'nbinsx':40, 'xmin':0   , 'xmax':6 }, unit=None, xtitle='#DeltaR (#mu_{1}, #mu_{2})'),
    VCfg(name='hnl_dr_hnvis0'    , binning={'nbinsx':40, 'xmin':0   , 'xmax':6 }, unit=None, xtitle='#DeltaR (dimuon, l_{0})'),

    VCfg(name='hnl_dphi_0met'    , binning={'nbinsx':40, 'xmin':-pi , 'xmax':pi}, unit=None, xtitle='#Delta#phi (l_{0}, E_{T}^{miss})'),
    VCfg(name='hnl_dphi_1met'    , binning={'nbinsx':40, 'xmin':-pi , 'xmax':pi}, unit=None, xtitle='#Delta#phi (#mu_{1}, E_{T}^{miss})'),
    VCfg(name='hnl_dphi_2met'    , binning={'nbinsx':40, 'xmin':-pi , 'xmax':pi}, unit=None, xtitle='#Delta#phi (#mu_{2}, E_{T}^{miss})'),
    VCfg(name='hnl_dphi_hnvismet', binning={'nbinsx':40, 'xmin':-pi , 'xmax':pi}, unit=None, xtitle='#Delta#phi (dimuon, E_{T}^{miss})'),

    VCfg(name='hnl_dphi_01'      , binning={'nbinsx':40, 'xmin':-pi , 'xmax':pi}, unit=None, xtitle='#Delta#phi (l_{0}, #mu_{1})'),
    VCfg(name='hnl_dphi_02'      , binning={'nbinsx':40, 'xmin':-pi , 'xmax':pi}, unit=None, xtitle='#Delta#phi (l_{0}, #mu_{2})'),
    VCfg(name='hnl_dphi_12'      , binning={'nbinsx':40, 'xmin':-pi , 'xmax':pi}, unit=None, xtitle='#Delta#phi (#mu_{1}, #mu_{2})'),
    VCfg(name='hnl_dphi_hnvis0'  , binning={'nbinsx':40, 'xmin':-pi , 'xmax':pi}, unit=None, xtitle='#Delta#phi (dimuon, l_{0})'),

    VCfg(name='hnl_2d_disp', binning={'nbinsx':40, 'xmin':0   , 'xmax':100 }, unit='cm' , xtitle='2D displacement'),
    VCfg(name='hnl_2d_small_disp', drawname='hnl_2d_disp', binning={'nbinsx':20, 'xmin':0   , 'xmax':40 }, unit='cm' , xtitle='2D displacement'),
    VCfg(name='hnl_2d_smaller_disp', drawname='hnl_2d_disp', binning={'nbinsx':25, 'xmin':0   , 'xmax':10 }, unit='cm' , xtitle='2D displacement'),
    VCfg(name='hnl_3d_disp', binning={'nbinsx':40, 'xmin':0   , 'xmax':200 }, unit='cm' , xtitle='3D displacement'),

    VCfg(name='pfmet_phi'        , binning={'nbinsx':40, 'xmin':-3.141593, 'xmax':3.141593}, unit=None, xtitle='E_{T}^{miss} #Phi (PF)'),
    VCfg(name='pfmet_pt'         , binning={'nbinsx':40, 'xmin':0., 'xmax':300.}, unit='GeV', xtitle='E_{T}^{miss} (PF)'),

    VCfg(name='sv_prob'          , binning={'nbinsx':40 , 'xmin':0   , 'xmax':1   }, unit=None, xtitle='SV probability'),
    VCfg(name='sv_cos'           , binning={'nbinsx':40 , 'xmin':-1  , 'xmax':1   }, unit=None, xtitle='SV cos'),
    VCfg(name='hnl_2d_disp_sig'  , binning={'nbinsx':40 , 'xmin':0   , 'xmax':20  }, unit=None, xtitle='SV L/#sigma'),
    VCfg(name='hnl_2d_disp_sig_extended', drawname='hnl_2d_disp_sig', binning={'nbinsx':100 , 'xmin':0   , 'xmax':1000  }, unit=None, xtitle='SV L/#sigma'),

    VCfg(name='nj' , binning={'nbinsx':12, 'xmin':-0.5, 'xmax':11.5}, unit=None, xtitle='N_{jets}'),
    VCfg(name='nbj', binning={'nbinsx':12, 'xmin':-0.5, 'xmax':11.5}, unit=None, xtitle='N_{b-jets}'),

    VCfg(name='ptCone', drawname='hnl_w_vis_pt',      binning={'nbinsx':14, 'xmin':0, 'xmax':70},    unit='GeV', xtitle='p^{Cone}_{T}'),
    VCfg(name='hnl_dphi_hnvis0_wide'  ,drawname='abs(hnl_dphi_hnvis0)', binning={'nbinsx':40, 'xmin': 0, 'xmax':pi}, unit=None, xtitle='|#Delta#phi (dimuon, l_{0})|'),
    VCfg(name='eta(di_L,l0)'   ,drawname='hnl_hn_eta - l0_eta', binning={'nbinsx':40, 'xmin':-2.5, 'xmax':2.5 }, unit=None , xtitle='Delta #eta (dimuon, l_{0})'),

    # VCfg(name='hnl_iso_rel', binning={'nbinsx':40, 'xmin':0., 'xmax':3.} , unit=None, xtitle='rel. dilepton isolation'),
    # VCfg(name='hnl_iso_abs', binning={'nbinsx':40, 'xmin':0., 'xmax':50.}, unit=None, xtitle='abs. dilepton isolation'),

]

test_vars = [
            VCfg(name='_norm_'     , drawname='1.', binning={'nbinsx':5, 'xmin':-1.5, 'xmax':3.5}, unit='', xtitle='Normalisation'),
            VCfg(name='nbj', binning={'nbinsx':12, 'xmin':-0.5, 'xmax':11.5}, unit=None, xtitle='N_{b-jets}'),
            VCfg(name='hnl_m_01', binning={'nbinsx':40, 'xmin':0   , 'xmax':200 }, unit='GeV', xtitle='mass(l_{0},l_{1})'),
            VCfg(name='hnl_m_02', binning={'nbinsx':40, 'xmin':0   , 'xmax':200 }, unit='GeV', xtitle='mass(l_{0},l_{2})'),
            VCfg(name='hnl_m_12', binning={'nbinsx':40, 'xmin':0   , 'xmax':200 }, unit='GeV', xtitle='mass(l_{1},l_{2})'),
            VCfg(name='l0_reliso_rho_03', binning={'nbinsx':20, 'xmin':0., 'xmax':0.0001}, unit=None, xtitle='prompt lepton relative isolation cone 0.3'),
            VCfg(name='l1_reliso_rho_03', binning={'nbinsx':20, 'xmin':0., 'xmax':0.0001}, unit=None, xtitle='1st muon relative isolation cone 0.3'),
            VCfg(name='l2_reliso_rho_03', binning={'nbinsx':20, 'xmin':0., 'xmax':0.0001}, unit=None, xtitle='2nd muon relative isolation cone 0.3'),
            # VCfg(name='hnl_dphi_hnvis0_wide'  ,drawname='abs(hnl_dphi_hnvis0)', binning={'nbinsx':40, 'xmin': 0, 'xmax':pi}, unit=None, xtitle='|#Delta#phi (dimuon, l_{0})|'),
            # VCfg(name='hnl_dphi_hnvis0_small'  ,drawname='abs(hnl_dphi_hnvis0)', binning={'nbinsx':40, 'xmin': 0, 'xmax':1.}, unit=None, xtitle='|#Delta#phi (dimuon, l_{0})|'),
            # VCfg(name='hnl_dphi_hnvis0_lare'  ,drawname='abs(hnl_dphi_hnvis0)', binning={'nbinsx':40, 'xmin':2.5 , 'xmax':pi}, unit=None, xtitle='|#Delta#phi (dimuon, l_{0})|'),
            VCfg(name='hnl_2d_smaller_disp', drawname='hnl_2d_disp', binning={'nbinsx':10, 'xmin':0   , 'xmax':10 }, unit='cm' , xtitle='2D displacement'),
            VCfg(name='hnl_w_vis_m', binning={'nbinsx':40, 'xmin':0   , 'xmax':250 }, unit='GeV', xtitle='3 lepton mass'),
             # VCfg(name='hnl_m_12_low' , drawname='hnl_m_12', binning={'nbinsx':10, 'xmin':0   , 'xmax':10  }, unit='GeV', xtitle='dimuon mass'),
            ]

PTCONE = '(  ( hnl_hn_vis_pt * (hnl_iso04_rel_rhoArea<0.15) ) + ( (hnl_iso04_rel_rhoArea>=0.15) * ( hnl_hn_vis_pt * (1. + hnl_iso04_rel_rhoArea - 0.15) ) )  )'

dde_vars = [
            VCfg(name='_norm_'     , drawname='1.', binning={'nbinsx':5, 'xmin':-1.5, 'xmax':3.5}, unit='', xtitle='Normalisation'),
            VCfg(name='hnl_m_01_Z', drawname = 'hnl_m_01', binning={'nbinsx':40, 'xmin':70.   , 'xmax':110 }, unit='GeV', xtitle='mass(l_{0},#mu_{1})'),
            VCfg(name='hnl_m_01_wide', drawname = 'hnl_m_01', binning={'nbinsx':80, 'xmin':0.   , 'xmax':110 }, unit='GeV', xtitle='mass(l_{0},#mu_{1})'),
            VCfg(name='hnl_m_01_low', drawname = 'hnl_m_01', binning={'nbinsx':80, 'xmin':0.   , 'xmax':20 }, unit='GeV', xtitle='mass(l_{0},#mu_{1})'),
            VCfg(name='m_triL', drawname='hnl_w_vis_m',       binning={'nbinsx':50, 'xmin':50., 'xmax':200}, unit='GeV', xtitle='Tri-Lepton Mass'),
            VCfg(name='m_triL_wide', drawname='hnl_w_vis_m',       binning={'nbinsx':40, 'xmin':0., 'xmax':250}, unit='GeV', xtitle='Tri-Lepton Mass'),
            VCfg(name='hnl_dphi_hnvis0_wide'  ,drawname='abs(hnl_dphi_hnvis0)', binning={'nbinsx':40, 'xmin': 0, 'xmax':pi}, unit=None, xtitle='|#Delta#phi (dimuon, l_{0})|'),
            VCfg(name='eta(di_L,l0)'   ,drawname='hnl_hn_eta - l0_eta', binning={'nbinsx':40, 'xmin':-2.5, 'xmax':2.5 }, unit=None , xtitle='Delta #eta (dimuon, l_{0})'),
           ]

def getVars(names, channel='all'):
    return [dict_channel_vars[channel][n] for n in names]
