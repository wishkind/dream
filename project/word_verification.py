from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
from io import BytesIO
from PIL import Image
import re
from project.chaojiying import CHAOJiYINGClient


class WordClick:

    def __init__(self, cookie):
        self.url = 'https://ehire.51job.com/Candidate/ResumeViewFolderV2.aspx?hidSeqID=12592228820&hidFolder=EMP&pageCode=24'
        self.cookie = cookie
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 20)
        self.client = CHAOJiYINGClient()

    def start(self):
        """
        打开网页，传递cookie访问
        :return:
        """
        # 打开网页
        self.driver.get(self.url)
        # 最大化
        self.driver.maximize_window()
        # 将传进来的cookie转成多个字典传入driver中
        cookies = self.cookie.split(';')
        self.input_cookie(cookies)
        # 再次打开网页，获取带有验证码网页
        self.driver.get(self.url)
        time.sleep(2)
        # 进行识别
        self.recognize()

    def input_cookie(self, cookies):
        """
        driver添加cookie
        :param:cookies
        :return:
        """
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

    def recognize(self):
        """
        获取图片，进行验证
        :return:
        """
        # 刷新验证码
        self.driver.find_element_by_xpath("//*[@id='btnVRefresh']").click()
        # 获取带文字的图片
        self.get_cut_img('full_word_img.png', 'yz-main')
        # 大图
        # self.get_cut_img('big_word_img.png', 'yz-pic-wrap')
        # 小图
        # self.get_cut_img('small_word_img.png', 'yz-pic-swrap')
        # 获取文字坐标列表
        all_position_list, pic_id = self.get_word_position()
        # 点击文字
        self.click_word(all_position_list)
        # 点击验证
        self.click_verify()
        time.sleep(2)
        # 关闭浏览器
        self.driver.close()

    def get_position(self, xpath):
        """
        获取验证码的位置
        :return: 验证码位置元祖
        """
        img = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, xpath)))
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

    def getfile(self, filepath):
        """
        读取文件
        :param filepath: 文件路径名称
        :return:bytes对象
        """
        with open(filepath, 'rb') as f:
            return f.read()

    def get_word_position(self):
        """
        获取文字的坐标
        :return: 一个列表 里面包括多个文字坐标元组
        """
        img = self.getfile('full_word_img.png')
        result = self.client.post_pic(img, 9004)
        pic_id = result['pic_id']
        if result['err_no'] == 0:
            pic_str = result['pic_str']
            position_str = pic_str.split('|')
            all_position_list = [[int(number) for number in group.split(',')] for group in position_str]
            print(all_position_list)
            self.client.report_error(pic_id)    #　目前账户余额410题分，每次消耗４０题分，运行这里不消耗超级鹰的题分，最好注释掉，避免账号被封
            return all_position_list, pic_id
        else:
            self.client.report_error(pic_id)
            return

    def click_word(self, all_position_list):
        """
        按照坐标依次点击文字
        :param all_position_list:
        :return:
        """
        element = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='yz-main']")))
        for position in all_position_list:
            ActionChains(self.driver).move_to_element_with_offset(element, position[0], position[1]).click().perform()
            print('点击一个文字 坐标{}'.format({position[0], position[1]}))
            time.sleep(2)

    def click_verify(self):
        """
        点击验证按钮
        :return:
        """
        self.driver.find_element_by_id('btnValidate').click()

    def get_cookie(self):
        """
        获取cookie
        :return:
        """
        cookie = self.driver.get_cookies()
        time.sleep(5)
        for i in cookie:
            self.driver.add_cookie(i)
        self.driver.get('https://ehire.51job.com/InboxResume/InboxRecentEngine.aspx?Style=1')
        time.sleep(5)
        cookies = self.driver.get_cookies()
        str_cookie = ''
        for j in cookies:
            name = j['name']
            value = j['value']
            str_cookie = str_cookie + name + '=' + value + ';'
        # 关闭浏览器
        self.driver.close()
        return str_cookie


if __name__ == '__main__':
    cookie = 'EhireGuid=22ef6943816348e2927ee41b0d427269;HRUSERINFO=CtmID=4371481&DBID=1&MType=02&HRUID=5809286&UserAUTHORITY=1111111111&IsCtmLevle=1&UserName=%e4%b8%8a%e6%b5%b7%e4%b8%b0%e8%8d%89%e6%96%87%e5%8c%96%e4%bc%a0%e6%92%ad%e6%9c%89%e9%99%90%e5%85%ac%e5%8f%b8&IsStandard=0&LoginTime=09%2f26%2f2019+08%3a47%3a04&ExpireTime=09%2f26%2f2019+08%3a57%3a04&CtmAuthen=0000011000000001000110010000000011100001&BIsAgreed=true&IsResetPwd=0&CtmLiscense=1&AccessKey=2866dcf515f92b2a&source=0;ASP.NET_SessionId=txraf2lkq4hw0tldhkmevs5h;LangType=Lang=&Flag=1;AccessKey=f1995dba0f2b4b3;KWD=EMP=;'
    w = WordClick(cookie)
    w.start()


