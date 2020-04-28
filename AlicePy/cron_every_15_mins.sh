# CRON Job to be run
# 0 0/15 9-11 ? * MON-FRI 
curl http://localhost:5000 >> ~/build/logs/cron.log 