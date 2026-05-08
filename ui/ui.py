from ascript.android.ui import WebWindow
# __init__.py 为初始入口文件,工程代码的入口文件.

# 导入动作库常用函数
from ascript.android.action import click,slide,Touch,gesture
# 导入控件检索相关
from ascript.android.node import Selector
# 导入图色相关
from ascript.android.screen import capture,FindColors,FindImages,Ocr
# 导入系统相关
from ascript.android import system
# 环境设备相关
from ascript.android.system import R,Device
from ascript.android.ui import WebWindow
from ascript.android.system import R
import json
from ..util import process

def filter_functions(data):
    """
    递归过滤数据中的函数类型，支持字典、列表、嵌套结构
    """
    # 处理字典：过滤值为函数的键值对
    if isinstance(data, dict):
        filtered = {}
        for key, value in data.items():
            # 递归处理值，若处理后的值不是函数则保留
            filtered_value = filter_functions(value)
            if not callable(filtered_value):
                filtered[key] = filtered_value
        return filtered

    # 处理列表/元组：过滤函数元素
    elif isinstance(data, (list, tuple)):
        filtered = []
        for item in data:
            # 递归处理元素，若处理后不是函数则保留
            filtered_item = filter_functions(item)
            if not callable(filtered_item):
                filtered.append(filtered_item)
        return filtered  # 元组会转为列表，若需保留元组可改为 tuple(filtered)

    # 处理其他可迭代对象（如集合）：转为列表后过滤
    elif hasattr(data, '__iter__') and not isinstance(data, (str, bytes)):
        return filter_functions(list(data))

    # 处理函数类型：直接返回 None（后续会被过滤）
    elif callable(data):
        return None

    # 基础类型（字符串、数字等）：直接返回
    else:
        return data

def genCheckList(cfg) :
    name = cfg['name']
    step = cfg['step']

    text = name
    check = "|".join('<input type="checkbox" id="checkbox">' + item['name'] for item in step)

    return '<br />' + text + '<br />' +  check

def genCheckValue(cfg) :
    name = cfg['name']
    step = cfg['step']

    text = name
    check = "|".join('<input type="checkbox id=' + item['name'] + '>' + item['name'] for item in step)

    return '<br />' + text + '<br />' +  check
def cfg(cfgList) :
    checklist = ''
    i = 0
    for cfg in cfgList :
        checklist += genCheckList(cfg)


    fileIn = open(R.ui("main.html"), mode='r')
    str = fileIn.read()
    print(checklist)
    str = str.replace('checklist', checklist)
    print(str)
    fileOut = open(R.ui("1.html"), mode='w')
    fileOut.write(str)
    fileOut.close()
    fileIn.close()

def setCfgList(cfgListIn):
    global cfgList

    cfgList = cfgListIn

def ready():
    print('cfgList', cfgList)
    cfgListStr = json.dumps(filter_functions(cfgList), ensure_ascii=False, indent=2).replace('\n', '').replace('\r', '')
    print(f'senddata(\'{cfgListStr}\')')
    # cfgListStr = http.escape(cfgListStr)
    # print("senddata2('" + cfgListStr + "')")
    # w.call("senddata('"+ cfgListStr + "')"
    w.call(f'senddata(\'{cfgListStr}\')')

def submit(v):
    print('submit2', v)

    global w
    w.close()

    result_dict = json.loads(v)
    print('result_dict', result_dict)
    process(result_dict)

def mission(v):
    print('mission', v)

    global w
    w.close()

    result_dict = json.loads("""{
  "抖音极速版": [
    "看广告",
    "逛街",
    "双倍奖励",
    "指定视频",
    "开宝箱",
    "吃饭打卡",
    "看视频"
  ],
  "喜番短剧": [
    "领金币"
  ]
}""")
    print('result_dict', result_dict)
    process(result_dict)

def qiandao(v):
    print('qiandao', v)

    global w
    w.close()

    result_dict = json.loads("""{
  "快手": [
    "签到"
  ],
  "抖音极速版": [
    "签到"
  ]
}""")
    print('qiandao result_dict', result_dict)
    process(result_dict)
def tunnel(k,v):
    print('k',k)
    print('v',v)

    if k == 'ready' :
        ready()
    elif k == 'submit' :
        submit(v)
    elif k == 'mission' :
        mission(v)
    elif k == 'qiandao' :
        qiandao(v)

w = None
cfgList = None

def show(cfgListIn):
    # cfg(cfgList)
    global w

    setCfgList(cfgListIn)

    w = WebWindow(R.ui('main.html'), tunnel)
    print(w)
    w.width("-1")
    w.height("-1")
    w.show()