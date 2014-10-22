__author__='lige'
#coding=utf-8
import urllib2
import re
import time
import ConfigParser
import login
import jquery
import os
from detail_spider import fetch_details
from detail_spider import fetch_mydetails

def config_login():
    config = ConfigParser.ConfigParser()
    config.read("config.ini")
    email = config.get("account", "email")
    password = config.get("account", "password")
    print email, password
    myid=login.open(email, password)
    return myid

def saveWebPage(filename, data):
    #print filename
    webpage = open(filename, 'w')
    webpage.write(data)
    webpage.close()


def save_lay1friend_file(data,filename):
    f=open(filename,'w+')
    f.write(data)
    f.close()
def read_myfriend_file(filename):
    f=open(filename,'r')
    data=f.readlines()
    return data

def get_myfriendlist(output_file,myid):
    f = open(output_file, 'w+')
    html = urllib2.urlopen('http://3g.renren.com/friendlist.do').read()
    page_cnt = 0
    person_cnt = 0
    #f.write("[")
    myfriendlist=""
    while True:
        profiles = map(lambda t : t.attrib['href'], jquery.query(html, "a[class=p]"))
        for p in profiles:
            print p
            myfriendlist=myfriendlist+p+"\n"
            person_cnt = person_cnt + 1

        if html.find("下一页") == -1:
            break
        next_page = jquery.query(html, u"[title=下一页]")[0].attrib['href']
        print next_page
        html = urllib2.urlopen(next_page).read()
        page_cnt = page_cnt + 1
        time.sleep(2)
    f.write(myfriendlist)
    f.write("\n")
    f.close()


def get_friendlist(file_input,lay2_file_path):
    files=os.listdir(file_input)

    sum_file=os.listdir('lay2/edge/')
    for file in files:#读取文件名
        print file
        input_filedata=open(file_input+file)
        pattern='详细资料.*(他|她)的好友'
        myfriendlist=""

        for data in input_filedata.readlines():#读取文件内容,也就市链接
            print data
            myfriendlist=""
            pattern1='id=\d+'
            filename=re.search(pattern1,data).group()
            if filename[3:] in sum_file:
                continue
            html = urllib2.urlopen(data,timeout=15).read()
            #time.sleep(2)
            if re.search('>关注者<',html)!=None:
                print '公共主页'
                time.sleep(10)
                continue
            #print html
            url=re.search(pattern,html).group()#得到好友的首页 url
            index1=url.find('href=')#找到好友的好友列表.
            buff=url[index1+6:-14]
            buff=re.sub('amp;','',buff)
            buff=re.sub('f=same','f=all',buff)#不加这句的话就是变成求 共同好友。
            #print buff
            html=urllib2.urlopen(buff,timeout=15).read()#打开好友的好友的列表
            time.sleep(2)
    ##############################################读取所有的好友#############################################
            while True:
                profiles = map(lambda t : t.attrib['href'], jquery.query(html, "a[class=p]"))
                for p in profiles:
                    print p
                    myfriendlist=myfriendlist+p+"\n"
                if html.find("下一页") == -1:
                    break
                next_page = jquery.query(html, u"[title=下一页]")[0].attrib['href']
                #print next_page
                html = urllib2.urlopen(next_page,timeout=15).read()
                time.sleep(2)
            save_lay1friend_file(myfriendlist,lay2_file_path+filename[3:])


###################################################################################################################
if  __name__=='__main__':
    myid=config_login()

    #登录
    lay1_file_edge='lay1/edge/'+myid
    lay1_file_node='lay1/node/'

    lay1_file_path='lay1/edge/'

    lay2_file_path='lay2/edge/'

    #get_myfriendlist(lay1_file_edge,myid)
    get_friendlist(lay1_file_path,lay2_file_path)
    #get_mydetail(lay1_file_node,myid)
    #get_myfriendlist(output_file,myid)#得到我的好友列表
    #file_inputname='295733348'
    #get_friendlist(file_inputname)#根据我的好友列表然后进行ｂｆｓ遍历查找 其余好友的列表 ，得到好友的好友的首页 。
    #filepath='myfrienddata/'

    #fetch_mydetails(myid,lay1_file_node)
    #fetch_details(lay1_file_path,lay1_file_path)
