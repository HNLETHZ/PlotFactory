########################## 
# Import relevant modules
##########################
import ROOT
import numpy as np
from glob import glob
import time
from array import array
import sys

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

def showTitle(text):
    logo = ROOT.TLatex()
    logo.SetNDC()
    logo.SetTextAlign(31)
    logo.SetTextFont(42)
    logo.SetTextSize(0.04)
    logo.DrawLatex(0.81,0.87,text)

def showlogopreliminary():
    logo = ROOT.TLatex()
    logo.SetNDC()
    logo.SetTextAlign(11)
    logo.SetTextFont(61)
    logo.SetTextSize(0.045)
    logo.DrawLatex(0.15,0.94,'CMS')
    
    preliminary = ROOT.TLatex()
    preliminary.SetNDC()
    preliminary.SetTextAlign(11)
    preliminary.SetTextFont(52)
    preliminary.SetTextSize(0.038)
    preliminary.DrawLatex(0.24,0.94,'Preliminary')
    
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
    # font = 62
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
    pfstyle.SetMarkerSize(0.5)
    pfstyle.SetLineWidth(1)
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
    pfstyle.SetPaintTextFormat('4.2f')
    ROOT.TH1.SetDefaultSumw2()

    ROOT.gROOT.SetStyle('pfstyle')


