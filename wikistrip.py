import urllib

def getWikiData(url):
    rawList = []
    filehandle = urllib.urlopen(url)
    for lines in filehandle.readlines():
        print lines

getWikiData('http://wikipedia.org')
