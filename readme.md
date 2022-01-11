# 搭建mongodb

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