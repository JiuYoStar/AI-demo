# Flask 命令行使用指南

## 🎯 Flask CLI 简介

Flask提供了强大的命令行工具,可以通过 `flask` 命令来管理和运行应用。

## 🚀 运行应用的多种方式

### 方式1: 使用 `python run.py` (传统方式)

```bash
cd /Users/lingk/work/py/demo/flask-demo1
source venv/bin/activate
python run.py
```

**优点**:
- ✅ 简单直观
- ✅ 可以自定义启动参数
- ✅ 适合初学者

**缺点**:
- ❌ 需要创建 `run.py` 文件
- ❌ 功能相对有限

### 方式2: 使用 `flask run` (推荐)

```bash
cd /Users/lingk/work/py/demo/flask-demo1
source venv/bin/activate
flask --app app run
```

**优点**:
- ✅ Flask官方推荐
- ✅ 功能强大,选项丰富
- ✅ 支持自动重载和调试
- ✅ 不需要 `run.py` 文件

**缺点**:
- ❌ 需要指定应用位置

### 方式3: 使用环境变量

```bash
export FLASK_APP=app
export FLASK_DEBUG=1
flask run
```

**优点**:
- ✅ 命令简短
- ✅ 可以在 `.env` 文件中配置

## 📋 Flask CLI 常用命令

### 1. 运行开发服务器

```bash
# 基本运行
flask --app app run

# 启用调试模式
flask --app app run --debug

# 指定主机和端口
flask --app app run --host=0.0.0.0 --port=8080

# 禁用自动重载
flask --app app run --no-reload

# 禁用调试器
flask --app app run --no-debugger

# 组合使用
flask --app app run --debug --host=0.0.0.0 --port=8080
```

### 2. 查看路由

```bash
# 列出所有路由
flask --app app routes

# 输出示例:
# Endpoint              Methods  Rule
# --------------------  -------  -----------------------
# index                 GET      /
# login                 GET      /login
# user.user_index       GET      /user/
# user.user_profile     GET      /user/profile
# admin.admin_dashboard GET      /admin/dashboard
```

### 3. 进入Shell环境

```bash
# 启动交互式Shell
flask --app app shell

# 在Shell中可以直接使用app对象
>>> from flask import current_app
>>> current_app.url_map
>>> for rule in current_app.url_map.iter_rules():
...     print(rule)
```

### 4. 自定义命令

可以在应用中添加自定义命令:

```python
# app/__init__.py
import click

@app.cli.command()
def init_db():
    """初始化数据库"""
    click.echo('Initializing database...')
    # 数据库初始化代码
    click.echo('Database initialized!')

@app.cli.command()
@click.argument('name')
def greet(name):
    """问候命令"""
    click.echo(f'Hello, {name}!')
```

使用自定义命令:

```bash
flask --app app init-db
flask --app app greet Alice
```

## ⚙️ 使用环境变量配置

### 方式1: 直接设置环境变量

```bash
# 设置应用位置
export FLASK_APP=app

# 设置调试模式
export FLASK_DEBUG=1

# 设置运行环境
export FLASK_ENV=development

# 然后可以简化命令
flask run
```

### 方式2: 使用 `.flaskenv` 文件

创建 `.flaskenv` 文件:

```bash
# .flaskenv
FLASK_APP=app
FLASK_DEBUG=1
FLASK_RUN_HOST=0.0.0.0
FLASK_RUN_PORT=5000
```

安装 `python-dotenv`:

```bash
pip install python-dotenv
```

然后直接运行:

```bash
flask run
```

### 方式3: 使用 `.env` 文件(敏感信息)

创建 `.env` 文件(不要提交到Git):

```bash
# .env
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://localhost/mydb
API_KEY=your-api-key
```

在应用中加载:

```python
# app/__init__.py
from dotenv import load_dotenv
import os

load_dotenv()

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
```

## 📊 对比表格

| 特性 | `python run.py` | `flask run` |
|------|----------------|-------------|
| 命令长度 | 短 | 中等 |
| 功能丰富度 | 基础 | 丰富 |
| 自动重载 | 需手动配置 | 内置支持 |
| 调试模式 | 需手动配置 | `--debug` 选项 |
| 路由查看 | 需自己实现 | `flask routes` |
| Shell环境 | 需自己实现 | `flask shell` |
| 自定义命令 | 不支持 | 支持 |
| 官方推荐 | - | ✅ |

## 💡 最佳实践

### 开发环境配置

创建 `.flaskenv` 文件:

```bash
# .flaskenv (可以提交到Git)
FLASK_APP=app
FLASK_DEBUG=1
FLASK_RUN_HOST=127.0.0.1
FLASK_RUN_PORT=5000
```

创建 `.env` 文件:

```bash
# .env (不要提交到Git,添加到.gitignore)
SECRET_KEY=dev-secret-key-change-in-production
DATABASE_URL=sqlite:///dev.db
```

### 生产环境配置

```bash
# 生产环境不使用flask run
# 使用WSGI服务器如Gunicorn

# 安装Gunicorn
pip install gunicorn

# 运行应用
gunicorn -w 4 -b 0.0.0.0:8000 'app:app'
```

## 🔧 常用命令速查

```bash
# 基本运行
flask --app app run

# 调试模式
flask --app app run --debug

# 指定端口
flask --app app run -p 8080

# 指定主机
flask --app app run -h 0.0.0.0

# 查看路由
flask --app app routes

# 进入Shell
flask --app app shell

# 使用环境变量(简化命令)
export FLASK_APP=app
flask run

# 使用.flaskenv(最简单)
# 创建.flaskenv文件后
flask run
```

## 📝 项目配置示例

### 1. 创建 `.flaskenv`

```bash
cd /Users/lingk/work/py/demo/flask-demo1
cat > .flaskenv << 'EOF'
FLASK_APP=app
FLASK_DEBUG=1
FLASK_RUN_HOST=127.0.0.1
FLASK_RUN_PORT=5000
EOF
```

### 2. 安装依赖

```bash
pip install python-dotenv
pip freeze > requirements.txt
```

### 3. 更新 `.gitignore`

```bash
# 确保.env被忽略
echo ".env" >> .gitignore

# .flaskenv可以提交
# 不需要添加到.gitignore
```

### 4. 运行应用

```bash
# 现在只需要
flask run

# 或者带调试
flask run --debug
```

## 🎓 Flask CLI 高级用法

### 1. 自定义命令组

```python
# app/cli.py
import click
from flask.cli import AppGroup

user_cli = AppGroup('user')

@user_cli.command('create')
@click.argument('username')
def create_user(username):
    """创建用户"""
    click.echo(f'Creating user: {username}')

@user_cli.command('delete')
@click.argument('username')
def delete_user(username):
    """删除用户"""
    click.echo(f'Deleting user: {username}')

# 在app/__init__.py中注册
from app.cli import user_cli
app.cli.add_command(user_cli)
```

使用:

```bash
flask --app app user create alice
flask --app app user delete bob
```

### 2. 带选项的命令

```python
@app.cli.command()
@click.option('--count', default=1, help='Number of greetings')
@click.option('--name', prompt='Your name', help='The person to greet')
def hello(count, name):
    """问候命令"""
    for _ in range(count):
        click.echo(f'Hello, {name}!')
```

使用:

```bash
flask --app app hello --count 3 --name Alice
```

### 3. 数据库迁移命令

```python
@app.cli.command()
def init_db():
    """初始化数据库"""
    click.echo('Initializing database...')
    # 创建表
    click.echo('✅ Database initialized!')

@app.cli.command()
def seed_db():
    """填充测试数据"""
    click.echo('Seeding database...')
    # 插入测试数据
    click.echo('✅ Database seeded!')

@app.cli.command()
@click.confirmation_option(prompt='Are you sure you want to drop the database?')
def drop_db():
    """删除数据库"""
    click.echo('Dropping database...')
    # 删除表
    click.echo('✅ Database dropped!')
```

## 🐛 故障排查

### 问题1: `flask: command not found`

**原因**: 虚拟环境未激活或Flask未安装

**解决**:
```bash
source venv/bin/activate
pip install flask
```

### 问题2: `Error: Could not locate a Flask application`

**原因**: 未指定FLASK_APP或路径错误

**解决**:
```bash
# 方式1: 指定应用
flask --app app run

# 方式2: 设置环境变量
export FLASK_APP=app
flask run

# 方式3: 使用.flaskenv
echo "FLASK_APP=app" > .flaskenv
flask run
```

### 问题3: 端口被占用

**解决**:
```bash
# 使用其他端口
flask --app app run -p 8080

# 或杀死占用进程
lsof -ti:5000 | xargs kill -9
```

## 📚 参考资源

- [Flask CLI文档](https://flask.palletsprojects.com/en/latest/cli/)
- [Click文档](https://click.palletsprojects.com/)
- [python-dotenv文档](https://github.com/theskumar/python-dotenv)

## 🎯 总结

### 推荐的开发流程:

1. **创建 `.flaskenv` 文件**
   ```bash
   FLASK_APP=app
   FLASK_DEBUG=1
   ```

2. **安装 python-dotenv**
   ```bash
   pip install python-dotenv
   ```

3. **运行应用**
   ```bash
   flask run
   ```

4. **查看路由**
   ```bash
   flask routes
   ```

5. **调试**
   ```bash
   flask shell
   ```

这样你就可以享受Flask CLI带来的便利! 🚀

