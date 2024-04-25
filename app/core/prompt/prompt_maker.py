import openai
import webbrowser
import urllib.request
import requests
from fastapi import Depends

import os


import app.core.api
from app.core.api import util_api


def get_system_prompt():
    system_prompt = "금융 상품을 고르는 상황 예시를 들어서 어려운 금융 지식을 각 문장의 글자 수가 50자 이내인 총 6문장으로 요약하여 고등학생에게 이야기를 들려주듯이 알려줍니다. "
    return system_prompt


def get_user_prompt():
    user_prompt = "투자, 세금, 저축 중 하나만 골라 주제를 정하고, 그 주제에 관한 구체적 상품 예시 하나를 들고 설명과 장단점 알려줘."
    return user_prompt


async def create_prompt(api_key):
    api_url, headers, data = util_api(api_key, "gpt-4", get_system_prompt(), get_user_prompt())

    response = requests.post(api_url, headers=headers, json=data)

    if response.status_code == 200:
        response_data = response.json()
        return response_data.get("choices", [{}])[0].get("message", {}).get("content", "")
    else:
        return f"Error: {response.status_code}, {response.text}"




