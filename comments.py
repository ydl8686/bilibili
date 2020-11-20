import jieba
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import requests
import re
from lxml import etree
import pandas as pd

r=requests.get('https://search.bilibili.com/all?keyword=网抑云&from_source=nav_suggest_new')
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
    dm_df.to_csv('/Users/yindelin/Desktop/comments.csv', encoding='utf_8_sig', mode='a', header=False)