# import os
from openai import OpenAI

client = OpenAI(
    # api_key=os.getenv("DASHSCOPE_API_KEY"),
    api_key='sk-7dea7af8f1824bedab1a176e92e42fe6',
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"  # 百炼服务的base_url
)

completion = client.embeddings.create(
    model="text-embedding-v4",
    input='我想知道迪士尼的退票政策',
    dimensions=1024, # 指定向量维度（仅 text-embedding-v3及 text-embedding-v4支持该参数）
    encoding_format="float"
)

print(completion.model_dump_json())


# {"data":[{"embedding":[0.0026341788470745087,-0.03762197867035866, ...,-0.047639328986406326,-0.03625597432255745],"index":0,"object":"embedding"}],"model":"text-embedding-v4","object":"list","usage":{"prompt_tokens":8,"total_tokens":8},"id":"e198e2e1-3c27-4839-b7a1-4d54ea0d9652"}
