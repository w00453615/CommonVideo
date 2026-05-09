import re
import time
from datetime import datetime
from random import randint, random
from typing import Optional

from ascript.android import action, system
from ascript.android.action import click

from ..util import swipeUp, swipe, register, forWait, clickNodeP, lookGuangGao, lookShortVideo, clickNode, clickXY, \
    findImageAndClick, imageFind, descFind, swipeBack, ocrFind, swipeBackOnes, ocrFindText, swipeBackApp, WAIT_LOW, \
    WAIT_HIGH, findWaitBack, extract_first_num_to_int, findText, findDesc, swipeDown, ocrFindTextRect
from ascript.android.screen import capture, FindColors, FindImages, Ocr
from ascript.android.system import R


def preproc():
    x, y = ocrFind("签到领")
    print(f'签到领 {x}')
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
    swipeBackApp('赚钱任务', 'ocr')


def lookDouyinGuangGaoOnes():
    global count
    # ocrFind('看广告赚金币')
    time.sleep(5 + random())
    text = findDesc("秒后")
    print(f'秒后可领奖励 {text}')
    if text is not None:
        procKeyword()
    else:
        t = randint(WAIT_LOW, WAIT_HIGH)
        print(f'自动进入活动 等待 {t}')
        time.sleep(t)
        swipeBackAppDouYinGuangGao()

    time.sleep(3 + random())
    x, y = ocrFind("继续观看")
    print('继续观看', x)
    if x is not None:
        clickXY(x, y)

    time.sleep(3 + random())
    text = findDesc("秒后")
    print(f'秒后可领奖励 {text}')
    if text is not None:
        leftStr = extract_first_num_to_int(text)
        if leftStr is not None:
            left = min(30, int(leftStr))
            print(f'秒后可领奖励 等待 {left}')

            time.sleep(left + 2 + random())

    time.sleep(2 + random())

    text = findDesc('领取成功')
    print(f'领取成功 {text}')
    if text is not None:
        swipeBackOnes()
        time.sleep(2)

    time.sleep(2 + random())
    x, y = ocrFind("领取奖励")
    print(f'领取奖励 {x}')
    if x is not None:
        clickXY(x, y)
        time.sleep(2)
        count = 0
        return 0

    time.sleep(2 + random())
    x, _ = ocrFind('评论')
    x1, _ = ocrFind('评价')
    x2, _ = ocrFind('赚钱任务')
    print(f'评论并收下金币 {x}, {x1}, {x2}')
    if x is not None or x1 is not None or x2 is not None:
        swipeBackOnes()
        return -1
    else:
        ocrFindText(None)

    print(f'lookDouyinGuangGaoOnes count {count}')
    if count == 2:
        count = 0
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
    time.sleep(3 + random())
    x, y = ocrFind("赚钱任务")
    if x is not None:
        print(f'赚钱任务 {x}')
        swipeBackAppDouYinShouYe()
        return -1
    return lookDouyinGuangGaoOnes()

def chaoduoqian(paras, x, y):
    x, y = ocrFind("赚钱任务")
    if x is not None:
        print(f'chaoduoqian 赚钱任务 {x}')
        return -1

    now = datetime.now()
    if now.hour >= 21:
        preproc()   
        return lookBaoXiang(paras, x, y)
    else:
        return -1

def lookBaoXiang(paras, x, y):
    preproc()

    x, y, text = ocrFindText(r"看广告再")
    print(f'看广告再 {text}')   
    if x is not None:
        clickXY(x, y)
    # else:
    #     ocrFindText(None)

    time.sleep(3 + random())
    x, y = ocrFind("赚钱任务")
    if x is not None:
        print(f'lookBaoXiang 赚钱任务 {x}')
        return -1

    return lookDouyinGuangGaoOnes()


def zhiding(paras, x, y):
    print('zhiding')

    x, y, text = ocrFindText(r"支付积分")
    print(f'支付积分 {text}')
    if x is not None:
        time.sleep(6 + random())
        x, y, text = ocrFindText(r"看指定")
        print(f'看指定 {text}')
        if x is not None:
            clickXY(x, y)
        else:
            return -1

    time.sleep(2 + random())

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
    swipeBackAppDouYinShouYe()

    return -1


def guangjie(paras, x, y):

    x, y = descFind("赚钱任务")
    if x is not None:
        print(f'赚钱任务 {x}')
        return -1

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
    return -1

def chifandaka(paras, x, y):
    time.sleep(2 + random())
    x, y = ocrFind("赚钱任务")
    if x is not None:
        print(f'chifandaka 赚钱任务 {x}')
        return -1
    
    x, y = ocrFind("看指定视频")
    if x is not None:
        return -1

    return lookDouyinGuangGaoOnes()

def double(paras, x, y):

    x, y = ocrFind("赚钱任务")
    if x is not None:
        print(f'double 赚钱任务 {x}')
        return -1

    for _ in range(5):
        lookShortVideo(paras, x, y, 18, 20)

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

def douyinLookShortVideo(paras, x, y, low = 4, up = 5):
    print('douyinLookShortVideo')
    x, y = ocrFind("赚钱任务")
    if x is not None:
        print(f'douyinLookShortVideo 赚钱任务 {x}')
        swipeBackOnes()

    return lookShortVideo(paras, x, y, low, up)

def kanzhibo(paras, x, y):
    time.sleep(5 + random())
    x, y, rect = ocrFindTextRect(r"开宝箱")
    print(f'开宝箱 {x}, {y} {rect}')
    if x is not None and rect is not None:
        clickXY(rect[2]-15, y, 0)
        print(f'开宝箱1 {rect[2]-15}, {y} {rect}')
        time.sleep(2 + random())
        
        
        swipeBackOnes()
    
    num = 120

    _,_,text =ocrFindText(r"(\d+).*后可开")
    print(f'kanzhibo {text}')
    if text is not None:
        match = re.search(r'(\d{1,2}):(\d{2})', text)
        if match:
            minutes = int(match.group(1))
            seconds = int(match.group(2))
            num = minutes * 60 + seconds
            print(f'提取的时间: {match.group(0)}, 转换为秒: {num}')
    
    time.sleep(num + random())
    swipeBackAppDouYinShouYe()
    return -1

def qiandaoshipin(paras, x, y):
    print('qiandaoshipin')

    # x, y = ocrFind("完成打卡")
    # print('完成打卡', x, y)
    # clickXY(x, y)
    # time.sleep(2)

    # x, y = ocrFind("分钟视频")
    # print('分钟视频', x, y)
    # clickXY(x, y)
    # time.sleep(2)

    # x, y = ocrFind("去看视频")
    # print('去看视频', x, y)
    # clickXY(x, y)
    # time.sleep(2)

    if not hasattr(qiandaoshipin, 'last_value'):
        qiandaoshipin.last_value = None
    if not hasattr(qiandaoshipin, 'start_time'):
        qiandaoshipin.start_time = datetime.now()
    text = findText(r"\d{2}:\d{2}$", index=1)
    print(f'1 最后两位数字: last {qiandaoshipin.last_value} now {text}')
    if text is not None:
        match = re.search(r'(\d{2})$', text)
        if match:
            last_two = match.group(1)
            
            print(f'2 最后两位数字: last {qiandaoshipin.last_value}  now {last_two}')
            print(f'3 最后两位数字: last {qiandaoshipin.start_time} now {datetime.now()} {datetime.now() - qiandaoshipin.start_time}')
            if qiandaoshipin.last_value is None or last_two == qiandaoshipin.last_value or (datetime.now() - qiandaoshipin.start_time).total_seconds() > randint(10, 20):
                swipeUp(0.2,0.6)
                qiandaoshipin.start_time = datetime.now()
            time.sleep(2+random())

            qiandaoshipin.last_value = last_two
            return 0
    swipeBackAppDouYinShouYe()
    return -1

def stopProcess():
    print('stopProcess')
    swipeBackAppDouYinShouYe()

    for _ in range(4):
        swipeDown(0.2, 0.7)
        time.sleep(0.5+random())

step = [
    {'name': '看广告', "display":"False", "path": ['rightocr:赚钱', "desc:指定视频任务|广告任务"]},  # 打开赚钱
    # {'name': '看视频赚超多钱', "path": ['path:/FrameLayout/ViewGroup/FrameLayout/FrameLayout']},
    {'name': '看视频赚超多钱', "display":"False", "path": ['rightocr:赚钱', "ocr:立即领取"]},
    {'name': '跑任务', "path": []},
    {'name': '签到', "display":"False", "path": ['rightocr:赚钱']},
    {'name': '逛街', "display":"False", "path": ['rightocr:赚钱', "desc:浏览低价"]},
    {'name': '双倍奖励', "display":"False", "path": ['rightocr:赚钱', "desc:双重奖励"]},
    {'name': '指定视频', "display":"Falsee", "path": ['rightocr:赚钱', "desc:做任务最高"]},
    {'name': '吃饭打卡', "display":"False", "path": ['rightocr:赚钱', "desc:打卡领吃饭补贴", 'ocr:看指定视频']},
    {'name': '看直播', "path": ['rightocr:赚钱']},
    {'name': '开宝箱', "display":"Falsee", "path": ['rightocr:赚钱', "ocr:开宝箱得金币|点击领"]},
    {'name': '签到视频', "display":"True", "path": ['rightocr:赚钱', "desc:今日待打卡", 'ocr:完成打卡', 'ocr:分钟视频', 'ocr:去看视频']},
    {'name': '看视频', "path": []}
]

node = {
    "看广告": [
        {'name': '看广告', "process": lookDouyinGuangGao, 'stop': stopProcess, "time": 1200, 'count': 0}
    ],
    "开宝箱": [
        {'name': '开宝箱', "process": lookBaoXiang, 'stop': stopProcess, "time": 1200, "delay": 0, 'count': 0}
    ],
    "看视频赚超多钱": [
        {'name': '看视频赚超多钱', "process": chaoduoqian, 'stop': stopProcess, "time": 600, 'count': 0}
    ],
    "跑任务": [
        {'name': '跑任务', "process": lookBaoXiang, 'stop': stopProcess, "time": 6000, "delay": 0, 'count': 0}
    ],
    "逛街": [
        {'name': '逛街', "process": guangjie, 'stop': stopProcess, "time": 1, "delay": 0, 'count': 0}
    ],
    "吃饭打卡": [
        {'name': '吃饭打卡', "process": chifandaka, 'stop': stopProcess, "time": 600, "delay": 0, 'count': 0}
    ],
    "看视频": [
        {'name': '看视频', "process": douyinLookShortVideo, "time": 600, 'count': 0}
    ],
    "双倍奖励": [
        {'name': '双倍奖励', "process": double, 'stop': stopProcess, "time": 600, 'count': 0}
    ],
    "指定视频": [
        {'name': '指定视频', "process": zhiding, 'stop': stopProcess, "time": 600, 'count': 0}
    ],
    "看直播": [
        {'name': '看直播', "desc": "看直播", "process": kanzhibo, 'stop': stopProcess, "time": 1, 'count': 0}
    ],
    "签到": [
        {'name': '签到', "process": qiandao, 'stop': stopProcess, "time": 1, 'count': 0}
    ],
    "签到视频": [
        {'name': '签到视频', "process": qiandaoshipin, 'stop': stopProcess, "time": 600, 'count': 0}
    ]
}

cfg = {
    "app": "com.ss.android.ugc.aweme.lite",
    'name': '抖音极速版',
    "step": step,
    "node": node
}
