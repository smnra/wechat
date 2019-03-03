#!usr/bin/env python  
#-*- coding:utf-8 _*-  

""" 
@Author: SMnRa 
@Email: smnra@163.com
@Project: wechat
@File: fileAnilyaz.py 
@Time: 2019/03/03 12:42

功能描述: 
从下载回来的 mr文件列表中分析 统计MR信息



"""

import re



class MR():
    def __init__(self,fileName):
        # 保存mr文件名列表的文件
        self.fileName = fileName

        # 列表中的总的文件夹数
        self.directCount = 0

        # 从文件路径中提取的基站的列表
        self.siteList = []

        # 列表中总的文件数
        self.fileCount = 0

        # 读取文件
        with open(self.fileName, mode='r', encoding='utf-8', errors='ignore') as f:
            self.mrFilePathList = f.readlines()
        if self.mrFilePathList:
            self.fileCount = len(self.mrFilePathList)

    def mrAnlyaz(self):
        for num, filePath in enumerate(self.mrFilePathList):
            line = filePath.strip("\n")
            if line.isdigit():
                self.directCount = self.directCount + 1
            elif '_NSN_OMC_' in line:
                # 匹配文件路径中的基站号
                self.searchObj = re.search(r'FDD-LTE_MR[OSE]_NSN_OMC_(.+)_.+\.', line, re.M | re.I)
                if self.searchObj:
                    if self.searchObj.group(1) not in self.siteList:
                        self.siteList.append(self.searchObj.group(1))

        self.mrFileSiteCount = len(self.siteList)
        print(self.siteList)
        return len(self.siteList)

    def getMrSiteCount(self):
        hasMRFileSiteCount = self.mrAnlyaz()
        print("存在MR文件的基站数: ",hasMRFileSiteCount)
        return hasMRFileSiteCount



if __name__=="__main__":
    mr = MR('MR9_filelist.txt')
    mrSiteCount = mr.getMrSiteCount()
    print(mrSiteCount)