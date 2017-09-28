from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os

from flask import Flask
from flask import request
from flask import make_response

import requests
from bs4 import BeautifulSoup as bs

app = Flask(__name__)

@app.route('/')
def index():
    return 'OK'

@app.route('/webhook',methods=['POST'])
def webhook():
    request = request.get_json(silent=True,force=True)
    print("Request : " + json.dumps(req, indent=4))

    endData = processRequest(request)
    response = make_response(endData)
    response.headers['Content-Type'] = 'application/json'
    return response


def processRequest(req):
    if req.get("result").get("action") != "SnapdealSearch":
      return {}

    searchParams = req.get("result").get("parameters").get("any")
    if searchParams is None:
        return {}
    searchResult = snapdeal(searchParams) #will return a list of five
    searchLinks = snapdealL(searchParams) #will return a list of links(use in context)

    r =  makeWebhookResult(searchResult,searchLinks)
    return r



def snapdeal(search):
    search = search.replace(" ","%20")
    cat2 = "&santizedKeyword=iphone&catId=0&categoryId=0&suggested=false&vertical=p&noOfResults=20&searchState=&clickSrc=go_header&lastKeyword=&prodCatId=&changeBackToAll=false&foundInAll=false&categoryIdSearched=&cityPageUrl=&categoryUrl=&url=&utmContent=&dealDetail=&sort=rlvncy" 
    cat1 = "https://www.snapdeal.com/search?keyword="
    url = cat1 + serch + cat2
    r = requests.get(url)
    soup = bs(r.content,"html.parser")
    sections = soup.findAll("section")
    result = list()

    for item in sections:
        n = item.findAll("div",{"class":"product-tuple-description"})
        for i in n:
            title = i.findAll("a")[0].findAll("p")[0].text
            price = i.findAll("a")[0].findAll("div",{"class":"product-price-row clearfix"})[0].findAll("span",{"class":"lfloat product-price"})[0].text
            result.append(title + " of price " + price )

    topresult = list()
    for i in range(5):
        topresult.append(result[i])

    return topresult

def snapdealL(search):
    search = search.replace(" ","%20")
    cat2 = "&santizedKeyword=iphone&catId=0&categoryId=0&suggested=false&vertical=p&noOfResults=20&searchState=&clickSrc=go_header&lastKeyword=&prodCatId=&changeBackToAll=false&foundInAll=false&categoryIdSearched=&cityPageUrl=&categoryUrl=&url=&utmContent=&dealDetail=&sort=rlvncy" 
    cat1 = "https://www.snapdeal.com/search?keyword="
    url = cat1 + serch + cat2
    r = requests.get(url)
    soup = bs(r.content,"html.parser")
    sections = soup.findAll("section")
    result = list()

    for item in sections:
        n = item.findAll("div",{"class":"product-tuple-description"})
        for i in n:
            l = i.findAll("a", href=True)[0]['href']
            result.append(l)

    topresult = list()
    for i in range(5):
        topresult.append(result[i])

    return topresult

def makeWebhookResult(TP,links):
    # for titles AND Prices only
    speech = "The top five results are"

    for item in TP:
        speech = speech = " " + item + " and "
    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        "data": "",
        "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }

    
    

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')

    



    
    
    
