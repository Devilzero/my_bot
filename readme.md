# 搭建 mirai

echo LANG="zh_CN.utf-8" >> ~/.bashrc

yum install cargo -y

yum install git -y

yum install openssl openssl-devel

git clone https://github.com.cnpmjs.org/iTXTech/mcl-installer.git

cd mcl-installer

cargo build --features native-tls --release

cd /root/

mkdir mcl

cd mcl/

/root/mcl-installer/

/root/mcl-installer/target/release/mcl-installer

./mcl --update-package net.mamoe:mirai-api-http --channel stable-v2 --type plugin

vim config/net.mamoe.mirai-api-http/setting.yml

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
    port: 8080
    cors: [*]

  ## 详情看 websocket adapter 使用说明 配置
  ws:
    host: localhost
    port: 8080
    reservedSyncId: -1
```

nohup ./mcl &

# 搭建 mongodb

## 安装

修改 mongodb yum 源

`vi /etc/yum.repos.d/mongodb-org-4.0.repo`

``` conf
[mngodb-org]
name=MongoDB Repository
baseurl=http://mirrors.aliyun.com/mongodb/yum/redhat/7Server/mongodb-org/4.0/x86_64/
gpgcheck=0
enabled=1
```

更新系统

`yum update -y`

安装
`yum -y install mongodb-org`

修改监听ip

`vi /etc/mongod.conf`

bindIp: 172.0.0.1  改为 bindIp: 0.0.0.0

security:
  authorization: enabled

启动

`systemctl start mongod.service`
开机自启

`systemctl enable mongod.service`

## 使用

创建用户

`use admin`
`db.createUser({user:"admin",pwd:"pwd",roles:[{role:"root",db:"admin"}]})`

打开mongodb

`mongo`

查看所有数据库

`show dbs`