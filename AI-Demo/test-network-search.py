import os
from openai import OpenAI
# 从环境变量中，获取 DASHSCOPE_API_KEY
api_key = os.environ.get('DASHSCOPE_API_KEY')
# print('api_key -> ', api_key)

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=api_key,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",  # 填写DashScope服务的base_url
)
completion = client.chat.completions.create(
    model="qwen-plus",  # 此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    messages=[
        {'role': 'system', 'content': 'You are a helpful assistant.'},
        {'role': 'user', 'content': '中国队在巴黎奥运会获得了多少枚金牌'}],
    extra_body={
        "enable_search": True
    }
)
print(completion.model_dump_json())

'''
# 额外的参数, 不同的模型支持的参数也不一样, 需要查看模型文档
extra_body={
    "enable_search": True,           # 启用联网搜索
    "result_format": "message",      # 返回格式
    "incremental_output": False,     # 是否流式输出
    "stop": ["END"],                 # 停止词
}

# ✅ 适合使用联网搜索的场景：
# - 需要实时信息（新闻、股价、天气）
# - 通用知识查询（历史事件、名人资料）
# - 快速原型开发

# ❌ 不适合使用联网搜索的场景：
# - 需要调用企业内部 API
# - 需要访问数据库
# - 需要精确控制数据源
# - 对隐私敏感的场景（搜索会发送到外部）
'''
