import time
from random import randint, random

from ascript.android import action
from ascript.android.action import click

from ..util import swipeUp, swipe, register, forWait, clickNodeP, lookGuangGao, lookShortVideo, clickNode, clickXY, \
    findImageAndClick, imageFind, descFind, swipeBack, ocrFind, swipeBackApp, ocrFindText, extract_first_num_to_int, \
    swipeBackOnes, findWaitBack, findTextAndClick, findText, textFind
from ascript.android.screen import capture, FindColors, FindImages, Ocr
from ascript.android.system import R

WAIT_LOW = 20
WAIT_HIGH = 30

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
def procKeyword():
    keyword = list()
    keyword.append('点击')
    keyword.append('立即')
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
    keyword.append('领金币')
    keyword.append('放弃')
    for it in keyword:
        x, _ = findWaitBack(it, 's后|已成功', 'text')
        if x is not None:
            break

def lookGuangGaoOnes(paras, x, y):
    time.sleep(3 + random())
    x, y = ocrFind('看视频最高')
    print('看视频最高', x)
    if x is not None:
        time.sleep(2 + random())
        clickXY(x, y)

    time.sleep(12 + random())
    text = findText("s后")
    print('s后', text)
    if text is not None:
        procKeyword()
    else:
        t = randint(WAIT_LOW, WAIT_HIGH)
        print('自动进入活动 等待', t)
        time.sleep(t)
        swipeBackOnes()


    time.sleep(3 + random())
    x, y = textFind("继续观看|换个|翻倍")
    print('继续观看', x)
    if x is not None:
        clickXY(x, y)

    time.sleep(2 + random())
    x, y = ocrFind("放弃")
    print('放弃', x)
    if x is not None:
        clickXY(x, y)
    time.sleep(2)

    time.sleep(3 + random())
    text = findText("s后")
    print('s后', text)
    if text is not None:
        leftStr = extract_first_num_to_int(text)
        if leftStr is not None:
            left = min(30, int(leftStr))
            print('秒后可领奖励 等待', left)

            time.sleep(left+2+random())

    time.sleep(2 + random())

    text = findText("已成功")
    print('已成功', text)
    if text is not None:
        swipeBackOnes()
        time.sleep(2)

    # time.sleep(2)
    # x, y = textFind("立即")
    # print('立即', x)
    # if x is not None:
    #     clickXY(x, y)

    time.sleep(2 + random())
    x, y = textFind("(立即领取|看视频|立即打开|立即下载|立即完成)")
    print('立即领取1', x)
    if x is not None:
        clickXY(x, y)
        time.sleep(2 + random())
        x, y = textFind("(立即领取|看视频|立即打开|立即下载|立即完成)")
        print('立即领取2', x)
        if x is not None:
            swipeBackOnes()
            time.sleep(2 + random())
            x, y = textFind("换个任务")
            print('换个任务', x)
            if x is not None:
                clickXY(x, y)
            return 0
        else:
            return 0
    time.sleep(2)

    text = findText('领现金|托盘')
    print('领现金', text)
    if text is not None:
        time.sleep(randint(5, 10))
        swipeBackApp('金币(凌晨自动兑现)', 'text')
        return -1
    else:
        ocrFindText(None)

    swipeBackApp('金币(凌晨自动兑现)', 'text')
    print('啥也没干，退出')
    return 0

def lingJinBi(paras, x, y):
    time.sleep(randint(2, 5))
    x, y = ocrFind(r'领(\d+)金币')
    if x is not None:
        time.sleep(2 + random())
        clickXY(x, y)
        return -1
    lookGuangGaoOnes(paras, x, y)

step = [
    {'name': '看视频', "path": []},
    {'name': '看视频翻倍', "path": ['ocr:福利|点击领取']},
    {'name': '领金币', "path": ['ocr:福利|点击领取']},

]

node = {
    # "赚钱": [
    #     {'name':'广告',"image": "看广告赚金币", "process": lookXiFanGuangGao, "delay": 0, 'count': 0},
    #     {'name':'逛街赚钱',"desc": "逛街赚钱", "process": None, "delay": 0, 'count': 0}
    # ],
    "看视频": [
        {'name':'看视频',"text": "首页", "process": lookShortVideo, "time": 600, "delay": 0, 'count': 0, 'jinBiPos': jinBiPos}
    ],
    "看视频翻倍": [
        {'name':'看视频翻倍',"ocr": "看视频翻倍", "process": lookGuangGaoOnes, "time": 600, "delay": 0, 'count': 0, 'jinBiPos': jinBiPos}
    ],
    "领金币": [
        {'name': '领金币', "text": r"^(领\\d+金币|\\d+:\\d+ 领金币)$", "process": lookGuangGaoOnes, "time": 600, "delay": 0, 'count': 0}
    ]
}

cfg = {
    "app": "com.kwai.theater",
    'name': '喜番短剧',
    "step": step,
    "node": node
}
