# -*- coding:utf-8 -*-

import io
import os
import sys
from bilibili import BilibiliLogin, BilibiliFilter


def loginOption(bili):
    '''
    登录选项  
    返回登录成功后的 session
    '''
    os.system('cls')
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
        session = bili.login()
    elif op == '2':
        os.system('cls')
        session = bili.qrLogin()
    else:
        os.system('cls')
        sys.exit()
    return session


def filtersOption(session):
    '''
    屏蔽列表选项
    '''
    biliFilter = BilibiliFilter(session)
    option = '''
    1 ------ 清空屏蔽列表
    2 ------ 上传屏蔽列表
    3 ------ 备份屏蔽列表
    0 ------ 退出
    '''
    while True:
        os.system('cls')
        print('欢迎 %s ' % user)
        print('屏蔽列表选项')
        print(option)
        op = input('选择: ')
        if op == '1':
            os.system('cls')
            biliFilter.delAll()
        elif op == '2':
            os.system('cls')
            biliFilter.syncFile('tv.bilibili.player.xml')
        elif op == '3':
            os.system('cls')
            biliFilter.backup('tv.bilibili.player.bak.xml')
        elif op == '0':
            os.system('cls')
            break
        else:
            continue
        if input('\n' + '*' * 15 + '按任意键继续' + '*' * 15 + '\n'):
            pass

user = None

if __name__ == '__main__':
    bili = BilibiliLogin()
    session = loginOption(bili)
    if session:
        user = bili.getUser()
        filtersOption(session)
        os.system('cls')
        bili.logout()
    if input('\n' + '*' * 15 + '按任意键继续' + '*' * 15 + '\n'):
        pass
