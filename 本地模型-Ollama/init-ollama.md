1. 本地 Ollama 接入说明
2. Python / Node.js 使用示例
3. cURL 测试
4. 一个 **封装好的 Python Client 类**（支持切换模型）

------

# 📘 Ollama 本地接入指南

## 1. 确认本地模型

查看你本地已经安装的模型：

```bash
ollama list
```

示例输出：

```
NAME               ID              SIZE      MODIFIED
qwen3:14b          bdbd181c33f2    9.3 GB    4 months ago
llama3.2:latest    a80c4f17acd5    2.0 GB    4 months ago
```

------

## 2. 启动服务

Ollama 默认会在后台监听 `http://localhost:11434`，如需手动启动：

```bash
ollama serve
# 查看端口占用情况（看下被哪个服务占用了，默认的ollama是11434）
lsof -i :11434
```

API 入口为：

```shell
http://localhost:11434/v1

# 列出本地模型
curl http://127.0.0.1:11434/v1/models

# 请求示例
curl -N http://127.0.0.1:11434/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3.2:latest",
    "messages": [
      {"role": "user", "content": "介绍一下Node.js"}
    ]
  }'


```

------

## 3. Python 接入

### 安装依赖

```bash
pip install openai
```

### 简单调用示例

```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

response = client.chat.completions.create(
    model="qwen3:14b",
    messages=[{"role": "user", "content": "写一个 Python 打印九九乘法表的程序"}],
)

print(response.choices[0].message["content"])
```

⚠️ 注意：

- `api_key` 本地不验证，可以随便写，例如 `"ollama"`。
- `model` 要与 `ollama list` 中的模型名称一致。

------

## 4. Node.js / JavaScript 接入

### 安装依赖

```bash
npm install openai
```

### 示例

```javascript
import OpenAI from "openai";

const client = new OpenAI({
  baseURL: "http://localhost:11434/v1",
  apiKey: "ollama", // 本地不验证，可以随便写
});

const response = await client.chat.completions.create({
  model: "llama3.2:latest",
  messages: [{ role: "user", content: "写一个 JS 版斐波那契函数" }],
});

console.log(response.choices[0].message.content);
```

------

## 5. cURL 测试

快速确认服务正常：

```bash
curl http://localhost:11434/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen3:14b",
    "messages": [{"role": "user", "content": "Hello, Ollama!"}]
  }'
```

------

## 6. 封装好的 Python Client 类

```python
from openai import OpenAI

class OllamaClient:
    def __init__(self, base_url="http://localhost:11434/v1", api_key="ollama"):
        self.client = OpenAI(base_url=base_url, api_key=api_key)
        self.model = None

    def set_model(self, model_name: str):
        """切换当前模型"""
        self.model = model_name

    def chat(self, prompt: str, system: str = None) -> str:
        """发送对话请求"""
        if not self.model:
            raise ValueError("请先调用 set_model() 设置模型")
        
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )
        return response.choices[0].message["content"]

# 使用示例
if __name__ == "__main__":
    ollama = OllamaClient()
    
    # 切换到 qwen3:14b
    ollama.set_model("qwen3:14b")
    print(ollama.chat("用 Python 打印九九乘法表"))
    
    # 切换到 llama3.2:latest
    ollama.set_model("llama3.2:latest")
    print(ollama.chat("用 JavaScript 写一个快速排序函数"))
```

------

## 7. 总结

- Ollama 提供 OpenAI 兼容 API，本地默认端口：`http://localhost:11434/v1`
- `api_key` 本地环境不校验，可随便填
- Python 和 Node.js 都能直接使用 `openai` SDK 调用
- 封装类可方便切换不同模型（如 `qwen3:14b`、`llama3.2:latest`）

------

要不要我帮你把这个 `.md` 文件导出成一个 **可下载的 Markdown 文件**，这样你直接存到本地就能随时打开？