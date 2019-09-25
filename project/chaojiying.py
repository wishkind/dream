#!/usr/bin/env python
# coding:utf-8

import requests
from hashlib import md5


class CHAOJiYINGClient(object):

    def __init__(self,):
        self.username = 'zjx15996163721'
        self.password = 'qwer1234'.encode('utf8')
        self.password = md5(self.password).hexdigest()
        self.soft_id = '901654'
        self.base_params = {
            'user': self.username,
            'pass2': self.password,
            'softid': self.soft_id,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
        }

    def post_pic(self, img, codetype):
        """
        im: 图片字节
        codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        """
        params = {
            'codetype': codetype,
        }
        params.update(self.base_params)
        # userfile=图片文件二进制流(或是称之为内存流,文件流,字节流的概念)
        # file_base64=图片文件base64字符串
        files = {'userfile': ('ccc.jpg', img)}
        r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, files=files, headers=self.headers)
        return r.json()

    def report_error(self, im_id):
        """
        im_id:报错题目的图片ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://upload.chaojiying.net/Upload/ReportError.php', data=params, headers=self.headers)
        return r.json()


if __name__ == '__main__':
    # chaojiying = CHAOJiYINGClient()
    # img = open('full_word_img.png', 'rb').read()
    # print(chaojiying.post_pic(img, 9004))
    result = {'err_no': 0, 'err_str': 'OK', 'pic_id': '3081313513096000010', 'pic_str': '188,141|274,123|219,109|148,133', 'md5': '4ca80fc499734df48f54b1f15e2381da'}
    pic_id = result['pic_id']
    pic_str = result['pic_str']
    position_str = pic_str.split('|')
    all_position_list = [[int(number) for number in group.split(',')] for group in position_str]
    print(all_position_list)

"""
{'err_no': 0, 'err_str': 'OK', 'pic_id': '3081313513096000010', 'pic_str': '188,141|274,123|219,109|148,133', 'md5': '4ca80fc499734df48f54b1f15e2381da'}
(188,141)
(274,123)
(219,109)
(148,133)
"""

