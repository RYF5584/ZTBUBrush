# coding: utf-8
# @Author: Ruan

import base64
import json
import re
import random
import string
import traceback

import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import urllib


class BrushClass:
    """
        51爱学教 云平台
        ZTBU刷课
    """

    def __init__(self, token: str):
        """
            传Token就行，开发者工具自己抓一下就可以，不想写登录了，太麻烦
        :param token:
        """
        assert token.startswith('aHR'), 'Token格式不对,应该是aHR开头!'
        self.token = token
        self.random_code = self.generate_webkit_boundary()
        self.random_code = 'WebKitFormBoundaryv0bzBwXwe0NLNG8B'
        self.class_dict = {}
        self.stid = None
        self.get_stid()
        self.BASE_XML = '''<?xml version="1.0" encoding="utf-8" ?>
<results examid="0" stid="[STID]" stname="" stsex="1" stcardid="" stsid="" stsname=""
         couid="[COUID]" tpid="" tpname="" sbjid="" sbjname="" begin="1698238104753"
         overtime="1698238669659" patter="50" score="100" isclac="true">
    <ques type="1" count="15" number="30">
        <q id="257165" num="2" ans="" sucess="true" score="2"></q>
        <q id="245354" num="2" ans="" sucess="true" score="2"></q>
        <q id="257156" num="2" ans="" sucess="true" score="2"></q>
        <q id="257171" num="2" ans="" sucess="true" score="2"></q>
        <q id="257219" num="2" ans="" sucess="true" score="2"></q>
        <q id="257233" num="2" ans="" sucess="true" score="2"></q>
        <q id="257155" num="2" ans="" sucess="true" score="2"></q>
        <q id="257215" num="2" ans="" sucess="true" score="2"></q>
        <q id="245359" num="2" ans="" sucess="true" score="2"></q>
        <q id="245339" num="2" ans="" sucess="true" score="2"></q>
        <q id="245380" num="2" ans="" sucess="true" score="2"></q>
        <q id="245369" num="2" ans="" sucess="true" score="2"></q>
        <q id="245383" num="2" ans="" sucess="true" score="2"></q>
        <q id="257190" num="2" ans="" sucess="true" score="2"></q>
        <q id="257169" num="2" ans="" sucess="true" score="2"></q>
    </ques>
    <ques type="2" count="20" number="40">
        <q id="245407" num="2" ans="472,218,963" sucess="true" score="2"></q>
        <q id="257259" num="2" ans="414,758" sucess="true" score="2"></q>
        <q id="245428" num="2" ans="" sucess="true" score="2"></q>
        <q id="257281" num="2" ans="" sucess="true" score="2"></q>
        <q id="257254" num="2" ans="" sucess="true" score="2"></q>
        <q id="257296" num="2" ans="" sucess="true" score="2"></q>
        <q id="257267" num="2" ans="" sucess="true" score="2"></q>
        <q id="257251" num="2" ans="" sucess="true" score="2"></q>
        <q id="257265" num="2" ans="" sucess="true" score="2"></q>
        <q id="257284" num="2" ans="" sucess="true" score="2"></q>
        <q id="257330" num="2" ans="" sucess="true" score="2"></q>
        <q id="257242" num="2" ans="" sucess="true" score="2"></q>
        <q id="257332" num="2" ans="" sucess="true" score="2"></q>
        <q id="257258" num="2" ans="" sucess="true" score="2"></q>
        <q id="245408" num="2" ans="" sucess="true" score="2"></q>
        <q id="257320" num="2" ans="" sucess="true" score="2"></q>
        <q id="257331" num="2" ans="" sucess="true" score="2"></q>
        <q id="245405" num="2" ans="" sucess="true" score="2"></q>
        <q id="245404" num="2" ans="" sucess="true" score="2"></q>
        <q id="257252" num="2" ans="" sucess="true" score="2"></q>
    </ques>
    <ques type="3" count="15" number="30">
        <q id="257411" num="2" ans="0" sucess="true" score="2"></q>
        <q id="257423" num="2" ans="1" sucess="true" score="2"></q>
        <q id="245474" num="2" ans="" sucess="true" score="2"></q>
        <q id="257391" num="2" ans="" sucess="true" score="2"></q>
        <q id="245476" num="2" ans="" sucess="true" score="2"></q>
        <q id="245464" num="2" ans="" sucess="true" score="2"></q>
        <q id="257408" num="2" ans="" sucess="true" score="2"></q>
        <q id="245470" num="2" ans="" sucess="true" score="2"></q>
        <q id="245457" num="2" ans="" sucess="true" score="2"></q>
        <q id="257368" num="2" ans="" sucess="true" score="2"></q>
        <q id="245475" num="2" ans="" sucess="true" score="2"></q>
        <q id="257340" num="2" ans="" sucess="true" score="2"></q>
        <q id="245491" num="2" ans="" sucess="true" score="2"></q>
        <q id="257341" num="2" ans="" sucess="true" score="2"></q>
        <q id="245503" num="2" ans="" sucess="true" score="2"></q>
    </ques>
</results> '''

    @classmethod
    def generate_webkit_boundary(cls, random_part_length=16):
        prefix = "WebKitFormBoundary"
        random_part = ''.join(random.choices(string.ascii_letters + string.digits, k=random_part_length))
        return prefix + random_part

    @property
    def topic_headers(self):
        return {
            "Host": "www.51ixuejiao.com",
            "Proxy-Connection": "keep-alive",
            "Content-Length": "6528",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "X-Custom-Return": "json",
            "Authorization": f"Basic {self.token}",
            "X-Custom-Action": "null",
            "X-Custom-Header": "WeishaKeji",
            "Access-Control-Allow-Methods": "POST,GET,DELETE,PUT,PATCH,HEAD,OPTIONS",
            "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryntJB8ZcpBYxj0NaF",
            "Accept": "application/json, text/plain, */*",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.61",
            "Encrypt": "true",
            "Access-Control-Allow-Headers": "X-Requested-With",
            "X-Custom-Method": "put",
            "Origin": "http://www.51ixuejiao.com",
            "Referer": "http://www.51ixuejiao.com/Web/Test/doing?tpid=1052&couid=1732",
            "Cookie": "Hm_lvt_b26bce9caf4acecec843f148fc84d8d7=1697102657,1698237253; Hm_lpvt_b26bce9caf4acecec843f148fc84d8d7=1698238104"
        }

    @property
    def api_headers(self):
        headers = {
            "Host": "www.51ixuejiao.com",
            "Connection": "keep-alive",
            "X-Custom-Return": "json",
            "Authorization": f"Basic {self.token}",
            "X-Custom-Action": "null",
            "X-Custom-Header": "WeishaKeji",
            "Access-Control-Allow-Methods": "POST,GET,DELETE,PUT,PATCH,HEAD,OPTIONS",
            "Accept": "application/json, text/plain, */*",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.188",
            "Encrypt": "true",
            "Access-Control-Allow-Headers": "X-Requested-With",
            "X-Custom-Method": "get",
            "Referer": "http://www.51ixuejiao.com/student/course/index",
        }
        return headers

    @property
    def olid_headers(self):
        headers = {
            "Host": "www.51ixuejiao.com",
            "Proxy-Connection": "keep-alive",
            "Accept": "application/json, text/plain, */*",
            "Access-Control-Allow-Headers": "X-Requested-With",
            "Authorization": f"Basic {self.token}",
            "X-Custom-Header": "weishakeji",
            "Access-Control-Allow-Methods": "POST,GET,DELETE,PUT,PATCH,HEAD,OPTIONS",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
            "Referer": "http://www.51ixuejiao.com/web/course/study.712",
        }
        return headers

    def brush_one_class(self, couid, olid):
        try:
            code = self.random_code
            url = 'http://www.51ixuejiao.com/api/v2/Course/StudyLog'
            data = f'''------{code}
Content-Disposition: form-data; name="couid"

{couid}
------{code}
Content-Disposition: form-data; name="olid"

{olid}
------{code}
Content-Disposition: form-data; name="playTime"

3600
------{code}
Content-Disposition: form-data; name="studyTime"

3600
------{code}
Content-Disposition: form-data; name="totalTime"

3600
------{code}--
'''
            print(data)
            headers = {
                "Host": "www.51ixuejiao.com",
                "Connection": "keep-alive",
                "Content-Length": "527",
                "X-Custom-Return": "json",
                "Authorization": f"Basic {self.token}",
                "X-Custom-Action": "null",
                "X-Custom-Header": "WeishaKeji",
                "Access-Control-Allow-Methods": "POST,GET,DELETE,PUT,PATCH,HEAD,OPTIONS",
                "Content-Type": f"multipart/form-data; boundary=----{code}",
                "Accept": "application/json, text/plain, */*",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.188",
                "Encrypt": "true",
                "Access-Control-Allow-Headers": "X-Requested-With",
                "X-Custom-Method": "post",
                "Origin": "http://www.51ixuejiao.com",
                "Referer": f"http://www.51ixuejiao.com/web/course/study.{couid}?referrer=http%3A%2F%2Fwww.51ixuejiao.com%2Fweb%2Fcourse%2Fdetail.{couid}&olid={olid}",
            }

            res = requests.post(url, data=data, headers=headers, verify=False)
            data = base64.b64decode(res.text).decode('utf-8')
            print(data)

            if re.search(r'success"\s*:\s*true', data):
                return True
        except:
            traceback.print_exc()
            return

    @staticmethod
    def decode_unicode(encoded_unicode):
        encoded_unicode = encoded_unicode.replace('%u', '\\u')
        decoded_string = bytes(encoded_unicode, 'ascii').decode('unicode-escape')
        return decoded_string

    def get_stid(self):
        url = 'http://www.51ixuejiao.com/api/v2/Account/Current'
        res = requests.get(url, verify=False, headers=self.api_headers)
        data = base64.b64decode(res.text).decode('utf-8')
        self.stid = re.search(r'Ac_ID*"\s*:\s*(\d+),', data).group(1)

        return self.stid

    def get_all_class(self):
        url = 'http://www.51ixuejiao.com/api/v2/Course/purchased'
        params = {
            "acid": self.stid,
            "search": "",
            "enable": "true",
            "size": "10",
            "index": "1"
        }
        res = requests.get(url, params=params, verify=False, headers=self.api_headers)
        res.raise_for_status()
        res.encoding = 'utf-8'
        data = base64.b64decode(res.text).decode('utf-8')
        data = re.sub(r'eval\(.*?rce\)', '\"\"', data)
        data = json.loads(data)
        classes_info = data.get("result")
        for info in classes_info:
            couids = info.get("Cou_ID")
            class_name = info.get("Cou_Name")
            class_name = self.decode_unicode(class_name)
            olids = self.get_olids(couids)
            if not olids:
                return
            self.class_dict[couids] = {
                "olids": olids,
                "name": class_name
            }
            print(f'识别到账号课程:\n{class_name}----Couids:{couids}----Olids:{olids}')
        return self.class_dict

    @classmethod
    def encode_to_unicode_msg(cls, text):
        encoded_text = ""
        for c in text:
            if '\u4e00' <= c <= '\u9fa5':  # 检查字符是否为中文
                encoded_text += '%u{:04X}'.format(ord(c))  # 如果是中文，进行Unicode编码
            else:
                encoded_text += urllib.parse.quote(c)  # 如果不是中文，进行URL编码
        return encoded_text

    def reply_topic(self, couid):
        topic_xml = self.BASE_XML
        topic_xml = topic_xml.replace('[STID]', self.stid)
        topic_xml = topic_xml.replace('[COUID]', couid)
        print(topic_xml)
        url = 'http://www.51ixuejiao.com/api/v2/TestPaper/InResult'
        data = f'''------WebKitFormBoundaryntJB8ZcpBYxj0NaF
Content-Disposition: form-data; name="result"

{self.encode_to_unicode_msg(topic_xml)}
------WebKitFormBoundaryntJB8ZcpBYxj0NaF--
        '''
        try:
            res = requests.post(url, headers=self.topic_headers, data=data)
            print(f'couid:{couid}一键做题完成,分数100!!!!')
        except:
            traceback.print_exc()

    def get_olids(self, couids):
        url = f'http://www.51ixuejiao.com/api/v2/Course/LogForOutlineVideo?stid={self.stid}&couid={couids}'
        res = requests.get(url, verify=False, headers=self.api_headers)
        res.raise_for_status()
        text = base64.b64decode(res.text).decode('utf-8')
        # print(text)
        res.encoding = 'utf-8'
        text = text.replace(' ', '')
        oilds = re.findall(r'Ol_ID\s*:\s*\"(\d+)\"', text)
        return oilds

    def main(self):
        suc_once = 0
        bad_once = 0
        self.get_all_class()
        sum_lesson = 0
        for x in self.class_dict.values():
            sum_lesson += len(list(x["olids"]))
        print(f'数据获取完毕,共计{len(self.class_dict)}个科目,{sum_lesson}节课!')
        print(self.class_dict)
        input('连续点击回车开始刷,多线程秒刷，只能点击一次,不要重复点击!!!')
        with ThreadPoolExecutor(max_workers=20) as Pool:
            threads = []
            for key, value in self.class_dict.items():
                couid = key
                name = value["name"]
                for olid in value["olids"]:
                    thread = Pool.submit(self.brush_one_class, couid=couid, olid=olid)
                    thread.name = f'课程:{name} | Couid:{couid} | Olid:{olid}'
                    print(thread.name + '   已经提交线程!!!')
                    threads.append(thread)
            for thread in as_completed(threads):
                res = thread.result()
                name = thread.name
                if res:
                    suc_once += 1
                else:
                    bad_once += 1
                print(f'{name} : {"完成" if res else "失败!!!!!"}')
            input('请点击我的课程-课程右上角-综合成绩--更新学习记录,更新完成后回车,自动答题!!!\n' * 5)
            for key, value in self.class_dict.items():
                self.reply_topic(key)
        print(f'共计{sum_lesson}节课,成功:{suc_once}次,失败:{bad_once}次!!!')
        print(f'''
刷课的数据,10分钟后才会更新,不会立即更新!!!!!!
刷课的数据,10分钟后才会更新,不会立即更新!!!!!!
刷课的数据,10分钟后才会更新,不会立即更新!!!!!!
刷课的数据,10分钟后才会更新,不会立即更新!!!!!!
刷课的数据,10分钟后才会更新,不会立即更新!!!!!!

如果十几分钟都显示没，直接多刷几遍！！！！！
所以不要着急,只要显示成功,就肯定是成功了!!!
        ''')
        print(f'''
如果想让立即生效，点击->课程->综合成绩->更新学习记录!!!!
如果想让立即生效，点击->课程->综合成绩->更新学习记录!!!!
如果想让立即生效，点击->课程->综合成绩->更新学习记录!!!!
如果想让立即生效，点击->课程->综合成绩->更新学习记录!!!!
如果想让立即生效，点击->课程->综合成绩->更新学习记录!!!!
如果想让立即生效，点击->课程->综合成绩->更新学习记录!!!!
''')


if __name__ == '__main__':
    print(f'''
    ******* 51爱学教云课堂AutoStudy1.0 *******
         本程序仅用于学习,切勿用于非法用途
                By:Ruan
            CSDN: https://blog.csdn.net/qq_34511096?type=blog
            GitHub: https://github.com/RYF5584
            知乎: https://www.zhihu.com/people/eternal-82-2
        程序会自动识别账号中存在的课程，已经过期的不会识别！！！
        只能刷课，题目做不了！！！
        刷课的数据,10分钟后才会更新,不会立即更新!!!!!!
        但是刷完以后，你点进视频，就会显示100%了
        学习进度10分钟后才会有变化！！
        如果想让立即生效，点击->课程->综合成绩->更新学习记录!
    ******* 51爱学教云课堂AutoStudy1.0 *******

    ''')

    while True:
        try:
            token = input(
                '请输入token:请点击浏览器开发者工具\n登录账号后随便点击一个网络请求,在请求标头中寻找Authorization参数,请复制Basic 后面所有（应该是aHR开头）,\n请输入:').strip()
            spider = BrushClass(token=token)
            print(spider.get_stid())
            spider.main()
            if input('回车继续刷课(q退出)......').lower() == 'q':
                break
        except Exception as e:
            print(e)
