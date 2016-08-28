from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
import requests
from urllib import request as req
from bs4 import BeautifulSoup as bs
from io import BytesIO
import base64

def viewurl(request,url):
    if url[-4:]==".ext":
        return HttpResponse(requests.get(url[:-4]).text)
    html=requests.get(url)
    pos=url.find('?')
    if pos>-1:
        url=url[:pos]
    soup=bs(html.text,"html.parser")
    replacelinks(soup.find_all('form', attrs = {'action' : True}),url,'action')
    replacelinks(soup.find_all('script', attrs = {'src' : True}),url,'src')

    replacelinks(soup.find_all('link', attrs = {'href' : True}),url)
    replacelinks(soup.find_all('a', attrs = {'href' : True}),url)

    result=soup.find_all('img', attrs = {'src' : True})
    for i in result:

            makeabsolute(i,url,'src')
            img=req.urlopen(i['src'])

            imag=base64.b64encode(BytesIO(img.read()).getvalue()).decode()
            i['src']="data:image/%s;base64,"%(i['src'][-3:])+imag
            if i.has_attr('srcset'):
                del i['srcset']


    return HttpResponse(soup.html)

def getform(request):
        return render(request,'form.html')

def makeabsolute(i,url,tag):
    if not i[tag].startswith("http"):
        if i[tag][0]=='/':
            i[tag]=url+i[tag]
        else:
            i[tag]=url+'/'+i[tag]

def replacelinks(result,url,param='href'):
    for i in result:
        try:
            makeabsolute(i,url,param)
            if not i[param].endswith('png'):
                i[param]='/'+i[param]
                if i.has_attr('type') or i.has_attr('rel'):
                    i[param]=i[param]+".ext"
            else:
                i[param]='https://willnorris.com/api/imageproxy/'+i[param]
        except:
            pass
