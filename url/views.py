from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from http import cookies,cookiejar
from urllib.parse import urlparse, urlencode
from urllib import request as req
from bs4 import BeautifulSoup as bs


@csrf_exempt
def viewurl(request,url):
    if not url.startswith("http"):
        url="http://"+url

    content=req.urlopen(req.Request(url+"?"+urlencode(request.GET),headers={'Cookie': ("" if not 'cookie' in request.COOKIES else request.COOKIES['cookie'])}))
    url=urlparse(url).netloc
    html=content.read()
    cook=cookies.SimpleCookie()
    if not 'html' in content.getheader('Content-Type'):
        #startswith('text/html')
        response=HttpResponse(html, content_type=content.getheader('Content-Type'))
        # for key,value in content.getheaders():
        #     if not key in hop:
        #      response[key]=content.getheader(key)
        # #response['Set-Cookie']=content.getheader('Set-Cookie')
        if 'cookie' in request.COOKIES:
            response.set_cookie( 'cookie', request.COOKIES['cookie']+str(content.getheader('Set-Cookie')))
        else:
            response.set_cookie( 'cookie', content.getheader('Set-Cookie'))


        return response


    soup=bs(html,"html.parser")
    replacelinks(soup.find_all('form', attrs = {'action' : True}),url,'action')
    replacelinks(soup.find_all('script', attrs = {'src' : True}),url,'src')

    replacelinks(soup.find_all('link', attrs = {'href' : True}),url)
    replacelinks(soup.find_all('a', attrs = {'href' : True}),url)
    replacelinks(soup.find_all('img', attrs = {'src' : True}),url,'src')

    response=HttpResponse(str(soup))
    if 'cookie' in request.COOKIES:
        response.set_cookie( 'cookie', str(content.getheader('Set-Cookie')))
    else:
        response.set_cookie( 'cookie', content.getheader('Set-Cookie'))


    # for key,value in content.getheaders():
    #     if not key in hop:
    #          response[key]=content.getheader(key)
    # #response['Set-Cookie']=content.getheader('Set-Cookie')

    return response

def getform(request):
        return render(request,'form.html')

def makeabsolute(i,url,tag):
    if not i[tag].startswith("http") and not i[tag].startswith("java"):
        if i[tag][0]=='/':
            i[tag]=url+i[tag]
        else:
            i[tag]=url+'/'+i[tag]

def replacelinks(result,url,param='href'):
    for i in result:
        try:
            makeabsolute(i,url,param)

            i[param]='/'+i[param]
            if param =='action':
                new_tag = soup.new_tag("a", href="/"+url)
                original_tag.append(new_tag)



        except:
            pass
