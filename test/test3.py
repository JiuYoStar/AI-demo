import os
from openai import OpenAI
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()

print("DASHSCOPE_API_KEY:", os.getenv("DASHSCOPE_API_KEY"))

# client = OpenAI(
#     # 从环境变量中读取API Key
#     api_key=os.getenv("DASHSCOPE_API_KEY"),
#     base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
# )
# completion = client.chat.completions.create(
#     model="qwen-plus",  # 此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
#     messages=[{'role': 'system', 'content': 'You are a helpful assistant.'},
#                 {'role': 'user', 'content': '你是谁？'}],
#     stream=True,
#     stream_options={"include_usage": True}
#     )
# for chunk in completion:
#     print(chunk.model_dump_json())
