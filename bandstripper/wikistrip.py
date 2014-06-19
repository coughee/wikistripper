import urllib
import re
import codecs
from sys import stdout
from HTMLParser import HTMLParser
from pattern.web import plaintext

class urlParser(HTMLParser):
    def __init__(self, output_list=None):
        HTMLParser.__init__(self)
        if output_list is None:
            self.output_list = []
        else:
            self.output_list = output_list
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            self.output_list.append(dict(attrs).get('href'))

def getData(url):
    #returns the page
    data = urllib.urlopen(url)
    return data

def findUrlsInLine(line):
    #strips urls from line
    p = urlParser()
    p.feed(line)
    return p.output_list
    
def findUrls(url):
    pageData = getData(url)
    urlList = []
    for lines in pageData.readlines():
        lineUrls = findUrlsInLine(lines)
        if(lineUrls is not []):
            for url in lineUrls:
                urlList.append(url)

    return urlList

def getFullUrlList(url):
    listOfUrls = findUrls(url)
    fullList = []
    prefix = 'http://en.wikipedia.org/'
    for lines in listOfUrls:
        if lines is not None:
            if lines.startswith('/wiki/L'):
                
                fullList.append(prefix + lines[1:])
    return fullList

def getListElements(page):
    newpage = []
    for lines in page:
        s = plaintext(str(lines), keep={'li'})
        if s is not None and s is not '':
            newpage.append(s)
    return newpage

def getFoods(url):
    print url
    page = getData(url)
    foodlist = []
    for lines in page:
        s = plaintext(str(lines),keep={'a':['href']})
        s = re.findall(r'>(.*?)<', s)
        if s:
            foodlist.append(s)
        
    return foodlist

def getFoodList(url):
    urlList = getFullUrlList(url)
    foodlist = []
    for urls in urlList:
        foodlist.extend(getFoods(urls))
    return foodlist


url = 'http://en.wikipedia.org/wiki/Lists_of_musicians'
foodlist = getFoodList(url)
f = codecs.open('bands.txt', 'w', encoding='utf-8')
for lines in foodlist:
    f.write("%s\n" % lines[0])
