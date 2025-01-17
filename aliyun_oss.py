import os
import oss2
from oss2.credentials import EnvironmentVariableCredentialsProvider
from utils.log_helper import Log_Helper
from dotenv import load_dotenv

logger = Log_Helper(logger_name="aliyu_oss", logger_level="INFO")

load_dotenv(".env")

# 设置环境变量
os.environ['OSS_ACCESS_KEY_ID'] = os.getenv('OSS_ACCESS_KEY_ID', '')
os.environ['OSS_ACCESS_KEY_SECRET'] = os.getenv('OSS_ACCESS_KEY_SECRET', '')

# 从环境变量中获取访问凭证
auth = oss2.ProviderAuth(EnvironmentVariableCredentialsProvider())

# 常量
BUCKET_URL = os.getenv('BUCKET_URL', '')
BUCKET_NAME = os.getenv('BUCKET_NAME', '')
STORE_PATH = os.getenv('STORE_PATH', '')

# 拼接ORIGINAL_URL
splited_url = BUCKET_URL.split("//")
ORIGINAL_URL = splited_url[0] + "//" + BUCKET_NAME + "." + splited_url[1]

# 创建 Bucket 实例
bucket = oss2.Bucket(auth, BUCKET_URL, BUCKET_NAME)

def upload(image_name: str, image_byte: bytes) -> str:
    """
    上传图片到阿里云 OSS 并返回图片的 URL。

    :param image_name: 图片名称
    :param image_byte: 图片字节流
    :return: 图片的 URL
    """
    path = f"{STORE_PATH}/{image_name}"
    logger.info(f"Waiting for uploading image file, name: {image_name}") 
    bucket.put_object(path, image_byte)
    file_url = f"{ORIGINAL_URL}/{path}"
    logger.info(f"Upload succeed, file URL: {file_url}")
    return file_url
