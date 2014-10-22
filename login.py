__author__ = 'lige'
#coding=utf-8
import urllib
import urllib2
import cookielib
import re
import jquery
def open(email, password):
    cookie = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    urllib2.install_opener(opener)
    html = urllib2.urlopen('http://m.renren.com').read()
    #print html
    #img = jquery.query(html, "img")[1].attrib['src']
    #verifykey = jquery.query(html, "input[name=verifykey]")[0].attrib['value']
    #print img
    #verifycode = raw_input("please visit the above url in your browser, and type the verify code on the page:\n")
    xn = {}
    xn['email'] = email
    xn['password'] = password
    #xn['verifycode'] = verifycode
    #xn['verifykey'] = verifykey
    #print xn
    data = urllib.urlencode(xn)
    req = urllib2.Request('http://3g.renren.com/login.do?fx=0&autoLogin=true', data)
    resp = urllib2.urlopen(req)
    #print resp.read()
    #print resp.read()
    buff=resp.read()
    #print buff
    pattern='id=\d+'
    pattern1='b>.*'
    uid = re.search(pattern,buff).group()
    #uname =re.search(pattern1,buff).group()
    #name = jquery.query(resp.read(), ".sec b a").text()
    #print uname[2:11]
    #profiles = map(lambda t : t.attrib['href'], jquery.query(resp.read(), "owner"))
    #print uid
    return uid[3:]