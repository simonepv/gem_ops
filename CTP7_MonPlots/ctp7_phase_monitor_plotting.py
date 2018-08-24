#!/bin/env python

import ROOT as r

def timeRunInfoDBInfoCorrelator(subsystem,datafile):
    """
    DATE,RUN,VALUE
    CLOCK_TYPE_AT_PRECONFIGURE.csv
    GEM_CONF_TIMES.csv
    LHC_CLOCK_STABLE.csv
    TCDS_CONF_TIMES.csv
    """
    import time,datetime,csv,re
    from dateutil import parser
    with open(datafile,'rb') as dbdata:
        reader = csv.DictReader(dbdata)
        rowcnt=0
        dbtuple = r.TTree(subsystem,"monitoring info from {}".format(subsystem))
        with open("dbtuple.tmp","w") as tmpfile:
            for row in reader:
                date = row["DATE"]
                val  = row["VALUE"]
                run  = row["RUN"]
                statetime = time.mktime(parser.parse(date).timetuple())
                tmpfile.write("{}\t'{}'\t{}\n".format(int(statetime),val,run))
                pass
            pass
        dbtuple.ReadFile('dbtuple.tmp',"date/I:value/C:run/I")
    return dbtuple


def timeDBInfoCorrelator(subsystem,datafile):
    """
    subsystem should be one of:
    TCDS_STATE
    GEM_STATE
    TCDS_CLOCK_SOURCE
    CMS_CLOCK_SOURCE
    LHC_CLOCK_STABLE
    """
    import time,datetime,csv,re
    with open(datafile,'rb') as dbdata:
        reader = csv.DictReader(dbdata)
        rowcnt=0
        dbtuple = r.TTree(subsystem,"monitoring info from {}".format(subsystem))
        with open("dbtuple.tmp","w") as tmpfile:
            for row in reader:
                val = row["STRING_VALUE"]
                splitstr=re.split(r',| |-|\.',row["TIME"])
                newtime="{}-{}-{} {}.{}.{}.{} {}".format(splitstr[0],splitstr[1],splitstr[2],splitstr[3],splitstr[4],splitstr[5],splitstr[6][:6],splitstr[7])
                statetime = time.mktime(datetime.datetime.strptime(newtime, '%d-%b-%y %I.%M.%S.%f %p').timetuple())
                tmpfile.write("{}\t'{}'\n".format(int(statetime),val))
                pass
            pass
        dbtuple.ReadFile('dbtuple.tmp',"date/I:value/C")
    return dbtuple

def timeCondDBInfoCorrelator(subsystem,datafile):
    """
    subsystem should be one of:
    TCDS_STATE
    GEM_STATE
    TCDS_CLOCK_SOURCE
    CMS_CLOCK_SOURCE
    LHC_CLOCK_STABLE
    """
    import time,datetime,csv,re
    with open(datafile,'rb') as dbdata:
        reader = csv.DictReader(dbdata)
        rowcnt=0
        dbtuple = r.TTree(subsystem,"monitoring info from {}".format(subsystem))
        with open("dbtuple.tmp","w") as tmpfile:
            for row in reader:
                val       = row["FREQUENCY"]
                statetime = row["TIMESTAMP"]
                tmpfile.write("{}\t{}\n".format(int(statetime),val))
                pass
            pass
        dbtuple.ReadFile('dbtuple.tmp',"date/I:value/F")
    return dbtuple

def timeTCDSFreqCorrelator(datafile):
    """
    ROW,WEIGHT,TIMESTAMP,FREQUENCY
    1,1,1529488151,4.0079011E7
    """
    import time,datetime,csv,re
    with open(datafile,'rb') as dbdata:
        reader = csv.DictReader(dbdata)
        rowcnt=0
        dbtuple = r.TTree("TCDS_FREQMON","TCDS clock frequency info")
        with open("dbtuple.tmp","w") as tmpfile:
            for row in reader:
                val       = row["FREQUENCY"]
                statetime = row["TIMESTAMP"]
                tmpfile.write("{}\t{}\n".format(int(statetime),val))
                pass
            pass
        dbtuple.ReadFile('dbtuple.tmp',"date/I:freq/F")
    return dbtuple

def timeTCDSFreqMonCorrelator(datafile):
    """
    DATE,VALUE
    4.0079011E7
    """
    import time,datetime,csv,re
    from dateutil import parser
    with open(datafile,'rb') as dbdata:
        reader = csv.DictReader(dbdata)
        rowcnt=0
        dbtuple = r.TTree("TCDS_FREQMON","TCDS clock frequency info")
        with open("dbtuple.tmp","w") as tmpfile:
            for row in reader:
                val       = row["VALUE"]
                statetime = row["DATE"]
                statetime = time.mktime(parser.parse(statetime).timetuple())
                tmpfile.write("{}\t{}\n".format(int(statetime),val))
                pass
            pass
        dbtuple.ReadFile('dbtuple.tmp',"date/I:freq/F")
    return dbtuple

def timeLVInfoCorrelator(chamber,subsystem):
    """
    subsystem should be one of:
    VFAT
    OH2V
    OH4V
    """
    import time,datetime,csv,re
    from dateutil import parser
    with open("{}_{}.csv".format(chamber,subsystem),'rb') as dbdata:
        reader = csv.DictReader(dbdata)
        rowcnt=0
        dbtuple = r.TTree("{}_{}".format(chamber,subsystem),"LV monitoring info from {} for {}".format(chamber,subsystem))
        pimon = -1
        pvmon = -1
        with open("dbtuple.tmp","w") as tmpfile:
            for row in reader:
                date = row["Date"]
                imon = row["ACTUAL_IMON"]
                vmon = row["ACTUAL_VMON"]
                if imon == 'None':
                    imon = pimon
                if vmon == 'None':
                    vmon = pvmon
                pimon = imon
                pvmon = vmon
                # smart guessing, since the DB query returned some without the usecs
                statetime = time.mktime(parser.parse(date).timetuple())
                # statetime = time.mktime(datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f').timetuple())
                tmpfile.write("{}\t{}\t{}\n".format(int(statetime)+7200,float(vmon),float(imon)))
                pass
            pass
        dbtuple.ReadFile('dbtuple.tmp',"date/I:vmon/F:imon/F")
    return dbtuple


def main(args):

    with file("ctp7_phase_monitor_{}.log".format(args.fname), 'r') as f:
        line = f.readline()
        nCols = len(line.split())
    if nCols == 16:
        ## default, nCols = 16
        headers="date/I:gthPhase/I:mmcmPhase/I:gthPhaseMean/I:mmcmPhaseMean/I:ttcSglErr/I:ttcDblErr/I:scaReady/I:OH2/I:OH3/I:OH4/I:OH5/I:OH6/I:OH7/I:OH8/I:OH9/I"
    elif nCols == 17:
        ## added ttsState nCols = 17
        headers="date/I:gthPhase/I:mmcmPhase/I:gthPhaseMean/I:mmcmPhaseMean/I:ttcSglErr/I:ttcDblErr/I:scaReady/I:OH2/I:OH3/I:OH4/I:OH5/I:OH6/I:OH7/I:OH8/I:OH9/I:ttsState/I"
    elif nCols == 23:
        ## 1.15.1 nCols = 23
        headers="date/I:gthPhase/I:mmcmPhase/I:gthPhaseMean/I:mmcmPhaseMean/I:ttcSglErr/I:ttcDblErr/I:scaReady/I:OH2/I:OH3/I:OH4/I:OH5/I:OH6/I:OH7/I:OH8/I:OH9/I:ttsState/I:killMask/I:bufDepth/I:bufMinDepth/I:bufMaxDepth/I:bufOOS/I:bufBusy/I"
    elif nCols == 29:
        ## 1.15.2 nCols = 29
        headers="date/I:gthPhase/I:mmcmPhase/I:gthPhaseMean/I:mmcmPhaseMean/I:ttcSglErr/I:ttcDblErr/I:scaReady/I:OH2/I:OH3/I:OH4/I:OH5/I:OH6/I:OH7/I:OH8/I:OH9/I:ttsState/I:killMask/I:bufDepth/I:bufMinDepth/I:bufMaxDepth/I:bufOOS/I:bufBusy/I:oosCnt/I:uvfCnt/I:ovfCnt/I:lastOOSSec/I:oosDurLast/I:oosDurMax/I"
    else:
        headers="date/I:gthPhase/I:mmcmPhase/I:gthPhaseMean/I:mmcmPhaseMean/I:ttcSglErr/I:ttcDblErr/I:scaReady/I:OH2/I:OH3/I:OH4/I:OH5/I:OH6/I:OH7/I:OH8/I:OH9/I:ttsState/I"

    f = r.TFile("CTP7PhaseMonData_{}.root".format(args.fname),"RECREATE");

    # for ch in range(27,31):
    #     for lay in range(1,3):
    #         vfat_vmon  = timeLVInfoCorrelator("GEMINIm{}L{}".format(ch,lay), 'VFAT')
    #         oh2v_vmon  = timeLVInfoCorrelator("GEMINIm{}L{}".format(ch,lay), 'OH2V')
    #         oh4v_vmon  = timeLVInfoCorrelator("GEMINIm{}L{}".format(ch,lay), 'OH4V')
    #         f.Write()
    
    # lhcClockTuple        = timeDBInfoCorrelator("LHC_CLOCK_STABLE",'export_lhc_clock_stable.csv')
    # tcdsClockTuple        = timeTCDSFreqCorrelator('tcds_clock_frequency.csv')
    # tcdsClockTuple       = timeDBInfoCorrelator("TCDS_CLOCK_STATE",'export_tcds_clock_source.csv')
    # cmsClockTuple        = timeDBInfoCorrelator("CMS_CLOCK_STATE", 'export_clock_state.csv')
    # tcdsConfiguringTuple = timeDBInfoCorrelator("TCDS_CONFIGURING",'export_tcds_configuring.csv')
    # gemConfiguringTuple  = timeDBInfoCorrelator("GEM_CONFIGURING", 'export_gem_configuring.csv')


    tcdsClockFreqTuple   = timeTCDSFreqMonCorrelator("TCDS_FREQMON.csv")
    tcdsClockSrcTuple    = timeRunInfoDBInfoCorrelator("CMS_CLK_TYPE","CLOCK_TYPE_AT_PRECONFIGURE.csv")
    lhcClockTuple        = timeRunInfoDBInfoCorrelator("LHC_CLK_STABLE","LHC_CLOCK_STABLE.csv")
    gemConfiguringTuple  = timeRunInfoDBInfoCorrelator("GEM_CONF","GEM_CONF_TIMES.csv")
    tcdsConfiguringTuple = timeRunInfoDBInfoCorrelator("TCDS_CONF","TCDS_CONF_TIMES.csv")

    t = r.TTree("ntuple","data from CTP7 phase monitoring");
    # t.ReadFile("ctp7_phase_monitor_tts_busy_mid_run.log",headers)

    t.ReadFile("ctp7_phase_monitor_{}.log".format(args.fname),headers)

    f.Write()

if __name__ == '__main__':
    import argparse
    import sys, os
    from dateutil import parser
    opts = argparse.ArgumentParser()

    opts.add_argument("fname", help="File name time", type=str)
    opts.add_argument("-d",    help="debug", action='store_true')

    args = opts.parse_args()

    main(args)
