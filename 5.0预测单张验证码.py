#-*-coding:utf-8 -*-
from __future__ import division
import cv2
import math
import numpy as np
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

if __name__ == '__main__':
    img = './img_test/1340.jpg'
    image = cv2.imread(img)
    pre_text = predict(image)
    print ('预测验证码为:%s'%(pre_text))




