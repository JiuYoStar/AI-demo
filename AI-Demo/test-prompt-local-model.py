# from modelscope import AutoModelForCausalLM, AutoTokenizer

# model_name = "/Users/lingk/work/py/vllm/deepseek-ai/DeepSeek-R1-Distill-Qwen-7B"
# model = AutoModelForCausalLM.from_pretrained(
#     model_name,
#     torch_dtype="auto",
#     device_map="cuda" # auto
# )
# tokenizer = AutoTokenizer.from_pretrained(model_name)
# prompt = "帮我写一个二分查找法"
# messages = [
#     {"role": "system", "content": "You are a helpful assistant."},
#     {"role": "user", "content": prompt}
# ]
# text = tokenizer.apply_chat_template(
#     messages,
#     tokenize=False,
#     add_generation_prompt=True
# )
# model_inputs = tokenizer([text], return_tensors="pt").to(model.device)
# generated_ids = model.generate(
#     **model_inputs,
#     max_new_tokens=2000
# )
# generated_ids = [
#     output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
# ]
# response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
# print(response)


import requests

# 本地 Ollama API 地址
url = "http://localhost:11434/v1/chat/completions"
headers = {"Content-Type": "application/json"}

# 你本地 Ollama 安装的模型名称，比如 qwen3:14b 或 llama3.2:latest
model_name = "qwen3:14b"

prompt = "帮我写一个二分查找法"
messages = [
    {"role": "system", "content": "????"},
    {"role": "user", "content": prompt}
]

data = {
    "model": model_name,
    "messages": messages,
    "max_tokens": 2000  # 生成最大 token 数
}

response = requests.post(url, json=data, headers=headers)
result = response.json()

# 输出模型生成的回答
# Ollama 返回格式中，生成内容通常在 result['choices'][0]['message']['content']
answer = result["choices"][0]["message"]["content"]
print(answer)
