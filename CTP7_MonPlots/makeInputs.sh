#!/bin/sh

for f in $(ls ctp7_phase_monitor_15*.log )
do
    nCols=$(awk -F' ' '{print NF; exit}' $f)
    cat $f |egrep -v Phase >> ctp7_phase_monitor_nCols${nCols}.log
done

for f in $(ls ctp7_phase_monitor_eagle61_15*.log )
do
    nCols=$(awk -F' ' '{print NF; exit}' $f)
    cat $f |egrep -v Phase >> ctp7_phase_monitor_eagle61_nCols${nCols}.log
done

for f in $(ls ctp7_phase_monitor_eagle33_15*.log )
do
    nCols=$(awk -F' ' '{print NF; exit}' $f)
    cat $f |egrep -v Phase >> ctp7_phase_monitor_eagle33_nCols${nCols}.log
done
