import ROOT as rt
import plotfactory as pf
import numpy as np
from glob import glob


ntDir_e   = '/eos/user/v/vstampf/ntuples/sig_mc_e/ntuples/'
ntDir_m   = '/eos/user/v/vstampf/ntuples/sig_mc_m/ntuples/'

plotDir  = '/eos/user/v/vstampf/plots/'

M_all_e = glob(ntDir_e + '*/HNLTreeProducer/tree.root')
M_all_mu = glob(ntDir_m + '*/HNLTreeProducer/tree.root')

M1_e   = [f for f in M_all_e if 'M_1_' in f]
M2_e   = [f for f in M_all_e if 'M_2_' in f]
M3_e   = [f for f in M_all_e if 'M_3_' in f]
M4_e   = [f for f in M_all_e if 'M_4_' in f]
M5_e   = [f for f in M_all_e if 'M_5_' in f]
M6_e   = [f for f in M_all_e if 'M_6_' in f]
M7_e   = [f for f in M_all_e if 'M_7_' in f]
M8_e   = [f for f in M_all_e if 'M_8_' in f]
M9_e   = [f for f in M_all_e if 'M_9_' in f]
M10_e  = [f for f in M_all_e if 'M_10_' in f]
M2p1_e = [f for f in M_all_e if 'M_2p1_' in f]
M2p5_e = [f for f in M_all_e if 'M_2p5_' in f]

M1_mu   = [f for f in M_all_mu if 'M_1_' in f]
M2_mu   = [f for f in M_all_mu if 'M_2_' in f]
M3_mu   = [f for f in M_all_mu if 'M_3_' in f]
M4_mu   = [f for f in M_all_mu if 'M_4_' in f]
M5_mu   = [f for f in M_all_mu if 'M_5_' in f]
M6_mu   = [f for f in M_all_mu if 'M_6_' in f]
M7_mu   = [f for f in M_all_mu if 'M_7_' in f]
M8_mu   = [f for f in M_all_mu if 'M_8_' in f]
M9_mu   = [f for f in M_all_mu if 'M_9_' in f]
M10_mu  = [f for f in M_all_mu if 'M_10_' in f]
M2p1_mu = [f for f in M_all_mu if 'M_2p1_' in f]
M2p5_mu = [f for f in M_all_mu if 'M_2p5_' in f]

Mlist_e  = [['1',M1_e],['2',M2_e],['2.1',M2p1_e],['2.5',M2p5_e],['3',M3_e],['4',M4_e],['5',M5_e],['6',M6_e],['7',M7_e],['8',M8_e],['9',M9_e],['10',M10_e],['all',M_all_e],]
Mlist_mu = [['1',M1_mu],['2',M2_mu],['2.1',M2p1_mu],['2.5',M2p5_mu],['3',M3_mu],['4',M4_mu],['5',M5_mu],['6',M6_mu],['7',M7_mu],['8',M8_mu],['9',M9_mu],['10',M10_mu],['all',M_all_mu],]

Mlist_em = []
for i in range(13):
    Mlist_em.append([Mlist_e[i][0],Mlist_e[i][1]+Mlist_mu[i][1]])

pf.setpfstyle()

def checkAcc(mode='e'):
    cut_denom =  ''
    cut   =  'l1_pt > 0 & l2_pt > 0' 
    if mode == 'e':
#        cut_mll   += ' & l0_matched_electron_pt > 30 & l0_matched_electron_reliso05 < 0.15'
        Mlist = Mlist_e
    if mode == 'mu':
#        cut_mll   += ' & l0_matched_muon_pt > 25 & l0_matched_muon_reliso05 < 0.15'
        Mlist = Mlist_mu
    if mode == 'cmbd':
        Mlist = Mlist_em 

    for m, mass in Mlist:
        t = rt.TChain('tree')
        for f in mass:
            t.Add(f)

        b_m = np.arange(0.,10,0.1)
        b_eff = np.arange(0.,1,0.1)

#        if m=='all': m=0
#        if m=='cmbd':m=11
#        if float(m) == 1: 
#            b_m = np.arange(0.,450,50)
#        if float(m) == 4: 
#            b_m = np.concatenate( (np.arange(0.,200,5),np.arange(200.,300,10), np.arange(300.,350,25)), axis=None )
#        if float(m) > 4:  
#            b_m = np.concatenate( (np.arange(0.,150,25), np.arange(150.,200,50), np.arange(200.,350,150)), axis=None)
#        if float(m) == 7: 
#            b_m = np.concatenate( (np.arange(0.,25,1), np.arange(25.,100,25)), axis=None)
#        if float(m) == 8: 
#            b_m = np.concatenate( (np.arange(0.,10,1), np.arange(10.,20,5), np.arange(20.,30,10)), axis=None)
#        if float(m) == 9:  
#            b_m = np.concatenate( (np.arange(0.,5,1), np.arange(5,15,2.5)), axis=None)
#        if float(m) == 10:  
#            b_m = np.concatenate( (np.arange(0.,2.5,0.5), np.arange(2.5,10,2.5)), axis=None)
#        if m==0:  m='all'
#        if m==11: m='cmbd'

        framer = rt.TH2F('framer','framer',len(b_m)-1,b_m,len(b_eff)-1,b_eff)
        framer.SetTitle('; 2D displacement [cm]; Signal acceptance')
        framer.SetAxisRange(0.,350,"X")
        framer.SetAxisRange(0.,1,"Y")

#        if m=='all': m=0
#        if float(m) == 1: 
#            framer.SetAxisRange(0.,450,"X")
#        if float(m) == 7: 
#            framer.SetAxisRange(0.,100,"X")
#        if float(m) == 8: 
#            framer.SetAxisRange(0.,30,"X")
#        if float(m) == 9:  
#            framer.SetAxisRange(0.,15,"X")
#        if float(m) == 10:  
#            framer.SetAxisRange(0.,10,"X")
#        if m==0: m='1-10'

        if mode =='mu': mode = '#mu'
        if mode =='cmbd':mode = '(e+#mu)'

        mll   = rt.TH1F('mll'  , 'mll' , len(b_m)-1, b_m)
        mll.SetTitle('; di-muon mass [GeV]; a.u.')

        print '\t mass:', m, 'entries:', t.GetEntries()

        print '\t done\n\thist entries: %i,'%t.GetEntries(cut), 'drawing mll ...'
        t.Draw('hnl_m_12 >> mll', cut)

        c_mll = rt.TCanvas('mll_M_%s_%s'%(m,mode),'mll_M_%s_%s'%(m,mode))
        mll.DrawNormalized()
        pf.showlogoprelimsim('CMS')
        pf.showlumi('m(N) = %s GeV'%m)
        pf.showTitle('%s#mu#mu'%mode)
        c_mll.Modified(); c_mll.Update()
        c_mll.SaveAs(plotDir + c_mll.GetTitle() + '.root')
        c_mll.SaveAs(plotDir + c_mll.GetTitle() + '.pdf')
        c_mll.SaveAs(plotDir + c_mll.GetTitle() + '.png')
      
