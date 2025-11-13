# Flask g 对象使用指南

## 🎯 什么是 g 对象?

`g` 是Flask提供的**请求级别的全局变量**,用于在整个请求处理过程中存储和共享数据。

### 核心特点:

- ✅ **请求级别**: 每个请求都有独立的g对象
- ✅ **自动清理**: 请求结束后自动清理
- ✅ **线程安全**: 基于Context实现,多线程安全
- ✅ **简单易用**: 像普通对象一样使用

## 📊 g 对象 vs 其他存储方式

| 特性 | g对象 | session | 全局变量 | request |
|------|------|---------|---------|---------|
| **生命周期** | 单个请求 | 多个请求 | 应用生命周期 | 单个请求 |
| **存储位置** | 服务器内存 | 客户端Cookie | 服务器内存 | 请求对象 |
| **用途** | 请求内数据共享 | 用户会话 | 应用配置 | 请求信息 |
| **可修改** | ✅ | ✅ | ✅ | ❌ |

## 🔍 基本使用

### 1. 设置和获取数据

```python
from flask import g

@app.before_request
def before_request():
    # 设置数据
    g.user = 'Alice'
    g.user_id = 123
    g.request_time = time.time()

@app.route('/')
def index():
    # 获取数据
    user = g.user
    user_id = g.user_id

    return f'Hello, {user}!'
```

### 2. 检查属性是否存在

```python
# 方式1: hasattr
if hasattr(g, 'user'):
    print(g.user)

# 方式2: getattr with default
user = getattr(g, 'user', 'Guest')

# 方式3: get方法
user = g.get('user', 'Guest')

# 方式4: pop方法(获取并删除)
user = g.pop('user', None)
```

## 💡 实际应用场景

### 场景1: 用户认证信息

```python
@app.before_request
def load_user():
    """在每个请求前加载用户信息"""
    # 从token或session获取用户ID
    user_id = request.headers.get('X-User-ID')

    if user_id:
        # 从数据库加载用户
        g.user = User.query.get(user_id)
        g.is_authenticated = True
    else:
        g.user = None
        g.is_authenticated = False

@app.route('/profile')
def profile():
    """使用g对象中的用户信息"""
    if not g.is_authenticated:
        return 'Please login', 401

    return f'Welcome, {g.user.name}!'
```

### 场景2: 数据库连接管理

```python
def get_db():
    """获取数据库连接(使用g对象缓存)"""
    if 'db' not in g:
        g.db = sqlite3.connect('database.db')
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_request
def close_db(error):
    """请求结束时关闭数据库连接"""
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route('/users')
def get_users():
    """使用数据库连接"""
    db = get_db()  # 第一次调用,创建连接
    users = db.execute('SELECT * FROM users').fetchall()

    db2 = get_db()  # 第二次调用,复用连接
    # db 和 db2 是同一个对象!

    return jsonify([dict(u) for u in users])
```

### 场景3: 请求追踪和日志

```python
import uuid

@app.before_request
def before_request():
    """生成请求ID用于日志追踪"""
    g.request_id = str(uuid.uuid4())
    g.start_time = time.time()

    app.logger.info(f'[{g.request_id}] {request.method} {request.path}')

@app.after_request
def after_request(response):
    """记录请求处理时间"""
    if hasattr(g, 'start_time'):
        elapsed = time.time() - g.start_time
        app.logger.info(f'[{g.request_id}] Completed in {elapsed:.4f}s')
        response.headers['X-Request-ID'] = g.request_id
        response.headers['X-Request-Time'] = f'{elapsed:.4f}s'

    return response
```

### 场景4: 权限检查

```python
from functools import wraps

def require_role(role):
    """装饰器: 检查用户角色"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not hasattr(g, 'user') or g.user.role != role:
                return 'Permission denied', 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.before_request
def load_user_role():
    """加载用户角色"""
    user_id = request.args.get('user_id')
    if user_id:
        g.user = User.query.get(user_id)
        g.user.role = 'admin'  # 从数据库获取

@app.route('/admin')
@require_role('admin')
def admin_panel():
    """需要admin权限"""
    return 'Admin Panel'
```

### 场景5: 缓存昂贵的计算

```python
def get_expensive_data():
    """获取昂贵的计算结果(使用g对象缓存)"""
    if 'expensive_data' not in g:
        # 只计算一次
        g.expensive_data = expensive_calculation()
    return g.expensive_data

@app.route('/page1')
def page1():
    data = get_expensive_data()  # 第一次计算
    return render_template('page1.html', data=data)

@app.route('/page2')
def page2():
    data = get_expensive_data()  # 使用缓存
    return render_template('page2.html', data=data)
```

## 🎨 完整示例

### 示例项目结构

```python
# app/blueprints/demo_g.py
from flask import Blueprint, g, request

demo_g_bp = Blueprint('demo_g', __name__, url_prefix='/demo-g')

@demo_g_bp.before_request
def before_request():
    """请求前: 设置用户信息和请求时间"""
    g.user = request.args.get('user', 'Guest')
    g.request_start_time = time.time()
    g.request_id = f"{int(time.time() * 1000)}"

@demo_g_bp.route('/')
def index():
    """视图函数: 使用g对象"""
    return jsonify({
        'user': g.user,
        'request_id': g.request_id
    })

@demo_g_bp.after_request
def after_request(response):
    """请求后: 添加响应头"""
    if hasattr(g, 'request_start_time'):
        elapsed = time.time() - g.request_start_time
        response.headers['X-Request-Time'] = f'{elapsed:.4f}s'
    return response

@demo_g_bp.teardown_request
def teardown_request(error):
    """请求结束: 清理资源"""
    db = g.pop('db', None)
    if db:
        db.close()
```

## ⚠️ 注意事项

### 1. g对象的生命周期

```python
# ❌ 错误: 在请求外使用g对象
def background_task():
    print(g.user)  # 错误! 没有请求上下文

# ✅ 正确: 只在请求处理中使用
@app.route('/')
def index():
    print(g.user)  # 正确! 在请求上下文中
```

### 2. 不要存储大对象

```python
# ❌ 不推荐: 存储大量数据
@app.before_request
def before():
    g.huge_data = load_huge_dataset()  # 不好

# ✅ 推荐: 只存储必要的引用
@app.before_request
def before():
    g.user_id = get_user_id()  # 好
```

### 3. 使用前检查是否存在

```python
# ❌ 可能出错
@app.route('/profile')
def profile():
    return g.user.name  # 如果g.user不存在会报错

# ✅ 安全的做法
@app.route('/profile')
def profile():
    if not hasattr(g, 'user'):
        return 'Not logged in', 401
    return g.user.name
```

### 4. 不要在g对象中存储敏感信息

```python
# ❌ 不安全
g.password = user_password  # 不要存储密码

# ✅ 安全
g.user_id = user.id  # 只存储ID
```

## 🔧 高级用法

### 1. 自定义g对象

```python
from flask import Flask, g
from werkzeug.local import LocalProxy

app = Flask(__name__)

# 创建便捷的访问器
def get_current_user():
    return getattr(g, 'user', None)

current_user = LocalProxy(get_current_user)

# 使用
@app.route('/')
def index():
    if current_user:
        return f'Hello, {current_user.name}!'
    return 'Hello, Guest!'
```

### 2. 与上下文管理器结合

```python
from contextlib import contextmanager

@contextmanager
def db_session():
    """数据库会话上下文管理器"""
    db = get_db()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        g.pop('db', None)
        db.close()

@app.route('/create-user')
def create_user():
    with db_session() as db:
        db.execute('INSERT INTO users VALUES (?)', ('Alice',))
    return 'User created'
```

## 📚 测试g对象

```python
def test_g_object():
    """测试g对象的使用"""
    with app.test_request_context('/?user=Alice'):
        # 模拟before_request
        g.user = 'Alice'

        # 测试视图函数
        assert g.user == 'Alice'

        # 测试清理
        g.pop('user')
        assert not hasattr(g, 'user')
```

## 🎯 最佳实践

### 1. 统一的初始化

```python
@app.before_request
def init_g():
    """统一初始化g对象"""
    g.user = None
    g.db = None
    g.request_id = generate_request_id()
    g.start_time = time.time()
```

### 2. 使用类型提示

```python
from typing import Optional
from flask import g

class User:
    name: str
    id: int

# 在使用时添加类型注解
def get_current_user() -> Optional[User]:
    return g.get('user')
```

### 3. 创建辅助函数

```python
def require_user():
    """确保用户已登录"""
    if not hasattr(g, 'user') or g.user is None:
        abort(401)
    return g.user

@app.route('/dashboard')
def dashboard():
    user = require_user()  # 简化代码
    return f'Welcome, {user.name}!'
```

## 📖 总结

### g对象的核心用途:

1. ✅ **用户认证**: 存储当前用户信息
2. ✅ **数据库连接**: 缓存数据库连接
3. ✅ **请求追踪**: 存储请求ID和时间
4. ✅ **权限检查**: 存储用户角色和权限
5. ✅ **缓存计算**: 缓存请求期间的计算结果

### 记住:

- `g` 对象只在**请求处理期间**有效
- 请求结束后**自动清理**
- **线程安全**,每个请求独立
- 适合存储**请求级别**的临时数据

---

**示例代码**: `app/blueprints/demo_g.py` 包含了8个完整的使用示例! 🚀

**测试命令**:
```bash
# 启动应用
flask run

# 测试各个示例
curl "http://127.0.0.1:5000/demo-g/?user=Alice&user_id=123"
curl "http://127.0.0.1:5000/demo-g/db-demo"
curl "http://127.0.0.1:5000/demo-g/admin-only?user=Alice"
curl "http://127.0.0.1:5000/demo-g/config-demo"
curl "http://127.0.0.1:5000/demo-g/inspect-g?user=Inspector"
```

