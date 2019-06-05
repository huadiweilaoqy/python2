import requests
import urllib.parse
import os
from lxml import etree
import random
import csv
import re
# word=input("请输入要搜索的物品：")
word="天气"
#转码
keyword=urllib.parse.quote(word)
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
        'Cookie':'BAIDUID=2648A2F413254851570B9384076B67B5:FG=1; PSTM=1549538544; BIDUPSID=5FCD029EA7F1A411C291E12C980BF8BD; BDUSS=hSVXRxZWRHTHJrU0hmRURLbk9wcnJJUW1udXk2MVVhUDQwSUNWLUtEb1BTWlJjQVFBQUFBJCQAAAAAAAAAAAEAAABc5iWmsrvP67HP0rW1xM6iwbkAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA-8bFwPvGxcRl; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; delPer=0; BD_CK_SAM=1; PSINO=5; H_PS_PSSID=; BDRCVFR[C0p6oIjvx-c]=mk3SLVN4HKm; BDSVRTM=152',
        'Host':'news.baidu.com'    
        }
j=1
details=[["标题","来源","发布时间","简介","链接"]]
class GetNews:
    #初始化
    def __init__(self):
        #创建文件夹
        global path
        path="./baidunew/"
        if not os.path.exists(path):
            os.mkdir(path)
        self.path=path
    def requests_get(self,url):
        r=requests.Session()
        response=r.get(url,headers=headers,timeout=random.randint(10,220),allow_redirects=False)
        response.encoding='utf-8'
        tree=etree.HTML(response.text)
        self.tree_results=tree.xpath('//div[@class="result"]')
        self.text=response.text
    def get_msg(self):
        try:
            results={}
            global j
            for result in self.tree_results:
                div_id=result.xpath('@id')[0]
    #             标题
                contents=""
                for i in result.xpath('//div[@id="{}"]/h3/a//text()'.format(div_id)):
                    contents+=i
                results['title']=contents.strip()
                #来源
                froms=''.join(result.xpath('//div[@id="{}"]//p[@class="c-author"]//text()'.format(div_id))).split()
                results['from']=froms[0]
                results['before']=froms[1]
                #简介
                texts=re.findall('<div class="result" id="{}">.*?</p>(.*?)<span.*?>'.format(div_id),self.text,re.S)
                for text in texts:
                    results['intro']=text.replace('<em>','').replace('</em>','').strip()
                #链接
                for i in result.xpath('//div[@id="{}"]/h3/a'.format(div_id)):
                    results['href']=i.xpath('@href')[0]
                #传入detail列表
                j+=1
                details.append([results[key] for key in results.keys()])
        except Exception as e:
            print("异常是：%s"%e)
#——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————            
#word是关键字，pn是页数，初始0，间隔20
for pn in range(0,560,20):
    url="http://news.baidu.com/ns?word={0}&pn={1}&cl=2&ct=1&tn=news&rn=20&ie=utf-8&bt=0&et=0".format(keyword,pn)
    pachong=GetNews()
    pachong.requests_get(url)
    pachong.get_msg()
with open(path+"baidunews.csv","a",newline="",encoding="gb18030") as fp:
    write=csv.writer(fp)
    a=1
    for msg in details:
        if len(msg) !=0:
            write.writerow(msg)
            print("已写入%d条信息"%a)
            a+=1
print("共爬取{0}页,{1}条信息！".format(pn//20+1,j-1))
print("CSV文件写入完毕！共写入%d条！"%(a-1))  #details里有一条初始数据，所以多一条