

import sys
import codecs
import requests,json,os
import base64
import codecs
import Crypto
from Crypto.Cipher import AES
import re


class Spider():
    def __init__(self,idNum):

        self.header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0',
                       'Referer': 'http://music.163.com/'}
        self.url = 'http://music.163.com/weapi/v1/resource/comments/R_SO_4_'+idNum+'?csrf_token='

    def __get_jsons(self,url,page):
        # 获取两个参数
        music = WangYiYun()
        text = music.create_random_16()
        # rid = re.findall("comments/(.*)\?", self.url)
        print (self.url)
        rid =re.findall(r"comments/(.*?)\?",self.url)[0]
        print (rid)
        params = music.get_params(rid,text,page)

        encSecKey = music.get_encSEcKey(text)
        fromdata = {'params' : params,'encSecKey' : encSecKey}
        jsons = requests.post(url, data=fromdata, headers=self.header)
        #print(jsons.raise_for_status())
        # 打印返回来的内容，是个json格式的
        #print(jsons.content)
        return jsons.text

    def json2list(self,jsons):
        '''把json转成字典，并把他重要的信息获取出来存入列表'''
        # 可以用json.loads()把他转成字典
        #print(json.loads(jsons.text))
        users = json.loads(jsons)
        comments = []
        for user in users['comments']:
            # print(user['user']['nickname']+' : '+user['content']+'   点赞数：'+str(user['likedCount']))
            name = user['user']['nickname']
            content = user['content']
            # 点赞数
            likedCount = user['likedCount']
            user_dict = {'name': name, 'content': content, 'likedCount': likedCount}
            comments.append(user_dict)
        return comments

    def run(self,idNum):
        self.page = 1
        while True:
            jsons = self.__get_jsons(self.url,self.page)
            comments = self.json2list(jsons)
            non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

##            print(str(comments[0]).translate(non_bmp_map))
            print('self.page = '+str(self.page))
            print(idNum)
            with open("./"+idNum+".txt","a",encoding='utf-8') as f:
##                print(len(comments))
                for ii in range(len(comments)):
                    f.write(str(comments[ii]).translate(non_bmp_map))
                    f.write('\n')
##                    print(ii)
                f.close()
            # 当这一页的评论数少于20条时，证明已经获取完
##            self.write2sql(comments)
            if len(comments) < 20:
                print('评论已经获取完')
                break
            self.page +=1

# 找出post的两个参数params和encSecKey
class WangYiYun():

    def __init__(self):
        # 在网易云获取的三个参数

        self.second_param = '010001'
        self.third_param = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
        self.fourth_param = '0CoJUm6Qyw8W8jud'

    def create_random_16(self):
        '''获取随机十六个字母拼接成的字符串'''
        return (''.join(map(lambda xx: (hex(ord(xx))[2:]), str(os.urandom(16)))))[0:16]

    def aesEncrypt(self, text, key):

        # 偏移量
        iv = '0102030405060708'
        # 文本

        pad = 16 - len(text) % 16
        text = text + pad * chr(pad)


        encryptor = AES.new(bytearray(key,'utf-8'), 2, bytearray(iv,'utf-8'))

       # encryptor = AES.new(key, 2, iv)

        ciphertext = encryptor.encrypt(bytearray(text,'utf-8'))
##        print(bytearray(key,'utf-8'))
        ciphertext = base64.b64encode(ciphertext)
        return ciphertext

    def get_params(self,rid,text,page):
        '''获取网易云第一个参数'''
        # 第一个参数
        if page == 1:
            self.first_param = '{rid: "%s", offset: "0", total: "true", limit: "20", csrf_token: ""}'%rid
            print (self.first_param)
        else:
            self.first_param = ('{rid:"%s", offset:%s, total: "false", limit: "20", csrf_token: ""}'%(rid ,str((page-1)*20)))


        params = self.aesEncrypt(self.first_param, self.fourth_param).decode('utf-8')
        params = self.aesEncrypt(params, text)

        return params

    def rsaEncrypt(self, pubKey, text, modulus):
        '''进行rsa加密'''
        text = text[::-1]
        rs = int(codecs.encode(text.encode('utf-8'), 'hex_codec'), 16) ** int(pubKey, 16) % int(modulus, 16)
        return format(rs, 'x').zfill(256)

    def get_encSEcKey(self,text):
        '''获取第二个参数'''
        pubKey = self.second_param
        moudulus = self.third_param
        encSecKey = self.rsaEncrypt(pubKey, text, moudulus)
        return encSecKey

def main(idPs):
    for jj in range(len(idPs)):
        idNum = idPs[jj]
        spider = Spider(idNum)
        spider.run(idNum)
