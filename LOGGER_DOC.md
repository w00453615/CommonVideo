# 日志模块使用文档

## 概述

本日志模块提供统一的日志记录和传输功能，支持本地日志打印和阿里云日志服务（SLS）实时传输。

## 文件结构

```
├── logger.py          # 日志模块核心实现
├── logger_config.json # 日志配置文件
└── LOG_DOC.md         # 本文档
```

## 日志格式

每条日志包含以下字段：

| 字段 | 类型 | 说明 |
|------|------|------|
| timestamp | string | ISO格式时间戳 |
| level | string | 日志级别（DEBUG/INFO/WARNING/ERROR） |
| step_id | string | 步骤标识 |
| operation | string | 操作描述 |
| params | dict | 关键参数 |
| app | string | 应用名称 |
| version | string | 版本号 |

## 配置方法

### 修改配置文件

编辑 `logger_config.json` 文件：

```json
{
    "log_level": "INFO",
    "enable_sls": true,
    "local_cache_dir": "./logs/cache/",
    "retry_max": 3,
    "retry_delay": 5,
    "app_name": "CommonVideo",
    "version": "1.0.0",
    "sls_config": {
        "endpoint": "cn-hangzhou.log.aliyuncs.com",
        "access_key_id": "your-access-key-id",
        "access_key_secret": "your-access-key-secret",
        "project": "your-project",
        "logstore": "your-logstore"
    }
}
```

### 配置项说明

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| log_level | string | INFO | 日志级别（DEBUG/INFO/WARNING/ERROR） |
| enable_sls | bool | false | 是否启用SLS传输 |
| local_cache_dir | string | ./logs/cache/ | 本地缓存目录 |
| retry_max | int | 3 | 重试次数 |
| retry_delay | int | 5 | 重试间隔（秒） |
| app_name | string | CommonVideo | 应用名称 |
| version | string | 1.0.0 | 版本号 |

## 阿里云SLS对接

### 准备工作

1. 登录阿里云控制台
2. 创建日志服务项目（Project）
3. 创建日志库（Logstore）
4. 获取访问密钥（AccessKey ID和AccessKey Secret）

### 安装SDK

```bash
pip install aliyun-log-python-sdk
```

### 配置示例

```json
{
    "enable_sls": true,
    "sls_config": {
        "endpoint": "cn-hangzhou.log.aliyuncs.com",
        "access_key_id": "AKIAIOSFODNN7EXAMPLE",
        "access_key_secret": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
        "project": "my-project",
        "logstore": "my-logstore"
    }
}
```

## 使用示例

### 基础用法

```python
from logger import logger

# 记录INFO级别日志
logger.info("STEP_001", "开始执行任务", {"task_name": "看视频", "app": "抖音极速版"})

# 记录DEBUG级别日志
logger.debug("STEP_002", "查找控件", {"type": "text", "value": "金币"})

# 记录WARNING级别日志
logger.warning("STEP_003", "控件查找超时", {"timeout": 10})

# 记录ERROR级别日志
logger.error("STEP_004", "任务执行失败", {"error": "网络超时"})
```

### 在步骤节点处添加日志

```python
def procSingle(cfgName, check):
    cfg = procList[cfgName]
    app = cfg['app']
    
    # 记录任务开始
    logger.info("PROC_START", "任务开始执行", {"cfgName": cfgName, "app": app})
    
    steps = cfg['step']
    nodes = cfg['node']
    
    for step in steps:
        step_name = step['name']
        
        # 记录步骤开始
        logger.info(f"STEP_{step_name}", "步骤开始", {"step": step_name})
        
        if not findPath(step, step_name):
            # 记录步骤失败
            logger.warning(f"STEP_{step_name}", "路径查找失败", {"step": step_name})
            continue
        
        for it in nodeList:
            # 记录节点处理
            logger.debug(f"NODE_{it['name']}", "处理节点", {"node": it})
            
            if proc:
                # 记录进程执行
                logger.info(f"PROC_{it['name']}", "执行进程", {"process": str(proc)})
```

## 日志传输机制

### 传输流程

1. **日志生成**：调用日志方法生成日志条目
2. **本地打印**：日志先打印到控制台
3. **队列缓冲**：如果启用SLS，日志加入传输队列
4. **后台传输**：后台线程从队列取出日志发送到SLS
5. **失败重试**：传输失败时自动重试（最多3次）
6. **本地缓存**：重试失败后缓存到本地，下次启动时重新传输

### 重试机制

- 最大重试次数：3次
- 重试间隔：5秒、10秒、15秒（递增）
- 超过重试次数后缓存到本地文件

### 本地缓存策略

- 缓存目录：`./logs/cache/`
- 缓存文件名：`cache_时间戳_对象ID.log`
- 应用启动时自动加载缓存日志并重新传输

## 日志级别控制

| 级别 | 说明 | 使用场景 |
|------|------|----------|
| DEBUG | 调试信息 | 详细的程序执行信息，用于开发调试 |
| INFO | 一般信息 | 正常的业务流程记录 |
| WARNING | 警告信息 | 潜在的问题或需要关注的情况 |
| ERROR | 错误信息 | 程序错误或异常情况 |

通过修改 `log_level` 配置项可以控制日志输出级别。

## 代码优化建议

### 1. 日志开关配置

在应用配置中添加日志开关：

```python
config = {
    'enable_log': True,
    'log_level': 'INFO',
    'enable_sls': False
}
```

### 2. 日志功能模块化

将日志功能封装为独立模块，便于维护和扩展：

- `logger.py`：核心日志类
- `logger_config.json`：配置文件
- `LOG_DOC.md`：文档说明

### 3. 性能优化

- 使用后台线程异步传输日志，不阻塞主流程
- 限制队列大小，防止内存溢出
- 批量传输，减少网络请求次数

### 4. 错误处理

- 记录日志发送失败的情况
- 提供日志传输状态查询接口
- 支持手动触发缓存日志重新传输

## 故障排除

### SLS连接失败

1. 检查网络连接
2. 验证Endpoint地址是否正确
3. 检查AccessKey是否有效
4. 确认Project和Logstore名称正确

### 日志没有输出

1. 检查 `log_level` 配置是否正确
2. 确认日志级别不低于配置的级别
3. 检查控制台输出是否正常

### 缓存日志过多

1. 检查网络连接是否正常
2. 确认SLS服务是否可用
3. 手动清理缓存目录

## 版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| 1.0.0 | 2026-05-09 | 初始版本，支持本地日志和SLS传输 |
