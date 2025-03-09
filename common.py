import os
import base64
import requests
import random
import time
from .log_helper import Log_Helper
import asyncio
import json

logger = Log_Helper(logger_name = __name__, logger_level ="INFO")
# 处理时间计算装饰器
def time_calculator(func):
    async def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = await func(*args, **kwargs)
        elapsed_time = time.perf_counter() - start
        logger.info(f"Function {func.__name__} execution time: {elapsed_time:.2f} seconds")
        return result
    return wrapper


def retry_request(make_request, max_attempts=4):
    async def wrapper(*args, **kwargs):
        # print("Making request...")
        for _ in range(max_attempts):
            try:
                response = await make_request(*args, **kwargs)
                if response["code"] == 0:
                    return response
                else:
                    logger.info(f"Failed to make request, response: {response}, retrying...")
                    asyncio.sleep(10)
                    continue
            except Exception as e:
                logger.info(f"An error occurred: {e}")
                logger.info("Failed to make request, retrying...")
                continue
        raise Exception(f"Failed to make request after {max_attempts} attempts")
    return wrapper

# 读取指定目录下的所有文件名
def read_directory(directory_path):
    file_names = []
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_names.append(file)
    return file_names

def download_image_to_base64(url):
    response = requests.get(url)
    if response.status_code == 200:
        image_data = response.content
        image_base64 = base64.b64encode(image_data).decode('utf-8')
        return image_base64
    else:
        raise "Error downloading image"
    

def generate_random_number(min_length, max_length):
    # 确定随机数的长度范围
    length = random.randint(min_length, max_length)
    # 生成随机数（包括最小和最大长度）
    return random.randint(10**(length-1), 10**length - 1)


import random
def create_random(n=20):
    # 根据n动态调整随机数范围
    min_val = 10 ** (n - 1)
    max_val = 10 ** n - 1
    # 生成一个在指定范围内的随机整数
    random_number = random.randint(min_val, max_val)
    # 将随机数转换为字符串，并确保长度为n位
    random_number_str = str(random_number).zfill(n)
    return random_number_str


# 读取 json 文件
def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data