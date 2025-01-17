# -*- coding: utf-8 -*-
import requests
import json
import uuid
from utils.log_helper import Log_Helper
import time

logger = Log_Helper(logger_name = "dify_llm",logger_level ="INFO")

class Dify:
    def __init__(self, api_key="app-TNobQJKHkUjj7vTUlg3FG5dA"):
        self.api_key = api_key
        self.url = 'http://14.29.175.216:8123/v1/workflows/run'

    def creat_uuid(self):
        return str(uuid.uuid4())
    
    def get_response_message(self, userid= "xxxx", inputs:dict={}, url:str=""): 
        """
        conversation_id: 非必需参数
        """
        userid = str(userid)
        response = requests.post(
            url = self.url,
            headers={'Authorization': f'Bearer {self.api_key}', 
                    'Content-Type': 'application/json'},
            json = {
            "inputs": inputs,
            "response_mode": "blocking",
            "user": userid,
            "files": [      {
        "type": "image",
        "transfer_method": "remote_url",
        "url": url
        # "upload_file_id": self.creat_uuid(),
      }],
            }
                    )
        logger.info(f"========= judge image by dify LLM ==========")
        # print("response: ", response.text)
        return response

    def handle_response(self, response: requests.Response):
        response = response.content.decode('utf-8')
        if response:
            response_dict = json.loads(response)
            if response_dict["data"].get("status", "") == "succeeded":
                judged_result = response_dict["data"]["outputs"]["result"]
            else:
                logger.error("dify response is not succeeded")
                logger.error(f"respond content: {response_dict}")
                judged_result = "error"
                           
            
        else:
            logger.error("dify response is empty")
            raise Exception("dify internal server error")

        return judged_result
    
    def judge_image(self, url:str):
        start_time = time.time()
        response = self.get_response_message(url = url)
        end_time = time.time()
        spended_time = end_time - start_time
        logger.info(f"========= the time judgging image by vision LLM is {spended_time} =========")
        return self.handle_response(response)



if __name__ == '__main__':
    dify = Dify()
    # response = dify.get_response_message(userid= "xxxx", url = "https://xinggeai.oss-cn-hangzhou.aliyuncs.com/comfyui-code/output/ComfyUI_00000000_172527212237042_409a0c19-22c8-4682-9ba3-b26701bb83a4_.png")
    print(dify.judge_image(url = "https://xinggeai.oss-cn-hangzhou.aliyuncs.com/comfyui-code/output/ComfyUI_00000000_172527212237042_409a0c19-22c8-4682-9ba3-b26701bb83a4_.png"))

