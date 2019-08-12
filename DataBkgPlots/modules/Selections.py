from pdb import set_trace
def defineDataCut(promptLeptonType):
    goodVertices                 = '  &&  Flag_goodVertices'    
    globalSuperTightHalo2016     = '  &&  Flag_globalSuperTightHalo2016Filter'    
    HBHENoise                    = '  &&  Flag_HBHENoiseFilter'                   
    HBHENoiseIso                 = '  &&  Flag_HBHENoiseIsoFilter'                
    EcalDeadCellTriggerPrimitive = '  &&  Flag_EcalDeadCellTriggerPrimitiveFilter'
    BadPFMuon                    = '  &&  Flag_BadPFMuonFilter'                   
    BadChargedCandidate          = '  &&  Flag_BadChargedCandidateFilter'         
    eeBadSc                      = '  &&  Flag_eeBadScFilter'                     
    ecalBadCalib                 = '  &&  Flag_ecalBadCalibFilter'                

    if promptLeptonType == "ele": 
        datacut   = goodVertices + globalSuperTightHalo2016 + HBHENoise + HBHENoiseIso + EcalDeadCellTriggerPrimitive + BadPFMuon + BadChargedCandidate + eeBadSc + ecalBadCalib 
    if promptLeptonType == "mu": 
        datacut   = 'l0_id_t' #Placeholder

    return datacut

def Z_veto():
    Z_veto_01       = '( (l0_q + l1_q == 0) && (abs(hnl_m_01 - 91.2) > 15) )  &&  (l0_q + l2_q != 0)  &&  (l1_q + l2_q != 0)'
    Z_veto_02       = '(l0_q + l1_q != 0)  &&  ( (l0_q + l2_q == 0) && (abs(hnl_m_02 - 91.2) > 15) )  &&  (l1_q + l2_q != 0)'
    Z_veto_12       = '(l0_q + l1_q != 0)  &&  (l0_q + l2_q != 0)  &&  ( (l1_q + l2_q == 0) && (abs(hnl_m_12 - 91.2) > 15) )' 

    Z_veto_01_02    = '( (l0_q + l1_q == 0) && (abs(hnl_m_01 - 91.2) > 15) )  &&  ( (l0_q + l2_q == 0) && (abs(hnl_m_02 - 91.2) > 15) )  &&  (l1_q + l2_q != 0)'  
    Z_veto_01_12    = '( (l0_q + l1_q == 0) && (abs(hnl_m_01 - 91.2) > 15) )  &&  (l0_q + l2_q != 0)  &&  ( (l1_q + l2_q == 0) && (abs(hnl_m_12 - 91.2) > 15) )'  
    Z_veto_02_12    = '(l0_q + l1_q != 0)  &&  ( (l0_q + l2_q == 0) && (abs(hnl_m_02 - 91.2) > 15) )  &&  ( (l1_q + l2_q == 0) && (abs(hnl_m_12 - 91.2) > 15) )'  

    Z_veto_01_02_12 = '( (l0_q + l1_q == 0) && (abs(hnl_m_01 - 91.2) > 15) )  &&  ( (l0_q + l2_q == 0) && (abs(hnl_m_02 - 91.2) > 15) )  &&  ( (l1_q + l2_q == 0) && (abs(hnl_m_12 - 91.2) > 15) )'

    single_Z_veto = '(  ' + Z_veto_01 + '   ||   ' + Z_veto_02 + '   ||   ' + Z_veto_12 + '  )'
    double_Z_veto = '(  ' + Z_veto_01_02 + '   ||   ' + Z_veto_01_12 + '   ||   ' + Z_veto_02_12 + '  )'

    Z_veto = ' && (   ' + single_Z_veto + '    ||    ' + double_Z_veto + '    ||    ' + Z_veto_01_02_12 + '   )' 
    return Z_veto

def CR_ttbar():
    selection = ('abs(hnl_m_12 - 91.18) > 15 ' #suppress Z 
                '&& abs(hnl_w_vis_m - 91.18) > 15 ' #suppress conversions 
                '&& hnl_m_12 > 12 ' #suppress conversions
                '&& nbj >=1 '
                )
    # selection = selection + Z_veto()
    return selection

def SR(channel):
    if channel is 'mmm':
        selection = '&'.join([
        'l0_pt > 25 '              , 
        'abs(l0_eta) < 2.4 '       ,
        'abs(l0_dz) < 0.2 '        ,
        'abs(l0_dxy) < 0.05 '      ,
        'l0_reliso_rho_03 < 0.2 '  ,
        'l0_id_m == 1  '           ,

        'l1_pt > 5 '              ,
        'abs(l1_eta) < 2.4 '       ,
        'abs(l1_dxy) > 0.002 '      ,
	# 'abs(l1_dxy) > 0.01 '      ,
	# 'abs(l1_dz) < 5',

        'l2_pt > 5 '               ,
        'abs(l2_eta) < 2.4 '       ,
        'abs(l2_dxy) > 0.002 '       ,
	# 'abs(l2_dxy) > 0.01 '       ,
	# 'abs(l2_dz) < 5',

        'hnl_q_12 == 0 '           ,
        # 'hnl_2d_disp > 0.0005',
        # 'hnl_dr_02 > 0.2',
        # 'hnl_dr_01 > 0.2',
        'abs(hnl_dphi_hnvis0) > 0.9 ',
        '(abs(hnl_m_12 - 3.1) > 0.05)', # avoid JPsi

        'hnl_m_12 < 80', # because this is the mass range our analysis is aiming for (and get rid of the Z peak)

	#Throw it on only for plotting
        
	# '(nbj == 0)',
	# '(hnl_w_vis_m > 50. && hnl_w_vis_m < 80.) ', 
        
        # '!(nbj == 0)', # activate for SR orthogonal
	# '!(hnl_w_vis_m > 50. && hnl_w_vis_m < 80.) ', # activate for SR orthogonal (sideband)
        '((!(nbj == 0)) || (!(hnl_w_vis_m > 50. && hnl_w_vis_m < 80.)))', #activate to train on all orthogonal regions
        
        ## auxiliary selections
        # '(hnl_w_vis_m > 80. && hnl_w_vis_m < 90.) ', # isolate conversions
	# 'hnl_dr_12 > 0.025', # the trick to make plots look nicer
        # '!(hnl_m_01 > 82.0 && hnl_m_01 < 95.) ', # get rid of Z peak
        # '!(hnl_w_vis_m > 80. && hnl_w_vis_m < 94.) ', # get rid of Z peak
        'sv_prob > 0.01', #get rid of bad vertex fit events
        ])

        selection_ignoreEverything = 'l1_pt > 0'

    # return selection_ignoreEverything
    return selection



def DY():
    selection = ('l0_pt>25 && abs(l0_eta)<2.4 && (l0_q != l1_q) '
                '&& l1_pt > 15 && abs(l1_eta) < 2.4 '
                '&& abs(l0_dxy) < 0.05 && abs(l0_dz) < 0.2 '
                '&& abs(l1_dxy) < 0.05 && abs(l1_dz) < 0.2 '
                '&& nbj == 0 '
                '&& l0_id_t ==1'
                '&& l1_id_t ==1'
                # '&& l1_eid_mva_iso_wp90'
                '&& l2_id_m ==1'
                '&& l0_reliso_rho_03 < 0.20 '
                # '&& l1_reliso_rho_03 < 0.20 '
                # '&& l2_reliso_rho_03 < 0.20 '
                # '&& abs(hnl_m_01 - 91.2) < 15 '
                '&& abs(hnl_dphi_hnvis0) > 2.0 '
                '&& abs(hnl_dphi_hnvis0) < 3.0 '
                )
    return selection

def Conversions(channel):
    selection = ('l0_pt>25 && abs(l0_eta)<2.4 && (l0_q != l1_q) '
                 '&& nbj == 0 '
                 '&& l0_reliso_rho_03 < 0.20 '
                 '&& l1_reliso_rho_03 < 0.20 '
                 '&& l2_reliso_rho_03 < 0.20 '
                 '&& hnl_w_vis_m > 50'
                 )
    return selection

def MR_nonprompt(channel): 
    if channel is 'mmm':
        selection = '&'.join([
        'l0_pt > 25 '              , 
        'abs(l0_eta) < 2.4 '       ,
        'abs(l0_dz) < 0.2 '        ,
        'abs(l0_dxy) < 0.05 '      ,
        'l0_reliso_rho_03 < 0.2 '  ,
        'l0_id_m == 1  '           ,

        'l1_pt > 5 '              ,
        'abs(l1_eta) < 2.4 '       ,
        # 'abs(l1_dxy) > 0.002 '      ,
        'abs(l1_dz) < 5',

        'l2_pt > 5 '               ,
        'abs(l2_eta) < 2.4 '       ,
        # 'abs(l2_dxy) > 0.002 '       ,
        'abs(l2_dz) < 5',

        'hnl_q_12 == 0 '           ,
        # 'hnl_dr_02 > 0.3',
        # 'hnl_dr_01 > 0.3',
        'abs(hnl_dphi_hnvis0) > 1.0 ',
        '(abs(hnl_m_12 - 3.1) > 0.05)', # avoid JPsi
        
        '(nbj == 0)',
        # '(hnl_w_vis_m > 50. && hnl_w_vis_m < 80.) ', 
        
        # '!(nbj == 0)', # activate for SR orthogonal
        '!(hnl_w_vis_m > 50. && hnl_w_vis_m < 80.) ', # activate for SR orthogonal
        
        ])

        selection_ignoreEverything = 'l1_pt > 0'

    # return selection_ignoreEverything
    return selection

def MR_DF(channel): 
    if channel is 'mmm':
        selection = (
                    'l0_pt > 25 '
                    '&& abs(l0_eta) < 2.4 '
                    '&& abs(l0_dz) < 0.2 '
                    '&& abs(l0_dxy) < 0.05 '
                    '&& l0_reliso_rho_03 < 0.2 '
                    '&& l0_id_m == 1 '
                    '&& l1_pt > 5 '
                    # '&& l1_pt > 10 '
                    '&& abs(l1_eta) < 2.4 '
                    # '&& abs(l1_dz) < 2 '#Martina uses 10
                    # '&& abs(l1_dxy) > 0.05 '
                    '&& l2_pt > 5 '
                    # '&& l2_pt > 10 '
                    '&& abs(l2_eta) < 2.4 '
                    # '&& abs(l2_dz) < 2 '#Martina uses 10
                    # '&& abs(l2_dxy) > 0.05 '
                    '&& hnl_q_12 == 0 '
                    # '&& hnl_2d_disp > 0.05 ' # included by default, can be removed for more statistics
                    # '&& hnl_2d_disp > 0.1 ' # included by default, can be removed for more statistics
                    # '&& nbj > 0 ' # measure DFs
                    # '&& hnl_w_vis_m > 20. '
                    '&& (hnl_w_vis_m < 50. || hnl_w_vis_m > 80.) '
                    # '&& (hnl_dr_12 < 0.05)' # just for some debugging, not included by default
                    # '&& (hnl_dr_12 > 0.05)' # just for some debugging, not included by default
                    # '&& (hnl_dr_12 > 0.02)'
                    )
        return selection

def MR_DF_closure(channel): 
    if channel is 'mmm':
        selection = (
                    'l0_pt > 25 '
                    '&& abs(l0_eta) < 2.4 '
                    '&& abs(l0_dz) < 0.2 '
                    '&& abs(l0_dxy) < 0.05 '
                    '&& l0_reliso_rho_03 < 0.2 '
                    '&& l0_id_m == 1 '
                    '&& l1_pt > 5 '
                    '&& abs(l1_eta) < 2.4 '
                    # '&& abs(l1_dz) < 2 '#Martina uses 10
                    '&& l2_pt > 5 '
                    '&& abs(l2_eta) < 2.4 '
                    # '&& abs(l2_dz) < 2 '#Martina uses 10
                    # '&& abs(l1_dxy) > 0.01 '
                    # '&& abs(l2_dxy) > 0.01 '
                    '&& hnl_q_12 == 0 '
                    # '&& hnl_2d_disp > 0.05 ' # included by default, can be removed for more statistics
                    # '&& hnl_2d_disp > 0.1 ' # included by default, can be removed for more statistics
                    # '&& nbj > 0 ' # measure DFs
                    # '&& hnl_w_vis_m > 20. '
                    '&& (hnl_w_vis_m < 50. || hnl_w_vis_m > 80.) '
                    # '&& (hnl_dr_12 < 0.05)' # just for some debugging, not included by default
                    # '&& (hnl_dr_12 > 0.05)' # just for some debugging, not included by default
                    # '&& (hnl_dr_12 > 0.02)'
                    # '&& !(abs(hnl_m_01 - 91.2) < 15 && hnl_q_01 == 0)'
                    # '&& !(abs(hnl_m_02 - 91.2) < 15 && hnl_q_02 == 0)'
                    '&& hnl_dr_12 > 0.05'
                    )
        return selection

def MR_SF1(channel): 
    if channel is 'mmm':
        selection = '&'.join([
        'l0_pt > 25 '              ,
        'abs(l0_eta) < 2.4 '       ,
        'abs(l0_dz) < 0.2 '        ,
        'abs(l0_dxy) < 0.05 '      ,
        'l0_reliso_rho_03 < 0.2 '  ,
        'l0_id_m == 1  '           ,

        'l2_pt > 10 '              ,
        'abs(l2_eta) < 2.4 '       ,
        'abs(l2_dz) < 0.2 '        ,
        'abs(l2_dxy) < 0.05 '      ,
        'l2_reliso_rho_03 < 0.2 '  ,
        'l2_id_m == 1  '           ,

        'l1_pt > 5 '               ,
        'abs(l1_eta) < 2.4 '       ,
        'l1_dxy > 0.01 '       ,

        # 'nbj == 0'                 ,
        'hnl_q_02 == 0 '           ,
        # '!(abs(hnl_m_01 - 91.2) < 15 && hnl_q_01 == 0)',
        ])
    return selection

def MR_SF2(channel): 
    if channel is 'mmm':
        selection = '&'.join([
        'l0_pt > 25 '              , 
        'abs(l0_eta) < 2.4 '       ,
        'abs(l0_dz) < 0.2 '        ,
        'abs(l0_dxy) < 0.05 '      ,
        'l0_reliso_rho_03 < 0.2 '  ,
        'l0_id_m == 1  '           ,

        'l1_pt > 10 '              ,
        'abs(l1_eta) < 2.4 '       ,
        'abs(l1_dz) < 0.2 '        ,
        'abs(l1_dxy) < 0.05 '      ,
        'l1_reliso_rho_03 < 0.2 '  ,
        'l1_id_m == 1  '           ,

        'l2_pt > 5 '               ,
        'abs(l2_eta) < 2.4 '       ,
        # 'l2_dxy > 0.01 '       ,

        # 'nbj == 0'                 ,
        'hnl_q_01 == 0 '           ,
        'hnl_dr_02 > 0.3',
        'hnl_dr_01 > 0.3',
        'hnl_dr_12 > 0.3',
        # '!(abs(hnl_m_02 - 91.2) < 15 && hnl_q_02 == 0)',
        ])
    return selection

def MR_SF2_closure(channel): 
    if channel is 'mmm':
        selection = '&'.join([
        'l0_pt > 25 '              , 
        'abs(l0_eta) < 2.4 '       ,
        'abs(l0_dz) < 0.2 '        ,
        'abs(l0_dxy) < 0.05 '      ,
        'l0_reliso_rho_03 < 0.2 '  ,
        'l0_id_m == 1  '           ,

        'l1_pt > 10 '              ,
        # 'l1_pt > 5 '              ,
        'abs(l1_eta) < 2.4 '       ,
        'abs(l1_dz) < 0.2 '        ,
        'abs(l1_dxy) < 0.05 '      ,
        # 'l1_reliso_rho_03 < 0.2 '  ,
        # 'l1_id_m == 1  '           ,

        'l2_pt > 5 '               ,
        'abs(l2_eta) < 2.4 '       ,
        'l2_dxy > 0.01 '       ,

        # 'nbj == 0'                 ,
        'hnl_q_01 == 0 '           ,
        # '!(abs(hnl_m_02 - 91.2) < 15 && hnl_q_02 == 0)',
        'hnl_dr_02 > 0.3',
        'hnl_dr_01 > 0.3',
        # 'hnl_dr_12 > 0.3',
        # '&& abs(hnl_dphi_hnvis0) > 1.0 '
        ])
    return selection



def getSelection(channel, selection_name):
    if channel == 'mmm':
        #testing the old version
        if selection_name == 'baseline':
            selection = baseline(channel)
            
            # selection = selection + Z_veto() 

        if selection_name == 'ttbar':
            selection = CR_ttbar()
                        
        if selection_name == 'DY':
            selection = DY()

        if selection_name == 'MR_DF':
            selection = MR_DF(channel)
                        
        if selection_name == 'MR_DF_closure':
            selection = MR_DF_closure(channel)
                        
        if selection_name == 'MR_SF1':
            selection = MR_SF1(channel)
        
        if selection_name == 'MR_SF2':
            selection = MR_SF2(channel)
        
        if selection_name == 'MR_SF2_closure':
            selection = MR_SF2_closure(channel)
        
        if selection_name == 'SR':
            selection = SR(channel)
                        
        if selection_name == 'SR_orth':
            selection = SR_orth(channel)
                        
        if selection_name == 'MR_nonprompt':
            # selection = MR_nonprompt(channel)
            selection = SR(channel)

        if selection_name == 'Conversions':
            selection = Conversions(channel)
                        
        if selection_name == 'T_T':
            selection = ('('
                        'l1_reliso_rho_03 < 0.2 ' 
                        '&& l2_reliso_rho_03 < 0.2 '
                        '&& l1_Medium == 1 '
                        '&& l2_Medium == 1 '
                        ')'
                        )
                        
        if selection_name == 'LNT_T':
            selection = ('!((l1_reliso_rho_03 < 0.2) '
                        '&& (l1_Medium == 1)) ' 
                        '&& ((l2_reliso_rho_03 < 0.2) '
                        '&& (l2_Medium == 1)) '
                        '&& ((l1_reliso_rho_03 < 0.38 && abs(l1_eta) < 1.2) || (l1_reliso_rho_03 < 0.29 && abs(l1_eta) > 1.2 && abs(l1_eta) < 2.1) || (l1_reliso_rho_03 < 0.20 && abs(l1_eta) > 2.1))'
                        )
                        
        if selection_name == 'T_LNT':
            selection = ('!((l2_reliso_rho_03 < 0.2) '
                        '&& (l2_Medium == 1)) ' 
                        '&& ((l1_reliso_rho_03 < 0.2) '
                        '&& (l1_Medium == 1)) '
                        '&& ((l2_reliso_rho_03 < 0.38 && abs(l2_eta) < 1.2) || (l2_reliso_rho_03 < 0.29 && abs(l2_eta) > 1.2 && abs(l2_eta) < 2.1) || (l2_reliso_rho_03 < 0.20 && abs(l2_eta) > 2.1))'
                        )
                        
        if selection_name == 'LNT_LNT_uncorrelated':
            selection = (
                        '   ((l1_reliso_rho_03 < 0.38 && abs(l1_eta) < 1.2) || (l1_reliso_rho_03 < 0.29 && abs(l1_eta) > 1.2 && abs(l1_eta) < 2.1) || (l1_reliso_rho_03 < 0.20 && abs(l1_eta) > 2.1))'
                        '&& ((l2_reliso_rho_03 < 0.38 && abs(l2_eta) < 1.2) || (l2_reliso_rho_03 < 0.29 && abs(l2_eta) > 1.2 && abs(l2_eta) < 2.1) || (l2_reliso_rho_03 < 0.20 && abs(l2_eta) > 2.1))'
                        '&& !((abs(l1_jet_pt - l2_jet_pt) < 1) && ((hnl_dr_12 < 0.3)))'
                        '&& !((l1_reliso_rho_03 < 0.2) && (l1_Medium == 1)) '
                        '&& !((l2_reliso_rho_03 < 0.2) && (l2_Medium == 1)) '
                        )
                        
        if selection_name == 'LNT_LNT_correlated':
            selection = (
                        '(hnl_iso04_rel_rhoArea < 2) ' 
                        '&& ((abs(l1_jet_pt - l2_jet_pt) < 1) && ((hnl_dr_12 < 0.3)))'
                        '&& !((l1_reliso_rho_03 < 0.2) && (l1_Medium == 1)) '
                        '&& !((l2_reliso_rho_03 < 0.2) && (l2_Medium == 1)) '
                        )

        if selection_name == 'L_T':
            selection = ( 
                        '((l1_reliso_rho_03 < 0.38 && abs(l1_eta) < 1.2) || (l1_reliso_rho_03 < 0.29 && abs(l1_eta) > 1.2 && abs(l1_eta) < 2.1) || (l1_reliso_rho_03 < 0.20 && abs(l1_eta) > 2.1))'
                        '&& ((l2_reliso_rho_03 < 0.2) && (l2_Medium == 1)) '
                        )
                        
        if selection_name == 'T_L':
            selection = ( 
                        '((l2_reliso_rho_03 < 0.38 && abs(l2_eta) < 1.2) || (l2_reliso_rho_03 < 0.29 && abs(l2_eta) > 1.2 && abs(l2_eta) < 2.1) || (l2_reliso_rho_03 < 0.20 && abs(l2_eta) > 2.1))'
                        '&& ((l1_reliso_rho_03 < 0.2) && (l1_Medium == 1)) '
                        )
                        
        if selection_name == 'L_L_uncorrelated':
            selection = (
                        '   ((l1_reliso_rho_03 < 0.38 && abs(l1_eta) < 1.2) || (l1_reliso_rho_03 < 0.29 && abs(l1_eta) > 1.2 && abs(l1_eta) < 2.1) || (l1_reliso_rho_03 < 0.20 && abs(l1_eta) > 2.1))'
                        '&& ((l2_reliso_rho_03 < 0.38 && abs(l2_eta) < 1.2) || (l2_reliso_rho_03 < 0.29 && abs(l2_eta) > 1.2 && abs(l2_eta) < 2.1) || (l2_reliso_rho_03 < 0.20 && abs(l2_eta) > 2.1))'
                        '&& !((abs(l1_jet_pt - l2_jet_pt) < 1) && ((hnl_dr_12 < 0.3)))'
                        )
                        
        if selection_name == 'L_L_correlated':
            selection = (
                        '(hnl_iso04_rel_rhoArea < 2) ' 
                        '&& ((abs(l1_jet_pt - l2_jet_pt) < 1) && ((hnl_dr_12 < 0.3)))'
                        )

        if selection_name == 'LNT_LNT':
            selection = (
                        '   ((l1_reliso_rho_03 < 0.38 && abs(l1_eta) < 1.2) || (l1_reliso_rho_03 < 0.29 && abs(l1_eta) > 1.2 && abs(l1_eta) < 2.1) || (l1_reliso_rho_03 < 0.20 && abs(l1_eta) > 2.1))'
                        '&& ((l2_reliso_rho_03 < 0.38 && abs(l2_eta) < 1.2) || (l2_reliso_rho_03 < 0.29 && abs(l2_eta) > 1.2 && abs(l2_eta) < 2.1) || (l2_reliso_rho_03 < 0.20 && abs(l2_eta) > 2.1))'
                        '&& !((l1_reliso_rho_03 < 0.2) && (l1_Medium == 1)) '
                        '&& !((l2_reliso_rho_03 < 0.2) && (l2_Medium == 1)) '
                        )
                        
    
        if selection_name == 'datacut':
            selection = defineDataCut('mu')
 
    return selection



#################################################################3
class Region(object):
    def __init__(self,name,channel,CR):
        Prompt_extension                = ' && (l1_gen_match_isPromptFinalState == 1 && l2_gen_match_isPromptFinalState == 1)'
        self.name                       = name
        self.channel                    = channel
        self.CR                         = CR
        #options: MR_DF, MR_SF, SR, DY, Conversions 
        self.baseline                   = '(' + ' && '\
                                          .join([\
                                          getSelection(channel,self.CR),\
                                          # getSelection(channel,'L_L_uncorrelated'),\
                                          # getSelection(channel,'L_L_correlated'),\
                                          ]) + ')' 
        self.data                       = '(' + ' && '\
                                          .join([\
                                          self.baseline,\
                                          # getSelection(channel,'L_L_uncorrelated'),\
                                          # getSelection(channel,'L_L_correlated'),\
                                          # getSelection(channel,'T_LNT'),\
                                          getSelection(channel,'T_T'),\
                                          ]) + ')' 
	self.signal 			= self.data
        self.MC                         = self.data 
        self.SF_LT                      = '(' + ' && '\
                                          .join([\
                                          self.baseline,\
                                          getSelection(channel,'L_L_uncorrelated'),\
                                          getSelection(channel,'LNT_T'),\
                                          ]) + ')' 
        self.SF_TL                      = '(' + ' && '\
                                          .join([\
                                          self.baseline,\
                                          getSelection(channel,'L_L_uncorrelated'),\
                                          getSelection(channel,'T_LNT'),\
                                          ]) + ')' 
        self.SF_LL                      = '(' + ' && '\
                                          .join([\
                                          self.baseline,\
                                          getSelection(channel,'LNT_LNT_uncorrelated'),\
                                          ]) + ')' 
        self.DF                         = '(' + ' && '\
                                          .join([\
                                          self.baseline,\
                                          getSelection(channel,'LNT_LNT_correlated'),\
                                          ]) + ')' 
        self.nonprompt                  = '(' + ' && '\
                                          .join([\
                                          self.baseline,\
                                          getSelection(channel,'LNT_LNT'),\
                                          ]) + ')' 


        self.MC_Conversions             = self.MC        + Prompt_extension
        self.MC_contamination_pass      = self.MC        + Prompt_extension
        self.MC_contamination_fail      = self.nonprompt + Prompt_extension

