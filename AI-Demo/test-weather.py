import json
import os
import dashscope
from dashscope.api_entities.dashscope_response import Role

# 从环境变量中，获取 DASHSCOPE_API_KEY
api_key = os.environ.get('DASHSCOPE_API_KEY')
dashscope.api_key = api_key

# 编写你的天气函数
# 为了演示流程，这里指定了天气的温度，实际上可以调用 高德接口获取实时天气。
# 这里可以先用每个城市的固定天气进行返回，查看大模型的调用情况
def get_current_weather(location, unit="摄氏度"):
    # 获取指定地点的天气
    temperature = -1
    if '上海' in location or 'Shanghai' in location:
        temperature = 10
    if '北京' in location or 'Beijing' in location:
        temperature = 36
    if '西安' in location or 'Xi\'an' in location:
        temperature = 37
    weather_info = {
        "location": location,
        "temperature": temperature,
        "unit": unit,
        "forecast": ["晴天", "微风"],
    }
    return json.dumps(weather_info)

# 封装模型响应函数
def get_response(messages):
    try:
        '''
        **关键点：**
        - `functions` 传递的是函数的**描述信息**（JSON Schema），不是可执行的函数代码
        - 大模型看到的是函数的"使用说明书"，而不是实际代码
        - 模型根据这些说明书**决定**是否调用、调用哪个、传什么参数
        '''
        response = dashscope.Generation.call(
            model='qwen-max',
            messages=messages,
            functions=functions, # 添加函数 -> 传递的函数描述,并非函数本身
            result_format='message' # 将输出设置为message形式
        )
        return response
    except Exception as e:
        print(f"API调用出错: {str(e)}")
        return None

# 使用function call进行QA
def run_conversation():
    query = "天津的天气怎样"
    messages=[{"role": "user", "content": query}]

    # 得到第一次响应
    response = get_response(messages)
    if not response or not response.output:
        print("获取响应失败")
        return None

    print('response=', response)
    '''
      response ->
      {
        "finish_reason": "function_call",  // 表示模型决定调用函数
        "message": {
          "role": "assistant",
          "content": "",
          "function_call": {
            "name": "get_current_weather",
            "arguments": "{\"location\": \"天津\", \"unit\": \"celsius\"}"
          }
        }
      }
    '''

    message = response.output.choices[0].message
    messages.append(message)
    print('message=', message)

    # Step 2, 判断用户是否要call function
    if hasattr(message, 'function_call') and message.function_call:
        function_call = message.function_call
        tool_name = function_call['name']
        # Step 3, 执行function call
        arguments = json.loads(function_call['arguments'])
        print('arguments=', arguments)
        tool_response = get_current_weather(
            location=arguments.get('location'),
            unit=arguments.get('unit'),
        )
        tool_info = {"role": "function", "name": tool_name, "content": tool_response}
        print('tool_info=', tool_info)
        messages.append(tool_info)
        print('messages=', messages)

        #Step 4, 得到第二次响应
        response = get_response(messages)
        if not response or not response.output:
            print("获取第二次响应失败")
            return None

        print('response=', response)
        message = response.output.choices[0].message
        return message
    return message

# 这个地方的description，我先用的英文，你可以动手改成中文试试
functions = [
    {
      'name': 'get_weather',
      'description': 'Get current weather',
      'parameters': {
            'properties': {
                'location': {'type': 'string', 'description': 'City'},
                'unit': {'type': 'string', 'enum': ['celsius', 'fahrenheit']}
            },
        'required': ['location']
      }
    }
]
# 预估 tokens: ~65-75（节省 40-50%）
# ✅ 平衡：既省 token 又保持清晰

if __name__ == "__main__":
    print(dashscope.api_key)
    result = run_conversation()
    if result:
        print("最终结果:", result)
    else:
        print("对话执行失败")

'''
response= {"status_code": 200, "request_id": "f5d853ee-2194-4c76-b85c-09a319634b40", "code": "", "message": "", "output": {"text": null, "finish_reason": null, "choices": [{"finish_reason": "function_call", "message": {"role": "assistant", "content": "", "function_call": {"arguments": "{\"location\": \"天津\", \"unit\": \"celsius\"}", "name": "get_current_weather"}}, "index": 0}]}, "usage": {"input_tokens": 275, "output_tokens": 25, "prompt_tokens_details": {"cached_tokens": 0}, "total_tokens": 300}}
message= {"role": "assistant", "content": "", "function_call": {"arguments": "{\"location\": \"天津\", \"unit\": \"celsius\"}", "name": "get_current_weather"}}
arguments= {'location': '天津', 'unit': 'celsius'}
tool_info= {'role': 'function', 'name': 'get_current_weather', 'content': '{"location": "\\u5929\\u6d25", "temperature": -1, "unit": "celsius", "forecast": ["\\u6674\\u5929", "\\u5fae\\u98ce"]}'}
messages= [{'role': 'user', 'content': '天津的天气怎样'}, Message({'role': 'assistant', 'content': '', 'function_call': {'arguments': '{"location": "天津", "unit": "celsius"}', 'name': 'get_current_weather'}}), {'role': 'function', 'name': 'get_current_weather', 'content': '{"location": "\\u5929\\u6d25", "temperature": -1, "unit": "celsius", "forecast": ["\\u6674\\u5929", "\\u5fae\\u98ce"]}'}]
response= {"status_code": 200, "request_id": "e5066c75-e0c9-4d3c-91cb-7ecef1befc33", "code": "", "message": "", "output": {"text": null, "finish_reason": null, "choices": [{"finish_reason": "stop", "message": {"role": "assistant", "content": "天津现在的天气是晴天，温度是-1°C，微风。"}, "index": 0}]}, "usage": {"input_tokens": 361, "output_tokens": 19, "prompt_tokens_details": {"cached_tokens": 0}, "total_tokens": 380}}
最终结果: {"role": "assistant", "content": "天津现在的天气是晴天，温度是-1°C，微风。"}
'''
