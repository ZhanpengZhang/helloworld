import re
import urllib.request
import urllib.error


def crawl(url, pg):
    html = urllib.request.urlopen(url).read()
    html = str(html)
    pat1 = r'<div id="plist".+? <div class="page clearfix">'
    result1 = re.compile(pat1).findall(html)
    result1 = result1[0]
    pat2 = r'<img width="200" height="200" data-img="1" src="//(.+?\.jpg)">|<img width="200" height="200" data-img="1" data-lazy-img="//(.+?\.jpg)">'
    imagelist = re.compile(pat2).findall(result1)
    num = 1
    global sum
    for imageurl in imagelist:
        if imageurl[0] != "":
            imageurl = "http://" + imageurl[0]
        else:
            imageurl = "http://" + imageurl[1]
        imagename = "../scraping/" + str(pg) + ":" + str(num) + ".jpg"
        print("downloading pic %d in page %d" % (num, pg))
        try:
            urllib.request.urlretrieve(imageurl, filename=imagename)
        except urllib.error.URLError as e:
            if hasattr(e, 'code') or hasattr(e, 'reason'):
                num += 1
        print("Pic %d in page %d downloaded" % (num, pg))
        num += 1
        sum += 1


sum = 0
for i in range(1, 259):
    pg = i
    url = "https://list.jd.com/list.html?cat=1713,3287,3797&page=%d" % pg
    crawl(url, pg)
