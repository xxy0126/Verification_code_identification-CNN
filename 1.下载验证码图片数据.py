from __future__ import unicode_literals
import cv2
import requests
import time
import json
import urllib.request
import importlib
import sys
import os
importlib.reload(sys)
import http.cookiejar

#数据来自于https://zb.cninfo.com.cn/

def download_pic(path, idx):
    timestamp = str(int(time.time() * 1000))
    cookie = http.cookiejar.CookieJar()  # 声明一个CookieJar对象实例来保存cookie
    handler = urllib.request.HTTPCookieProcessor(cookie)  # 利用urllib2库的HTTPCookieProcessor对象来创建cookie处理器
    opener = urllib.request.build_opener(handler)  # 通过handler来构建opener

    # 这是一个get请求，获取图片资源
    image_code_url = "https://zb.cninfo.com.cn/api1/api-a/image/imageCheck?timestamp=" + str(timestamp)
    res = opener.open(image_code_url).read()
    file_name = path + '/' + str(idx) + '.jpg'
    with open(file_name, 'wb') as f:  # 将图片保存在本地
        f.write(res)

count = 1000
img_path = 'img_download'
for i in range(count):
    if i % 50 == 0:
        print('download ', i)
    time.sleep(2)
    try:
        download_pic(img_path, i)
    except Exception as e:
        print('download error', e)
