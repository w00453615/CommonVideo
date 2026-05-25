import re
import time
import io
import numpy as np
from datetime import datetime
from random import randint, random
from typing import Optional
from PIL import Image

from ascript.android import action, system
from ascript.android.action import click

from ..util import findPosSingle, ocrFindTextPad, swipeUp, swipe, register, forWait, clickNodeP, lookGuangGao, lookShortVideo, clickNode, clickXY, \
    findImageAndClick, imageFind, descFind, swipeBack, ocrFind, swipeBackOnes, ocrFindText, swipeBackApp, WAIT_LOW, \
    WAIT_HIGH, findWaitBack, extract_first_num_to_int, findText, findDesc, swipeDown, ocrFindTextRect, swipeDownTo, wait_with_jitter
from ascript.android.screen import capture, FindColors, FindImages, Ocr
from ascript.android.system import R
from ascript.android.node import Selector
from ..logger.yunpanlogger import logger

def preproc(paras, x, y):
    x, y = ocrFind("签到领")
    logger.info(f'签到领 {x}')
    if x is not None:
        clickXY(x, y)
        wait_with_jitter(3)
        x, y, text = ocrFindText("看广告")
        if x is not None:
            clickXY(x, y)
            return lookDouyinGuangGaoOnes()
        logger.info(f'签到领 {x}')
        if x is not None:
            clickXY(x, y)
            wait_with_jitter(2)

            x, y, text = ocrFindText("看广告")
            if x is not None:
                clickXY(x, y)
                return lookDouyinGuangGaoOnes()
    return -1

def jinBiPos():
    logger.info("金币位置检测")
    res = FindImages.find_template([R.img("抖音极速版/金币.png"), ], confidence=0.7)
    if res:
        logger.info("找到金币了", res)
    else:
        logger.info("没找到金币")

    return [880, 420, 1048, 588]


# def procTwice(proc, text):
#     for i in range(2):
#         time.sleep(3 + random())
#         if i == 1 and proc(text) == False:

count = 0


def swipeBackAppDouYinGuangGao():
    swipeBackApp('秒后|领取成功', 'desc')


def swipeBackAppDouYinShouYe():
    swipeBackApp('赚钱任务|首页', 'ocr')


def lookDouyinGuangGaoOnes():
    global count
    # ocrFind('看广告赚金币')
    logger.info('lookDouyinGuangGaoOnes')
    time.sleep(5 + random())
    text = findDesc("秒后")
    logger.info(f'秒后可领奖励 {text}')
    if text is not None:
        procKeyword()
    else:
        t = randint(WAIT_LOW, WAIT_HIGH)
        logger.info(f'自动进入活动 等待 {t}')
        time.sleep(t)
        swipeBackAppDouYinGuangGao()

    time.sleep(3 + random())
    logger.info(f'秒后可领奖励 {text}')
    if text is not None:
        procKeyword()
    else:
        t = randint(WAIT_LOW, WAIT_HIGH)
        logger.info(f'自动进入活动 等待 {t}')
        time.sleep(t)
        swipeBackAppDouYinGuangGao()

    time.sleep(3 + random())
    x, y = ocrFind("继续观看")
    logger.info(f'继续观看 {x}')
    if x is not None:
        clickXY(x, y)

    time.sleep(3 + random())
    text = findDesc("秒后")
    logger.info(f'秒后可领奖励 {text}')
    if text is not None:
        leftStr = extract_first_num_to_int(text)
        if leftStr is not None:
            left = min(30, int(leftStr))
            logger.info(f'秒后可领奖励 等待 {left}')

            time.sleep(left + 2 + random())

    time.sleep(2 + random())

    text = findDesc('领取成功')
    logger.info(f'领取成功 {text}')
    if text is not None:
        swipeBackOnes()
        wait_with_jitter(2)

    time.sleep(2 + random())
    x, y = ocrFind("领取奖励")
    logger.info(f'领取奖励 {x}')
    if x is not None:
        clickXY(x, y)
        wait_with_jitter(2)
        count = 0
        return 0

    time.sleep(2 + random())
    x, _ = ocrFind('评论')
    x1, _ = ocrFind('评价')
    x2, _ = ocrFind('赚钱任务')
    logger.info(f'评论并收下金币 {x}, {x1}, {x2}')
    if x is not None or x1 is not None:
        swipeBackOnes()
        return -1
    elif x2 is not None:
        return -1
    else:
        ocrFindText(None)

    logger.info(f'lookDouyinGuangGaoOnes count {count}')    
    return -1


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
    time.sleep(10+random())
    x, _ = ocrFind("赚钱任务")
    if x is not None:
        logger.info(f'find 赚钱任务 exit')
        swipeBackAppDouYinShouYe()
        return -1
    return lookDouyinGuangGaoOnes()

def chaoduoqian(paras, x, y):
    now = datetime.now()
    if now.hour >= 21: 
        return lookBaoXiang(paras, x, y)
    else:
        return -1

def lookBaoXiang(paras, x, y):

    x, y, text = ocrFindText(r"看广告再")
    logger.info(f'看广告再 {text}')   
    if x is not None:
        clickXY(x, y)
    # else:
    #     ocrFindText(None)

    time.sleep(2 + random())
    x, y = ocrFind("赚钱任务")
    if x is not None:
        logger.info(f'lookBaoXiang 赚钱任务 {x}')
        return -1

    return lookDouyinGuangGaoOnes()


def zhiding(paras, x, y):
    logger.info('zhiding')
    time.sleep(2 + random())
    x, y, text = ocrFindText(r"支付积分")
    logger.info(f'支付积分 {text}')
    if x is not None:
        time.sleep(5 + random())
        x, y, text = ocrFindText(r"看指定")
        logger.info(f'看指定 {text}')
        if x is not None:
            clickXY(x, y)
        else:
            return -1

    time.sleep(2 + random())

    return lookDouyinGuangGaoOnes()


def qiandao(paras, x, y):
    logger.info('qiandao')

    x, y = descFind("个任务完成打卡")
    logger.info(f'个任务完成打卡 {x}')
    if x is not None:
        return -1

    # x, y = ocrFind("完成打卡")
    # logger.info('完成打卡', x, y)
    # clickXY(x, y)
    # time.sleep(1.5)

    # x, y = ocrFind("指定视频")
    # print('指定视频', x, y)
    # clickXY(x, y)
    # time.sleep(1.5)

    text = findDesc("后可完成任务")
    if text is not None:
        leftStr = extract_first_num_to_int(text)
        if leftStr is not None:
            left = min(30, int(leftStr))
            logger.info(f'秒后可领奖励 等待 {left}')

            time.sleep(left + 2 + random())
    else:
        time.sleep(randint(30, 35))
    swipeBackAppDouYinShouYe()

    return -1


def guangjie(paras, x, y):

    logger.info('guangjie')

    x, y = descFind("赚钱任务")
    if x is not None:
        logger.info(f'赚钱任务 {x}')
        return -1

    text = findDesc('15/15')
    if text is not None:
        return -1

    x, y, text = ocrFindText(r"看广告再")
    logger.info(f'看广告再 {text}')
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
    time.sleep(3 + random())
    x, y = ocrFind("赚钱任务")
    if x is not None:
        logger.info(f'chifandaka 赚钱任务 {x}') 
        return -1
    
    x, y = ocrFind("看指定视频")
    if x is not None:
        return -1

    return lookDouyinGuangGaoOnes()

def double(paras, x, y):
    time.sleep(2 + random())
    x, y = ocrFind("赚钱任务")
    if x is not None:
        logger.info(f'double 赚钱任务 {x}')
        return -1

    for _ in range(5):
        findText("已暂停", 12)
        swipeUp(0.2,0.6)

    return -1

def douyinLookShortVideo(paras, x, y, low = 4, up = 5):
    logger.info('douyinLookShortVideo')
    x, y = ocrFind("赚钱任务")
    if x is not None:
        logger.info(f'douyinLookShortVideo 赚钱任务 {x}')
        swipeBackOnes()

    return lookShortVideo(paras, x, y, low, up)

def kanzhibo(paras, x, y):
    time.sleep(5 + random())
    x, y, = findPosSingle('ocr', "开宝箱")
    logger.info(f'开宝箱ocr {x}, {y}')
    if x is not None:
        clickXY(x, y)
    
    time.sleep(1 + random())    
    x, y, = findPosSingle('rightocr', "开宝箱")
    logger.info(f'开宝箱rightocr {x}, {y}')
    if x is not None:
        clickXY(x, y, 0)
        logger.info(f'开宝箱1 {x}, {y}')
        time.sleep(2 + random())
        
    swipeBackOnes()
    
    num = 120

    views = Selector().type("ScrollView").find_all()
    if views:
        node = views[2]
        _,_,text =ocrFindText(r"(\d{1,2}):(\d{2})", rect=node.rect)
        logger.info(f'kanzhibo {text} {node.rect}')
        if text is not None:
            match = re.search(r'(\d{1,2}):(\d{2})', text)
            if match:
                minutes = int(match.group(1))
                seconds = int(match.group(2))
                num = minutes * 60 + seconds
                logger.info(f'提取的时间: {match.group(0)}, 转换为秒: {num}')
        
        time.sleep(num + random())
    swipeBackAppDouYinShouYe()
    return -1

def qiandaoshipin(paras, x, y):
    logger.info('qiandaoshipin')

    if not hasattr(qiandaoshipin, 'last_value'):
        qiandaoshipin.last_value = None
    if not hasattr(qiandaoshipin, 'start_time'):
        qiandaoshipin.start_time = datetime.now()
    text = findText(r"\d{2}:\d{2}$", index=1)
    logger.info(f'1 最后两位数字: last {qiandaoshipin.last_value} now {text}')
    if text is not None:
        match = re.search(r'(\d{2})$', text)
        if match:
            last_two = match.group(1)
            
            logger.info(f'2 最后两位数字: last {qiandaoshipin.last_value}  now {last_two}')
            logger.info(f'3 最后两位数字: last {qiandaoshipin.start_time} now {datetime.now()} {datetime.now() - qiandaoshipin.start_time}')
            if qiandaoshipin.last_value is None or last_two == qiandaoshipin.last_value or (datetime.now() - qiandaoshipin.start_time).total_seconds() > randint(10, 20):
                swipeUp(0.2,0.6)
                qiandaoshipin.start_time = datetime.now()

            qiandaoshipin.last_value = last_two
            return 0
    swipeBackAppDouYinShouYe()
    return -1

def save_error_screenshot():
    """保存错误截图并上传"""
    try:
        screenshot = capture()
        if screenshot:
            # 获取 step 名称作为文件名
            if hasattr(logger, 'current_step_name') and logger.current_step_name:
                filename = f"{logger.current_step_name}.png"
            else:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"error_screenshot_{timestamp}.png"
                
            if hasattr(logger, 'device_name') and hasattr(logger, 'run_date') and hasattr(logger, 'cfg_start_time') and hasattr(logger, 'current_cfg_name'):
                folder_path = f"log/{logger.device_name}/{logger.run_date}/{logger.cfg_start_time}/{logger.current_cfg_name}"
                
                # 使用 compress 方法直接处理 Android Bitmap
                if hasattr(screenshot, 'compress'):
                    from android.graphics import Bitmap
                    from java.io import ByteArrayOutputStream
                    
                    stream = ByteArrayOutputStream()
                    screenshot.compress(Bitmap.CompressFormat.PNG, 100, stream)
                    stream.flush()
                    screenshot_data = stream.toByteArray()
                    stream.close()
                    
                    logger.upload_image(screenshot_data, filename, folder_path)
                else:
                    # 其他类型的处理
                    img_bytes = io.BytesIO()
                    if hasattr(screenshot, 'tobytes') and hasattr(screenshot, 'shape'):
                        Image.fromarray(np.array(screenshot)).save(img_bytes, format='PNG')
                        img_bytes.seek(0)
                        screenshot_data = img_bytes.getvalue()
                        logger.upload_image(screenshot_data, filename, folder_path)
                    elif hasattr(screenshot, 'save'):
                        screenshot.save(img_bytes, format='PNG')
                        img_bytes.seek(0)
                        screenshot_data = img_bytes.getvalue()
                        logger.upload_image(screenshot_data, filename, folder_path)
                    else:
                        logger.info(f'无法处理的截图类型: {type(screenshot)}')
    except Exception as screenshot_error:
        logger.info(f'保存截图失败: {screenshot_error}')


def read_gold_coins():
    gold_coins = 0
    try:
        wait_with_jitter(1)
        # 使用OCR找到"金币收益"和"每天凌晨"两段文字的位置
        logger.info('查找金币收益位置...')
        result1 = ocrFindTextRect('金币收益')
        logger.info('查找每天凌晨位置...')
        result2 = ocrFindTextRect('每天凌晨')

        if result1 and result2:
            _, _, rect1 = result1
            _, _, rect2 = result2
            if rect1 is None or rect2 is None:
                logger.info('未找到金币收益或每天凌晨文字位置')
                save_error_screenshot()
                return gold_coins
            logger.info(f'金币收益位置: {rect1}')
            logger.info(f'每天凌晨位置: {rect2}')
            
            # 计算两个位置组成的长方形范围
            min_x = min(rect1[0], rect2[0])
            min_y = min(rect1[1], rect2[1])
            max_x = max(rect1[2], rect2[2])
            max_y = max(rect1[3], rect2[3])
            
            # 稍微扩展一下范围，确保包含金币数字
            search_rect = [
                max(0, min_x - 50),
                max(0, min_y - 20),
                max_x + 50,
                max_y + 20
            ]
            logger.info(f'搜索区域: {search_rect}')
            
            # 在这个范围内使用OCR找数字
            import re
            _, _, gold_str = ocrFindText(r'(\d{1,3}(?:,\d{3})*|\d+)', rect=search_rect)

            # 匹配数字（支持带逗号的格式）
            if gold_str is not None and gold_str.isdigit():
                gold_coins = int(gold_str)
                logger.info(f'获取到金币数: {gold_coins}')
        else:
            logger.info('未找到金币收益或每天凌晨文字')
            save_error_screenshot()

    except Exception as e:
        logger.info(f'读取金币数失败: {e}')
        import traceback
        logger.info(f'错误堆栈: {traceback.format_exc()}')
    return gold_coins

def stopProcess():
    logger.info('stopProcess')

    x, y = ocrFind("赚钱")
    if x is not None:
        clickXY(x, y)
    wait_with_jitter(1)
    swipeBackAppDouYinShouYe()

    swipeDownTo('每天凌晨')
    
    return read_gold_coins()

def doubleStopProcess():
    logger.info('doubleStopProcess stopProcess')

    swipeBackOnes()
    time.sleep(1+random())

    x, y = ocrFind("坚持")
    logger.info(f'坚持 {x}')
    if x is not None:
        clickXY(x, y)
        return -1

    wait_with_jitter(1)
    x, y = ocrFind("退出")
    logger.info(f'退出 {x}')
    if x is not None:
        clickXY(x, y)

    swipeBackAppDouYinShouYe()

    swipeDownTo('每天凌晨')
    
    return read_gold_coins()

step = [
    {'name': '开始', "display":"False", "path": ['rightocr:赚钱']},  # 打开赚钱
    {'name': '看广告', "display":"False", "path": ['rightocr:赚钱', "desc:指定视频任务|广告任务"]},  # 打开赚钱
    # {'name': '看视频赚超多钱', "path": ['path:/FrameLayout/ViewGroup/FrameLayout/FrameLayout']},
    {'name': '看视频赚超多钱', "display":"False", "path": ['rightocr:赚钱', "ocr:立即领取"]},
    {'name': '跑任务', "path": []},
    {'name': '签到', "display":"Falsee", "path": ['rightocr:赚钱', "desc:今日待打卡", 'ocr:完成打卡', "ocr:指定视频"]},
    {'name': '逛街', "display":"False", "path": ['rightocr:赚钱', "desc:浏览低价"]},
    {'name': '双倍奖励', "display":"False", "path": ['rightocr:赚钱', "desc:双重奖励"]},
    {'name': '指定视频', "display":"False", "path": ['rightocr:赚钱', "desc:做任务最高"]},
    {'name': '吃饭打卡', "display":"False", "path": ['rightocr:赚钱', "desc:打卡领吃饭补贴", 'ocr:看指定视频']},
    {'name': '看直播', "path": ['rightocr:赚钱', "desc:开宝箱最高"]},
    {'name': '开宝箱', "display":"False", "path": ['rightocr:赚钱', "ocr:开宝箱得金币|点击领"]},
    {'name': '签到视频', "display":"True", "path": ['rightocr:赚钱', "desc:今日待打卡", 'ocr:完成打卡', "ocr:分钟视频", "ocr:看视频"]},
    {'name': '看视频', "path": []}
]

node = {
    "开始": [
        {'name': '开始', 'stop': stopProcess}
    ],
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
        {'name': '双倍奖励', "process": double, 'stop': doubleStopProcess, "time": 600, 'count': 0}
    ],
    "指定视频": [
        {'name': '指定视频', "process": zhiding, 'stop': stopProcess, "time": 600, 'count': 0}
    ],
    "看直播": [
        {'name': '看直播', "process": kanzhibo, 'stop': stopProcess, "time": 1, 'count': 0}
    ],
    "签到": [
        {'name': '签到', "process": qiandao, 'stop': stopProcess, "time": 1, 'count': 0}
    ],
    "签到视频": [
        {'name': '签到视频', "process": qiandaoshipin, 'stop': stopProcess, "time": 1200, 'count': 0}
    ]
}

cfg = {
    "app": "com.ss.android.ugc.aweme.lite",
    'name': '抖音极速版',
    "step": step,
    "node": node
}