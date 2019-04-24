#!usr/bin/env python  
#-*- coding:utf-8 _*-  

""" 
@Author: SMnRa 
@Email: smnra@163.com
@Project: wechat
@File: sshTiaoban.py 
@Time: 2019/04/24 12:16

功能描述:
        通过ssh 跳板机自动登陆ssh

sshTiaoban("10.100.162.117" ,"richuser","richr00t", "10.100.162.135" ,"richuser","richr00t", r'ls l3fw_mr/kpi_import/20190423/ -R >~/MR_10_filelist.txt')

"""

#!/usr/bin/env python
import paramiko
import os,sys,time
def sshTiaoban(blip,bluser,blpasswd,hostname,username,password,cmd):
    cmdResult = ''   # 命令返回结果

    # hostname="10.100.162.135"     #业务主机ip
    # username="richuser"
    # password="richr00t"

    # blip="10.100.162.117"   #堡垒机ip
    # bluser="richuser"
    # blpasswd="richr00t"

    # cmd = r'ls l3fw_mr/kpi_import/20190423/ -R >~/MR_10_filelist.txt'

    port=22
    passinfo=r"'s password: "               #ssh 登陆输入密码时的前缀
    paramiko.util.log_to_file('syslogin.log')

    ssh=paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=blip,username=bluser,password=blpasswd)

    #new session
    channel=ssh.invoke_shell()
    channel.settimeout(10)

    buff = ''
    resp = ''
    channel.send('ssh '+username+'@'+hostname+'\n')     # 发送ssh root@192.168.1.20
    print('ssh '+username+'@'+hostname+'\n')
    while not buff.endswith(passinfo):               # 是否以字符串 's password 结尾
        try:
            resp = channel.recv(9999)
        except Exception as e:
            print('Error info:%s connection time.' % (str(e)))
            channel.close()
            ssh.close()
            sys.exit()
        # print(type(buff),buff)
        # print(type(resp),resp)
        buff += resp.decode('utf-8')
        if not buff.find('yes/no')==-1:       #模拟ssh登陆是输入yes
            channel.send('yes\n')
        #buff=''

    channel.send(password+'\n')       #发送密码

    buff=''
    while not buff.endswith('$ '):
        resp = channel.recv(9999)
        if not resp.decode('utf-8').find(passinfo)==-1:
            print('Error info: Authentication failed.')
            channel.close()
            ssh.close()
            sys.exit()
        buff += resp.decode('utf-8')

    channel.send( cmd + '\n')             #发送测试命令 ping
    buff=''
    try:
        while buff.find('$ ')==-1:
            resp = channel.recv(9999)
            buff += resp.decode('utf-8')
    except Exception as e:
        print("error info:"+str(e))

    buff = buff.replace("\r\r","\r")
    buff = buff.replace("[01;31m","").replace("[0m","").replace("[01;34m","")
    channel.close()
    ssh.close()
    return  buff

if __name__ =='__main__':
    result = sshTiaoban("10.100.162.117", "richuser", "richr00t", "10.100.162.133", "richuser", "richr00t",
               r'ls ~/l3fw_mr/kpi_import/20190423/ -R')
    print(result)


