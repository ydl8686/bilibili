import jieba
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import requests
import re
from lxml import etree
import pandas as pd
import time
import os


# 传进来的第一个参数是想要查询的内容，第二个参数是csv文件存储的位置
def spider(content, path):
    # 先判断一下存储弹幕的文件是否存在，如果存在要删掉，因为防止数据重复
    if os.path.isfile(path):
        os.remove(path)
    r = requests.get('https://search.bilibili.com/all?keyword='+content+'&from_source=nav_suggest_new')
    print("----------------------------------------")
    content = r.text
    result = re.findall('<a href="//www.bilibili.com/video/(.*?)?from=search"', content, re.S)
    print(len(result))
    cidList=[]
    for i in result:
        print(i)
        ree = requests.get('https://www.bilibili.com/video/'+i+'?from=search%3D')
        html = ree.text
        cidList.append(re.search('"cid":(.*?),', html))
    print('+++++++++++++++++++++++++++++++++++++++')
    allComment = []
    for i in cidList:
        print(i.group(1))
        # 发送请求
        response = requests.get('https://comment.bilibili.com/'+i.group(1)+'.xml')
        xmll = etree.fromstring(response.content)
        # 解析数据
        # dm.append(xml.findall("./d"))
        tmp = xmll.xpath("./d//text()")
        # 把列表转换成 dataframe
        dm_df = pd.DataFrame(tmp, columns=['弹幕内容'])

        # 存到本地
        # 解决了中文乱码问题
        dm_df.to_csv(path, encoding='utf_8_sig', mode='a', header=False)



def sleeptime(hour, min, sec):
    return hour*3600 + min*60 + sec


# 每隔30s重新爬取一次数据
second = sleeptime(0, 0, 30)
while True:
    time.sleep(second)
    print('新的一轮')
    spider('网抑云', '/Users/yindelin/Desktop/comments.csv')
