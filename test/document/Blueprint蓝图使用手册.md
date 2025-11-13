# Flask Blueprint 蓝图使用手册

## 📚 目录

1. [什么是蓝图](#什么是蓝图)
2. [为什么使用蓝图](#为什么使用蓝图)
3. [蓝图的基本使用](#蓝图的基本使用)
4. [项目结构](#项目结构)
5. [创建蓝图](#创建蓝图)
6. [注册蓝图](#注册蓝图)
7. [蓝图的URL前缀](#蓝图的url前缀)
8. [蓝图的请求钩子](#蓝图的请求钩子)
9. [蓝图的错误处理](#蓝图的错误处理)
10. [API版本控制](#api版本控制)
11. [测试蓝图路由](#测试蓝图路由)
12. [最佳实践](#最佳实践)

---

## 什么是蓝图

**蓝图(Blueprint)** 是Flask提供的一种组织应用的机制,可以将大型应用分解成多个可重用的模块。

### 核心概念:

```python
# 蓝图就像是一个"子应用"
# 它可以定义路由、错误处理、请求钩子等
# 但它不是独立的应用,需要注册到主应用才能工作
```

### 类比理解:

| 概念 | 类比 |
|------|------|
| Flask应用 | 一栋大楼 |
| 蓝图 | 大楼里的不同楼层(用户层、管理层、API层) |
| 路由 | 每层楼的房间号 |

---

## 为什么使用蓝图

### ✅ 优势:

1. **模块化**: 将应用分成独立的功能模块
2. **可重用**: 同一个蓝图可以在多个应用中使用
3. **团队协作**: 不同团队成员可以独立开发不同的蓝图
4. **URL组织**: 通过URL前缀清晰地组织路由
5. **版本控制**: 方便实现API版本管理

### 对比:

```python
# ❌ 不使用蓝图 - 所有路由混在一起
@app.route('/user/profile')
@app.route('/user/settings')
@app.route('/admin/dashboard')
@app.route('/admin/users')
@app.route('/api/v1/posts')
@app.route('/api/v2/posts')

# ✅ 使用蓝图 - 清晰的模块划分
# user_bp: /user/*
# admin_bp: /admin/*
# api_v1_bp: /api/v1/*
# api_v2_bp: /api/v2/*
```

---

## 蓝图的基本使用

### 三步走:

```python
# 步骤1: 创建蓝图
from flask import Blueprint
user_bp = Blueprint('user', __name__, url_prefix='/user')

# 步骤2: 定义路由
@user_bp.route('/profile')
def profile():
    return 'User Profile'

# 步骤3: 注册蓝图到应用
app.register_blueprint(user_bp)
```

---

## 项目结构

```
test/
├── app/
│   ├── __init__.py           # 创建Flask应用,注册蓝图
│   ├── views.py              # 传统路由(非蓝图)
│   ├── auth.py               # 认证路由(非蓝图)
│   └── blueprints/           # 蓝图目录
│       ├── __init__.py       # 蓝图包初始化
│       ├── user.py           # 用户蓝图
│       ├── admin.py          # 管理员蓝图
│       └── api.py            # API蓝图(v1和v2)
├── run.py                    # 应用启动入口
└── document/                 # 文档目录
    └── Blueprint蓝图使用手册.md
```

---

## 创建蓝图

### 基本语法:

```python
from flask import Blueprint

# Blueprint(name, import_name, **options)
blueprint_name = Blueprint(
    'blueprint_name',      # 蓝图名称(内部标识,用于url_for)
    __name__,              # 模块名称(帮助Flask定位资源)
    url_prefix='/prefix',  # URL前缀(可选)
    template_folder=None,  # 模板文件夹(可选)
    static_folder=None,    # 静态文件夹(可选)
    static_url_path=None   # 静态文件URL路径(可选)
)
```

### 示例1: 用户蓝图

```python
# app/blueprints/user.py
from flask import Blueprint, jsonify

# 创建用户蓝图
user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/')
def user_index():
    """访问: http://127.0.0.1:5000/user/"""
    return jsonify({'message': 'User Index'})

@user_bp.route('/profile')
def user_profile():
    """访问: http://127.0.0.1:5000/user/profile"""
    return jsonify({'username': 'guest'})

@user_bp.route('/profile/<int:user_id>')
def user_profile_by_id(user_id):
    """访问: http://127.0.0.1:5000/user/profile/123"""
    return jsonify({'user_id': user_id})
```

### 示例2: 管理员蓝图

```python
# app/blueprints/admin.py
from flask import Blueprint, jsonify

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
def admin_dashboard():
    """访问: http://127.0.0.1:5000/admin/dashboard"""
    return jsonify({'total_users': 1250})

@admin_bp.route('/users')
def admin_users():
    """访问: http://127.0.0.1:5000/admin/users"""
    return jsonify({'users': []})
```

---

## 注册蓝图

### 在主应用中注册:

```python
# app/__init__.py
from flask import Flask
from app.blueprints.user import user_bp
from app.blueprints.admin import admin_bp

app = Flask(__name__)

# 注册蓝图
app.register_blueprint(user_bp)
app.register_blueprint(admin_bp)
```

### 注册时修改URL前缀:

```python
# 方式1: 创建蓝图时指定
user_bp = Blueprint('user', __name__, url_prefix='/user')

# 方式2: 注册时指定(会覆盖创建时的设置)
app.register_blueprint(user_bp, url_prefix='/users')

# 方式3: 不使用前缀
app.register_blueprint(user_bp, url_prefix='')
```

---

## 蓝图的URL前缀

### URL前缀的作用:

```python
# 创建蓝图时指定url_prefix='/user'
user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/')           # 实际URL: /user/
@user_bp.route('/profile')    # 实际URL: /user/profile
@user_bp.route('/settings')   # 实际URL: /user/settings
```

### 嵌套URL前缀:

```python
# API版本控制示例
api_v1_bp = Blueprint('api_v1', __name__, url_prefix='/api/v1')
api_v2_bp = Blueprint('api_v2', __name__, url_prefix='/api/v2')

@api_v1_bp.route('/posts')    # 实际URL: /api/v1/posts
@api_v2_bp.route('/posts')    # 实际URL: /api/v2/posts
```

---

## 蓝图的请求钩子

### 蓝图级别的钩子:

```python
from flask import Blueprint, request, g

user_bp = Blueprint('user', __name__, url_prefix='/user')

# before_request: 在处理请求之前执行
@user_bp.before_request
def before_user_request():
    """只对user蓝图的路由生效"""
    print(f"Processing user request: {request.path}")
    g.user = 'guest'

# after_request: 在处理请求之后执行
@user_bp.after_request
def after_user_request(response):
    """可以修改响应"""
    response.headers['X-Custom-Header'] = 'User Blueprint'
    return response

# teardown_request: 请求结束时执行(即使出错也会执行)
@user_bp.teardown_request
def teardown_user_request(exception):
    """清理资源"""
    if exception:
        print(f"Error occurred: {exception}")
```

### 应用级别 vs 蓝图级别:

```python
# 应用级别的钩子 - 对所有路由生效
@app.before_request
def before_all_requests():
    pass

# 蓝图级别的钩子 - 只对当前蓝图的路由生效
@user_bp.before_request
def before_user_requests():
    pass
```

---

## 蓝图的错误处理

### 蓝图级别的错误处理:

```python
from flask import Blueprint, jsonify

user_bp = Blueprint('user', __name__, url_prefix='/user')

# 处理404错误
@user_bp.errorhandler(404)
def user_not_found(error):
    """只处理user蓝图中的404错误"""
    return jsonify({
        'error': 'User resource not found',
        'path': request.path
    }), 404

# 处理403错误
@user_bp.errorhandler(403)
def user_forbidden(error):
    return jsonify({
        'error': 'Forbidden',
        'message': 'Access denied'
    }), 403

# 处理自定义异常
class UserNotFoundError(Exception):
    pass

@user_bp.errorhandler(UserNotFoundError)
def handle_user_not_found(error):
    return jsonify({'error': str(error)}), 404
```

---

## API版本控制

### 使用蓝图实现API版本管理:

```python
# app/blueprints/api.py
from flask import Blueprint, jsonify

# API v1
api_v1_bp = Blueprint('api_v1', __name__, url_prefix='/api/v1')

@api_v1_bp.route('/posts')
def api_v1_posts():
    """旧版API: http://127.0.0.1:5000/api/v1/posts"""
    return jsonify({
        'version': 'v1',
        'posts': [{'id': 1, 'title': 'Post 1'}]
    })

# API v2
api_v2_bp = Blueprint('api_v2', __name__, url_prefix='/api/v2')

@api_v2_bp.route('/posts')
def api_v2_posts():
    """新版API: http://127.0.0.1:5000/api/v2/posts"""
    return jsonify({
        'version': 'v2',
        'posts': [
            {
                'id': 1,
                'title': 'Post 1',
                'author': 'Alice',
                'tags': ['python', 'flask']
            }
        ]
    })

# 注册两个版本的API
app.register_blueprint(api_v1_bp)
app.register_blueprint(api_v2_bp)
```

### 优势:

- ✅ 同时支持多个API版本
- ✅ 渐进式升级,不影响旧版本用户
- ✅ 清晰的版本隔离

---

## 测试蓝图路由

### 启动应用:

```bash
cd /Users/lingk/work/py/demo/test
source venv/bin/activate
python run.py
```

### 测试用户蓝图:

```bash
# 用户首页
curl http://127.0.0.1:5000/user/

# 用户资料
curl http://127.0.0.1:5000/user/profile

# 指定用户资料
curl http://127.0.0.1:5000/user/profile/123

# 用户设置(GET)
curl http://127.0.0.1:5000/user/settings

# 用户设置(POST)
curl -X POST http://127.0.0.1:5000/user/settings \
  -H "Content-Type: application/json" \
  -d '{"theme": "light", "language": "en"}'
```

### 测试管理员蓝图:

```bash
# 管理后台首页
curl http://127.0.0.1:5000/admin/

# 仪表盘
curl http://127.0.0.1:5000/admin/dashboard

# 用户列表(带分页)
curl "http://127.0.0.1:5000/admin/users?page=1&limit=5"

# 用户详情
curl http://127.0.0.1:5000/admin/users/123

# 系统统计
curl http://127.0.0.1:5000/admin/stats
```

### 测试API蓝图:

```bash
# API v1
curl http://127.0.0.1:5000/api/v1/
curl http://127.0.0.1:5000/api/v1/posts
curl http://127.0.0.1:5000/api/v1/posts/1

# API v2
curl http://127.0.0.1:5000/api/v2/
curl http://127.0.0.1:5000/api/v2/posts
curl http://127.0.0.1:5000/api/v2/posts/1
curl "http://127.0.0.1:5000/api/v2/comments?post_id=1"
```

### 查看所有路由:

```python
# 在Python交互式环境中
from app import app

for rule in app.url_map.iter_rules():
    print(f"{rule.endpoint:30s} {rule.rule}")
```

输出示例:
```
user.user_index                /user/
user.user_profile              /user/profile
user.user_profile_by_id        /user/profile/<int:user_id>
admin.admin_dashboard          /admin/dashboard
admin.admin_users_list         /admin/users
api_v1.api_v1_posts            /api/v1/posts
api_v2.api_v2_posts            /api/v2/posts
```

---

## 最佳实践

### 1. 目录结构组织

```
app/
├── __init__.py              # 主应用,注册所有蓝图
├── blueprints/              # 所有蓝图放在这个目录
│   ├── __init__.py
│   ├── user.py             # 用户相关功能
│   ├── admin.py            # 管理员功能
│   ├── api.py              # API接口
│   └── auth.py             # 认证功能
└── models/                  # 数据模型
    ├── __init__.py
    ├── user.py
    └── post.py
```

### 2. 蓝图命名规范

```python
# ✅ 好的命名
user_bp = Blueprint('user', __name__)
admin_bp = Blueprint('admin', __name__)
api_v1_bp = Blueprint('api_v1', __name__)

# ❌ 不好的命名
bp1 = Blueprint('bp1', __name__)
my_blueprint = Blueprint('my', __name__)
```

### 3. URL前缀设计

```python
# ✅ 清晰的URL结构
/user/profile
/user/settings
/admin/dashboard
/admin/users
/api/v1/posts
/api/v2/posts

# ❌ 混乱的URL结构
/profile
/settings
/dashboard
/users
/posts
```

### 4. 使用url_for生成URL

```python
from flask import url_for

# ✅ 使用蓝图名称.函数名称
url_for('user.user_profile')           # /user/profile
url_for('admin.admin_dashboard')       # /admin/dashboard
url_for('api_v1.api_v1_posts')         # /api/v1/posts

# 带参数
url_for('user.user_profile_by_id', user_id=123)  # /user/profile/123
```

### 5. 蓝图之间的独立性

```python
# ✅ 每个蓝图应该是独立的模块
# user.py 不应该直接导入 admin.py 的内容
# 如果需要共享代码,应该放在公共模块中

# 公共模块
# app/utils/helpers.py
def format_date(date):
    return date.strftime('%Y-%m-%d')

# 在蓝图中使用
from app.utils.helpers import format_date
```

### 6. 权限控制

```python
from functools import wraps
from flask import abort

def admin_required(f):
    """装饰器: 检查管理员权限"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_admin():
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/dashboard')
@admin_required
def admin_dashboard():
    return jsonify({'data': 'sensitive data'})
```

### 7. 蓝图的测试

```python
# tests/test_user_blueprint.py
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_user_profile(client):
    """测试用户资料接口"""
    response = client.get('/user/profile')
    assert response.status_code == 200
    assert b'username' in response.data
```

---

## 总结

### 🎯 核心要点:

1. **蓝图是模块化工具**: 用于组织大型Flask应用
2. **三步使用**: 创建蓝图 → 定义路由 → 注册到应用
3. **URL前缀**: 清晰地组织路由结构
4. **独立性**: 每个蓝图应该是独立的功能模块
5. **版本控制**: 方便实现API版本管理

### 📊 蓝图 vs 传统路由:

| 特性 | 传统路由 | 蓝图 |
|------|---------|------|
| 适用场景 | 小型应用 | 大型应用 |
| 模块化 | ❌ | ✅ |
| 可重用 | ❌ | ✅ |
| URL组织 | 混乱 | 清晰 |
| 团队协作 | 困难 | 容易 |

### 🚀 下一步:

- 实践创建自己的蓝图
- 尝试不同的URL前缀组合
- 实现权限控制和错误处理
- 编写蓝图的单元测试

---

## 参考资源

- [Flask官方文档 - Blueprints](https://flask.palletsprojects.com/en/latest/blueprints/)
- [Flask大型应用结构](https://flask.palletsprojects.com/en/latest/patterns/packages/)
- 项目示例: `/Users/lingk/work/py/demo/test/app/blueprints/`

