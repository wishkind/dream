from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import base64
import random
from PIL import Image
from project.spider import Spider


class Verification:

    def __init__(self):
        self.url = 'https://ehire.51job.com/'
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 20)

    def start(self):
        """
        启动
        :return:
        """
        # 打开网页
        self.driver.get(self.url)
        # 最大化
        self.driver.maximize_window()
        time.sleep(2)
        # 获取第一个输入框，输入会员名
        self.driver.find_element_by_id('txtMemberNameCN').send_keys('上海丰草')
        # 获取第二个输入框，输入用户名
        self.driver.find_element_by_id('txtUserNameCN').send_keys('上海丰草文化传播有限公司')
        # 获取第三个输入框，输入密码
        self.driver.find_element_by_id('txtPasswordCN').send_keys('denglimin11')
        # 点击登录
        self.driver.find_element_by_id('Login_btnLoginCN').click()
        time.sleep(5)
        self.move()

    def move(self):
        # 刷新一下验证码
        self.driver.find_element_by_xpath('//a[@class="geetest_refresh_1"]').click()
        time.sleep(1)
        # 保存有缺口的图片
        self.save_img('cut.png', 'geetest_canvas_bg')
        # 保存没有缺口的图片
        self.save_img('full.png', 'geetest_canvas_fullbg')
        cut_img = Image.open('cut.png')
        full_img = Image.open('full.png')
        # 计算距离 需要减去距离左边的间隙
        distance = self.get_distance(cut_img, full_img) - random.randint(6, 9)
        # 开始移动
        self.drag(distance)

        # 判断是否验证成功
        try:
            self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="geetest_slider geetest_success"]')))
            print('验证成功')
        except TimeoutException:
            print('再试一次')
            time.sleep(5)
            try:
                self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="geetest_panel_error_content"]'))).click()
                time.sleep(5)
                self.move()
            except TimeoutException:
                self.move()

        # 获取cookie
        self.get_cookie()

    def save_img(self, img_name, class_name):
        """
        获取验证码图片
        :param img_name: 图片名称
        :param class_name: xpath选择器
        :return:
        """
        # 执行js 获取网页上的base64编码图片，解码成bytes类型后保存图片
        getImgJS = 'return document.getElementsByClassName("' + class_name + '")[0].toDataURL("image/png");'
        img = self.driver.execute_script(getImgJS)
        base64_data_img = img[img.find(',') + 1:]
        image_base = base64.b64decode(base64_data_img)
        file = open(img_name, 'wb')
        file.write(image_base)
        file.close()

    def get_distance(self, cut_img, full_img):
        """
        计算缺口距离
        :param cut_img: 有缺口的图片
        :param full_img: 无缺口的图片
        :return: 缺口距离
        """
        for x in range(cut_img.width):
            for y in range(cut_img.height):
                cpx = cut_img.getpixel((x, y))
                fpx = full_img.getpixel((x, y))
                if not self.is_similar_color(cpx, fpx):
                    img = cut_img.crop((x, y, x + 50, y + 50))
                    img.save('gap.png')
                    return x

    @staticmethod
    def is_similar_color(x_pixel, y_pixel):
        """
        判断两张图片的像素是否相同
        :param x_pixel: 有缺口的图片像素元组
        :param y_pixel: 无缺口的图片像素元组
        :return: True or False
        """
        for i, pixel in enumerate(x_pixel):
            if abs(y_pixel[i] - pixel) > 50:
                return False
        return True

    def get_slider(self):
        """
        获取滑块
        :return: 滑块对象
        """
        slider = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_slider_button')))
        return slider

    def drag(self, distance):
        """
        开始移动
        :param distance: 缺口距离
        :return:
        """
        # 获取滑块
        slider = self.get_slider()
        # 按下鼠标左键
        ActionChains(self.driver).click_and_hold(slider).perform()
        time.sleep(1)
        while distance > 0:
            if distance > 10:
                span = random.randint(5, 8)
            else:
                span = random.randint(2, 3)
            ActionChains(self.driver).move_by_offset(span, 0).perform()
            distance -= span
            time.sleep(random.randint(10, 50) / 100)
        ActionChains(self.driver).move_by_offset(distance, 1).perform()
        # 释放鼠标
        ActionChains(self.driver).release(on_element=slider).perform()

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
        print(str_cookie)
        # 关闭浏览器
        self.driver.close()
        # 将cookie传入爬虫代码
        # s = Spider(str_cookie)
        # s.start()


if __name__ == '__main__':
    v = Verification()
    v.start()
