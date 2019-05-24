from pdb import set_trace
def defineDataCut(promptLeptonType):
    goodVertices                 = '  &  Flag_goodVertices'    
    globalSuperTightHalo2016     = '  &  Flag_globalSuperTightHalo2016Filter'    
    HBHENoise                    = '  &  Flag_HBHENoiseFilter'                   
    HBHENoiseIso                 = '  &  Flag_HBHENoiseIsoFilter'                
    EcalDeadCellTriggerPrimitive = '  &  Flag_EcalDeadCellTriggerPrimitiveFilter'
    BadPFMuon                    = '  &  Flag_BadPFMuonFilter'                   
    BadChargedCandidate          = '  &  Flag_BadChargedCandidateFilter'         
    eeBadSc                      = '  &  Flag_eeBadScFilter'                     
    ecalBadCalib                 = '  &  Flag_ecalBadCalibFilter'                

    if promptLeptonType == "ele": 
        datacut   = goodVertices + globalSuperTightHalo2016 + HBHENoise + HBHENoiseIso + EcalDeadCellTriggerPrimitive + BadPFMuon + BadChargedCandidate + eeBadSc + ecalBadCalib 
    if promptLeptonType == "mu": 
        datacut   = 'l0_id_t' #Placeholder

    return datacut

def Z_veto():
    Z_veto_01       = '( (l0_q + l1_q == 0) & (abs(hnl_m_01 - 91.2) > 15) )  &  (l0_q + l2_q != 0)  &  (l1_q + l2_q != 0)'
    Z_veto_02       = '(l0_q + l1_q != 0)  &  ( (l0_q + l2_q == 0) & (abs(hnl_m_02 - 91.2) > 15) )  &  (l1_q + l2_q != 0)'
    Z_veto_12       = '(l0_q + l1_q != 0)  &  (l0_q + l2_q != 0)  &  ( (l1_q + l2_q == 0) & (abs(hnl_m_12 - 91.2) > 15) )' 

    Z_veto_01_02    = '( (l0_q + l1_q == 0) & (abs(hnl_m_01 - 91.2) > 15) )  &  ( (l0_q + l2_q == 0) & (abs(hnl_m_02 - 91.2) > 15) )  &  (l1_q + l2_q != 0)'  
    Z_veto_01_12    = '( (l0_q + l1_q == 0) & (abs(hnl_m_01 - 91.2) > 15) )  &  (l0_q + l2_q != 0)  &  ( (l1_q + l2_q == 0) & (abs(hnl_m_12 - 91.2) > 15) )'  
    Z_veto_02_12    = '(l0_q + l1_q != 0)  &  ( (l0_q + l2_q == 0) & (abs(hnl_m_02 - 91.2) > 15) )  &  ( (l1_q + l2_q == 0) & (abs(hnl_m_12 - 91.2) > 15) )'  

    Z_veto_01_02_12 = '( (l0_q + l1_q == 0) & (abs(hnl_m_01 - 91.2) > 15) )  &  ( (l0_q + l2_q == 0) & (abs(hnl_m_02 - 91.2) > 15) )  &  ( (l1_q + l2_q == 0) & (abs(hnl_m_12 - 91.2) > 15) )'

    single_Z_veto = '(  ' + Z_veto_01 + '   |   ' + Z_veto_02 + '   |   ' + Z_veto_12 + '  )'
    double_Z_veto = '(  ' + Z_veto_01_02 + '   |   ' + Z_veto_01_12 + '   |   ' + Z_veto_02_12 + '  )'

    Z_veto = ' & (   ' + single_Z_veto + '    |    ' + double_Z_veto + '    |    ' + Z_veto_01_02_12 + '   )' 
    return Z_veto

def CR_ttbar():
    selection = ('abs(hnl_m_12 - 91.18) > 15 ' #suppress Z 
                '& abs(hnl_w_vis_m - 91.18) > 15 ' #suppress conversions 
                '& hnl_m_12 > 12 ' #suppress conversions
                '& nbj >=1 '
                )
    # selection = selection + Z_veto()
    return selection

def SR():
    selection = ('hnl_dr_12 < 1 ' 
                '& nbj == 0 '
                '& hnl_w_vis_m < 80 '
                # '& hnl_w_vis_m > 50 '
                # '& hnl_dr_01 > 1 '
                # '& hnl_dr_02 > 1 '
                )
    selection = selection + Z_veto()
    return selection

def DY():
    selection = ('abs(hnl_m_12 - 91.18) < 15'
                '& abs(hnl_w_vis_m - 91.18) > 15 '
                '& nbj == 0 ' 
                '& pfmet_pt < 30 '
                '& hnl_mt_0 < 30 '
                )
    return selection


def baseline(channel): 
    if channel == 'mmm':
            selection = (
                        'l0_pt > 25'
                        '& abs(l0_eta) < 2.4'
                        '& abs(l0_dz) < 0.2'
                        '& abs(l0_dxy) < 0.05'
                        '& l0_reliso_rho_03 < 0.2'
                        '& l0_id_m == 1'
                        '& l1_pt > 5'
                        '& abs(l1_eta) < 2.4'
                        '& abs(l1_dz) < 2'
                        # '& abs(l1_dxy) > 0.05'
                        '& l2_pt > 5'
                        '& abs(l2_eta) < 2.4'
                        '& abs(l2_dz) < 2'
                        # '& abs(l2_dxy) > 0.05'
                        '& hnl_q_12 == 0'
                        '& hnl_2d_disp > 0.05'
                        # '& hnl_2d_disp > 0.1'
                        # '& nbj > 0' # measure DFs
                        '& hnl_w_vis_m > 20.'
                        '& (hnl_w_vis_m < 50. || hnl_w_vis_m > 80.)'
                        )
            
    return selection



def getSelection(channel, selection_name):
    if channel == 'mmm':
        #testing the old version
        if selection_name == 'baseline':
            selection = baseline(channel)
            
            # selection = selection + Z_veto() 

        if selection_name == 'CR_ttbar':
            selection = CR_ttbar()

        if selection_name == 'SR':
            selection = SR()
                        
        if selection_name == 'CR_DY':
            selection = DY()
                        
        if selection_name == 'TT':
            selection = ('('
                        'l1_reliso_rho_03 < 0.2 ' 
                        '& l2_reliso_rho_03 < 0.2 '
                        '& l1_Medium == 1 '
                        '& l2_Medium == 1 '
                        ')'
                        )
                        
        if selection_name == 'LT':
            selection = ('l1_reliso_rho_03 > 0.2 ' 
                        '& l2_reliso_rho_03 < 0.2 '
                        )
                        
        if selection_name == 'TL':
            selection = ('l1_reliso_rho_03 < 0.2 ' 
                        '& l2_reliso_rho_03 > 0.2 '
                        )
                        
        if selection_name == 'LL_uncorrelated':
            selection = ('l1_reliso_rho_03 < 1. ' 
                        '& l2_reliso_rho_03 < 1. '
                        )
                        
        if selection_name == 'LL_correlated':
            selection = ('abs(l1_jet_pt - l2_jet_pt) < 1 '
                        '& hnl_dr_12 < 0.3 '
                        '& hnl_iso04_rel_rhoArea < 2 ' # tune it to enrich the statistics
                        )
    
        if selection_name == 'datacut':
            selection = defineDataCut('mu')


 
    return selection

# class Region(object):
    # def __init__(self,name,channel,CR):
        # self.name                       = name
        # self.channel                    = channel
        # self.CR                         = CR
        # self.data                       = '(' + ' & '.join([getSelection(channel,'baseline'),getSelection(channel,CR),getSelection(channel,'TT'),getSelection(channel,'datacut')]) + ')'
        # self.MC                         = '(' + ' & '.join([getSelection(channel,'baseline'),getSelection(channel,CR),getSelection(channel,'TT')]) + ')'
        # self.signal                     = '(' + ' & '.join([getSelection(channel,'baseline'),getSelection(channel,CR),getSelection(channel,'TT')]) + ')'
        # self.N_TL                       = '(' + ' & '.join([getSelection(channel,'baseline'),getSelection(channel,CR),getSelection(channel,'TL')]) + ')'
        # self.N_LT                       = '(' + ' & '.join([getSelection(channel,'baseline'),getSelection(channel,CR),getSelection(channel,'LT')]) + ')'
        # self.N_LL_uncorrelated          = '(' + ' & '.join([getSelection(channel,'baseline'),getSelection(channel,CR),getSelection(channel,'LL_uncorrelated')]) + ')'
        # self.N_LL_correlated            = '(' + ' & '.join([getSelection(channel,'baseline'),getSelection(channel,CR),getSelection(channel,'LL_correlated')]) + ')'
        # self.SF_TL                      = self.N_TL + ' * (weight_fr/(1-weight_fr))'  
        # self.SF_LT                      = self.N_LT + ' * (weight_fr/(1-weight_fr))'  
        # self.SF_LL_uncorrelated         = self.N_LL_uncorrelated + ' * (-1) * ((weight_fr/(1-weight_fr))*(weight_fr/(1-weight_fr)))'  
        # self.SF                         = self.SF_TL + ' + ' + self.SF_LT + ' + ' + self.SF_LL_uncorrelated
        # self.DF                         = self.N_LL_correlated + ' * (weight_fr/(1-weight_fr))'

# #DY_prompt
# class Region(object):
    # def __init__(self,name,channel,CR):
        # self.name                       = name
        # self.channel                    = channel
        # self.CR                         = CR
        # self.baseline = ('l0_pt>25 & abs(l0_eta)<2.4 & (l0_q != l1_q) '
                     # '& l1_pt > 15 & abs(l1_eta) < 2.4 '
                     # '& abs(l0_dxy) < 0.05 & abs(l0_dz) < 0.2 '
                     # '& abs(l1_dxy) < 0.05 & abs(l1_dz) < 0.2 '
                     # '& nbj == 0 '
                     # '& l0_id_t ==1'
                     # '& l1_id_t ==1'
                     # # '& l1_eid_mva_iso_wp90'
                     # '& l2_id_m ==1'
                     # '& l0_reliso_rho_03 < 0.20 '
                     # '& l1_reliso_rho_03 < 0.20 '
                     # '& l2_reliso_rho_03 < 0.20 '
                     # '& abs(hnl_m_01 - 91.2) < 15 '
                     # '& abs(hnl_dphi_hnvis0) > 2.0 '
                     # '& abs(hnl_dphi_hnvis0) < 3.0 '
                     # )
        # self.data                       = self.baseline
        # self.signal                     = self.baseline
        # self.MC                         = self.baseline 
        # self.SF                         = self.baseline 
        # # self.MC_DY                      = self.data + '& (!(l1_gen_match_pdgid == 22 & l1_gen_match_isPromptFinalState == 1) & !(l2_gen_match_pdgid == 22 & l2_gen_match_isPromptFinalState == 1))'
        # # self.MC_SingleConversions       = self.data + '& ((l1_gen_match_pdgid == 22 & l1_gen_match_isPromptFinalState == 1) | (l2_gen_match_pdgid == 22 & l2_gen_match_isPromptFinalState == 1))'
        # # self.MC_DoubleConversions       = self.data + '& ((l1_gen_match_pdgid == 22 & l1_gen_match_isPromptFinalState == 1) & (l2_gen_match_pdgid == 22 & l2_gen_match_isPromptFinalState == 1))'
        # self.MC_DY                      = self.data + '& (!(l1_gen_match_pdgid == 22) & !(l2_gen_match_pdgid == 22))'
        # self.MC_SingleConversions       = self.data + '& ((l1_gen_match_pdgid == 22) | (l2_gen_match_pdgid == 22))'
        # self.MC_DoubleConversions       = self.data + '& ((l1_gen_match_pdgid == 22) & (l2_gen_match_pdgid == 22))'

# #Conversion_prompt
# class Region(object):
    # def __init__(self,name,channel,CR):
        # self.name                       = name
        # self.channel                    = channel
        # self.CR                         = CR
        # self.baseline = ('l0_pt>25 & abs(l0_eta)<2.4 & (l0_q != l1_q) '
                     # # '& l1_pt > 15 & abs(l1_eta) < 2.4 '
                     # # '& abs(l0_dxy) < 0.05 & abs(l0_dz) < 0.2 '
                     # # '& abs(l1_dxy) < 0.05 & abs(l1_dz) < 0.2 '
                     # '& nbj == 0 '
                     # # '& l0_id_t ==1'
                     # # '& l1_id_t ==1'
                     # # '& l1_eid_mva_iso_wp90'
                     # # '& l2_id_m ==1'
                     # '& l0_reliso_rho_03 < 0.20 '
                     # '& l1_reliso_rho_03 < 0.20 '
                     # '& l2_reliso_rho_03 < 0.20 '
                     # '& hnl_w_vis_m > 50'
                     # # '& abs(hnl_m_01 - 91.2) < 15 '
                     # # '& abs(hnl_dphi_hnvis0) > 2.0 '
                     # # '& abs(hnl_dphi_hnvis0) < 3.0 '
                     # # '& (hnl_m_01 > 60 & hnl_m_01 < 80)'
                     # # '& (hnl_m_02 > 35 & hnl_m_02 < 65)'
                     # # '& hnl_m_12 < 0.8'
                     # # '& (hnl_w_vis_m > 80 & hnl_w_vis_m < 100)'
                     # # '& hnl_m_12 < 65'
                     # # '& l0_pt < 45'
                     # # '& (l1_pt > 15 & l1_pt < 50 & abs(l1_eta) < 2.4)' # get rid of WJets
                     # # '& (l2_pt > 10 & l2_pt < 25 & abs(l2_eta) < 2.4)'
                     # # '& pt_cone > 20 '
                     # )
        # self.data                       = self.baseline
        # self.signal                     = self.baseline
        # self.MC                         = self.baseline 
        # self.SF                         = self.baseline 
        # self.MC_DY                      = self.data + '& (!(l1_gen_match_pdgid == 22 & l1_gen_match_isPromptFinalState == 1) & !(l2_gen_match_pdgid == 22 & l2_gen_match_isPromptFinalState == 1))'
        # self.MC_SingleConversions       = self.data + '& ((l1_gen_match_pdgid == 22 & l1_gen_match_isPromptFinalState == 1) | (l2_gen_match_pdgid == 22 & l2_gen_match_isPromptFinalState == 1))'
        # self.MC_DoubleConversions       = self.data + '& ((l1_gen_match_pdgid == 22 & l1_gen_match_isPromptFinalState == 1) & (l2_gen_match_pdgid == 22 & l2_gen_match_isPromptFinalState == 1))'
        # # self.MC_DY                      = self.data + '& (!(l1_gen_match_pdgid == 22) & !(l2_gen_match_pdgid == 22))'
        # # self.MC_SingleConversions       = self.data + '& ((l1_gen_match_pdgid == 22) | (l2_gen_match_pdgid == 22))'
        # # self.MC_DoubleConversions       = self.data + '& ((l1_gen_match_pdgid == 22) & (l2_gen_match_pdgid == 22))'
        # # self.MC_DY                      = self.data + '& (!(l1_gen_match_isPrompt == 1) & !(l2_gen_match_isPrompt == 1))'
        # # self.MC_SingleConversions       = self.data + '& ((l1_gen_match_isPrompt == 1) | (l2_gen_match_isPrompt == 1))'
        # # self.MC_DoubleConversions       = self.data + '& ((l1_gen_match_isPrompt == 1) & (l2_gen_match_isPrompt == 1))'
        # # self.MC_DY                      = self.data + '& (!(l1_gen_match_pdgid != 22 & l1_gen_match_isPrompt == 1) & !(l2_gen_match_pdgid != 22 & l2_gen_match_isPrompt == 1))'
        # # self.MC_SingleConversions       = self.data + '& ((l1_gen_match_pdgid != 22 & l1_gen_match_isPrompt == 1) | (l2_gen_match_pdgid != 22 & l2_gen_match_isPrompt == 1))'
        # # self.MC_DoubleConversions       = self.data + '& ((l1_gen_match_isPrompt == 1) & (l2_gen_match_isPrompt == 1))'

#------------------------------------
# #TTbar_prompt
# class Region(object):
    # def __init__(self,name,channel,CR):
        # self.name                       = name
        # self.channel                    = channel
        # self.CR                         = CR
        # self.baseline = (
                     # 'l0_pt > 35 & abs(l0_eta) < 2.4'
                     # '& l1_pt > 10 & abs(l1_eta) < 2.5'
                     # '& l2_pt > 10 & abs(l2_eta) < 2.4'
                     # '& nbj > 0 '
                     # '& hnl_m_01 > 15'
                     # '& hnl_m_02 > 15'
                     # '& hnl_m_12 > 15'
                     # # '& abs(hnl_w_vis_m - 91.2) > 15'
                     # '& abs(l0_dxy) < 0.05 & abs(l0_dz) < 0.2 '
                     # '& abs(l1_dxy) < 0.05 & abs(l1_dz) < 0.2 '
                     # # '& l0_reliso_rho_03 < 0.12 '
                     # # '& l1_reliso_rho_03 < 0.12 '
                     # # '& l2_reliso_rho_03 < 0.12 '
                     # # '& ((l0_q != l1_q & hnl_m_01 > 12) | (l0_q == l1_q))'
                     # # '& ((l0_q != l2_q & hnl_m_02 > 12) | (l0_q == l1_q))'
                     # # '& ((l1_q != l2_q & hnl_m_12 > 12) | (l1_q == l2_q))'
                     # )
        # self.data                       = self.baseline
        # self.MC                         = self.baseline 
        # self.SF                         = self.baseline 

# #------------------------------------

#SR_mmm
class Region(object):
    def __init__(self,name,channel,CR):
        self.name                       = name
        self.channel                    = channel
        self.CR                         = CR
        self.baseline = (
                     'l0_pt > 25 & abs(l0_eta) < 2.4' 
                     # '& l0_id_t ==1'
                     '& l0_id_m ==1'
                     '& l0_reliso_rho_03 < 0.10 '
                     '& abs(l0_dxy) < 0.05 & abs(l0_dz) < 0.2 '
                     '& l1_Medium == 1 '
                     '& l2_Medium == 1 '
                     # '& l1_MediumWithIso ==1'
                     '& l1_pt > 5 & abs(l1_eta) < 2.4 '
                     '& l2_pt > 5 & abs(l2_eta) < 2.4 '
                     # '& l1_reliso_rho_03 < 0.20 '
                     # '& l2_reliso_rho_03 < 0.20 '
                     '& abs(l1_dxy) > 0.01'
                     '& abs(l2_dxy) > 0.01'
                     '& (l1_q != l2_q) '
                     '& hnl_dr_12 < 1.0 '
                     # '& nbj == 0 ' 
                     '& nbj > 0 ' #activate for orthogonal SR
                     '& 50 < hnl_w_vis_m'
                     '& hnl_w_vis_m < 85'
                     # '& 85 < hnl_w_vis_m' #activate for orthogal SR
                     '& abs(hnl_dphi_hnvis0) > 1.0 '
                     )
        self.baseline                   = '(' + ' & '\
                                          .join([\
                                          self.baseline,\
                                          getSelection(channel,'LL_correlated'),\
                                          ]) + ')' 
        self.data                       = '(' + ' & '\
                                          .join([\
                                          self.baseline,\
                                          getSelection(channel,'TT'),\
                                          ]) + ')' 
        # self.data                       = self.baseline
        self.MC                         = self.data 
        self.SF                         = self.baseline 
        self.DF                         = self.baseline 
        self.MC_DY                      = self.data + '& (!(l1_gen_match_pdgid == 22) & !(l2_gen_match_pdgid == 22))'
        self.MC_SingleConversions       = self.data + '& ((l1_gen_match_pdgid == 22) | (l2_gen_match_pdgid == 22))'
        self.MC_DoubleConversions       = self.data + '& ((l1_gen_match_pdgid == 22) & (l2_gen_match_pdgid == 22))'



# #################################################################3
# #Measurement Region DFR mmm
# class Region(object):
    # def __init__(self,name,channel,CR):
        # self.name                       = name
        # self.channel                    = channel
        # self.CR                         = CR
        # self.baseline                   = '(' + ' & '\
                                          # .join([\
                                          # getSelection(channel,'baseline'),\
                                          # getSelection(channel,'LL_correlated'),\
                                          # ]) + ')' 
        # self.data                       = '(' + ' & '\
                                          # .join([\
                                          # self.baseline,\
                                          # getSelection(channel,'TT'),\
                                          # ]) + ')' 
        # # self.data                       = self.baseline
        # self.MC                         = self.data 
        # self.SF                         = self.baseline 
        # self.DF                         = self.baseline 
        # self.MC_DY                      = self.data + '& (!(l1_gen_match_pdgid == 22) & !(l2_gen_match_pdgid == 22))'
        # self.MC_SingleConversions       = self.data + '& ((l1_gen_match_pdgid == 22) | (l2_gen_match_pdgid == 22))'
        # self.MC_DoubleConversions       = self.data + '& ((l1_gen_match_pdgid == 22) & (l2_gen_match_pdgid == 22))'

