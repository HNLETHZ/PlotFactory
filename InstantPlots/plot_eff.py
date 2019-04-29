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
output_dir = 'temp/'

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


logspace = False

if logspace == True:
    bins = np.logspace(0, 3., 100) # 50 evenly spaced points from 10^-3 to 10^3 cm 

if logspace == False:
    bins = np.arange(0, 750, 5.0) 

h1_den        = ROOT.TH1F('h1_den'       , '', len(bins)-1, bins)
h1_num_muon = ROOT.TH1F('h1_num_muon', '', len(bins)-1, bins)
# h1_num_muontrack = ROOT.TH1F('h1_num_muontrack', '', len(bins)-1, bins)
h1_num_dsmuon  = ROOT.TH1F('h1_num_dsmuon' , '', len(bins)-1, bins)
h1_num_dgmuon  = ROOT.TH1F('h1_num_dgmuon' , '', len(bins)-1, bins)

h2_den        = ROOT.TH1F('h2_den'       , '', len(bins)-1, bins)
h2_num_muon = ROOT.TH1F('h2_num_muon', '', len(bins)-1, bins)
# h2_num_muontrack = ROOT.TH1F('h2_num_muontrack', '', len(bins)-1, bins)
h2_num_dsmuon  = ROOT.TH1F('h2_num_dsmuon' , '', len(bins)-1, bins)
h2_num_dgmuon  = ROOT.TH1F('h2_num_dgmuon' , '', len(bins)-1, bins)

for hh in [h1_den, h1_num_muon, h1_num_dsmuon, h1_num_dgmuon, h2_den, h2_num_muon, h2_num_dsmuon, h2_num_dgmuon]:
    hh.GetXaxis().SetTitle('2D gen displacement [cm]')
    hh.GetYaxis().SetTitle('Efficiency')
    hh.GetXaxis().SetTitleOffset(1.3)
    hh.GetYaxis().SetRangeUser(0.,1.05)
    hh.SetMarkerStyle(8)
    hh.SetMarkerSize(0.4)
    hh.SetMaximum(1.)

h1_den       .SetLineColor(ROOT.kBlack) ; h1_den       .SetMarkerColor(ROOT.kBlack) 
h1_num_muon.SetLineColor(ROOT.kBlue+2 ) ; h1_num_muon.SetMarkerColor(ROOT.kBlue+2 ) 
# h1_num_muontrack.SetLineColor(ROOT.kMagenta+2 ) ; h1_num_muontrack.SetMarkerColor(ROOT.Magenta+2 ) 
h1_num_dsmuon .SetLineColor(ROOT.kRed+2  ) ; h1_num_dsmuon .SetMarkerColor(ROOT.kRed+2  ) 
h1_num_dgmuon .SetLineColor(ROOT.kGreen+2  ) ; h1_num_dgmuon .SetMarkerColor(ROOT.kGreen+2  ) 

h2_den       .SetLineColor(ROOT.kBlack) ; h2_den       .SetMarkerColor(ROOT.kBlack)
h2_num_muon.SetLineColor(ROOT.kBlue ) ; h2_num_muon.SetMarkerColor(ROOT.kBlue )
# h2_num_muontrack.SetLineColor(ROOT.kMagenta+2 ) ; h2_num_muontrack.SetMarkerColor(ROOT.Magenta+2 ) 
h2_num_dsmuon .SetLineColor(ROOT.kRed  ) ; h2_num_dsmuon .SetMarkerColor(ROOT.kRed  )
h2_num_dgmuon .SetLineColor(ROOT.kGreen  ) ; h2_num_dgmuon .SetMarkerColor(ROOT.kGreen  ) 

# sel1_den        = 'l1_pt>3 & abs(l1_eta)>0.8 & abs(l1_eta)<2.4 & abs(l1_pdgId)==13' #default value: pt>3 , eta < 2.4
sel1_den        = 'l1_pt>10 & abs(l1_eta)<2.4 & abs(l1_pdgId)==13' #default value: pt>3 , eta < 2.4

# sel1_num_muontrack = 'l1_matched_muon_pt > 0 & (l1_matched_muon_id_s | l1_matched_muon_id_l | l1_matched_muon_id_m | l1_matched_muon_id_t | l1_matched_muon_id_tnv | l1_matched_muon_id_hpt)'
# sel1_num_muon = 'l1_matched_muon_pt > 0 & (l1_matched_muon_id_hpt )'
sel1_num_muon = 'l1_matched_muon_pt > 0'

sel1_num_dsmuon  = 'l1_matched_dsmuon_pt > 0'
sel1_num_dgmuon  = 'l1_matched_dgmuon_pt > 0'

# sel2_den        = 'l2_pt>3 & abs(l2_eta)>0.8 & abs(l1_eta)<2.4 & abs(l2_pdgId)==13' 
sel2_den        = 'l2_pt>10 & abs(l2_eta)<2.4 & abs(l2_pdgId)==13' 

# sel2_num_muontrack        = 'l2_pt>3 & abs(l2_eta)<2.4 & (l2_matched_muon_id_s | l2_matched_muon_id_l | l2_matched_muon_id_m | l2_matched_muon_id_t | l2_matched_muon_id_tnv | l2_matched_muon_id_hpt)'
# sel2_num_muon = 'l2_matched_muon_pt > 0 & (l2_matched_muon_id_hpt)'
sel2_num_muon = 'l2_matched_muon_pt > 0'

sel2_num_dsmuon  = 'l2_matched_dsmuon_pt > 0'
sel2_num_dgmuon  = 'l2_matched_dgmuon_pt > 0'

c_eff = ROOT.TCanvas('c_eff', 'c_eff')
# c_eff.SetLogx()
c_eff.SetGridx()
c_eff.SetGridy()

tt.Draw('hnl_2d_disp >> h1_den'       , sel1_den                              )
tt.Draw('hnl_2d_disp >> h1_num_muon', '&'.join([sel1_den, sel1_num_muon]) )
# tt.Draw('hnl_2d_disp >> h1_num_muontrack', '&'.join([sel1_den, sel1_num_muontrack]) )
tt.Draw('hnl_2d_disp >> h1_num_dsmuon' , '&'.join([sel1_den, sel1_num_dsmuon ]) )
tt.Draw('hnl_2d_disp >> h1_num_dgmuon' , '&'.join([sel1_den, sel1_num_dgmuon ]) )

tt.Draw('hnl_2d_disp >> h2_den'       , sel2_den                              )
tt.Draw('hnl_2d_disp >> h2_num_muon', '&'.join([sel2_den, sel2_num_muon]) )
# tt.Draw('hnl_2d_disp >> h2_num_muontrack', '&'.join([sel2_den, sel2_num_muontrack]) )
tt.Draw('hnl_2d_disp >> h2_num_dsmuon' , '&'.join([sel2_den, sel2_num_dsmuon ]) )
tt.Draw('hnl_2d_disp >> h2_num_dgmuon' , '&'.join([sel2_den, sel2_num_dgmuon ]) )

h1_den       .Add(h2_den       )
h1_num_muon.Add(h2_num_muon)
# h1_num_muontrack.Add(h2_num_muontrack)
h1_num_dsmuon.Add(h2_num_dsmuon )
h1_num_dgmuon.Add(h2_num_dgmuon )

h1_num_muon.Divide(h1_den)
# h1_num_muontrack.Divide(h1_den)
h1_num_dsmuon.Divide(h1_den)
h1_num_dgmuon.Divide(h1_den)

h1_num_tot = h1_num_muon.Clone()
h1_num_tot.Add(h1_num_dsmuon)
h1_num_tot.SetLineColor(ROOT.kBlack)
h1_num_tot.SetMarkerColor(ROOT.kBlack)

h1_num_dsmuon.Draw('hist pe')
# h1_num_dgmuon.Draw('hist pe same')
h1_num_muon.Draw('hist pe same')

# h1_num_muontrack.Draw('hist pe same')
# h1_num_tot   .Draw('hist pe same')


leg = ROOT.TLegend(.4,.75,.8,.88)
# leg.SetBorderSize(0)
# leg.SetFillColor(0)
# leg.SetFillStyle(0)
# leg.SetTextFont(42)
# leg.SetTextSize(0.03)
leg.AddEntry(h1_num_muon, 'slimmedMuons'            ,'EP')
# leg.AddEntry(h1_num_muontrack, 'standard slimmed muon reco'            ,'EP')
leg.AddEntry(h1_num_dsmuon , 'displacedStandAloneMuons','EP')
leg.AddEntry(h1_num_dgmuon   , 'diplacedGlobalMuons'                 ,'EP')
leg.Draw('apez same')

pf.showlogopreliminary('CMS','Simulation Preliminary')

set_trace()
c_eff.Update()
c_eff.SaveAs(output_dir + 'c_eff.pdf')
c_eff.SaveAs(output_dir + 'c_eff.root')



