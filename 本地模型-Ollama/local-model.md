# ========== M1Max - 32GB 内存配置 ==========
推荐模型大小：
├── 7B 模型（最佳体验）
│   ├── Qwen2.5-7B ✅✅✅
│   ├── DeepSeek-R1-Distill-Qwen-7B ✅✅✅
│   └── Llama-3.1-8B ✅✅✅
│
├── 14B 模型（良好体验）
│   ├── Qwen2.5-14B ✅✅
│   └── DeepSeek-Coder-V2-Lite-Instruct ✅✅
│
└── 32B 模型（勉强可用，需要量化）
    ├── Qwen2.5-32B（需要 4-bit 量化）⚠️
    └── DeepSeek-V3（太大，不推荐）❌

# ========== M1Max - 64GB 内存配置 ==========
推荐模型大小：
├── 7B-14B 模型（极佳体验）✅✅✅
├── 32B 模型（良好体验）✅✅
├── 72B 模型（可用，需要量化）✅
└── 100B+ 模型（不推荐）❌



# 模型内存占用估算

# Float16（半精度）
模型大小(GB) = 参数量(B) × 2 bytes

# 4-bit 量化
模型大小(GB) = 参数量(B) × 0.5 bytes

# 示例：
Qwen2.5-7B:
  - Float16: 7B × 2 = 14GB
  - 4-bit: 7B × 0.5 = 3.5GB

Qwen2.5-32B:
  - Float16: 32B × 2 = 64GB（超过 32GB 内存！）
  - 4-bit: 32B × 0.5 = 16GB ✅

# 实际运行还需要额外内存：
总需求 = 模型大小 + 上下文内存(2-4GB) + 系统开销(4-6GB)
```

### 推荐配置表

| 内存大小 | 推荐模型 | 量化方式 | 体验 |
|---------|---------|---------|------|
| **32GB** | 7B | Float16 | ⭐⭐⭐⭐⭐ 完美 |
| **32GB** | 14B | Float16 | ⭐⭐⭐⭐ 流畅 |
| **32GB** | 32B | 4-bit | ⭐⭐⭐ 可用 |
| **64GB** | 7B | Float16 | ⭐⭐⭐⭐⭐ 极快 |
| **64GB** | 32B | Float16 | ⭐⭐⭐⭐⭐ 完美 |
| **64GB** | 72B | 4-bit | ⭐⭐⭐⭐ 流畅 |

## 方案 1：使用 Ollama（强烈推荐 macOS）

### 为什么 Ollama 最适合 macOS？
```
✅ 原生支持 Apple Silicon（Metal 加速）
✅ 自动管理内存和量化
✅ 安装极其简单
✅ 性能优化最好
✅ 支持 M1/M2/M3 芯片



| 项目     | Ollama 模型 (GGUF)              | Transformers / ModelScope 模型 (safetensors / bin) |
| -------- | ------------------------------- | -------------------------------------------------- |
| 文件后缀 | `.gguf`                         | `.safetensors` 或 `.bin`                           |
| 底层框架 | llama.cpp                       | PyTorch / TensorFlow                               |
| 优化目的 | 轻量、CPU/GPU都能运行、量化压缩 | 高精度训练、推理（未量化）                         |
| 加载库   | `ollama` 或 `llama.cpp`         | `transformers` / `modelscope`                      |