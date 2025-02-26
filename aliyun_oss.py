import os
import oss2
from oss2.credentials import EnvironmentVariableCredentialsProvider
from utils.log_helper import Log_Helper
from dotenv import load_dotenv

logger = Log_Helper(logger_name = "aliyu_oss",logger_level ="INFO")
load_dotenv("./.env")
# 设置环境变量
# os.environ['OSS_ACCESS_KEY_ID'] = 
# os.environ['OSS_ACCESS_KEY_SECRET'] = 

# 从环境变量中获取访问凭证。运行本代码示例之前，请确保已设置环境变量OSS_ACCESS_KEY_ID和OSS_ACCESS_KEY_SECRET。
auth = oss2.ProviderAuth(EnvironmentVariableCredentialsProvider())
# yourEndpoint填写Bucket所在地域对应的Endpoint。以华东1（杭州）为例，Endpoint填写为https://oss-cn-hangzhou.aliyuncs.com。
# 填写Bucket名称。
bucket = oss2.Bucket(auth, 'https://oss-cn-hangzhou.aliyuncs.com', 'xinggeai')
PATH = "comfyui-code/output"
# 那文件的链接就是：https://js-repair.oss-cn-shenzhen.aliyuncs.com/path/to/file
ORIGINAL_URL = "https://xinggeai.oss-cn-hangzhou.aliyuncs.com"

def upload(image_name:str,image_byte:bytes):
    path = PATH + "/"+ image_name
    logger.info(f"waiting for uploading image file , name::::{image_name}") 
    bucket.put_object(path, image_byte)
    file_url = ORIGINAL_URL + "/" + path
    logger.info(f"upload succeed::file_url:{file_url}")
    return file_url