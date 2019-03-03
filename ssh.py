# -*- coding: UTF-8 -*-
import paramiko


class sshOpen:
    def __init__(self):
        pass
    def sshcon(self,taghost,tagport = 22,taguser = 'root',tagpassword = 'smnra000',tagcmd = 'ls -l'):
        self.ssh = paramiko.SSHClient()  #创建SSH对象
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())   #把要连接的机器添加到known_hosts文件中
        self.ssh.connect(hostname = taghost, port = tagport, username = taguser, password = tagpassword) #连接服务器
        self.stdin, self.stdout, self.stderr = self.ssh.exec_command(tagcmd) #执行命令语句
        self.result = self.stdout.read()
        if not self.result:
            self.result = self.stderr.read()
        self.ssh.close()
        return self.result.decode()

def remoteScp(taghost, tagport=22, taguser='root', tagpassword='smnra000', tag_file=r'/home/richuser/MR_filelist.txt', local_file=r'./file/MR_filelist.txt'):
    scp = paramiko.Transport((taghost, tagport))
    scp.connect(username=taguser, password=tagpassword)
    sftp = paramiko.SFTPClient.from_transport(scp)
    sftp.get(tag_file, local_file)
    scp.close()
    return ("success")

def sshOpenFunc(taghost,tagport = 22,taguser = 'root',tagpassword = 'smnra000',tagcmd = 'ls -l'):
    ssh = paramiko.SSHClient()  #创建SSH对象
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())   #把要连接的机器添加到known_hosts文件中
    ssh.connect(hostname = taghost, port = tagport, username = taguser, password = tagpassword) #连接服务器
    #tagcmd = 'ls -l;ifconfig' #多个命令用;隔开
    stdin, stdout, stderr = ssh.exec_command(tagcmd) #执行命令语句
    result = stdout.read()
    if not result:
        result = stderr.read()
    ssh.close()
    #print(result.decode())
    return result.decode()





if __name__ == '__main__':
    print(sshOpenFunc('10.100.162.115',22,'richuser','richr00t',"netstat -an|awk '{print $4}' | grep ':21$'"))