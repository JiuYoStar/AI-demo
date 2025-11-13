# 🐍 Python venv + requirements.txt 最佳实践

## 1️⃣ 创建虚拟环境

进入项目目录：

```bash
python -m venv .venv   # 推荐放在项目下，目录名用 .venv
```

目录结构：

```
myproject/
  ├── .venv/           # 虚拟环境（不要提交到 git）
  ├── requirements.txt
  └── app.py
```

---

## 2️⃣ 激活环境

```bash
# macOS / Linux
source .venv/bin/activate

# Windows (cmd)
.venv\Scripts\activate

# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

提示符前会出现 `(.venv)`，表示已进入虚拟环境。
退出：

```bash
deactivate
```

---

## 3️⃣ 安装依赖

```bash
pip install requests flask
```

---

## 4️⃣ 导出依赖

```bash
pip freeze > requirements.txt
```

示例文件：

```
flask==2.3.3
requests==2.31.0
```

---

## 5️⃣ 在新环境安装依赖

```bash
pip install -r requirements.txt
```

---

## 6️⃣ Git 管理

在 `.gitignore` 里忽略 `.venv/`：

```
.venv/
```

👉 只提交 `requirements.txt`，保证依赖可复现。

---

## 7️⃣ 部署服务器（常见流程）

```bash
git clone https://xxx/myproject.git
cd myproject
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

---

## ✅ 总结

* 每个项目用独立 `.venv/`，保证依赖隔离
* 所有依赖都写到 `requirements.txt`，保证可复现
* 部署时只需：**建环境 + 激活 + 安装依赖**



# 中大型项目, 可以使用 Poetry
