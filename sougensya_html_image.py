import requests
import lxml.html
import MySQLdb
import requests
import re
import uuid
from bs4 import BeautifulSoup


# データベースに接続する
connection = MySQLdb.connect(
    user="calcdrops",
    passwd="Hiro04070528",
    host="localhost",
    db="swim_test",
    charset="utf8"
    )

# カーソルを生成する
cursor = connection.cursor()


# 1ページ目以降を連続で取得する
print("1ページ目以降を連続で取得する")
for page in range(1, 10):
    num_page = page
    r_page = requests.get("http://www.tsogen.co.jp/np/searchresult.html?lgen_id=1&page=%d" % (page))
    r_page.encoding = r_page.apparent_encoding
    html_page = r_page.text
    root_page = lxml.html.fromstring(html_page)
    print(str(num_page) + "ページ目に取り組みますわい")


    for int in range(5, 25):
        num_book = (num_page-1)*20 + int - 4
        t1 = root_page.xpath("//*[@id='main']/div[2]/div[%d]/div[1]/p[1]/a/strong/span[1]" % (int))
        t2 = root_page.xpath("//*[@id='main']/div[2]/div[%d]/div[1]/p[2]/a/strong/span[1]" % (int))
        l1 = root_page.xpath("//*[@id='main']/div[2]/div[%d]/div[1]/p[1]/a" % (int))
        l2 = root_page.xpath("//*[@id='main']/div[2]/div[%d]/div[1]/p[2]/a" % (int))
        a1 = root_page.xpath("//*[@id='main']/div[2]/div[%d]/div[1]/p[2]/a[1]" % (int))
        a2 = root_page.xpath("//*[@id='main']/div[2]/div[%d]/div[1]/p[3]/a[1]" % (int))
        o1 = root_page.xpath("//*[@id='main']/div[2]/div[%d]/div[2]/p/text()" % (int))
        i1 = root_page.xpath("//*[@id='main']/div[2]/div[%d]/p[2]/a/img" % (int))

        if len(t1)==0:
            title = t2[0].text
        else:
            title = t1[0].text

        if "searchresult.html" in l1[0].attrib["href"]:
            link = l2[0].attrib["href"]
        else:
            link = l1[0].attrib["href"]

        if a1[0].text is None:
            auther = a2[0].text
        else:
            auther = a1[0].text

        overview = o1[0]
        image_url = i1[0].attrib["src"]

        cursor.execute("INSERT INTO sougensya_with_image_url VALUES(%s, %s, %s, %s, %s, %s)", (num_book, title, link, auther, overview, image_url))
        connection.commit()

        # 画像の取得
        print(image_url)
        image_r = requests.get("http://www.tsogen.co.jp%s" % (image_url))
        with open(str('./picture/') + str(num_book) + str('.jpeg'), 'wb') as file:
                file.write(image_r.content)

print("全部保存したぞ！")
