__author__ = 'lige'
#encoding:utf-8
import pymongo
import json

def store_data(data):
    connection=pymongo.Connection('localhost',27017)
    db = connection.test_database
    table1=db.posts

    #if table1.find_one({'uid':281788949}) is not None:
       # return
    #else:
    table1.insert(data)
    #i=0
    for content in table1.find().limit(5):
        #print type(u)
        print content['uid']
        print content['Name']
        print content['publicpage']
        print content['birthday']

        #print json.dumps(u, encoding='gbk', ensure_ascii=False, indent=1)

        #print u

if __name__=='__main__':
    f=open('UserInfo/364944677','r')
    data = json.load(f)
    #print data
    store_data(data)



