# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 22:00:02 2015
@author: TsingJyujing

库的作用：封装了一些常用的和互联网相关的函数
"""
from list_file_io import write_raw

import urllib2 as ul2
import urllib  as ul
import threading
import time
import re
import os


class mt_picdowner(threading.Thread):
    def __init__(self,picurl,filename):
        threading.Thread.__init__(self)
        self.imgurl = picurl
        self.fpname = filename
        self.done = 0
        
    def run(self):
        print self.fpname + "Started!"

        if os.path.exists(self.fpname):#已经下载过了
            su = 7
        else:
            su = self.download_image(self.imgurl,self.fpname)
        
        if su == 0 :
            print self.fpname + " Failed!"
        elif su == 7:
            print self.fpname + " Has Downloaded!"
        else:
            print self.fpname + " Done!"
            
        self.done = 1
            
    def mt_picdowner_savefile(self,filename,data):
        f = open(filename,'wb')
        f.write(data)
        f.close()
    
    def download_image(self,imgurl,fpname):
        print "Image will save as %s" % fpname
        for i in range(10):#最多重试10次，主要用于断网的处理
            try:
                data = self.read_url(imgurl,5)#最多重新刚下载5次

                if len(data)==0:
                    raise DataError('No Data')

                self.mt_picdowner_savefile(fpname,data)
                
                print "  Download %s successfully!" % imgurl
                return 1
            except:
                print "  Retrying to get %s...." % imgurl
                print "  Testing internet..."
                while(1):
                    u = self.check_url_validation("http://www.baidu.com/",7)
                    if u == 1:
                        print '  Connected to internet normally!'
                        break;
                    else:
                        print "  Mabye no internet, waiting..."

        return(0)

    def read_url(self,url,fail_tms):
        for i in range(fail_tms):
            try:
                Host = re.findall('://.*?/',url,re.DOTALL)
                Host = Host[0][3:-1]
                print "  host detected:%s" % Host

                req_header = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                'Accept-Encoding': 'gzip, deflate',
                'Host': Host
                }
                req_timeout = 25
                print '  Http parameters has set'

                req = ul2.Request(url,None,req_header)
                print '  Request has sent'

                resp = ul2.urlopen(req,None,req_timeout)
                print '  Response has got'

                data = resp.read()
                print "  Got data successfully!"

                break;
            except:
                print "  Error detected, (re)trying getting data...."
                data = ""

        return data
        
    def check_url_validation(self,url,fail_tms):
        for i in range(fail_tms):
            try:
                response = ul2.urlopen(url)
                print "  Get response successfully!"
                return(1)
            except:
                print "  (Re)Trying to get response...."
        return 0

def download_image_list(DirName,ImageURLs):
    thread_list = []
    N = len(ImageURLs)
    for (index,URL) in enumerate(ImageURLs):
        expr = re.findall("\.(\w+)$",URL,re.DOTALL)[0]
        fn =  DirName+("%d.%s" % (index,expr))
        thread_list.append(  mt_picdowner(URL,fn)  )

    for i in range(N):
        thread_list[i].start()
        time.sleep(0.1)

    for i in range(N):
        thread_list[i].join()
        #锁住子线程和父线程的运行
    print "Image list has all download."   

def download_image_list_single_thread(DirName,ImageURLs):
    for (index,URL) in enumerate(ImageURLs):
        expr = re.findall("\.(\w+)$",URL,re.DOTALL)[0]
        fn = DirName+("%d.%s" % (index,expr))
        if os.path.exists(fn):
            print "%s is an existed file!(Jumped)" % fn
        else:
            res = download_image(URL,fn)
            if res == 1:
                print "Download %s as %s successfully." % (URL,fn)
            else:
                print "Download %s as %s failed." % (URL,fn)
    print "Image list has all download."


def download_image(imgurl,fpname):
    print "Image will save as %s" % fpname
    for i in range(10):#最多重试3次，主要用于断网的处理
        try:
            data = read_url2(imgurl,5)#最多重新刚下载5次

            if len(data)==0:
                raise DataError('No Data')

            write_raw(fpname,data)
            
            print "  Download %s successfully!" % imgurl
            return 1
        except:
            print "  Retrying to get %s...." % imgurl
            print "  Testing internet..."
            while(1):
                u = check_url_validation("http://www.baidu.com/",5)
                if u == 1:
                    print '  Connected to internet normally!'
                    break;
                else:
                    print "  Mabye no internet, waiting..."

    return(0)

def read_url2(url,fail_tms):
    print "Reading..."+url
    for i in range(fail_tms):
        try:
            Host = re.findall('://.*?/',url,re.DOTALL)
            Host = Host[0][3:-1]
            print "  host detected:%s" % Host

            req_header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Host': Host
            }
            req_timeout = 5
            print '  Http parameters has set'

            req = ul2.Request(url,None,req_header)
            print '  Request has sent'

            resp = ul2.urlopen(req,None,req_timeout)
            print '  Response has got'

            data = resp.read()
            print "  Got data successfully!"
            if data!="":
                break;
            else:
                print "Error while reading url:EMPTY"
        except:
            print "  Error detected, (re)trying getting data...."
            data = ""
    if data=="":
        print "ERROR WHILE READING "+url
    #print "DATA:"+data
    return(data)

def read_url(url,fail_tms):
    print "Reading..."+url
    for i in range(fail_tms):
        try:
            resp = ul2.urlopen(url)
            print '  Response has got'
            data = resp.read()
            print "  Got data successfully!"
            if data!="":
                break;
            else:
                print "Error while reading url:EMPTY"
        except:
            print "  Error detected, (re)trying getting data...."
            data = ""
    if data=="":
        print "ERROR WHILE READING "+url
    #print "DATA:"+data
    return(data)

def check_url_validation(url,fail_tms):
    for i in range(fail_tms):
        try:
            response = ul2.urlopen(url)
            print "  Get response successfully!"
            return 1
        except:
            print "  (Re)Trying to get response...."
    return 0


if __name__=="__main__":
    print "Usage: from pyinternet import *"
