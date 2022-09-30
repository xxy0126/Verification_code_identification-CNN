# -*-coding:utf-8 -*-
from __future__ import unicode_literals
import cv2
import requests
import time
import json
import urllib.request
import importlib
import sys
import os
import http.cookiejar
import joblib
import numpy as np
import math

def del_noise(im_cut):
    ''' variable：bins：灰度直方图bin的数目
                  num_gray:像素间隔
        method：1.找到灰度直方图中像素第二多所对应的像素，即second_max,因为图像空白处比较多所以第一多的应该是空白，第二多的才是我们想要的内容。
                2.计算mode
                3.除了在mode+-一定范围内的，全部变为空白。
    '''
    bins = 16
    num_gray = math.ceil(256 / bins)
    hist = cv2.calcHist([im_cut], [0], None, [bins], [0, 256])
    lists = []
    for i in range(len(hist)):
        # print hist[i][0]
        lists.append(hist[i][0])
    second_max = sorted(lists)[-2]
    bins_second_max = lists.index(second_max)

    mode = (bins_second_max + 0.5) * num_gray

    for i in range(len(im_cut)):
        for j in range(len(im_cut[0])):
            if im_cut[i][j] < mode - 15 or im_cut[i][j] > mode + 15:
                # print im_cut[i][j]
                im_cut[i][j] = 255
    return im_cut


def predict(image):
    im = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    clf = joblib.load('model_knn.pkl')
    im_cut_1 = im[8:47, 27:52]
    im_cut_2 = im[8:47, 52:77]
    im_cut_3 = im[8:47, 77:102]
    im_cut_4 = im[8:47, 102:127]

    im_cut = [im_cut_1, im_cut_2, im_cut_3, im_cut_4]
    pre_text = []
    for i in range(4):
        # 图片转换成1维后，变成[[图片数组]]，2维的输入变量x
        im_temp = del_noise(im_cut[i])
        image = im_temp.reshape(-1)
        tmp = []
        tmp.append(list(image))
        x = np.array(tmp)

        pre_y = clf.predict(x)
        pre_y = np.argmax(pre_y[0])
        pre_text.append(str(pre_y))
    pre_text = ''.join(pre_text)
    return pre_text

def get_image_code():
    ''' 获取验证码并识别验证码返回 '''
    global timestamp,opener
    # 这是一个get请求，获取图片资源
    image_code_url = "https://zb.cninfo.com.cn/api1/api-a/image/imageCheck?timestamp=" + str(timestamp)
    res = opener.open(image_code_url).read()
    with open("%s.jpg" % 'image_code', "wb") as f:  # 将图片保存在本地
        f.write(res)
    image = cv2.imread('image_code.jpg')
    pre_code = predict(image) #调用predict_code进行图片识别
    print ('预测验证码为：%s' %(pre_code))
    return pre_code


def login(username, password):
    pre_code = get_image_code()
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Length': '124',
        'Content-Type': 'application/json;charset=UTF-8',
        'Host': 'zb.cninfo.com.cn:3367',
        'Origin': 'https://zb.cninfo.com.cn:8080',
        'Referer': 'https://zb.cninfo.com.cn:8080/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36',
    }
    datas = {
        'checkCode': pre_code,
        'imageCode': timestamp,
        'password': password,
        'username': username,
    }

    posturl = 'https://zb.cninfo.com.cn:3367/api-a/user/login'
    response = requests.post(url=posturl, data=json.dumps(datas), headers=headers)
    res_content = response.content
    json_dict = json.loads(response.text)
	
    # 判断登陆失败，则重新登陆
    if json_dict['code'] != 0:
        res_content = login(username, password)

    print (res_content)
    print ('登陆成功！')
    return res_content

if __name__ == "__main__":
    global opener, timestamp
    cookie = http.cookiejar.CookieJar()     # 声明一个CookieJar对象实例来保存cookie
    handler = urllib.request.HTTPCookieProcessor(cookie)     # 利用urllib2库的HTTPCookieProcessor对象来创建cookie处理器
    opener = urllib.request.build_opener(handler)     # 通过handler来构建opener

    timestamp = str(int(time.time() * 1000))
    username = 'tuxiaochao'
    password = 'f6b1dba6158981dc2511d2276eed1acec8041cc6'
    login(username, password)
