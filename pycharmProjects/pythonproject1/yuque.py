from selenium import webdriver
import time
import pyautogui
import pickle
pyautogui.PAUSE = 0.5


class zang():
    def __init__(self):
        self.driver = webdriver.Edge('msedgedriver.exe')

        self.driver.maximize_window()
        self.driver.get('https://sheyue.yuque.com/')
        #assert "深入" in self.driver.title
        time.sleep(1)

    def login(self, username, password):
        coords = pyautogui.locateOnScreen(r'E:\\PYTHON\\pycharmProjects\\img\\1.png')
        x, y = pyautogui.center(coords)
        pyautogui.leftClick(x, y)
        time.sleep(0.5)
        self.driver.find_element_by_xpath(
            '//*[@id="ReactApp"]/div/div[2]/div/div/div/div/div/div[2]/div/form/div[1]/div/div/span/div/span/input'
        ).send_keys(username)
        self.driver.find_element_by_xpath('//*[@id="password"]').send_keys(
            password)
        self.driver.find_element_by_xpath(
            '//*[@id="ReactApp"]/div/div[2]/div/div/div/div/div/div[2]/div/div[1]/label/span[1]/input'
        ).click()
        self.driver.find_element_by_xpath(
            '//*[@id="ReactApp"]/div/div[2]/div/div/div/div/div/div[2]/div/form/div[3]/div/div/span/button'
        ).click()
        
        time.sleep(1)
if __name__ == '__main__':
    username = '13343034001'
    password = 'Ma@#19940205'
    zang = zang()
    zang.login(username, password)
    time.sleep(500)

