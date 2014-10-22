#encoding:utf-8
import os
import re
import urllib2
import time
import jquery
import util

def fetch_mydetails(myid,output_path):
    f = open(output_path+myid, 'w+')
    html = urllib2.urlopen('http://3g.renren.com/profile.do').read()
    pattern='详细资料'
    #取得发布,评论详细内容
    pattern1='</a>:&nbsp;.*<br />'#匹配发布的内容
    




    #取得个人详细资料


    f.write("[")
    f.write("]\n")
    f.close()


def fetch_details(filepath,outputfile):
    #path='UserData/'
    files=os.listdir(filepath)
    print files
    number=0
    for file in files:#有 许多的文件在里面 。
        f=open(filepath+file,'r')
        person_cnt=0
        filedata=f.readlines()
        no=0
        for data in filedata: #一 个 文件作为，每个文件里面包含诜多个链接，每个链接都可有一个用户。
##############################################得到组信息################################
            pattern1='id=\d+'
            filename=re.search(pattern1,data).group()
            f_detail=open(outputfile+filename,'w+')
            f_detail.write('[')
            print data
            html=urllib2.urlopen(data).read()
#################################得到详细资料##########################################################################
            url = data.replace("profile", "details")
            uid = re.findall(r"id=([0-9]+)", url)[0]
            detail_page=urllib2.urlopen(url).read()
            time.sleep(2)
            name = jquery.query(detail_page, ".sec b a").text()
            res = jquery.query(detail_page, ".list")
            info = "\n".join(res.listOuterHtml());
            if len(info) == 0:
                info = u"null"
            if person_cnt>0:
                f_detail.write(",");
            f_detail.write("{\n");
            f_detail.write(("\t\"%s\": %d")%("uid", int(uid)))
            f_detail.write((",\n\t\"%s\": \"%s\"")%("Name", util.utf8_wrapper(name)))
            for s in re.findall(ur"[^>]*：[^<]*", info):
                idx = s.find(u"：");
                f_detail.write(util.utf8_wrapper((",\n\t\"%s\": \"%s\"")%(s[0:idx], s[idx+1:])))
            #f_detail.write(util.utf8_wrapper((",\n\t\"%s\": \"%s\"")%("publicpage", publicindexs)))
            time.sleep(1)
            f_detail.write("\n}")
            f_detail.flush()
            person_cnt=person_cnt+1
            f_detail.write('\n'+']')
            f_detail.close()
            f.close()
            number=number+1
        print "已分析数据 "+str(number)+'个'