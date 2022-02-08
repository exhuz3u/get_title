import requests
from bs4 import BeautifulSoup
import urllib3
import sys
import threadpool
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url=[]
the_url=[]
the_urls=[]
keywords=""
def get_title(url):
    try:
        resp = requests.get(url, verify=False, timeout=3)
        html=BeautifulSoup(resp.content,'lxml')
        title=html.title.text
        print("url:"+url," "+"title:"+title)
        if keywords in title:
            with open ("result.txt","a") as f:
                f.write("url: "+url+"       "+"title: "+title+"\n")
    except requests.exceptions.ConnectionError:
        print("url:"+url+" 无效")
        
def url_list(file_name):
    global the_url
    with open (file_name,'r') as f:
        the_url=f.readlines()
    the_url = [ x.strip() for x in the_url if x.strip() != '']
    for i in the_url:
        ni="http://"+i
        nis="https://"+i
        the_url[the_url.index(i)]=ni
        the_urls.append(nis)
        
def td():
    print(url)
    pool = threadpool.ThreadPool(50) 
    requests = threadpool.makeRequests(get_title, url)
    [pool.putRequest(req) for req in requests]
    pool.wait()
    
def main():
    global url,keywords
    pwd=sys.argv[0].rsplit("\\",1)
    print("当前位置:"+pwd[0])
    file_name=input("请输入文件名:")
    keywords=input("请输入关键词:")
    url_list(str(pwd[0]+"\\"+file_name))
    url=the_url+the_urls
    td()
    
main()
