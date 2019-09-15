from flask import Flask
from flask import render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__, static_folder='static')


@app.route('/')
def index():
    novelName = "九星霸体诀"

    URL = "https://www.biquge.com.cn/search.php?keyword=" + novelName
    r = requests.get(URL)
    soup1 = BeautifulSoup(r.content, 'html.parser')
    book_url = soup1.find_all(
        "a", class_="result-game-item-title-link")[0].get_attribute_list('href')[0]

    r = requests.get(book_url)
    soup2 = BeautifulSoup(r.content, 'html.parser')
    contents = soup2.find_all("dd")

    data = []
    for item in contents:
        temp = {}
        temp["chapterName"] = item.a.get_text()
        temp["link"] = item.a.get_attribute_list('href')[0]
        data.append(temp)

    return render_template('home.html', novelName=novelName, data=data)


@app.route('/chapter')
def get_chapter():
    chapterLink = request.args.get('chapterLink')

    URL = "https://www.biquge.com.cn" + chapterLink
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html.parser')

    title = soup.select("div.bookname h1")[0].get_text()
    content = soup.find(id="content")

    return render_template('chapter.html', title=title, content=content, chapterLink=chapterLink)


@app.route('/nav_chapter')
def nav_chapter():
    diretion = request.args.get('diretion')
    chapterLink = request.args.get('chapterLink')

    bookId = chapterLink.split('/')[2]
    chapterId = int(chapterLink.split('/')[-1].split('.')[0])

    if diretion == 'prev':
        chapterId = chapterId - 1
    else:
        chapterId = chapterId + 1

    chapterLink = "/book/" + \
        bookId + "/" + str(chapterId) + ".html"

    URL = "https://www.biquge.com.cn" + chapterLink
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html.parser')

    title = soup.select("div.bookname h1")[0].get_text()
    content = soup.find(id="content")

    return render_template('chapter.html', title=title, content=content, chapterLink=chapterLink)


# We only need this for local development.
if __name__ == '__main__':
    app.run(debug=True)
