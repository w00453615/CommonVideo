import re
import time
from datetime import datetime
from random import randint, random
from typing import Optional

from ascript.android import action, system
from ascript.android.action import click

from ..util import swipeUp, swipe, register, forWait, clickNodeP, lookGuangGao, lookShortVideo, clickNode, clickXY, \
    findImageAndClick, imageFind, descFind, swipeBack, ocrFind, swipeBackOnes, ocrFindText, swipeBackApp, WAIT_LOW, \
    WAIT_HIGH, findWaitBack, extract_first_num_to_int, findText, findDesc
from ascript.android.screen import capture, FindColors, FindImages, Ocr
from ascript.android.system import R

def preproc():
    x, y = ocrFind("签到领")
    print('签到领', x)
    if x is not None:
        clickXY(x, y)
        time.sleep(2)
        x, y, text = ocrFindText("看广告")
        if x is not None:
            clickXY(x, y)
            lookDouyinGuangGaoOnes()

        x, y = ocrFind("签到领")
        print('签到领', x)
        if x is not None:
            clickXY(x, y)
            time.sleep(2)

            x, y, text = ocrFindText("看广告")
            if x is not None:
                clickXY(x, y)
                lookDouyinGuangGaoOnes()

def jinBiPos():
    print("金币位置检测")
    res = FindImages.find_template([R.img("抖音极速版/金币.png"), ], confidence=0.7)
    if res:
        print("找到金币了", res)
    else:
        print("没找到金币")

    return [880, 420, 1048, 588]

# def procTwice(proc, text):
#     for i in range(2):
#         time.sleep(3 + random())
#         if i == 1 and proc(text) == False:

count = 0

def swipeBackAppDouYinGuangGao():
    swipeBackApp('秒后|领取成功', 'desc')

def swipeBackAppDouYinShouYe():
    swipeBackApp('首页', 'desc')

def lookDouyinGuangGaoOnes():
    global count
    # ocrFind('看广告赚金币')
    time.sleep(5+random())
    text = findDesc("秒后")
    print('秒后可领奖励', text)
    if text is not None:
        procKeyword()
    else:
        t = randint(WAIT_LOW, WAIT_HIGH)
        print('自动进入活动 等待', t)
        time.sleep(t)
        swipeBackAppDouYinGuangGao()

    time.sleep(3+random())
    x, y = ocrFind("继续观看")
    print('继续观看', x)
    if x is not None:
        clickXY(x, y)

    time.sleep(3 + random())
    text = findDesc("秒后")
    print('秒后可领奖励', text)
    if text is not None:
        leftStr = extract_first_num_to_int(text)
        if leftStr is not None:
            left = min(30, int(leftStr))
            print('秒后可领奖励 等待', left)

            time.sleep(left+2+random())

    time.sleep(2 + random())

    text = findDesc('领取成功', 0.8)
    print('领取成功', text)
    if text is not None:
        swipeBackOnes()
        time.sleep(2)

    time.sleep(2 + random())
    x, y = ocrFind("领取奖励")
    print('领取奖励',x)
    if x is not None:
        clickXY(x, y)
        time.sleep(2)
        count = 0
        return 0

    time.sleep(2 + random())
    x, y = ocrFind('评论|评价|赚钱任务')
    print('评论并收下金币', x)
    if x is not None:
        clickXY(x, y)
        time.sleep(randint(5, 10))
        swipeBackAppDouYinShouYe()
        return -1
    else:
        ocrFindText(None)

    text = findText('看视频赚超多钱')
    if text is not None:
        swipeBackAppDouYinShouYe()
        return -1

    text = findText('首页')
    if text is not None:
        return -1

    print('lookDouyinGuangGaoOnes count', count)
    if count == 2:
        count = 0
        # system.open('com.ss.android.ugc.aweme.lite')
        swipeBackAppDouYinShouYe()
        print('啥也没干，退出')

        return -1
    else :
        count = count + 1
        return 0

def procKeyword():
    keyword = list()
    keyword.append('点击')
    keyword.append('打开')
    keyword.append('下载')
    keyword.append('充值')
    keyword.append('购买')
    keyword.append('优惠')
    keyword.append('美食')
    keyword.append('更多')
    keyword.append('了解')
    keyword.append('抢购')
    keyword.append('详情')
    keyword.append('查看')
    keyword.append('直播间')
    keyword.append('立即')
    keyword.append('一键')
    keyword.append('速来')
    keyword.append('抢先')
    for it in keyword:
        x, _ = findWaitBack(it, '秒后|领取成功', 'desc')
        if x is not None:
            break
    swipeBackAppDouYinGuangGao()


def lookDouyinGuangGao(paras, x, y):
    preproc()
    return lookDouyinGuangGaoOnes()

def lookBaoXiang(paras, x, y):
    preproc()

    time.sleep(2+random())
    x, y, text = ocrFindText("看广告")
    if x is not None:
        clickXY(x, y)

    return lookDouyinGuangGaoOnes()

step = [
    {'name': '看视频', "path": []},
    {'name': '看广告', "path": ['path:/FrameLayout/ViewGroup/FrameLayout/ImageView']},#打开赚钱
    {'name': '看视频赚超多钱', "path": ['path:/FrameLayout/ViewGroup/FrameLayout/ImageView']},
    {'name': '跑任务', "path": []},
    {'name': '开宝箱', "path": ['path:/FrameLayout/ViewGroup/FrameLayout/ImageView']}
]

node = {
    "看广告": [
        {'name':'广告',"desc": "指定视频任务", "process": lookDouyinGuangGao, "time": 6000, 'count': 0}
    ],
    "开宝箱": [
        {'name':'开宝箱',"ocr": "开宝箱得金币|点击领", "process": lookBaoXiang, "time": 6000, "delay": 0, 'count': 0}
    ],
    "看视频赚超多钱": [
        {'name':'看视频赚超多钱',"ocr": "立即领取", "process": lookBaoXiang, "delay": 0, 'count': 0}
    ],
    "跑任务": [
        {'name':'跑任务',"process": lookBaoXiang, "time": 6000, "delay": 0, 'count': 0}
    ],
    "看视频": [
        {'name':'看视频',"text": "首页", "process": lookShortVideo, "time": 600, 'count': 0, 'jinBiPos': jinBiPos}
    ]
}

cfg = {
    "app": "com.ss.android.ugc.aweme.lite",
    'name': '抖音极速版',
    "step": step,
    "node": node
}
