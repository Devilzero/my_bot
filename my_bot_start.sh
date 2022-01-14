cd /root/mcl/
kill -9 $(ps -ef|grep mcl|grep -v grep|awk '{print $2}')
nohup ./mcl &

cd /root/my_bot/
source venv/bin/activate
git pull
kill -9 $(ps -ef|grep start.py|grep -v grep|awk '{print $2}')
nohup python start.py &
ps -ef|grep start.py|grep -v grep|awk '{print $2}'

cp /root/my_bot/my_bot_start.sh /etc/cron.hourly/
chmod +x /etc/cron.hourly/my_bot_start.sh