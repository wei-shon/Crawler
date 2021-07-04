#conda activate base
import requests
from bs4 import  BeautifulSoup
import pandas
import time


def crawler(src):
    #use request
    #use headers because the goodinfo will block the crawler to crawl
    headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
    }
    response = requests.get(src,headers=headers)
    response.encoding='utf-8' #since there are a lots of chinese then we use utf-8 to encode then we can know the content

    #Using bs4 analying the content. we want to use pandas so we should use bs4
    soup = BeautifulSoup(response.text,'lxml')
    #要注意他的標籤時常更換!!!!!!! 所以抓不出資料代表標籤又更換了!!!!!!
    data = soup.find('table',class_='b1 p4_2 r10')
    #using pandas to get the table of stock
    dfs=pandas.read_html(data.prettify())
    df=dfs[0]

    #抓出表格內容，並寫入stock.txt
    with open('stock.txt','ab') as f:
        for i in range(0,len(df)-3):
            for j in range(0,len(df.columns)):
                if(i==0 and j>0):
                    break
                else:
                    f.write((str(df.at[i,j])+str('  ')).encode('utf-8'))
            f.write('\n'.encode('utf-8'))
        #f.write(df.to_string().encode('utf-8'))
        f.write('\n'.encode('utf-8'))
        f.close()

#先把Stock.txt裡面的內容清空
f=open('stock.txt','w')
f.write('')
f.close()
#再來呼叫crawlre 把我想要的股票資訊抓進去
source=['https://goodinfo.tw/StockInfo/StockDetail.asp?STOCK_ID=2330' ,
        'https://goodinfo.tw/StockInfo/StockDetail.asp?STOCK_ID=2610' ,
        'https://goodinfo.tw/StockInfo/StockDetail.asp?STOCK_ID=2618' ,
        'https://goodinfo.tw/StockInfo/StockDetail.asp?STOCK_ID=2884' ,
        'https://goodinfo.tw/StockInfo/StockDetail.asp?STOCK_ID=2885']
#若抓太多次 服務會被Goodinfo關閉!!!!
for i in range(len(source)):
    crawler(source[i])

print("Done.")