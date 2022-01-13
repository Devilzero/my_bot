cd /root/my_bot/
source venv/bin/activate
git pull
kill -9 $(ps -ef|grep start.py|grep -v grep|awk '{print $2}')
nohup python start.py &
ps -ef|grep start.py|grep -v grep|awk '{print $2}'

if [ !-f "/etc/cron.daily/my_bot_start.sh" ];then
    cp cd /root/my_bot/my_bot_start.sh /etc/cron.daily/
fi