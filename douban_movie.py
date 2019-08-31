# -*- coding: utf-8 -*-
import requests
import csv
import time
#第一个函数获取申肖克救赎的海报图片
def douban():
    try:
        url ='https://api.douban.com/v2/movie/1292052?apikey=0df993c66c0c636e29ecbb5344252a4a'
        r = requests.get(url,timeout=30)
        r.raise_for_status()  #如果状态不是200, 引发HTTPError异常
        r.encoding = r.apparent_encoding
#将请求得到的json格式的字符串直接转成一个真正的字典。
        res_dict=r.json()
#获得image的url地址
        res_url=res_dict['image']
#新的url发送get请求        
        req=requests.get(res_url)
#将req.content得到的二进制内容以二进制形式写入本地的sxk.jpg 文件中  
        with open('sxk.jpg', 'wb') as f: 
            f.write(req.content)
        print('sxk.jpg已保存到当前文件夹')
    except:
         print("产生异常")



#第二个函数获取top250影片信息
def top250():
    try:
#新建空列表用于存放影片信息       
        relist=[]
#设置循环控制star变量每次得到20个影片
        for i in range(0,250,20):
            url  =('https://api.douban.com/v2/movie/top250?start=%s&apikey=0df993c66c0c636e29ecbb5344252a4a' % i)
            r=requests.get(url)
            r.raise_for_status() 
#如果状态不是200, 引发HTTPError异常
            r.encoding = r.apparent_encoding
            re_dict=r.json()
 #获取字典subjects键对应的影片信息          
            subjects=re_dict['subjects']
#批量获取影片的名称,id,评分,类型，时长，年代，影片地址
            for c in subjects:
                title=c['title']
                id=c['id']
                rating=c['rating']['average']
                genres=c['genres'][:]
                durations=c['durations'][:]
                year=c['year']
                alt=c['alt']
#把所获得的信息添加到空列表中                  
                relist.append([
             title,id,rating,genres,durations,year,alt
        ])
                 #这段，先打开文件获取文件top250csv，其中newline是用来控制不要写入一行，能够匹配到\r\n空格等，然后使用writer获取文件写入对象，最后使用writerow来一行行的写入
        with open('top250.csv', 'w', newline='') as csvfile:
            cvwrite = csv.writer(csvfile)
            cvwrite.writerow(
         [
            '影片名','id','评分','类型','时长','年代','地址'
         ] )
            
            for x in relist:
               cvwrite.writerow(x)
            print('获取成功:保存在当前目录top250.csv文件')
    except:
         print('获取失败')


#第三个函数批量top250海报图片
def haibao():
#设置变量t获得当前下载的得图片位数	
    t=1
#利用循环获得top250对应的海报图片
    for i in range(0,250,20):
    
        url =('https://api.douban.com/v2/movie/top250?start=%s&apikey=0df993c66c0c636e29ecbb5344252a4a' % i)
        r=requests.get(url)
        r.raise_for_status() 
#如果状态不是200, 引发HTTPError异常
        r.encoding = r.apparent_encoding
        re_dict=r.json()
#利用字典获取subjects对应的键值信息       
        subjects=re_dict['subjects']
#遍历subjects中的海报图片和影片id   
        for a in subjects:
            print('正在下载第%s张图片' % t)
#获取海报图片地址这里选择small小图。            
            image=a['images']['small']
#获取影片id，用id给海报图片命名          
            id=a['id']
#获得海报图片的地址            
            imagelist=requests.get(image)
 #设置海报图片文件名           
            path=id+'.jpg'
#设置保存路径picture文件夹            
            with open('picture/'+path,'wb') as f:
#写入二进制数据	        
		            f.write(imagelist.content)
            time.sleep(3)     
            t+=1
    print('图片已保存在当前目录下的picture文件夹')      
                 
        
if __name__=="__main__":
   print('肖申克救赎图片下载')
   douban()
   print('批量获取top250影片信息')
   top250()
   print('批量获取top250海报')
   haibao()
