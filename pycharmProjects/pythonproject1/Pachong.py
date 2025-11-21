import os
import socket
import requests
from bs4 import BeautifulSoup

socket.setdefaulttimeout(500)

base = 'https://www.xxo.ee/'
baseurl = 'https://www.xxo.ee/forum.php?mod=forumdisplay&fid=159&filter=lastpost&orderby=lastpost'
co = open('E:\PYTHON\pycharmProjects\cookie\meicookie.txt', 'r')
cook = co.read()
header = {
    'cookie':
    cook,
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.42'
}


def login(baseurl):
    resq = requests.get(url=baseurl, headers=header)
    resq.encoding = resq.apparent_encoding
    html = resq.text
    bs = BeautifulSoup(html, 'lxml')
    divs = bs.find('form', id='moderate')
    tbodys = divs.find_all('a')
    return tbodys


def main(baseurl):
    global n
    tbodys = login(baseurl)
    for tbody in tbodys:
        href = tbody.get('href')
        name = tbody.text
        if name.find('石家庄') != -1 and name.find('中介') == -1 and name.find(
                '卸货') == -1:
            res = requests.get(href, headers=header)
            bs1 = BeautifulSoup(res.text, 'lxml')
            txts = bs1.find('div', class_="t_fsz")
            txte = txts.find('td', class_="t_f")
            txte = txte.text

            files = os.makedirs(R'E:\\PYTHON\\MEI\\' + i.__str__() + '-' +
                                n.__str__() + name)
            fil = R"E:\\PYTHON\\MEI\\" + i.__str__() + '-' + n.__str__(
            ) + name + '\\' + name + '.txt'
            f = open(fil, 'a', encoding='utf-8')
            f.write(txte)

            imgs = txts.find_all('img')
            for img in imgs:

                if img.get('zoomfile') is not None:
                    imgurl = base + img.get('zoomfile')
                    img_name = str(img.get('zoomfile').split('/')[-1])
                    img_path = R"E:\\PYTHON\\MEI\\" + i.__str__(
                    ) + '-' + n.__str__() + name + '\\' + img_name
                    img_get = requests.get(imgurl, headers=header).content
                    with open(img_path, 'wb') as f:
                        f.write(img_get)
            n += 1
            # print(img.get('zoomfile').split('/')[-1])


if __name__ == '__main__':
    n = 1
    for i in range(1, 20):
        if i == 1:
            main(baseurl)
            i += 1
        else:
            main(baseurl + '&page=' + i.__str__())
            i += 1
