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
from ascript.android.ui import Dialog


import math
import time

curApp = None
WAIT_LOW = 30
WAIT_HIGH = 35

def clickNode(node):
    centerX = node.rect.centerX() + math.floor(random() * 11) - 5
    centerY = node.rect.centerY() + math.floor(random() * 11) - 5
    print(centerX, centerY)
    click(centerX, centerY)

def clickXY(x, y, delta = 5):
    centerX = randint(x-delta, x+delta)
    centerY = randint(y-delta, y+delta)
    # print(centerX, centerY)
    click(centerX, centerY)

def findDescAndClick(keyword, delay=5):
    print(f'findDescAndClick {keyword}')
    for _ in range(delay):
        node = Selector().desc(keyword).find()
        if node:
            clickNode(node)

            return node
        else:
            time.sleep(2)
    print(f'findDescAndClick exit {keyword}')
    return None


def findPathAndClick(keyword, delay=5):
    print(f'findPathAndClick {keyword}')
    for _ in range(delay):
        node = Selector().path(keyword).find()
        if node:
            clickNode(node)
            return node
        else:
            time.sleep(2)

    print(f'findPathAndClick exit {keyword}')
    return None


def findTextAndClick(keyword, delay=5):
    print(f'findTextAndClick {keyword}')
    for _ in range(delay):
        node = Selector().text(keyword).find()

        if node:
            clickNode(node)

            return node
        else:
            time.sleep(2)
    print(f'findTextAndClick exit {keyword}')
    return None

def findText(keyword, delay=5, index=0):
    print(f'findText {keyword}')
    keyword = keyword.replace('\\\\', '\\')
    for _ in range(delay):
        if index == 0:
            node = Selector().text(keyword).find()
        else:
            all = Selector().text(keyword).find_all()
            # print(f'findTextAll {all}')
            if all is None:
                return None
            elif len(all) <= index:
                node = all[0]
            else:
                node = all[index]

        if node:
            print(f'findText end {node.text}')
            return node.text
        else:
            time.sleep(2)
    print(f'findText exit {keyword}')
    return None

def findDesc(keyword, delay=5):
    print(f'findDesc {keyword}')
    for _ in range(2):
        node = Selector().desc(keyword).find()

        if node:
            print(f'findDesc end {node.desc}')
            return node.desc
        else:
            time.sleep(2)
    print(f'findDesc error {keyword}')
    return None

def findImageAndClick(keyword, delay=5):
    print(f'findImageAndClick {keyword}')
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
    print(f'findImageAndClick exit {keyword}')
    return None


def findTextEndAndClick(keyword, end, delay=5):
    print(f'findTextEndAndClick {keyword}')
    for _ in range(delay):
        node = Selector().text(keyword).find()

        if node:
            clickNode(node)
            print(f'findTextEndAndClick1 end {node}')
            return node
        else:
            time.sleep(2)

        node2 = Selector().text(end).find()
        if node2:
            print(f'findTextEndAndClick2 end {node2}')
            return node
    print(f'findTextEndAndClick exit {keyword}')
    return None


def swipeBackOnes():
    d = Device.display()
    weight = d.widthPixels
    action.slide(weight - 2 - math.floor(random() * 5), 500 + math.floor(random() * 11) - 5,
                 weight - 260 + math.floor(random() * 11) - 5, 550 + math.floor(random() * 11) - 5,
                 300 + random() * 200)
def swipeBackCount(count):
    for _ in range(count):
        d = Device.display()
        weight = d.widthPixels
        action.slide(weight - 2 - math.floor(random() * 5), 500 + math.floor(random() * 11) - 5,
                     weight - 260 + math.floor(random() * 11) - 5, 550 + math.floor(random() * 11) - 5,
                     300 + random() * 200)
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
    # print('swipeBack')
    x = None
    y = None
    count = 0
    time.sleep(1 + random() / 2)

    while True:
        if type == 'ocr':
            x, y = ocrFind(to)
        elif type == 'desc':
            x, y = descFind(to)
        elif type == 'text':
            x, y = textFind(to)
        if x is not None:
            break
        d = Device.display()
        weight = d.widthPixels
        action.slide(weight - 2 - math.floor(random() * 5), 500 + math.floor(random() * 11) - 5,
                     weight - 260 + math.floor(random() * 11) - 5, 550 + math.floor(random() * 11) - 5,
                     300 + random() * 200)

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
    print(f'swipeUp {startX}, {startY}, {endX}, {endY}, {t}')


def swipeDown(low=0.2, high=0.7):
    size = Device.display()
    width = int(size.widthPixels * 0.5)
    startX = randint(width - 10, width + 10)
    endY = randint(int(size.heightPixels * high) - 10, int(size.heightPixels * high) + 10)
    endX = randint(width + 10, width + 20)
    startY = randint(int(size.heightPixels * low) - 10, int(size.heightPixels * low) + 10)
    # action.slide(500 + randint(0, 100), 1800 + randint(0, 100),
    #              500 + randint(0, 100), 1100 + randint(0, 100), 200 + randint(100, 200))

    # action.slide(startX, startY, startX, startY - 100, randint(95, 105))
    # action.slide(startX, startY-100, startX, startY-300, randint(95, 105))
    # action.slide(startX, startY - 300, startX, endY, randint(95, 105))
    t = randint(200, 220)
    action.slide(startX, startY, endX, endY, t)
    print(f'swipeDown {startX}, {startY}, {endX}, {endY}, {t}')


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
    text = text.replace('\\\\', '\\')
    node = Selector().text(text).find()
    if node:
        return node.rect.centerX(), node.rect.centerY()
    else:
        return None, None

def idFind(text):
    node = Selector().id(text).find()
    if node:
        return node.rect.centerX(), node.rect.centerY()
    else:
        return None, None

def descFind(text):
    text = text.replace('\\\\', '\\')
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
    res = Ocr.mlkitocr_v2(None, pattern=text)
    if res:
        for r in res:
            # print(f'ocrFindText {r.text} end')
            if text is not None:
                # print(r.text)  # 打印出文本
                return r.center_x, r.center_y, r.text
                # print(r['center_x'], r['center_y'])  # 识别范围
                # print(r['confidence'])  # 可信度

    # print('ocrFind not find', text)
    return None, None, None

def ocrFindTextPad(text, confidence=0.9):
    # print('ocrFind', text)
    res = Ocr.paddleocr(None, pattern=text)
    if res:
        for r in res:
            print(f'ocrFindText {r.text} end')
            if text is not None:
                # print(r.text)  # 打印出文本
                return r.center_x, r.center_y, r.text
                # print(r['center_x'], r['center_y'])  # 识别范围
                # print(r['confidence'])  # 可信度

    # print('ocrFind not find', text)
    return None, None, None

def ocrFindTextRect(text, confidence=0.9):
    # print('ocrFind', text)
    res = Ocr.mlkitocr_v2(None, text)
    if res:
        for r in res:
            print('ocrFindText', r.text, 'end')
            if text is not None:
                # print(r.text)  # 打印出文本
                return r.center_x, r.center_y, r.rect
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
    # print('getJinBi')
    if 'jinBiPos' not in paras:
        # print('getJinBi exit')
        return 0
    jinBiPos = paras['jinBiPos']
    rect = jinBiPos()
    # print('getJinBi', jinBiPos, 'rect', rect)

    # res = Ocr(rect=rect).paddleocr_v3()
    res = Ocr.mlkitocr_v2(rect, r'^[1-9]\d*$')
    if res:
        for r in res:
            # print(r)
            print(r.text)  # 打印出文本
            return int(r.text)
            # print(r['center_x'], r['center_y'])  # 识别范围
            # print(r['confidence'])  # 可信度
        # print('end')


def lookShortVideo(paras, x, y, low = 4, up = 5):
    time.sleep(3)

    before = getJinBi(paras)
    count = 0
    for _ in range(2):
        time.sleep(randint(low, up))
        after = getJinBi(paras)
        if after is None:
            # time.sleep(5)
            swipeUp(0.2,0.6)

            continue
        # print(f'lookShortVideo {before} {after} {count}')
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
    # print('register', cfg)
    procList[cfg['name']] = cfg


def findPath(step, name):
    path = step['path']
    if len(path) == 0:
        return True
    for it in path:
        type, value = it.split(':',1)
        print(f'findPath1 {it} name {name} type {type} value {value}')
        time.sleep(2+random())
        
        find = False
        for _ in range(4):
            x,y = findPosSingle(type, value)
            if x is not None:
                print(f'findPath3 found {it} {name} x {x} y {y} find {find}')
                clickXY(x, y)
                find = True
                break
            
            # if i == 0:
            #     for _ in range(4):
            #         swipeDown()
            #         time.sleep(2+random())

            swipeUp(0.2, 0.6)
            time.sleep(2+random())
        print(f'findPath4 {type} {value} find {find}')
        if not find:
            print(f'findPath {type} {value} not found')
            # for _ in range(4):
            #     swipeDown(0.2, 0.7)
            #     time.sleep(0.5+random())
            return False
    return True

        


def procSingle(cfgName, check):
    cfg = procList[cfgName]
    app = cfg['app']

    global curApp
    curApp = app

    system.open(app)
    time.sleep(4)

    steps = cfg['step']
    nodes = cfg['node']
    name = cfg['name']
    for i in range(1):

        for step in steps:
            if i < 2 and step['name'] not in check:
                continue

            print(f'procSingle {cfgName} {step["name"]}')
            if not findPath(step, step['name']):
                print(f'procSingle {cfgName} {step["name"]} not found')
                callStopCallbacks(nodes, step['name'])
                continue

            find = False

            for _ in range(1):

                nodeList = nodes[step['name']]
                print(f'nodeList {nodeList}')
                for it in nodeList:
                    proc = it['process']
                    print(f'find node {it["name"]} proc {proc}')

                    if proc:

                        if 'time' in it:
                            procTime = it['time']
                        else:
                            procTime = 600
                        time1 = datetime.now()
                        while True:
                            time.sleep(2 + random())
                            # Dialog.toast(it["name"],3000)
                            if proc(it, None, None) == -1:
                                break
                            time2 = datetime.now()
                            time_diff = (time2 - time1).total_seconds()
                            print(f'procSingle {proc} time {time_diff}')
                            if time_diff > procTime:
                                break

                    else:
                        break
                    callStopCallbacks(nodes, step['name'])

def callStopCallbacks(nodes, step_name):
    if step_name in nodes:
        nodeList = nodes[step_name]
        for it in nodeList:
            if 'stop' in it and callable(it['stop']):
                print(f'calling stop callback for {it["name"]}')
                it['stop']()

def findPosSingle(type, text):
    x = None
    y = None
    print(f'findPosSingle {type} {text}')
    if 'text' == type:
        x, y = textFind(text)
    elif 'desc' == type:
        x, y = descFind(text)
    elif 'path' == type:
        x, y = pathFind(text)
    elif 'id' == type:
        x, y = idFind(text)
    # elif 'image' == type:
    #     print(step['name'] + '/' + it['image'])
    #     x, y = imageFind(name + '/' + it['image'] + '.png')
    elif 'ocr' == type:
        text = text.replace('\\\\', '\\')
        x, y = ocrFind(r'' + text)
        # print(f'findPosSingle xy {x} {y}')
        if x is not None:
            return x, y
    elif 'rightocr' == type:
        text = text.replace('\\\\', '\\')
        resList = Ocr.mlkitocr_v2(pattern=r'' + text)
        for res in resList:
            x, y = res.rect[2]-20, res.center_y
            print(f'findPosSingle rightocr {text} x {x} y {y} rect {res.rect} ')
            if x is not None:
                return x, y
            # else:
            #     x, y, _ = ocrFindTextPad(r'' + text)
            #     print(f'findPosSingle rightocrPad {text} x {x} y {y} rect {res["rect"]} ')
            #     if x is not None:
            #         return x, y
    return x, y

def findPos(it, name, step):
    x = None
    y = None
    time.sleep(3)
    print(f'findPos {it} step {step}')

    for _ in range(4):
        if 'text' in it:
            x, y = findPosSingle('text', it['text'])
        elif 'desc' in it:
            x, y = findPosSingle('desc',it['desc'])
        elif 'path' in it:
            x, y = findPosSingle('path',it['path'])
        elif 'id' in it:
            x, y = findPosSingle('path',it['id'])
        elif 'image' in it:
            print(f'findPos {step["name"]} {it["image"]}')
            x, y = imageFind(name + '/' + it['image'] + '.png')
        elif 'ocr' in it:
            for _ in range(2):
                text = it['ocr'].replace('\\\\','\\')
                x, y = findPosSingle('ocr', r''+text)
                print(f'findPos {text} {x} {y}')
                if x is not None:
                    return x, y
            # ocrFindText(None)
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
    print(f'findPos {it["name"]} {x} {y}')
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
    Ocr.set_engine("mlkit")
    print(f'process {check}')
    for _ in range(100):
        for cfg in procList:
            # print('cfg', cfg, 'check', check)
            if cfg in check:
                procSingle(cfg, check[cfg])
