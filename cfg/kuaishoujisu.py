import time
from random import randint

from ascript.android import action
from ascript.android.action import click

from ..util import WAIT_HIGH, WAIT_LOW, findText, findTextAndClick, findWaitBack, swipeBackOnes, swipeUp, swipe, register, forWait, clickNodeP, lookGuangGao, lookShortVideo, clickNode, clickXY, \
    findImageAndClick, imageFind, descFind, swipeBack, findDesc, textFind, swipeBackApp, ocrFind, wait_with_jitter
from ascript.android.screen import capture, FindColors, FindImages, Ocr
from ascript.android.system import R
from ascript.android.node import Selector
from ..logger.yunpanlogger import logger

def jinBiPos():
    logger.info("金币位置检测")
    res = FindImages.find_template([R.img("抖音极速版/金币.png"), ], confidence=0.7)
    if res:
        logger.info("找到金币了", res)
    else:
        logger.info("没找到金币")

    return [880, 420, 1048, 588]

def qiandao(paras, x, y):
    logger.info('qiandao')

    wait_with_jitter(2)
    nodes = Selector().text("去观看").find_all()
    if nodes:
        node = nodes[-1]
    else:
        node = None
    
    logger.info(f'qiandao 去观看 {node}')
    if node is not None:
        clickNode(node)

    wait_with_jitter(2)
    x, y = textFind('广告完成任务')
    print('qiandao 广告完成任务', x)
    if x is not None:
        clickXY(x, y)
    else:
        return -1
    wait_with_jitter(1)
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
    logger.info(f'完成去观看打卡 {x}, {y}')
    clickXY(x, y)
    wait_with_jitter(2)
def swipeBackAppKuaiShoujisuGuangGao():
    swipeBackApp('s后|成功领取', 'text')

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
    keyword.append('免费')
    for it in keyword:
        x, _ = findWaitBack(it, 's后|成功领取', 'text')
        if x is not None:
            break
        
    swipeBackAppKuaiShoujisuGuangGao()

def kanguanggao(paras, x, y):
    logger.info('kanguanggao')

    text = findText("s后")
    logger.info(f's后可领取奖励 {text}')
    if text is not None:
        procKeyword()
    else:
        t = randint(WAIT_LOW, WAIT_HIGH)
        logger.info(f'自动进入活动 等待 {t}')
        time.sleep(t)
    
    text = findText("s后")
    logger.info(f's后可领奖励 {text}')
    if text is not None:
        leftStr = extract_first_num_to_int(text)
        if leftStr is not None:
            left = min(30, int(leftStr))
            logger.info(f'秒后可领奖励 等待 {left}')

            time.sleep(left + 2 + random())

    swipeBackOnes()
    
    result = findTextAndClick("领取奖励")
    if result is not None:
        logger.info(f'领取奖励 成功')
        return 0

    x, y = textFind("看广告得金币")
    logger.info(f'看广告得金币 {x}, {y}')
    if x is not None:
        swipeBackOnes()
    return -1
    

def stopProcess():
    print('stopProcess')
    swipeBackApp('首页', 'ocr')
    
    return 0

step = [
    {'name': '看视频', "path": []},
    # {'name': '签到', "display":"Falsee", "path": ['id:com.smile.gifmaker:id/kem_task_pendant_new', 'ocr:连续打卡']},
    {'name': '看广告', "display":"True", "path": ['ocr:去赚钱', 'text:看广告得金币']},
    {'name': '跑任务', "display":"True", "path": []}
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
    "看广告": [
        {'name': '看广告', "process": kanguanggao, "time": 600, 'count': 0}
    ],
    "跑任务": [
        {'name': '跑任务', "process": kanguanggao, "time": 600, 'count': 0}
    ],
    "签到视频": [
        {'name': '签到视频', "process": qiandaoshipin, "time": 600, 'count': 0}
    ]
}

cfg = {
    "app": "com.kuaishou.nebula",
    'name': '快手极速',
    "step": step,
    "node": node
}
