########################## 
# Configuration
##########################
import ROOT
import plotfactory as pf
import numpy as np
from array import array
import sys
from pdb import set_trace

pf.setpfstyle()

######################################### 
# Make Chain from selection of samples
#########################################
# Get the option from the command line, using 'True' as a fallback.
if len(sys.argv)>=2 and sys.argv[1] == 'test':
    setting = False
    print('Using a selection of samples')
else:
    setting = True
    print('Using all samples')

tt = pf.makechain(setting)

nentries = tt.GetEntries()
print('number of events: %d'%(nentries))

etalow  = 0.0
etahigh = 0.8   

output_dir = 'temp/'

########################## 
# Define x-axis
##########################
binsx_width = 10. 
binsx = np.arange(0.,50.5,binsx_width) 
binsx_sub = np.arange(-1.,2.,0.02) 
binsx_sub_g = np.arange(-1.,2.,0.06) 
binsx_sub_r3 = np.arange(-1.,3.,0.2) 
binsx_sub_r3_fine = np.arange(-1.,2.,0.1) 


########################## 
# Create canvas(es)
##########################
print('preparing canvas')

c_ptres_sub  = ROOT.TCanvas('c_ptres_sub', 'c_ptres_sub')
c_ptres_subr3  = ROOT.TCanvas('c_ptres_subr3', 'c_ptres_subr3')
c_ptres_r1   = ROOT.TCanvas('c_ptres_r1', 'c_ptres_r1')
c_ptres_rt1  = ROOT.TCanvas('c_ptres_rt1', 'c_ptres_rt1')
c_ptres_rt2  = ROOT.TCanvas('c_ptres_rt2', 'c_ptres_rt2')
c_ptres_r2   = ROOT.TCanvas('c_ptres_r2', 'c_ptres_r2')
c_ptres_r3   = ROOT.TCanvas('c_ptres_r3', 'c_ptres_r3')
c_dsmuon_r1  = ROOT.TCanvas('c_dsmuon_r1', 'c_dsmuon_r1')
c_dsmuon_rt1 = ROOT.TCanvas('c_dsmuon_rt1', 'c_dsmuon_rt1')
c_dsmuon_rt2 = ROOT.TCanvas('c_dsmuon_rt2', 'c_dsmuon_rt2')
c_dsmuon_r2  = ROOT.TCanvas('c_dsmuon_r2', 'c_dsmuon_r2')
c_dsmuon_r3  = ROOT.TCanvas('c_dsmuon_r3', 'c_dsmuon_r3')
c_smuon_r1   = ROOT.TCanvas('c_smuon_r1', 'c_smuon_r1')
c_smuon_rt1  = ROOT.TCanvas('c_smuon_rt1', 'c_smuon_rt1')
c_smuon_rt2  = ROOT.TCanvas('c_smuon_rt2', 'c_smuon_rt2')
c_smuon_r2   = ROOT.TCanvas('c_smuon_r2', 'c_smuon_r2')
c_smuon_r3   = ROOT.TCanvas('c_smuon_r3', 'c_smuon_r3')

########################## 
# 4) Create histograms
##########################
h_pt_dsMuon = ROOT.TH1F('h_pt','',len(binsx)-1,binsx)
h_ptres_dsMuon = ROOT.TH1F('h_ptres_dsMuon','',len(binsx)-1,binsx)
h_ptres_sub = ROOT.TH1F('h_ptres_sub','',len(binsx_sub)-1,binsx_sub)
h_ptres_sub_l1 = ROOT.TH1F('h_ptres_sub_l1','',len(binsx_sub)-1,binsx_sub)
h_ptres_sub_l2 = ROOT.TH1F('h_ptres_sub_l2','',len(binsx_sub)-1,binsx_sub)
h_ptres_subr3 = ROOT.TH1F('h_ptres_subr3','',len(binsx_sub_r3)-1,binsx_sub_r3)
h_ptres_subr3_l1 = ROOT.TH1F('h_ptres_subr3_l1','',len(binsx_sub_r3)-1,binsx_sub_r3)
h_ptres_subr3_l2 = ROOT.TH1F('h_ptres_subr3_l2','',len(binsx_sub_r3)-1,binsx_sub_r3)

h_dsmuon_r1 = ROOT.TH2F('h_dsmuon_r1','',len(binsx)-1,binsx,len(binsx_sub)-1,binsx_sub)
h_dsmuon_rt1= ROOT.TH2F('h_dsmuon_rt1','',len(binsx)-1,binsx,len(binsx_sub)-1,binsx_sub)
h_dsmuon_rt2= ROOT.TH2F('h_dsmuon_rt2','',len(binsx)-1,binsx,len(binsx_sub)-1,binsx_sub)
h_dsmuon_r2 = ROOT.TH2F('h_dsmuon_r2','',len(binsx)-1,binsx,len(binsx_sub)-1,binsx_sub)
h_dsmuon_r3 = ROOT.TH2F('h_dsmuon_r3','',len(binsx)-1,binsx,len(binsx_sub_r3)-1,binsx_sub_r3)
h_smuon_r1 = ROOT.TH2F('h_smuon_r1','',len(binsx)-1,binsx,len(binsx_sub)-1,binsx_sub)
h_smuon_rt1 = ROOT.TH2F('h_smuon_rt1','',len(binsx)-1,binsx,len(binsx_sub)-1,binsx_sub)
h_smuon_rt2 = ROOT.TH2F('h_smuon_rt2','',len(binsx)-1,binsx,len(binsx_sub)-1,binsx_sub)
h_smuon_r2 = ROOT.TH2F('h_smuon_r2','',len(binsx)-1,binsx,len(binsx_sub)-1,binsx_sub)
h_smuon_r3 = ROOT.TH2F('h_smuon_r3','',len(binsx)-1,binsx,len(binsx_sub_r3)-1,binsx_sub_r3)

h_sub = ROOT.TH2F('h_sub','',len(binsx)-1,binsx,len(binsx_sub)-1,binsx_sub)
h_subr3 = ROOT.TH2F('h_subr3','',len(binsx)-1,binsx,len(binsx_sub_r3)-1,binsx_sub_r3)

########################## 
# 5) Specify histogram formats
##########################
# define plot formats
for hh in [h_pt_dsMuon, h_ptres_dsMuon]:
    hh.GetXaxis().SetTitle('p_{T}[GeV]')
    hh.GetYaxis().SetTitle('#Delta (p_{T})/(p_{T})')
    hh.GetXaxis().SetTitleOffset(1.3)
    hh.GetYaxis().SetTitleOffset(1.4)
    hh.SetMarkerStyle(8)
    hh.SetMarkerSize(0.4)

h_pt_dsMuon     .SetLineColor       (ROOT.kRed+2)
h_pt_dsMuon     .SetMarkerColor     (ROOT.kRed+2)
h_ptres_dsMuon  .SetLineColor       (ROOT.kGreen+2)
h_ptres_dsMuon  .SetMarkerColor     (ROOT.kGreen+2)

for hh in[h_ptres_sub, h_ptres_subr3]:
    hh.GetXaxis().SetTitle('#Delta (p_{T})/(p_{T})')
    hh.GetYaxis().SetTitle('Entries')
    hh.GetXaxis().SetTitleOffset(1.1)
    hh.GetYaxis().SetTitleOffset(1.4)
    hh.SetMarkerStyle(8)
    hh.SetMarkerSize(0.4)

for hh in [h_dsmuon_r1,h_dsmuon_rt1,h_dsmuon_rt2,h_dsmuon_r2,h_dsmuon_r3,h_smuon_r1,h_smuon_rt1,h_smuon_rt2,h_smuon_r2,h_smuon_r3]:
    hh.GetXaxis().SetTitle('p_{T}[GeV]')
    hh.GetYaxis().SetTitle('#Delta (p_{T})/(p_{T})')
    hh.GetXaxis().SetTitleOffset(1.1)
    hh.GetYaxis().SetTitleOffset(1.4)
    hh.GetXaxis().SetRangeUser(0.,50.)
    hh.GetYaxis().SetRangeUser(-1.1,1.0)
    hh.GetXaxis().SetTitleSize(0.05)
    hh.GetYaxis().SetTitleSize(0.05)
    hh.GetXaxis().SetLabelSize(0.05)
    hh.GetYaxis().SetLabelSize(0.05)
    hh.GetZaxis().SetLabelSize(0.05)
    hh.SetMarkerStyle(8)
    hh.SetMarkerSize(0.4)

    
h_ptres_sub  .SetLineColor       (ROOT.kBlue+2)
h_ptres_sub  .SetMarkerColor     (ROOT.kBlue+2)
h_ptres_subr3  .SetLineColor       (ROOT.kBlue+2)
h_ptres_subr3 .SetMarkerColor     (ROOT.kBlue+2)

########################## 
# 6) Building core histograms
##########################
print('building core histograms')

x= array( 'f', binsx ) 
x= array('f',[i+(binsx_width/2.) for i in x])

n   = len(x)

y_dsmu_r1   = array( 'f', [binsx_width/2.] * len(x) )
y_dsmu_rt1  = array( 'f', [binsx_width/2.] * len(x) )
y_dsmu_rt2  = array( 'f', [binsx_width/2.] * len(x) )
y_dsmu_r2   = array( 'f', [binsx_width/2.] * len(x) )
y_dsmu_r3   = array( 'f', [binsx_width/2.] * len(x) )
y_smu_r1    = array( 'f', [binsx_width/2.] * len(x) )
y_smu_rt1   = array( 'f', [binsx_width/2.] * len(x) )
y_smu_rt2   = array( 'f', [binsx_width/2.] * len(x) )
y_smu_r2    = array( 'f', [binsx_width/2.] * len(x) )
y_smu_r3    = array( 'f', [binsx_width/2.] * len(x) )
exl_dsmu_r1 = array( 'f', [binsx_width/2.] * len(x) )
exl_dsmu_rt1= array( 'f', [binsx_width/2.] * len(x) )
exl_dsmu_rt2= array( 'f', [binsx_width/2.] * len(x) )
exl_dsmu_r2 = array( 'f', [binsx_width/2.] * len(x) )
exl_dsmu_r3 = array( 'f', [binsx_width/2.] * len(x) )
exh_dsmu_r1 = array( 'f', [binsx_width/2.] * len(x) )
exh_dsmu_rt1= array( 'f', [binsx_width/2.] * len(x) )
exh_dsmu_rt2= array( 'f', [binsx_width/2.] * len(x) )
exh_dsmu_r2 = array( 'f', [binsx_width/2.] * len(x) )
exh_dsmu_r3 = array( 'f', [binsx_width/2.] * len(x) )
eyl_dsmu_r1 = array( 'f', [binsx_width/2.] * len(x) )
eyl_dsmu_rt1= array( 'f', [binsx_width/2.] * len(x) )
eyl_dsmu_rt2= array( 'f', [binsx_width/2.] * len(x) )
eyl_dsmu_r2 = array( 'f', [binsx_width/2.] * len(x) )
eyl_dsmu_r3 = array( 'f', [binsx_width/2.] * len(x) )
eyh_dsmu_r1 = array( 'f', [binsx_width/2.] * len(x) )
eyh_dsmu_rt1= array( 'f', [binsx_width/2.] * len(x) )
eyh_dsmu_rt2= array( 'f', [binsx_width/2.] * len(x) )
eyh_dsmu_r2 = array( 'f', [binsx_width/2.] * len(x) )
eyh_dsmu_r3 = array( 'f', [binsx_width/2.] * len(x) )
exl_smu_r1  = array( 'f', [binsx_width/2.] * len(x) )
exl_smu_rt1 = array( 'f', [binsx_width/2.] * len(x) )
exl_smu_rt2 = array( 'f', [binsx_width/2.] * len(x) )
exl_smu_r2  = array( 'f', [binsx_width/2.] * len(x) )
exl_smu_r3  = array( 'f', [binsx_width/2.] * len(x) )
exh_smu_r1  = array( 'f', [binsx_width/2.] * len(x) )
exh_smu_rt1 = array( 'f', [binsx_width/2.] * len(x) )
exh_smu_rt2 = array( 'f', [binsx_width/2.] * len(x) )
exh_smu_r2  = array( 'f', [binsx_width/2.] * len(x) )
exh_smu_r3  = array( 'f', [binsx_width/2.] * len(x) )
eyl_smu_r1  = array( 'f', [binsx_width/2.] * len(x) )
eyl_smu_rt1 = array( 'f', [binsx_width/2.] * len(x) )
eyl_smu_rt2 = array( 'f', [binsx_width/2.] * len(x) )
eyl_smu_r2  = array( 'f', [binsx_width/2.] * len(x) )
eyl_smu_r3  = array( 'f', [binsx_width/2.] * len(x) )
eyh_smu_r1  = array( 'f', [binsx_width/2.] * len(x) )
eyh_smu_rt1 = array( 'f', [binsx_width/2.] * len(x) )
eyh_smu_rt2 = array( 'f', [binsx_width/2.] * len(x) )
eyh_smu_r2  = array( 'f', [binsx_width/2.] * len(x) )
eyh_smu_r3  = array( 'f', [binsx_width/2.] * len(x) )


for ibin in xrange(len(binsx)-1):
# for ibin in xrange(1):
    for ireco in ['dsmu','smu']:
        for ir in ['r1','rt1','rt2','r2','r3']:
    # for ireco in ['smu']:
        # for ir in ['r3']:
            # tools.progress(ibin+1,len(binsx)-1,'processing bin %d/%d, %s, %s'%(ibin,len(binsx)-1,ireco,ir))
            ptlow  = binsx[ibin]
            pthigh = binsx[ibin+1]

            h_ptres_sub.Reset()
            h_ptres_sub_l1.Reset()
            h_ptres_sub_l2.Reset()
            h_ptres_subr3.Reset()
            h_ptres_subr3_l1.Reset()
            h_ptres_subr3_l2.Reset()

            # range r1: 0 cm - 4 cm (before Pixel)
            if ir == 'r1':
                rl = 0. 
                rh = 4.
            
            # range rt1: 4 cm - 60 cm (Tracker)
            if ir == 'rt1':
                rl = 4. 
                rh = 60.
            
            # range rt2: 60 cm - 120 cm (Tracker)
            if ir == 'rt2':
                rl = 60. 
                rh = 120.
            
            #range r2: 120 cm - 350 cm (between Pixel and MuDetector)
            if ir == 'r2':
                rl = 120.
                rh = 350.

            #range r3: 350 cm - 600 cm (inside MuDetector until Layer 3)
            if ir == 'r3':
                rl = 350.
                rh = 600.

            if ireco == 'dsmu':
                reco = 'dsmuon'

            if ireco == 'smu':
                reco = 'muon'

            if ir != 'r3':
                c_ptres_sub.cd()
                # tt.Draw("(l0_matched_%s_pt-l0_pt)/l0_pt >> h_ptres_sub"%(reco),"l0_matched_%s_pt>0 & abs(l0_pdgId) == 13 & abs(l0_eta)<2.4 & %d<l0_pt & l0_pt<%d & hnl_2d_disp>%d & hnl_2d_disp<%d" % (reco,ptlow,pthigh,rl,rh))
                if ireco == 'smu':
                    tt.Draw("(l1_matched_%s_pt-l1_pt)/l1_pt >> h_ptres_sub_l1"%(reco),"l1_matched_%s_is_sa==1 & l1_matched_%s_pt>0 & abs(l1_pdgId) == 13 & abs(l1_eta)>%f & abs(l1_eta)>%f & l1_matched_%s_charge == l1_charge & %d<l1_pt & l1_pt<%d & hnl_2d_disp>%d & hnl_2d_disp<%d" % (reco,reco,etalow,etahigh,reco,ptlow,pthigh,rl,rh))
                    h_ptres_sub.Add(h_ptres_sub_l1)
                    tt.Draw("(l2_matched_%s_pt-l2_pt)/l2_pt >> h_ptres_sub_l2"%(reco),"l2_matched_%s_is_sa==1 & l2_matched_%s_pt>0 & abs(l2_pdgId) == 13 & abs(l2_eta)>%f & abs(l2_eta)<%f & l2_matched_%s_charge == l2_charge & %d<l2_pt & l2_pt<%d & hnl_2d_disp>%d & hnl_2d_disp<%d" % (reco,reco,etalow,etahigh,reco,ptlow,pthigh,rl,rh))

                if ireco == 'dsmu':
                    tt.Draw("(l1_matched_%s_pt-l1_pt)/l1_pt >> h_ptres_sub_l1"%(reco),"l1_matched_%s_pt>0 & abs(l1_pdgId) == 13 & abs(l1_eta)>%f & abs(l1_eta)>%f & l1_matched_%s_charge == l1_charge & %d<l1_pt & l1_pt<%d & hnl_2d_disp>%d & hnl_2d_disp<%d" % (reco,etalow,etahigh,reco,ptlow,pthigh,rl,rh))
                    h_ptres_sub.Add(h_ptres_sub_l1)
                    tt.Draw("(l2_matched_%s_pt-l2_pt)/l2_pt >> h_ptres_sub_l2"%(reco),"l2_matched_%s_pt>0 & abs(l2_pdgId) == 13 & abs(l2_eta)>%f & abs(l2_eta)<%f & l2_matched_%s_charge == l2_charge & %d<l2_pt & l2_pt<%d & hnl_2d_disp>%d & hnl_2d_disp<%d" % (reco,etalow,etahigh,reco,ptlow,pthigh,rl,rh))

                h_ptres_sub.Add(h_ptres_sub_l2)
                ROOT.gPad.Update()
                c_ptres_sub.SaveAs(output_dir + 'raw/c_ptres_bin%d_%s_%s.root'%(ibin,ireco,ir))
                c_ptres_sub.SaveAs(output_dir + 'raw/c_ptres_bin%d_%s_%s.pdf'%(ibin,ireco,ir))

                sub_entries = h_ptres_sub.GetEntries()
                maxbin  = h_ptres_sub.GetMaximumBin()
                maxres  = h_ptres_sub.GetBinCenter(maxbin)
                maxcont = h_ptres_sub.GetBinContent(maxbin)
                lowbin  = maxbin
                highbin = maxbin

                while True:
                    lowbin  -=1
                    lowcont = h_ptres_sub.GetBinContent(lowbin)
                    if lowcont <= (maxcont/2.0):
                        break
                lowres = h_ptres_sub.GetBinCenter(lowbin)
                lowerr = maxres - lowres

                while True:
                    highbin  += 1
                    highcont = h_ptres_sub.GetBinContent(highbin)
                    if highcont <= (maxcont/2.0):
                        break
                highres = h_ptres_sub.GetBinCenter(highbin)
                higherr = highres - maxres

            if ir == 'r3':
                c_ptres_subr3.cd()
                if ireco == 'smu':
                    tt.Draw("(l1_matched_%s_pt-l1_pt)/l1_pt >> h_ptres_subr3_l1"%(reco),"l1_matched_%s_is_sa==1 & l1_matched_%s_pt>0 & abs(l1_pdgId) == 13 & abs(l1_eta)>%f & abs(l1_eta)>%f & l1_matched_%s_charge == l1_charge & %d<l1_pt & l1_pt<%d & hnl_2d_disp>%d & hnl_2d_disp<%d" % (reco,reco,etalow,etahigh,reco,ptlow,pthigh,rl,rh))
                    h_ptres_subr3.Add(h_ptres_subr3_l1)
                    tt.Draw("(l2_matched_%s_pt-l2_pt)/l2_pt >> h_ptres_subr3_l2"%(reco),"l2_matched_%s_is_sa==1 & l2_matched_%s_pt>0 & abs(l2_pdgId) == 13 & abs(l2_eta)>%f & abs(l2_eta)<%f & l2_matched_%s_charge == l2_charge & %d<l2_pt & l2_pt<%d & hnl_2d_disp>%d & hnl_2d_disp<%d" % (reco,reco,etalow,etahigh,reco,ptlow,pthigh,rl,rh))

                if ireco == 'dsmu':
                    tt.Draw("(l1_matched_%s_pt-l1_pt)/l1_pt >> h_ptres_subr3_l1"%(reco),"l1_matched_%s_pt>0 & abs(l1_pdgId) == 13 & abs(l1_eta)>%f & abs(l1_eta)>%f & l1_matched_%s_charge == l1_charge & %d<l1_pt & l1_pt<%d & hnl_2d_disp>%d & hnl_2d_disp<%d" % (reco,etalow,etahigh,reco,ptlow,pthigh,rl,rh))
                    h_ptres_subr3.Add(h_ptres_subr3_l1)
                    tt.Draw("(l2_matched_%s_pt-l2_pt)/l2_pt >> h_ptres_subr3_l2"%(reco),"l2_matched_%s_pt>0 & abs(l2_pdgId) == 13 & abs(l2_eta)>%f & abs(l2_eta)<%f & l2_matched_%s_charge == l2_charge & %d<l2_pt & l2_pt<%d & hnl_2d_disp>%d & hnl_2d_disp<%d" % (reco,etalow,etahigh,reco,ptlow,pthigh,rl,rh))

                h_ptres_subr3.Add(h_ptres_subr3_l2)
                ROOT.gPad.Update()
                c_ptres_subr3.SaveAs(output_dir + 'raw/c_ptres_bin%d_%s_%s.root'%(ibin,ireco,ir))
                c_ptres_subr3.SaveAs(output_dir + 'raw/c_ptres_bin%d_%s_%s.pdf'%(ibin,ireco,ir))

                sub_entries = h_ptres_subr3.GetEntries()
                maxbin  = h_ptres_subr3.GetMaximumBin()
                maxres  = h_ptres_subr3.GetBinCenter(maxbin)
                maxcont = h_ptres_subr3.GetBinContent(maxbin)
                lowbin  = maxbin
                highbin = maxbin

                while True:
                    lowbin  -=1
                    lowcont = h_ptres_subr3.GetBinContent(lowbin)
                    if lowcont <= (maxcont/2.0):
                        break
                lowres = h_ptres_subr3.GetBinCenter(lowbin)
                lowerr = maxres - lowres

                while True:
                    highbin  += 1
                    highcont = h_ptres_subr3.GetBinContent(highbin)
                    if highcont <= (maxcont/2.0):
                        break
                highres = h_ptres_subr3.GetBinCenter(highbin)
                higherr = highres - maxres

            if ireco == 'dsmu'and ir == 'r1':
                y_dsmu_r1[ibin]       = maxres
                eyl_dsmu_r1[ibin]     = lowerr
                eyh_dsmu_r1[ibin]     = higherr
            if ireco == 'dsmu'and ir == 'rt1':
                y_dsmu_rt1[ibin]       = maxres
                eyl_dsmu_rt1[ibin]     = lowerr
                eyh_dsmu_rt1[ibin]     = higherr
            if ireco == 'dsmu'and ir == 'rt2':
                y_dsmu_rt2[ibin]       = maxres
                eyl_dsmu_rt2[ibin]     = lowerr
                eyh_dsmu_rt2[ibin]     = higherr
            if ireco == 'dsmu'and ir == 'r2':
                y_dsmu_r2[ibin]       = maxres
                eyl_dsmu_r2[ibin]     = lowerr
                eyh_dsmu_r2[ibin]     = higherr
            if ireco == 'dsmu'and ir == 'r3':
                y_dsmu_r3[ibin]       = maxres
                eyl_dsmu_r3[ibin]     = lowerr
                eyh_dsmu_r3[ibin]     = higherr
            if ireco == 'smu'and ir == 'r1':
                y_smu_r1[ibin]       = maxres
                eyl_smu_r1[ibin]     = lowerr
                eyh_smu_r1[ibin]     = higherr
            if ireco == 'smu'and ir == 'rt1':
                y_smu_rt1[ibin]       = maxres
                eyl_smu_rt1[ibin]     = lowerr
                eyh_smu_rt1[ibin]     = higherr
            if ireco == 'smu'and ir == 'rt2':
                y_smu_rt2[ibin]       = maxres
                eyl_smu_rt2[ibin]     = lowerr
                eyh_smu_rt2[ibin]     = higherr
            if ireco == 'smu'and ir == 'r2':
                y_smu_r2[ibin]       = maxres
                eyl_smu_r2[ibin]     = lowerr
                eyh_smu_r2[ibin]     = higherr
            if ireco == 'smu'and ir == 'r3':
                y_smu_r3[ibin]       = maxres
                eyl_smu_r3[ibin]     = lowerr
                eyh_smu_r3[ibin]     = higherr

            # tools.progress(ibin+1,len(binsx)-1,'done bin %d/%d, %s, %s (maxres/lowres/highres: %d/%d/%d)'%(ibin,len(binsx)-1,ireco,ir,maxres,lowres,highres))
            # print('done bin %d/%d, \t%s, \t%s, \tentries = %d, \t(maxres/lowres/highres: \t%.4f/\t%.4f/\t%.4f)'%(ibin+1,len(binsx)-1,ireco,ir,sub_entries,maxres,lowres,highres))

g_ptres_dsMuon_r1= ROOT.TGraphAsymmErrors(n,x,y_dsmu_r1,exl_dsmu_r1,exh_dsmu_r1,eyl_dsmu_r1,eyh_dsmu_r1)
g_ptres_dsMuon_rt1=ROOT.TGraphAsymmErrors(n,x,y_dsmu_rt1,exl_dsmu_rt1,exh_dsmu_rt1,eyl_dsmu_rt1,eyh_dsmu_rt1)
g_ptres_dsMuon_rt2= ROOT.TGraphAsymmErrors(n,x,y_dsmu_rt2,exl_dsmu_rt2,exh_dsmu_rt2,eyl_dsmu_rt2,eyh_dsmu_rt2)
g_ptres_dsMuon_r2= ROOT.TGraphAsymmErrors(n,x,y_dsmu_r2,exl_dsmu_r2,exh_dsmu_r2,eyl_dsmu_r2,eyh_dsmu_r2)
g_ptres_dsMuon_r3= ROOT.TGraphAsymmErrors(n,x,y_dsmu_r3,exl_dsmu_r3,exh_dsmu_r3,eyl_dsmu_r3,eyh_dsmu_r3)
g_ptres_sMuon_r1 = ROOT.TGraphAsymmErrors(n,x,y_smu_r1,exl_smu_r1,exh_smu_r1,eyl_smu_r1,eyh_smu_r1)
g_ptres_sMuon_rt1 = ROOT.TGraphAsymmErrors(n,x,y_smu_rt1,exl_smu_rt1,exh_smu_rt1,eyl_smu_rt1,eyh_smu_rt1)
g_ptres_sMuon_rt2 = ROOT.TGraphAsymmErrors(n,x,y_smu_rt2,exl_smu_rt2,exh_smu_rt2,eyl_smu_rt2,eyh_smu_rt2)
g_ptres_sMuon_r2 = ROOT.TGraphAsymmErrors(n,x,y_smu_r2,exl_smu_r2,exh_smu_r2,eyl_smu_r2,eyh_smu_r2)
g_ptres_sMuon_r3 = ROOT.TGraphAsymmErrors(n,x,y_smu_r3,exl_smu_r3,exh_smu_r3,eyl_smu_r3,eyh_smu_r3)

for gg in[g_ptres_dsMuon_r1, g_ptres_dsMuon_rt1, g_ptres_dsMuon_rt2, g_ptres_dsMuon_r2, g_ptres_dsMuon_r3, g_ptres_sMuon_r1, g_ptres_sMuon_rt1, g_ptres_sMuon_rt2, g_ptres_sMuon_r2, g_ptres_sMuon_r3]:
    gg.GetXaxis().SetTitle('p_{T}[GeV]')
    gg.GetYaxis().SetTitle('#Delta (p_{T})/(p_{T})')
    # gg.GetXaxis().SetTitleOffset(1.3)
    # gg.GetYaxis().SetTitleOffset(1.4)
    # gg.SetMarkerStyle(8)
    # gg.SetMarkerSize(0.9)
    # gg.SetLineWidth(2)
    # hh.GetXaxis().SetTitleSize(0.05)
    # hh.GetYaxis().SetTitleSize(0.05)
    # hh.GetXaxis().SetLabelSize(0.05)
    # hh.GetYaxis().SetLabelSize(0.05)
    # hh.GetZaxis().SetLabelSize(0.05)
    gg.GetXaxis().SetRangeUser(0.,50.)
    gg.GetYaxis().SetRangeUser(-1.0,1.0)
    gg.SetTitle('')

g_ptres_dsMuon_r1.SetMarkerColor(ROOT.kRed)
g_ptres_dsMuon_rt1.SetMarkerColor(ROOT.kRed)
g_ptres_dsMuon_rt2.SetMarkerColor(ROOT.kRed)
g_ptres_dsMuon_r2.SetMarkerColor(ROOT.kRed)
g_ptres_dsMuon_r3.SetMarkerColor(ROOT.kRed)
g_ptres_sMuon_r1 .SetMarkerColor(ROOT.kBlue)
g_ptres_sMuon_rt1 .SetMarkerColor(ROOT.kBlue)
g_ptres_sMuon_rt2 .SetMarkerColor(ROOT.kBlue)
g_ptres_sMuon_r2 .SetMarkerColor(ROOT.kBlue)
g_ptres_sMuon_r3 .SetMarkerColor(ROOT.kBlue)

g_ptres_dsMuon_r1.SetLineColor(ROOT.kRed)
g_ptres_dsMuon_rt1.SetLineColor(ROOT.kRed)
g_ptres_dsMuon_rt2.SetLineColor(ROOT.kRed)
g_ptres_dsMuon_r2.SetLineColor(ROOT.kRed)
g_ptres_dsMuon_r3.SetLineColor(ROOT.kRed)
g_ptres_sMuon_r1 .SetLineColor(ROOT.kBlue)
g_ptres_sMuon_rt1 .SetLineColor(ROOT.kBlue)
g_ptres_sMuon_rt2 .SetLineColor(ROOT.kBlue)
g_ptres_sMuon_r2 .SetLineColor(ROOT.kBlue)
g_ptres_sMuon_r3 .SetLineColor(ROOT.kBlue)

print('drawing 2d histograms')
for ireco in ['dsmu','smu']:
    for ir in ['r1','rt1','rt2','r2','r3']:
        # range r1: 0 cm - 4 cm (before Pixel)
        if ir == 'r1':
            rl = 0. 
            rh = 4.
        
        # range rt: 4 cm - 60 cm (Tracker Region)
        if ir == 'rt1':
            rl = 4. 
            rh = 60.
        
        # range rt: 60 cm - 120 cm (Tracker Region)
        if ir == 'rt2':
            rl = 60. 
            rh = 120.
        
        #range r2: 120 cm - 350 cm (between Pixel and MuDetector)
        if ir == 'r2':
            rl = 120.
            rh = 350.

        #range r3: 350 cm - 600 cm (inside MuDetector until Layer 3)
        if ir == 'r3':
            rl = 350.
            rh = 600.

        if ireco == 'dsmu':
            reco = 'dsmuon'

        if ireco == 'smu':
            reco = 'muon'

        if ireco == 'dsmu' and ir == 'r1':
            c_dsmuon_r1.cd()
            tt.Draw("(l1_matched_%s_pt-l1_pt)/l1_pt : l1_pt >> h_dsmuon_r1"%(reco),"l1_matched_%s_pt>0 & abs(l1_pdgId) == 13 & abs(l1_eta)>%f &  abs(l1_eta)<%f & l1_matched_%s_charge == l1_charge & hnl_2d_disp>%d & hnl_2d_disp<%d" % (reco,etalow,etahigh,reco,rl,rh))
            tt.Draw("(l2_matched_%s_pt-l2_pt)/l2_pt : l2_pt >> h_sub"%(reco),"l2_matched_%s_pt>0 & abs(l2_pdgId) == 13 & abs(l2_eta)>%f &  abs(l2_eta)<%f & l2_matched_%s_charge == l2_charge & hnl_2d_disp>%d & hnl_2d_disp<%d" % (reco,etalow,etahigh,reco,rl,rh))
            h_dsmuon_r1.Add(h_sub)
            h_sub.Reset()
            h_dsmuon_r1.Draw('colz')
            ROOT.gPad.Update()

        if ireco == 'dsmu' and ir == 'rt1':
            c_dsmuon_rt1.cd()
            tt.Draw("(l1_matched_%s_pt-l1_pt)/l1_pt : l1_pt >> h_dsmuon_rt1"%(reco),"l1_matched_%s_pt>0 & abs(l1_pdgId) == 13 & abs(l1_eta)>%f &  abs(l1_eta)<%f & l1_matched_%s_charge == l1_charge & hnl_2d_disp>%d & hnl_2d_disp<%d" % (reco,etalow,etahigh,reco,rl,rh))
            tt.Draw("(l2_matched_%s_pt-l2_pt)/l2_pt : l2_pt >> h_sub"%(reco),"l2_matched_%s_pt>0 & abs(l2_pdgId) == 13 & abs(l2_eta)>%f &  abs(l2_eta)<%f & l2_matched_%s_charge == l2_charge & hnl_2d_disp>%d & hnl_2d_disp<%d" % (reco,etalow,etahigh,reco,rl,rh))
            h_dsmuon_rt1.Add(h_sub)
            h_sub.Reset()
            h_dsmuon_rt1.Draw('colz')
            ROOT.gPad.Update()

        if ireco == 'dsmu' and ir == 'rt2':
            c_dsmuon_rt2.cd()
            tt.Draw("(l1_matched_%s_pt-l1_pt)/l1_pt : l1_pt >> h_dsmuon_rt2"%(reco),"l1_matched_%s_pt>0 & abs(l1_pdgId) == 13 & abs(l1_eta)>%f &  abs(l1_eta)<%f & l1_matched_%s_charge == l1_charge & hnl_2d_disp>%d & hnl_2d_disp<%d" % (reco,etalow,etahigh,reco,rl,rh))
            tt.Draw("(l2_matched_%s_pt-l2_pt)/l2_pt : l2_pt >> h_sub"%(reco),"l2_matched_%s_pt>0 & abs(l2_pdgId) == 13 & abs(l2_eta)>%f &  abs(l2_eta)<%f & l2_matched_%s_charge == l2_charge & hnl_2d_disp>%d & hnl_2d_disp<%d" % (reco,etalow,etahigh,reco,rl,rh))
            h_dsmuon_rt2.Add(h_sub)
            h_sub.Reset()
            h_dsmuon_rt2.Draw('colz')
            ROOT.gPad.Update()

        if ireco == 'dsmu' and ir == 'r2':
            c_dsmuon_r2.cd()
            tt.Draw("(l1_matched_%s_pt-l1_pt)/l1_pt : l1_pt >> h_dsmuon_r2"%(reco),"l1_matched_%s_pt>0 & abs(l1_pdgId) == 13 & abs(l1_eta)>%f &  abs(l1_eta)<%f & l1_matched_%s_charge == l1_charge & hnl_2d_disp>%d & hnl_2d_disp<%d" % (reco,etalow,etahigh,reco,rl,rh))
            tt.Draw("(l2_matched_%s_pt-l2_pt)/l2_pt : l2_pt >> h_sub"%(reco),"l2_matched_%s_pt>0 & abs(l2_pdgId) == 13 & abs(l2_eta)>%f &  abs(l2_eta)<%f & l2_matched_%s_charge == l2_charge & hnl_2d_disp>%d & hnl_2d_disp<%d" % (reco,etalow,etahigh,reco,rl,rh))
            h_dsmuon_r2.Add(h_sub)
            h_sub.Reset()
            h_dsmuon_r2.Draw('colz')
            ROOT.gPad.Update()

        if ireco == 'dsmu' and ir == 'r3':
            c_dsmuon_r3.cd()
            tt.Draw("(l1_matched_%s_pt-l1_pt)/l1_pt : l1_pt >> h_dsmuon_r3"%(reco),"l1_matched_%s_pt>0 & abs(l1_pdgId) == 13 & abs(l1_eta)>%f &  abs(l1_eta)<%f & l1_matched_%s_charge == l1_charge & hnl_2d_disp>%d & hnl_2d_disp<%d" % (reco,etalow,etahigh,reco,rl,rh))
            tt.Draw("(l2_matched_%s_pt-l2_pt)/l2_pt : l2_pt >> h_subr3"%(reco),"l2_matched_%s_pt>0 & abs(l2_pdgId) == 13 & abs(l2_eta)>%f &  abs(l2_eta)<%f & l2_matched_%s_charge == l2_charge & hnl_2d_disp>%d & hnl_2d_disp<%d" % (reco,etalow,etahigh,reco,rl,rh))
            h_dsmuon_r3.Add(h_subr3)
            h_sub.Reset()
            h_dsmuon_r3.Draw('colz')
            ROOT.gPad.Update()

        if ireco == 'smu' and ir == 'r1':
            c_smuon_r1.cd()
            tt.Draw("(l1_matched_%s_pt-l1_pt)/l1_pt : l1_pt >> h_smuon_r1"%(reco),"l1_matched_%s_pt>0 & abs(l1_pdgId) == 13 & abs(l1_eta)>%f &  abs(l1_eta)<%f & l1_matched_%s_charge == l1_charge & hnl_2d_disp>%d & hnl_2d_disp<%d" % (reco,etalow,etahigh,reco,rl,rh))
            tt.Draw("(l2_matched_%s_pt-l2_pt)/l2_pt : l2_pt >> h_sub"%(reco),"l2_matched_%s_pt>0 & abs(l2_pdgId) == 13 & abs(l2_eta)>%f &  abs(l2_eta)<%f & l2_matched_%s_charge == l2_charge & hnl_2d_disp>%d & hnl_2d_disp<%d" % (reco,etalow,etahigh,reco,rl,rh))
            h_smuon_r1.Add(h_sub)
            h_sub.Reset()
            h_smuon_r1.Draw('colz')
            ROOT.gPad.Update()

        if ireco == 'smu' and ir == 'rt1':
            c_smuon_rt1.cd()
            tt.Draw("(l1_matched_%s_pt-l1_pt)/l1_pt : l1_pt >> h_smuon_rt1"%(reco),"l1_matched_%s_is_sa==1 & l1_matched_%s_pt>0 & abs(l1_pdgId) == 13 & abs(l1_eta)>%f &  abs(l1_eta)<%f & l1_matched_%s_charge == l1_charge & hnl_2d_disp>%d & hnl_2d_disp<%d" % (reco,reco,etalow,etahigh,reco,rl,rh))
            tt.Draw("(l2_matched_%s_pt-l2_pt)/l2_pt : l2_pt >> h_sub"%(reco),"l2_matched_%s_is_sa==1 & l2_matched_%s_pt>0 & abs(l2_pdgId) == 13 & abs(l2_eta)>%f &  abs(l2_eta)<%f & l2_matched_%s_charge == l2_charge & hnl_2d_disp>%d & hnl_2d_disp<%d" % (reco,reco,etalow,etahigh,reco,rl,rh))
            h_smuon_rt1.Add(h_sub)
            h_sub.Reset()
            h_smuon_rt1.Draw('colz')
            ROOT.gPad.Update()

        if ireco == 'smu' and ir == 'rt2':
            c_smuon_rt2.cd()
            tt.Draw("(l1_matched_%s_pt-l1_pt)/l1_pt : l1_pt >> h_smuon_rt2"%(reco),"l1_matched_%s_is_sa==1 & l1_matched_%s_pt>0 & abs(l1_pdgId) == 13 & abs(l1_eta)>%f &  abs(l1_eta)<%f & l1_matched_%s_charge == l1_charge & hnl_2d_disp>%d & hnl_2d_disp<%d" % (reco,reco,etalow,etahigh,reco,rl,rh))
            tt.Draw("(l2_matched_%s_pt-l2_pt)/l2_pt : l2_pt >> h_sub"%(reco),"l2_matched_%s_is_sa==1 & l2_matched_%s_pt>0 & abs(l2_pdgId) == 13 & abs(l2_eta)>%f &  abs(l2_eta)<%f & l2_matched_%s_charge == l2_charge & hnl_2d_disp>%d & hnl_2d_disp<%d" % (reco,reco,etalow,etahigh,reco,rl,rh))
            h_smuon_rt2.Add(h_sub)
            h_sub.Reset()
            h_smuon_rt2.Draw('colz')
            ROOT.gPad.Update()

        if ireco == 'smu' and ir == 'r2':
            c_smuon_r2.cd()
            tt.Draw("(l1_matched_%s_pt-l1_pt)/l1_pt : l1_pt >> h_smuon_r2"%(reco),"l1_matched_%s_pt>0 & abs(l1_pdgId) == 13 & abs(l1_eta)>%f &  abs(l1_eta)<%f & l1_matched_%s_charge == l1_charge & hnl_2d_disp>%d & hnl_2d_disp<%d" % (reco,etalow,etahigh,reco,rl,rh))
            tt.Draw("(l2_matched_%s_pt-l2_pt)/l2_pt : l2_pt >> h_sub"%(reco),"l2_matched_%s_pt>0 & abs(l2_pdgId) == 13 & abs(l2_eta)>%f &  abs(l2_eta)<%f & l2_matched_%s_charge == l2_charge & hnl_2d_disp>%d & hnl_2d_disp<%d" % (reco,etalow,etahigh,reco,rl,rh))
            h_smuon_r2.Add(h_sub)
            h_sub.Reset()
            h_smuon_r2.Draw('colz')
            ROOT.gPad.Update()

        if ireco == 'smu' and ir == 'r3':
            c_smuon_r3.cd()
            tt.Draw("(l1_matched_%s_pt-l1_pt)/l1_pt : l1_pt >> h_smuon_r3"%(reco),"l1_matched_%s_pt>0 & abs(l1_pdgId) == 13 & abs(l1_eta)>%f &  abs(l1_eta)<%f & l1_matched_%s_charge == l1_charge & hnl_2d_disp>%d & hnl_2d_disp<%d" % (reco,etalow,etahigh,reco,rl,rh))
            tt.Draw("(l2_matched_%s_pt-l2_pt)/l2_pt : l2_pt >> h_subr3"%(reco),"l2_matched_%s_pt>0 & abs(l2_pdgId) == 13 & abs(l2_eta)>%f &  abs(l2_eta)<%f & l2_matched_%s_charge == l2_charge & hnl_2d_disp>%d & hnl_2d_disp<%d" % (reco,etalow,etahigh,reco,rl,rh))
            h_smuon_r3.Add(h_subr3)
            h_subr3.Reset()
            h_smuon_r3.Draw('colz')
            ROOT.gPad.Update()





########################## 
# 7) Filling canvas(es)
##########################
print('adding final plots to canvas')
c_dsmuon_r1.cd()
g_ptres_dsMuon_r1.Draw('ep same')
h_dsmuon_r1.GetZaxis().SetTitle('Entries')
pf.showlogopreliminary('CMS','Simulation Preliminary')
ROOT.gPad.Update()
c_dsmuon_r1.SaveAs(output_dir + 'c_dsmuon_r1.root')
c_dsmuon_r1.SaveAs(output_dir + 'c_dsmuon_r1.pdf')

c_dsmuon_rt1.cd()
g_ptres_dsMuon_rt1.Draw('ep same')
h_dsmuon_rt1.GetZaxis().SetTitle('Entries')
pf.showlogopreliminary('CMS','Simulation Preliminary')
ROOT.gPad.Update()
c_dsmuon_rt1.SaveAs(output_dir + 'c_dsmuon_rt1.root')
c_dsmuon_rt1.SaveAs(output_dir + 'c_dsmuon_rt1.pdf')

c_dsmuon_rt2.cd()
g_ptres_dsMuon_rt2.Draw('ep same')
h_dsmuon_rt2.GetZaxis().SetTitle('Entries')
pf.showlogopreliminary('CMS','Simulation Preliminary')
ROOT.gPad.Update()
c_dsmuon_rt2.SaveAs(output_dir + 'c_dsmuon_rt2.root')
c_dsmuon_rt2.SaveAs(output_dir + 'c_dsmuon_rt2.pdf')

c_dsmuon_r2.cd()
g_ptres_dsMuon_r2.Draw('ep same')
h_dsmuon_r2.GetZaxis().SetTitle('Entries')
pf.showlogopreliminary('CMS','Simulation Preliminary')
ROOT.gPad.Update()
c_dsmuon_r2.SaveAs(output_dir + 'c_dsmuon_r2.root')
c_dsmuon_r2.SaveAs(output_dir + 'c_dsmuon_r2.pdf')

c_dsmuon_r3.cd()
g_ptres_dsMuon_r3.Draw('ep same')
h_dsmuon_r3.GetZaxis().SetTitle('Entries')
pf.showlogopreliminary('CMS','Simulation Preliminary')
ROOT.gPad.Update()
c_dsmuon_r3.SaveAs(output_dir + 'c_dsmuon_r3.root')
c_dsmuon_r3.SaveAs(output_dir + 'c_dsmuon_r3.pdf')

c_smuon_r1.cd()
g_ptres_sMuon_r1.Draw('ep same')
h_smuon_r1.GetZaxis().SetTitle('Entries')
pf.showlogopreliminary('CMS','Simulation Preliminary')
ROOT.gPad.Update()
c_smuon_r1.SaveAs(output_dir + 'c_smuon_r1.root')
c_smuon_r1.SaveAs(output_dir + 'c_smuon_r1.pdf')

c_smuon_rt1.cd()
g_ptres_sMuon_rt1.Draw('ep same')
h_smuon_rt1.GetZaxis().SetTitle('Entries')
pf.showlogopreliminary('CMS','Simulation Preliminary')
ROOT.gPad.Update()
c_smuon_rt1.SaveAs(output_dir + 'c_smuon_rt1.root')
c_smuon_rt1.SaveAs(output_dir + 'c_smuon_rt1.pdf')

c_smuon_rt2.cd()
g_ptres_sMuon_rt2.Draw('ep same')
h_smuon_rt2.GetZaxis().SetTitle('Entries')
pf.showlogopreliminary('CMS','Simulation Preliminary')
ROOT.gPad.Update()
c_smuon_rt2.SaveAs(output_dir + 'c_smuon_rt2.root')
c_smuon_rt2.SaveAs(output_dir + 'c_smuon_rt2.pdf')

c_smuon_r2.cd()
g_ptres_sMuon_r2.Draw('ep same')
h_smuon_r2.GetZaxis().SetTitle('Entries')
pf.showlogopreliminary('CMS','Simulation Preliminary')
ROOT.gPad.Update()
c_smuon_r2.SaveAs(output_dir + 'c_smuon_r2.root')
c_smuon_r2.SaveAs(output_dir + 'c_smuon_r2.pdf')

c_smuon_r3.cd()
g_ptres_sMuon_r3.Draw('ep same')
h_smuon_r3.GetZaxis().SetTitle('Entries')
pf.showlogopreliminary('CMS','Simulation Preliminary')
ROOT.gPad.Update()
c_smuon_r3.SaveAs(output_dir + 'c_smuon_r3.root')
c_smuon_r3.SaveAs(output_dir + 'c_smuon_r3.pdf')


c_ptres_r1.cd()
mg_r1 = ROOT.TMultiGraph('mg_r1','')
mg_r1.Add(g_ptres_dsMuon_r1)
mg_r1.Add(g_ptres_sMuon_r1 )
mg_r1.Draw('AP')
mg_r1.GetXaxis().SetTitle('p_{T}[GeV]')
mg_r1.GetYaxis().SetTitle('#Delta (p_{T})/(p_{T})')
mg_r1.GetXaxis().SetTitleOffset(1.3)
mg_r1.GetYaxis().SetTitleOffset(1.4)
mg_r1.GetXaxis().SetRangeUser(0.,50.)
mg_r1.GetYaxis().SetRangeUser(-1.0,1.0)
mg_r1.SetTitle('')

c_ptres_rt1.cd()
mg_rt1 = ROOT.TMultiGraph('mg_rt1','')
mg_rt1.Add(g_ptres_dsMuon_rt1)
mg_rt1.Add(g_ptres_sMuon_rt1 )
mg_rt1.Draw('AP')
mg_rt1.GetXaxis().SetTitle('p_{T}[GeV]')
mg_rt1.GetYaxis().SetTitle('#Delta (p_{T})/(p_{T})')
mg_rt1.GetXaxis().SetTitleOffset(1.3)
mg_rt1.GetYaxis().SetTitleOffset(1.4)
mg_rt1.GetXaxis().SetRangeUser(0.,50.)
mg_rt1.GetYaxis().SetRangeUser(-1.0,1.0)
mg_rt1.SetTitle('')

c_ptres_rt2.cd()
mg_rt2 = ROOT.TMultiGraph('mg_rt2','')
mg_rt2.Add(g_ptres_dsMuon_rt2)
mg_rt2.Add(g_ptres_sMuon_rt2 )
mg_rt2.Draw('AP')
mg_rt2.GetXaxis().SetTitle('p_{T}[GeV]')
mg_rt2.GetYaxis().SetTitle('#Delta (p_{T})/(p_{T})')
mg_rt2.GetXaxis().SetTitleOffset(1.3)
mg_rt2.GetYaxis().SetTitleOffset(1.4)
mg_rt2.GetXaxis().SetRangeUser(0.,50.)
mg_rt2.GetYaxis().SetRangeUser(-1.0,1.0)
mg_rt2.SetTitle('')

c_ptres_r2.cd()
mg_r2 = ROOT.TMultiGraph('mg_r2','')
mg_r2.Add(g_ptres_dsMuon_r2)
mg_r2.Add(g_ptres_sMuon_r2 )
mg_r2.Draw('AP')
mg_r2.GetXaxis().SetTitle('p_{T}[GeV]')
mg_r2.GetYaxis().SetTitle('#Delta (p_{T})/(p_{T})')
mg_r2.GetXaxis().SetTitleOffset(1.3)
mg_r2.GetYaxis().SetTitleOffset(1.4)
mg_r2.GetXaxis().SetRangeUser(0.,50.)
mg_r2.GetYaxis().SetRangeUser(-1.0,1.0)
mg_r2.SetTitle('')

c_ptres_r3.cd()
mg_r3 = ROOT.TMultiGraph('mg_r3','')
mg_r3.Add(g_ptres_dsMuon_r3)
mg_r3.Add(g_ptres_sMuon_r3 )
mg_r3.Draw('AP')
mg_r3.GetXaxis().SetTitle('p_{T}[GeV]')
mg_r3.GetYaxis().SetTitle('#Delta (p_{T})/(p_{T})')
mg_r3.GetXaxis().SetTitleOffset(1.3)
mg_r3.GetYaxis().SetTitleOffset(1.4)
mg_r3.GetXaxis().SetRangeUser(0.,50.)
mg_r3.GetYaxis().SetRangeUser(-1.0,1.0)
mg_r3.SetTitle('')

c_ptres_sub.cd()
h_ptres_sub.Draw('hist pe')



########################## 
# 8) Draw Legend(s)
##########################
print('drawing the legend')

c_ptres_r1.cd()
leg1 = ROOT.TLegend(.16,.16,.4,.3)
leg1.SetBorderSize(0)
leg1.SetFillColor(ROOT.kWhite)
leg1.SetFillStyle(0)
leg1.SetTextFont(42)
leg1.SetTextSize(0.03)
leg1.AddEntry(g_ptres_dsMuon_r1, 'dSA#mu_r1'            ,'EP')
leg1.AddEntry(g_ptres_sMuon_r1 , '  S#mu_r1'            ,'EP')
leg1.Draw('apez same')

c_ptres_rt1.cd()
legt = ROOT.TLegend(.16,.16,.4,.3)
legt.SetBorderSize(0)
legt.SetFillColor(ROOT.kWhite)
legt.SetFillStyle(0)
legt.SetTextFont(42)
legt.SetTextSize(0.03)
legt.AddEntry(g_ptres_dsMuon_rt1, 'dSA#mu_rt1'            ,'EP')
legt.AddEntry(g_ptres_sMuon_rt1 , '  SA#mu_rt1'            ,'EP')
legt.Draw('apez same')

c_ptres_rt2.cd()
legt = ROOT.TLegend(.16,.16,.4,.3)
legt.SetBorderSize(0)
legt.SetFillColor(ROOT.kWhite)
legt.SetFillStyle(0)
legt.SetTextFont(42)
legt.SetTextSize(0.03)
legt.AddEntry(g_ptres_dsMuon_rt2, 'dSA#mu_rt2'            ,'EP')
legt.AddEntry(g_ptres_sMuon_rt2 , '  SA#mu_rt2'            ,'EP')
legt.Draw('apez same')

c_ptres_r2.cd()
leg2 = ROOT.TLegend(.16,.16,.4,.3)
leg2.SetBorderSize(0)
leg2.SetFillColor(ROOT.kWhite)
leg2.SetFillStyle(0)
leg2.SetTextFont(42)
leg2.SetTextSize(0.03)
leg2.AddEntry(g_ptres_dsMuon_r2, 'dSA#mu_r2'            ,'EP')
leg2.AddEntry(g_ptres_sMuon_r2 , '  S#mu_r2'            ,'EP')
leg2.Draw('apez same')

c_ptres_r3.cd()
leg3 = ROOT.TLegend(.16,.16,.4,.3)
leg3.SetBorderSize(0)
leg3.SetFillColor(ROOT.kWhite)
leg3.SetFillStyle(0)
leg3.SetTextFont(42)
leg3.SetTextSize(0.03)
leg3.AddEntry(g_ptres_dsMuon_r3, 'dSA#mu_r3'            ,'EP')
leg3.AddEntry(g_ptres_sMuon_r3 , '  S#mu_r3'            ,'EP')
leg3.Draw('apez same')



########################## 
# 9) Final Update(s)
##########################
print('finishing...')
c_ptres_sub.cd()
ROOT.gPad.Update()

for cc in [c_ptres_r1,c_ptres_rt1,c_ptres_rt2,c_ptres_r2,c_ptres_r3]:
    cc.cd()
    ROOT.gPad.Update()

    if cc == c_ptres_r1:
        pf.showlogopreliminary('CMS','Simulation Preliminary')
        cc.SaveAs(output_dir + 'c_ptres_r1.root')
        cc.SaveAs(output_dir + 'c_ptres_r1.pdf')
    if cc == c_ptres_rt1:
        pf.showlogopreliminary('CMS','Simulation Preliminary')
        cc.SaveAs(output_dir + 'c_ptres_rt1.root')
        cc.SaveAs(output_dir + 'c_ptres_rt1.pdf')
    if cc == c_ptres_rt2:
        pf.showlogopreliminary('CMS','Simulation Preliminary')
        cc.SaveAs(output_dir + 'c_ptres_rt2.root')
        cc.SaveAs(output_dir + 'c_ptres_rt2.pdf')
    if cc == c_ptres_r2:
        pf.showlogopreliminary('CMS','Simulation Preliminary')
        cc.SaveAs(output_dir + 'c_ptres_r2.root')
        cc.SaveAs(output_dir + 'c_ptres_r2.pdf')
    if cc == c_ptres_r3:
        pf.showlogopreliminary('CMS','Simulation Preliminary')
        cc.SaveAs(output_dir + 'c_ptres_r3.root')
        cc.SaveAs(output_dir + 'c_ptres_r3.pdf')






