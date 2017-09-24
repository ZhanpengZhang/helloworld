# -*- coding: utf-8 -*-
# 下载捧腹网的笑话
import sys
import urllib.request
from bs4 import BeautifulSoup
import csv
import re
import math

# source code
# 抓取网页源代码
def gethtml(page):
  url = 'https://www.pengfu.com/index_' + str(page) + '.html'
  headers = {
      'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
  req = urllib.request.Request(url)
  html = urllib.request.urlopen(req).read()
  bsObj = BeautifulSoup(html, "lxml")
  return bsObj


# get the headings on a page, and make them a headinglist.
# 抓取当页小标题，存入全局的一个列表--refined_hl.
def getheadinglist(page):
  headinglist = gethtml(page).find_all("h1", {"class": "dp-b"})
  for heading in headinglist:
    refined_hl.append(heading.text.strip(' \t\n\r'))
  return refined_hl


# get content on the page and group them into a contentlist.
# 抓取当页笑话的图片地址或文字，存入全局的一个列表--refined_cl.
def getcontentlist(page):
  num = 0
  contentlist = gethtml(page).find_all(
      "div", {"class": "content-img clearfix pt10 relative"})
  for content in contentlist:
    if (content.img) != None:
      try:
        imageurl = content.img.attrs["gifsrc"]
        print("An gif found:", imageurl)
      except KeyError:
        print("Oops, a keyerror encountered",
              content.img.attrs.get("gifsrc"), "gif here")
        if content.video != None:
          imageurl = content.video.attrs['poster']
          videourl = content.source.attrs["src"]
          print("Hey, a video found:", videourl)
          imageurl = imageurl + "\n" + videourl
        else:
          imageurl = content.img.attrs["jpgsrc"]
        print ("An jpg found:", imageurl)
      if content.text != None:
        description = content.text.strip(' \t\n\r')
        pics_ds = imageurl + "\n" + description
        refined_cl.append(pics_ds)
      else:
        refined_cl.append(imageurl)
    else:
      refined_cl.append(content.text.strip(' \t\n\r'))
    num += 1
    print("Page %d Joke number %d gotton from the messy world of pengfu's html" % (
        page, num))
  return refined_cl


# match headings and content into tuples and group them into a list.
# 将收集好的内容列表和小标题列表匹配成很多个元祖，归入一个列表中
def mergelist():
  heading_content_zipped = zip(refined_hl, refined_cl)
  global heading_content
  heading_content = list(heading_content_zipped)
  heading_content.insert(0, ("heading", "content"))
  return heading_content


# 将这个列表逐行写入一个csv文件
def saveintocsv():
  csvfile = open("./peng_fu.csv", "wt", newline="", encoding="utf-8")
  writer = csv.writer(csvfile)
  for row in heading_content:
    writer.writerow(row)
  csvfile.close()


# 从内容列表里找出图片地址，下载保存到本地一个文件夹，命名格式为：所在页：笑话在当页的序号。
def download_pictures():
  num_of_pic = 0
  jpgpat = re.compile(".+\.jpg")
  gifpat = re.compile(".+\.gif")
  for link in refined_cl:
    num = refined_cl.index(link) + 1
    pg = math.ceil(num / 10)
    if num / 10 == num // 10:
      numwithin = 10
    else:
      numwithin = num - math.floor(num / 10) * 10
    jpglink = jpgpat.match(link)
    giflink = gifpat.match(link)
    if jpglink:
      imagename = "./scraping/peng_fu/" + \
          str(pg) + ":" + str(numwithin) + ".jpg"
      imageurl = jpglink.group()
    elif giflink:
      imagename = "./scraping/peng_fu/" + \
          str(pg) + ":" + str(numwithin) + ".gif"
      imageurl = giflink.group()
    else:
      continue
    urllib.request.urlretrieve(imageurl, filename=imagename)
    num_of_pic += 1
    print("%d images downloaded." % num_of_pic)


# 只有作为主文件执行时，才会开始抓取。目前设置为抓取54页（这是网站的页数）。import不会实施抓取。
if __name__ == "__main__":
  global page
  global refined_hl
  global refined_cl
  refined_cl = []
  refined_hl = []
  heading_content = []
  numofpages = 55
  for i in range(1, numofpages):
    page = i
    getheadinglist(page)
    getcontentlist(page)
  mergelist()
  saveintocsv()
  download_pictures()

