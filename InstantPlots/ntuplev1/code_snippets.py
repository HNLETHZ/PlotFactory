
###################################
# counting bin content explicitly #
# and plotting result in a TGraph #
###################################

bincf1 = np.array([])
bincf0 = np.array([])
x0 = np.array([])
x1 = np.array([])

for i in range(len(binsx)):
    #print("bin", i, "content", h0_smu_cf1_pT.GetBinContent(i)) 
    bincf1 = np.append(bincf1,h1.GetBinContent(i))
    bincf0 = np.append(bincf0,h0.GetBinContent(i))
    if (bincf1[i]+bincf0[i])!=0:
        x1 = np.append(x1,bincf1[i]/(bincf0[i]+bincf1[i]))
        x0 = np.append(x0,bincf0[i]/(bincf0[i]+bincf1[i]))

print("#binsx=%i"%len(binsx),"and #x1=%i"%len(x1)," resp. #x0=%i"%len(x0))

c30.cd()
gr0 = ROOT.TGraph(len(x0),binsx,x0)
gr0.Draw("AB")

c31.cd()
gr1 = ROOT.TGraph(len(x1),binsx,x1)
gr1.Draw("AB")

#########################
# some plotting options #
#########################

logspace = False 
 
if logspace == True: 
    binsx = np.logspace(-6, 3, 50) # 50 evenly spaced points from -6 to 3   
    binsy = np.logspace(-2.2, 0.03, 50) # 50 evenly spaced points from 10^-3 to 10^3 cm 

c1.SetLogx()
c1.SetLogy()
c1.SetGridx()
c1.SetGridy()
c2.SetGridx()
c2.SetGridy()
