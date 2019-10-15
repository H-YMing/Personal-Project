#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding=utf-8
from PyQt5.QtWidgets import (QMessageBox, QWidget, QPushButton, QDesktopWidget, QLineEdit, QLabel, QComboBox, QApplication)
from PyQt5.QtGui import QIcon
import sys
import requests
from bs4 import BeautifulSoup
import re
from random import choice
Headers = [{'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36', "Referer": 'http://www.baidu.com/'},
           {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1', "Referer": 'http://www.baidu.com/'},
           {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0', "Referer": 'http://www.baidu.com/'},
           {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50', "Referer": 'http://www.baidu.com/'},
           {'User-Agent': 'Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50', "Referer": 'http://www.baidu.com/'}]


class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.headers = Headers
        self.resize(500, 300)    # 主窗口尺寸、坐标、标题
        self.center()
        self.setWindowTitle('小说下载')
        self.setWindowIcon(QIcon('web.jpg'))
        self.setMinimumSize(500, 300)  # 设置最小尺寸
        self.set_UI()
        self.novdetailurl = ""

    def set_UI(self):
        self.qle = QLineEdit(self)  # 小说名
        self.btn = QPushButton("搜索", self)  # 搜索按钮
        self.combo = QComboBox(self)  # 小说网站下拉列表
        self.combo.addItem("笔趣阁")
        self.nov = QLabel(self)  # 搜索到的小说名
        self.writer = QLabel(self)  # 搜索到的小说作者
        self.click = QPushButton("下载", self)  # 点击下载小说全部内容
        self.click.setVisible(False)
        self.click.clicked.connect(self.novelDetail)
        self.btn.clicked.connect(self.buttonClicked)

    def novelDetail(self):
        try:
            r = requests.get(url=self.novdetailurl, headers=choice(self.headers))
            r.encoding = 'gbk'
            content = r.text
            # print(content)
            self.praseNovelContent(content)
        except Exception as e:
            self.error(e)

    def praseNovelContent(self, content):
        re_chapter = r'id="list".*?</dt>(.*?)</dl>'
        chapter_list = re.findall(re_chapter, content, re.S | re.M)
        re_chapter = r'<dd>(.*?)</dd>'
        # print("chapter_list:", len(chapter_list))
        chapter_list = re.findall(re_chapter, chapter_list[0], re.S | re.M)
        file = open(f'./{self.nov.text()}.txt', 'a', encoding="utf-8")
        for chapter in chapter_list:
            chapter_url = re.findall(r'<a.*?href="(.*?)"', chapter, re.S | re.M)
            chapter_url = self.novdetailurl+chapter_url[0].strip()
            chapter_name = re.findall(r'>(.*?)</a>', chapter, re.S | re.M)
            chapter_name = chapter_name[0].strip()
            self.chapter_download(chapter_url, chapter_name, file)
            # print(chapter_name+"......")
        # print("小说下载完毕。。。")
        self.message('小说下载完毕！')
        file.close()

    def chapter_download(self, url, name, file):
        r = requests.get(url=url, headers=choice(self.headers))
        r.encoding = 'gbk'
        if r.text:
            # re_chapter = r'id="list".*?</dt>.*?</dt>(.*?)</dl>'
            chapter_list = re.findall(r'<div.*?id="content".*?>(.*?)</div>', r.text, re.S | re.M)
            # content = BeautifulSoup(r.text, 'html.parser').find(name='div', id='content').text
            # content = re.sub(r"</p>", "\\n", content)
            content = chapter_list[0]
            # print(content)
            content = content.replace("</p>", "\n")
            content = content.replace("<br>", "\n")
            content = content.replace("<br />", "\n")
            content = content.replace("</br>", "\n")
            content = content.replace("&nbsp;", " ")
            # print("====", content)
            # content = re.sub(r"<br>", "\\n", content)
            # print(content)
            content = re.sub(r"<script>(.*?)</script>", "", content)
            content = re.sub(r"</?(.+?)>", "", content)
            file.write(name+"\n\n")
            file.write(content+"\n\n")

    def buttonClicked(self):
        name = self.qle.text()
        webname = self.combo.currentText()
        if webname.strip() == "笔趣阁":
            web = "https://www.biduo.cc/search.php?keyword="+name
        self.content(web)

    def content(self, web):
        try:
            r = requests.get(url=web, headers=choice(self.headers))
            r.encoding = 'utf-8'
            content = r.text
            self.praseContent(content)

        except Exception as e:
            self.error(e)

    # 解析内容
    def praseContent(self, content):
        # print(111)
        soup = BeautifulSoup(content, 'html.parser')
        novels = soup.find(name='div', class_="result-item result-game-item")
        if novels:
            self.novdetailurl = novels.find('a').get('href')
            self.nov.setText(novels.span.text.strip())
            self.writer.setText("作者："+novels.find(name='p', class_='result-game-item-info-tag').find_all('span')[1].text.strip())
            self.click.setVisible(True)
        else:
            self.message('网站没有找到该小说')

        # content = soup.find(name='div', id="content").text
        # next1 = soup.find(name='div', class_="bottem1").find_all('a')[2].get('href')

    def message(self, mes):
        reply = QMessageBox.information(self, '提示', mes)

    def error(self, e):
        reply = QMessageBox.critical(self, 'Error', str(e))

    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def resizeEvent(self, event):
        self.qle.resize(300, 25)
        self.qle.move((self.width()-self.qle.width())/2, self.height()/8)

        self.btn.resize(50, 25)
        self.btn.move(self.qle.geometry().x()+self.qle.width()+10, self.qle.geometry().y())

        self.combo.resize(100, 25)
        self.combo.move((self.width()-self.combo.width())/2, self.qle.geometry().y()-30)

        self.nov.resize(300, 25)
        self.nov.move((self.width()-self.qle.width())/2, self.height()/8+30)

        self.writer.resize(300, 25)
        self.writer.move((self.width()-self.qle.width())/2, self.height()/8+50)

        self.click.resize(100, 25)
        self.click.move((self.width()-self.qle.width())/2, self.height()/8+70)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = Example()
    window.show()
    sys.exit(app.exec_())
