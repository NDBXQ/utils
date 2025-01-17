import cv2
import numpy as np
from .log_helper import Log_Helper
import base64
from .dify_llm import Dify


logger = Log_Helper(logger_name = "image_utils",logger_level ="INFO")
dify = Dify()

def judge_black_and_white_photos(image_path:str="", base64_image:str="", threshold:int = 30):
    """
    Discribe:判断图片是否为黑白图片
    Args:
        image_path (str): 图片路径
        threshold (int): 阈值. Defaults to 15.
    return:
        int: 0为黑白图片，1为彩色图片.
    """
    if image_path == "" and base64_image == "":
        raise Exception("image_path and image_base64 can't be empty at the same time")
    elif image_path != "" and base64_image != "":
        raise Exception("image_path and image_base64 can't be not empty at the same time")

    elif image_path == "" and base64_image != "":
        # 将base64图片转换为numpy数组
        np_image = cv2.imdecode(np.frombuffer(
            base64.b64decode(base64_image),
            np.uint8),
            cv2.IMREAD_COLOR)
        
        logger.info("输入的图片数据为base64格式")

    elif image_path.split("/")[-1].split(".")[-1] in ["jpg", "png", "jpeg"]:
        logger.info("图片为本地路径格式")
        np_image = cv2.imread(image_path)
    else:
        raise Exception("请检查图片的格式")
    
    # 根据图片的最长边将图片缩放到指定大小
    # 计算图片的长宽
    origin_size = np_image.shape[:2]
    height, width = origin_size
    logger.info(f"原始的图片大小为：：：：：{origin_size}")
    if height >= width:
        scale_rate = 512/height
        scaled_width = int(width*scale_rate)
        np_image = cv2.resize(np_image, (scaled_width, 512))
    else:
        scale_rate = 512/width
        scaled_height = int(height*scale_rate)
        np_image = cv2.resize(np_image, (512, scaled_height))

    resized_size = np_image.shape[:2]
    logger.info(f"调整之后的图片大小为：：：{resized_size}")
    np_image = cv2.cvtColor(np_image, cv2.COLOR_BGR2RGB)

    # 初始化一个计数器，用于统计彩色像素的数量
    color_n = 0

    # 遍历图片的每个像素
    for row in np_image:
        for pixel in row:
            # 计算R, G, B值之间的最大差异
            max_diff = np.max(pixel) - np.min(pixel)
            # 如果差异小于阈值，则认为这是一个黑白像素
            if max_diff > threshold:
                color_n += 1
    
    # 计算总的像素数量
    total_pixels = np_image.shape[0] * np_image.shape[1]

    proportion = color_n / total_pixels
    logger.info(f"彩色像素点的个数为：{color_n};  总像素点个素为：{total_pixels}; 彩色像素点占比为：{round(proportion, 4)}")

    # 如果大部分像素是黑白像素，则认为图片是黑白的
    if proportion > 0.020:
        logger.info("图片为彩色图片")
        return 1, round(proportion, 4)
    else:
        logger.info("图片为黑白图片")
        return 0, round(proportion, 4)
    
    
def judge_black_and_white_photos_by_LLM(image_path:str="", image_url = "" ):
    """
    Discribe:判断图片是否为黑白图片
    Args:
        image_path (str): 图片路径
        threshold (int): 阈值. Defaults to 50.
    return:
        int: 0为黑白图片，1为彩色图片, 2为LLM判断出错或者dify内部错误.
    """
    if image_path == "" and image_url == "":
        raise Exception("image_path and image_url can't be empty at the same time")
    elif image_path != "" and image_url != "":
        raise Exception("image_path and image_url can't be not empty at the same time")

    elif image_path == "" and image_url != "" and image_url.startswith("http"):
        judged_result = dify.judge_image(url = image_url)

        logger.info("输入的图片为url")
    # NOTE: 本地图片的处理还需要完整，目前暂无此功能
    elif image_path.split("/")[-1].split(".")[-1] in ["jpg", "png", "jpeg"]:
        logger.info("图片为本地")
        np_image = cv2.imread(image_path)
    else:
        raise Exception("请检查图片的格式")
    
    if judged_result == "color":
        logger.info("图片为彩色图片")
        return 1
    elif judged_result == "grey":
        logger.info("图片为黑白图片")
        return 0
    else:
        logger.info("LLM 判断出错 or dify内部错误")
        return 2
    
 
def isBlackWhite(image_path:str="", base64_image:str="", threshold:int = 50):
    """
    Discribe:判断图片是否为灰度照片
    Args:
        image_path (str): 图片路径
        threshold (int): 阈值. Defaults to 50.
    return:
        int: 0为灰度照片，1为彩色照片.
    """
    if image_path == "" and base64_image == "":
        raise Exception("image_path and image_base64 can't be empty at the same time")
    elif image_path != "" and base64_image != "":
        raise Exception("image_path and image_base64 can't be not empty at the same time")

    elif image_path == "" and base64_image != "":
        # 将base64图片转换为numpy数组
        np_image = cv2.imdecode(np.frombuffer(
            base64.b64decode(base64_image),
            np.uint8),
            cv2.IMREAD_COLOR)
        
        logger.info("输入的图片数据为base64格式")

    elif image_path.split("/")[-1].split(".")[-1] in ["jpg", "png", "jpeg"]:
        logger.info("图片为本地路径格式")
        np_image = cv2.imread(image_path)
    else:
        raise Exception("请检查图片的格式")
    
    # 根据图片的最长边将图片缩放到指定大小
    # 计算图片的长宽
    origin_size = np_image.shape[:2]
    height, width = origin_size
    logger.info(f"原始的图片大小为：：：：：{origin_size}")
    if height >= width:
        scale_rate = 512/height
        scaled_width = int(width*scale_rate)
        np_image = cv2.resize(np_image, (scaled_width, 512))
    else:
        scale_rate = 512/width
        scaled_height = int(height*scale_rate)
        np_image = cv2.resize(np_image, (512, scaled_height))

    resized_size = np_image.shape[:2]
    logger.info(f"调整之后的图片大小为：：：{resized_size}")
    np_image = cv2.cvtColor(np_image, cv2.COLOR_BGR2RGB)
 


    red_channel = np_image[:, :, 0]
    green_channel = np_image[:, :, 1]
    blue_channel = np_image[:, :, 2]

    diff1 = np.var(red_channel-green_channel)
    diff2 = np.var(red_channel-blue_channel)
    diff3 = np.var(green_channel-blue_channel)

    diff_sum = (diff1 + diff2 + diff3) / 3.0

    if diff_sum <= threshold:
        return "grey"
    else:
        return "color"
