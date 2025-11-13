# 全局 g 对象配置说明

## 🎯 概述

项目已配置全局的 `g` 对象处理,**所有请求都会自动经过g对象的初始化、处理和清理流程**。

## 📋 请求处理流程

```
客户端请求
    ↓
【before_request】初始化g对象
    ├─ 生成请求ID
    ├─ 记录开始时间
    ├─ 获取用户信息
    ├─ 获取客户端信息
    └─ 打印请求日志
    ↓
【处理请求】执行视图函数
    ↓
【after_request】添加响应头和日志
    ├─ 计算处理时间
    ├─ 添加自定义响应头
    └─ 打印响应日志
    ↓
【teardown_request】清理资源
    ├─ 关闭数据库连接
    ├─ 记录错误(如果有)
    └─ 清理其他资源
    ↓
返回响应给客户端
```

## 🔧 g 对象中的变量

### 自动设置的变量

所有请求都会自动在 `g` 对象中设置以下变量:

| 变量名 | 类型 | 说明 | 示例 |
|--------|------|------|------|
| `g.request_id` | str | 请求唯一ID(8位) | `'a1b2c3d4'` |
| `g.request_start_time` | float | 请求开始时间戳 | `1635724800.123` |
| `g.user` | str | 用户名 | `'Alice'` 或 `'Guest'` |
| `g.user_id` | int\|None | 用户ID | `123` 或 `None` |
| `g.client_ip` | str | 客户端IP地址 | `'127.0.0.1'` |
| `g.user_agent` | str | 用户代理字符串 | `'Mozilla/5.0...'` |
| `g.request_path` | str | 请求路径 | `'/api/users'` |
| `g.request_method` | str | 请求方法 | `'GET'`, `'POST'` |
| `g.db` | object\|None | 数据库连接(按需创建) | `None` 或 连接对象 |

## 💡 如何使用

### 1. 在视图函数中直接使用

```python
from flask import g, jsonify

@app.route('/my-route')
def my_route():
    # 直接访问g对象中的变量
    return jsonify({
        'request_id': g.request_id,
        'user': g.user,
        'user_id': g.user_id,
        'client_ip': g.client_ip,
        'method': g.request_method,
        'path': g.request_path
    })
```

### 2. 在蓝图中使用

```python
from flask import Blueprint, g, jsonify

my_bp = Blueprint('my', __name__, url_prefix='/my')

@my_bp.route('/info')
def info():
    # 蓝图中也可以直接访问g对象
    return jsonify({
        'message': f'Hello, {g.user}!',
        'request_id': g.request_id,
        'ip': g.client_ip
    })
```

### 3. 在辅助函数中使用

```python
def log_action(action):
    """记录用户操作"""
    print(f"[{g.request_id}] 用户 {g.user} 执行了 {action}")

@app.route('/delete-item')
def delete_item():
    log_action('删除项目')  # 辅助函数可以访问g对象
    return 'Item deleted'
```

### 4. 权限检查

```python
from functools import wraps

def require_login(f):
    """装饰器: 要求用户登录"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if g.user == 'Guest':
            return jsonify({'error': 'Login required'}), 401
        return f(*args, **kwargs)
    return decorated

@app.route('/protected')
@require_login
def protected():
    return f'Welcome, {g.user}!'
```

## 📊 自动添加的响应头

所有响应都会自动添加以下响应头:

| 响应头 | 说明 | 示例 |
|--------|------|------|
| `X-Request-ID` | 请求唯一ID | `'a1b2c3d4'` |
| `X-Request-Time` | 请求处理时间 | `'0.0123s'` |
| `X-Processed-By` | 处理服务标识 | `'Flask-Demo-App'` |

### 查看响应头

```bash
# 使用curl查看响应头
curl -v http://127.0.0.1:5000/

# 输出包含:
# < X-Request-ID: a1b2c3d4
# < X-Request-Time: 0.0123s
# < X-Processed-By: Flask-Demo-App
```

## 📝 日志输出

### 请求开始日志

```
======================================================================
[请求开始] ID: a1b2c3d4
  方法: GET
  路径: /api/users
  用户: Alice (ID: 123)
  IP: 127.0.0.1
======================================================================
```

### 请求完成日志

```
======================================================================
[请求完成] ID: a1b2c3d4
  状态码: 200
  耗时: 0.0123s
  用户: Alice
======================================================================
```

### 错误日志

```
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
[异常] 请求ID: a1b2c3d4
  错误类型: ValueError
  错误信息: Invalid input
  用户: Alice
  路径: /api/users
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
```

## 🔍 传递用户信息的方式

### 方式1: URL参数(推荐用于测试)

```bash
curl "http://127.0.0.1:5000/api/users?user=Alice&user_id=123"
```

### 方式2: HTTP Header(推荐用于生产)

```bash
curl -H "X-User: Alice" -H "X-User-ID: 123" http://127.0.0.1:5000/api/users
```

### 方式3: 优先级

```
Header > URL参数 > 默认值(Guest)
```

## 🛠️ 扩展g对象

### 在before_request中添加自定义变量

```python
@app.before_request
def custom_before_request():
    """在全局before_request之后执行"""
    # 添加自定义变量
    g.custom_data = "my custom data"
    g.feature_flags = {
        'new_ui': True,
        'beta_feature': False
    }
```

### 在视图函数中使用

```python
@app.route('/test')
def test():
    return jsonify({
        'custom_data': g.custom_data,
        'feature_flags': g.feature_flags
    })
```

## ⚙️ 数据库连接管理

### 按需创建数据库连接

```python
import sqlite3

def get_db():
    """获取数据库连接(使用g对象缓存)"""
    if g.db is None:
        g.db = sqlite3.connect('database.db')
        g.db.row_factory = sqlite3.Row
        print(f"[DB] 创建新连接")
    return g.db

@app.route('/users')
def get_users():
    db = get_db()  # 自动缓存在g.db中
    users = db.execute('SELECT * FROM users').fetchall()
    return jsonify([dict(u) for u in users])
```

### 自动清理

数据库连接会在 `teardown_request` 中自动关闭,无需手动管理。

## 🐛 错误处理

### 404错误

```bash
curl http://127.0.0.1:5000/not-exists

# 响应:
{
  "error": "Not Found",
  "message": "The requested URL /not-exists was not found",
  "request_id": "a1b2c3d4",
  "user": "Guest"
}
```

### 500错误

```bash
curl http://127.0.0.1:5000/error-route

# 响应:
{
  "error": "ValueError",
  "message": "Something went wrong",
  "request_id": "a1b2c3d4",
  "user": "Guest",
  "path": "/error-route"
}
```

## 📚 实际示例

### 示例1: API接口

```python
@app.route('/api/profile')
def api_profile():
    """用户资料接口"""
    if g.user == 'Guest':
        return jsonify({'error': 'Login required'}), 401

    return jsonify({
        'user': g.user,
        'user_id': g.user_id,
        'ip': g.client_ip,
        'request_id': g.request_id
    })
```

### 示例2: 操作日志

```python
@app.route('/api/delete/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    """删除项目"""
    # 记录操作日志
    app.logger.info(
        f"[{g.request_id}] 用户 {g.user}(ID:{g.user_id}) "
        f"从 {g.client_ip} 删除项目 {item_id}"
    )

    # 执行删除操作
    # ...

    return jsonify({'message': 'Deleted', 'request_id': g.request_id})
```

### 示例3: 性能监控

```python
@app.route('/api/slow-operation')
def slow_operation():
    """慢操作"""
    import time
    time.sleep(2)  # 模拟慢操作

    # 处理时间会自动记录在响应头中
    return jsonify({
        'message': 'Done',
        'request_id': g.request_id
    })

# 响应头会包含:
# X-Request-Time: 2.0012s
```

## 🎯 最佳实践

### 1. 始终检查g对象属性是否存在

```python
# ✅ 推荐
user = getattr(g, 'user', 'Guest')

# ✅ 推荐
if hasattr(g, 'user'):
    print(g.user)

# ❌ 不推荐(可能报错)
print(g.user)  # 如果user不存在会报错
```

### 2. 使用g对象传递请求级别的数据

```python
# ✅ 适合使用g对象
g.user = 'Alice'           # 当前用户
g.request_id = 'abc123'    # 请求ID
g.db = get_db()            # 数据库连接

# ❌ 不适合使用g对象
g.app_config = {...}       # 应用配置(应该用app.config)
g.global_cache = {...}     # 全局缓存(应该用其他方案)
```

### 3. 在teardown_request中清理资源

```python
@app.teardown_request
def cleanup(error):
    """清理资源"""
    # 关闭数据库
    db = g.pop('db', None)
    if db:
        db.close()

    # 关闭文件
    file = g.pop('file', None)
    if file:
        file.close()
```

## 🔍 调试技巧

### 查看g对象的所有内容

```python
@app.route('/debug/g')
def debug_g():
    """查看g对象中的所有变量"""
    g_data = {}
    for key in dir(g):
        if not key.startswith('_'):
            try:
                value = getattr(g, key)
                if isinstance(value, (str, int, float, bool, type(None))):
                    g_data[key] = value
                else:
                    g_data[key] = f"<{type(value).__name__}>"
            except:
                pass

    return jsonify(g_data)
```

## 📖 总结

### 配置位置

`app/__init__.py` 中的全局请求处理部分

### 核心功能

1. ✅ **自动初始化**: 所有请求自动初始化g对象
2. ✅ **请求追踪**: 每个请求有唯一ID
3. ✅ **用户信息**: 自动提取用户信息
4. ✅ **性能监控**: 自动记录请求处理时间
5. ✅ **错误处理**: 统一的错误响应格式
6. ✅ **资源清理**: 自动清理数据库连接等资源

### 使用方式

在任何视图函数、蓝图或辅助函数中直接使用 `g.变量名` 即可!

---

**所有请求都会自动经过g对象处理,无需额外配置!** 🎉

