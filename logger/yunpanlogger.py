"""
日志模块 - 提供统一的日志记录和传输功能
直接上传到阿里云盘，不保存本地文件
使用HTTP方式，不依赖SDK
支持个人用户仅用refresh_token访问
"""

import os
import time
import json
import requests
import importlib.util
from datetime import datetime
from typing import Optional, Dict, Any

_aliyunpan_spec = importlib.util.spec_from_file_location("aliyunpan", os.path.join(os.path.dirname(__file__), "aliyunpan.py"))
_aliyunpan_module = importlib.util.module_from_spec(_aliyunpan_spec)
_aliyunpan_spec.loader.exec_module(_aliyunpan_module)
upload_file_to_aliyunpan = _aliyunpan_module.upload_file_to_aliyunpan
download_file_from_aliyunpan = _aliyunpan_module.download_file_from_aliyunpan

LOG_LEVELS = {
    'DEBUG': 0,
    'INFO': 1,
    'WARNING': 2,
    'ERROR': 3
}

class AliCloudDriveAPI:
    def __init__(self, config: Dict[str, Any]):
        self.refresh_token = config.get('refresh_token', '')

    def upload_file(self, content: str, file_name: str = None, folder_path: str = None) -> bool:
        import tempfile
        if not file_name:
            file_name = datetime.now().strftime('%Y%m%d_%H%M%S') + '.txt'

        try:
            with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', suffix='.txt', delete=False) as f:
                f.write(content)
                temp_path = f.name

            share_url = upload_file_to_aliyunpan(temp_path, file_name, self.refresh_token, folder_path)
            os.unlink(temp_path)
            print(f"[AliCloud] 文件上传成功: {folder_path}/{file_name}")
            return True
        except Exception as e:
            print(f"[AliCloud] 文件上传异常: {e}")
            return False

    def upload_file_from_buffer(self, file_buffer, file_name: str, folder_path: str = None) -> bool:
        import tempfile
        try:
            with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
                f.write(file_buffer.getvalue())
                temp_path = f.name

            share_url = upload_file_to_aliyunpan(temp_path, file_name, self.refresh_token, folder_path)
            os.unlink(temp_path)
            print(f"[AliCloud] 文件上传成功: {folder_path}/{file_name}")
            return True
        except Exception as e:
            print(f"[AliCloud] 文件上传异常: {e}")
            return False


class YunPanLogger:
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or self._load_config()
        self.log_level = LOG_LEVELS.get(self.config.get('log_level', 'INFO'), 1)
        self.enable_alicloud = self.config.get('enable_alicloud', True)
        self.upload_interval = self.config.get('upload_interval', 600)

        self.log_buffer = []
        self.buffer_max_size = 10000000
        self.last_upload_time = time.time()

        self.alicloud_client = None
        self.step_start_time = None
        self.cfg_start_time = None

        if self.enable_alicloud:
            self._init_alicloud_client()

    def _load_config(self) -> Dict[str, Any]:
        config_path = os.path.join(os.path.dirname(__file__), 'logger_config.json')
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            'log_level': 'INFO',
            'enable_alicloud': True,
            'upload_interval': 60,
            'alicloud_folder_id': 'root'
        }

    def _init_alicloud_client(self):
        try:
            if not self.config.get('refresh_token', ''):
                print(f"[LOGGER] 未配置 refresh_token，跳过云端上传")
                self.enable_alicloud = False
                return

            self.alicloud_client = AliCloudDriveAPI(self.config)
            print(f"[LOGGER] 阿里云盘客户端初始化成功")
        except Exception as e:
            print(f"[LOGGER] 阿里云盘客户端初始化失败: {e}，日志仅打印到控制台")
            self.enable_alicloud = False

    def _should_log(self, level: str) -> bool:
        return LOG_LEVELS.get(level, 1) >= self.log_level

    def _format_log(self, level: str, message: str, params: Dict[str, Any] = None) -> str:
        timestamp = datetime.now().isoformat()
        if params:
            params_str = json.dumps(params, ensure_ascii=False, default=str)
            return f"[{timestamp}] [{level}] {message} - {params_str}\n"
        return f"[{timestamp}] [{level}] {message}\n"

    def _upload_to_alicloud(self, force: bool = False, filename: str = None, folder_path: str = None) -> bool:
        if not self.alicloud_client or not self.enable_alicloud:
            return False

        current_time = time.time()
        if not force:
            return False

        if not self.log_buffer:
            return False

        log_content = "".join(self.log_buffer)
        self.log_buffer.clear()

        if not filename:
            filename = datetime.now().strftime('%Y%m%d_%H%M%S') + '.txt'

        if not folder_path and self.cfg_start_time:
            if self.device_name and hasattr(self, 'current_cfg_name') and hasattr(self, 'run_date') and self.run_date:
                folder_path = f"log/{self.device_name}/{self.run_date}/{self.cfg_start_time}/{self.current_cfg_name}"
            elif self.device_name and hasattr(self, 'current_cfg_name'):
                folder_path = f"log/{self.device_name}/{self.cfg_start_time}/{self.current_cfg_name}"
            elif self.device_name:
                folder_path = f"log/{self.device_name}/{self.cfg_start_time}"
            elif hasattr(self, 'current_cfg_name') and hasattr(self, 'run_date') and self.run_date:
                folder_path = f"log/{self.run_date}/{self.cfg_start_time}/{self.current_cfg_name}"
            elif hasattr(self, 'current_cfg_name'):
                folder_path = f"log/{self.cfg_start_time}/{self.current_cfg_name}"
            else:
                folder_path = f"log/{self.cfg_start_time}"

        if self.alicloud_client.upload_file(log_content, filename, folder_path):
            self.last_upload_time = current_time
            return True

        self.log_buffer.append(log_content)
        return False

    def log(self, level: str, message: str, params: Dict[str, Any] = None):
        if not self._should_log(level):
            return

        log_content = self._format_log(level, message, params)
        print(log_content.strip())
        self.log_buffer.append(log_content)

        self._upload_to_alicloud()

    def start_cfg(self, cfg_name: str, device_name: str = None, timestamp: str = None, run_date: str = None):
        self.device_name = device_name
        self.current_cfg_name = cfg_name
        if timestamp:
            self.cfg_start_time = timestamp
        else:
            self.cfg_start_time = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.run_date = run_date
        self.step_start_time = datetime.now()

    def start_step(self, step_name: str = None):
        self.step_start_time = datetime.now()
        if step_name:
            self.current_step_name = step_name

    def debug(self, message: str, params: Dict[str, Any] = None):
        self.log('DEBUG', message, params)

    def info(self, message: str, params: Dict[str, Any] = None):
        self.log('INFO', message, params)

    def warning(self, message: str, params: Dict[str, Any] = None):
        self.log('WARNING', message, params)

    def error(self, message: str, params: Dict[str, Any] = None):
        self.log('ERROR', message, params)

    def _format_duration(self, seconds: float) -> str:
        if seconds < 60:
            return f"{int(seconds)}s"
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        if minutes < 60:
            return f"{minutes}m{secs}s"
        hours = int(minutes // 60)
        mins = int(minutes % 60)
        return f"{hours}h{mins}m{secs}s"

    def flush(self, cfg_name: str = None, step_name: str = None):
        if cfg_name and step_name and self.cfg_start_time and self.step_start_time:
            end_time = datetime.now()
            duration = (end_time - self.step_start_time).total_seconds()
            duration_str = self._format_duration(duration)
            if self.device_name:
                if self.run_date:
                    folder_path = f"log/{self.device_name}/{self.run_date}/{self.cfg_start_time}/{cfg_name}"
                else:
                    folder_path = f"log/{self.device_name}/{self.cfg_start_time}/{cfg_name}"
            else:
                if self.run_date:
                    folder_path = f"log/{self.run_date}/{self.cfg_start_time}/{cfg_name}"
                else:
                    folder_path = f"log/{self.cfg_start_time}/{cfg_name}"
            filename = f"{step_name}_{duration_str}.txt"
            self._upload_to_alicloud(force=True, filename=filename, folder_path=folder_path)
            self.step_start_time = None

    def upload_html_report(self, html_content, filename, folder_path):
        """上传HTML报表到阿里云盘"""
        return self.upload_report(html_content, filename, folder_path)

    def upload_excel_report(self, excel_buffer, filename, folder_path):
        """上传Excel报表到阿里云盘"""
        if not self.alicloud_client or not self.enable_alicloud:
            print("[LOGGER] 阿里云盘未启用，无法上传报表")
            return False
        try:
            success = self.alicloud_client.upload_file_from_buffer(excel_buffer, filename, folder_path)
            if success:
                print(f"[LOGGER] 报表上传成功: {filename}")
            return success
        except Exception as e:
            print(f"[LOGGER] 报表上传失败: {e}")
            return False

    def upload_image(self, image_data, filename, folder_path):
        """上传图片到阿里云盘"""
        if not self.alicloud_client or not self.enable_alicloud:
            print("[LOGGER] 阿里云盘未启用，无法上传图片")
            return False
        try:
            import io
            # 处理 Java byte[] 类型
            if hasattr(image_data, 'length') and not isinstance(image_data, (bytes, bytearray)):
                # Java byte[] 转换为 Python bytes
                image_data = bytes(image_data)
            buffer = io.BytesIO(image_data)
            success = self.alicloud_client.upload_file_from_buffer(buffer, filename, folder_path)
            if success:
                print(f"[LOGGER] 图片上传成功: {folder_path}/{filename}")
            return success
        except Exception as e:
            print(f"[LOGGER] 图片上传失败: {e}")
            import traceback
            print(f"[LOGGER] 错误堆栈: {traceback.format_exc()}")
            return False

    def upload_report(self, content, filename, folder_path):
        """上传报表到阿里云盘（通用方法）"""
        if not self.alicloud_client or not self.enable_alicloud:
            print("[LOGGER] 阿里云盘未启用，无法上传报表")
            return False
        try:
            success = self.alicloud_client.upload_file(content, filename, folder_path)
            if success:
                print(f"[LOGGER] 报表上传成功: {filename}")
            return success
        except Exception as e:
            print(f"[LOGGER] 报表上传失败: {e}")
            return False
            
    def download_excel_report(self, filename, folder_path):
        """从阿里云盘下载Excel报表，返回BytesIO对象，不存在则返回None"""
        if not self.enable_alicloud:
            print("[LOGGER] 阿里云盘未启用，无法下载报表")
            return None
        try:
            content = download_file_from_aliyunpan(filename, self.config.get('refresh_token'), folder_path)
            if content:
                import io
                return io.BytesIO(content)
            return None
        except Exception as e:
            print(f"[LOGGER] 报表下载失败: {e}")
            return None

logger = YunPanLogger()