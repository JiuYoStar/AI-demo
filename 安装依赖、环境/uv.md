###  解释器

```shell
➜  uv uv python find 3.12
/Users/lingk/.local/share/uv/python/cpython-3.12.12-macos-aarch64-none/bin/python3.12
# 使用uv的时候, 指向当前环境中的py
/Users/lingk/work/py/demo/AI-Test/.venv/bin/python
```





## 1. 安装 uv

在 macOS / Linux / Windows（含 WSL）下均可：

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

验证安装：

```bash
uv --version
```

---

## 2. 创建新项目

1. 创建项目目录：

```bash
mkdir my-agent
cd my-agent
```

2. 安装指定 Python 版本（uv 会自动下载并缓存）：

```bash
uv python install 3.12
```

3. 创建虚拟环境：

```bash
uv venv
```

虚拟环境目录 `.venv/` 会在项目下生成。

---



**uv init** : 初始化一下, 否则安装不上

## 3. 安装依赖

1. 安装单个依赖：

```bash
uv add fastapi
uv add openai
uv add langchain
```

2. 查看已安装依赖树：

```bash
uv tree
```

3. 安装多个依赖：

```bash
uv add requests pydantic numpy
```

---

## 4. 导出依赖

将当前项目依赖导出为 `requirements.txt`：

```bash
uv export > requirements.txt
```

从 `requirements.txt` 安装依赖（可用于其他机器或部署环境）：

```bash
uv sync requirements.txt
```

---

## 5. 运行项目

直接运行 Python 脚本：

```bash
uv run python app/main.py
```

运行 FastAPI / Uvicorn 项目：

```bash
uv run uvicorn app.main:app --reload
```

---

## 6. 虚拟环境操作

激活虚拟环境（macOS / Linux）：

```bash
source .venv/bin/activate
```

Windows：

```bash
.venv\Scripts\activate
```

退出虚拟环境：

```bash
deactivate
```

---

## 7. 同步项目依赖

在团队协作或迁移项目时，使用锁文件 `uv.lock` 保证依赖一致：

```bash
uv sync
```

此命令会自动安装 `uv.lock` 中锁定的版本。

---

## 8. 总结

* `uv` 集成了 Python 版本管理、虚拟环境管理和依赖管理。
* 适合多项目隔离、快速启动、Agent 开发和部署。
* 配合 `uv.lock` 或 `requirements.txt` 可轻松在其他机器同步环境。