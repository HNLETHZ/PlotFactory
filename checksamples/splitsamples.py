import numpy as np
from allsamplefiles import allsamples as samples 
# diff = in my useables but not riccardo's
diff = ['M-6_V-0.004472135955_e_onshell',
'M-7_V-0.002296_mu_onshell',
'M-7_V-0.00459211224_mu_onshell',
'M-9_V-0.00244948974278_e_onshell']

M_6_V_0p004472135955_e_onshell = [ss for ss in samples if diff[0] in ss]
M_7_V_0p002296_mu_onshell = [ss for ss in samples if diff[1] in ss]
M_7_V_0p00459211224_mu_onshell = [ss for ss in samples if diff[2] in ss]
M_9_V_0p00244948974278_e_onshell = [ss for ss in samples if diff[3] in ss]

# diff = [ sample for sample in myuseablesamples if not sample in riccardosgoodlist]

print(len(M_6_V_0p004472135955_e_onshell))
for j in np.arange(len(M_6_V_0p004472135955_e_onshell)):
   print(M_6_V_0p004472135955_e_onshell[j])
print('######################################################################################################')
print(len(M_7_V_0p002296_mu_onshell))
for j in np.arange(len(M_7_V_0p002296_mu_onshell)):
   print(M_7_V_0p002296_mu_onshell[j])
print('######################################################################################################')
print(len(M_7_V_0p002296_mu_onshell))
for j in np.arange(len(M_7_V_0p002296_mu_onshell)):
   print(M_7_V_0p002296_mu_onshell[j])
print('######################################################################################################')
print(len(M_9_V_0p00244948974278_e_onshell))
for j in np.arange(len(M_9_V_0p00244948974278_e_onshell)):
   print(M_9_V_0p00244948974278_e_onshell[j])
