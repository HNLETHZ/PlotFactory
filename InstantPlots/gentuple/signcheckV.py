import ROOT as rt
import numpy as np
import plotfactory as pf
import sys
from pdb import set_trace

output_dir = '/afs/cern.ch/work/v/vstampf/plots/candidates/gentuple/' 

fout = rt.TFile(output_dir+'signcheckV.root', 'recreate')

######################################### 
# Make Chain from selection of samples
#########################################

# Get the option from the command line, using 'True' as a fallback.

ntup_dir = '/afs/cern.ch/work/v/vstampf/ntuples/gen/'

samples = ['HN3L_M_1_V_0p00282842712475_e_onshell',    
'HN3L_M_1_V_0p00316227766017_e_onshell',    
'HN3L_M_1_V_0p004472135955_e_onshell',      
'HN3L_M_1_V_0p004472135955_mu_onshell',     
'HN3L_M_1_V_0p00547722557505_e_onshell',    
'HN3L_M_1_V_0p00547722557505_mu_onshell',   
'HN3L_M_1_V_0p00707106781187_e_onshell',    
'HN3L_M_1_V_0p00707106781187_mu_onshell',   
'HN3L_M_1_V_0p00836660026534_e_onshell',    
'HN3L_M_1_V_0p00836660026534_mu_onshell',   
'HN3L_M_1_V_0p59587618054_e_onshell',       
'HN3L_M_1_V_0p59587618054_mu_onshell',      
'HN3L_M_2_V_0p00244948974278_e_onshell',    
'HN3L_M_2_V_0p00244948974278_mu_onshell',   
'HN3L_M_2_V_0p01_e_onshell',                
'HN3L_M_2_V_0p01_mu_onshell',               
'HN3L_M_2p1_V_0p00244948974278_e_onshell',  
'HN3L_M_2p1_V_0p00244948974278_mu_onshell', 
'HN3L_M_2p1_V_0p00282842712475_e_onshell',  
'HN3L_M_2p1_V_0p00282842712475_mu_onshell', 
'HN3L_M_2p1_V_0p00316227766017_e_onshell',  
'HN3L_M_2p1_V_0p00316227766017_mu_onshell', 
'HN3L_M_2p1_V_0p004472135955_e_onshell',    
'HN3L_M_2p1_V_0p004472135955_mu_onshell',   
'HN3L_M_2p1_V_0p00547722557505_e_onshell',  
'HN3L_M_2p1_V_0p00547722557505_mu_onshell', 
'HN3L_M_2p1_V_0p00707106781187_e_onshell',  
'HN3L_M_2p1_V_0p00707106781187_mu_onshell', 
'HN3L_M_2p1_V_0p00836660026534_e_onshell',  
'HN3L_M_2p1_V_0p00836660026534_mu_onshell', 
'HN3L_M_2p1_V_0p01_e_onshell',              
'HN3L_M_2p1_V_0p01_mu_onshell',             
'HN3L_M_2p1_V_0p0141421356237_e_onshell',   
'HN3L_M_2p1_V_0p0141421356237_mu_onshell',  
'HN3L_M_2p1_V_0p0173205080757_e_onshell',   
'HN3L_M_2p1_V_0p0173205080757_mu_onshell',  
'HN3L_M_2p5_V_0p004472135955_e_onshell',    
'HN3L_M_2p5_V_0p004472135955_mu_onshell',   
'HN3L_M_2p5_V_0p00547722557505_e_onshell',  
'HN3L_M_2p5_V_0p00547722557505_mu_onshell', 
'HN3L_M_2p5_V_0p00707106781187_e_onshell',  
'HN3L_M_2p5_V_0p00707106781187_mu_onshell', 
'HN3L_M_2p5_V_0p00836660026534_e_onshell',  
'HN3L_M_2p5_V_0p00836660026534_mu_onshell', 
'HN3L_M_2p5_V_0p01_e_onshell',              
'HN3L_M_2p5_V_0p01_mu_onshell',             
'HN3L_M_2p5_V_0p0141421356237_e_onshell',   
'HN3L_M_2p5_V_0p0141421356237_mu_onshell',  
'HN3L_M_2p5_V_0p0173205080757_e_onshell',   
'HN3L_M_2p5_V_0p0173205080757_mu_onshell',  
'HN3L_M_3_V_0p00244948974278_e_onshell',    
'HN3L_M_3_V_0p00244948974278_mu_onshell',   
'HN3L_M_3_V_0p00282842712475_e_onshell',    
'HN3L_M_3_V_0p00282842712475_mu_onshell',   
'HN3L_M_3_V_0p00316227766017_e_onshell',    
'HN3L_M_3_V_0p00316227766017_mu_onshell',   
'HN3L_M_3_V_0p004472135955_e_onshell',      
'HN3L_M_3_V_0p004472135955_mu_onshell',     
'HN3L_M_3_V_0p00547722557505_e_onshell',    
'HN3L_M_3_V_0p00547722557505_mu_onshell',   
'HN3L_M_3_V_0p00707106781187_e_onshell',    
'HN3L_M_3_V_0p00707106781187_mu_onshell',   
'HN3L_M_3_V_0p00836660026534_e_onshell',    
'HN3L_M_3_V_0p00836660026534_mu_onshell',   
'HN3L_M_3_V_0p01_e_onshell',                
'HN3L_M_3_V_0p01_mu_onshell',               
'HN3L_M_3_V_0p0141421356237_mu_onshell',    
'HN3L_M_3_V_0p0173205080757_e_onshell',     
'HN3L_M_3_V_0p0173205080757_mu_onshell',    
'HN3L_M_3_V_0p03823254899_e_onshell',       
'HN3L_M_3_V_0p03823254899_mu_onshell',      
'HN3L_M_4_V_0p00244948974278_e_onshell',    
'HN3L_M_4_V_0p00244948974278_mu_onshell',   
'HN3L_M_4_V_0p00282842712475_e_onshell',    
'HN3L_M_4_V_0p00282842712475_mu_onshell',   
'HN3L_M_4_V_0p00316227766017_e_onshell',    
'HN3L_M_4_V_0p00316227766017_mu_onshell',   
'HN3L_M_4_V_0p004472135955_e_onshell',      
'HN3L_M_4_V_0p004472135955_mu_onshell',     
'HN3L_M_4_V_0p00547722557505_e_onshell',    
'HN3L_M_4_V_0p00547722557505_mu_onshell',   
'HN3L_M_4_V_0p00707106781187_e_onshell',    
'HN3L_M_4_V_0p00707106781187_mu_onshell',   
'HN3L_M_4_V_0p00836660026534_2l_onshell',   
'HN3L_M_4_V_0p00836660026534_e_onshell',    
'HN3L_M_4_V_0p00836660026534_mu_onshell',   
'HN3L_M_4_V_0p01_e_onshell',                
'HN3L_M_4_V_0p01_mu_onshell',               
'HN3L_M_4_V_0p0141421356237_e_onshell',     
'HN3L_M_4_V_0p0141421356237_mu_onshell',    
'HN3L_M_4_V_0p01860689426_e_onshell',       
'HN3L_M_4_V_0p01860689426_mu_onshell',      
'HN3L_M_5_V_0p00244948974278_e_onshell',    
'HN3L_M_5_V_0p00244948974278_mu_onshell',   
'HN3L_M_5_V_0p00282842712475_e_onshell',    
'HN3L_M_5_V_0p00282842712475_mu_onshell',   
'HN3L_M_5_V_0p00316227766017_e_onshell',    
'HN3L_M_5_V_0p00316227766017_mu_onshell',   
'HN3L_M_5_V_0p004472135955_e_onshell',      
'HN3L_M_5_V_0p004472135955_mu_onshell',     
'HN3L_M_5_V_0p00547722557505_e_onshell',    
'HN3L_M_5_V_0p00547722557505_mu_onshell',   
'HN3L_M_5_V_0p00707106781187_e_onshell',    
'HN3L_M_5_V_0p00707106781187_mu_onshell',   
'HN3L_M_5_V_0p00836660026534_e_onshell',    
'HN3L_M_5_V_0p00836660026534_mu_onshell',   
'HN3L_M_5_V_0p01_e_onshell',                
'HN3L_M_5_V_0p01_mu_onshell',               
'HN3L_M_5_V_0p01065503443_e_onshell',       
'HN3L_M_5_V_0p01065503443_mu_onshell',      
'HN3L_M_6_V_0p001479_e_onshell',            
'HN3L_M_6_V_0p001479_mu_onshell',           
'HN3L_M_6_V_0p00244948974278_e_onshell',    
'HN3L_M_6_V_0p00244948974278_mu_onshell',   
'HN3L_M_6_V_0p00282842712475_e_onshell',    
'HN3L_M_6_V_0p00282842712475_mu_onshell',   
'HN3L_M_6_V_0p00316227766017_e_onshell',    
'HN3L_M_6_V_0p00316227766017_mu_onshell',   
'HN3L_M_6_V_0p004472135955_e_onshell',      
'HN3L_M_6_V_0p004472135955_mu_onshell',     
'HN3L_M_6_V_0p00547722557505_e_onshell',    
'HN3L_M_6_V_0p00547722557505_mu_onshell',   
'HN3L_M_6_V_0p00675244664_e_onshell',       
'HN3L_M_6_V_0p00675244664_e',               
'HN3L_M_6_V_0p00675244664_mu_onshell',      
'HN3L_M_6_V_0p00675244664_mu',              
'HN3L_M_6_V_0p00707106781187_e_onshell',    
'HN3L_M_6_V_0p00707106781187_mu_onshell',   
'HN3L_M_6_V_0p00836660026534_e_onshell',    
'HN3L_M_6_V_0p00836660026534_mu_onshell',   
'HN3L_M_7_V_0p002174_e_onshell',            
'HN3L_M_7_V_0p002296_mu_onshell',           
'HN3L_M_7_V_0p00244948974278_e_onshell',    
'HN3L_M_7_V_0p00244948974278_mu_onshell',   
'HN3L_M_7_V_0p00282842712475_e_onshell',    
'HN3L_M_7_V_0p00282842712475_mu_onshell',   
'HN3L_M_7_V_0p00316227766017_e_onshell',    
'HN3L_M_7_V_0p00316227766017_mu_onshell',   
'HN3L_M_7_V_0p004472135955_e_onshell',      
'HN3L_M_7_V_0p004472135955_mu_onshell',     
'HN3L_M_7_V_0p00459211224_e_onshell',       
'HN3L_M_7_V_0p00459211224_e',               
'HN3L_M_7_V_0p00459211224_mu_onshell',      
'HN3L_M_7_V_0p00459211224_mu',              
'HN3L_M_7_V_0p00547722557505_e_onshell',    
'HN3L_M_7_V_0p00547722557505_mu_onshell',   
'HN3L_M_7_V_0p00707106781187_e_onshell',    
'HN3L_M_7_V_0p00707106781187_mu_onshell',   
'HN3L_M_8_V_0p00244948974278_e_onshell',    
'HN3L_M_8_V_0p00244948974278_mu_onshell',   
'HN3L_M_8_V_0p00282842712475_e_onshell',    
'HN3L_M_8_V_0p00282842712475_mu_onshell',   
'HN3L_M_8_V_0p00316227766017_e_onshell',    
'HN3L_M_8_V_0p00316227766017_mu_onshell',   
'HN3L_M_8_V_0p004472135955_e_onshell',      
'HN3L_M_8_V_0p004472135955_mu_onshell',     
'HN3L_M_8_V_0p00547722557505_e_onshell',    
'HN3L_M_8_V_0p00547722557505_mu_onshell',   
'HN3L_M_9_V_0p00244948974278_e_onshell',    
'HN3L_M_9_V_0p00244948974278_mu_onshell',   
'HN3L_M_9_V_0p00282842712475_e_onshell',    
'HN3L_M_9_V_0p00282842712475_mu_onshell',   
'HN3L_M_9_V_0p00316227766017_e_onshell',    
'HN3L_M_9_V_0p00316227766017_mu_onshell',   
'HN3L_M_9_V_0p004472135955_e_onshell',      
'HN3L_M_9_V_0p004472135955_mu_onshell',     
'HN3L_M_10_V_0p00244948974278_e_onshell',   
'HN3L_M_10_V_0p00244948974278_mu_onshell',  
'HN3L_M_10_V_0p00282842712475_e_onshell',   
'HN3L_M_10_V_0p00282842712475_mu_onshell',  
'HN3L_M_10_V_0p00316227766017_e_onshell',   
'HN3L_M_10_V_0p00316227766017_mu_onshell',  
'HN3L_M_10_V_0p004472135955_e_onshell',     
'HN3L_M_10_V_0p004472135955_mu_onshell',    
'HN3L_M_10_V_0p01_e_onshell',               
'HN3L_M_10_V_0p01_mu_onshell',]              
    
tt_V1 = rt.TChain('tree')
tt_V2 = rt.TChain('tree')
tt_V3 = rt.TChain('tree')

V00 = np.array([])
for j in range(10):
   V00 = np.append(V00, [ss for ss in samples if '0p00%s'%j in ss])
V0 = np.array([])
for j in range(10):
   V0 = np.append(V0, [ss for ss in samples if ('0p0%s'%j in ss and ss not in V00)])
VR = np.array([])
VR = np.append(VR, [ss for ss in samples if (ss not in V00 and ss not in V0)])

V = np.array([])
V = np.append(V,V00)
V = np.append(V,V0)
V = np.append(V,VR)


for sig in range(len(V)/3-1):
   tt_V1.Add(ntup_dir + '%s/HNLGenTreeProducer/tree.root'%V[sig])
for sig in range(len(V)/3-1,2*len(V)/3-1,1):
   tt_V2.Add(ntup_dir + '%s/HNLGenTreeProducer/tree.root'%V[sig])
for sig in range(2*len(V)/3-1,len(V)-1,1):
   tt_V3.Add(ntup_dir + '%s/HNLGenTreeProducer/tree.root'%V[sig])

n_entries_V1 = tt_V1.GetEntries()
n_entries_V2 = tt_V2.GetEntries()
n_entries_V3 = tt_V3.GetEntries()

print('number of total entries in chain: 1: %d, 2: %d, 3: %d'%(n_entries_V1,n_entries_V2,n_entries_V3))
pf.setpfstyle()

c_V1_l01 = rt.TCanvas('signs_V1_l01','signs_V1_l01')
c_V1_l12 = rt.TCanvas('signs_V1_l12','signs_V1_l12')
c_V1_l02 = rt.TCanvas('signs_V1_l02','signs_V1_l02')
c_V2_l01 = rt.TCanvas('signs_V2_l01','signs_V2_l01')
c_V2_l12 = rt.TCanvas('signs_V2_l12','signs_V2_l12')
c_V2_l02 = rt.TCanvas('signs_V2_l02','signs_V2_l02')
c_V3_l01 = rt.TCanvas('signs_V3_l01','signs_V3_l01')
c_V3_l12 = rt.TCanvas('signs_V3_l12','signs_V3_l12')
c_V3_l02 = rt.TCanvas('signs_V3_l02','signs_V3_l02')

b_signs = np.arange(-1.,3,1.5)

h_V1_l01 = rt.TH2F('V1_l01','V1_l01',len(b_signs)-1,b_signs,len(b_signs)-1,b_signs)
h_V1_l12 = rt.TH2F('V1_l12','V1_l12',len(b_signs)-1,b_signs,len(b_signs)-1,b_signs)
h_V1_l02 = rt.TH2F('V1_l02','V1_l02',len(b_signs)-1,b_signs,len(b_signs)-1,b_signs)
h_V2_l01 = rt.TH2F('V2_l01','V2_l01',len(b_signs)-1,b_signs,len(b_signs)-1,b_signs)
h_V2_l12 = rt.TH2F('V2_l12','V2_l12',len(b_signs)-1,b_signs,len(b_signs)-1,b_signs)
h_V2_l02 = rt.TH2F('V2_l02','V2_l02',len(b_signs)-1,b_signs,len(b_signs)-1,b_signs)
h_V3_l01 = rt.TH2F('V3_l01','V3_l01',len(b_signs)-1,b_signs,len(b_signs)-1,b_signs)
h_V3_l12 = rt.TH2F('V3_l12','V3_l12',len(b_signs)-1,b_signs,len(b_signs)-1,b_signs)
h_V3_l02 = rt.TH2F('V3_l02','V3_l02',len(b_signs)-1,b_signs,len(b_signs)-1,b_signs)

tt_V1.Draw('l1_charge : l0_charge >> V1_l01') 
tt_V1.Draw('l2_charge : l1_charge >> V1_l12') 
tt_V1.Draw('l2_charge : l0_charge >> V1_l02') 
tt_V2.Draw('l1_charge : l0_charge >> V2_l01')
tt_V2.Draw('l2_charge : l1_charge >> V2_l12')
tt_V2.Draw('l2_charge : l0_charge >> V2_l02')
tt_V3.Draw('l1_charge : l0_charge >> V3_l01')
tt_V3.Draw('l2_charge : l1_charge >> V3_l12')
tt_V3.Draw('l2_charge : l0_charge >> V3_l02')
 
fout.Write()

hstupd8lst = [h_V1_l01,h_V1_l12,h_V1_l02,h_V2_l01,h_V2_l12,h_V2_l02,h_V3_l01,h_V3_l12,h_V3_l02]

for hh in hstupd8lst:
   if 'l01' in hh.GetTitle():
      hh.SetTitle('; l0_sign; l1_sign')
   if 'l12' in hh.GetTitle():
      hh.SetTitle('; l1_sign; l2_sign')
   if 'l02' in hh.GetTitle():
      hh.SetTitle('; l0_sign; l2_sign')
   hh.GetXaxis().SetTitleOffset(1.2)
   hh.GetYaxis().SetTitleOffset(1.4)
   hh.GetZaxis().SetTitleOffset(1.4)
   hh.SetMarkerSize(3)

c_V1_l01.cd()
h_V1_l01.Draw('colztext')
c_V1_l12.cd()
h_V1_l12.Draw('colztext')
c_V1_l02.cd()
h_V1_l02.Draw('colztext')

c_V2_l01.cd()
h_V2_l01.Draw('colztext')
c_V2_l12.cd()
h_V2_l12.Draw('colztext')
c_V2_l02.cd()
h_V2_l02.Draw('colztext')

c_V3_l01.cd()
h_V3_l01.Draw('colztext')
c_V3_l12.cd()
h_V3_l12.Draw('colztext')
c_V3_l02.cd()
h_V3_l02.Draw('colztext')

for cc in [c_V1_l01,c_V1_l12,c_V1_l02,c_V2_l01,c_V2_l12,c_V2_l02,c_V3_l01,c_V3_l12,c_V3_l02]:
   cc.cd()
   pf.showlogoprelimsim('CMS')
   cc.Modified()
   cc.Update()
   cc.SaveAs(output_dir+cc.GetTitle()+'.root')
   cc.SaveAs(output_dir+cc.GetTitle()+'.pdf')

