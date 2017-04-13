# bilibili脚本
> 基于 Python3.5

## 简介 
哔哩哔哩上的屏蔽列表没有清空功能，因此作为一个强迫症，每次修改完屏蔽列表文件后要删除一大堆相似的规则，用手点实在是太累了。。。  
于是想着可以清空后重新上传一次来去掉多余的规则

## 特性
- 可以通过用户名密码方式登录或者通过扫二维码的方式进行登录
- 可以对屏蔽列表进行清空、上传、备份操作

## 更新说明
### 2017.04.12
- 添加清空、上传、备份功能

## 关键URL
- http://passport.bilibili.com/qrcode/getLoginUrl 获取二维码URL
- http://passport.bilibili.com/qrcode/getLoginInfo 检测二维码是否允许登录
- https://passport.bilibili.com/login?act=getkey 获取RSA加密KEY
- http://api.bilibili.com/x/dm/filter/user 用户屏蔽列表

## 下载安装  
- 需要安装的库
``` python
pip install requests
pip install pillow
pip install rsa
```

## 使用方法
> 运行脚本  
> 选择登录方式  
> 选择功能操作  

## 注意事项
1. 第一次登录需要输入用户名和密码，脚本会将其保存在同目录 'bilibili.conf' 文件中
2. 验证码弹出后需要关闭才能继续登录
3. 二维码有一定的时间限制，太长时间未扫会失效
4. 清空屏蔽列表会先备份到当前目录的 'tv.bilibili.player.bak.xml' 文件中
5. 上传需要当前目录存在正确格式的　'tv.bilibili.player.xml' 文件