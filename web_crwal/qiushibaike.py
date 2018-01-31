# coding:utf-8
import requests
import re
from bs4 import BeautifulSoup
import time
import numpy as np
# get HTML Text
def getHTMLText(url):
    try:
        r = requests.get(url, timeout = 60)                                  # 向服务器发送请求
        r.raise_for_status()                                                 # 若状态码 != 200， 抛出异常
        r.encoding = r.apparent_encoding                                     # utf-8 编码
        return r.text                                                        # 返回文本内容
    except:
        return ''

# 解析页面，得到第i个段子pair
def parsePage(html):
    try:
        soup = BeautifulSoup(html, 'html.parser')
        pattern = re.compile(r'[\u4e00-\u9fa5]+')                               # 匹配中文字符串
        jokes = soup.find_all('div', attrs='content')                           # type(jokes[0]) = <class 'bs4.element.Tag'>
        comments = soup.find_all('span', attrs="body", text=pattern, limit=20)  # type(comment) = <class 'bs4.element.Tag'>                                            # 从content中取出段子
        return (jokes, comments)
    except:
        return None


# 将得到的段子保存至本地
def storage(results,i):
    if results == None:
        return None
    fname = 'results/jokes' + str(i) + '.txt'                                                # 将结果保存至fname中
    with open(fname,'w+') as f:
        joke = results[0][0]
        comments = results[1]
        f.writelines(joke)
        for comment in comments:
            comment = comment.contents[0]
            if comment != None and comment[:2] != '回复':
                f.writelines('\n')
                f.writelines(comment)

    f.close()



if __name__ == '__main__':
    numjokes = 1000000                                                               # 笑话数
    failed_counts = 0                                                            # 抓取页面失败的次数
    for i in range(numjokes):
        print('processing:{}, {}% finished.'.format(i,i/float(numjokes/100)))
        try:
            x_id = 110693660 + i
            url = 'https://www.qiushibaike.com/article/' + str(x_id)      # 对应的url链接
            html = getHTMLText(url)                                              # 得到HTML页面
            results = parsePage(html)                                            # 对HTML页面进行解析,得到joke和comments
            if results == None:
                continue
            storage(results,x_id)                                                   # 保存结果

        except:
            continue

        sleeptime = np.random.randint(10,12)                                     # 防止频繁访问
        time.sleep(sleeptime)
