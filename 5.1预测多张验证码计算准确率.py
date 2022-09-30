#-*-coding:utf-8 -*-
from __future__ import division
import cv2
import math
import numpy as np
import os
import joblib


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


def predict(image, img_name):
    # image = cv2.imread('./img/8.jpg')
    im = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # im_cut_real = im[8:47, 28:128]

    im_cut_1 = im[8:47, 27:52]
    im_cut_2 = im[8:47, 52:77]
    im_cut_3 = im[8:47, 77:102]
    im_cut_4 = im[8:47, 102:127]

    im_cut = [im_cut_1, im_cut_2, im_cut_3, im_cut_4]
    pre_text = []
    for i in range(4):
        # 图片转换成1维后，变成[[图片数组]]，2维的输入变量x
        im_temp = del_noise(im_cut[i])
        # print type(im_temp)
        image = im_temp.reshape(-1)
        # print image.shape
        tmp = []
        tmp.append(list(image))
        x = np.array(tmp)

        pre_y = clf.predict(x)
        pre_y = np.argmax(pre_y[0])
        pre_text.append(str(pre_y))
    # print pre_text
    pre_text = ''.join(pre_text)
    if pre_text != img_name:
        print ('label:%s'%(img_name),'predict:%s'%(pre_text),'\t','false')
        return 0
    else:
        print ('label:%s'%(img_name),'predict:%s'%(pre_text))
        return 1

if __name__ == '__main__':
    img_dir = './img_test'
    img_name = os.listdir(img_dir)  # 列出文件夹下所有的目录与文件
    right = 0
    global clf
    clf = joblib.load('model_knn.pkl')
    for i in range(len(img_name)):
        path = os.path.join(img_dir, img_name[i])
        image = cv2.imread(path)
        name_list = list(img_name[i])[:4]
        name = ''.join(name_list)
        pre = predict(image, name)
        right += pre
    accuracy = (right/len(img_name))*100
    print (u'准确率为：%s%%,一共%s张验证码，正确：%s,错误：%s'%(accuracy,len(img_name),right,len(img_name)-right))



