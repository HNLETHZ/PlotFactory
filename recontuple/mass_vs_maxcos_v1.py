import ROOT as rt
import numpy as np
import plotfactory as pf
import ntup_dir as nt
from glob import glob
import sys
from pdb import set_trace
from os.path import normpath, basename
####################################################################################################
outdir = '/afs/cern.ch/work/v/vstampf/plots/recontuple/'
indir = nt.getntupdir()
####################################################################################################
ntdr = basename(normpath(indir))
####################################################################################################
masses = ['10','1','2','2p1','2p5','3','4','5','6','7','8','9']
masses_num = [10,1,2,2.1,2.5,3,4,5,6,7,8,9]
chain = []
all_files = []
for s in masses:
    chain.append( rt.TChain('tree') )
    all_files.append( glob(indir + 'HN3L_M_%s*/HNLTreeProducerSignal/tree.root'%s) ) 

for i in all_files[0]: all_files[1].remove(i)

for i in all_files[3]+all_files[4]: all_files[2].remove(i)

for i in range(len(masses)):
    for sample in all_files[i]: 
        chain[i].Add(sample)
#set_trace()
####################################################################################################
####################################################################################################
pf.setpfstyle()
####################################################################################################
####################################################################################################
####################################################################################################
b_masses = np.arange(0.,11,0.1)
####################################################################################################
####################################################################################################
####################################################################################################
h_masses_eff_denom = rt.TH1F('masses_eff_denom','masses_eff_denom',len(b_masses)-1,b_masses)
h_masses_eff_numer = rt.TH1F('masses_eff_numer','masses_eff_numer',len(b_masses)-1,b_masses)
h_masses_pur_denom = rt.TH1F('masses_pur_denom','masses_pur_denom',len(b_masses)-1,b_masses)
h_masses_pur_numer = rt.TH1F('masses_pur_numer','masses_pur_numer',len(b_masses)-1,b_masses)
####################################################################################################
####################################################################################################
####################################################################################################
eff = []
pur = []
for i in range(1,len(masses)+1):
    eff_numer = chain[i-1].GetEntries('flag_IsThereTHEDimuon == 1 & flag_matchedHNLMaxCosBPA == 1')
    eff_denom = chain[i-1].GetEntries('flag_IsThereTHEDimuon == 1')

    pur_numer = chain[i-1].GetEntries('flag_matchedHNLMaxCosBPA == 1')
    pur_denom = chain[i-1].GetEntries('flag_matchedHNLMaxCosBPA == 1') + chain[i-1].GetEntries('flag_matchedHNLMaxCosBPA == 0')

    j = int(10*masses_num[i-1]+1)

    
    if eff_denom != 0:  #set_trace()
        eff.append((float(eff_numer)/eff_denom))
        h_masses_eff_denom.SetBinContent(j,eff_denom)
        h_masses_eff_numer.SetBinContent(j,eff_numer)
    else: eff.append(0)

    if pur_denom != 0:
        h_masses_pur_denom.SetBinContent(j,pur_denom)
        h_masses_pur_numer.SetBinContent(j,pur_numer)
        pur.append((float(pur_numer)/pur_denom))
    else: pur.append(0)
 
    print(j, eff[i-1], pur[i-1], masses[i-1])
 #   print(j, eff, pur, masses)
####################################################################################################
####################################################################################################
####################################################################################################
#h_masses_eff_numer.Draw('apez')
#h_masses_eff_denom.Draw('apez')
#h_masses_pur_numer.Draw('apez')
#h_masses_pur_denom.Draw('apez')
h_masses_pur_numer.Divide(h_masses_pur_denom)
h_masses_eff_numer.Divide(h_masses_eff_denom)
####################################################################################################
####################################################################################################
hlist = [h_masses_pur_numer,h_masses_eff_numer]
####################################################################################################
####################################################################################################
for h in hlist:
    h.GetXaxis().SetTitle('HNL Mass [GeV]')
    h.SetMarkerColor(rt.kBlue+2)
    h.SetTitle('Selection: MaxCosBPA')
h_masses_eff_numer.SetAxisRange(0.95,1.01,'Y')
####################################################################################################
####################################################################################################
####################################################################################################
c_masses_eff = rt.TCanvas('masses_eff','masses_eff')
c_masses_pur = rt.TCanvas('masses_pur','masses_pur')
####################################################################################################
####################################################################################################
clist = [c_masses_pur,c_masses_pur]
####################################################################################################
####################################################################################################
c_masses_eff .cd()
h_masses_eff_numer.Draw('ep')
####################################################################################################
####################################################################################################
c_masses_pur.cd()
h_masses_pur_numer.Draw('ep')
####################################################################################################
####################################################################################################
for c in clist:
    c.cd()
    pf.showlogoprelimsim('CMS')
#    rt.gStyle.SetOptStat()
    c.Modified()
    c.Update()
    c.SaveAs(outdir+c.GetTitle()+'_'+ntdr+'.root')
    c.SaveAs(outdir+c.GetTitle()+'_'+ntdr+'.png')
