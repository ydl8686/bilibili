import jieba
# import matplotlib.pyplot as plt
from wordcloud import WordCloud
import requests
import re
from lxml import etree
import pandas as pd
from wordcloud import random_color_func

r=requests.get('https://search.bilibili.com/all?keyword=黑人抬棺&from_source=nav_suggest_new')
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
# jieba分词
dm_str = " ".join(tmp)
words_list = jieba.lcut(dm_str)  # 切分的是字符串,返回的是列表
words_str = " ".join(words_list)
# 读取本地文件
# backgroud_Image = plt.imread('/Users/yindelin/Documents/个人信息/图片/柴犬.jpeg')

# 创建词云
wc = WordCloud(
    background_color='white',
    font_path='/System/Library/Fonts/PingFang.ttc',  # 设置本地字体

    max_words=2000,
    max_font_size=100,
    min_font_size=10,
)

word_cloud = wc.generate(words_str) # 产生词云
word_cloud.to_file("/Users/yindelin/Desktop/yumu.jpg") #保存图片