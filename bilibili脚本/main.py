# -*- coding:utf-8 -*-

import io
import os
import sys

from bilibili import BilibiliFilter, BilibiliLogin


if __name__ == '__main__':
    bili = BilibiliLogin()
    session = bili.login()
    if session:
        user = bili.getUser()
        bili_filter = BilibiliFilter(session, user)
        bili_filter.filterOption()
        os.system('cls')
    if input('\n' + '*' * 15 + '按回车键继续' + '*' * 15 + '\n'):
        pass
