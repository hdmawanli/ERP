import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import time
lis = ''
page = 2
def main(pic_list_url,page):

    
    Myheaders = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.52'
                    
    }
    
    #req = requests.session()
    pic_list_html = requests.get(pic_list_url, headers = Myheaders)
    pic_list_html.encoding = 'gbk'
    
    soup = BeautifulSoup(pic_list_html.text,'lxml')
    pic_lists = soup.find('ul',{'class' : 'clearfix'})
    pic_lists =  pic_lists.find_all('li')

    x = 1
    for li in pic_lists:
        pic_url = 'https://pic.netbian.com/' + li.a.get('href')
        
        pic_html = requests.get(pic_url,headers = Myheaders)
        pic_html.encoding = 'gbk'
        
        sp = BeautifulSoup(pic_html.text,'lxml')
        names=str(sp.find('a',{'id':'img'}).img.get('title'))

        pic_download = 'https://pic.netbian.com/' + sp.find('a',{'id' : 'img'}).img.get('src')
        #获取返回的字节类型
        img = requests.get(pic_download, headers=Myheaders).content
        path = r'D:\\图片\\Saved Pictures\\' + names + ".jpg"
        
        with open(path, 'wb') as f:
                f.write(img)
                time.sleep(1)
                print("第【{}】页第【{}】张图片下载完成！".format(page,x))
                x += 1
        
    page += 1


if __name__ == "__main__":
    for page in tqdm(range(1,1)):
        if page == 1:
            pic_list_url = 'https://pic.netbian.com/' + lis + '/index'  + '.html'
            main(pic_list_url,page)
        else:
            pic_list_url = 'https://pic.netbian.com/' + lis + '/index_'  + str(page) + '.html'
            main(pic_list_url,page)


 