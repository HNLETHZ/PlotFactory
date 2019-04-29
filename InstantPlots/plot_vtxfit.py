import ROOT
import plotfactory as pf
import numpy as np
import sys

pf.setpfstyle()
output_dir = '/eos/user/d/dezhu/HNL/plots/projects/20181107_VtxFit/'

######################################### 
# Make Chain from selection of samples
#########################################

#kinematic vertex fitter
tt_kinpf = ROOT.TChain('tree')
tt_kinpf.Add('/afs/cern.ch/work/d/dezhu/HNL/CMSSW_9_4_6_patch1/src/CMGTools/HNL/0_result/2_ntuples/HN3L_M_2_V_0p022360679775_e_massiveAndCKM_LO_2/HNLTreeProducer/tree.root')

#kalman vertex fitter
tt_kalpf = ROOT.TChain('tree')
tt_kalpf.Add('/afs/cern.ch/work/d/dezhu/HNL/CMSSW_9_4_6_patch1/src/CMGTools/HNL/0_result/2_ntuples/HN3L_M_2_V_0p022360679775_e_massiveAndCKM_LO_3/HNLTreeProducer/tree.root')

#kinematic vertex fitter
tt_kinsa = ROOT.TChain('tree')
tt_kinsa.Add('/afs/cern.ch/work/d/dezhu/HNL/CMSSW_9_4_6_patch1/src/CMGTools/HNL/0_result/2_ntuples/HN3L_M_2_V_0p022360679775_e_massiveAndCKM_LO_4/HNLTreeProducer/tree.root')

#kalman vertex fitter
tt_kalsa = ROOT.TChain('tree')
tt_kalsa.Add('/afs/cern.ch/work/d/dezhu/HNL/CMSSW_9_4_6_patch1/src/CMGTools/HNL/0_result/2_ntuples/HN3L_M_2_V_0p022360679775_e_massiveAndCKM_LO_5/HNLTreeProducer/tree.root')


nentries = tt_kinpf.GetEntries()
print('number of events: %d'%(nentries))

######################################### 
# Make Plot
#########################################

# kinematic fitter
c_kinpf = ROOT.TCanvas('c_kinpf','c_kinpf')
binsx = np.arange(0.,100.,2.)
binsy = np.arange(0.,100.,2.)
h_kinpf = ROOT.TH2F('h','',len(binsx)-1,binsx,len(binsy)-1,binsy)
h_kinpf.SetTitle(';Gen production radius [cm] ; RECO production radius [cm];entries')
tt_kinpf.Draw('hnl_2d_disp:hnl_2d_gen_disp >> h')
h_kinpf.Draw('colz')
pf.showlumi('KinVtxFit, PF#mu')
c_kinpf.Update()

# kalman fitter
c_kalpf = ROOT.TCanvas('c_kalpf','c_kalpf')
binsx = np.arange(0.,100.,2.)
h_kalpf = ROOT.TH2F('h','',len(binsx)-1,binsx,len(binsy)-1,binsy)
h_kalpf.SetTitle(';Gen production radius [cm] ; RECO production radius [cm];entries')
tt_kalpf.Draw('hnl_2d_disp:hnl_2d_gen_disp >> h')
h_kalpf.Draw('colz')
pf.showlumi('KalVtxFit, PF#mu')
c_kalpf.Update()

# kinematic fitter
c_kinsa = ROOT.TCanvas('c_kinsa','c_kinsa')
binsx = np.arange(0.,100.,2.)
binsy = np.arange(0.,100.,2.)
h_kinsa = ROOT.TH2F('h','',len(binsx)-1,binsx,len(binsy)-1,binsy)
h_kinsa.SetTitle(';Gen production radius [cm] ; RECO production radius [cm];entries')
tt_kinsa.Draw('hnl_2d_disp:hnl_2d_gen_disp >> h')
h_kinsa.Draw('colz')
pf.showlumi('KinVtxFit, SA#mu')
c_kinsa.Update()

# kalman fitter
c_kalsa = ROOT.TCanvas('c_kalsa','c_kalsa')
binsx = np.arange(0.,100.,2.)
h_kalsa = ROOT.TH2F('h','',len(binsx)-1,binsx,len(binsy)-1,binsy)
h_kalsa.SetTitle(';Gen production radius [cm] ; RECO production radius [cm];entries')
tt_kalsa.Draw('hnl_2d_disp:hnl_2d_gen_disp >> h')
h_kalsa.Draw('colz')
pf.showlumi('KalVtxFit, SA#mu')
c_kalsa.Update()



c_kinpf.SaveAs(output_dir + 'KinPF.pdf')
c_kinpf.SaveAs(output_dir + 'KinPF.root')
c_kalpf.SaveAs(output_dir + 'KalPF.pdf')
c_kalpf.SaveAs(output_dir + 'KalPF.root')
c_kinsa.SaveAs(output_dir + 'KinSA.pdf')
c_kinsa.SaveAs(output_dir + 'KinSA.root')
c_kalsa.SaveAs(output_dir + 'KalSA.pdf')
c_kalsa.SaveAs(output_dir + 'KalSA.root')
