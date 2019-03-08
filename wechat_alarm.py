# -*- coding: UTF-8 -*-
import datetime
import ssh
import wechat
import os
import fileAnilyaz

now = datetime.datetime.now()   #获取当前时间
#print("Today is %s." % now.strftime('%Y%m%d')) 

def mrServerStatus(host,serverName):        #参数为IP地址 和 mr服务器名称
    sshmr_1 = ssh.sshOpen()

    pathTime = now.strftime('%Y%m%d')
    filePath = r'./file/' + now.strftime('%Y%m%d') + r'/'

    # 远程 MR 服务器上 MR数据文件保存路径
    mrDirRemote = r'l3fw_mr/kpi_import/' + now.strftime('%Y%m%d')

    # 保存 MR文件名列表的文件路径 在远程MR服务器上
    mrFileNameRemote = r'/home/richuser/' + serverName + '_filelist.txt'

    # 保存 MR文件名列表的文件路径 在本地电脑上
    mrFileNameLocal =  filePath + serverName + '_filelist.txt'

    # 保存 采集到MR数据的基站列表文件
    siteListFileNameLocal = filePath + serverName + '_sitelist.csv'

    if os.path.exists(filePath):  # 判断路径是否存在
        print(u"目标已存在:", filePath)  # 如果存在 打印路径已存在,
    else:
        os.makedirs(filePath)  # 如果不存在 创建目录


    try:
        ftpStr = sshmr_1.sshcon(host, 22, 'richuser', 'richr00t',
                                "netstat -an|awk '{print $4}' | grep ':21$'")  # 执行查看ftp端口是否打开
        mrStr = sshmr_1.sshcon(host, 22, 'richuser', 'richr00t',
                               "ps -ef|awk '{print $10,$9}' | grep l3fw")  # 检查mr进程是否打开

        # 服务器上执行将 mr文件路径列表 写入到文件中
        sshmr_1.sshcon(host, 22, 'richuser', 'richr00t',
                       "ls " + mrDirRemote + "/ -R >~/"+ serverName + "_filelist.txt")  # 统计mr基站数

        # 从服务器 sftp 下载mr文件路径列表文件 到本地
        ssh.remoteScp(host, 22, 'richuser', 'richr00t',
                  tag_file=mrFileNameRemote,
                  local_file=mrFileNameLocal)

        mr = fileAnilyaz.MR(mrFileNameLocal)

        #  获取有MR文件的基站列表
        mrSiteList = mr.mrAnlyaz()



        # 将列表写入文件
        with open(siteListFileNameLocal, mode='w', encoding='gbk', errors='ignore') as f:
            f.write("\n".join(mrSiteList))

        # 统计基站数
        mrNum = len(mrSiteList)


        traceNum = sshmr_1.sshcon(host,22,'richuser','richr00t',"ls l3fw_mr/import/" + now.strftime('%Y%m%d') + "| wc -w")      #统计trace基站数
        if ftpStr.find(':::21') == -1:
            ftpStatus = "Faild"
        else:
            ftpStatus = "OK"

        if mrStr.find('watchdog.sh') == -1:
            mrStatus = "Faild"
        else:
            mrStatus = "OK"
        print(serverName, ftpStatus, mrStatus, str(mrNum), str(traceNum.strip()))
        return [serverName, ftpStatus, mrStatus, str(mrNum), str(traceNum.strip())]  # 函数返回一个mr服务器的以上状态的列表

    except Exception as e:
        print(serverName,e.__str__())
        return serverName + '  ' + str(type(e)).replace('class ','').replace("'",'') +  '  ' + str(e.errno)

 

#massage_info = "Server\\tFTP\\tMR\\teNodeB\\tTrace\\n Server\\tFTP\\tMR\\teNodeB\\tTrace"

#wechat.send_msg(massage_info) 

def trimStatus(mr):
    '''
    整理 输出数据格式 如果是字符串格式 说明 执行有报错直接返回 字符串
    :param mr: 远程服务器返回的值
    :return: 整理后用于发送微信的字符串
    '''
    if type(mr)==list:
        return "%s  %s    %s    %s        %s\\n" % (mr[0],mr[1],mr[2],mr[3],mr[4])
    elif type(mr)==str:
        return mr + '\\n'


def getServerStatus():
    mr1 = mrServerStatus("10.100.162.112","MR_1")
    mr2 = mrServerStatus("10.100.162.111","MR_2")
    mr3 = mrServerStatus("10.100.162.110","MR_3")
    mr4 = mrServerStatus("10.100.162.109","MR_4")
    mr5 = mrServerStatus("10.100.162.108","MR_5")
    mr6 = mrServerStatus("10.100.162.115","MR_6")
    mr7 = mrServerStatus("10.100.162.117","MR_7")
    mr8 = mrServerStatus("10.100.162.119","MR_8")
    mr9 = mrServerStatus("10.100.162.120","MR_9")
    mrs = [mr1, mr2, mr3, mr4, mr5, mr6, mr7, mr8, mr9]

    title = ("%s MR Server Status:\\n" % now.strftime('%Y-%m-%d'))
    message_wx0 = "Server FTP  MR   eNodeB Trace\\n"
    mrs = [trimStatus(mr) for mr in mrs]



    if not os.path.isdir(os.path.abspath('./log')) :        #若 log 文件夹不存在则创建log文件夹
        os.makedirs(os.path.abspath('./log'))
    file = open(os.path.abspath('./log/')+ '\\' + now.strftime('%Y_%m_%d_%H_%M_%S')+ '.log' ,mode = 'w+' ,encoding = 'utf-8')
    file.write(title + '\n'+ message_wx0 + '\n' +  '\n'.join(mrs))
    file.flush()
    file.close()
    print(title + '\n'+ message_wx0 + '\n'+  '\n'.join(mrs))
    return title + message_wx0 + ''.join(mrs)



if __name__ == '__main__':
    message = getServerStatus()
    wechat.send_msg(message)
    print('over!')