#!/bin/bash
echo "Getting DCS STATUS INFO"
echo "Start time $(date -u)"
cp template.sql request.sql
sed -i -e "s/CURRENT_DATE/$(date -u +'%Y.%m.%d %H:%M:%S')/g" request.sql
sed -i -e "s/START_DATE_SHORT/$(date -d '-2 day' -u +'%Y.%m.%d %H:%M:%S')/g" request.sql
sed -i -e "s/START_DATE_LONG/$(date -d '-7 day' -u +'%Y.%m.%d %H:%M:%S')/g" request.sql

sqlplus CMS_COND_GENERAL_R/p3105rof@cms_omds_adg	@request.sql > /dev/null

python GEM_DCS_STATUS.py  > GEM_DCS_REPORT.txt

rm GEM_all.csv
rm request.sql

cat GEM_DCS_REPORT.txt
echo "End time $(date -u)"
