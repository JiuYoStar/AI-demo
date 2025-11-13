# app/blueprints/demo_g.py
# Flask g 对象使用示例
# g 是请求级别的全局变量,在整个请求期间共享数据

from flask import Blueprint, g, request, jsonify
import time
import sqlite3

demo_g_bp = Blueprint('demo_g', __name__, url_prefix='/demo-g')


# ==================== 示例1: 基本使用 ====================

@demo_g_bp.before_request
def before_request():
    """
    在每个请求之前执行
    设置请求开始时间和用户信息
    """
    # 1. 记录请求开始时间
    g.request_start_time = time.time()

    # 2. 从请求参数中获取用户信息
    g.user = request.args.get('user', 'Guest')
    g.user_id = request.args.get('user_id', type=int)

    # 3. 设置请求ID(用于日志追踪)
    g.request_id = f"{int(time.time() * 1000)}"

    print(f"[Before Request] 用户: {g.user}, 请求ID: {g.request_id}")


@demo_g_bp.route('/')
def index():
    """
    示例: 在视图函数中使用g对象
    访问: http://127.0.0.1:5000/demo-g/?user=Alice&user_id=123
    """
    return jsonify({
        'message': f'Hello, {g.user}!',
        'user_id': g.user_id,
        'request_id': g.request_id,
        'endpoint': request.endpoint
    })


@demo_g_bp.after_request
def after_request(response):
    """
    在每个请求之后执行
    计算请求处理时间
    """
    # 计算请求处理时间
    if hasattr(g, 'request_start_time'):
        elapsed = time.time() - g.request_start_time
        response.headers['X-Request-Time'] = f'{elapsed:.4f}s'
        print(f"[After Request] 请求ID: {g.request_id}, 耗时: {elapsed:.4f}s")

    return response


# ==================== 示例2: 数据库连接管理 ====================

def get_db():
    """
    获取数据库连接
    使用g对象缓存数据库连接,避免重复创建
    """
    if 'db' not in g:
        # 第一次调用时创建连接
        g.db = sqlite3.connect(':memory:')  # 使用内存数据库演示
        g.db.row_factory = sqlite3.Row
        print(f"[DB] 创建新的数据库连接")
    else:
        print(f"[DB] 复用已有的数据库连接")

    return g.db


def close_db(error=None):
    """
    关闭数据库连接
    在请求结束时自动调用
    """
    db = g.pop('db', None)

    if db is not None:
        db.close()
        print(f"[DB] 关闭数据库连接")


# 注册teardown函数
@demo_g_bp.teardown_request
def teardown_request(error):
    """
    请求结束时执行(即使出错也会执行)
    """
    close_db(error)

    if error:
        print(f"[Teardown] 请求出错: {error}")
    else:
        print(f"[Teardown] 请求正常结束")


@demo_g_bp.route('/db-demo')
def db_demo():
    """
    示例: 使用g对象管理数据库连接
    访问: http://127.0.0.1:5000/demo-g/db-demo
    """
    # 第一次调用get_db() - 创建连接
    db1 = get_db()

    # 创建测试表
    db1.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER, name TEXT)')
    db1.execute('INSERT INTO users VALUES (1, "Alice"), (2, "Bob")')
    db1.commit()

    # 第二次调用get_db() - 复用连接
    db2 = get_db()

    # 查询数据
    cursor = db2.execute('SELECT * FROM users')
    users = [dict(row) for row in cursor.fetchall()]

    return jsonify({
        'message': '数据库连接演示',
        'db1_id': id(db1),
        'db2_id': id(db2),
        'same_connection': db1 is db2,  # True - 是同一个连接
        'users': users
    })


# ==================== 示例3: 权限检查 ====================

def check_permission(required_role):
    """
    装饰器: 检查用户权限
    """
    from functools import wraps

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # 从g对象获取用户角色
            user_role = getattr(g, 'user_role', 'guest')

            if user_role != required_role:
                return jsonify({
                    'error': 'Permission denied',
                    'required_role': required_role,
                    'your_role': user_role
                }), 403

            return f(*args, **kwargs)

        return decorated_function
    return decorator


@demo_g_bp.before_request
def load_user_role():
    """
    加载用户角色到g对象
    """
    # 模拟从数据库或token中获取用户角色
    role_map = {
        'Alice': 'admin',
        'Bob': 'user',
        'Guest': 'guest'
    }

    g.user_role = role_map.get(g.user, 'guest')
    print(f"[Auth] 用户 {g.user} 的角色: {g.user_role}")


@demo_g_bp.route('/admin-only')
@check_permission('admin')
def admin_only():
    """
    示例: 需要admin权限的接口
    访问: http://127.0.0.1:5000/demo-g/admin-only?user=Alice  (成功)
    访问: http://127.0.0.1:5000/demo-g/admin-only?user=Bob    (失败)
    """
    return jsonify({
        'message': 'Welcome, admin!',
        'user': g.user,
        'role': g.user_role
    })


@demo_g_bp.route('/user-area')
@check_permission('user')
def user_area():
    """
    示例: 需要user权限的接口
    访问: http://127.0.0.1:5000/demo-g/user-area?user=Bob  (成功)
    """
    return jsonify({
        'message': 'Welcome, user!',
        'user': g.user,
        'role': g.user_role
    })


# ==================== 示例4: 缓存计算结果 ====================

@demo_g_bp.route('/expensive-calculation')
def expensive_calculation():
    """
    示例: 使用g对象缓存昂贵的计算结果
    访问: http://127.0.0.1:5000/demo-g/expensive-calculation
    """
    # 检查缓存
    if not hasattr(g, 'calculation_result'):
        print("[Calculation] 执行昂贵的计算...")
        time.sleep(0.1)  # 模拟耗时操作
        g.calculation_result = sum(range(1000000))
        g.calculation_cached = False
    else:
        print("[Calculation] 使用缓存结果")
        g.calculation_cached = True

    return jsonify({
        'result': g.calculation_result,
        'cached': g.calculation_cached
    })


# ==================== 示例5: 请求上下文传递 ====================

def helper_function():
    """
    辅助函数: 可以访问g对象
    """
    return {
        'helper_user': g.user,
        'helper_request_id': g.request_id
    }


@demo_g_bp.route('/context-demo')
def context_demo():
    """
    示例: g对象在函数间传递上下文
    访问: http://127.0.0.1:5000/demo-g/context-demo?user=Charlie
    """
    # 在视图函数中设置数据
    g.custom_data = "This is custom data"

    # 调用辅助函数,它可以访问g对象
    helper_result = helper_function()

    return jsonify({
        'message': 'Context demo',
        'view_user': g.user,
        'custom_data': g.custom_data,
        'helper_result': helper_result
    })


# ==================== 示例6: 错误处理 ====================

@demo_g_bp.route('/error-demo')
def error_demo():
    """
    示例: 在错误处理中使用g对象
    访问: http://127.0.0.1:5000/demo-g/error-demo
    """
    # 故意触发错误
    raise ValueError("This is a test error")


@demo_g_bp.errorhandler(ValueError)
def handle_value_error(error):
    """
    错误处理器: 可以访问g对象
    """
    return jsonify({
        'error': str(error),
        'user': getattr(g, 'user', 'Unknown'),
        'request_id': getattr(g, 'request_id', 'Unknown'),
        'timestamp': time.time()
    }), 400


# ==================== 示例7: 多次调用同一个函数 ====================

def get_config():
    """
    获取配置(使用g对象缓存)
    """
    if 'config' not in g:
        print("[Config] 加载配置...")
        g.config = {
            'app_name': 'Flask Demo',
            'version': '1.0.0',
            'debug': True
        }
    else:
        print("[Config] 使用缓存的配置")

    return g.config


@demo_g_bp.route('/config-demo')
def config_demo():
    """
    示例: 多次调用get_config(),只加载一次
    访问: http://127.0.0.1:5000/demo-g/config-demo
    """
    # 第一次调用
    config1 = get_config()

    # 第二次调用(使用缓存)
    config2 = get_config()

    # 第三次调用(使用缓存)
    config3 = get_config()

    return jsonify({
        'config': config1,
        'same_object': config1 is config2 is config3  # True
    })


# ==================== 示例8: 查看g对象的所有内容 ====================

@demo_g_bp.route('/inspect-g')
def inspect_g():
    """
    示例: 查看g对象中存储的所有数据
    访问: http://127.0.0.1:5000/demo-g/inspect-g?user=Inspector
    """
    # 获取g对象的所有属性
    g_data = {}
    for key in dir(g):
        if not key.startswith('_'):
            try:
                value = getattr(g, key)
                # 只显示简单类型
                if isinstance(value, (str, int, float, bool, type(None))):
                    g_data[key] = value
                else:
                    g_data[key] = f"<{type(value).__name__}>"
            except:
                pass

    return jsonify({
        'message': 'g对象内容',
        'g_data': g_data
    })

