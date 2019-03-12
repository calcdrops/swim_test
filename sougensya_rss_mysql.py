import feedparser
import MySQLdb

"""東京創元社の新刊情報に関するRSSを取得してMySQLに保存する"""
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

def rss_read():
    rss = feedparser.parse("http://www.tsogen.co.jp/np/newbooks_bunko.rss")
    num = len(rss["entries"])
    num_book = 0

    for i in range(num):
        num_book += 1
        title = rss["entries"][i]["title"].split()[0] #タイトルの取得
        auther = rss["entries"][i]["title"].split()[1] #著者の取得
        try:
            translator = rss["entries"][i]["title"].split()[3] # 著者の取得
        except:
            translator = '訳者なし'
        overview = rss["entries"][i]["summary"][15:] # あらすじの取得
        pub_date = rss["entries"][i]["summary"][1:12] # 発売日の取得
        link = rss["entries"][i]["link"] # リンクの取得

        cursor.execute("INSERT INTO sougensya_rss VALUES(0, %s, %s, %s, %s, %s, %s, %s)", (num_book, title, link, auther, translator, overview, pub_date))
        connection.commit()

# main実行ブロック
if __name__ == '__main__':
    rss_read()
    print("全部保存したぞ！")
