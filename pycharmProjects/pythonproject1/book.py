import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import time

def main():
    Myheaders = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.52'
                    
    }
    pic_list_url = "http://www.bqge.org/book/8872/"

    pic_list_html = requests.get(pic_list_url, headers = Myheaders)
    pic_list_html.encoding = 'uft-8'
    time.sleep(1)

    soup = BeautifulSoup(pic_list_html.text,'lxml')
    pic_lists = soup.find('div',{"class":'listmain'})
    pic_lists =  pic_lists.find_all('dd')
    time.sleep(1)

    for pic_li in tqdm(pic_lists):
        pic_url = 'http://www.bqge.org'+pic_li.find('a').get('href')
        pic_name = pic_li.find('a').get_text()
        
        book = requests.get(pic_url,headers = Myheaders)
        book.encoding = 'uft-8'

        book_txt = BeautifulSoup(book.text,'lxml')
        book_txt_txt = book_txt.find('div',id = 'content').get_text()
        book_txt_lists = book_txt_txt.replace('\n','').replace('\r','').replace('\t','').replace(' ', '').replace('首发域名ｍ.bqge。org',
         '').replace('一秒记住网址ｈｔtｐ://ｍ.bqge。org', '')
        book_txt_lists = book_txt_lists.replace('\xa0\xa0\xa0\xa0\xa0','\n  ')

        print(book_txt_lists)
        # with open('从游方道士开始.txt','a',encoding='utf-8') as f:
        #     f.write(pic_name)
        #     f.write('\n')
        #     f.write(''.join(book_txt_lists))
        #     f.write('\n')


       
    


if __name__ == "__main__":
    main()

