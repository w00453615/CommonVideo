import re
import time
from datetime import datetime
from random import randint, random
from typing import Optional

from ascript.android import action, system
from ascript.android.action import click

from ..util import swipeUp, swipe, register, forWait, clickNodeP, lookGuangGao, lookShortVideo, clickNode, clickXY, \
    findImageAndClick, imageFind, descFind, swipeBack, ocrFind, swipeBackOnes, ocrFindText, swipeBackApp, WAIT_LOW, \
    WAIT_HIGH, findWaitBack, extract_first_num_to_int, findText, findDesc, swipeDown
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
    time.sleep(5 + random())
    text = findDesc("秒后")
    print('秒后可领奖励', text)
    if text is not None:
        procKeyword()
    else:
        t = randint(WAIT_LOW, WAIT_HIGH)
        print('自动进入活动 等待', t)
        time.sleep(t)
        swipeBackAppDouYinGuangGao()

    time.sleep(3 + random())
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

            time.sleep(left + 2 + random())

    time.sleep(2 + random())

    text = findDesc('领取成功', 0.8)
    print('领取成功', text)
    if text is not None:
        swipeBackOnes()
        time.sleep(2)

    time.sleep(2 + random())
    x, y = ocrFind("领取奖励")
    print('领取奖励', x)
    if x is not None:
        clickXY(x, y)
        time.sleep(2)
        count = 0
        return 0

    time.sleep(2 + random())
    x, _ = ocrFind('评论')
    x1, _ = ocrFind('评价')
    x2, _ = ocrFind('赚钱任务')
    print('评论并收下金币', x, x1, x2)
    if x is not None or x1 is not None or x2 is not None:
        time.sleep(randint(5, 10))
        swipeBackAppDouYinShouYe()
        return -1
    else:
        ocrFindText(None)

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
    else:
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

    time.sleep(2 + random())
    x, y, text = ocrFindText(r"看广告再")
    print('看广告再', x, y)
    if x is not None:
        clickXY(x, y)
    else:
        ocrFindText(None)

    return lookDouyinGuangGaoOnes()


def zhiding(paras, x, y):
    print('zhiding')
    time.sleep(2 + random())
    x, y, text = ocrFindText(r"看指定")
    print('看指定', x, y)
    if x is not None:
        clickXY(x, y)

    x, y, text = ocrFindText(r"支付积分")
    print('支付积分', x, y)
    if x is not None:
        return -1

    return lookDouyinGuangGaoOnes()


def qiandao(paras, x, y):
    print('qiandao')

    x, y = descFind("今日待打卡")
    print('今日待打卡', x, y)
    if x is not None:
        clickXY(x, y)
        time.sleep(2)
    else:
        return -1

    x, y = ocrFind("完成打卡")
    print('完成打卡', x, y)
    clickXY(x, y)
    time.sleep(2)

    x, y = ocrFind("指定视频")
    print('指定视频', x, y)
    clickXY(x, y)
    time.sleep(2)

    text = findDesc("后可完成任务")
    if text is not None:
        leftStr = extract_first_num_to_int(text)
        if leftStr is not None:
            left = min(30, int(leftStr))
            print('秒后可领奖励 等待', left)

            time.sleep(left + 2 + random())
    else:
        time.sleep(randint(30, 35))
    swipeBackApp('首页', 'text')

    return -1


def guangjie(paras, x, y):
    text = findDesc('15/15')
    if text is not None:
        return -1

    x, y, text = ocrFindText(r"看广告再")
    print('看广告再', x, y)
    if x is not None:
        clickXY(x, y)

    time1 = datetime.now()
    i = 0
    while True:
        i = i + 1
        if i % 4 == 0:
            swipeDown()
        else:
            swipeUp()
        time.sleep(4 + random())

        time2 = datetime.now()
        time_diff = (time2 - time1).total_seconds()
        # print('等待时间', time_diff)
        if time_diff > 90:
            break
        swipeDown()
        time.sleep(2 + random())
    swipeBackApp('首页', 'text')
    return -1

def chifandaka(paras, x, y):
    time.sleep(2 + random())
    x, y = ocrFind("赚钱任务")
    if x is not None:
        print('赚钱任务', x)
        return -1
    
    x, y = ocrFind("看指定视频")
    if x is not None:
        print('看指定视频', x)
        clickXY(x, y)

    return lookDouyinGuangGaoOnes()

def double(paras, x, y):
    x, y = ocrFind("赚钱任务")
    if x is not None:
        return -1

    for _ in range(5):
        lookShortVideo(paras, x, y, 16, 18)

    swipeBackOnes()
    time.sleep(2)
    x, y = ocrFind("坚持")
    print('坚持', x)
    if x is not None:
        clickXY(x, y)
        return -1

    time.sleep(2)
    x, y = ocrFind("退出")
    print('退出', x)
    if x is not None:
        clickXY(x, y)
    return -1


step = [
    {'name': '看视频', "path": []},
    {'name': '看广告', "path": ['id:com.ss.android.ugc.aweme.lite:id/kd']},  # 打开赚钱
    # {'name': '看视频赚超多钱', "path": ['path:/FrameLayout/ViewGroup/FrameLayout/FrameLayout']},
    {'name': '看视频赚超多钱', "path": ['id:com.ss.android.ugc.aweme.lite:id/kd']},
    {'name': '跑任务', "path": []},
    {'name': '签到', "path": ['id:com.ss.android.ugc.aweme.lite:id/kd']},
    {'name': '逛街', "path": ['id:com.ss.android.ugc.aweme.lite:id/kd']},
    {'name': '双倍奖励', "path": ['id:com.ss.android.ugc.aweme.lite:id/kd']},
    {'name': '指定视频', "path": ['id:com.ss.android.ugc.aweme.lite:id/kd']},
    {'name': '吃饭打卡', "path": ['id:com.ss.android.ugc.aweme.lite:id/kd']},
    {'name': '开宝箱', "path": ['id:com.ss.android.ugc.aweme.lite:id/kd']}
]

node = {
    "看广告": [
        {'name': '广告', "desc": "指定视频任务|广告任务", "process": lookDouyinGuangGao, "time": 1200, 'count': 0}
    ],
    "开宝箱": [
        {'name': '开宝箱', "ocr": "开宝箱得金币|点击领", "process": lookBaoXiang, "time": 1200, "delay": 0, 'count': 0}
    ],
    "看视频赚超多钱": [
        {'name': '看视频赚超多钱', "ocr": "立即领取", "process": lookBaoXiang, "delay": 0, 'count': 0}
    ],
    "跑任务": [
        {'name': '跑任务', "process": lookBaoXiang, "time": 6000, "delay": 0, 'count': 0}
    ],
    "逛街": [
        {'name': '跑任务', "desc": "浏览低价", "process": guangjie, "time": 1, "delay": 0, 'count': 0}
    ],
    "吃饭打卡": [
        {'name': '吃饭打卡', "desc": "打卡领吃饭补贴", "process": chifandaka, "time": 600, "delay": 0, 'count': 0}
    ],
    "看视频": [
        {'name': '看视频', "process": lookShortVideo, "time": 600, 'count': 0}
    ],
    "双倍奖励": [
        {'name': '看视频', "desc": "双重奖励", "process": double, "time": 600, 'count': 0}
    ],
    "指定视频": [
        {'name': '看视频', "desc": "做任务最高", "process": zhiding, "time": 600, 'count': 0}
    ],
    "签到": [
        {'name': '签到', "process": qiandao, "time": 1, 'count': 0}
    ]
}

cfg = {
    "app": "com.ss.android.ugc.aweme.lite",
    'name': '抖音极速版',
    "step": step,
    "node": node
}
