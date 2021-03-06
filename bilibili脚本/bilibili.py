# -*- coding:utf-8 -*-

import binascii
import codecs
import io
import json
import os
import re
from xml.dom import minidom
from xml.etree import ElementTree as et

import qrcode
import requests
import rsa
from PIL import Image
from requests.utils import cookiejar_from_dict as dict2cookies
from requests.utils import dict_from_cookiejar as cookies2dict


class BilibiliLogin():
    '''
    Bilibili 登录类
    '''

    def __init__(self):
        # 用户昵称
        self.user = ''
        self.qrcode_url = 'http://passport.bilibili.com/qrcode/getLoginUrl'
        self.qrcheck_url = 'http://passport.bilibili.com/qrcode/getLoginInfo'
        self.login_url = 'https://passport.bilibili.com/login'
        self.captcha_url = 'https://passport.bilibili.com/captcha'
        self.getkey_url = 'https://passport.bilibili.com/login?act=getkey'
        self.check_url = 'https://passport.bilibili.com/login/dologin'
        self.user_url = 'https://account.bilibili.com/home/userInfo'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) Chrome/53.0.2785.104',
            'Host': 'passport.bilibili.com',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': self.login_url,
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Proxy-Connection': 'keep-alive',
        }
        self.session = requests.Session()
        # cookies保存文件
        self.cookies_file = 'cookies.json'
        # 登录账号
        self.username = ''
        # 登录密码
        self.password = ''
        try:
            self.login_page = self.session.get(self.login_url)
            print('连接服务器成功')
        except requests.exceptions.ConnectionError as e:
            print('连接服务器失败，请检查网络设置')

    def __loadCookies(self):
        '''
        从文件 cookies.json 中
        读取登录成功的Cookies  
        '''
        if not os.path.exists(self.cookies_file):
            print('Cookies文件读取失败，请先登录')
            return False
        try:
            with open(self.cookies_file, 'r') as fp:
                cookies = json.load(fp)
                self.session.cookies = dict2cookies(cookies)
                return True
        except:
            os.remove(self.cookies_file)
            print('Cookies文件读取错误，请先登录')
            return False

    def normalLogin(self):
        '''
        通过 用户名 密码 验证码 形式登录 bilibili  
        返回登录 session
        '''
        self.username = input('请输入用户名：')
        self.password = input('请输入密码：')
        captcha = '0'
        while captcha == '0':
            self.__getCaptcha()
            captcha = input('请输入验证码(输入0刷新验证码)：')
        username = self.username
        password = self.__getRsaPwd(self.password)
        data = {
            'userid': username,
            'pwd': password,
            'vdcode': captcha,
        }
        print('登录中。。。。。。')
        try:
            self.session.post(self.check_url, data=data)
        except requests.exceptions.ConnectionError as e:
            print('!' * 17 + '登录超时' + '!' * 17)
        if self.__isLogin():
            self.__saveCookies()
            return self.session
        else:
            print('!' * 13 + '验证码或密码错误' + '!' * 13)

    def qrLogin(self):
        '''
        通过客户端扫二维码登录 bilibili  
        返回登录 session
        '''
        while True:
            html = self.session.get(self.qrcode_url).text
            params = json.loads(html)
            qr_url = params['data']['url']
            oauthKey = re.findall('oauthKey=(.*)', qr_url)[0]
            qr = qrcode.QRCode(
                version=2,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=1
            )
            qr.add_data(qr_url)
            qr.make(fit=True)
            img = qr.make_image()
            img.show()
            op = input('按回车键继续(输入0刷新二维码)：')
            if op != '0':
                break
        print('登录中。。。。。。', end='')
        self.session.post(self.qrcheck_url, data={'oauthKey': oauthKey})
        if self.__isLogin():
            self.__saveCookies()
            return self.session
        else:
            print('!' * 11 + '二维码超时或拒绝登录' + '!' * 11)

    def __getCaptcha(self):
        '''
        获取验证码并显示
        '''
        captcha = self.session.get(self.captcha_url, stream=True).content
        img = Image.open(io.BytesIO(captcha))
        img.show()

    def __getRsaPwd(self, password):
        '''
        返回加密后的密码
        '''
        response = self.session.get(self.getkey_url)
        token = json.loads(response.text)
        text = str(token['hash'] + password).encode('utf-8')
        key = rsa.PublicKey.load_pkcs1_openssl_pem(token['key'])
        pwd = rsa.encrypt(text, key)
        pwd = binascii.b2a_base64(pwd)
        return pwd

    def __isLogin(self):
        '''
        判断是否登录成功  
        成功返回 True  
        失败返回 False
        '''
        html = self.session.get(self.user_url).text
        params = json.loads(html)
        code = params['code']
        if code == 0:
            self.user = params['data']['uname']
            print('用户 %s 登录成功' % self.user)
            return True
        else:
            print('!' * 17 + '登录失败' + '!' * 17)
            return False

    def __saveCookies(self):
        '''
        保存登录成功的Cookies  
        到文件 cookies.json 中
        '''
        with open('cookies.json', 'wb') as fp:
            cookises = cookies2dict(self.session.cookies)
            fp.write(json.dumps(cookises, indent=True).encode('utf-8'))

    def getUser(self):
        return self.user

    def login(self):
        '''
        登录Bilibili  
        返回登录成功后的 session
        '''
        os.system('cls')
        if self.__loadCookies() and self.__isLogin():
            return self.session
        print('登录选项')
        option = '''
        1 ------ 用户名密码登录
        2 ------ 二维码登录
        0 ------ 退出
        '''
        print(option)
        op = input('选择: ')
        if op == '1':
            os.system('cls')
            return self.normalLogin()
        elif op == '2':
            os.system('cls')
            return self.qrLogin()
        else:
            os.system('cls')
            return


class BilibiliFilter():
    '''
    Bilibili 屏蔽列表类  
    需传入登录成功的 SESSION  
    和用户昵称（可选）
    '''

    def __init__(self, session, user='B站用户'):
        self.filter_url = 'http://api.bilibili.com/x/dm/filter/user'
        self.filter_del_url = 'http://api.bilibili.com/x/dm/filter/user/del'
        self.filter_add_url = 'http://api.bilibili.com/x/dm/filter/user/add'
        self.session = session
        self.user = user
        self.session.headers['Host'] = 'api.bilibili.com'
        self.session.headers['Referer'] = 'http://static.hdslb.com/play.swf'

    def getFilters(self):
        '''
        返回获取到的屏蔽列表  
        '''
        html = self.session.get(self.filter_url).text
        params = json.loads(html)
        filters = params['data']['rule']
        return filters

    def syncFile(self, filename='tv.bilibili.player.xml'):
        '''
        上传屏蔽列表  
        默认上传文件为当前目录的  
        tv.bilibili.player.xml
        '''
        r = re.compile(r'<item enabled="true">(\w)=(.*?)</item>')
        try:
            with open(filename, 'rb') as fp:
                text = fp.read().decode('utf-8')
                filters = r.findall(text)
        except IOError:
            print('当前目录不存在 %s 文件' % filename)
            return
        print('上传屏蔽列表中。。。。。。')
        for item in filters:
            data = {}
            if item[0] == 't':
                data['type'] = '0'
            elif item[0] == 'r':
                data['type'] = '1'
            elif item[0] == 'u':
                data['type'] = '2'
            else:
                data['type'] = '0'
            data['filter'] = item[1]
            self.session.post(self.filter_add_url, data=data)
        print('*' * 13 + '上传屏蔽列表完成' + '*' * 13)

    def delAll(self):
        '''
        清空同步列表
        '''
        self.backup()
        filters = self.getFilters()
        if not filters:
            print('!' * 10 + '清空终止，屏蔽列表为空' + '!' * 10)
            return
        ids = []
        for item in filters:
            ids.append(item['id'])
        print('清空屏蔽列表中。。。。。。')
        for i in ids:
            data = {'ids': i}
            self.session.post(self.filter_del_url, data=data)
        print('*' * 13 + '清空屏蔽列表完成' + '*' * 13)

    def backup(self, filename='tv.bilibili.player.bak.xml'):
        '''
        备份屏蔽列表  
        默认保存文件为当前目录的  
        tv.bilibili.player.bak.xml
        '''
        filters = self.getFilters()
        if not filters:
            print('!' * 10 + '备份终止，屏蔽列表为空' + '!' * 10)
            return
        print('备份屏蔽列表中。。。。。。')
        with codecs.open(filename, 'w', encoding='utf-8') as fp:
            doc = minidom.Document()
            root = doc.createElement('filters')
            doc.appendChild(root)
            for item in filters:
                node = doc.createElement('item')
                node.setAttribute('enabled', 'true')
                if item['type'] == 0:
                    s = 't=' + item['filter']
                elif item['type'] == 1:
                    s = 'r=' + item['filter']
                elif item['type'] == 2:
                    s = 'u=' + item['filter']
                else:
                    s = 'null'
                node.appendChild(doc.createTextNode(s))
                root.appendChild(node)
            doc.writexml(fp, newl='\n', encoding='utf-8')
        print('*' * 13 + '备份屏蔽列表完成' + '*' * 13)

    def filterOption(self):
        '''
        屏蔽列表选项
        '''
        option = '''
        1 ------ 清空屏蔽列表
        2 ------ 上传屏蔽列表
        3 ------ 备份屏蔽列表
        0 ------ 退出
        '''
        while True:
            os.system('cls')
            print('欢迎 %s ' % self.user)
            print('屏蔽列表选项')
            print(option)
            op = input('选择: ')
            if op == '1':
                os.system('cls')
                self.delAll()
            elif op == '2':
                os.system('cls')
                self.syncFile()
            elif op == '3':
                os.system('cls')
                self.backup()
            elif op == '0':
                os.system('cls')
                break
            else:
                continue
            if input('\n' + '*' * 15 + '按回车键继续' + '*' * 15 + '\n'):
                pass
