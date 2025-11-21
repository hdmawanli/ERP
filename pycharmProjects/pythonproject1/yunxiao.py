import time
import pandas
from selenium import webdriver


web = 'https://yunxiao.sjgjj.cn/task/644524'
co = open('E:\PYTHON\pycharmProjects\cookie\cookie.txt', 'r')
cook = co.read()


def get_excel():
    # 读取excel
    get_excels = pandas.read_excel('E:\工作空间\月度工作计划、总结\马万里工作日志 (自动保存的).xlsx',
                                   '工作日志')
    data = get_excels.values.tolist()
    get_excel_data = data[-1][1]        #获取data第二列最后一行数据
    return get_excel_data


def login():
    driver = webdriver.Edge('msedgedriver.exe')
    driver.maximize_window()
    #driver.add_cookie(cookie_dict=cookie_dict)
    driver.get(url=web)
    driver.delete_all_cookies()
    for i in cook.split('; '):
        cookie = {'name': i.split('=')[0], 'value': i.split('=')[1]}
        driver.add_cookie(cookie)
    time.sleep(1)
    driver.get(url=web)
    #assert "研究数据展示工具" in self.driver.title
    time.sleep(10)
    return driver


def dowork():
    driver = login()
    gongshi = driver.find_element_by_xpath(
        '//*[@id="issue-form"]/div[2]/div[2]/div/div[6]/div[2]/div/input'
    ).get_attribute("value")
    xiang = driver.find_element_by_xpath(
        '//*[@id="issue-form"]/div[2]/div[2]/div/div[6]/div[4]/div/input'
    ).get_attribute("value")
    time.sleep(2)
    gongshi = int(gongshi) + 11
    xiang = xiang.replace('计划】', '总结】')
    xiang = xiang + get_excel()
    driver.find_element_by_xpath(
        '//*[@id="issue-form"]/div[2]/div[2]/div/div[6]/div[2]/div/input'
    ).clear()
    driver.find_element_by_xpath(
        '//*[@id="issue-form"]/div[2]/div[2]/div/div[6]/div[4]/div/input'
    ).clear()
    time.sleep(2)
    gongshi = driver.find_element_by_xpath(
        '//*[@id="issue-form"]/div[2]/div[2]/div/div[6]/div[2]/div/input'
    ).send_keys(gongshi)
    xiang = driver.find_element_by_xpath(
        '//*[@id="issue-form"]/div[2]/div[2]/div/div[6]/div[4]/div/input'
    ).send_keys(xiang)
    time.sleep(100)


if __name__ == "__main__":

    dowork()
    time.sleep(1000)