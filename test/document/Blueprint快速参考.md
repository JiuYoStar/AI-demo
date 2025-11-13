# Flask Blueprint 快速参考

## 🚀 快速开始

### 1. 创建蓝图

```python
# app/blueprints/user.py
from flask import Blueprint, jsonify

user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/')
def index():
    return jsonify({'message': 'User Index'})
```

### 2. 注册蓝图

```python
# app/__init__.py
from flask import Flask
from app.blueprints.user import user_bp

app = Flask(__name__)
app.register_blueprint(user_bp)
```

### 3. 访问路由

```bash
curl http://127.0.0.1:5000/user/
```

---

## 📋 常用代码片段

### 带参数的路由

```python
@user_bp.route('/profile/<int:user_id>')
def user_profile(user_id):
    return jsonify({'user_id': user_id})
```

### 多种HTTP方法

```python
@user_bp.route('/settings', methods=['GET', 'POST', 'PUT', 'DELETE'])
def settings():
    if request.method == 'POST':
        return jsonify({'message': 'Updated'})
    return jsonify({'settings': {}})
```

### 请求钩子

```python
@user_bp.before_request
def before_request():
    print(f"Processing: {request.path}")

@user_bp.after_request
def after_request(response):
    response.headers['X-Custom'] = 'value'
    return response
```

### 错误处理

```python
@user_bp.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404
```

---

## 🎯 项目中的蓝图

### 用户蓝图 (user_bp)

| 路由 | 方法 | 说明 |
|------|------|------|
| `/user/` | GET | 用户首页 |
| `/user/profile` | GET | 当前用户资料 |
| `/user/profile/<user_id>` | GET | 指定用户资料 |
| `/user/settings` | GET/POST | 用户设置 |

```bash
# 测试命令
curl http://127.0.0.1:5000/user/
curl http://127.0.0.1:5000/user/profile
curl http://127.0.0.1:5000/user/profile/123
curl http://127.0.0.1:5000/user/settings
```

### 管理员蓝图 (admin_bp)

| 路由 | 方法 | 说明 |
|------|------|------|
| `/admin/` | GET | 管理后台首页 |
| `/admin/dashboard` | GET | 仪表盘 |
| `/admin/users` | GET | 用户列表 |
| `/admin/users/<user_id>` | GET/PUT/DELETE | 用户管理 |
| `/admin/stats` | GET | 统计信息 |

```bash
# 测试命令
curl http://127.0.0.1:5000/admin/
curl http://127.0.0.1:5000/admin/dashboard
curl "http://127.0.0.1:5000/admin/users?page=1&limit=10"
curl http://127.0.0.1:5000/admin/users/123
curl http://127.0.0.1:5000/admin/stats
```

### API v1 蓝图 (api_v1_bp)

| 路由 | 方法 | 说明 |
|------|------|------|
| `/api/v1/` | GET | API v1 首页 |
| `/api/v1/posts` | GET | 文章列表 |
| `/api/v1/posts/<post_id>` | GET | 文章详情 |

```bash
# 测试命令
curl http://127.0.0.1:5000/api/v1/
curl http://127.0.0.1:5000/api/v1/posts
curl http://127.0.0.1:5000/api/v1/posts/1
```

### API v2 蓝图 (api_v2_bp)

| 路由 | 方法 | 说明 |
|------|------|------|
| `/api/v2/` | GET | API v2 首页 |
| `/api/v2/posts` | GET | 文章列表(增强) |
| `/api/v2/posts/<post_id>` | GET | 文章详情(增强) |
| `/api/v2/comments` | GET | 评论列表 |

```bash
# 测试命令
curl http://127.0.0.1:5000/api/v2/
curl http://127.0.0.1:5000/api/v2/posts
curl http://127.0.0.1:5000/api/v2/posts/1
curl "http://127.0.0.1:5000/api/v2/comments?post_id=1"
```

---

## 🔧 常用命令

### 查看所有路由

```python
from app import app

for rule in app.url_map.iter_rules():
    print(f"{rule.endpoint:35s} {rule.rule}")
```

### 生成URL

```python
from flask import url_for

# 蓝图路由使用: 蓝图名.函数名
url_for('user.user_profile')                    # /user/profile
url_for('user.user_profile_by_id', user_id=123) # /user/profile/123
url_for('admin.admin_dashboard')                # /admin/dashboard
url_for('api_v1.api_v1_posts')                  # /api/v1/posts
```

### 启动应用

```bash
cd /Users/lingk/work/py/demo/flask-demo1
source venv/bin/activate
python run.py
```

---

## 📁 项目结构

```
flask-demo1/
├── app/
│   ├── __init__.py              # 注册所有蓝图
│   ├── views.py                 # 传统路由
│   ├── auth.py                  # 认证路由
│   └── blueprints/              # 蓝图目录
│       ├── __init__.py          # 蓝图包
│       ├── user.py              # 用户蓝图 ✅
│       ├── admin.py             # 管理员蓝图 ✅
│       └── api.py               # API蓝图(v1/v2) ✅
├── document/
│   ├── Blueprint蓝图使用手册.md  # 详细文档
│   └── Blueprint快速参考.md     # 快速参考(本文件)
└── run.py                       # 启动入口
```

---

## 💡 最佳实践

### ✅ 推荐

```python
# 清晰的命名
user_bp = Blueprint('user', __name__, url_prefix='/user')

# 使用url_for
url = url_for('user.user_profile')

# 蓝图级别的钩子
@user_bp.before_request
def check_user():
    pass
```

### ❌ 避免

```python
# 不清晰的命名
bp1 = Blueprint('bp1', __name__)

# 硬编码URL
url = '/user/profile'

# 蓝图之间的强耦合
from app.blueprints.admin import admin_function  # 不推荐
```

---

## 🐛 常见问题

### Q: 蓝图路由404?
A: 检查是否已注册蓝图: `app.register_blueprint(user_bp)`

### Q: URL前缀重复?
A: 检查Blueprint创建时和注册时的url_prefix设置

### Q: 蓝图之间如何共享代码?
A: 创建公共模块,不要直接在蓝图之间导入

### Q: 如何调试蓝图路由?
A: 使用 `app.url_map.iter_rules()` 查看所有注册的路由

---

## 📚 相关文档

- [Blueprint蓝图使用手册.md](./Blueprint蓝图使用手册.md) - 详细教程
- [Flask官方文档](https://flask.palletsprojects.com/en/latest/blueprints/)
- 示例代码: `app/blueprints/`

