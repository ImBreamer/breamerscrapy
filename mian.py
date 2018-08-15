import os
import urllib.request

import pymysql


class TestMain(object):
    def __init__(self):
        pass


if __name__ == "__main__":
    ps = None
    ps = ps + "lll"
    print(ps)
    # db_client = pymysql.connect(host='106.74.146.168', user='root', password='root#123QAZ', db='app', charset='utf8')
    # cursor = db_client.cursor()
    # sql = "select title, content from app_white_book"
    # print(sql)
    # cursor.execute(sql)
    # # cursor.execute("select id from app_news")
    # results = cursor.fetchall()
    # # db_client.commit()
    # x = set()
    # for s in results:
    #     print(s[0])
    #     print(s[1])
    #     print('*********************************************************************************************')
    # print(x)
    # str = "创新未有穷期，航天云网助力开启工业强国之路"
    # str1 = "云端营销用户手册】2.1 营销员操作流程"
    # print(str.find("手册"))
    # print(str1.find("手册"))
    # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0'}
    # # res = urllib.request.urlopen('', headers=headers)
    # file_name = os.path.join('C:/Users/23769/Desktop',  'x.pdf')
    # # os.path.join将多个路径组合后返回
    # urllib.request.urlretrieve('http://www.aii-alliance.org/index.php?m=content&c=index&a=document_'
    #                            'download&ftype=3&fid=271&fno=0',  file_name)