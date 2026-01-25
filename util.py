import re
from datetime import datetime
from random import random, randint
from typing import Optional

from ascript.android.system import open
from ascript.android import action
# __init__.py 为初始入口文件,工程代码的入口文件.

# 导入动作库常用函数
from ascript.android.action import click, slide, Touch, gesture
# 导入控件检索相关
from ascript.android.node import Selector
# 导入图色相关
from ascript.android.screen import capture, FindColors, FindImages, Ocr
# 导入系统相关
from ascript.android import system
# 环境设备相关
from ascript.android.system import R, Device

import math
import time

curApp = None
WAIT_LOW = 20
WAIT_HIGH = 30

def clickNode(node):
    centerX = node.rect.centerX() + math.floor(random() * 11) - 5
    centerY = node.rect.centerY() + math.floor(random() * 11) - 5
    print(centerX, centerY)
    click(centerX, centerY)

def clickXY(x, y):
    centerX = randint(x-5, x+5)
    centerY = randint(y-5, y+5)
    # print(centerX, centerY)
    click(centerX, centerY)

def findDescAndClick(keyword, delay=5):
    print('findDescAndClick' + keyword)
    for _ in range(delay):
        node = Selector().desc(keyword).find()
        if node:
            clickNode(node)

            return node
        else:
            time.sleep(2)
    print('findDescAndClick exit' + keyword)
    return None


def findPathAndClick(keyword, delay=5):
    print('findPathAndClick' + keyword)
    for _ in range(delay):
        node = Selector().path(keyword).find()
        if node:
            clickNode(node)
            return node
        else:
            time.sleep(2)

    print('findPathAndClick exit' + keyword)
    return None


def findTextAndClick(keyword, delay=5):
    print('findTextAndClick' + keyword)
    for _ in range(delay):
        node = Selector().text(keyword).find()

        if node:
            clickNode(node)

            return node
        else:
            time.sleep(2)
    print('findTextAndClick exit' + keyword)
    return None

def findText(keyword, delay=5):
    print('findText' + keyword)
    for _ in range(delay):
        node = Selector().text(keyword).find()

        if node:
            print('findText end' + node.text)
            return node.text
        else:
            time.sleep(2)
    print('findText exit' + keyword)
    return None

def findDesc(keyword, delay=5):
    print('findDesc' + keyword)
    for _ in range(2):
        node = Selector().desc(keyword).find()

        if node:
            print('findDesc end' + node.desc)
            return node.desc
        else:
            time.sleep(2)
    print('findDesc error' + keyword)
    return None

def findImageAndClick(keyword, delay=5):
    print('findImageAndClick' + keyword)
    for _ in range(delay):
        res = FindImages.find_template([R.img(keyword), ], confidence=0.7)

        if res:
            print("findImageAndClick", res)
            x = res["center_x"] + randint(-10, 20)
            y = res["center_y"] + randint(-10, 20)

            click(x, y)

            return True
        else:
            time.sleep(2)
    print('findImageAndClick exit' + keyword)
    return None


def findTextEndAndClick(keyword, end, delay=5):
    print('findTextEndAndClick' + keyword)
    for _ in range(delay):
        node = Selector().text(keyword).find()

        if node:
            clickNode(node)

            return node
        else:
            time.sleep(2)

        node2 = Selector().text(end).find()
        if node2:
            return node
    print('findTextAndClick exit' + keyword)
    return None


def swipeBackOnes():
    action.slide(1060 + math.floor(random() * 11) - 5, 500 + math.floor(random() * 11) - 5,
                 800 + math.floor(random() * 11) - 5, 550 + math.floor(random() * 11) - 5, randint(300, 500))

def swipeBackCount(count):
    for _ in range(count):
        action.slide(1060 + math.floor(random() * 11) - 5, 500 + math.floor(random() * 11) - 5,
                 800 + math.floor(random() * 11) - 5, 550 + math.floor(random() * 11) - 5, randint(300, 500))
        time.sleep(0.2 + random() / 2)


# def swipeBack(to, to2=None):
#     print('swipeBack')
#
#     count = 0
#     time.sleep(2 + random() / 2)
#     while True:
#         x, y = ocrFind(to)
#         if x is not None:
#             if to2 is not None:
#                 x2, y2 = ocrFind(to2)
#                 if x2 is not None:
#                     break
#             else:
#                 break
#         action.slide(1060 + math.floor(random() * 11) - 5, 500 + math.floor(random() * 11) - 5,
#                      800 + math.floor(random() * 11) - 5, 550 + math.floor(random() * 11) - 5, 300 + random() * 200)
#         time.sleep(2 + random() / 2)
#         count += 1
#         if count > 3:
#             return False
#     return True

def swipeBack(to, type='ocr'):
    print('swipeBack')
    x = None
    y = None
    count = 0
    time.sleep(2 + random() / 2)
    while True:
        if type == 'ocr':
            x, y = ocrFind(to)
        elif type == 'desc':
            x, y = descFind(to)
        elif type == 'text':
            x, y = textFind(to)
        if x is not None:
            break
        action.slide(1060 + math.floor(random() * 11) - 5, 500 + math.floor(random() * 11) - 5,
                     800 + math.floor(random() * 11) - 5, 550 + math.floor(random() * 11) - 5, 300 + random() * 200)
        time.sleep(2 + random() / 2)
        count += 1
        if count > 3:
            return False
    return True

def swipeBackApp(to, type='ocr'):
    if swipeBack(to, type) == False:
        print('swipeBackApp fail retry', curApp)
        time.sleep(2)
        action.Key.home()
        time.sleep(2)
        print('swipeBackApp open', curApp)
        system.open(curApp)
        swipeBack(to, type)

def swipeUp(low=0.2, high=0.7):
    size = Device.display()
    width = int(size.widthPixels * 0.5)
    startX = randint(width - 10, width + 10)
    startY = randint(int(size.heightPixels * high) - 10, int(size.heightPixels * high) + 10)
    endX = randint(width + 10, width + 20)
    endY = randint(int(size.heightPixels * low) - 10, int(size.heightPixels * low) + 10)
    # action.slide(500 + randint(0, 100), 1800 + randint(0, 100),
    #              500 + randint(0, 100), 1100 + randint(0, 100), 200 + randint(100, 200))

    # action.slide(startX, startY, startX, startY - 100, randint(95, 105))
    # action.slide(startX, startY-100, startX, startY-300, randint(95, 105))
    # action.slide(startX, startY - 300, startX, endY, randint(95, 105))
    t = randint(200, 220)
    action.slide(startX, startY, endX, endY, t)
    # print('swipe', startX, startY, endX, endY, t)


def swipeDown():
    action.slide(500 + math.floor(random() * 11) - 5, 1300 + math.floor(random() * 11) - 5,
                 500 + math.floor(random() * 11) - 5, 1600 + math.floor(random() * 11) - 5, 200 + randint(0, 100))


def swipes(sec=15):
    left = sec
    for _ in range(sec):
        print('swipes left', left)
        if left <= 0:
            break
        swipeUp()
        time.sleep(2 + random())
        swipeDown()
        time.sleep(2 + random())
        left = left - 4

        if Selector().text('任务已完成').find():
            return


def textFind(text):
    node = Selector().text(text).find()
    if node:
        return node.rect.centerX(), node.rect.centerY()
    else:
        return None, None


def descFind(text):
    node = Selector().desc(text).find()
    if node:
        return node.rect.centerX(), node.rect.centerY()
    else:
        return None, None

def pathFind(text):
    print('pathFind', text)
    node = Selector().path(text).find()
    if node:
        print('pathFind', text, node)
        return node.rect.centerX(), node.rect.centerY()
    else:
        print('pathFind not find', text)
        return None, None
def imageFind(text, confidence=0.9):
    res = FindImages.find_template([R.img(text), ], confidence=confidence)
    if res:
        return res["center_x"], res["center_y"]
    else:
        return None, None

def ocrFindText(text, confidence=0.9):
    # print('ocrFind', text)
    res = Ocr.mlkitocr_v2(None, text)
    if res:
        for r in res:
            print('ocrFindText', r.text, 'end')
            if text is not None:
                # print(r.text)  # 打印出文本
                return r.center_x, r.center_y, r.text
                # print(r['center_x'], r['center_y'])  # 识别范围
                # print(r['confidence'])  # 可信度

    # print('ocrFind not find', text)
    return None, None, None

def ocrFind(text, confidence=0.9):
    x, y, _ = ocrFindText(text, confidence)
    return x,y
def swipe(paras):
    delay = paras['delay']
    count = paras['count']
    for _ in range(count):
        swipeUp()
        time.sleep(delay + randint(0, 20))


def forWait(paras, node):
    delay = paras['delay']
    count = paras['count']
    for _ in range(count):
        time.sleep(delay + randint(0, 20))

def findWaitBack(text, back, type):
    x, y = ocrFind(text)
    if x is not None:
        clickXY(x, y)
        left = randint(WAIT_LOW, WAIT_HIGH)
        print('time',left, 'sleep',text)
        time1 = datetime.now()
        while True:
            swipeUp()
            time.sleep(4 + random())

            time2 = datetime.now()
            time_diff = (time2 - time1).total_seconds()
            # print('等待时间', time_diff)
            if time_diff > left:
                break
        swipeBackApp(back, type)
    return x, y

def extract_first_num_to_int(s: str) -> Optional[int]:
    """
    提取字符串中第一个出现的连续数字段并转为int，无数字返回None
    :param s: 待处理字符串（数字前可能有字母/符号）
    :return: 转换后的整数（成功）/None（失败）
    """
    # 正则匹配：\d+ 匹配1个及以上连续数字；search找任意位置的第一个匹配
    match = re.search(r'\d+', s)
    if not match:
        print(f"字符串 '{s}' 中未找到数字")
        return None

    # 提取数字字符串并转换为int（自动忽略前导0）
    try:
        num_str = match.group()
        return int(num_str)
    except ValueError:
        # 理论上\d+匹配的字符串不会触发此异常，仅做兜底
        print(f"数字字符串 '{num_str}' 转换失败")
        return None
def lookGuangGao(paras, x, y):
    for _ in range(10):
        time.sleep(3 + randint(0, 2))
        if textFind('领取成功'):
            swipeBackOnes()
        else:
            time.sleep(5 + random())


def getJinBi(paras):
    print('getJinBi')
    if 'jinBiPos' not in paras:
        print('getJinBi exit')
        return 0
    jinBiPos = paras['jinBiPos']
    rect = jinBiPos()
    print('getJinBi', jinBiPos, 'rect', rect)

    # res = Ocr(rect=rect).paddleocr_v3()
    res = Ocr.mlkitocr_v2(rect, r'^[1-9]\d*$')
    if res:
        for r in res:
            # print(r)
            print(r.text)  # 打印出文本
            return int(r.text)
            # print(r['center_x'], r['center_y'])  # 识别范围
            # print(r['confidence'])  # 可信度
        print('end')


def lookShortVideo(paras, x, y):
    time.sleep(3)
    print('lookShortVideo')

    before = getJinBi(paras)
    count = 0
    for _ in range(2):
        time.sleep(randint(10, 20))
        after = getJinBi(paras)
        if after is None:
            # time.sleep(5)
            swipeUp()

            continue
        print('lookShortVideo', before, after, count)
        if before == after:
            count += 1
        else:
            before = after
            count = 0
        if count >= 2:
            swipeUp()
            before = getJinBi(paras)

def clickNodeP(paras, x, y):
    clickXY(x, y)


def swipeUpP(paras, node):
    delay = paras['delay']
    delay = randint(delay, delay + 10)
    for _ in range(0, delay, 3):
        time.sleep(randint(3, 5))
        swipeUp()


procList = {}


def register(cfg):
    print('register', cfg)
    procList[cfg['name']] = cfg


def findPath(step, name):
    path = step['path']
    for it in path:
        type, value = it.split(':')
        time.sleep(1+random())
        x,y = findPosSingle(type, value)
        if x is not None:
            clickXY(x, y)
            break
        # if type == 'text':
        #     if findTextAndClick(value, 3):
        #         break
        # if type == 'desc':
        #     if findDescAndClick(value, 3):
        #         break
        # if type == 'image':
        #     if findImageAndClick(name + '/' + value + '.png', 3):
        #         break
        # if type == 'ocr':
        #     x, y = ocrFind(value)
        #     if x is not None:
        #         clickXY(x, y)
        #         break
        swipeUp()


def procSingle(cfgName, check):
    cfg = procList[cfgName]
    print('cfg', cfg, 'check', check)
    app = cfg['app']

    global curApp
    curApp = app

    system.open(app)
    time.sleep(5)

    steps = cfg['step']
    nodes = cfg['node']
    name = cfg['name']
    for i in range(2):

        for step in steps:
            if i < 2 and step['name'] not in check:
                continue
            findPath(step, name)

            find = False

            for _ in range(1):

                nodeList = nodes[step['name']]
                print('nodeList', nodeList)
                for it in nodeList:
                    time.sleep(4+random())
                    x, y = findPos(it, name, step)
                    if x is not None:
                        clickXY(x, y)

                    proc = it['process']
                    print('find node', it['name'], proc)

                    if proc:

                        if 'time' in it:
                            procTime = it['time']
                        else:
                            procTime = 600
                        time1 = datetime.now()
                        while True:
                            time.sleep(2 + random())

                            if proc(it, x, y) == -1:
                                break
                            time2 = datetime.now()
                            time_diff = (time2 - time1).total_seconds()
                            print('procSingle time', time_diff)
                            if time_diff > procTime:
                                break
                        # find = True

                    else:
                        break

    swipeBackCount(5)
                # if find:
                #     break
                # else:
                #     if i < 1:
                #         swipeUp(0.2, 0.5)

def findPosSingle(type, text):
    x = None
    y = None
    if 'text' in type:
        x, y = textFind(text)
    elif 'desc' in type:
        x, y = descFind(text)
    elif 'path' in type:
        x, y = pathFind(text)
    # elif 'image' == type:
    #     print(step['name'] + '/' + it['image'])
    #     x, y = imageFind(name + '/' + it['image'] + '.png')
    elif 'ocr' in type:
        for _ in range(2):
            text = text.replace('\\\\', '\\')
            x, y = ocrFind(r'' + text)
            print('findPos', text, x)
            if x is not None:
                return x, y
        ocrFindText(None)
    return x, y

def findPos(it, name, step):
    x = None
    y = None
    swipeDown()
    time.sleep(3)

    for _ in range(2):
        if 'text' in it:
            x, y = findPosSingle('text', it['text'])
        elif 'desc' in it:
            x, y = findPosSingle('desc',it['desc'])
        elif 'path' in it:
            x, y = findPosSingle('path',it['path'])
        elif 'image' in it:
            print(step['name'] + '/' + it['image'])
            x, y = imageFind(name + '/' + it['image'] + '.png')
        elif 'ocr' in it:
            for _ in range(2):
                text = it['ocr'].replace('\\\\','\\')
                x, y = findPosSingle('ocr', r''+text)
                print('findPos', text, x)
                if x is not None:
                    return x, y
            ocrFindText(None)
                # else :
                #     swipeUp(0.2, 0.6)
                #     time.sleep(2)
        else:
            return None, None
        if x is not None:
            break
        else:
            swipeUp(0.2, 0.5)
            time.sleep(3)
    print('findPos', it, x, y)
    return x, y


def process(check):
    # jinBiPos = textFind('立即领取')
    # rect = jinBiPos.rect
    # print('jinBiPos', jinBiPos, 'rect', rect)
    # print(rect.width() + 100, rect.height() + 100)
    #
    # rectTmp = [rect.left - 100, rect.top - 300, rect.left + rect.width(), rect.top + rect.height() + 100]
    # res = Ocr().paddleocr_v3()
    # if res:
    #     for r in res:
    #         # print(r)
    #         print(r.text)  # 打印出文本
    #         # print(r['rect'])  # 范围
    #         # print(r['center_x'], r['center_y'])  # 识别范围
    #         # print(r['confidence'])  # 可信度
    #     print('end')
    # while True:
    #     swipeUp()
    #     time.sleep(randint(60, 100))

    print(procList, check)
    for _ in range(10):
        for cfg in procList:
            print('cfg', cfg, 'check', check)
            if cfg in check:
                procSingle(cfg, check[cfg])
