# VLLM 本地 Mac 使用指南 (M1 Max 32GB)

本文档总结了在 Mac M1 Max 32GB 上使用 VLLM 本地跑 Qwen-7B 模型的完整流程，包括安装、下载模型、启动、调试、关闭和重启。

------

## 1. 安装环境

1.  **安装 Python 3.11+**（推荐使用 pyenv 管理版本）

    ```bash
    pyenv install 3.11.7
    pyenv global 3.11.7
    python --version
    ```

2.  **安装虚拟环境**

    ```bash
    python -m venv vllm_env
    source vllm_env/bin/activate
    ```

3.  **升级 pip**

    ```bash
    pip install --upgrade pip setuptools wheel
    ```

4.  **安装 VLLM**

    ```bash
    pip install vllm
    ```

5.  **安装 PyTorch 支持 MPS**（Apple GPU）

    ```bash
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
    ```

------

## 2. 下载模型 (Qwen-7B)

### 方法 1：Hugging Face

1.  注册 Hugging Face，获取访问权限（部分模型需要 token）。

2.  使用 `transformers-cli` 下载模型：

    ```bash
    pip install huggingface_hub
    huggingface-cli login
    # 需要先在 Hugging Face 网站获取 token (Settings -> Access Tokens)
    git lfs install
    # 必须使用 brew安装,否则安装的model是空的
    git clone https://huggingface.co/DeepSeekAI/Qwen-7B
    ```

### 方法 2：ModelScope（国内镜像）

```bash
git clone https://modelscope.cn/models/deepseek-ai/DeepSeek-R1-Distill-Qwen-7B
```

**注意**：为了减少内存占用，建议下载 **FP16 或 Int4/Int8 量化模型**。

------

## 3. 启动 VLLM

```python
from vllm import LLM, SamplingParams

# 指定模型路径和设备为 MPS
llm = LLM(model="/path/to/Qwen-7B", device="mps")

# 测试生成
response = llm.generate(
    "Hello, VLLM on Mac M1 Max!",
    sampling_params=SamplingParams(max_tokens=50)
)
print(response)

'''
python -c "import torch; print(torch.cuda.is_available(), torch.backends.mps.is_available())"
>>> False True  >>> 当前的环境有GPU但是vllm没有使用(Mac GPU不支持)

'''
```

### 说明：

-   `device="mps"`：使用 Mac GPU
-   `max_tokens`：控制生成长度

------

## 4. 调试常用技巧

1.  **查看设备状态**

```python
import torch
print(torch.backends.mps.is_available())
print(torch.backends.mps.is_built())
```

1.  **控制生成速度和显存**
    -   减少 `batch_size`
    -   使用 `int4` 或 `int8` 量化模型
2.  **开启日志**

```bash
export VLLM_LOG_LEVEL=DEBUG
```

或在 Python 中：

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

------

## 5. 关闭 VLLM

```python
llm.close()
```

-   释放 GPU 内存
-   必须在退出程序前调用

------

## 6. 重启 VLLM

1.  关闭实例：

```python
llm.close()
```

1.  再次初始化：

```python
llm = LLM(model="/path/to/Qwen-7B", device="mps")
```

1.  测试生成确认可用

------

## 7. 常见问题

| 问题       | 解决方案                                  |
| ---------- | ----------------------------------------- |
| 内存不足   | 使用 Int4/Int8 量化模型，降低 batch_size  |
| 模型加载慢 | 量化模型 + 存在本地 SSD                   |
| MPS 不可用 | 确认 PyTorch >= 2.1 并使用 `device="mps"` |

------

## 8. 参考资料

-   [VLLM 官方文档](https://vllm.readthedocs.io/)
-   [PyTorch MPS 支持](https://pytorch.org/docs/stable/notes/mps.html)
-   [Qwen 模型 Hugging Face 页面](https://huggingface.co/DeepSeekAI/Qwen-7B)
