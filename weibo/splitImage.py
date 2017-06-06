# -*-coding:utf8-*-
#                       _oo0oo_
#                      o8888888o
#                      88" . "88
#                      (| -_- |)
#                      0\  =  /0
#                    ___/`---'\___
#                  .' \\|     |// '.
#                 / \\|||  :  |||// \
#                / _||||| -:- |||||- \
#               |   | \\\  -  /// |   |
#               | \_|  ''\---/''  |_/ |
#               \  .-\__  '-'  ___/-. /
#             ___'. .'  /--.--\  `. .'___
#          ."" '<  `.___\_<|>_/___.' >' "".
#         | | :  `- \`.;`\ _ /`;.`/ - ` : | |
#         \  \ `_.   \_ __\ /__ _/   .-` /  /
#     =====`-.____`.___ \_____/___.-`___.-'=====
#                       `=---='
#
#
#     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#               佛祖保佑         永无BUG
#
#
'''
@version: ??
@author: xiholix
@contact: x123872842@163.com
@software: PyCharm
@file: splitImage.py
@time: 17-6-6 下午12:31
'''
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
import cv2
from PIL import Image
from captcha_utils import CaptchaUtils
import numpy as np


def get_line_width(_image, _height=27, _width=4):
    '''
    对于一个二维的图像数组,值为255表示的是空白,返回从点_height,_width开始的非空白长度
    :param _image:
    :param _height:
    :param _width:
    :return:
    '''
    lineWidth = 0
    # print(_image[_height])
    for i in xrange(_width, _image.shape[1]):
        if _image[_height][i] == 255:
            return lineWidth
        lineWidth += 1

    return lineWidth


def remove_line(_image):
    '''
    根据图片在某点有连续两行有大于2的非空白区域,则判断该点对应的是噪声线条,这两行赋值对应的非空白区域变为空白区域
    这两行变为空白区域的长度是两行的非空白区域的最小值
    :param _image:
    :return:
    '''
    startHeight = 0
    startWidth = 0

    nowHeight = 0
    nowWidth = 0
    while nowHeight<_image.shape[0] and nowWidth <_image.shape[1]:
        lineWidth = get_line_width(_image, nowHeight, nowWidth)
        while lineWidth == 0:
            if nowWidth+1<_image.shape[1]:
                nowWidth += 1
            else:
                nowHeight += 1
                if nowHeight == _image.shape[0]:
                    break
                nowWidth = 0
            # if(nowHeight==27 ):
            #     print(nowWidth)
            lineWidth = get_line_width(_image, nowHeight, nowWidth)
        sign = False
        if lineWidth > 2:
            # print('linewidth is ')
            # print(lineWidth)
            # print('nowHeight %d, nowWidth %d'%(nowHeight, nowWidth))
            if nowHeight+1 == _image.shape[0]:
                break
            a = get_line_width(_image, nowHeight+1, nowWidth)
            b = get_line_width(_image, nowHeight+1, nowWidth+1)
            c = get_line_width(_image, nowHeight+1, nowWidth-1)
            max_a_b = max(a, b)
            max_a_b_c = max(max_a_b, c)
            # print(max_a_b_c)
            sign = True
            if max_a_b_c > 2:
                if max_a_b_c == c:
                    if max_a_b_c > lineWidth:
                        _image[nowHeight][nowWidth:nowWidth+lineWidth] = 255
                        _image[nowHeight+1][nowWidth-1:nowWidth-1+lineWidth] = 255
                    else:
                        _image[nowHeight][nowWidth:nowWidth+c] = 255
                        _image[nowHeight+1][nowWidth-1:nowWidth-1+c] = 255
                else:
                    if max_a_b == a:
                        if max_a_b_c > lineWidth:
                            _image[nowHeight][nowWidth:nowWidth + lineWidth] = 255
                            _image[nowHeight + 1][nowWidth:nowWidth + lineWidth] = 255
                        else:
                            _image[nowHeight][nowWidth:nowWidth + max_a_b_c] = 255
                            _image[nowHeight][nowWidth:nowWidth + max_a_b_c] = 255
                    else:
                        if max_a_b_c > lineWidth:
                            _image[nowHeight][nowWidth:nowWidth + lineWidth] = 255
                            _image[nowHeight + 1][nowWidth+1:nowWidth+1 + lineWidth] = 255
                        else:
                            _image[nowHeight][nowWidth:nowWidth + max_a_b_c] = 255
                            _image[nowHeight][nowWidth+1:nowWidth +1 +max_a_b_c] = 255
        # print(lineWidth)
        if sign and lineWidth>max_a_b_c and max_a_b_c>2:
            lineWidth = max_a_b_c
        nowWidth += lineWidth
        # print('lineWidth is %d nowWidth is %d'%(lineWidth, nowWidth))
        if nowWidth >= _image.shape[1]-1:
            nowHeight += 1
            nowWidth = 0

        if nowHeight == _image.shape[0]:
            break
    return _image

def test_clearnoise():
    path = 'img/5gbw4.png'
    im = cv2.imread(path, cv2.IMREAD_COLOR)
    print(im.shape)
    # im = cv2.flip(im, -1)
    # clear_horizontal_noise_line(im)
    # im = cv2.flip(im, -1)
    # clear_horizontal_noise_line(im)
    # clear_color(im)
    im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    print(im)
    print(im.shape)
    for i in xrange(im.shape[0]):
        for j in xrange(im.shape[1]):
            if im[i][j]<=180:
                im[i][j] = 0
            else:
                im[i][j] = 255
    # im = cv2.threshold(im, 150, 255, cv2.THRESH_BINARY)[1]
    # CaptchaUtils.clear_peper_noise(im, 2)
    t = im!=255
    t = np.array(t, dtype=np.int32)
    np.savetxt('value/test.txt', t, fmt='%d')
    # print(get_line_width(im))
    # print(im.shape)
    # print(im[0][0])
    im = remove_line(im)
    im = Image.fromarray(im)
    im.show()


def clear_horizontal_noise_line(image):
    first_height = 0
    has_find = False
    for i in range(image.shape[0]):
        if image[i][0][0] < 12 and image[i][0][1] < 12 and image[i][0][2] < 12 \
                and get_horizontal_noise_line_width(image, i, 0) >= 2:
            first_height = i
            has_find = True
    # print("first:", first_height)

    if not has_find:
        return
    now_width = 0
    now_height = first_height
    while now_width < image.shape[1]:
        width = get_horizontal_noise_line_width(image, now_height, now_width)
        # print(now_width, now_height, "width", width)

        # clear the horizontal noise line
        for i in range(now_width, now_width+width-1):
            top_num = 0
            bottom_num = 0
            # the upper pixel
            if is_black(i, now_height-1, image):
                top_num += 1
            # the upper left pixel
            if is_black(i-1, now_height-1, image):
                top_num += 1
            # the upper right pixel
            if is_black(i+1, now_height-1, image):
                top_num += 1
            # the lower pixel
            if is_black(i, now_height+1, image):
                bottom_num += 1
            # the left lower pixel
            if is_black(i-1, now_height+1, image):
                bottom_num += 1
            # the right lower pixel
            if is_black(i+1, now_height+1, image):
                bottom_num += 1

            if now_height != 0 and now_height != image.shape[0]:
                if top_num > 0 and bottom_num > 0:
                    continue

            image[now_height][i][0] = 255
            image[now_height][i][1] = 255
            image[now_height][i][2] = 255

        # find the next noise pixel
        a = get_horizontal_noise_line_width(image, now_height - 1, now_width + width - 1)
        b = get_horizontal_noise_line_width(image, now_height + 1, now_width + width - 1)
        c = get_horizontal_noise_line_width(image, now_height - 1, now_width + width)
        d = get_horizontal_noise_line_width(image, now_height + 1, now_width + width)
        if now_height == 0:
            a = 0
            c = 0

        if now_height == (image.shape[0] - 1):
            b = 0
            d = 0

        max_a_b = max(a, b)
        max_c_d = max(c, d)
        max_a_b_c_d = max(max_a_b, max_c_d)
        if max_a_b_c_d < 2:
            break
        if max_a_b == max_a_b_c_d:
            now_width += width-1
            if max_a_b == a:
                now_height -= 1
            else:
                now_height += 1

        else:
            now_width += width
            if max_c_d == c:
                now_height -= 1
            else:
                now_height += 1


def is_black(i, j, image):
    b = image[j, i][0]
    g = image[j, i][1]
    r = image[j, i][2]
    average = (int(r) + int(g) + int(b))/3
    if r < 244 and abs(average-b) < 4 and abs(average-g) < 4 and abs(average-r) < 4:
        return True
    return False


def clear_color(image):
    for i in range(image.shape[1]):
        for j in range(image.shape[0]):
            if is_black(i, j, image):
                image[j][i][0] = 20
                image[j][i][1] = 20
                image[j][i][2] = 20


def get_horizontal_noise_line_width(image, now_height, now_width):
    end_width = now_width
    while end_width < image.shape[1] \
            and image[now_height][end_width][0] < 12 \
            and image[now_height][end_width][1] < 12 \
            and image[now_height][end_width][2] < 12:

        # print(image[now_height][end_width][0],
        #       image[now_height][end_width][1],
        #       image[now_height][end_width][2])

        end_width += 1

    return end_width - now_width


if __name__ == "__main__":
    test_clearnoise()

