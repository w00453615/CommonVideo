import requests
import os


REFRESH_TOKEN = "f766054e7d484b30a10e666d1da8d752"

def get_access_token(refresh_token: str = None) -> tuple:
    if refresh_token is None:
        refresh_token = REFRESH_TOKEN

    resp = requests.post(
        "https://auth.aliyundrive.com/v2/account/token",
        json={
            "grant_type": "refresh_token",
            "refresh_token": refresh_token
        }
    )
    data = resp.json()
    access_token = data["access_token"]
    drive_id = data["default_drive_id"]
    return access_token, drive_id

def create_folder(drive_id: str, name: str, parent_file_id: str, headers: dict) -> str:
    create_resp = requests.post(
        "https://api.aliyundrive.com/v2/file/create",
        headers=headers,
        json={
            "drive_id": drive_id,
            "parent_file_id": parent_file_id,
            "name": name,
            "type": "folder"
        }
    ).json()
    return create_resp.get("file_id", "")

def find_folder_in_list(drive_id: str, parent_id: str, folder_name: str, headers: dict) -> str:
    """在指定父目录下查找文件夹"""
    search_resp = requests.post(
        "https://api.aliyundrive.com/adrive/v3/file/list",
        headers=headers,
        json={
            "drive_id": drive_id,
            "parent_file_id": parent_id,
            "limit": 200
        }
    ).json()
    # print(f"[AliCloud] 查找文件夹 '{folder_name}' 在父目录 '{parent_id}' 中")
    # print(f"[AliCloud] API响应: {search_resp}")

    items = search_resp.get("items", [])
    for item in items:
        item_name = item.get("name", "")
        item_type = item.get("type", "")
        item_id = item.get("file_id", "")
        # print(f"[AliCloud] 检查项: name={item_name}, type={item_type}, id={item_id}")
        if item_name == folder_name and item_type == "folder":
            return item_id
    # print(f"[AliCloud] 文件夹 '{folder_name}' 未找到")
    return ""

def get_folder_id_by_path(drive_id: str, folder_path: str, headers: dict) -> str:
    parts = folder_path.strip("/").split("/")
    parent_id = "root"
    print(f"[AliCloud] 开始创建目录: {folder_path}")

    for part in parts:
        # print(f"[AliCloud] 查找/创建目录: '{part}' (父目录: {parent_id})")
        folder_id = find_folder_in_list(drive_id, parent_id, part, headers)
        if folder_id:
            # print(f"[AliCloud] 目录 '{part}' 已存在, ID: {folder_id}")
            parent_id = folder_id
        else:
            # print(f"[AliCloud] 目录 '{part}' 不存在, 尝试创建...")
            create_resp = requests.post(
                "https://api.aliyundrive.com/v2/file/create",
                headers=headers,
                json={
                    "drive_id": drive_id,
                    "parent_file_id": parent_id,
                    "name": part,
                    "type": "folder"
                }
            ).json()

            file_id = create_resp.get("file_id", "")
            if file_id:
                print(f"[AliCloud] 目录 '{part}' 创建成功, ID: {file_id}")
                parent_id = file_id
            else:
                print(f"[AliCloud] 目录 '{part}' 创建失败, 响应: {create_resp}")
                return ""

    return parent_id

def find_file_in_folder(drive_id: str, folder_id: str, filename: str, headers: dict) -> str:
    """在指定文件夹中查找文件"""
    search_resp = requests.post(
        "https://api.aliyundrive.com/adrive/v3/file/list",
        headers=headers,
        json={
            "drive_id": drive_id,
            "parent_file_id": folder_id,
            "limit": 200
        }
    ).json()
    
    items = search_resp.get("items", [])
    for item in items:
        item_name = item.get("name", "")
        item_type = item.get("type", "")
        item_id = item.get("file_id", "")
        if item_name == filename and item_type == "file":
            return item_id
    return ""

def delete_file(drive_id: str, file_id: str, headers: dict) -> bool:
    """删除指定文件"""
    try:
        requests.post(
            "https://api.aliyundrive.com/v2/file/delete",
            headers=headers,
            json={
                "drive_id": drive_id,
                "file_id": file_id
            }
        )
        return True
    except Exception as e:
        print(f"[AliCloud] 删除文件失败: {e}")
        return False

def download_file_from_aliyunpan(filename: str, refresh_token: str = None, folder_path: str = None) -> bytes:
    """从阿里云盘下载文件，返回文件内容的 bytes"""
    access_token, drive_id = get_access_token(refresh_token)
    headers = {"Authorization": f"Bearer {access_token}"}
    
    parent_file_id = "root"
    if folder_path:
        parent_file_id = get_folder_id_by_path(drive_id, folder_path, headers)
        if not parent_file_id:
            return None
    
    file_id = find_file_in_folder(drive_id, parent_file_id, filename, headers)
    if not file_id:
        return None
    
    # 获取下载链接
    download_resp = requests.post(
        "https://api.aliyundrive.com/v2/file/get_download_url",
        headers=headers,
        json={
            "drive_id": drive_id,
            "file_id": file_id
        }
    ).json()
    
    download_url = download_resp.get("url")
    if not download_url:
        return None
    
    # 下载文件
    file_resp = requests.get(download_url)
    if file_resp.status_code == 200:
        return file_resp.content
    return None

def upload_file_to_aliyunpan(file_path: str, upload_name: str = None, refresh_token: str = None, folder_path: str = None) -> str:
    if upload_name is None:
        upload_name = os.path.basename(file_path)

    access_token, drive_id = get_access_token(refresh_token)
    headers = {"Authorization": f"Bearer {access_token}"}

    parent_file_id = "root"
    if folder_path:
        print(f"[AliCloud] 文件将上传到目录: {folder_path}")
        parent_file_id = get_folder_id_by_path(drive_id, folder_path, headers)
        if not parent_file_id:
            print(f"[AliCloud] 目录创建失败, 文件将上传到根目录")
        else:
            # 上传前删除同名文件
            existing_file_id = find_file_in_folder(drive_id, parent_file_id, upload_name, headers)
            if existing_file_id:
                delete_file(drive_id, existing_file_id, headers)

    file_size = os.path.getsize(file_path)
    create_resp = requests.post(
        "https://api.aliyundrive.com/v2/file/create",
        headers=headers,
        json={
            "drive_id": drive_id,
            "parent_file_id": parent_file_id,
            "name": upload_name,
            "type": "file",
            "size": file_size,
            "check_name_mode": "auto_rename"
        }
    ).json()

    file_id = create_resp.get("file_id")
    if not file_id:
        print(f"[AliCloud] 文件创建失败，响应: {create_resp}")
        return ""

    if "part_info_list" in create_resp:
        upload_url = create_resp["part_info_list"][0]["upload_url"]
        with open(file_path, "rb") as f:
            requests.put(upload_url, data=f)

        requests.post(
            "https://api.aliyundrive.com/v2/file/complete",
            headers=headers,
            json={
                "drive_id": drive_id,
                "file_id": file_id,
                "upload_id": create_resp["upload_id"]
            }
        )
    else:
        print("✅ 秒传成功！")

    share_url = f"https://www.aliyundrive.com/drive/file/{file_id}"
    return share_url

if __name__ == "__main__":
    FILE_PATH = "test.txt"
    UPLOAD_NAME = "test.txt"

    # print("正在上传文件...")
    share_url = upload_file_to_aliyunpan(FILE_PATH, UPLOAD_NAME)

    print("\n" + "="*60)
    print("✅ 上传成功！")
    print(f"🔗 文件链接（登录后打开）：")
    print(share_url)
    print("="*60)     
