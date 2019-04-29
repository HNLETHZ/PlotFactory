import ROOT
import plotfactory as pf
import numpy as np
import sys
from pdb import set_trace

pf.setpfstyle()

t = ROOT.TChain('tree')
t.Add('/work/dezhu/5_Miscellaneous/20190320_FRStudies/TTJets/HNLTreeProducer/tree.root')

# bins_ptCone = np.arange(0.,75.,5.)
# bins_ptCone = np.array([0.,5.,10.,15.,20.,25.,35.,70])
bins_ptCone = np.array([5.,15.,25.,35.,70.])
bins_eta = np.array([0.,1.2,2.1,2.4])

def baseline(channel):
    if channel == 'mmm':
        selection = ('(l0_id_m '
            '& l0_pt > 25 '
            '& l0_Medium '
            '& l0_eta < 2.4 '
            '& l0_reliso_rho_03 < 1 '
            '& abs(l0_dz) < 0.1 '
            '& abs(l0_dxy) < 0.05 '
            '& abs(hnl_3d_disp_sig) < 4 '
            '& l0_is_oot == 0 '
            '& l1_Medium '
            '& l2_Medium '
            '& l1_pt > 5 ' #electron 10 GeV, muon 5 GeV
            '& l2_pt > 5 '
            '& l1_eta < 2.4 '
            '& l2_eta < 2.4 '
            '& l1_reliso_rho_03 < 1 '
            '& l2_reliso_rho_03 < 1 '
            # '& abs(l1_dxy) > 0.01 '
            # '& abs(l2_dxy) > 0.01 '
            '& l1_is_oot == 0  '
            '& l2_is_oot == 0  '
            '& l1_q != l2_q ' #opposite charge for the dilepton
            ')'
            )
    return selection

def selection_IsPrompt(lepton):
    selection = '(l%s_gen_match_fromHardProcessFinalState | l%s_gen_match_isPromptFinalState | l%s_gen_match_isDirectPromptTauDecayProductFinalState | l%s_gen_match_isDirectHardProcessTauDecayProductFinalState)'%(lepton,lepton,lepton,lepton)
    return selection

def selection_IsNonPrompt(lepton):
    selection = '(l%s_gen_match_fromHardProcessFinalState == 0 & l%s_gen_match_isPromptFinalState == 0 & l%s_gen_match_isDirectPromptTauDecayProductFinalState == 0 & l%s_gen_match_isDirectHardProcessTauDecayProductFinalState == 0 & abs(l%s_dxy) > 0.01)'%(lepton,lepton,lepton,lepton,lepton)
    return selection

def selection_IsLoose(lepton):
    if lepton == '0':
        sel = '(' + ' & '.join([baseline('mmm'),selection_IsNonPrompt('0'),selection_IsPrompt('1'),selection_IsPrompt('2')]) + ')'
    if lepton == '2':
        sel = '(' + ' & '.join([baseline('mmm'),selection_IsPrompt('0'),selection_IsPrompt('1'),selection_IsNonPrompt('2')]) + ')'
    if lepton == '1':
        sel = '(' + ' & '.join([baseline('mmm'),selection_IsPrompt('0'),selection_IsNonPrompt('1'),selection_IsPrompt('2')]) + ')'
    selection = '(' + sel + ' & l%s_reliso_rho_03 < 1. )'%(lepton) 
    return selection

def selection_IsTight(lepton):
    selection = '(' + selection_IsLoose(lepton) + ' & l%s_reliso_rho_03 < 0.1 )'%(lepton) 
    return selection
    

def ptCone(lepton):
    PTCONE = '((l%s_pt*(l%s_reliso_rho_03<0.1))+((l%s_reliso_rho_03>=0.1)*(l%s_pt*(1. + l%s_reliso_rho_03 - 0.1))))'%(lepton,lepton,lepton,lepton,lepton)
    return PTCONE

def drawCommand(lepton,histo):
    command = 'l%s_eta:'%(lepton) + ptCone(lepton) + '>>%s'%(histo) 
    return command


def measureFR(lepton):
    # c_TTL = ROOT.TCanvas('c_TTL_l%s'%(lepton),'c_TTL_l%s'%(lepton))


    h_loose = ROOT.TH2F('h_loose','',len(bins_ptCone)-1,bins_ptCone,len(bins_eta)-1,bins_eta)
    h_tight = ROOT.TH2F('h_tight','',len(bins_ptCone)-1,bins_ptCone,len(bins_eta)-1,bins_eta)
    h_TTL = ROOT.TH2F('h_TTL','',len(bins_ptCone)-1,bins_ptCone,len(bins_eta)-1,bins_eta)

    h_loose.SetTitle('loose;ptCone [GeV];|#eta|;Loose')
    h_tight.SetTitle('loose;ptCone [GeV];|#eta|;Tight')

    t.Draw(drawCommand(lepton,'h_loose'),selection_IsLoose(lepton))
    t.Draw(drawCommand(lepton,'h_tight'),selection_IsTight(lepton))


    h_tight.Draw('colz')
    h_loose.Draw('colz')

    # c_TTL.cd()
    h_TTL = h_tight.Clone()
    h_TTL.Divide(h_loose)
    h_TTL.SetTitle('loose;ptCone [GeV];|#eta|;TTL ratio (aka SFR muon)')
    h_TTL.Draw('colz')
    # c_TTL.Update()
    return h_loose,h_tight,h_TTL

def measureCombinedFR(lepton1,lepton2):

    c_TTL = ROOT.TCanvas('c_TTL_l%sl%s'%(lepton1,lepton2),'c_TTL_l%sl%s'%(lepton1,lepton2))

    h_loose_l1,h_tight_l1,h_TTL_l1 = measureFR('1')
    h_loose_l2,h_tight_l2,h_TTL_l2 = measureFR('2')

    h_loose_l1.Add(h_loose_l2)
    h_tight_l1.Add(h_loose_l2)

    h_TTL = ROOT.TH2F('h_TTL','',len(bins_ptCone)-1,bins_ptCone,len(bins_eta)-1,bins_eta)
    h_TTL = h_tight_l1.Clone()
    h_TTL.Divide(h_loose_l1)
    h_TTL.SetTitle('loose;ptCone [GeV];|#eta|;TTL ratio (aka SFR muon)')
    h_TTL.Draw('colz')
    c_TTL.Update()
    

# measureCombinedFR('1','2')
lepton1 = '1'
lepton2 = '2'
c_TTL_l1 = ROOT.TCanvas('c_TTL_l%s'%(lepton1),'c_TTL_l%s'%(lepton1))
c_TTL_l2 = ROOT.TCanvas('c_TTL_l%s'%(lepton2),'c_TTL_l%s'%(lepton2))
c_tight_l2 = ROOT.TCanvas('c_tight%s'%(lepton2),'c_tight%s'%(lepton2))
c_loose_l2 = ROOT.TCanvas('c_loose%s'%(lepton2),'c_loose%s'%(lepton2))
h_loose_l1,h_tight_l1,h_TTL_l1 = measureFR('1')
h_loose_l2,h_tight_l2,h_TTL_l2 = measureFR('2')

# c_TTL_l1.cd()
# h_TTL_l1.Draw('colz')
# c_TTL_l1.Update()

c_TTL_l2.cd()
h_TTL_l2.Draw('colz')
c_TTL_l2.Update()

c_tight_l2.cd()
h_tight_l2.Draw('colz')
c_tight_l2.Update()

c_loose_l2.cd()
h_loose_l2.Draw('colz')
c_loose_l2.Update()


# #just for testing

# c_loose = ROOT.TCanvas('c_loose','c_loose')
# c_tight = ROOT.TCanvas('c_tight','c_tight')
# c_TTL = ROOT.TCanvas('c_TTL','c_TTL')

# # bins_ptCone = np.arange(0.,75.,5.)
# bins_ptCone = np.array([0.,5.,10.,15.,20.,25.,35.,70])
# bins_eta = np.array([0.,1.2,2.1,2.4])

# h_loose = ROOT.TH2F('h_loose','',len(bins_ptCone)-1,bins_ptCone,len(bins_eta)-1,bins_eta)
# h_tight = ROOT.TH2F('h_tight','',len(bins_ptCone)-1,bins_ptCone,len(bins_eta)-1,bins_eta)
# h_TTL = ROOT.TH2F('h_TTL','',len(bins_ptCone)-1,bins_ptCone,len(bins_eta)-1,bins_eta)

# h_loose.SetTitle('loose;ptCone [GeV];|#eta|;Loose')
# h_tight.SetTitle('loose;ptCone [GeV];|#eta|;Tight')

# t.Draw(drawCommand('2','h_loose'),selection_IsLoose('2'))
# t.Draw(drawCommand('2','h_tight'),selection_IsTight('2'))


# c_tight.cd()
# h_tight.Draw('colz')
# c_tight.Update()


# c_loose.cd()
# h_loose.Draw('colz')
# c_loose.Update()

# c_TTL.cd()
# h_TTL = h_tight.Clone()
# h_TTL.Divide(h_loose)
# h_TTL  .SetTitle('loose;ptCone [GeV];|#eta|;TTL ratio (aka SFR muon)')
# h_TTL.Draw('colz')
# c_TTL.Update()

