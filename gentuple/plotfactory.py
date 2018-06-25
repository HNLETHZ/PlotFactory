########################## 
# Import relevant modules
##########################
import ROOT
import numpy as np
from glob import glob
import time
from array import array
import sys
import ntup_dir as nt

########################## 
# Prepare chain of trees
##########################
#This is the location where all ntuples are stored. Adapt the location to your path. 
# ntup_dir = '/afs/cern.ch/user/d/dezhu/workspace/public/ntuples/'    
ntup_dir = nt.getntupdir()
# Returns a TChain object which either contains all samples (allsamples = True) or a selected sample (allsamples = False) with different displacements. 
def makechain(allsamples):    

    #access multiple trees by "chaining" them
    chain = ROOT.TChain('tree')
    all_files = glob(ntup_dir + '*/HNLGenTreeProducer/tree.root')

    if allsamples == True:
        for sample in all_files: #for the first 10 files
            chain.Add(sample)

    if allsamples == False:
        chain.Add(ntup_dir + 'HN3L_M_1_V_0p00282842712475_e_onshell/HNLGenTreeProducer/tree.root')
        chain.Add(ntup_dir + 'HN3L_M_1_V_0p00316227766017_e_onshell/HNLGenTreeProducer/tree.root')
        chain.Add(ntup_dir + 'HN3L_M_1_V_0p004472135955_e_onshell/HNLGenTreeProducer/tree.root')
        chain.Add(ntup_dir + 'HN3L_M_1_V_0p004472135955_mu_onshell/HNLGenTreeProducer/tree.root')
        chain.Add(ntup_dir + 'HN3L_M_1_V_0p00547722557505_e_onshell/HNLGenTreeProducer/tree.root')
        chain.Add(ntup_dir + 'HN3L_M_1_V_0p00547722557505_mu_onshell/HNLGenTreeProducer/tree.root')
        chain.Add(ntup_dir + 'HN3L_M_1_V_0p00707106781187_e_onshell/HNLGenTreeProducer/tree.root')
        chain.Add(ntup_dir + 'HN3L_M_1_V_0p00707106781187_mu_onshell/HNLGenTreeProducer/tree.root')
        chain.Add(ntup_dir + 'HN3L_M_1_V_0p00836660026534_e_onshell/HNLGenTreeProducer/tree.root')
        chain.Add(ntup_dir + 'HN3L_M_1_V_0p00836660026534_mu_onshell/HNLGenTreeProducer/tree.root')
        chain.Add(ntup_dir + 'HN3L_M_2_V_0p00244948974278_e_onshell/HNLGenTreeProducer/tree.root')
        chain.Add(ntup_dir + 'HN3L_M_2_V_0p00244948974278_mu_onshell/HNLGenTreeProducer/tree.root')
        chain.Add(ntup_dir + 'HN3L_M_2_V_0p01_e_onshell/HNLGenTreeProducer/tree.root')
        chain.Add(ntup_dir + 'HN3L_M_2_V_0p01_mu_onshell/HNLGenTreeProducer/tree.root')
        chain.Add(ntup_dir + 'HN3L_M_2p1_V_0p00244948974278_e_onshell/HNLGenTreeProducer/tree.root')
        chain.Add(ntup_dir + 'HN3L_M_2p1_V_0p00244948974278_mu_onshell/HNLGenTreeProducer/tree.root')
        chain.Add(ntup_dir + 'HN3L_M_2p1_V_0p00282842712475_e_onshell/HNLGenTreeProducer/tree.root')
        chain.Add(ntup_dir + 'HN3L_M_2p1_V_0p00282842712475_mu_onshell/HNLGenTreeProducer/tree.root')
        chain.Add(ntup_dir + 'HN3L_M_2p1_V_0p00316227766017_e_onshell/HNLGenTreeProducer/tree.root')
        chain.Add(ntup_dir + 'HN3L_M_2p1_V_0p00316227766017_mu_onshell/HNLGenTreeProducer/tree.root')

    nentries = chain.GetEntries()
    print('Created a TChain object with %d events.'%(nentries))
    print('using '+ntup_dir)
    return chain

########################## 
# Additional tools
##########################

# prints out a progressbar which will be flushed at the terminal
def progressbar(count, total, status=''):
        sys.stdout.flush()
        bar_len = 60
        filled_len = int(round(bar_len * count / float(total)))
        percents = round(100.0 * count / float(total), 1)
        bar = '=' * (filled_len-1) + '>' +'-' * (bar_len - filled_len)
        sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))

def showlumi(title):
    latex = ROOT.TLatex()
    latex.SetNDC()
    latex.SetTextAlign(31)
    latex.SetTextFont(42)
    latex.SetTextSize(0.04)
    latex.DrawLatex(0.83,0.94,title)
    # 'xxx fb^{-1} (xxx TeV)'

def showlogo(text):
    logo = ROOT.TLatex()
    logo.SetNDC()
    logo.SetTextAlign(11)
    logo.SetTextFont(61)
    logo.SetTextSize(0.045)
    logo.DrawLatex(0.15,0.94,text)

def showlogopreliminary(text1,text2):
    logo = ROOT.TLatex()
    logo.SetNDC()
    logo.SetTextAlign(11)
    logo.SetTextFont(61)
    logo.SetTextSize(0.045)
    logo.DrawLatex(0.15,0.94,text1)
    
    preliminary = ROOT.TLatex()
    preliminary.SetNDC()
    preliminary.SetTextAlign(11)
    preliminary.SetTextFont(52)
    preliminary.SetTextSize(0.038)
    preliminary.DrawLatex(0.24,0.94,text2)
    
def showlogoprelimsim(text):
    logo = ROOT.TLatex()
    logo.SetNDC()
    logo.SetTextAlign(11)
    logo.SetTextFont(61)
    logo.SetTextSize(0.045)
    logo.DrawLatex(0.15,0.94,text)

    preliminary = ROOT.TLatex()
    preliminary.SetNDC()
    preliminary.SetTextAlign(11)
    preliminary.SetTextFont(52)
    preliminary.SetTextSize(0.038)
    preliminary.DrawLatex(0.24,0.94,'Simulation Preliminary')

######################################## 
# Style settings (based on CMS TDRStyle)
########################################
def setpfstyle():
    pfstyle = ROOT.TStyle('pfstyle','pfstyle')

    pfstyle.SetOptStat(0)
    pfstyle.SetPalette(ROOT.kBird) # look up the color palette options in https://root.cern.ch/doc/master/classTColor.html

    # Canvas
    pfstyle.SetCanvasDefH(500)
    pfstyle.SetCanvasDefW(550)
    
    # Use plain black on white colors
    icol = 0
    pfstyle.SetFrameBorderMode(icol)
    pfstyle.SetCanvasBorderMode(icol)
    pfstyle.SetPadBorderMode(icol)
    pfstyle.SetPadColor(icol)
    pfstyle.SetCanvasColor(icol)
    pfstyle.SetStatColor(icol)

    # Set the paper & margin sizes
    pfstyle.SetPaperSize(20,26)
    pfstyle.SetPadTopMargin(0.08)
    pfstyle.SetPadRightMargin(0.17)
    pfstyle.SetPadBottomMargin(0.12)
    pfstyle.SetPadLeftMargin(0.15)

    # Use large fonts
    font = 42
    tsize = 0.045
    pfstyle.SetTextFont(font)

    # Global Title Properties
    pfstyle.SetOptTitle(0)
    pfstyle.SetTitleFont(font)
    pfstyle.SetTitleSize(tsize)
    pfstyle.SetTitleBorderSize(0)
    pfstyle.SetTitleColor(1)
    pfstyle.SetTitleTextColor(1)
    pfstyle.SetTitleFillColor(0)
    pfstyle.SetTitleFontSize(tsize)
    pfstyle.SetTitleH(0.05)
    pfstyle.SetTitleW(0.)
    pfstyle.SetTitleStyle(1001)
    pfstyle.SetTitleAlign(13)

    # Axis Titles and Labels
    ROOT.TGaxis.SetMaxDigits(3)
    pfstyle.SetTextSize(tsize)
    pfstyle.SetLabelFont(font,"x")
    pfstyle.SetTitleFont(font,"x")
    pfstyle.SetLabelFont(font,"y")
    pfstyle.SetTitleFont(font,"y")
    pfstyle.SetLabelFont(font,"z")
    pfstyle.SetTitleFont(font,"z")

    pfstyle.SetLabelSize(tsize,"x")
    pfstyle.SetTitleSize(tsize,"x")
    pfstyle.SetLabelSize(tsize,"y")
    pfstyle.SetTitleSize(tsize,"y")
    pfstyle.SetLabelSize(tsize,"z")
    pfstyle.SetTitleSize(tsize,"z")

    pfstyle.SetTitleOffset(1.1,"x")
    pfstyle.SetTitleOffset(1.3,"y")
    pfstyle.SetTitleOffset(1.35,"z")

    pfstyle.SetMarkerStyle(20)
    pfstyle.SetMarkerSize(0.9)
    pfstyle.SetLineWidth(2)
    # pfstyle.SetHistLineWidth(2.)
    pfstyle.SetLineStyleString(2,'[12 12]') # postscript dashes
    
    # Draw horizontal and vertical grids
    pfstyle.SetPadGridX(ROOT.kTRUE)
    pfstyle.SetPadGridY(ROOT.kTRUE)
    pfstyle.SetGridStyle(3)
    pfstyle.SetPadTickX(1)
    pfstyle.SetPadTickY(1)

    # Legend
    pfstyle.SetLegendBorderSize(1)
    pfstyle.SetLegendFont(font)
    # pfstyle.SetFillColor(0) # White
    # pfstyle.SetfillStyle(4000) # Transparent
   
    #Statistics
    pfstyle.SetOptFit(111)
    pfstyle.SetStatX(.80)
    pfstyle.SetStatY(0.26)
    pfstyle.SetStatBorderSize(1)
    pfstyle.SetStatW(0.16)
    pfstyle.SetStatH(0.15)
    pfstyle.SetStatFont(font)
    pfstyle.SetStatFontSize(0.01)

    # When this static function is called with sumw2=kTRUE, all new histograms will automatically activate the storage of the sum of squares of errors
    ROOT.TH1.SetDefaultSumw2()

    ROOT.gROOT.SetStyle('pfstyle')


