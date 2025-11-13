from flask import Flask, request, g, current_app

app = Flask(__name__)

@app.before_request
def before():
    g.user = "Alice"
    g.route_name = request.endpoint  # 记录路由名称
    print(f"\n🟢 [Before Request] 路径: {request.path}, 路由: {request.endpoint}")


# ==================== 方法1: 使用 teardown_request 并检查路径 ====================

@app.teardown_request
def teardown_by_path(exception):
    """
    方法1: 在teardown中检查请求路径,执行不同的清理逻辑
    """
    if not hasattr(g, 'route_name'):
        return

    print(f"\n⚫ [Teardown Request] 清理路由: {g.route_name}")

    # 根据不同的路径执行不同的清理
    if g.route_name == 'index':
        print("   ✅ 执行 index 路由的专属清理")
        # index 特定的清理逻辑

    elif g.route_name == 'slow_route':
        print("   ✅ 执行 slow 路由的专属清理")
        # slow 特定的清理逻辑

    elif g.route_name == 'api_route':
        print("   ✅ 执行 api 路由的专属清理")
        # api 特定的清理逻辑

    else:
        print(f"   ℹ️  通用清理 (路由: {g.route_name})")


# ==================== 方法2: 使用蓝图的 teardown_request ====================

from flask import Blueprint

# 为不同的功能模块创建蓝图
user_bp = Blueprint('user', __name__, url_prefix='/user')
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@user_bp.teardown_request
def user_teardown(exception):
    """
    方法2: 蓝图级别的teardown
    只对 /user/* 路由生效
    """
    print(f"\n⚫ [User Blueprint Teardown] 清理用户模块资源")
    print(f"   路由: {g.route_name}")


@user_bp.route('/profile')
def user_profile():
    print(f"🔵 [User Route] 处理用户资料请求")
    return f"User Profile: {g.user}"


@admin_bp.teardown_request
def admin_teardown(exception):
    """
    只对 /admin/* 路由生效
    """
    print(f"\n⚫ [Admin Blueprint Teardown] 清理管理员模块资源")
    print(f"   路由: {g.route_name}")


@admin_bp.route('/dashboard')
def admin_dashboard():
    print(f"🔵 [Admin Route] 处理管理员仪表盘请求")
    return f"Admin Dashboard: {g.user}"


# 注册蓝图
app.register_blueprint(user_bp)
app.register_blueprint(admin_bp)


# ==================== 方法3: 使用装饰器模式 ====================

from functools import wraps

def with_cleanup(cleanup_func):
    """
    方法3: 使用装饰器为特定路由添加清理函数
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                # 执行视图函数
                result = f(*args, **kwargs)
                return result
            finally:
                # 执行清理函数
                print(f"\n⚫ [Decorator Cleanup] 执行 {f.__name__} 的清理")
                cleanup_func()
        return wrapper
    return decorator


def cleanup_for_index():
    """index路由的清理函数"""
    print("   ✅ Index路由专属清理完成")


def cleanup_for_slow():
    """slow路由的清理函数"""
    print("   ✅ Slow路由专属清理完成")


@app.route('/')
@with_cleanup(cleanup_for_index)
def index():
    print(f"🔵 [Index Route] 处理首页请求")
    return f"Hello {g.user}"


@app.route('/slow')
@with_cleanup(cleanup_for_slow)
def slow_route():
    print(f"🔵 [Slow Route] 处理慢请求")
    import time
    time.sleep(0.1)
    return f"Slow response for {g.user}"


@app.route('/api/data')
def api_route():
    print(f"🔵 [API Route] 处理API请求")
    return f"API data for {g.user}"


# ==================== 全局 teardown (所有请求都会执行) ====================

@app.teardown_appcontext
def global_teardown_1(exception):
    """全局teardown 1"""
    print(f"\n⚫ [Global Teardown 1] 路由: {getattr(g, 'route_name', 'Unknown')}")


@app.teardown_appcontext
def global_teardown_2(exception):
    """全局teardown 2 (后注册,先执行)"""
    print(f"\n⚫ [Global Teardown 2] 路由: {getattr(g, 'route_name', 'Unknown')}")


if __name__ == "__main__":
    print("\n" + "="*70)
    print("Flask 路由特定清理演示")
    print("="*70)
    print("\n测试命令:")
    print("  curl http://127.0.0.1:5000/")
    print("  curl http://127.0.0.1:5000/slow")
    print("  curl http://127.0.0.1:5000/user/profile")
    print("  curl http://127.0.0.1:5000/admin/dashboard")
    print("  curl http://127.0.0.1:5000/api/data")
    print("\n" + "="*70 + "\n")

    app.run(debug=True)
