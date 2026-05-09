import time
from random import randint

from ascript.android import action
from ascript.android.action import click

from ..util import swipeUp, swipe, register, forWait, clickNodeP, lookGuangGao, lookShortVideo, clickNode, clickXY, \
    findImageAndClick, imageFind, descFind, swipeBack, findDesc, textFind, swipeBackApp, ocrFind
from ascript.android.screen import capture, FindColors, FindImages, Ocr
from ascript.android.system import R
from ascript.android.node import Selector


def jinBiPos():
    print("金币位置检测")
    res = FindImages.find_template([R.img("抖音极速版/金币.png"), ], confidence=0.7)
    if res:
        print("找到金币了", res)
    else:
        print("没找到金币")

    return [880, 420, 1048, 588]

def lookXiFanGuangGao(paras, x, y):
    clickXY(x, y)
    time.sleep(randint(35, 50))

    action.Key.back()
    # 点击继续观看
    while True:
        if findImageAndClick("抖音极速版/评论并收下金币.png", 1) is not None:
            time.sleep(randint(5, 10))
            if findImageAndClick("抖音极速版/看广告赚金币.png", 1) is not None:
                break

        if findImageAndClick("抖音极速版/领取奖励.png", 1) is not None:
            continue
        if findImageAndClick("抖音极速版/继续观看.png", 1)is not None:
            continue
        if findImageAndClick("抖音极速版/立即打开.png", 1)is not None:
            time.sleep(randint(35, 50))
            swipeBack('领取成功')
            action.Key.back()
            continue
        if findImageAndClick("抖音极速版/立即下载.png", 1)is not None:
            time.sleep(randint(35, 50))
            swipeBack('领取成功')
            action.Key.back()
            continue

        if descFind('领取成功'):
            action.Key.back()
            continue

        time.sleep(randint(35, 50))
        action.Key.back()


def qiandao(paras, x, y):
    print('qiandao')

    time.sleep(2)
    node = Selector().text("去观看").find_all()[-1]
    
    print('qiandao 去观看', node)
    if node is not None:
        clickNode(node)

    time.sleep(2)
    x, y = textFind('广告完成任务')
    print('qiandao 广告完成任务', x)
    if x is not None:
        clickXY(x, y)
    else:
        return -1
    time.sleep(1)
    x, y = textFind('去看广告')
    print('qiandao 去看广告', x)
    if x is not None:
        clickXY(x, y)

    time.sleep(randint(30, 35))
    swipeBackApp('去观看', 'text')
    return 0

def qiandaoshipin(paras, x, y):
    print('qiandaoshipin')

    #看视频xxxxxxxxxxxx

    x, y = ocrFind("去观看")
    print('完成去观看打卡', x, y)
    clickXY(x, y)
    time.sleep(2)

def stopProcess():
    print('stopProcess')
    swipeBackApp('首页', 'text')
 

step = [
    {'name': '看视频', "path": []},
    {'name': '签到', "display":"Falsee", "path": ['id:com.smile.gifmaker:id/kem_task_pendant_new', 'text:连续打卡白拿手机']},
    {'name': '签到视频', "display":"True", "path": ['id:com.smile.gifmaker:id/kem_task_pendant_new', 'text:今日待打卡']}
]

node = {
    # "赚钱": [
    #     {'name':'广告',"image": "看广告赚金币", "process": lookXiFanGuangGao, "delay": 0, 'count': 0},
    #     {'name':'逛街赚钱',"desc": "逛街赚钱", "process": None, "delay": 0, 'count': 0}
    # ],
    "看视频": [
        {'name':'看视频',"text": "精选", "process": lookShortVideo, "delay": 0, 'count': 0, 'jinBiPos': jinBiPos}
    ],
    "签到": [
        {'name':'签到',"process": qiandao, 'stop': stopProcess, "time": 300, 'count': 0}
    ],
    "签到视频": [
        {'name': '签到视频', "text": "连续打卡白拿手机", "process": qiandaoshipin, "time": 600, 'count': 0}
    ]
}

cfg = {
    # "app": "com.kuaishou.nebula",
    "app": "com.smile.gifmaker",
    'name': '快手',
    "step": step,
    "node": node
}
