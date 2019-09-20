from selenium import webdriver
from io import BytesIO
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
from PIL import Image
from project.spider import Spider


class Verification:

    def __init__(self):
        self.url = 'https://ehire.51job.com/'
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 20)

    def start(self):
        # 打开网页
        self.driver.get(self.url)
        # 最大化
        # self.driver.maximize_window()
        time.sleep(2)
        # 获取第一个输入框，输入会员名
        input_member_name = self.driver.find_element_by_id('txtMemberNameCN').send_keys('上海丰草')
        # 获取第二个输入框，输入用户名
        input_user_name = self.driver.find_element_by_id('txtUserNameCN').send_keys('上海丰草文化传播有限公司')
        # h获取第三个输入框，输入密码
        input_password = self.driver.find_element_by_id('txtPasswordCN').send_keys('denglimin11')
        # 点击登录
        login_button = self.driver.find_element_by_id('Login_btnLoginCN').click()

        # self.get_cookie()

        # todo 验证码
        # self.get_position()

        # self.get_screen_image()
        slider = self.get_slider()
        slider.click()

    def get_position(self):
        """
        获取验证码位置
        :return: 验证码位置元组
        """
        img = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_canvas_img')))
        location = img.location
        size = img.size
        top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size['width']
        print('验证码位置：', top, bottom, left, right)
        return top, bottom, left, right

    def get_img(self, name='capthcha.png'):
        """
        获取验证码图片
        :return: 图片对象
        """
        top, bottom, left, right = self.get_position()
        screen_image = self.get_screen_image()
        # 裁剪验证码
        capthcha = screen_image.crop((left, top, right, bottom))
        # 保存
        capthcha.save(name)
        return capthcha

    def get_screen_image(self):
        """
        获取网页截图
        :return: 截图对象
        """
        screen_img = self.driver.get_screenshot_as_png()
        screen_img = Image.open(BytesIO(screen_img))
        return screen_img

    def get_slider(self):
        """
        获取滑块
        :return: 滑块对象
        """
        slider = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_slider_button')))
        return slider

    def get_cookie(self):
        cookie = self.driver.get_cookies()
        print(cookie)
        for i in cookie:
            self.driver.add_cookie(i)
        self.driver.get('https://ehire.51job.com/InboxResume/InboxRecentEngine.aspx?Style=1')

        cookies = self.driver.get_cookies()
        print(cookies)
        str_cookie = ''
        for j in cookies:
            name = j['name']
            value = j['value']
            str_cookie = str_cookie + name + '=' + value + ';'
        print(str_cookie)
        # todo 将cookie传入爬虫代码
        s = Spider(str_cookie)
        s.start_crawler()


if __name__ == '__main__':
    v = Verification()
    v.start()