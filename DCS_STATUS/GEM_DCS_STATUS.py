import csv
import datetime
#from RPCHVLabel_cfi import *
from GEMDCSLabels_cfi import *
#import pandas as pd
#import numpy as np

reader = csv.reader(open("GEM_all.csv"))
data0 = []

def print_gas_flow_cell():
  print "Gas:"
  for cell in sorted(flow_cells):
    try:
      print "%s: In = %s l/h Out: %s l/h    Measured at %s UTC 2017" % (cell, round(imons[flow_cells[cell]["In"]]*100)/100, round(imons[flow_cells[cell]["Out"]]*100)/100,dates[flow_cells[cell]["In"]])
    except KeyError:
      print "%s: DB READING ERROR!" % (cell)
  print ""

def print_gas_pressure():
  print "Gas:"
  for cell in sorted(gas_pressure):
    id = gas_pressure[cell]
    try:
      print "%s: %s    Measured at %s UTC 2017" % (cell, round(imons[id]*100)/100, dates[id])
    except KeyError:
      print "%s: DB READING ERROR!" % (cell)
  print ""


def print_reg_chamber(chamber):
  print "%s:" %(chamber)
  id = chamber_settings[chamber]["HV"]
  try:
    print "HV:%s, I:%s    Measured at %s UTC 2017" % (round(vmons[id]*100)/100, round(imons[id]*100)/100,dates[id])
  except KeyError:
    print "HV: DB READING ERROR!"
  id = chamber_settings[chamber]["LV_VFATS"]
  try:
    print "VFAT LV:%s, I:%s    Measured at %s UTC 2017" % (round(vmons[id]*100)/100, round(imons[id]*100)/100,dates[id])
  except KeyError:
    print "VFAT LV: DB READING ERROR!"
  id = chamber_settings[chamber]["LV_OH2V"]
  try:
    print "OH_2V LV:%s, I:%s    Measured at %s UTC 2017" % (round(vmons[id]*100)/100, round(imons[id]*100)/100,dates[id])
  except KeyError:
    print "OH_2V LV: DB READING ERROR!"
  id = chamber_settings[chamber]["LV_OH4V"]
  try:
    print "OH_4V LV:%s, I:%s    Measured at %s UTC 2017" % (round(vmons[id]*100)/100, round(imons[id]*100)/100,dates[id])
  except KeyError:
    print "OH_4V LV: DB READING ERROR!"
  print ""

def print_multichan_chamber(chamber):
  print "%s:" %(chamber)
  try:
    id = mult_chamber_settings[chamber]["Drift"]
    print "Drift %s, I:%s    Measured at %s UTC 2017" % (round(vmons[id]*100)/100, round(imons[id]*100)/100,dates[id])
    id = mult_chamber_settings[chamber]["G1Top"]
    print "G1Top %s, I:%s    Measured at %s UTC 2017" % (round(vmons[id]*100)/100, round(imons[id]*100)/100,dates[id])
    id = mult_chamber_settings[chamber]["G1Bottom"]
    print "G1Bottom %s, I:%s    Measured at %s UTC 2017" % (round(vmons[id]*100)/100, round(imons[id]*100)/100,dates[id])
    id = mult_chamber_settings[chamber]["G2Top"]
    print "G2Top %s, I:%s    Measured at %s UTC 2017" % (round(vmons[id]*100)/100, round(imons[id]*100)/100,dates[id])
    id = mult_chamber_settings[chamber]["G2Bottom"]
    print "G2Bottom %s, I:%s    Measured at %s UTC 2017" % (round(vmons[id]*100)/100, round(imons[id]*100)/100,dates[id])
    id = mult_chamber_settings[chamber]["G3Top"]
    print "G3Top %s, I:%s    Measured at %s UTC 2017" % (round(vmons[id]*100)/100, round(imons[id]*100)/100,dates[id])
    id = mult_chamber_settings[chamber]["G3Bottom"]
    print "G3Bottom %s, I:%s    Measured at %s UTC 2017" % (round(vmons[id]*100)/100, round(imons[id]*100)/100,dates[id])
  except KeyError:
    print "Multichannel HV: DB READING ERROR!"
  id = mult_chamber_settings[chamber]["LV_VFATS"]
  try:
    print "VFAT LV:%s, I:%s    Measured at %s UTC 2017" % (round(vmons[id]*100)/100, round(imons[id]*100)/100,dates[id])
  except KeyError:
    print "VFAT LV: DB READING ERROR!"
  id = mult_chamber_settings[chamber]["LV_OH2V"]
  try:
    print "OH_2V LV:%s, I:%s    Measured at %s UTC 2017" % (round(vmons[id]*100)/100, round(imons[id]*100)/100,dates[id])
  except KeyError:
    print "OH_2V LV: DB READING ERROR!"
  id = mult_chamber_settings[chamber]["LV_OH4V"]
  try:
    print "OH_4V LV:%s, I:%s    Measured at %s UTC 2017" % (round(vmons[id]*100)/100, round(imons[id]*100)/100,dates[id])
  except KeyError:
    print "OH_4V LV: DB READING ERROR!"
  print ""


vmon=0.
imon=0.
for row in reader:
    if len(row) != 4 :
        continue
    id = int(str(row[0]))
    dd2 = datetime.datetime.strptime(str(row[3]),  "%Y.%m.%d %H:%M:%S")

    if  not  len(str(row[2]).strip()) is 0 :  imon = float("%.4f"%float(row[2]))
    else                                  :  imon = -1.
    if  not len(str(row[1]).strip()) is 0 :  vmon = float(row[1])
    else                                  :  vmon = -1.

    adata = {"id":id,"imon":imon,"vmon":vmon,"date":str(row[3]),"dateN":dd2}
    data0.append(adata)


data0.sort(key=lambda x: x['dateN'] )

aaa = set()
names = {}
vmons = {}
imons = {}
dates = {}
dates2 = {}
for row in data0:
   if not endcap.has_key(int(row["id"])) :
       continue
   id  = int(row["id"])
   if row["imon"] != -1   : imon = row["imon"]
   elif imons.has_key(id) : imon = imons[id]
   else                   : imon = -1.

   if row["vmon"] != -1   : vmon = row["vmon"]
   elif vmons.has_key(id) : vmon = vmons[id]
   else                   : vmon = -1.
   #print "test"

   name = endcap[int(row["id"])]
   date = row["date"]
   date2 = datetime.datetime.strptime(date, "%Y.%m.%d %H:%M:%S")
   if (not names.has_key(id)) or (names.has_key(id) and dates2[id]<=date2):
       names[id] =name
       vmons[id] =vmon
       imons[id] =imon
       dates[id] =date
       dates2[id]=date2
   aaa.add(id)

#print "check len(aaa):"+str(len(aaa))+";"
#for id in names.keys():
  #print id,names[id],str(round(vmons[id]*100)/100),dates[id]
  #print id,names[id],str(round(imons[id]*100)/100),str(round(vmons[id]*100)/100),dates[id]
  #print str(round(imons[id]*100)/100),str(round(vmons[id]*100)/100),dates[id]
  #print names[id]
  #print str(round(imons[id]*100)/100)
  #print str(round(vmons[id]*100)/100)
 
#print_gas_flow_cell()
print_gas_pressure()
print ""
for ch in sorted(chamber_settings):
  print_reg_chamber(ch)
print ""
for ch in sorted(mult_chamber_settings):
  print_multichan_chamber(ch)
