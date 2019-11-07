import re
import os
import copy

from math import log10, floor
from ROOT import TCanvas, TPaveText, TBox, gStyle, gROOT, kTRUE, kFALSE, gErrorIgnoreLevel, kWarning, TFile
from modules.Stack import Stack

from modules.CMS_lumi import CMS_lumi
from modules.officialStyle import officialStyle
from pdb import set_trace
officialStyle(gStyle)

def ensureDir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

class HistDrawer:
    ocan = None
    can = None
    pad = None
    padr = None

    @classmethod 
    def buildCanvas(cls):
        can = cls.can
        pad = cls.pad
        padr = cls.padr
        if not all([can, pad, padr]):
            can = cls.can = TCanvas('can', '', 800, 800) if not can else can
            can.Divide(1, 2, 0.0, 0.0)

            pad = cls.pad = can.GetPad(1) if not pad else pad
            padr = cls.padr = can.GetPad(2) if not padr else padr

            # Set Pad sizes
            pad.SetPad(0.0, 0.32, 1.0, 1.0)
            padr.SetPad(0.0, 0.00,1.0, 0.34)

            pad.SetTopMargin(0.08)
            pad.SetLeftMargin(0.16)
            pad.SetBottomMargin(0.03)
            pad.SetRightMargin(0.10)

            padr.SetBottomMargin(0.35)
            padr.SetLeftMargin(0.16)
            padr.SetRightMargin(0.10)

        can.cd()
        can.Draw()
        pad.Draw()
        padr.Draw()

        return can, pad, padr

    @classmethod
    def buildCanvasSingle(cls):
        ocan = TCanvas('ocan', '', 800, 800)
        ocan.cd()
        ocan.Draw()
        return ocan

    @staticmethod
    def datasetInfo(plot):
        year = ''
        year = '2017'
        lumi = plot.lumi/1000. if hasattr(plot, 'lumi') else 0.
        unit = plot.lumi_unit if hasattr(plot, 'lumi_unit') else 'fb'
        energy = plot.com_energy if hasattr(plot, 'com_energy') else 13
        return year, lumi, energy, unit

    @staticmethod
    def CMSPrelim(plot, pad, channel, legend='right'):
        pad.cd()
        year, lumi, energy, unit = HistDrawer.datasetInfo(plot)
        theStr = '{lumi:3.3} {unit}^{{-1}} ({energy:d} TeV)'.format(year=year, unit=unit, lumi=lumi, energy=energy)
        CMS_lumi(pad, theStr, iPosX=0)

        lowY = 0.78

        r = pad.GetRightMargin()
        l = pad.GetLeftMargin()
        posX = l + 0.045*(1-l-r)
        posXhigh = 0.25

#        if legend == 'left':
        # posX = 1. - r - 0.09
        posX = 1. - r - 0.15
        # posXhigh = 1. - r - 0.03
        posXhigh = 1. - r - 0.09

        plot.chan = TPaveText(posX, lowY, posXhigh, lowY+0.15, "NDC")
        plot.chan.SetBorderSize(0)
        plot.chan.SetFillStyle(0)
        plot.chan.SetTextAlign(12)
        plot.chan.SetTextSize(0.6*pad.GetTopMargin()) # To have it the same size as CMS_lumi
        plot.chan.SetTextFont(42)
        plot.chan.AddText(channel)
        plot.chan.Draw('same')


    unitpat = re.compile('.*\((.*)\)\s*$')

    keeper = []

    @staticmethod
    def draw(plot, do_ratio=True, channel='e#mu#mu', plot_dir='/plots/', 
             plot_name=None, SetLogy=0, 
             blindxmin=None, blindxmax=None, unit=None, server='starseeker', region = 'DY', channel_dir = 'mmm', dataset = '2017'):
        print plot
        Stack.STAT_ERRORS = True

        can = pad = padr = None

        if do_ratio:
            can, pad, padr = HistDrawer.buildCanvas()
            pad.cd()
            pad.SetLogy(SetLogy)
        else:
            can = HistDrawer.buildCanvasSingle()
            pad = can
            pad.cd()
            pad.SetLogy(SetLogy)


        plot.DrawStack('HIST', print_norm=plot.name=='_norm_', ymin=0.1) # magic word to print integrals in legend

        h = plot.supportHist
        h.GetXaxis().SetLabelColor(1)
        # h.GetXaxis().SetLabelSize(1)

        unitsperbin = h.GetXaxis().GetBinWidth(1)
        ytitle = 'Events'
        if unit:
            round_to_n = lambda x, n: round(x, -int(floor(log10(abs(x)))) + (n - 1))
            ytitle += round_to_n(unitsperbin, 3)

        h.GetYaxis().SetTitle('Events')
        h.GetYaxis().SetTitleOffset(1.4)
        h.GetXaxis().SetTitleOffset(2.0)

        if do_ratio:
            padr.cd()
            ratio = copy.deepcopy(plot)
            ratio.legendOn = True
            ratio.STAT_ERRORS = True

        if blindxmin or blindxmax:
            if not blindxmin:
                blindxmin = 0
            if not blindxmax:
                blindxmax = plot.stack.totalHist.GetXaxis().GetXmax()
            if do_ratio:
                ratio.Blind(blindxmin, blindxmax, True)
            plot.Blind(blindxmin, blindxmax, False)

        if do_ratio:
            ratio.DrawDataOverMCMinus1(-0.5, 0.5)
            hr = ratio.dataOverMCHist

            # Gymnastics to get same label sizes etc in ratio and main plot
            ytp_ratio = 2.
            xtp_ratio = 2.

            # hr.GetYaxis().SetNdivisions(4)

            hr.GetYaxis().SetTitleSize(h.GetYaxis().GetTitleSize() * xtp_ratio)
            hr.GetXaxis().SetTitleSize(h.GetXaxis().GetTitleSize() * ytp_ratio)
            
            hr.GetYaxis().SetTitleOffset(h.GetYaxis().GetTitleOffset() / xtp_ratio)
            hr.GetXaxis().SetTitleOffset(h.GetXaxis().GetTitleOffset() / ytp_ratio)

            hr.GetYaxis().SetLabelSize(h.GetYaxis().GetLabelSize() * xtp_ratio)
            hr.GetXaxis().SetLabelSize(h.GetXaxis().GetLabelSize() * ytp_ratio)

            h.GetXaxis().SetLabelColor(0)
            h.GetXaxis().SetLabelSize(0)
            padr.Update()

        # blinding
        if blindxmin or blindxmax:
            pad.cd()
            max = plot.stack.totalHist.GetMaximum()
            box = TBox(blindxmin, 0,  blindxmax, max)
            box.SetFillColor(1)
            box.SetFillStyle(3004)
            box.Draw()
            HistDrawer.keeper.append(box)

        HistDrawer.CMSPrelim(plot, pad, channel, legend=plot.legendPos)
        can.cd()
        
        gErrorIgnoreLevel = kWarning
        h.GetYaxis().SetRangeUser(0, pad.GetUymax() * 1.)
        plotname = plot_name if plot_name else plot.name



        if 'dz' in plotname:
            pad.SetLogx(True)
            padr.SetLogx(True)

        if not os.path.exists(plot_dir + '/pdf/'):
            os.mkdir(plot_dir + '/pdf/')
            os.mkdir(plot_dir + '/pdf/linear/')
            os.mkdir(plot_dir + '/pdf/log/')
        if not os.path.exists(plot_dir + '/root/'):
            os.mkdir(plot_dir + '/root/')
            os.mkdir(plot_dir + '/root/linear/')
            os.mkdir(plot_dir + '/root/log')
        if not os.path.exists(plot_dir + '/png/'):
            os.mkdir(plot_dir + '/png/')
            os.mkdir(plot_dir + '/png/linear/')
            os.mkdir(plot_dir + '/png/log/')
	if not os.path.exists(plot_dir + '/datacards/'):
            os.mkdir(plot_dir + '/datacards/')	
        can.SaveAs(plot_dir + '/pdf/linear/'  + plotname  + '.pdf')
        can.SaveAs(plot_dir + '/root/linear/' + plotname  + '.root')
        can.SaveAs(plot_dir + '/png/linear/'  + plotname  + '.png')

        if server == "starseeker":
            if dataset == '2017':
                t3_dir='/home/dehuazhu/t3work/3_figures/1_DataMC/FinalStates/'+channel_dir+'/'+region.name 
            if dataset == '2018':
                t3_dir='/home/dehuazhu/t3work/3_figures/1_DataMC/FinalStates/2018/'+channel_dir+'/'+region.name 
            can.SaveAs(t3_dir + '/pdf/linear/'  + plotname  + '.pdf')
            can.SaveAs(t3_dir + '/root/linear/' + plotname  + '.root')
            can.SaveAs(t3_dir + '/png/linear/'  + plotname  + '.png')


        # Also save with log y
        h.GetYaxis().SetRangeUser(pad.GetUymax() * 5./1000000., pad.GetUymax() * 1000.)
        pad.SetLogy(True)
        can.SaveAs(plot_dir + '/png/log/'  + plotname + '_log.png')
        can.SaveAs(plot_dir + '/root/log/' + plotname + '_log.root')
        can.SaveAs(plot_dir + '/pdf/log/'  + plotname + '_log.pdf')
        if server == "starseeker":
            can.SaveAs(t3_dir + '/pdf/log/'  + plotname  + '_log.pdf')
            can.SaveAs(t3_dir + '/root/log/' + plotname  + '_log.root')
            can.SaveAs(t3_dir + '/png/log/'  + plotname  + '_log.png')
        pad.SetLogy(0)
        if 'dz' in plotname:
            pad.SetLogx(False)
            padr.SetLogx(False)
#        return ratio

        #VS 10/30/19: dump all histo's in a root file (=datacard)
        s_pad  = can.GetPrimitive('can_1')
        s_list = pad.GetListOfPrimitives()

        if server == "starseeker":
            if dataset == '2017':
                t3_dir='/home/dehuazhu/t3work/3_figures/1_DataMC/FinalStates/'+channel_dir+'/'+region.name 
            if dataset == '2018':
                t3_dir='/home/dehuazhu/t3work/3_figures/1_DataMC/FinalStates/2018/'+channel_dir+'/'+region.name 
            datacard = TFile.Open(t3_dir + '/datacards/' + plotname  + '.datacard.root', 'recreate')
        else:
            datacard = TFile.Open(plot_dir + '/datacards/' + plotname  + '.datacard.root', 'recreate')

        datacard.cd()

        for s_h in s_list:
            s_h_name = s_h.GetName()
            if 'HN3L' in s_h_name:
                s_h_name = re.sub('.*HN3L_M_', 'M', s_h_name)
                s_h_name = re.sub('_V_0', '_V', s_h_name)
                s_h_name = re.sub('_mu_massiveAndCKM_LO', '_maj', s_h_name)
                s_h_name = re.sub('_mu_Dirac_massiveAndCKM_LO', '_dir', s_h_name)
                s_h_name = re.sub('_mu_Dirac_cc_massiveAndCKM_LO', '_dir_cc', s_h_name)
                s_h_name = re.sub('_e_massiveAndCKM_LO', '_maj', s_h_name)
                s_h_name = re.sub('_e_Dirac_massiveAndCKM_LO', '_dir', s_h_name)
                s_h_name = re.sub('_e_Dirac_cc_massiveAndCKM_LO', '_dir_cc', s_h_name)
                s_h.SetName(s_h_name)
                s_h.Write()
            elif 'data' in s_h_name:
                s_h.SetName('data_obs')
                s_h.Write()
            elif 'stack' in s_h_name:
                s_h.SetName('stack')
                s_h.Write()
            elif 'TFrame' in s_h_name:
                continue
            else: 
                continue #ToDo
        datacard.ls()
        datacard.Close()

    drawRatio = draw


