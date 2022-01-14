kill -9 $(ps -ef|grep start.py|grep -v grep|awk '{print $2}')

cd /root/my_bot/
git pull

\cp /root/my_bot/my_bot_start.sh /etc/cron.hourly/
chmod +x /etc/cron.hourly/my_bot_start.sh

source /root/my_bot/venv/bin/activate
nohup python start.py >/dev/null 2>&1 &