# 🚀 快速启动指南

## 📦 安装依赖

```bash
cd /Users/lingk/work/py/demo/test
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 🎯 运行应用

### 方式1: 使用 Flask CLI (推荐) ⭐

```bash
# 简单运行(已配置.flaskenv)
flask run

# 或指定应用
flask --app app run

# 调试模式
flask run --debug

# 指定端口
flask run -p 8080
```

### 方式2: 使用 Python

```bash
python run.py
```

## 🔍 查看路由

```bash
# 列出所有路由
flask routes

# 或在Python中
python -c "from app import app; [print(f'{r.endpoint:35s} {r.rule}') for r in app.url_map.iter_rules()]"
```

## 🧪 测试应用

```bash
# 运行测试脚本
python test_blueprints.py

# 手动测试
curl http://127.0.0.1:5000/
curl http://127.0.0.1:5000/user/
curl http://127.0.0.1:5000/admin/dashboard
curl http://127.0.0.1:5000/api/v1/posts
curl http://127.0.0.1:5000/product/list
```

## 📚 查看文档

```bash
# 在浏览器中打开
open document/README.md

# 或使用命令行
cat document/README.md
```

## 🛠️ 常用命令

```bash
# 进入Flask Shell
flask shell

# 查看应用配置
flask shell
>>> app.config

# 探索API
python explore_api.py

# 查看蓝图
python -c "from app import app; print(list(app.blueprints.keys()))"
```

## 📁 项目结构

```
test/
├── app/                  # 应用主目录
│   ├── __init__.py      # Flask应用实例
│   ├── views.py         # 主路由
│   ├── auth.py          # 认证路由
│   └── blueprints/      # 蓝图目录(自动注册)
│       ├── user.py      # 用户蓝图
│       ├── admin.py     # 管理员蓝图
│       ├── api.py       # API蓝图
│       └── product.py   # 产品蓝图
├── document/            # 文档目录
├── run.py              # 启动脚本
├── test_blueprints.py  # 测试脚本
├── .flaskenv           # Flask环境配置
└── requirements.txt    # 依赖列表
```

## ✨ 核心特性

- ✅ **自动注册蓝图**: 在 `app/blueprints/` 创建文件即可
- ✅ **Flask CLI支持**: 使用 `flask run` 命令
- ✅ **调试模式**: 代码修改自动重载
- ✅ **API版本控制**: v1和v2共存
- ✅ **完整文档**: 详细的使用手册

## 🎓 学习资源

| 文档 | 说明 |
|------|------|
| [README.md](document/README.md) | 项目介绍 |
| [Blueprint蓝图使用手册.md](document/Blueprint蓝图使用手册.md) | 蓝图教程 |
| [自动注册蓝图说明.md](document/自动注册蓝图说明.md) | 自动注册功能 |
| [Flask命令行使用.md](document/Flask命令行使用.md) | CLI使用指南 |
| [Flask-API快速参考.md](document/Flask-API快速参考.md) | API参考 |

## 🐛 故障排查

### 问题: ModuleNotFoundError

```bash
# 确保激活虚拟环境
source venv/bin/activate
pip install -r requirements.txt
```

### 问题: 端口被占用

```bash
# 使用其他端口
flask run -p 8080

# 或杀死占用进程
lsof -ti:5000 | xargs kill -9
```

### 问题: IDE显示导入错误

参考: [document/IDE配置说明.md](document/IDE配置说明.md)

---

**快速开始**: `source venv/bin/activate && flask run` 🎉

