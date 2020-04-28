# CRON Job to be run
# * 0/15 9-23 ? 1-12 * 
# Every second, every 15 minutes starting at minute :00, every hour between 09am and 23pm, every month between January and December
# crontab -e 0 0/15 9-11 * * MON-FRI * /apps/cron_every_15_mins.sh
# */15 9-23 * * 1-5 curl http://localhost:5000 >> /home/ubuntu/build/logs/cron.log
curl http://localhost:5000 >> /home/ubuntu/build/logs/cron.log 