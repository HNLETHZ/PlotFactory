import ROOT
import numpy as np
import plotfactory as pf
from glob import glob

pf.setpfstyle()
tt = pf.makechain(True)

output_dir = '/afs/cern.ch/user/v/vstampf/CMSSW_8_0_30/PlotFactory/plots/4_reg/'

#file = ROOT.TFile('tree.root')
#tt = file.Get('tree')
ntries = tt.GetEntries()

outfile = ROOT.TFile(output_dir + 'hist.root','recreate')   # always out after reading tree file

print('Number of entries: ' + str(ntries))

pTbins = np.arange(3.,75, 5)

#t = ROOT.TCanvas('t','t')

## BARREL

smul1d5barnf = ROOT.TH1F('smul1barnf','smul1barnf',len(pTbins)-1,pTbins)
smul2d5barnf = ROOT.TH1F('smul2barnf','smul2barnf',len(pTbins)-1,pTbins)
smul1d5barcf = ROOT.TH1F('smul1barcf','smul1barcf',len(pTbins)-1,pTbins)
smul2d5barcf = ROOT.TH1F('smul2barcf','smul2barcf',len(pTbins)-1,pTbins)

dsmul1d5barnf = ROOT.TH1F('dsmul1barnf','dsmul1barnf',len(pTbins)-1,pTbins)
dsmul2d5barnf = ROOT.TH1F('dsmul2barnf','dsmul2barnf',len(pTbins)-1,pTbins)
dsmul1d5barcf = ROOT.TH1F('dsmul1barcf','dsmul1barcf',len(pTbins)-1,pTbins)
dsmul2d5barcf = ROOT.TH1F('dsmul2barcf','dsmul2barcf',len(pTbins)-1,pTbins)

smul1d1barnf = ROOT.TH1F('smul1d1barnf','smul1d1barnf',len(pTbins)-1,pTbins)
smul2d1barnf = ROOT.TH1F('smul2d1barnf','smul2d1barnf',len(pTbins)-1,pTbins)
smul1d1barcf = ROOT.TH1F('smul1d1barcf','smul1d1barcf',len(pTbins)-1,pTbins)
smul2d1barcf = ROOT.TH1F('smul2d1barcf','smul2d1barcf',len(pTbins)-1,pTbins)

dsmul1d1barnf = ROOT.TH1F('dsmul1d1barnf','dsmul1d1barnf',len(pTbins)-1,pTbins)
dsmul2d1barnf = ROOT.TH1F('dsmul2d1barnf','dsmul2d1barnf',len(pTbins)-1,pTbins)
dsmul1d1barcf = ROOT.TH1F('dsmul1d1barcf','dsmul1d1barcf',len(pTbins)-1,pTbins)
dsmul2d1barcf = ROOT.TH1F('dsmul2d1barcf','dsmul2d1barcf',len(pTbins)-1,pTbins)

smul1d2barnf = ROOT.TH1F('smul1d2barnf','smul1d2barnf',len(pTbins)-1,pTbins)
smul2d2barnf = ROOT.TH1F('smul2d2barnf','smul2d2barnf',len(pTbins)-1,pTbins)
smul1d2barcf = ROOT.TH1F('smul1d2barcf','smul1d2barcf',len(pTbins)-1,pTbins)
smul2d2barcf = ROOT.TH1F('smul2d2barcf','smul2d2barcf',len(pTbins)-1,pTbins)

dsmul1d2barnf = ROOT.TH1F('dsmul1d2barnf','dsmul1d2barnf',len(pTbins)-1,pTbins)
dsmul2d2barnf = ROOT.TH1F('dsmul2d2barnf','dsmul2d2barnf',len(pTbins)-1,pTbins)
dsmul1d2barcf = ROOT.TH1F('dsmul1d2barcf','dsmul1d2barcf',len(pTbins)-1,pTbins)
dsmul2d2barcf = ROOT.TH1F('dsmul2d2barcf','dsmul2d2barcf',len(pTbins)-1,pTbins)

smul1d3barnf = ROOT.TH1F('smul1d3barnf','smul1d3barnf',len(pTbins)-1,pTbins)
smul2d3barnf = ROOT.TH1F('smul2d3barnf','smul2d3barnf',len(pTbins)-1,pTbins)
smul1d3barcf = ROOT.TH1F('smul1d3barcf','smul1d3barcf',len(pTbins)-1,pTbins)
smul2d3barcf = ROOT.TH1F('smul2d3barcf','smul2d3barcf',len(pTbins)-1,pTbins)

dsmul1d3barnf = ROOT.TH1F('dsmul1d3barnf','dsmul1d3barnf',len(pTbins)-1,pTbins)
dsmul2d3barnf = ROOT.TH1F('dsmul2d3barnf','dsmul2d3barnf',len(pTbins)-1,pTbins)
dsmul1d3barcf = ROOT.TH1F('dsmul1d3barcf','dsmul1d3barcf',len(pTbins)-1,pTbins)
dsmul2d3barcf = ROOT.TH1F('dsmul2d3barcf','dsmul2d3barcf',len(pTbins)-1,pTbins)

smul1d4barnf = ROOT.TH1F('smul1d4barnf','smul1d4barnf',len(pTbins)-1,pTbins)
smul2d4barnf = ROOT.TH1F('smul2d4barnf','smul2d4barnf',len(pTbins)-1,pTbins)
smul1d4barcf = ROOT.TH1F('smul1d4barcf','smul1d4barcf',len(pTbins)-1,pTbins)
smul2d4barcf = ROOT.TH1F('smul2d4barcf','smul2d4barcf',len(pTbins)-1,pTbins)

dsmul1d4barnf = ROOT.TH1F('dsmul1d4barnf','dsmul1d4barnf',len(pTbins)-1,pTbins)
dsmul2d4barnf = ROOT.TH1F('dsmul2d4barnf','dsmul2d4barnf',len(pTbins)-1,pTbins)
dsmul1d4barcf = ROOT.TH1F('dsmul1d4barcf','dsmul1d4barcf',len(pTbins)-1,pTbins)
dsmul2d4barcf = ROOT.TH1F('dsmul2d4barcf','dsmul2d4barcf',len(pTbins)-1,pTbins)

## ENDCAP

smul1d5capnf = ROOT.TH1F('smul1capnf','smul1capnf',len(pTbins)-1,pTbins)
smul2d5capnf = ROOT.TH1F('smul2capnf','smul2capnf',len(pTbins)-1,pTbins)
smul1d5capcf = ROOT.TH1F('smul1capcf','smul1capcf',len(pTbins)-1,pTbins)
smul2d5capcf = ROOT.TH1F('smul2capcf','smul2capcf',len(pTbins)-1,pTbins)

dsmul1d5capnf = ROOT.TH1F('dsmul1capnf','dsmul1capnf',len(pTbins)-1,pTbins)
dsmul2d5capnf = ROOT.TH1F('dsmul2capnf','dsmul2capnf',len(pTbins)-1,pTbins)
dsmul1d5capcf = ROOT.TH1F('dsmul1capcf','dsmul1capcf',len(pTbins)-1,pTbins)
dsmul2d5capcf = ROOT.TH1F('dsmul2capcf','dsmul2capcf',len(pTbins)-1,pTbins)

smul1d1capnf = ROOT.TH1F('smul1d1capnf','smul1d1capnf',len(pTbins)-1,pTbins)
smul2d1capnf = ROOT.TH1F('smul2d1capnf','smul2d1capnf',len(pTbins)-1,pTbins)
smul1d1capcf = ROOT.TH1F('smul1d1capcf','smul1d1capcf',len(pTbins)-1,pTbins)
smul2d1capcf = ROOT.TH1F('smul2d1capcf','smul2d1capcf',len(pTbins)-1,pTbins)

dsmul1d1capnf = ROOT.TH1F('dsmul1d1capnf','dsmul1d1capnf',len(pTbins)-1,pTbins)
dsmul2d1capnf = ROOT.TH1F('dsmul2d1capnf','dsmul2d1capnf',len(pTbins)-1,pTbins)
dsmul1d1capcf = ROOT.TH1F('dsmul1d1capcf','dsmul1d1capcf',len(pTbins)-1,pTbins)
dsmul2d1capcf = ROOT.TH1F('dsmul2d1capcf','dsmul2d1capcf',len(pTbins)-1,pTbins)

smul1d2capnf = ROOT.TH1F('smul1d2capnf','smul1d2capnf',len(pTbins)-1,pTbins)
smul2d2capnf = ROOT.TH1F('smul2d2capnf','smul2d2capnf',len(pTbins)-1,pTbins)
smul1d2capcf = ROOT.TH1F('smul1d2capcf','smul1d2capcf',len(pTbins)-1,pTbins)
smul2d2capcf = ROOT.TH1F('smul2d2capcf','smul2d2capcf',len(pTbins)-1,pTbins)

dsmul1d2capnf = ROOT.TH1F('dsmul1d2capnf','dsmul1d2capnf',len(pTbins)-1,pTbins)
dsmul2d2capnf = ROOT.TH1F('dsmul2d2capnf','dsmul2d2capnf',len(pTbins)-1,pTbins)
dsmul1d2capcf = ROOT.TH1F('dsmul1d2capcf','dsmul1d2capcf',len(pTbins)-1,pTbins)
dsmul2d2capcf = ROOT.TH1F('dsmul2d2capcf','dsmul2d2capcf',len(pTbins)-1,pTbins)

smul1d3capnf = ROOT.TH1F('smul1d3capnf','smul1d3capnf',len(pTbins)-1,pTbins)
smul2d3capnf = ROOT.TH1F('smul2d3capnf','smul2d3capnf',len(pTbins)-1,pTbins)
smul1d3capcf = ROOT.TH1F('smul1d3capcf','smul1d3capcf',len(pTbins)-1,pTbins)
smul2d3capcf = ROOT.TH1F('smul2d3capcf','smul2d3capcf',len(pTbins)-1,pTbins)

dsmul1d3capnf = ROOT.TH1F('dsmul1d3capnf','dsmul1d3capnf',len(pTbins)-1,pTbins)
dsmul2d3capnf = ROOT.TH1F('dsmul2d3capnf','dsmul2d3capnf',len(pTbins)-1,pTbins)
dsmul1d3capcf = ROOT.TH1F('dsmul1d3capcf','dsmul1d3capcf',len(pTbins)-1,pTbins)
dsmul2d3capcf = ROOT.TH1F('dsmul2d3capcf','dsmul2d3capcf',len(pTbins)-1,pTbins)

smul1d4capnf = ROOT.TH1F('smul1d4capnf','smul1d4capnf',len(pTbins)-1,pTbins)
smul2d4capnf = ROOT.TH1F('smul2d4capnf','smul2d4capnf',len(pTbins)-1,pTbins)
smul1d4capcf = ROOT.TH1F('smul1d4capcf','smul1d4capcf',len(pTbins)-1,pTbins)
smul2d4capcf = ROOT.TH1F('smul2d4capcf','smul2d4capcf',len(pTbins)-1,pTbins)

dsmul1d4capnf = ROOT.TH1F('dsmul1d4capnf','dsmul1d4capnf',len(pTbins)-1,pTbins)
dsmul2d4capnf = ROOT.TH1F('dsmul2d4capnf','dsmul2d4capnf',len(pTbins)-1,pTbins)
dsmul1d4capcf = ROOT.TH1F('dsmul1d4capcf','dsmul1d4capcf',len(pTbins)-1,pTbins)
dsmul2d4capcf = ROOT.TH1F('dsmul2d4capcf','dsmul2d4capcf',len(pTbins)-1,pTbins)

smudsum  = ROOT.TH1F('smudsum','smudsum',len(pTbins)-1,pTbins)
smudbarcf   = ROOT.TH1F('smudbarcf','slimmedMuon',len(pTbins)-1,pTbins)

# buffer[reco][lepton][range]
# barrel
dr1l1barcf = [smul1d1barcf,smul1d2barcf,smul1d3barcf,smul1d4barcf,smul1d5barcf]
dr1l2barcf = [smul2d1barcf,smul2d2barcf,smul2d3barcf,smul2d4barcf,smul2d5barcf]

dr2l1barcf = [dsmul1d1barcf,dsmul1d2barcf,dsmul1d3barcf,dsmul1d4barcf,dsmul1d5barcf]
dr2l2barcf = [dsmul2d1barcf,dsmul2d2barcf,dsmul2d3barcf,dsmul2d4barcf,dsmul2d5barcf]

dr1l1barnf = [smul1d1barnf,smul1d2barnf,smul1d3barnf,smul1d4barnf,smul1d5barnf]
dr1l2barnf = [smul2d1barnf,smul2d2barnf,smul2d3barnf,smul2d4barnf,smul2d5barnf]

dr2l1barnf = [dsmul1d1barnf,dsmul1d2barnf,dsmul1d3barnf,dsmul1d4barnf,dsmul1d5barnf]
dr2l2barnf = [dsmul2d1barnf,dsmul2d2barnf,dsmul2d3barnf,dsmul2d4barnf,dsmul2d5barnf]

r1barcf = [dr1l1barcf,dr1l2barcf]
r1barnf = [dr1l1barnf,dr1l2barnf]

r2barcf = [dr2l1barcf,dr2l2barcf]
r2barnf = [dr2l1barnf,dr2l2barnf]

bufbarcf = [r1barcf,r2barcf]
bufbarnf = [r1barnf,r2barnf]

# cap 
dr1l1capcf = [smul1d1capcf,smul1d2capcf,smul1d3capcf,smul1d4capcf,smul1d5capcf]
dr1l2capcf = [smul2d1capcf,smul2d2capcf,smul2d3capcf,smul2d4capcf,smul2d5capcf]

dr2l1capcf = [dsmul1d1capcf,dsmul1d2capcf,dsmul1d3capcf,dsmul1d4capcf,dsmul1d5capcf]
dr2l2capcf = [dsmul2d1capcf,dsmul2d2capcf,dsmul2d3capcf,dsmul2d4capcf,dsmul2d5capcf]

dr1l1capnf = [smul1d1capnf,smul1d2capnf,smul1d3capnf,smul1d4capnf,smul1d5capnf]
dr1l2capnf = [smul2d1capnf,smul2d2capnf,smul2d3capnf,smul2d4capnf,smul2d5capnf]

dr2l1capnf = [dsmul1d1capnf,dsmul1d2capnf,dsmul1d3capnf,dsmul1d4capnf,dsmul1d5capnf]
dr2l2capnf = [dsmul2d1capnf,dsmul2d2capnf,dsmul2d3capnf,dsmul2d4capnf,dsmul2d5capnf]

r1capcf = [dr1l1capcf,dr1l2capcf]
r1capnf = [dr1l1capnf,dr1l2capnf]

r2capcf = [dr2l1capcf,dr2l2capcf]
r2capnf = [dr2l1capnf,dr2l2capnf]

bufcapcf = [r1capcf,r2capcf]
bufcapnf = [r1capnf,r2capnf]

# total

bufcf = [bufbarcf,bufcapcf]
bufnf = [bufbarnf,bufcapnf]


# define different dxy regions #
d1 = 4      # pixel
d2 = 120    # tracker
d3 = 350    # cals
d4 = 600    # drift chambers

# sanity check: adding up entries of the loops #
endcap = 0
barrel = 0
rest = 0

print('Filling histograms')

# filling histograms #
for i in range(ntries):
    tt.GetEntry(i)
    pf.progressbar(i,ntries)
# reco loop # 
#    reco = 'muon'
#    recoind = 0
    for reco in ['muon','dsmuon']:
#    lep = 'l1'
        recoind = 2
        if reco == 'muon':
            recoind = 0
        elif reco == 'dsmuon':
            recoind = 1
# lepton loop # 
        for lep in ['l1','l2']:
#    lep = 'l1'
            lepind = 2
            if lep == 'l1': 
                lepind = 0
            elif lep == 'l2':
                lepind = 1
#    lepind = 0
# setting the filling variables #
            pdgId = tt.GetLeaf('%s_pdgId'%lep).GetValue()
            eta = tt.GetLeaf('%s_eta'%lep).GetValue()
            pt = tt.GetLeaf('%s_pt'%lep).GetValue()
            charge = tt.GetLeaf('%s_charge'%lep).GetValue()
            hnld = tt.GetLeaf('hnl_2d_disp').GetValue()
            matched_pt = tt.GetLeaf('%s_matched_%s_pt'%(lep,reco)).GetValue()
            matched_charge = tt.GetLeaf('%s_matched_%s_charge'%(lep,reco)).GetValue()
# range loop #
            for r in [0,1,2,3,4]: # the last turn produces the control plot
                d = [-1,d1,d2,d3,d4,800]
                if r == 4:       
                    d[4] = -1
#            r = 4
# barrel: abs(eta) < 0.8, selection: abs(pdgId)==13 & reco'd pt>3
                if (abs(eta)<0.8 and abs(pdgId) == 13 and hnld > d[r] and hnld < d[r+1]):
                    if(matched_pt > 3 and matched_charge == charge):
                        bufnf[0][recoind][lepind][r].Fill(pt)
                    elif(matched_pt > 3 and matched_charge != charge):
                        bufcf[0][recoind][lepind][r].Fill(pt)
                    barrel += 1
#endcap: abs(eta) < 2.4 &  abs(eta) > 1.2, selection: abs(pdgId) == 13 & reco'd pt > 3
                elif (abs(eta)<2.4 and abs(eta) > 1.2 and abs(pdgId) == 13 and hnld > d[r] and hnld < d[r+1]):
                    if(matched_pt > 3 and matched_charge == charge):
                        bufnf[1][recoind][lepind][r].Fill(pt)
                    elif(matched_pt > 3 and matched_charge != charge):
                        bufcf[1][recoind][lepind][r].Fill(pt)
                    endcap += 1
#last line in lepton loop: adding hists
                else: 
                    rest += 1
#end of range loop
#end of lepton loop
#end of reco loop


print('\nAdding and saving final histograms')

for wo in [0,1]:
    for rec in [0,1]:
        for dist in [0,1,2,3,4]:
            bufcf[wo][rec][0][dist].Add(bufcf[wo][rec][1][dist])
            bufnf[wo][rec][0][dist].Add(bufnf[wo][rec][1][dist])
            bufcf[wo][rec][0][dist].Write()#SaveAs(output_dir + 'w%i_r%i_d%i_cf.root'%(wo,rec,dist+1))
            bufnf[wo][rec][0][dist].Write()#SaveAs(output_dir + 'w%i_r%i_d%i_nf.root'%(wo,rec,dist+1))


#t.cd()
#smul1d5barnf.Add(smul2barnf)
#smul1d5barcf.Add(smul2barcf)
#smudsum.Add(smul1d5barcf)
#smudsum.Add(smul1d5capcf)
#smudsum.Add(smul1d5barnf)
#smudsum.Add(smul1d5capnf)
#bufff = ROOT.TH1F('cf','xxx',len(pTbins)-1,pTbins)
#bufff.Add(smul1d5capcf)
#bufff.Add(smul1d5barcf)
#smudbarcf.Divide(bufff,smudsum)


#dsmul1d5barnf.Add(dsmul2barnf)
#dsmul1d5barcf.Add(dsmul2barcf)
#dsmudsum.Add(dsmul1d5barcf)
#dsmudsum.Add(dsmul1d5barnf)
#dsmudbarcf.Divide(dsmul1d5barcf,dsmudsum)

#dsmudbarcf.Draw()
#smudbarcf.Draw('same')
#smudsum.Draw()

#pf.showlumi(' l1+l2 / eta<0.8 / alld / %.2f M entries'%(ntries / 1000000.))
#smudbarcf.SetMarkerColor(4)
#dsmudbarcf.SetMarkerColor(2)
#smudbarcf.GetXaxis().SetTitle('p_{T}[GeV]')
#smudbarcf.GetYaxis().SetTitle('Entries (normalized)')
#smudbarcf.GetXaxis().SetTitleOffset(1.2)
#smudbarcf.GetYaxis().SetTitleOffset(1.2)
#pf.showlogoprelimsim('CMS')

#leg = ROOT.TLegend(.18,.76,.4,.9)
#leg.SetBorderSize(0)
#leg.SetFillColor(ROOT.kWhite)
#leg.SetFillStyle(0)
#leg.SetTextFont(42)
#leg.SetTextSize(0.03)
#leg.AddEntry(dsmudbarcf, 'dSA#mu', 'EP')
#leg.AddEntry(smudbarcf , 'S#mu', 'EP')
#leg.Draw('apez same')
#t.Update()
print(barrel, endcap, rest, barrel + endcap + rest - ntries)

#outfile.Write()
outfile.Close()
