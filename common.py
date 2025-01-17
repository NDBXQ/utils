import os
import base64
import requests
import random
import time

# 处理时间计算装饰器
def time_calculator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"函数 {func.__name__} 执行时间: {end_time - start_time} 秒")
        return result
    return wrapper


def retry_request(make_request):
    async def wrapper(*args, **kwargs):
        # print("Making request...")
        for _ in range(3):
            try:
                response = await make_request(*args, **kwargs)
                if response["code"] == 0:
                    return response
                else:
                    print("Failed to make request, retrying...")
                    continue
            except Exception as e:
                print(f"An error occurred: {e}, {response}")
                print("Failed to make request, retrying...")
                continue
        raise Exception("Failed to make request after 3 attempts")
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
