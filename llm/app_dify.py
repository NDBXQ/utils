# -*- coding: utf-8 -*-
import requests
import asyncio
import aiohttp
from utils.log_helper import Log_Helper

logger = Log_Helper(logger_name = "dify_llm",logger_level ="INFO")

class Dify:
    def __init__(self, api_key="app-TNobQJKHkUjj7vTUlg3FG5dA"):
        self.api_key = api_key
        self.url = 'http://14.29.175.216:8123/v1/workflows/run'

    async def get_response_message(self, userid= "xxxx", inputs:dict={}):
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f'Bearer {self.api_key}',
                "Content-Type": "application/json"
            }
            payload = {
            "inputs": inputs,
            "response_mode": "blocking",
            "user": userid,
            }
            async with session.post(url=self.url, json=payload, headers=headers) as resp:
                response:dict = await resp.json()
                return response
            

