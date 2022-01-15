## 依赖安装
``` shell
# 更新 yum 源
yum -y update
# 安装 git
yum -y git
# clone 项目代码
cd /root/
git clone https://github.com.cnpmjs.org/ermaozi/my_bot.git
# 安装 python 依赖
yum -y install python3-devel
# 安装 docker 依赖
yum install -y yum-utils device-mapper-persistent-data lvm2
# 修改 docker yum 源
yum-config-manager --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
# 安装最新的 docker
yum makecache fast
yum install -y docker-ce
# 启动 docker 并设置开机启动
systemctl start docker
systemctl enable docker
```

## Mirai 安装、配置、启动
``` shell
# 下载并第一次启动 mirai
docker run --rm -it --name="mirai" -v /root/mirai/config:/app/config ermaozi/mirai:latest
```

第一次启动后退出，修改 mirai-api-http 配置文件

``` shell
vim /root/mirai/config/net.mamoe.mirai-api-http/setting.yml
```

通过自己的聪明才智理解并洞察该配置文件的内容后, 将其修改成自己喜欢的样子并保存

下面是样例, 注意端口(port)要与下方 docker 映射端口保持一致

``` yaml
## 配置文件中的值，全为默认值

## 启用的 adapter, 内置有 http, ws, reverse-ws, webhook
adapters:
  - http
  - ws

## 是否开启认证流程, 若为 true 则建立连接时需要验证 verifyKey
## 建议公网连接时开启
enableVerify: true
verifyKey: 1234567890

## 开启一些调式信息
debug: false

## 是否开启单 session 模式, 若为 true，则自动创建 session 绑定 console 中登录的 bot
## 开启后，接口中任何 sessionKey 不需要传递参数
## 若 console 中有多个 bot 登录，则行为未定义
## 确保 console 中只有一个 bot 登陆时启用
singleMode: false

## 历史消息的缓存大小
## 同时，也是 http adapter 的消息队列容量
cacheSize: 4096

## adapter 的单独配置，键名与 adapters 项配置相同
adapterSettings:
  ## 详情看 http adapter 使用说明 配置
  http:
    host: localhost
    port: 8088
    cors: [*]

  ## 详情看 websocket adapter 使用说明 配置
  ws:
    host: localhost
    port: 8088
    reservedSyncId: -1
```

完成后再次启动, 此时需要设置自动登陆, 因为很麻烦, 所以后面再做补充

``` shell
docker run --rm -it --name="mirai" -p 8088:8088 -v /root/mirai/config:/app/config ermaozi/mirai:latest
```

然后在后台启动就 OK 了

``` shell
docker run -d --name="mirai" -p 8088:8088 -v /root/mirai/config:/app/config ermaozi/mirai:latest
```

## mongodb 安装、配置、启动

下载并启动 mongodb

``` shell
docker run -itd --name="mongo" -p 27017:27017 mongo --auth
```

进入 mongodb 创建用户

``` shell
docker exec -it mongo /bin/bash
# docker 的伪终端
mongo
```

pwd 记得写自己的

```
> use admin
> db.createUser({user:"admin",pwd:"pwd",roles:[{role:"root",db:"admin"}]})
> exit
```

配置远程访问, 如果不需要远程访问的话可以忽略这一步

``` shell
# docker 的伪终端
apt-get update
apt-get install vim -y
vim /etc/mongod.conf.orig
```

写入以下内容

```
bindIp: 127.0.0.1
改为
bindIp: 0.0.0.0
```

```
#security:

改为

security:
  authorization: enabled
```

## 启动机器人

初始化工具
``` shell
cd /root/my_bot/
pip3 install -r requirements.txt
chmod +x ./start.py
cp ./conf/config.json.template ./conf/config.json
vim ./conf/config.json
```

根据实际情况修改好 config.json

启动服务

``` shell
ln -sf /root/my_bot/asset/my_bot.service /etc/systemd/system/my_bot.service
systemctl daemon-reload
systemctl start my_bot
systemctl enable my_bot
```