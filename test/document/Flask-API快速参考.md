# Flask API 快速参考

## 🔍 如何查看Flask的方法?

### 方法1: 使用 `dir()`

```python
from app import app

# 查看所有方法和属性
print(dir(app))

# 只看公共方法(不以_开头)
public_methods = [m for m in dir(app) if not m.startswith('_')]
print(public_methods)
```

### 方法2: 使用 `help()`

```python
# 查看详细文档
help(app)
help(app.route)
help(app.register_blueprint)
```

### 方法3: 使用探索工具

```bash
# 运行探索脚本
python explore_api.py

# 保存到文件
python explore_api.py > flask_api_reference.txt
```

---

## 📋 Flask应用(app)常用方法

### 🛣️ 路由相关

| 方法 | 说明 | 示例 |
|------|------|------|
| `@app.route(rule, **options)` | 注册路由 | `@app.route('/path')` |
| `app.add_url_rule(rule, endpoint, view_func)` | 手动添加路由 | `app.add_url_rule('/', 'index', index_view)` |
| `app.url_for(endpoint, **values)` | 生成URL | `url_for('user.profile', user_id=123)` |
| `app.url_map` | 查看所有路由 | `for rule in app.url_map.iter_rules()` |

```python
# 基本路由
@app.route('/hello')
def hello():
    return 'Hello'

# 带参数的路由
@app.route('/user/<int:user_id>')
def user(user_id):
    return f'User {user_id}'

# 多种HTTP方法
@app.route('/api', methods=['GET', 'POST', 'PUT', 'DELETE'])
def api():
    return 'API'
```

### 🎨 蓝图相关

| 方法 | 说明 | 示例 |
|------|------|------|
| `app.register_blueprint(bp, **options)` | 注册蓝图 | `app.register_blueprint(user_bp)` |
| `app.blueprints` | 查看所有蓝图 | `print(app.blueprints)` |
| `app.iter_blueprints()` | 遍历蓝图 | `for bp in app.iter_blueprints()` |

```python
from flask import Blueprint

# 创建蓝图
user_bp = Blueprint('user', __name__, url_prefix='/user')

# 注册蓝图
app.register_blueprint(user_bp)

# 查看所有蓝图
for name, blueprint in app.blueprints.items():
    print(f"蓝图: {name}")
```

### 🔗 请求钩子

| 装饰器 | 说明 | 执行时机 |
|--------|------|----------|
| `@app.before_request` | 请求前执行 | 每个请求之前 |
| `@app.after_request` | 请求后执行 | 每个请求之后 |
| `@app.teardown_request` | 请求结束 | 请求结束时(即使出错) |
| `@app.context_processor` | 模板上下文 | 渲染模板前 |

```python
@app.before_request
def before():
    print("Before request")
    g.user = 'guest'

@app.after_request
def after(response):
    print("After request")
    response.headers['X-Custom'] = 'value'
    return response

@app.teardown_request
def teardown(exception):
    print("Teardown")
    # 清理资源
```

### ⚠️ 错误处理

| 方法 | 说明 | 示例 |
|------|------|------|
| `@app.errorhandler(code)` | 处理错误 | `@app.errorhandler(404)` |
| `app.register_error_handler(code, func)` | 手动注册 | `app.register_error_handler(404, not_found)` |

```python
@app.errorhandler(404)
def not_found(error):
    return {'error': 'Not found'}, 404

@app.errorhandler(500)
def internal_error(error):
    return {'error': 'Internal server error'}, 500

# 处理自定义异常
class CustomError(Exception):
    pass

@app.errorhandler(CustomError)
def handle_custom_error(error):
    return {'error': str(error)}, 400
```

### ⚙️ 配置相关

| 属性/方法 | 说明 | 示例 |
|-----------|------|------|
| `app.config` | 配置字典 | `app.config['DEBUG'] = True` |
| `app.config.from_file()` | 从文件加载 | `app.config.from_file('config.json')` |
| `app.config.from_object()` | 从对象加载 | `app.config.from_object('config.Config')` |

```python
# 直接设置
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['DEBUG'] = True

# 从对象加载
class Config:
    SECRET_KEY = 'secret'
    DEBUG = False

app.config.from_object(Config)

# 查看配置
print(app.config)
```

### 🎯 其他常用方法

| 方法 | 说明 | 示例 |
|------|------|------|
| `app.run(**options)` | 运行应用 | `app.run(debug=True, port=5000)` |
| `app.test_client()` | 测试客户端 | `client = app.test_client()` |
| `app.make_response(rv)` | 创建响应 | `response = app.make_response('text')` |
| `app.logger` | 日志记录器 | `app.logger.info('message')` |

```python
# 运行应用
if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )

# 使用日志
app.logger.info('Info message')
app.logger.warning('Warning message')
app.logger.error('Error message')

# 创建响应
from flask import make_response
response = make_response('Hello', 200)
response.headers['X-Custom'] = 'value'
```

---

## 📘 Blueprint(蓝图)常用方法

### 创建和配置

```python
from flask import Blueprint

bp = Blueprint(
    'name',              # 蓝图名称
    __name__,            # 模块名
    url_prefix='/prefix', # URL前缀
    template_folder='templates',  # 模板目录(可选)
    static_folder='static'        # 静态文件目录(可选)
)
```

### 蓝图方法(与app类似)

| 方法 | 说明 |
|------|------|
| `@bp.route(rule)` | 注册路由 |
| `@bp.before_request` | 请求前钩子 |
| `@bp.after_request` | 请求后钩子 |
| `@bp.errorhandler(code)` | 错误处理 |
| `@bp.context_processor` | 模板上下文 |

```python
# 蓝图路由
@bp.route('/')
def index():
    return 'Blueprint Index'

# 蓝图钩子
@bp.before_request
def before():
    print("Before blueprint request")

# 蓝图错误处理
@bp.errorhandler(404)
def not_found(error):
    return {'error': 'Not found'}, 404
```

---

## 🔧 实用工具函数

### Flask模块提供的工具

```python
from flask import (
    request,        # 请求对象
    g,              # 请求期间的全局对象
    session,        # 会话对象
    jsonify,        # 返回JSON
    render_template,# 渲染模板
    redirect,       # 重定向
    url_for,        # 生成URL
    abort,          # 抛出HTTP错误
    make_response,  # 创建响应
    send_file,      # 发送文件
    send_from_directory, # 从目录发送文件
)

# 使用示例
@app.route('/api/data')
def get_data():
    # 获取请求数据
    args = request.args
    json_data = request.get_json()

    # 使用g对象
    g.user = 'guest'

    # 返回JSON
    return jsonify({'key': 'value'})

@app.route('/redirect')
def do_redirect():
    return redirect(url_for('index'))

@app.route('/error')
def error():
    abort(404)  # 抛出404错误
```

---

## 📊 查看应用信息

### 查看所有路由

```python
from app import app

# 方法1: 遍历url_map
for rule in app.url_map.iter_rules():
    print(f"{rule.endpoint:30s} {rule.methods} {rule.rule}")

# 方法2: 使用列表推导
routes = [
    (rule.endpoint, rule.rule, rule.methods)
    for rule in app.url_map.iter_rules()
]
```

### 查看所有蓝图

```python
# 查看蓝图字典
print(app.blueprints)

# 遍历蓝图
for name, blueprint in app.blueprints.items():
    print(f"蓝图名称: {name}")
    print(f"URL前缀: {blueprint.url_prefix}")
```

### 查看配置

```python
# 查看所有配置
for key, value in app.config.items():
    print(f"{key}: {value}")

# 查看特定配置
print(app.config.get('DEBUG'))
print(app.config.get('SECRET_KEY'))
```

---

## 💡 调试技巧

### 1. 使用Python交互式环境

```bash
cd /Users/lingk/work/py/demo/flask-demo1
source venv/bin/activate
python

>>> from app import app
>>> dir(app)
>>> help(app.route)
>>> app.url_map
```

### 2. 使用IPython(更好的交互体验)

```bash
pip install ipython
ipython

In [1]: from app import app
In [2]: app.<Tab>  # 按Tab键自动补全
In [3]: app.route?  # 查看文档
In [4]: app.route??  # 查看源代码
```

### 3. 使用探索脚本

```bash
# 运行探索工具
python explore_api.py

# 保存输出
python explore_api.py > flask_api_reference.txt
```

### 4. 查看源代码

```python
import inspect

# 查看方法源代码
print(inspect.getsource(app.route))

# 查看方法签名
print(inspect.signature(app.route))

# 查看方法文档
print(inspect.getdoc(app.route))
```

---

## 📚 参考资源

- [Flask官方API文档](https://flask.palletsprojects.com/en/latest/api/)
- [Flask快速开始](https://flask.palletsprojects.com/en/latest/quickstart/)
- [Blueprint文档](https://flask.palletsprojects.com/en/latest/blueprints/)
- 本项目探索工具: `python explore_api.py`

---

## 🎯 快速命令参考

```bash
# 查看所有方法
python -c "from app import app; print([m for m in dir(app) if not m.startswith('_')])"

# 查看所有路由
python -c "from app import app; [print(f'{r.endpoint:30s} {r.rule}') for r in app.url_map.iter_rules()]"

# 查看所有蓝图
python -c "from app import app; print(list(app.blueprints.keys()))"

# 运行探索工具
python explore_api.py

# 交互式探索
python -i -c "from app import app"
```

