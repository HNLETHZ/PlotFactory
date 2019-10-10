from math import pi

from modules.PlotConfigs import VariableCfg as VCfg
from modules.binning import binning_svfitMass_finer, binning_mttotal, binning_mttotal_fine
import numpy as np

essential_vars = [
            # VCfg(name='_norm_'     , drawname='norm_count', binning={'nbinsx':5, 'xmin':-1.5, 'xmax':3.5}, unit='', xtitle='Normalisation'),
	    # VCfg(name='hnl_m_12_money' , drawname='hnl_m_12', binning={'nbinsx':6, 'xmin':0   , 'xmax':12.  }, unit='GeV', xtitle='dilepton mass (GeV)'),
	    # VCfg(name='hnl_2d_disp_wide',drawname='hnl_2d_disp', binning={'nbinsx':20, 'xmin':0   , 'xmax':20 }, unit='cm' , xtitle='2D displacement (cm)'),
	    # VCfg(name='hnl_2d_disp', binning={'nbinsx':10, 'xmin':0   , 'xmax':2. }, unit='cm' , xtitle='2D displacement'),

            # VCfg(name='m_triL_wide', drawname='hnl_w_vis_m',       binning={'nbinsx':40, 'xmin':0., 'xmax':200}, unit='GeV', xtitle='Tri-Lepton Mass (GeV)'),
            # VCfg(name='hnl_2d_disp_low',drawname='hnl_2d_disp', binning={'nbinsx':20, 'xmin':0   , 'xmax':0.02 }, unit='cm' , xtitle='2D displacement (cm)'),
            # VCfg(name='hnl_m_12_wide' , drawname='hnl_m_12', binning={'nbinsx':40, 'xmin':0   , 'xmax':120  }, unit='GeV', xtitle='dilepton mass (GeV)'),
            # VCfg(name='hnl_m_12_low' , drawname='hnl_m_12', binning={'nbinsx':22, 'xmin':0   , 'xmax':22.  }, unit='GeV', xtitle='dilepton mass (GeV)'),
            # VCfg(name='hnl_dr_12_wide', drawname='hnl_dr_12', binning={'nbinsx':20, 'xmin':0   , 'xmax':6. }, unit=None, xtitle='#DeltaR (#mu_{1}, #mu_{2})'),
            # VCfg(name='hnl_dr_12_low', drawname='hnl_dr_12', binning={'nbinsx':30, 'xmin':0   , 'xmax':0.6 }, unit=None, xtitle='#DeltaR (#mu_{1}, #mu_{2})'),
            # VCfg(name='hnl_m_01_wide', drawname = 'hnl_m_01', binning={'nbinsx':40, 'xmin':0.   , 'xmax':110 }, unit='GeV', xtitle='mass(l_{0},#mu_{1}) (GeV)'),
            # VCfg(name='hnl_m_02_wide', drawname = 'hnl_m_02', binning={'nbinsx':40, 'xmin':0.   , 'xmax':110 }, unit='GeV', xtitle='mass(l_{0},#mu_{2}) (GeV)'),
            # VCfg(name='l0_pt'      , binning={'nbinsx':20, 'xmin':0.  , 'xmax':120.}, unit='GeV', xtitle='l0 p_{T} (GeV)'),
            # VCfg(name='l1_pt'      , binning={'nbinsx':20, 'xmin':0.  , 'xmax':80.}, unit='GeV', xtitle='l1 p_{T} (GeV)'),
            # VCfg(name='l2_pt'      , binning={'nbinsx':20, 'xmin':0.  , 'xmax':50.}, unit='GeV', xtitle='l2 p_{T} (GeV)'),
            # VCfg(name='l1_dxy'      , binning={'nbinsx':40, 'xmin':-0.02  , 'xmax':.02}, unit='cm', xtitle='l1_dxy (GeV)'),
            # VCfg(name='l2_dxy'      , binning={'nbinsx':40, 'xmin':-0.02  , 'xmax':.02}, unit='cm', xtitle='l2_dxy (GeV)'),
            # VCfg(name='n_vtx', binning={'nbinsx':30, 'xmin':0, 'xmax':60}, unit=None, xtitle='N_{vertices}'),
            # VCfg(name='pfmet_pt'         , binning={'nbinsx':40, 'xmin':0., 'xmax':300.}, unit='GeV', xtitle='E_{T}^{miss} (PF) (GeV)'),
            # VCfg(name='sv_prob'          , binning={'nbinsx':40 , 'xmin':0   , 'xmax':1   }, unit=None, xtitle='SV probability'),
            # VCfg(name='l1_reliso_rho_03', binning={'nbinsx':20, 'xmin':0., 'xmax':0.5}, unit=None, xtitle='1st muon relative isolation cone 0.3'),
            # VCfg(name='l2_reliso_rho_03', binning={'nbinsx':20, 'xmin':0., 'xmax':0.5}, unit=None, xtitle='2nd muon relative isolation cone 0.3'),
            # VCfg(name='hnl_dphi_01'  ,drawname='abs_dphi_01', binning={'nbinsx':40, 'xmin': 0, 'xmax':pi+0.3}, unit=None, xtitle='|#Delta#phi (l_{0}, l_{1})|'),
            # VCfg(name='hnl_dphi_02'  ,drawname='abs_dphi_02', binning={'nbinsx':40, 'xmin': 0, 'xmax':pi+0.3}, unit=None, xtitle='|#Delta#phi (l_{0}, l_{2})|'),
            # VCfg(name='l0_phi'      , drawname='l0_phi',binning={'nbinsx':40, 'xmin':-pi  , 'xmax':pi}, unit='GeV', xtitle='l0 #phi'),
            # VCfg(name='l1_phi'      , drawname='l1_phi',binning={'nbinsx':40, 'xmin':-pi  , 'xmax':pi}, unit='GeV', xtitle='l1 #phi'),
            # VCfg(name='l2_phi'      , drawname='l2_phi',binning={'nbinsx':40, 'xmin':-pi  , 'xmax':pi}, unit='GeV', xtitle='l1 #phi'),
            # VCfg(name='dilepton_pt', drawname='hnl_hn_vis_pt',      binning={'nbinsx':20, 'xmin':0, 'xmax':80},    unit='GeV', xtitle='dilepton p_{T}'),
            # VCfg(name='hnl_hn_vis_eta', drawname='hnl_hn_vis_eta', binning={'nbinsx':40, 'xmin':-2.5, 'xmax':2.5 }, unit=None , xtitle='dilepton #eta'),
            # VCfg(name='hnl_hn_vis_phi', drawname='hnl_hn_vis_phi', binning={'nbinsx':40, 'xmin':-pi, 'xmax':pi }, unit=None , xtitle='dilepton #phi'),
            # VCfg(name='hnl_2d_disp_sig', drawname='hnl_2d_disp_sig', binning={'nbinsx':20, 'xmin':0., 'xmax':80. }, unit=None , xtitle='hnl_2d_disp_sig'),
            # VCfg(name='l1_dxy_error'      , binning={'nbinsx':40, 'xmin':0  , 'xmax':.02}, unit='cm', xtitle='l1_dxy_error'),
            # VCfg(name='l2_dxy_error'      , binning={'nbinsx':40, 'xmin':0  , 'xmax':.02}, unit='cm', xtitle='l2_dxy_error'),
            # VCfg(name='l0_eta'      , drawname='l0_eta',binning={'nbinsx':40, 'xmin':-2.6  , 'xmax':2.6}, unit='GeV', xtitle='l0 #eta'),
            # VCfg(name='l1_eta'      , drawname='l1_eta',binning={'nbinsx':40, 'xmin':-2.6  , 'xmax':2.6}, unit='GeV', xtitle='l1 #eta'),
            # VCfg(name='l2_eta'      , drawname='l2_eta',binning={'nbinsx':40, 'xmin':-2.6  , 'xmax':2.6}, unit='GeV', xtitle='l2 #eta'),
            # VCfg(name='hnl_q_01'     , drawname='hnl_q_01', binning={'nbinsx':7, 'xmin':-3, 'xmax':4}, unit='', xtitle='hnl_q_01'),
            # VCfg(name='hnl_q_02'     , drawname='hnl_q_02', binning={'nbinsx':7, 'xmin':-3, 'xmax':4}, unit='', xtitle='hnl_q_02'),
            # VCfg(name='hnl_dphi_12'  ,drawname='hnl_dphi_12', binning={'nbinsx':40, 'xmin': -(pi+0.3), 'xmax':pi+0.3}, unit=None, xtitle='#Delta#phi (l_{1}, l_{2})'),
            # VCfg(name='hnl_dr_01', drawname='hnl_dr_01', binning={'nbinsx':30, 'xmin':0   , 'xmax':6 }, unit=None, xtitle='#DeltaR (#mu_{0}, #mu_{1})'),
            # VCfg(name='hnl_dr_02', drawname='hnl_dr_02', binning={'nbinsx':30, 'xmin':0   , 'xmax':6 }, unit=None, xtitle='#DeltaR (#mu_{0}, #mu_{2})'),
            # VCfg(name='hnl_dphi_hnvis0_wide'  ,drawname='abs_dphi_hnvis0', binning={'nbinsx':40, 'xmin': 0, 'xmax':pi+0.3}, unit=None, xtitle='|#Delta#phi (dilepton, l_{0})|'),
            # VCfg(name='hnl_2d_disp_sig', drawname='hnl_2d_disp_sig', binning={'nbinsx':20, 'xmin':0., 'xmax':1000. }, unit=None , xtitle='hnl_2d_disp_sig'),
            # VCfg(name='abs_l1_dz', drawname = 'abs_l1_Dz', binning={'bins': np.logspace(-7,2,40)}, unit=None, xtitle='|l1 dz|'),
            # VCfg(name='abs_l2_dz', drawname = 'abs_l2_Dz', binning={'bins': np.logspace(-7,2,40)}, unit=None, xtitle='|l2 dz|'),
            # VCfg(name='hnl_m_12_money_disp1_0p5' , drawname='hnl_m_12', binning={'nbinsx':6, 'xmin':0   , 'xmax':12.  }, unit='GeV', xtitle='dilepton mass (GeV)'),
            # VCfg(name='hnl_m_12_money_disp2_0p5_10' , drawname='hnl_m_12', binning={'nbinsx':12, 'xmin':0   , 'xmax':12.  }, unit='GeV', xtitle='dilepton mass (GeV)'),
            # VCfg(name='hnl_m_12_money_disp3_10' , drawname='hnl_m_12', binning={'nbinsx':2, 'xmin':0   , 'xmax':12.  }, unit='GeV', xtitle='dilepton mass (GeV)'),

	    VCfg(name='Martina_nl_m_12_money' , drawname='hnl_m_12', binning={'nbinsx':20, 'xmin':0   , 'xmax':20.  }, unit='GeV', xtitle='dilepton mass (GeV)'),
	    VCfg(name='Martina_nl_m_12_money_disp1_0p5' , drawname='hnl_m_12', binning={'nbinsx':20, 'xmin':0   , 'xmax':20.  }, unit='GeV', xtitle='dilepton mass (GeV)'),
	    VCfg(name='Martina_nl_m_12_money_disp2_0p5_10' , drawname='hnl_m_12', binning={'nbinsx':20, 'xmin':0   , 'xmax':20.  }, unit='GeV', xtitle='dilepton mass (GeV)'),
	    VCfg(name='Martina_nl_m_12_money_disp3_10' , drawname='hnl_m_12', binning={'nbinsx':2, 'xmin':0   , 'xmax':20.  }, unit='GeV', xtitle='dilepton mass (GeV)'),
	    VCfg(name='Martina_nl_2d_disp',drawname='hnl_2d_disp', binning={'nbinsx':40, 'xmin':0   , 'xmax':8 }, unit='cm' , xtitle='2D displacement (cm)'),
	    VCfg(name='Martina_nl_dr_12', drawname='hnl_dr_12', binning={'nbinsx':40, 'xmin':0   , 'xmax':4. }, unit=None, xtitle='#DeltaR (#mu_{1}, #mu_{2})'),
	    VCfg(name='Martina__triL_wide', drawname='hnl_w_vis_m',       binning={'nbinsx':40, 'xmin':0., 'xmax':200}, unit='GeV', xtitle='Tri-Lepton Mass (GeV)'),
	    VCfg(name='Martina_2_dxy',drawname='l2_dxy'      , binning={'nbinsx':40, 'xmin':-0.02  , 'xmax':1.0}, unit='cm', xtitle='l2_dxy (GeV)'),
            # VCfg(name='hnl_m_12_money_2bins' , drawname='hnl_m_12', binning={'nbinsx':2, 'xmin':0   , 'xmax':12.  }, unit='GeV', xtitle='dilepton mass (GeV)'),
            # VCfg(name='hnl_m_12_money_6bins' , drawname='hnl_m_12', binning={'nbinsx':6, 'xmin':0   , 'xmax':12.  }, unit='GeV', xtitle='dilepton mass (GeV)'),
            # VCfg(name='hnl_m_12_money_12bins' , drawname='hnl_m_12', binning={'nbinsx':12, 'xmin':0   , 'xmax':12.  }, unit='GeV', xtitle='dilepton mass (GeV)'),
            # VCfg(name='hnl_m_12_money_disp3_10' , drawname='hnl_m_12', binning={'nbinsx':12, 'xmin':0   , 'xmax':12.  }, unit='GeV', xtitle='dilepton mass (GeV)'),
            # VCfg(name='l1_dz'      , binning={'nbinsx':40, 'xmin':-100  , 'xmax':100}, unit='GeV', xtitle='1st lepton dz'),
            # VCfg(name='l2_dz'      , binning={'nbinsx':40, 'xmin':-100  , 'xmax':100}, unit='GeV', xtitle='2nd lepton dz'),
	    # VCfg(name='hnl_m_12_cone_wide' , drawname='hnl_m_12_ConeCorrected2', binning={'nbinsx':120, 'xmin':0   , 'xmax':120  }, unit='GeV', xtitle='dilepton mass (cone corrected)'),
	    # VCfg(name='hnl_m_12_cone_low' , drawname='hnl_m_12_ConeCorrected2', binning={'nbinsx':22, 'xmin':0   , 'xmax':22.  }, unit='GeV', xtitle='dilepton mass (cone corrected)'),
	    # VCfg(name='hnl_m_12_cone_money' , drawname='hnl_m_12_ConeCorrected2', binning={'nbinsx':11, 'xmin':0   , 'xmax':11.  }, unit='GeV', xtitle='dilepton mass (cone corrected)'),
	    # VCfg(name='m12Cone_vs_m12' , drawname='m12Cone_vs_m12', binning={'nbinsx':105, 'xmin':0.95   , 'xmax':1.3  }, unit='GeV', xtitle='M_{12,cone} / M_{12}'),
            # VCfg(name='nbj', binning={'nbinsx':5, 'xmin':0, 'xmax':5}, unit=None, xtitle='N_{b-jets}'),
            # VCfg(name='ptCone', drawname='pt_cone',      binning={'nbinsx':20, 'xmin':0, 'xmax':70},    unit='GeV', xtitle='p^{Cone}_{T} (GeV)'),
	    # VCfg(name='l1_dz'      , binning={'nbinsx':40, 'xmin':-.02  , 'xmax':.02}, unit='GeV', xtitle='1st lepton dz'),
	    # VCfg(name='l2_dz'      , binning={'nbinsx':40, 'xmin':-.02  , 'xmax':.02}, unit='GeV', xtitle='2nd lepton dz'),
	    # VCfg(name='l1_ptcone_vs_pt', drawname='l1_ptcone_vs_pt',      binning={'nbinsx':105, 'xmin':0.95, 'xmax':2},    unit='GeV', xtitle='l1 p^{Cone}_{T} / l1 p_T'),
	    # VCfg(name='l2_ptcone_vs_pt', drawname='l2_ptcone_vs_pt',      binning={'nbinsx':105, 'xmin':0.95, 'xmax':2},    unit='GeV', xtitle='l2 p^{Cone}_{T} / l2 p_T'),
            # VCfg(name='sv_prob_zoom', drawname = 'sv_prob', binning={'nbinsx':20 , 'xmin':0   , 'xmax':.0000001   }, unit=None, xtitle='SV probability'),
	    # VCfg(name='sv_prob_zoom', drawname = 'sv_prob', binning={'bins': np.logspace(-12,0,50)}, unit=None, xtitle='SV probability'),
            # VCfg(name='hnl_m_12_zoom' , drawname='hnl_m_12', binning={'nbinsx':15, 'xmin':1   , 'xmax':4.  }, unit='GeV', xtitle='dilepton mass'),
	    # VCfg(name='hnl_m_01_zoom', drawname = 'hnl_m_01', binning={'nbinsx':10, 'xmin':40.   , 'xmax':50. }, unit='GeV', xtitle='mass(l_{0},#mu_{1})'),
	    # VCfg(name='hnl_m_02_zoom', drawname = 'hnl_m_02', binning={'nbinsx':20, 'xmin':0.   , 'xmax':10. }, unit='GeV', xtitle='mass(l_{0},#mu_{1})'),
            # VCfg(name='l2_dxy_zoom', drawname='l2_dxy', binning={'nbinsx':40, 'xmin':0.0075  , 'xmax':.0085}, unit='cm', xtitle='l2_dxy'),
            # VCfg(name='hnl_dr_12_zoom', drawname='hnl_dr_12', binning={'nbinsx':30, 'xmin':0  , 'xmax':3 }, unit=None, xtitle='#DeltaR (#mu_{1}, #mu_{2})'),
            # VCfg(name='m_triL_wide', drawname='hnl_w_vis_m',       binning={'nbinsx':40, 'xmin':75., 'xmax':105}, unit='GeV', xtitle='Tri-Lepton Mass'),
	    # VCfg(name='hnl_2d_disp_micro',drawname='hnl_2d_disp', binning={'nbinsx':20, 'xmin':0   , 'xmax':0.01 }, unit='cm' , xtitle='2D displacement'),
            # VCfg(name='l2_pt_low'      ,drawname='l1_pt', binning={'nbinsx':20, 'xmin':0.  , 'xmax':20.}, unit='GeV', xtitle='l2 p_{T}'),
            # VCfg(name='hnl_m_01_wide', drawname = 'hnl_m_01', binning={'nbinsx':40, 'xmin':80.   , 'xmax':100 }, unit='GeV', xtitle='mass(l_{0},#mu_{1})'),
            # VCfg(name='eta(di_L,l0)'   ,drawname='eta_hnl_l0', binning={'nbinsx':40, 'xmin':-2.5, 'xmax':2.5 }, unit=None , xtitle='Delta #eta (dilepton, l_{0})'),
            # VCfg(name='hnl_2d_disp_low',drawname='hnl_2d_disp', binning={'nbinsx':20, 'xmin':0   , 'xmax':0.05 }, unit='cm' , xtitle='2D displacement'),
            # VCfg(name='hnl_2d_disp', binning={'nbinsx':20, 'xmin':0   , 'xmax':.1 }, unit='cm' , xtitle='2D displacement'),
            # VCfg(name='abs_l2_eta'      , drawname='abs_l2_eta',binning={'nbinsx':20, 'xmin':0.  , 'xmax':2.5}, unit='GeV', xtitle='2nd muon |#eta|'),
	    # VCfg(name='l1_ptCone', drawname='l1_ptcone',      binning={'nbinsx':20, 'xmin':0, 'xmax':50},    unit='GeV', xtitle='l1 p^{Cone}_{T}'),
	    # VCfg(name='l2_ptCone', drawname='l2_ptcone',      binning={'nbinsx':20, 'xmin':0, 'xmax':50},    unit='GeV', xtitle='l2 p^{Cone}_{T}'),
            # VCfg(name='abs_l2_dxy'      , binning={'nbinsx':50, 'xmin':0.  , 'xmax':.1}, unit='GeV', xtitle='2nd lepton dxy'),
            # VCfg(name='doubleFakeRate', drawname = 'doubleFakeRate', binning={'nbinsx':100, 'xmin':0.   , 'xmax':1. }, unit='', xtitle='dilepton double fakerate'),
            # VCfg(name='abs_hnl_hn_vis_eta', drawname='abs_hnl_hn_vis_eta', binning={'nbinsx':20, 'xmin':0., 'xmax':2.5 }, unit=None , xtitle='dilepton #eta'),
            # VCfg(name='hnl_dr_12', drawname='hnl_dr_12', binning={'nbinsx':30, 'xmin':0   , 'xmax':6 }, unit=None, xtitle='#DeltaR (#mu_{1}, #mu_{2})'),
            # VCfg(name='hnl_q_01', drawname='hnl_q_01', binning={'nbinsx':5, 'xmin':-2   , 'xmax':3 }, unit=None, xtitle='#DeltaR (charge 01)'),
            # VCfg(name='hnl_q_02', drawname='hnl_q_02', binning={'nbinsx':5, 'xmin':-2   , 'xmax':3 }, unit=None, xtitle='#DeltaR (charge 02)'),
            # VCfg(name='hnl_q_12', drawname='hnl_q_12', binning={'nbinsx':5, 'xmin':-2   , 'xmax':3 }, unit=None, xtitle='#DeltaR (charge 12)'),
            # VCfg(name='hnl_m_12_corrected' , drawname='hnl_m_12_ConeCorrected', binning={'nbinsx':20, 'xmin':0   , 'xmax':10  }, unit='GeV', xtitle='dilepton mass'),
            # VCfg(name='hnl_m_12_corrected_test' , drawname='hnl_m_12_ConeCorrected_test', binning={'nbinsx':20, 'xmin':0   , 'xmax':10  }, unit='GeV', xtitle='dilepton mass'),
            # VCfg(name='m_triL_wide', drawname='hnl_w_vis_m',       binning={'nbinsx':20, 'xmin':70., 'xmax':110}, unit='GeV', xtitle='Tri-Lepton Mass'),
            # VCfg(name='hnl_m_01_wide', drawname = 'hnl_m_01', binning={'nbinsx':30, 'xmin':50.   , 'xmax':110 }, unit='GeV', xtitle='mass(l_{0},#mu_{1})'),
            # VCfg(name='hnl_2d_disp', binning={'nbinsx':20, 'xmin':0   , 'xmax':2. }, unit='cm' , xtitle='2D displacement'),
            # VCfg(name='l0_pt'      , binning={'nbinsx':10, 'xmin':0.  , 'xmax':100.}, unit='GeV', xtitle='prompt lepton p_{T}'),
            # VCfg(name='l1_pt'      , binning={'nbinsx':6, 'xmin':0.  , 'xmax':60.}, unit='GeV', xtitle='1st muon p_{T}'),
            # VCfg(name='m_triL_SR', drawname='hnl_w_vis_m',       binning={'nbinsx':5, 'xmin':40., 'xmax':90}, unit='GeV', xtitle='Tri-Lepton Mass'),
            # VCfg(name='m_triL_Z', drawname='hnl_w_vis_m',       binning={'nbinsx':30, 'xmin':80., 'xmax':110}, unit='GeV', xtitle='Tri-Lepton Mass'),
            # VCfg(name='doubleFakeRate', drawname='doubleFakeRate',      binning={'nbinsx':100, 'xmin':0, 'xmax':0.3},    unit='', xtitle='double fake rate'),
            # VCfg(name='doubleFakeWeight', drawname='doubleFakeWeight',      binning={'nbinsx':100, 'xmin':0, 'xmax':0.3},    unit='', xtitle='double fake weight'),
            # VCfg(name='pfmet_phi'        , binning={'nbinsx':40, 'xmin':-3.141593, 'xmax':3.141593}, unit=None, xtitle='E_{T}^{miss} #Phi (PF)'),
            # VCfg(name='pfmet_pt'         , binning={'nbinsx':40, 'xmin':0., 'xmax':300.}, unit='GeV', xtitle='E_{T}^{miss} (PF)'),

            #RESONANCES
            # VCfg(name='hnl_m_12_eta' , drawname='hnl_m_12', binning={'nbinsx':20, 'xmin':0.40   , 'xmax':0.7  }, unit='GeV', xtitle='dilepton mass'),
            # VCfg(name='hnl_m_12_rho' , drawname='hnl_m_12', binning={'nbinsx':20, 'xmin':0.63   , 'xmax':0.84  }, unit='GeV', xtitle='dilepton mass'),
            # VCfg(name='hnl_m_12_omega' , drawname='hnl_m_12', binning={'nbinsx':20, 'xmin':0.776   , 'xmax':0.789  }, unit='GeV', xtitle='dilepton mass'),
            # VCfg(name='hnl_m_12_phi' , drawname='hnl_m_12', binning={'nbinsx':20, 'xmin':0.09   , 'xmax':0.05  }, unit='GeV', xtitle='dilepton mass'),
            # VCfg(name='hnl_m_12_JPsi' , drawname='hnl_m_12', binning={'nbinsx':20, 'xmin':2.8   , 'xmax':3.3  }, unit='GeV', xtitle='dilepton mass'),
	    # VCfg(name='hnl_m_12_JPsi2S' , drawname='hnl_m_12', binning={'nbinsx':15, 'xmin':3.2   , 'xmax':4.2  }, unit='GeV', xtitle='dilepton mass'),
	    # VCfg(name='hnl_m_12_Upsilon' , drawname='hnl_m_12', binning={'nbinsx':15, 'xmin':8.80   , 'xmax':10.20  }, unit='GeV', xtitle='dilepton mass'),
            # VCfg(name='hnl_m_12_Upsilon2S' , drawname='hnl_m_12', binning={'nbinsx':20, 'xmin':9.88   , 'xmax':10.16  }, unit='GeV', xtitle='dilepton mass'),
            # VCfg(name='hnl_m_12_Upsilon3S' , drawname='hnl_m_12', binning={'nbinsx':20, 'xmin':10.21   , 'xmax':10.49  }, unit='GeV', xtitle='dilepton mass'),
	    # VCfg(name='hnl_m_12_Z' , drawname='hnl_m_12', binning={'nbinsx':15, 'xmin':80   , 'xmax':100  }, unit='GeV', xtitle='dilepton mass'),
           ]

resonances = sorted([ #(mass, expected experimental width, ID)
    ( 0.5479, 0.030,  1), # eta
    ( 0.7753, 0.075,  2), # rho # not very narrow... maybe relax this?
    ( 0.7827, 0.030,  3), # omega
    ( 1.0195, 0.030,  4), # phi
    ( 3.0969, 0.030,  5), # J/Psi
    ( 3.6861, 0.030,  6), # J/Psi (2S)
    ( 9.4603, 0.070,  7), # Upsilon
    (10.0233, 0.070,  8), # Upsilon (2S)
    (10.3552, 0.070,  9), # Upsilon (3S)
    (91.1976, 2.495, 10), # Z
    ], key=lambda x: x[1]
)

def getVars(names, channel='all'):
    return [dict_channel_vars[channel][n] for n in names]
