import ROOT as rt
import numpy as np
import plotfactory as pf
import sys
from pdb import set_trace

output_dir = '/afs/cern.ch/work/v/vstampf/plots/candidates/gentuple/' 

fout = rt.TFile(output_dir+'flavcheckV_tr_sl.root', 'recreate')

######################################### 
# Make Chain from selection of samples
#########################################

# Get the option from the command line, using 'True' as a fallback.

ntup_dir = '/eos/user/m/manzoni/HNL/gentuple_050318_v4/'

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

c_V1 = rt.TCanvas('flavors_V1_tr_sl','flavors_V1_tr_sl')
c_V2 = rt.TCanvas('flavors_V2_tr_sl','flavors_V2_tr_sl')
c_V3 = rt.TCanvas('flavors_V3_tr_sl','flavors_V3_tr_sl')

b_flavor = np.arange(11.,15,1.5)

h_V1_l1 = rt.TH2F('V1_l1','V1_l1',len(b_flavor)-1,b_flavor,len(b_flavor)-1,b_flavor)
h_V1_l2 = rt.TH2F('V1_l2','V1_l2',len(b_flavor)-1,b_flavor,len(b_flavor)-1,b_flavor)
h_V2_l1 = rt.TH2F('V2_l1','V2_l1',len(b_flavor)-1,b_flavor,len(b_flavor)-1,b_flavor)
h_V2_l2 = rt.TH2F('V2_l2','V2_l2',len(b_flavor)-1,b_flavor,len(b_flavor)-1,b_flavor)
h_V3_l1 = rt.TH2F('V3_l1','V3_l1',len(b_flavor)-1,b_flavor,len(b_flavor)-1,b_flavor)
h_V3_l2 = rt.TH2F('V3_l2','V3_l2',len(b_flavor)-1,b_flavor,len(b_flavor)-1,b_flavor)

tt_V1.Draw('abs(l2_pdgId) : abs(l1_pdgId) >> V1_l1', 'abs(l1_pdgId) == abs(n_pdgId) - 1') # l1 trailing)
tt_V1.Draw('abs(l1_pdgId) : abs(l2_pdgId) >> V1_l2', 'abs(l2_pdgId) == abs(n_pdgId) - 1') # l2 trailing
tt_V2.Draw('abs(l2_pdgId) : abs(l1_pdgId) >> V2_l1', 'abs(l1_pdgId) == abs(n_pdgId) - 1')
tt_V2.Draw('abs(l1_pdgId) : abs(l2_pdgId) >> V2_l2', 'abs(l2_pdgId) == abs(n_pdgId) - 1')
tt_V3.Draw('abs(l2_pdgId) : abs(l1_pdgId) >> V3_l1', 'abs(l1_pdgId) == abs(n_pdgId) - 1')
tt_V3.Draw('abs(l1_pdgId) : abs(l2_pdgId) >> V3_l2', 'abs(l2_pdgId) == abs(n_pdgId) - 1')
 
fout.Write()

h_V1_l1.Add(h_V1_l2)
h_V2_l1.Add(h_V2_l2)
h_V3_l1.Add(h_V3_l2)

hstupd8lst = [h_V1_l1,h_V2_l1,h_V3_l1]

for hh in hstupd8lst:
   hh.SetTitle(';l_subleading_pdgId ; l_trailing_pdgId')
   hh.GetXaxis().SetTitleOffset(1.2)
   hh.GetYaxis().SetTitleOffset(1.4)
   hh.GetZaxis().SetTitleOffset(1.4)

c_V1.cd()
h_V1_l1.Draw('colz')

c_V2.cd()
h_V2_l1.Draw('colz')

c_V3.cd()
h_V3_l1.Draw('colz')

for cc in [c_V1,c_V2,c_V3]:
   cc.Modified()
   cc.Update()
   cc.SaveAs(output_dir+cc.GetTitle()+'.root')
   cc.SaveAs(output_dir+cc.GetTitle()+'.pdf')

