#!/bin/env python

def csvImporter(fname):
    import ROOT as r
    if not args.d:
        r.gROOT.SetBatch(r.kTRUE)
    headers="count/I:gthShift/I:phase/F:phaseNS/F:gthPhase/F:gthPhaseNS/F:pllLockCnt/I:bc0Locked/I:ttcSglErrCnt/I:ttcDblErrCnt/I:bestLock/I"
    #0,0,234,4.352678,214,3.980655,0,1,0,0,0
    
    f = r.TFile("CTP7PhaseShift_{}.root".format(fname),"RECREATE");

    t = r.TTree("ntuple","data from CTP7 phase shifting");
    t.ReadFile("{}.csv".format(fname),headers)
    f.Write()
    h1 = r.TH2D("h1","",25000,-0.5,24999.5, 2,-0.5,1.5)
    h2 = r.TH2D("h2","",25000,-0.5,24999.5, 20,-0.5,19.5)
    h3 = r.TH2D("h3","",25000,-0.5,24999.5, 5000,-0.5,4999.5)
    h4 = r.TH2D("h4","",25000,-0.5,24999.5, 250,-0.5,249.5)
    can = r.TCanvas("can","",1000,1000)
    can.Divide(1,4)
    can.cd(1)
    t.Draw("bestLock:gthShift>>h1","","colz")
    can.cd(2)
    t.Draw("pllLockCnt:gthShift>>h2","","colz")
    can.cd(3)
    t.Draw("phase:gthShift>>h3","","colz")
    can.cd(4)
    t.Draw("gthPhase:gthShift>>h4","","colz")
    if args.d:
        raw_input("enter to continue")
    f.Close()

    if args.d:
        can.SaveAs("phase_shifting_{}.png".format(args.fname))
        can.SaveAs("phase_shifting_{}.pdf".format(args.fname))
def main(args):
    csvImporter(args.fname)

if __name__ == '__main__':
    import argparse
    import sys, os
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument("fname", help="File name time", type=str)
    parser.add_argument("-d",    help="debug", action='store_true')

    args = parser.parse_args()

    main(args)
