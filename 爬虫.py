import requests
import os
from bs4 import BeautifulSoup
import time

def request(url,header={'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"}):
    r=requests.get(url,headers=header)
    return r
def all_images(html):
    soup=BeautifulSoup(html,'lxml') #先解析再遍历查找！
    #找到所有的套图链接
    list=soup.find('div',class_="all").find_all('a')
    list.pop(0) #第一个为无用信息
    for link in list:
        title=link.get_text()
        print('开始保存：',title)
        path=title
        mkdir(path)
        all_url=link.get('href')
        image_html=request(all_url).text
        get_html(image_html,all_url)
def get_html(html,href):
    soup=BeautifulSoup(html,'lxml')
    tag=soup.find('div',class_="pagenavi")
    max_span = tag.find_all('span')[-2].get_text()
    for cnt in range(1,int(max_span)+1):
        next_href=href+'/'+str(cnt)
        print(next_href)
        image(next_href,href)
def image(next_href,href):
    time.sleep(2) ##下载延迟，防被抓！
    html=request(next_href).text
    img_url=BeautifulSoup(html,'lxml').find('div',class_='main-image').find('img')['src']
    save(img_url,next_href)
def save(img_url,next_href):
    name=img_url[-9:-4]
    header={'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",'referer':next_href}
    try:
        img=request(img_url,header).content    
    except:
        time.sleep(5)
    with open(name+'.jpg','ab') as f:
        f.write(img)
def mkdir(path):
    exist=os.path.exists(os.path.join("/mztu/download",path))
    if not exist:
        os.makedirs(os.path.join("/mztu/download",path)) #创建多层目录
        os.chdir(os.path.join("/mztu/download",path))
def main():
    url="https://www.mzitu.com//all"
    html=request(url)
    all_images(html.text)
main()