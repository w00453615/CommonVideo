import time
from random import randint

from ascript.android import action
from ascript.android.action import click

from ..util import swipeUp, swipe, register, forWait, clickNodeP, lookGuangGao, lookShortVideo, clickNode, clickXY, \
    findImageAndClick, imageFind, descFind, swipeBack
from ascript.android.screen import capture, FindColors, FindImages, Ocr
from ascript.android.system import R


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

step = [
    {'name': '看视频', "path": ['text:视频']},
    # {'name': '赚钱', "path": ['image:赚钱']}

]

node = {
    # "赚钱": [
    #     {'name':'广告',"image": "看广告赚金币", "process": lookXiFanGuangGao, "delay": 0, 'count': 0},
    #     {'name':'逛街赚钱',"desc": "逛街赚钱", "process": None, "delay": 0, 'count': 0}
    # ],
    "看视频": [
        {'name':'看视频',"text": "视频", "process": lookShortVideo, "delay": 0, "time": 600, 'count': 0, 'jinBiPos': jinBiPos}
    ]
}

cfg = {
    "app": "com.baidu.searchbox.lite",
    'name': '百度',
    "step": step,
    "node": node
}
