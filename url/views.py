from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
import requests
from urllib import request as req
from bs4 import BeautifulSoup as bs
from io import BytesIO
import base64

def viewurl(request,url):
    html=requests.get(url)
    soup=bs(html.text,"html.parser")
    soup.body="ads"
    result=soup.find_all('form')
    for i in result:
        try:
            makeabsolute(i,url,'action')
        except:
            pass

    result=soup.find_all('link')
    for i in result:
        try:
            makeabsolute(i,url)
            if not i.endswith('png'):
                i['href']='./'+i['href']
            else:
                i['href']='https://willnorris.com/api/imageproxy/'+i['href']
        except:
            pass
    result=soup.find_all('img')
    for i in result:

            makeabsolute(i,url,'src')
            img=req.urlopen(i['src'])


            i['src']="data:image/%s;base64,"%(i['src'][-3:])+base64.b64encode(BytesIO(img.read()).getvalue()).decode()

    result=soup.find_all('a')
    for i in result:
        try:
            makeabsolute(i,url)
            i['href']='./'+i['href']
        except:
            pass
    return HttpResponse(soup.html)

def getform(request):
        return render(request,'form.html')

def makeabsolute(i,url,tag='href'):
    if not i[tag].startswith("http"):
        if i[tag][0]=='/':
            i[tag]=url+i[tag]
        else:
            i[tag]=url+'/'+i[tag]