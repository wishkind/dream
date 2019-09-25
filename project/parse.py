import requests
from lxml import etree
import re
import pandas as pd
import time
from project.word_verification import WordClick
from lib.log import LogHandler
log = LogHandler(__name__)


class Parse:

    def __init__(self, cookie):

        self.headers = {
            'Connection': 'keep-alive',
            'Host': 'ehire.51job.com',
            'Referer': 'https://ehire.51job.com/Navigate.aspx?ShowTips=11&PwdComplexity=N',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
            'Cookie': cookie
        }
        self.cookie = cookie

    def start(self, url, user_id):
        params = {
            'hidSeqID': user_id,
            'hidFolder': 'EMP',
            'pageCode': 24
        }
        try:
            r = requests.get(url=url, headers=self.headers, params=params)
        except Exception:
            return
        tree = etree.HTML(r.text)
        # 姓名
        name = tree.xpath("//*[@id='tdseekname']")
        if len(name) > 0:
            name = tree.xpath("//*[@id='tdseekname']/text()")[0]
            name = ''.join(name.split())
        elif '此人为恶意投递，简历屏蔽中' in r.text:
            print('此页失效')
            return
        else:
            print('有文字验证码')
            # todo 验证后继续抓取  ???
            # w = WordClick(self.cookie)
            # new_cookie = w.start()
            # s = Parse(new_cookie)
            # s.start(url, user_id)

        # 应聘职位
        position_applied = tree.xpath("//*[@id='hidPositionName']/@value")[0]
        # 投递时间
        time_applied = tree.xpath("//*[@id='hidPutDate']/@value")[0]
        # 应聘公司
        company_applied = tree.xpath("//*[@id='hidCompanyName']/@value")[0]
        # 匹配度
        match_value = tree.xpath("//*[@id='hidMatchValue']/@value")[0]
        # 工作状态
        status = tree.xpath("//table[@class='infr']/tr[2]/td[1]/table[1]/tr[1]/td[2]/text()")[0]
        status = ''.join(status.split())
        # 电话
        phone = tree.xpath("//table[@class='infr']/tr[2]/td[1]/table[1]/tr[1]/td[4]/text()")[0]
        # 邮箱
        email = tree.xpath("//table[@class='infr']/tr[2]/td[1]/table[1]/tr[1]/td[6]/div[1]/a[1]")
        if len(email) > 0:
            email = tree.xpath("//table[@class='infr']/tr[2]/td[1]/table[1]/tr[1]/td[6]/div[1]/a[1]/text()")[0]
        else:
            email = ''

        gender_info = tree.xpath("//table[@class='infr']/tr[3]/td[1]")
        if len(gender_info) > 0:
            gender_info = tree.xpath("//table[@class='infr']/tr[3]/td[1]")[0]
            gender_info = gender_info.xpath('string(.)')
            gender_info = ''.join(gender_info.split())
            # 性别
            gender = gender_info.split('|')[0]
            # 年龄
            age_info = gender_info.split('|')[1]
            age = re.search('(\d+岁)', age_info, re.S | re.M).group(1)
            # 出生年月
            date_of_birth = re.search('(\d+年\d+月\d+日)', age_info, re.S | re.M).group(1)
            # 现居住地
            residence = gender_info.split('|')[2]
            # 工作经验
            experience = gender_info.split('|')[3]
        else:
            gender = ''
            age = ''
            date_of_birth = ''
            residence = ''
            experience = ''

        # 一级分类 最近工作
        recently_work = tree.xpath("//table[@class='box2']/tr[1]/td[1]/table[1]/tr[1]/td[1]/table[1]/tbody/tr[1]/td[1]")
        if len(recently_work) > 0:
            recently_work = tree.xpath("//table[@class='box2']/tr[1]/td[1]/table[1]/tr[1]/td[1]/table[1]/tbody/tr[1]/td[1]/text()")[0]
            recently_work = ''.join(recently_work.split())
            # 最近工作时间
            recently_work_time = tree.xpath("//table[@class='box2']/tr[1]/td[1]/table[1]/tr[1]/td[1]/table[1]/tbody/tr[1]/td[1]/span[1]/text()")[0]
            recently_work_time = ''.join(recently_work_time.split()).replace('（', '').replace(')', '')
            # 二级分类 最近职位
            position = tree.xpath("//table[@class='box2']/tr[1]/td[1]/table[1]/tr[1]/td[1]/table[1]/tbody/tr[2]/td[1]/text()")[0]
            position = position.replace('\u3000', '')
            recently_position = tree.xpath("//table[@class='box2']/tr[1]/td[1]/table[1]/tr[1]/td[1]/table[1]/tbody/tr[2]/td[2]/text()")[0]
            # 最近公司
            company = tree.xpath("//table[@class='box2']/tr[1]/td[1]/table[1]/tr[1]/td[1]/table[1]/tbody/tr[3]/td[1]/text()")[0]
            company = company.replace('\u3000', '')
            recently_company = tree.xpath("//table[@class='box2']/tr[1]/td[1]/table[1]/tr[1]/td[1]/table[1]/tbody/tr[3]/td[2]/text()")[0]
            # 行业
            industry = tree.xpath("//table[@class='box2']/tr[1]/td[1]/table[1]/tr[1]/td[1]/table[1]/tbody/tr[4]/td[1]/text()")[0]
            industry = industry.replace('\u3000', '')
            industry_info = tree.xpath("//table[@class='box2']/tr[1]/td[1]/table[1]/tr[1]/td[1]/table[1]/tbody/tr[4]/td[2]/text()")[0]
        else:
            recently_work = ''
            recently_work_time = ''
            position = ''
            recently_position = ''
            company = ''
            recently_company = ''
            industry = ''
            industry_info = ''

        # 一级分类 最高学历/学位
        highest_education = tree.xpath("//table[@class='box2']/tr[1]/td[1]/table[1]/tr[1]/td[2]/table[1]/tr[1]/td[1]")
        if len(highest_education) > 0:
            highest_education = tree.xpath("//table[@class='box2']/tr[1]/td[1]/table[1]/tr[1]/td[2]/table[1]/tr[1]/td[1]/text()")[0]
            highest_education = ''.join(highest_education.split())
            # 二级分类
            major = tree.xpath("//table[@class='box2']/tr[1]/td[1]/table[1]/tr[1]/td[2]/table[1]/tr[2]/td[1]/text()")[0]
            major = major.replace('\u3000', '')
            major_info = tree.xpath("//table[@class='box2']/tr[1]/td[1]/table[1]/tr[1]/td[2]/table[1]/tr[2]/td[2]/text()")[0]
            major_info = ''.join(major_info.split())
            # 学校
            school = tree.xpath("//table[@class='box2']/tr[1]/td[1]/table[1]/tr[1]/td[2]/table[1]/tr[3]/td[1]/text()")[0]
            school = school.replace('\u3000', '')
            school_info = tree.xpath("//table[@class='box2']/tr[1]/td[1]/table[1]/tr[1]/td[2]/table[1]/tr[3]/td[2]/text()")[0]
            # 学位
            degree = tree.xpath("//table[@class='box2']/tr[1]/td[1]/table[1]/tr[1]/td[2]/table[1]/tr[4]/td[1]/text()")[0]
            degree_info = tree.xpath("//table[@class='box2']/tr[1]/td[1]/table[1]/tr[1]/td[2]/table[1]/tr[4]/td[2]/text()")[0]
        else:
            highest_education = ''
            major = ''
            major_info = ''
            school = ''
            school_info = ''
            degree = ''
            degree_info = ''

        data = {
            '姓名': name,
            '应聘职位': position_applied,
            '投递时间': time_applied,
            '应聘公司': company_applied,
            '匹配度': match_value,
            '工作状态': status,
            '电话': phone,
            '邮箱': email,
            '性别': gender,
            '年龄': age,
            '出生年月': date_of_birth,
            '现居住地': residence,
            '工作经验': experience,
            recently_work: {
                recently_work: recently_work_time,
                position: recently_position,
                company: recently_company,
                industry: industry_info
            },
            highest_education: {
                major: major_info,
                school: school_info,
                degree: degree_info
            }
        }

        more_info = tree.xpath("//tr[@id='divInfo']/td[1]/table")
        for info in more_info:
            # 一级分类
            one_level_info_name = info.xpath(".//tr[1]/td[@class='plate1']")
            if len(one_level_info_name) > 0:
                one_level_info_name = info.xpath(".//tr[1]/td[@class='plate1']/text()")[0]
                one_level_info_name = ''.join(one_level_info_name.split())
                one_level_info = info.xpath(".//tr[1]/td[@class='plate1']/span[1]")
                if len(one_level_info) > 0:
                    one_level_info = info.xpath(".//tr[1]/td[@class='plate1']/span[1]/text()")
                    if len(one_level_info) > 0:
                        one_level_info = info.xpath(".//tr[1]/td[@class='plate1']/span[1]/text()")[0]
                        one_level_info = ''.join(one_level_info.split())
                    else:
                        one_level_info = ''
                else:
                    one_level_info = ''
                one_level_info_name_dict = {
                    one_level_info_name: one_level_info
                }
                # 二级分类
                # 个人信息
                two_level_info_a = info.xpath("./tbody/tr[2]/td[1]/table[1]/tbody/tr/td/table[1]/tbody[1]/tr")
                # 求职意向
                two_level_info_b = info.xpath("./tr[2]/td[1]/table[1]/tr/td/table[1]/tbody[1]/tr")
                # 项目经验
                two_level_info_c = info.xpath("./tr[2]/td[1]/table[1]/tr/td/table/tr")
                # 教育经历
                two_level_info_d = info.xpath("./tbody/tr[2]/td[1]/table[1]/tbody/tr/td/table[1]/tr")
                # 技能特长
                two_level_info_e = info.xpath("./tr[2]/td[1]/table[1]/tbody/tr/td/table/tr")

                if len(two_level_info_a) > 0:
                    one_level_info_name_dict = self.get_more_info(two_level_info_a, one_level_info_name_dict)
                elif len(two_level_info_b) > 0:
                    one_level_info_name_dict = self.get_more_info(two_level_info_b, one_level_info_name_dict)
                elif len(two_level_info_c) > 0:
                    one_level_info_name_dict = self.get_more_info(two_level_info_c, one_level_info_name_dict)
                elif len(two_level_info_d) > 0:
                    one_level_info_name_dict = self.get_more_info(two_level_info_d, one_level_info_name_dict)
                elif len(two_level_info_e) > 0:
                    one_level_info_name_dict = self.get_more_info(two_level_info_e, one_level_info_name_dict)

                data.update({
                    one_level_info_name: one_level_info_name_dict
                })
        # df = pd.DataFrame(data=[data])
        # df.to_csv("./test.csv", encoding='utf-8-sig', header=False, index=False)
        log.info(data)

    @staticmethod
    def get_more_info(two_level_info, one_level_info_name_dict):
        for i in two_level_info:
            two_level_info_name = i.xpath('./td[1]')
            if len(two_level_info_name) > 0:
                two_level_info_name = two_level_info_name[0].xpath('string(.)')
                two_level_info_name = ''.join(two_level_info_name.split())
            else:
                two_level_info_name = ''
            two_level_info_status = i.xpath('./td[2]')
            if len(two_level_info_status) > 0:
                two_level_info_status = two_level_info_status[0].xpath('string(.)')
                two_level_info_status = ''.join(two_level_info_status.split())
            else:
                two_level_info_status = ''
            one_level_info_name_dict.update({
                two_level_info_name: two_level_info_status
            })
        return one_level_info_name_dict


if __name__ == '__main__':
    p = Parse('guid=fa1f7d11e1e6c06f95cf8c6fcc300d52; EhireGuid=ef2f1a33bfbd47cbaf3a5f5dd2d8eaa8; LangType=Lang=&Flag=1; RememberLoginInfo=member_name=42C0E5A4273247A0CA6AD9118CC10153&user_name=42C0E5A4273247A0BE39E05CE3F038B97F346A4FD26D49881290FBC4487FA1C3; adv=adsnew%3D0%26%7C%26adsresume%3D1%26%7C%26adsfrom%3Dhttps%253A%252F%252Fsp0.baidu.com%252F9q9JcDHa2gU2pMbgoY3K%252Fadrc.php%253Ft%253D06KL00c00fDewkY0KKG-00uiAsjdy3wI000007jzr-C00000xDd5wZ.THYdnyGEm6K85yF9pywd0ZnqujmvuymsuAnsnj7bmhRsP6Kd5RDzfWm3fRPAnWTzPDndnbDvnRNjfYcLPYR4fWuAfb7A0ADqI1YhUyPGujY1nWT4njbsPHTdFMKzUvwGujYkP6K-5y9YIZK1rBtEIZF9mvR8PH7JUvc8mvqVQLwzmyP-QMKCTjq9uZP8IyYqnW0sPjc3nBu9pM0qmR9inAPcHHunXH-YmHPwIR4RwM7Bnb-dyHc4IDs1Rh4nnY4_m-n4IvN_rZ-PwDRYHAdCnAFgIzqpUbGvm-fkpN-gUAVbyDcvFh_qn1u-njRYmyDsPjR4m1F-uAfdmWfLuWRLmvcvnHKbrjc0mLFW5HnsP1f4%2526tpl%253Dtpl_11534_19968_16032%2526l%253D1513812560%2526attach%253Dlocation%25253D%252526linkName%25253D%252525E6%252525A0%25252587%252525E5%25252587%25252586%252525E5%252525A4%252525B4%252525E9%25252583%252525A8-%252525E6%252525A0%25252587%252525E9%252525A2%25252598-%252525E4%252525B8%252525BB%252525E6%252525A0%25252587%252525E9%252525A2%25252598%252526linkText%25253D%252525E3%25252580%25252590%252525E5%25252589%2525258D%252525E7%252525A8%2525258B%252525E6%25252597%252525A0%252525E5%252525BF%252525A751Job%252525E3%25252580%25252591-%25252520%252525E5%252525A5%252525BD%252525E5%252525B7%252525A5%252525E4%252525BD%2525259C%252525E5%252525B0%252525BD%252525E5%2525259C%252525A8%252525E5%25252589%2525258D%252525E7%252525A8%2525258B%252525E6%25252597%252525A0%252525E5%252525BF%252525A7%2521%252526xp%25253Did%2528%25252522m3279090575_canvas%25252522%2529%2525252FDIV%2525255B1%2525255D%2525252FDIV%2525255B1%2525255D%2525252FDIV%2525255B1%2525255D%2525252FDIV%2525255B1%2525255D%2525252FDIV%2525255B1%2525255D%2525252FH2%2525255B1%2525255D%2525252FA%2525255B1%2525255D%252526linkType%25253D%252526checksum%25253D220%2526ie%253DUTF-8%2526f%253D8%2526tn%253Dbaidu%2526wd%253D51job%2526rqlang%253Dcn%26%7C%26adsnum%3D2004282; ASP.NET_SessionId=1gxli4twp5m20n0q3t4taalk; AccessKey=09b0d4961f3146d; HRUSERINFO=CtmID=4371481&DBID=1&MType=02&HRUID=5809286&UserAUTHORITY=1111111111&IsCtmLevle=1&UserName=%e4%b8%8a%e6%b5%b7%e4%b8%b0%e8%8d%89%e6%96%87%e5%8c%96%e4%bc%a0%e6%92%ad%e6%9c%89%e9%99%90%e5%85%ac%e5%8f%b8&IsStandard=0&LoginTime=09%2f24%2f2019+12%3a31%3a28&ExpireTime=09%2f24%2f2019+12%3a41%3a28&CtmAuthen=0000011000000001000110010000000011100001&BIsAgreed=true&IsResetPwd=0&CtmLiscense=1&AccessKey=c3e7f69956b5e772&source=0; KWD=EMP=')
    p.start('https://ehire.51job.com/Candidate/ResumeViewFolderV2.aspx', '12586591446')



