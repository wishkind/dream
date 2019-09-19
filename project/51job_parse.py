import requests
from lxml import etree
import re
import time
from lib.log import LogHandler
from lib.proxy_iterator import Proxies
p = Proxies()
p = p.get_one(proxies_number=1)
log = LogHandler(__name__)


class Parse:

    def __init__(self):

        self.headers = {
            'Connection': 'keep-alive',
            'Host': 'ehire.51job.com',
            'Referer': 'https://ehire.51job.com/Navigate.aspx?ShowTips=11&PwdComplexity=N',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
            # 这里要传进去
            'Cookie': 'EhireGuid=b316ed37653449729b260b8351e0ab02; adv=adsnew%3D1%26%7C%26adsresume%3D1%26%7C%26adsfrom%3Dhttps%253A%252F%252Fsp0.baidu.com%252F9q9JcDHa2gU2pMbgoY3K%252Fadrc.php%253Ft%253D06KL00c00fDewkY0KKG-00uiAs0k43FI000007jzr-C00000xDd5wZ.THYdnyGEm6K85yF9pywd0ZnquW0Luhfznycsnj0snvc3msKd5RPjfRnYP1m3PHNKwbD1rHu7PHT3wj-awjFDrHDkfW7D0ADqI1YhUyPGujY1nWT4njbsPHTdFMKzUvwGujYkP6K-5y9YIZK1rBtEIZF9mvR8PH7JUvc8mvqVQLwzmyP-QMKCTjq9uZP8IyYqnW0sPjc3nBu9pM0qmR9inAPcHHunXH-YmHPwIR4RwM7Bnb-dyHc4IDs1Rh4nnY4_m-n4IvN_rZ-PwDRYHAdCnAFgIzqpUbGvm-fkpN-gUAVbyDcvFh_qn1u-njRYmyDsPjR4m1F-uAfdmWfLuWRLmvcvnHKbrjc0mLFW5Hn1n1T3%2526tpl%253Dtpl_11534_19968_16032%2526l%253D1513812560%2526attach%253Dlocation%25253D%252526linkName%25253D%252525E6%252525A0%25252587%252525E5%25252587%25252586%252525E5%252525A4%252525B4%252525E9%25252583%252525A8-%252525E6%252525A0%25252587%252525E9%252525A2%25252598-%252525E4%252525B8%252525BB%252525E6%252525A0%25252587%252525E9%252525A2%25252598%252526linkText%25253D%252525E3%25252580%25252590%252525E5%25252589%2525258D%252525E7%252525A8%2525258B%252525E6%25252597%252525A0%252525E5%252525BF%252525A751Job%252525E3%25252580%25252591-%25252520%252525E5%252525A5%252525BD%252525E5%252525B7%252525A5%252525E4%252525BD%2525259C%252525E5%252525B0%252525BD%252525E5%2525259C%252525A8%252525E5%25252589%2525258D%252525E7%252525A8%2525258B%252525E6%25252597%252525A0%252525E5%252525BF%252525A7%2521%252526xp%25253Did%2528%25252522m3279090575_canvas%25252522%2529%2525252FDIV%2525255B1%2525255D%2525252FDIV%2525255B1%2525255D%2525252FDIV%2525255B1%2525255D%2525252FDIV%2525255B1%2525255D%2525252FDIV%2525255B1%2525255D%2525252FH2%2525255B1%2525255D%2525252FA%2525255B1%2525255D%252526linkType%25253D%252526checksum%25253D220%2526ie%253DUTF-8%2526f%253D8%2526tn%253Dbaidu%2526wd%253D51job%2526rqlang%253Dcn%26%7C%26adsnum%3D2004282; guid=2c4e9db35cd1346f1505a5a52ae7085a; LangType=Lang=&Flag=1; RememberLoginInfo=member_name=42C0E5A4273247A0CA6AD9118CC10153&user_name=42C0E5A4273247A0BE39E05CE3F038B97F346A4FD26D49881290FBC4487FA1C3; ASP.NET_SessionId=jujao1b4umm1lq3qikbjflx1; AccessKey=87589d62af294ca; HRUSERINFO=CtmID=4371481&DBID=1&MType=02&HRUID=5809286&UserAUTHORITY=1111111111&IsCtmLevle=1&UserName=%e4%b8%8a%e6%b5%b7%e4%b8%b0%e8%8d%89%e6%96%87%e5%8c%96%e4%bc%a0%e6%92%ad%e6%9c%89%e9%99%90%e5%85%ac%e5%8f%b8&IsStandard=0&LoginTime=09%2f19%2f2019+17%3a07%3a12&ExpireTime=09%2f19%2f2019+17%3a17%3a12&CtmAuthen=0000011000000001000110010000000011100001&BIsAgreed=true&IsResetPwd=0&CtmLiscense=1&AccessKey=cf5e5d616f0b9d21&source=0; KWD=EMP=',
        }

    def start_crawler(self, url, user_id):
        params = {
            'hidSeqID': user_id,
            'hidFolder': 'EMP',
            'pageCode': 24
        }
        r = requests.get(url=url, headers=self.headers, params=params)
        print(r.text)
        tree = etree.HTML(r.text)
        name = tree.xpath("//*[@id='tdseekname']/text()")[0]
        print(name)


if __name__ == '__main__':
    p = Parse()
    p.start_crawler('https://ehire.51job.com/Candidate/ResumeViewFolderV2.aspx', '12569346824')



