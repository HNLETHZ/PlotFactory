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
    selection = (
                 'l0_pt > 25 && abs(l0_eta) < 2.4' 
                 '&& l0_id_m ==1'
                 '&& l0_reliso_rho_03 < 0.10 '
                 '&& abs(l0_dxy) < 0.05 && abs(l0_dz) < 0.2 '
                 '&& l1_Medium == 1 '
                 '&& l2_Medium == 1 '
                 '&& l1_pt > 5 && abs(l1_eta) < 2.4 '
                 '&& l2_pt > 5 && abs(l2_eta) < 2.4 '
                 # '&& hnl_2d_disp > 0.5'#removed for higher stat
                 # '&& abs(l1_dxy) > 0.01'
                 # '&& abs(l2_dxy) > 0.01'
                 '&& (l1_q != l2_q) '
                 # '&& nbj == 0 ' 
                 '&& nbj > 0 ' #activate for orthogonal SR
                 '&& 50 < hnl_w_vis_m && hnl_w_vis_m < 85'
                 # '&& 85 < hnl_w_vis_m' #activate for orthogal SR
                 '&& abs(hnl_dphi_hnvis0) > 1.0 '
                 '&& sv_prob > 0.05 ' 
                 )
    return selection

def SR_orth(channel): #A region orthogonal to the signal region dedicated for closure tests
    selection = (
                 'l0_pt > 25 && abs(l0_eta) < 2.4' 
                 '&& l0_id_m ==1'
                 '&& l0_reliso_rho_03 < 0.10 '
                 '&& abs(l0_dxy) < 0.05 && abs(l0_dz) < 0.2 '
                 '&& l1_Medium == 1 '
                 '&& l2_Medium == 1 '
                 '&& l1_pt > 5 && abs(l1_eta) < 2.4 '
                 '&& l2_pt > 5 && abs(l2_eta) < 2.4 '
                 # '&& hnl_2d_disp > 0.5'#removed for higher stat
                 # '&& abs(l1_dxy) > 0.01'
                 # '&& abs(l2_dxy) > 0.01'
                 '&& (l1_q != l2_q) '
                 # '&& nbj == 0 ' 
                 '&& nbj > 0 ' #activate for orthogonal SR
                 # '&& 50 < hnl_w_vis_m && hnl_w_vis_m < 85'
                 '&& 85 < hnl_w_vis_m' #activate for orthogal SR
                 # '&& abs(hnl_dphi_hnvis0) > 1.0 '
                 # '&& sv_prob > 0.05 ' 
                 )
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
                    '&& abs(l1_eta) < 2.4 '
                    # '&& abs(l1_dz) < 2 '#Martina uses 10
                    # '&& abs(l1_dxy) > 0.05 '
                    '&& l2_pt > 5 '
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
                    # '&& abs(l1_dxy) > 0.05 '
                    '&& l2_pt > 5 '
                    '&& abs(l2_eta) < 2.4 '
                    # '&& abs(l2_dz) < 2 '#Martina uses 10
                    # '&& abs(l2_dxy) > 0.05 '
                    '&& hnl_q_12 == 0 '
                    # '&& hnl_2d_disp > 0.05 ' # included by default, can be removed for more statistics
                    # '&& hnl_2d_disp > 0.1 ' # included by default, can be removed for more statistics
                    '&& nbj > 0 ' # measure DFs
                    # '&& hnl_w_vis_m > 20. '
                    # '&& (hnl_w_vis_m < 50. || hnl_w_vis_m > 80.) '
                    # '&& (hnl_dr_12 < 0.05)' # just for some debugging, not included by default
                    # '&& (hnl_dr_12 > 0.05)' # just for some debugging, not included by default
                    # '&& (hnl_dr_12 > 0.02)'
                    )
        return selection

def MR_SF(channel): 
    if channel is 'mmm':
        #based on Vinz's original measurement 
        # selection = (
                # 'abs(hnl_m_02 - 91.19) < 10 '
                # '&& hnl_dr_12 > 0.3 '
                # '&& abs(hnl_m_01 - 91.19) < 10 '
                # '&& hnl_dr_02 > 0.3 && hnl_dr_12 > 0.3 '
                # '&& l0_pt > 25 '
                # '&& abs(l0_eta) < 2.4 && abs(l0_dz) < 0.2 && abs(l0_dxy) < 0.05 && l0_reliso_rho_03 < 0.2 && l0_id_m == 1 '
                # '&& l1_pt > 10 && abs(l1_eta) < 2.4 && abs(l1_dz) < 0.2 && abs(l1_dxy) < 0.05 && l1_reliso_rho_03 < 0.2 && l1_id_m == 1 '
                # '&& l2_pt > 5 && abs(l2_eta) < 2.4 && abs(l2_dz) < 2 && abs(l2_dxy) > 0.05 '
                # '&& hnl_q_01 == 0 '
                # '&& ( (l2_reliso_rho_03 < 0.38 && abs(l2_eta) < 1.2) || (l2_reliso_rho_03 < 0.29 && abs(l2_eta) > 1.2 && abs(l2_eta) < 2.1) || (l2_reliso_rho_03 < 0.19 && abs(l2_eta) > 2.1) )'
                # )
        #based on the DY CR
        # selection = (
                    # 'l0_pt > 25 && abs(l0_eta) < 2.4 '
                    # '&& l1_pt > 15 && abs(l1_eta) < 2.4 '
                    # '&& (l0_q != l1_q) '
                    # '&& abs(l0_dxy) < 0.05 && abs(l0_dz) < 0.2 '
                    # '&& abs(l1_dxy) < 0.05 && abs(l1_dz) < 0.2 '
                    # '&& nbj == 0 '
                    # '&& l0_id_t ==1'
                    # '&& l1_id_t ==1'
                    # # '&& l1_eid_mva_iso_wp90'
                    # '&& l2_id_m ==1'
                    # '&& l0_reliso_rho_03 < 0.20 '
                    # '&& l1_reliso_rho_03 < 0.20 '
                    # # '&& l2_reliso_rho_03 < 0.20 '
                    # '&& abs(hnl_m_01 - 91.2) < 15 '
                    # # '&& abs(hnl_dphi_hnvis0) > 2.0 '
                    # # '&& abs(hnl_dphi_hnvis0) < 3.0 '
                    # )
        #based of the ML cut
        selection = (
                    '    l0_pt > 25 && abs(l0_eta) < 2.4 && abs(l0_dz) < 0.2 && abs(l0_dxy) < 0.05 && l0_reliso_rho_03 < 0.2 && l0_id_m == 1 '
                    ' && l1_pt > 10 && abs(l1_eta) < 2.4 && abs(l1_dz) < 0.2 && abs(l1_dxy) < 0.05 && l1_reliso_rho_03 < 0.2 && l1_id_m == 1 '
                    # '&& l2_pt > 5 && abs(l2_eta) < 2.4 && abs(l2_dz) < 2 && abs(l2_dxy) > 0.01'
                    ' && l2_pt > 5 && abs(l2_eta)'
                    ' && hnl_q_01 == 0'
                    ' && ( (l2_reliso_rho_03 < 0.38 && abs(l2_eta) < 1.2) || (l2_reliso_rho_03 < 0.29 && abs(l2_eta) > 1.2 && abs(l2_eta) < 2.1) || (l2_reliso_rho_03 < 0.19 && abs(l2_eta) > 2.1) )'
                    # ' && hnl_dr_02 > 0.1'
                    # ' && hnl_dr_12 > 0.1'
                    # ' && (abs(hnl_m_02 - 91) > 10 && hnl_q_02 == 0) '
                    # ' && (abs(hnl_m_12 - 91) > 10 && hnl_q_12 == 0) '
                    )
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
                        
        if selection_name == 'MR_SF':
            selection = MR_SF(channel)
        
        if selection_name == 'SR':
            selection = SR(channel)
                        
        if selection_name == 'SR_orth':
            selection = SR_orth(channel)
                        
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
            selection = ('!((l1_reliso_rho_03 < 0.2) && (l1_Medium == 1)) ' 
                        '&& ((l2_reliso_rho_03 < 0.2) && (l2_Medium == 1)) '
                        '&& (l1_reliso_rho_03 < 1.) '
                        )
                        
        if selection_name == 'T_LNT':
            selection = ('!((l2_reliso_rho_03 < 0.2) && (l2_Medium == 1)) ' 
                        '&& ((l1_reliso_rho_03 < 0.2) && (l1_Medium == 1)) '
                        '&& (l2_reliso_rho_03 < 1.) '
                        )
                        
        if selection_name == 'LNT_LNT_uncorrelated':
            selection = (
                        '(l1_reliso_rho_03 < 1.) ' 
                        '&& (l2_reliso_rho_03 < 1.) '
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
                        '(l1_reliso_rho_03 < 1.) '
                        '&& ((l2_reliso_rho_03 < 0.2) && (l2_Medium == 1)) '
                        )
                        
        if selection_name == 'T_L':
            selection = ( 
                        '(l2_reliso_rho_03 < 1.) '
                        '&& ((l1_reliso_rho_03 < 0.2) && (l1_Medium == 1)) '
                        )
                        
        if selection_name == 'L_L_uncorrelated':
            selection = (
                        '(l1_reliso_rho_03 < 1.) ' 
                        '&& (l2_reliso_rho_03 < 1.) '
                        '&& !((abs(l1_jet_pt - l2_jet_pt) < 1) && ((hnl_dr_12 < 0.3)))'
                        )
                        
        if selection_name == 'L_L_correlated':
            selection = (
                        '(hnl_iso04_rel_rhoArea < 2) ' 
                        '&& ((abs(l1_jet_pt - l2_jet_pt) < 1) && ((hnl_dr_12 < 0.3)))'
                        )
    
        if selection_name == 'datacut':
            selection = defineDataCut('mu')
 
    return selection


# #DY_prompt
# class Region(object):
    # def __init__(self,name,channel,CR):
        # self.name                       = name
        # self.channel                    = channel
        # self.CR                         = CR
        # self.baseline = ('l0_pt>25 && abs(l0_eta)<2.4 && (l0_q != l1_q) '
                     # '&& l1_pt > 15 && abs(l1_eta) < 2.4 '
                     # '&& abs(l0_dxy) < 0.05 && abs(l0_dz) < 0.2 '
                     # '&& abs(l1_dxy) < 0.05 && abs(l1_dz) < 0.2 '
                     # '&& nbj == 0 '
                     # '&& l0_id_t ==1'
                     # '&& l1_id_t ==1'
                     # # '&& l1_eid_mva_iso_wp90'
                     # '&& l2_id_m ==1'
                     # '&& l0_reliso_rho_03 < 0.20 '
                     # '&& l1_reliso_rho_03 < 0.20 '
                     # '&& l2_reliso_rho_03 < 0.20 '
                     # '&& abs(hnl_m_01 - 91.2) < 15 '
                     # '&& abs(hnl_dphi_hnvis0) > 2.0 '
                     # '&& abs(hnl_dphi_hnvis0) < 3.0 '
                     # )
        # self.data                       = self.baseline
        # self.signal                     = self.baseline
        # self.MC                         = self.baseline 
        # self.SF                         = self.baseline 
        # # self.MC_DY                      = self.data + '&& (!(l1_gen_match_pdgid == 22 && l1_gen_match_isPromptFinalState == 1) && !(l2_gen_match_pdgid == 22 && l2_gen_match_isPromptFinalState == 1))'
        # # self.MC_SingleConversions       = self.data + '&& ((l1_gen_match_pdgid == 22 && l1_gen_match_isPromptFinalState == 1) || (l2_gen_match_pdgid == 22 && l2_gen_match_isPromptFinalState == 1))'
        # # self.MC_DoubleConversions       = self.data + '&& ((l1_gen_match_pdgid == 22 && l1_gen_match_isPromptFinalState == 1) && (l2_gen_match_pdgid == 22 && l2_gen_match_isPromptFinalState == 1))'
        # self.MC_DY                      = self.data + '&& (!(l1_gen_match_pdgid == 22) && !(l2_gen_match_pdgid == 22))'
        # self.MC_SingleConversions       = self.data + '&& ((l1_gen_match_pdgid == 22) || (l2_gen_match_pdgid == 22))'
        # self.MC_DoubleConversions       = self.data + '&& ((l1_gen_match_pdgid == 22) && (l2_gen_match_pdgid == 22))'

#------------------------------------
# #TTbar_prompt
# class Region(object):
    # def __init__(self,name,channel,CR):
        # self.name                       = name
        # self.channel                    = channel
        # self.CR                         = CR
        # self.baseline = (
                     # 'l0_pt > 35 && abs(l0_eta) < 2.4'
                     # '&& l1_pt > 10 && abs(l1_eta) < 2.5'
                     # '&& l2_pt > 10 && abs(l2_eta) < 2.4'
                     # '&& nbj > 0 '
                     # '&& hnl_m_01 > 15'
                     # '&& hnl_m_02 > 15'
                     # '&& hnl_m_12 > 15'
                     # # '&& abs(hnl_w_vis_m - 91.2) > 15'
                     # '&& abs(l0_dxy) < 0.05 && abs(l0_dz) < 0.2 '
                     # '&& abs(l1_dxy) < 0.05 && abs(l1_dz) < 0.2 '
                     # # '&& l0_reliso_rho_03 < 0.12 '
                     # # '&& l1_reliso_rho_03 < 0.12 '
                     # # '&& l2_reliso_rho_03 < 0.12 '
                     # # '&& ((l0_q != l1_q && hnl_m_01 > 12) || (l0_q == l1_q))'
                     # # '&& ((l0_q != l2_q && hnl_m_02 > 12) || (l0_q == l1_q))'
                     # # '&& ((l1_q != l2_q && hnl_m_12 > 12) || (l1_q == l2_q))'
                     # )
        # self.data                       = self.baseline
        # self.MC                         = self.baseline 
        # self.SF                         = self.baseline 



#################################################################3
#Measurement Region DFR mmm
class Region(object):
    def __init__(self,name,channel,CR):
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
                                          # getSelection(channel,'T_LNT'),\
                                          getSelection(channel,'T_T'),\
                                          ]) + ')' 
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

        self.MC_DY                      = self.data + '&& (!(l1_gen_match_pdgid == 22) && !(l2_gen_match_pdgid == 22))'
        self.MC_SingleConversions       = self.data + '&& ((l1_gen_match_pdgid == 22 && l2_gen_match_pdgid != 22) || (l2_gen_match_pdgid == 22 && l1_gen_match_pdgid != 22))'
        self.MC_DoubleConversions       = self.data + '&& ((l1_gen_match_pdgid == 22) && (l2_gen_match_pdgid == 22))'

