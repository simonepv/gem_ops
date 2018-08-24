#!/bin/env python

def drawConfTimes(tree,color,tmin,tmax,minval,maxval):
    import ROOT as r
    from gcROOT import *
    for tc in tree:
        if tc.date < tmin or tc.date > tmax:
            continue
        l = r.TLine(tc.date,minval,tc.date,maxval)
        l.SetLineWidth(1)
        l.SetLineStyle(2)
        l.SetLineColor(color)
        l.Draw("")

def drawRatios(hist1,opts1,hist2,opts2,hist3,opts3,can,subcan,tcdsConf,gemConf,tmin,tmax):
    import ROOT as r
    from gcROOT import *
    val=1
    can.cd(subcan)
    plotPad  = r.TPad("plotPad", "plotPad",0.0,0.5,1.0,1.0)
    plotPad.SetFillStyle(4000)
    plotPad.SetFrameFillStyle(4000)
    plotPad.SetTopMargin(0.025)
    plotPad.SetBottomMargin(0.00)
    plotPad.SetLeftMargin(0.075)
    plotPad.SetRightMargin(0.05)
    plotPad.Draw()
    plotPad.cd()
    hist1.Draw(opts1)
    r.gPad.SetLogy(r.kFALSE)
    r.gPad.SetLogz(r.kTRUE)
    r.gStyle.SetPalette(r.kTemperatureMap)
    r.gPad.SetGridy(r.kTRUE)
    r.gPad.SetGridx(r.kTRUE)
    
    can.cd(subcan)
    ratioPad = r.TPad("ratioPad","ratioPad",0.0,0.0,1.0,0.25)
    ratioPad.SetFillStyle(4000)
    ratioPad.SetFrameFillStyle(4000)
    ratioPad.SetTopMargin(0.00)
    ratioPad.SetBottomMargin(0.1)
    ratioPad.SetLeftMargin(0.075)
    ratioPad.SetRightMargin(0.05)
    ratioPad.Draw()
    ratioPad.cd()
    hist2.Draw(opts2)
    r.gPad.SetLogy(r.kFALSE)
    r.gPad.SetLogz(r.kTRUE)
    r.gStyle.SetPalette(r.kTemperatureMap)
    r.gPad.SetGridy(r.kTRUE)
    r.gPad.SetGridx(r.kTRUE)

    can.cd(subcan)
    lvPad = r.TPad("lvPad","lvPad",0.0,0.25,1.0,0.5)
    lvPad.SetFillStyle(4000)
    lvPad.SetFrameFillStyle(4000)
    lvPad.SetTopMargin(0.0)
    lvPad.SetBottomMargin(0.0)
    lvPad.SetLeftMargin(0.075)
    lvPad.SetRightMargin(0.05)
    lvPad.Draw()
    lvPad.cd()
    hist3.Draw(opts3)
    if tcdsConf:
        drawConfTimes(tcdsConf,r.kRed,tmin,tmax,0,250)
    if gemConf:
        drawConfTimes(gemConf,r.kBlue,tmin,tmax,250,500)
    r.gPad.SetLogy(r.kFALSE)
    r.gPad.SetLogz(r.kTRUE)
    r.gStyle.SetPalette(r.kCMYK)
    # r.gStyle.SetPalette(r.kInvertedDarkBodyRadiator)
    r.gPad.SetGridy(r.kTRUE)
    r.gPad.SetGridx(r.kTRUE)

def main(args):
    import ROOT as r
    from gcROOT import *

    if not args.d:
        r.gStyle.SetOptStat(0)

    f = r.TFile("CTP7PhaseMonData_{}.root".format(args.fname),"read")
    t = f.Get("ntuple")
    if args.d:
        print(f)
        print(t)

    lhcClk   = f.Get("LHC_CLOCK_STABLE")
    tcdsClk  = f.Get("TCDS_FREQMON")
    cmsClk   = f.Get("CMS_CLK_TYPE")
    tcdsConf = f.Get("TCDS_CONF")
    gemConf  = f.Get("GEM_CONF")

    tc = r.TCanvas("test","",1400,900)
    c  = r.TCanvas("can","",1400,900)
    c.Divide(4,2)
    c.cd(1)

    h1ds = [
        ["mmcmPhase","MMCM Phase"],
        ["mmcmPhaseMean","MMCM Phase Mean"],
        ["gthPhase","GTH Phase"],
        ["gthPhaseMean","GTH Phase Mean"],
    ]
    histos = []
    hoff = 0
    for h in range(4):
        print("h offset is {}, hist index is {}, histos index is {}, canvas index is {}".format(hoff,h,h+1,h+1))
        histos.append(r.TH1D("h{}".format(h+1),"",5000,0,5000))
        tc.cd()
        t.Draw("{:s}>>h{:d}".format(h1ds[h][0],h+1),"","")
        c.cd(h+1)
        histos[h].SetTitle(h1ds[h][1])
        histos[h].Draw("")
        r.gPad.SetLogy(r.kTRUE)
        r.gPad.SetGridy(r.kTRUE)
        r.gPad.SetGridx(r.kTRUE)
        hoff+=1

    tmin=1.52975e9
    tmax=1.53015e9

    if args.tmin:
        print("setting minimum time to: {:f}".format(args.tmin))
        tmin = args.tmin
    if args.tmax:
        print("setting maximum time to: {:f}".format(args.tmax))
        tmax = args.tmax

    print("minimum time is: {:f}".format(tmin))
    print("maximum time is: {:f}".format(tmax))

    h2ds = [
        ["mmcmPhase:date"    ,"MMCM Phase"],
        ["mmcmPhaseMean:date","MMCM Phase Mean"],
        ["gthPhase:date"     ,"GTH Phase"],
        ["gthPhaseMean:date" ,"GTH Phase Mean"],
    ]

    if args.d:
        print("h offset is {}".format(hoff))
    for h in range(4):
        if args.d:
            print("h offset is {}, hist index is {}, histos index is {}, canvas index is {}".format(hoff,hoff,hoff+1,hoff+1))
        histos.append(r.TH2D("h{:d}".format(hoff+1),"",5000,tmin,tmax,5000,0,5000))

        tc.cd()
        t.Draw("{:s}>>h{:d}".format(h2ds[h][0],hoff+1),"date>{:d}&&date<{:d}".format(int(tmin),int(tmax)),"colz")
        c.cd(hoff+1)
        # histos[hoff].SetTitle("{:s} vs. Time".format(h2ds[h][1]))
        histos[hoff].SetTitle("")
        histos[hoff].GetYaxis().SetTitle(h2ds[h][1])
        histos[hoff].GetXaxis().SetTitle("Unix timestamp [UTC]")
        if args.d:
            print(histos[hoff].GetYaxis().GetTitleSize())
        histos[hoff].GetYaxis().SetTitleSize(0.04)
        histos[hoff].Draw("colz")
        if tcdsConf:
            drawConfTimes(tcdsConf,r.kRed,tmin,tmax,0,250)
        if gemConf:
            drawConfTimes(gemConf,r.kBlue,tmin,tmax,250,500)
        r.gPad.SetLogz(r.kTRUE)
        r.gStyle.SetPalette(r.kTemperatureMap)
        r.gPad.SetGridy(r.kTRUE)
        r.gPad.SetGridx(r.kTRUE)
        hoff+=1

    raw_input("enter")
    c.SaveAs("phase_stability_{}.png".format(args.fname))
    c.SaveAs("phase_stability_{}.pdf".format(args.fname))

    c.Clear()
    c.Divide(2,2)

    h2ds = [
        # ["ttcSglErr:date","TTC Single Bit Errors",[100,-100,0x10000]],
        # ["ttcDblErr:date","TTC Double Bit Errors",[100,-100,0x10000]],
        # ["killMask:date", "Kill mask",            [100,-100,0x400  ]],
        # ["scaReady:date", "SCA Status",           [100,-100,0x400  ]],
        ["bufMinDepth:date","TTC buffer min depth",  [10,-0.5,9.5]],
        ["bufMaxDepth:date", "TTC buffer max depth", [10,-0.5,9.5]],
        ["bufOOS:date", "TTC Buffer OOS",            [2,-0.5,1.5 ]],
        ["bufBusy:date", "TTC Buffer BUSY",          [2,-0.5,1.5 ]],
        # ["ttsState:date", "TTS State",            [16, -0.5,15.5   ]],
        ["mmcmPhaseMean:date","MMCM Phase Mean",  [500,-0.5,499.5  ]],
    ]
    if args.d:
        print("h offset is {}".format(hoff))
    comphisto = r.TH2D("comphisto","",1000,tmin,tmax,h2ds[4][2][0],h2ds[4][2][1],h2ds[4][2][2])
    comphisto.SetTitle("")
    comphisto.GetXaxis().SetTitle("Time [UTC]")
    comphisto.GetYaxis().SetTitle("MMCM Phase Mean")
    if args.d:
        print(comphisto.GetYaxis().GetTitleSize())
    comphisto.GetYaxis().SetTitleSize(0.0775)
    comphisto.GetYaxis().SetLabelSize(0.0775)
    comphisto.GetYaxis().SetTitleOffset(0.3)
    comphisto.GetXaxis().SetTitleSize(0.07)
    comphisto.GetXaxis().SetLabelSize(0.075)
    tc.cd()
    t.Draw("{:s}>>comphisto".format(h2ds[4][0]),"","colz")

    clkhisto = r.TH2D("clkhisto","",1000,tmin,tmax,2500,4.0075E7,4.008E7)
    if args.d:
        print(clkhisto)
    clkhisto.SetTitle("")
    clkhisto.GetXaxis().SetTitle("Time [UTC]")
    clkhisto.GetYaxis().SetTitle("Clock frequency")
    if args.d:
        print(clkhisto.GetYaxis().GetTitleSize())
    clkhisto.GetYaxis().SetTitleSize(0.0775)
    clkhisto.GetYaxis().SetLabelSize(0.0775)
    clkhisto.GetYaxis().SetTitleOffset(0.3)
    clkhisto.GetXaxis().SetTitleSize(0.07)
    clkhisto.GetXaxis().SetLabelSize(0.075)
    tc.cd()
    if tcdsClk:
        tcdsClk.Draw("freq:date>>clkhisto","","colz")
    for h in range(4):
        if args.d:
            print("h offset is {}, hist index is {}, histos index is {}, canvas index is {}".format(hoff,hoff,hoff+1,h+1))
        histos.append(r.TH2D("h{:d}".format(hoff+1),"",1000,tmin,tmax,h2ds[h][2][0],h2ds[h][2][1],h2ds[h][2][2]))

        tc.cd()
        t.Draw("{:s}>>h{:d}".format(h2ds[h][0],hoff+1),"","colz")
        c.cd(h+1)
        # histos[hoff].SetTitle("{:s} vs. Time".format(h2ds[h][1]))
        histos[hoff].SetTitle("")
        histos[hoff].GetYaxis().SetTitle(h2ds[h][1])
        histos[hoff].GetYaxis().SetTitleOffset(0.4)
        histos[hoff].GetYaxis().SetTitleSize(0.06)
        drawRatios(histos[hoff],"colz",clkhisto,"colz",comphisto,"colz",c,h+1,tcdsConf,gemConf,tmin,tmax)
        # histos[hoff].Draw("colz")
        hoff+=1

    raw_input("enter")
    c.SaveAs("error_stability_{}.png".format(args.fname))
    c.SaveAs("error_stability_{}.pdf".format(args.fname))
    c.cd(1)

    c.Clear()
    c.Divide(3,3)
    infos = ["OH{:d}:date","OH{:d} Errors"]
    # ["scaReady:date", "SCA Status",           [100,-100,0x400  ]],

    tc.cd()
    comphisto = r.TH2D("comphisto2","",1000,tmin,tmax,h2ds[2][2][0],h2ds[2][2][1],h2ds[2][2][2])
    t.Draw("{:s}>>comphisto2".format(h2ds[2][0]),"","colz")
    comphisto.SetTitle("")
    comphisto.GetXaxis().SetTitle("Time [UTC]")
    comphisto.GetYaxis().SetTitle("SCA Status Ready")
    comphisto.GetYaxis().SetTitleSize(0.0775)
    comphisto.GetYaxis().SetLabelSize(0.0775)
    comphisto.GetYaxis().SetTitleOffset(0.3)
    comphisto.GetXaxis().SetTitleSize(0.07)
    comphisto.GetXaxis().SetLabelSize(0.075)

    if args.d:
        print("h offset is {}".format(hoff))
    linkmap = {
      0: "GEMINIm01L1",
      1: "GEMINIm01L2",
      2: "GEMINIm27L1",
      3: "GEMINIm27L2",
      4: "GEMINIm28L1",
      5: "GEMINIm28L2",
      6: "GEMINIm29L1",
      7: "GEMINIm29L2",
      8: "GEMINIm30L1",
      9: "GEMINIm30L2",
    }
    for h in range(8):
        if args.d:
            print("h offset is {}, hist index is {}, histos index is {}, canvas index is {}".format(hoff,hoff,hoff+1,h+1))
        histos.append(r.TH2D("h{:d}".format(hoff+1),"",1000,tmin,tmax,25,-0.5,24.5))
        vfatLVInfo   = f.Get("{}_VFAT".format(linkmap[h+2]))
        oh2vLVInfo   = f.Get("{}_OH2V".format(linkmap[h+2]))
        oh4vLVInfo   = f.Get("{}_OH4V".format(linkmap[h+2]))

        lvhisto = r.TH2D("lvhisto{}".format(linkmap[h+2]),"",1000,tmin,tmax,100,-0.5,9.5)
        lvhisto.SetTitle("")
        lvhisto.GetXaxis().SetTitle("")
        lvhisto.GetYaxis().SetTitle("VFAT LV")
        lvhisto.GetYaxis().SetTitleSize(0.0775)
        lvhisto.GetYaxis().SetLabelSize(0.0775)
        lvhisto.GetYaxis().SetTitleOffset(0.3)
        tc.cd()
        if vfatLVInfo:
            vfatLVInfo.Draw("{:s}>>lvhisto{}".format("vmon:date",linkmap[h+2]),"","colz")
        # raw_input("continue")
        tc.cd()
        t.Draw("{:s}>>h{:d}".format(infos[0].format(h+2),hoff+1),"","colz")
        c.cd(h+1)
        histos[hoff].SetTitle("")
        histos[hoff].GetYaxis().SetTitle(infos[1].format(h+2))
        histos[hoff].GetYaxis().SetTitleOffset(0.4)
        histos[hoff].GetYaxis().SetTitleSize(0.06)
        drawRatios(histos[hoff],"colz",clkhisto,"colz",comphisto,"colz",c,h+1,tcdsConf,gemConf,tmin,tmax)
        hoff+=1

    raw_input("enter")
    c.SaveAs("link_stability_{}.png".format(args.fname))
    c.SaveAs("link_stability_{}.pdf".format(args.fname))
    c.cd(1)
    
if __name__ == '__main__':
    import argparse
    import sys, os, time
    from dateutil import parser

    opts = argparse.ArgumentParser()

    opts.add_argument("fname",  help="File name time",      type=str)
    opts.add_argument("-tmin",  help="Minimum time",        type=float)
    opts.add_argument("-tmax",  help="Maximum time",        type=float)
    opts.add_argument("-stmin", help="String minimum time", type=str)
    opts.add_argument("-stmax", help="String maximum time", type=str)
    opts.add_argument("-d",     help="debug", action='store_true')

    args = opts.parse_args()

    if args.stmin:
        # args.tmin = time.mktime(datetime.datetime.strptime(args.stmin, '%Y.%b.%d %I.%M.%S').timetuple())
        args.tmin = time.mktime(parser.parse(args.stmin).timetuple())
        print("Parsed {} as {}".format(args.stmin,args.tmin))
    if args.stmax:
        # args.tmax = time.mktime(datetime.datetime.strptime(args.stmax, '%Y.%b.%d %I.%M.%S').timetuple())
        args.tmax = time.mktime(parser.parse(args.stmax).timetuple())
        print("Parsed {} as {}".format(args.stmax,args.tmax))

    main(args)
