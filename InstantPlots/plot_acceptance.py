import ROOT as rt
import plotfactory as pf
import numpy as np
import sys

pf.setpfstyle()

######################################### 
# Make Chain from selection of samples
#########################################
# Get the option from the command line, using 'True' as a fallback.
if len(sys.argv)>1 and sys.argv[1] == 'test':
    setting = False
    print('Using a selection of samples')
else:
    setting = True
    print('Using all samples')

tt = pf.makechain(setting)

nentries = tt.GetEntries()
print('number of events: %d'%(nentries))


######################################### 
# Make Canvas and Histograms
#########################################
c_acc1 = rt.TCanvas('c_acc1','c_acc2')

binsx = np.arange(0.,60.,2.)

h_denom = rt.TH1F('h_denom','',len(binsx)-1,binsx)
h_allmass = rt.TH1F('h_allmass','',len(binsx)-1,binsx)
h_allmass.SetTitle(';promt electron pt cut [GeV]; acceptance')
h_allmass.GetYaxis().SetRangeUser(0.,1.04)
h_allmass.SetLineColor   (rt.kBlack)
h_allmass.SetMarkerColor (rt.kBlack)

h_denom_0_1 = rt.TH1F('h_denom_0_1','',len(binsx)-1,binsx)
h_0_1 = rt.TH1F('h_0_1','',len(binsx)-1,binsx)
h_0_1.SetTitle(';promt electron pt cut [GeV]; acceptance')
h_0_1.GetYaxis().SetRangeUser(0.,1.04)
h_0_1.SetLineColor   (rt.kRed)
h_0_1.SetMarkerColor (rt.kRed)

h_denom_1_2 = rt.TH1F('h_denom_1_2','',len(binsx)-1,binsx)
h_1_2 = rt.TH1F('h_1_2','',len(binsx)-1,binsx)
h_1_2.SetTitle(';promt electron pt cut [GeV]; acceptance')
h_1_2.GetYaxis().SetRangeUser(0.,1.04)
h_1_2.SetLineColor   (rt.kBlue)
h_1_2.SetMarkerColor (rt.kBlue)

h_denom_2_3 = rt.TH1F('h_denom_2_3','',len(binsx)-1,binsx)
h_2_3 = rt.TH1F('h_2_3','',len(binsx)-1,binsx)
h_2_3.SetTitle(';promt electron pt cut [GeV]; acceptance')
h_2_3.GetYaxis().SetRangeUser(0.,1.04)
h_2_3.SetLineColor   (rt.kGreen)
h_2_3.SetMarkerColor (rt.kGreen)

h_denom_3_10 = rt.TH1F('h_denom_3_10','',len(binsx)-1,binsx)
h_3_10 = rt.TH1F('h_3_10','',len(binsx)-1,binsx)
h_3_10.SetTitle(';promt electron pt cut [GeV]; acceptance')
h_3_10.GetYaxis().SetRangeUser(0.,1.04)
h_3_10.SetLineColor   (rt.kMagenta)
h_3_10.SetMarkerColor (rt.kMagenta)

sel0 = 'abs(l0_pdgId)==11 & is_in_acc==1'
n_sel0 = tt.GetEntries(sel0)

tt.Draw('l0_pt>>h_denom',sel0)
tt.Draw('l0_pt>>h_denom_0_1',sel0 +' & hnl_hn_m <= 1')
tt.Draw('l0_pt>>h_denom_1_2',sel0 +' & hnl_hn_m > 1 & hnl_hn_m <= 2')
tt.Draw('l0_pt>>h_denom_2_3',sel0 +' & hnl_hn_m > 2 & hnl_hn_m <= 3')
tt.Draw('l0_pt>>h_denom_3_10',sel0 +' & hnl_hn_m > 3')

for ibin in range(len(binsx)):
    ipt = binsx[ibin]
    # iacc = float(h_denom.Integral(ibin,len(binsx)))/float(h_denom.Integral()) 
    int_tot = float(h_denom.Integral(0,len(binsx)))
    int_tot_0_1= float(h_denom_0_1.Integral(0,len(binsx)))
    int_tot_1_2= float(h_denom_1_2.Integral(0,len(binsx)))
    int_tot_2_3= float(h_denom_2_3.Integral(0,len(binsx)))
    int_tot_3_10= float(h_denom_3_10.Integral(0,len(binsx)))

    int_sub = float(h_denom.Integral(ibin,len(binsx)))
    int_sub_0_1= float(h_denom_0_1.Integral(ibin,len(binsx)))
    int_sub_1_2= float(h_denom_1_2.Integral(ibin,len(binsx)))
    int_sub_2_3= float(h_denom_2_3.Integral(ibin,len(binsx)))
    int_sub_3_10= float(h_denom_3_10.Integral(ibin,len(binsx)))

    iacc = int_sub/int_tot
    iacc_0_1=  int_sub_0_1/int_tot_0_1
    iacc_1_2=  int_sub_1_2/int_tot_1_2
    iacc_2_3=  int_sub_2_3/int_tot_2_3
    iacc_3_10= int_sub_3_10/int_tot_3_10

    # print('%d    %d    %d    %d    %.2f'%(ibin,ipt,int_tot,int_sub,iacc))
    h_allmass.SetBinContent(ibin,iacc)
    h_0_1.SetBinContent(ibin,iacc_0_1)
    h_1_2.SetBinContent(ibin,iacc_1_2)
    h_2_3.SetBinContent(ibin,iacc_2_3)
    h_3_10.SetBinContent(ibin,iacc_3_10)

h_allmass.Draw('EP')
h_0_1 .Draw('same EP')
h_1_2 .Draw('same EP')
h_2_3 .Draw('same EP')
h_3_10.Draw('same EP')

l_acc = rt.TLegend(.6,.7,.8,.88)
l_acc.AddEntry(h_allmass,'all mass','EP')
l_acc.AddEntry(h_0_1, '0<m<1','EP')
l_acc.AddEntry(h_1_2, '1<m<2','EP')
l_acc.AddEntry(h_2_3, '2<m<3','EP')
l_acc.AddEntry(h_3_10,'3<m','EP')
l_acc.Draw('apez same')

pf.showlogopreliminary('CMS','Simulation Preliminary')
c_acc1.Update()
