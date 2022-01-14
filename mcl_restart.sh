kill -9 $(ps -ef|grep mcl|grep -v grep|awk '{print $2}')
cd /root/mcl/
nohup ./mcl &