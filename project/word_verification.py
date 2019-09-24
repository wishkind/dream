from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import base64
import random
from io import BytesIO
from PIL import Image
import re


class WordClick:

    def __init__(self, cookie):
        self.url = 'https://ehire.51job.com/Candidate/ResumeViewFolderV2.aspx?hidSeqID=12592228820&hidFolder=EMP&pageCode=24'
        self.cookie = cookie
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 20)

    def start(self):
        # 打开网页
        self.driver.get(self.url)
        # 最大化
        self.driver.maximize_window()
        # 将传进来的cookie转成多个字典传入driver中
        cookies = self.cookie.split(';')
        for i in cookies[:-1]:
            name = re.search('(.*?)=', i).group(1)
            value = i.split(name)[1][1:]
            cookie_dist = {
                'domain': 'ehire.51job.com',
                'httpOnly': True,
                'path': '/',
                'secure': True,
                'name': name,
                'value': value
            }
            # 添加cookie
            self.driver.add_cookie(cookie_dist)
        # 再次打开网页，获取带有验证码网页
        self.driver.get(self.url)
        time.sleep(2)
        self.save_img()

    def save_img(self):
        # 刷新验证码
        self.driver.find_element_by_xpath("//*[@id='btnVRefresh']").click()
        # 获取带文字的两张图片
        self.get_cut_img('big_word_img.png', 'divVImage')
        self.get_cut_img('small_word_img.png', 'divVPhrase')

    def get_position(self, xpath):
        """
        获取验证码的位置
        :return: 验证码位置元祖
        """
        img = self.wait.until(EC.presence_of_element_located((By.ID, xpath)))
        time.sleep(2)
        location = img.location
        size = img.size
        top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size['width']
        return top, bottom, left, right

    def get_screen_image(self):
        """
        获取网页截图
        :return: 截图对象
        """
        screen_img = self.driver.get_screenshot_as_png()
        screen_img = Image.open(BytesIO(screen_img))
        return screen_img

    def get_cut_img(self, name='word_cut.png', xpath='yz-pic-b'):
        """
        获取验证码图片
        :return: 图片对象,Image对象
        """
        top, bottom, left, right = self.get_position(xpath)
        print('验证码位置：', top, bottom, left, right)
        screen_img = self.get_screen_image()
        # 剪裁图片
        word_cut_img = screen_img.crop((left, top, right, bottom))
        word_cut_img.save(name)
        return word_cut_img


if __name__ == '__main__':
    cookie = 'EhireGuid=0ac534134836478fad24064c051c20a6;ASP.NET_SessionId=yvfcyhlxvljmrqqwb4i2hghj;LangType=Lang=&Flag=1;HRUSERINFO=CtmID=4371481&DBID=1&MType=02&HRUID=5809286&UserAUTHORITY=1111111111&IsCtmLevle=1&UserName=%e4%b8%8a%e6%b5%b7%e4%b8%b0%e8%8d%89%e6%96%87%e5%8c%96%e4%bc%a0%e6%92%ad%e6%9c%89%e9%99%90%e5%85%ac%e5%8f%b8&IsStandard=0&LoginTime=09%2f24%2f2019+16%3a41%3a53&ExpireTime=09%2f24%2f2019+16%3a51%3a53&CtmAuthen=0000011000000001000110010000000011100001&BIsAgreed=true&IsResetPwd=0&CtmLiscense=1&AccessKey=6623560edcf43de8&source=0;AccessKey=a2313acdcb7648d;KWD=EMP=;'
    w = WordClick(cookie)
    w.start()


