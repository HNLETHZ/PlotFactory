import ROOT as rt
import plotfactory as pf
import numpy as np
from glob import glob


ntDir   = '/eos/user/v/vstampf/ntuples/archive/gen_v1_refurbshd/'
plotDir  = '/eos/user/v/vstampf/plots/'

M_all = glob(ntDir + '*/HNLGenTreeProducer/tree.root')

M_all_e   = [f for f in M_all if '_e' in f]
M_all_mu = [f for f in M_all if '_mu' in f]

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


pf.setpfstyle()

def checkAcc(mode='e'):
    cut_denom =  ''
    cut_num   =  'is_in_acc == 1 & l1_matched_dsmuon_pt > 5 & l2_matched_dsmuon_pt > 5' # CHECK this should work for e os and m os 
    if mode == 'e':
        cut_num   += ' & l0_matched_electron_pt > 30 & l0_matched_electron_reliso05 < 0.15'
        Mlist = Mlist_e
    if mode == 'mu':
        cut_num   += ' & l0_matched_muon_pt > 25 & l0_matched_muon_reliso05 < 0.15'
        Mlist = Mlist_mu


    for m, mass in Mlist:
        t = rt.TChain('tree')
        for f in mass:
            t.Add(f)

        b_2disp = np.arange(0.,350,5)
        b_eff   = np.arange(0.,1,0.1) 

        if m=='all': m=0
        if float(m) == 1: 
            b_2disp = np.arange(0.,450,50)
        if float(m) == 4: 
            b_2disp = np.concatenate( (np.arange(0.,200,5),np.arange(200.,300,10), np.arange(300.,350,25)), axis=None )
        if float(m) > 4:  
            b_2disp = np.concatenate( (np.arange(0.,150,25), np.arange(150.,200,50), np.arange(200.,350,150)), axis=None)
        if float(m) == 7: 
            b_2disp = np.concatenate( (np.arange(0.,25,1), np.arange(25.,100,25)), axis=None)
        if float(m) == 8: 
            b_2disp = np.concatenate( (np.arange(0.,10,1), np.arange(10.,20,5), np.arange(20.,30,10)), axis=None)
        if float(m) == 9:  
            b_2disp = np.concatenate( (np.arange(0.,5,1), np.arange(5,15,2.5)), axis=None)
        if float(m) == 10:  
            b_2disp = np.concatenate( (np.arange(0.,2.5,0.5), np.arange(2.5,10,2.5)), axis=None)
        if m==0: m='all'

        framer = rt.TH2F('framer','framer',len(b_2disp)-1,b_2disp,len(b_eff)-1,b_eff)
        framer.SetTitle('; 2D displacement [cm]; Signal acceptance')
        framer.SetAxisRange(0.,350,"X")
        framer.SetAxisRange(0.,1,"Y")

        if m=='all': m=0
        if float(m) == 1: 
            framer.SetAxisRange(0.,450,"X")
        if float(m) == 7: 
            framer.SetAxisRange(0.,100,"X")
        if float(m) == 8: 
            framer.SetAxisRange(0.,30,"X")
        if float(m) == 9:  
            framer.SetAxisRange(0.,15,"X")
        if float(m) == 10:  
            framer.SetAxisRange(0.,10,"X")
        if m==0: m='1-10'

        if mode =='mu': mode = '#mu'

        num   = rt.TH1F('num'  , 'num' , len(b_2disp)-1, b_2disp)
        denom = rt.TH1F('denom','denom', len(b_2disp)-1, b_2disp)

        print '\t mass:', m, 'entries:', t.GetEntries()
        
        print '\t denom entries: %i,'%t.GetEntries(cut_denom), 'drawing denom ...'
        t.Draw('hnl_2d_disp >> denom', cut_denom)

        print '\t denom done\n\tnum entries: %i,'%t.GetEntries(cut_num), 'drawing num ...'
        t.Draw('hnl_2d_disp >> num', cut_num)

        eff = rt.TEfficiency(num, denom)

        c_eff = rt.TCanvas('eff_M_%s_%s'%(m,mode),'eff_M_%s_%s'%(m,mode))
        framer.Draw()
        eff.Draw('same')
        pf.showlogoprelimsim('CMS')
        pf.showlumi('m(N) = %s GeV'%m)
        pf.showTitle('%s#mu#mu'%mode)
        c_eff.Modified(); c_eff.Update()
        c_eff.SaveAs(plotDir + c_eff.GetTitle() + '.root')
        c_eff.SaveAs(plotDir + c_eff.GetTitle() + '.pdf')
        c_eff.SaveAs(plotDir + c_eff.GetTitle() + '.png')
      
