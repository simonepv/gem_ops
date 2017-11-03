# gem_ops
This repository is intended to keep useful operational scripts
## DCS STATUS DB query script
* Can be run from lxplus
### Usage:
`cd DCS_STATUS && sh get_gem_dcs_status.sh`

#### Comment:
* Modulo frequency of the DCS DB updates this set of scripts works well. It takes about 5 minutes to run from lxplus. It looks 30 days back to query gas flow and 2 days back to query HV/LV/currents.
* Known issue: due to uneven DCS DB updates sometimes data for certain fields (mostly LV) can be empty. In this case it means that this value didn't change during last two days and therefore the DB has not been updated, so such value can be taken from previous DOC daily report.
