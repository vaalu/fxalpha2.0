# Edit this file to introduce tasks to be run by cron.
#
# Each task to run has to be defined through a single line
# indicating with different fields when the task will be run
# and what command to run for the task
#
# To define the time you can provide concrete values for
# minute (m), hour (h), day of month (dom), month (mon),
# and day of week (dow) or use '*' in these fields (for 'any').#
# Notice that tasks will be started based on the cron's system
# daemon's notion of time and timezones.
#
# Output of the crontab jobs (including errors) is sent through
# email to the user the crontab file belongs to (unless redirected).
#
# For example, you can run a backup of all your user accounts
# at 5 a.m every week with:
# 0 5 * * 1 tar -zcf /var/backups/home.tgz /home/
#
# For more information see the manual pages of crontab(5) and cron(8)
#
# m h  dom mon dow   command

# Call localhost to keep websocket connection alive once every 15 mins
*/15 9-23 * * 1-5 curl http://localhost:5000 >> /home/ubuntu/build/logs/cron.log

# Create separate log folders in backup location based on date and time at the start of the day
# There is a separate script that needs to be called at the start of every day ie., 8PM
0 8 * * 1-5 /home/ubuntu/cron/create_log_backups_folders.sh

# Copy log files from processes to backup folders to free up mem load while writing logs
*/59 9-23 * * 1-5 