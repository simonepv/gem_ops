### Using these scripts

#### From the outputs of the `ctp7_phase_monitor.py` script:
##### `makeInputs.sh`
Collects the input files (copied from the CTP7) and `cat`s them together, provided they exist in the same directory as the script is run from
* Script will automatically detect which version of the FW the log was made from and add the number of columns to the output file name
* One can manually create a file for use with the phase monitor/phase history tools by doing
  * `cat ctp7_phase_monitor_eagle61_153{4865857,5*}.log |egrep -v Phase > ctp7_phase_monitor_eagle61_aug24.log`

##### `ctp7_phase_monitor_plotting.py`
Creates an ntuple out of the phase logging data
* Optionally (if files are present) will add `TTree`s for:
  * `tcdsClockFreqTuple   = timeTCDSFreqMonCorrelator("TCDS_FREQMON.csv")`
  * `tcdsClockSrcTuple    = timeRunInfoDBInfoCorrelator("CMS_CLK_TYPE","CLOCK_TYPE_AT_PRECONFIGURE.csv")`
  * `lhcClockTuple        = timeRunInfoDBInfoCorrelator("LHC_CLK_STABLE","LHC_CLOCK_STABLE.csv")`
  * `gemConfiguringTuple  = timeRunInfoDBInfoCorrelator("GEM_CONF","GEM_CONF_TIMES.csv")`
  * `tcdsConfiguringTuple = timeRunInfoDBInfoCorrelator("TCDS_CONF","TCDS_CONF_TIMES.csv")`

```
usage: ctp7_phase_monitor_plotting.py [-h] [-d] fname

positional arguments:
  fname       File name (ctp7_phase_monitor_<fname>.log)

optional arguments:
  -h, --help  show this help message and exit
  -d          debug
```

##### `phase_history_plotter.py`
Actually make the plots from the phase monitoring log files
* Optionally, if the extra `TTree`s are present in the `ROOT` file, it will overlay that information

```
usage: phase_history_plotter.py [-h] [-tmin TMIN] [-tmax TMAX] [-stmin STMIN]
                                [-stmax STMAX] [-d]
                                fname

positional arguments:
  fname         File name (CTP7PhaseMonData_<fname>.root)

optional arguments:
  -h, --help    show this help message and exit
  -tmin TMIN    Minimum time
  -tmax TMAX    Maximum time
  -stmin STMIN  String minimum time
  -stmax STMAX  String maximum time
  -d            debug
```

##### Example usage
* Prepare the input files (must have the raw inputs from the CTP7 already)
  * `cat ctp7_phase_monitor_eagle61_153{4865857,5*}.log |egrep -v Phase > ctp7_phase_monitor_eagle61_aug24.log`
* Prepare the `ROOT` file (or run the `makeInputs.sh` script
  * `./ctp7_phase_monitor_plotting.py eagle61_aug24`
* Make plots of data from 8am Aug 23, 2018 to 12pm, Aug24, 2018:
  * `./phase_history_plotter.py eagle61_aug24 -stmin "08:00:00 Aug 23, 2018" -stmax "12:00:00 Aug 24, 2018"`

#### From the outputs of the `test_phase_shifting.py` script:
##### `ctp7_phase_shifting_analyzer.py`
Analyze the post phase shifting information, runs on the `csv` file created during the phase shifting procedure

```
usage: ctp7_phase_shifting_analyzer.py [-h] [-d] fname

positional arguments:
  fname       File name time

optional arguments:
  -h, --help  show this help message and exit
  -d          debug
```

##### `vfat2_reg_reset.py`
Script that checks if a register has the expected value and will reset it if not (currently **only** for `VFAT2` `ContReg0`)

```
usage: vfat2_reg_reset.py [-h] [-s SLOT] [-g LINK] [--shelf SHELF] [-d]
                          register value

positional arguments:
  register              Register to write
  value                 Value to write

optional arguments:
  -h, --help            show this help message and exit
  -s SLOT, --slot SLOT  Slot number
  -g LINK, --link LINK  Optical link number
  --shelf SHELF         uTCA shelf number
  -d                    debug
```
