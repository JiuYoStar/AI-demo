# app/blueprints/context_demo.py
# Flask 上下文演示 - 请求上下文 vs 应用上下文

from flask import Blueprint, g, request, current_app, jsonify
import time

context_demo_bp = Blueprint('context_demo', __name__, url_prefix='/context')


# ==================== 请求上下文演示 ====================

@context_demo_bp.before_request
def before_request():
    """
    在每个请求之前执行
    这里有请求上下文,可以使用: g, request
    """
    print("\n" + "🟢 " * 35)
    print("【Before Request】请求上下文已创建")
    print("=" * 70)

    # ✅ 可以使用 g 对象
    g.user = request.args.get('user', 'Guest')
    g.request_id = f"REQ-{int(time.time() * 1000)}"
    g.start_time = time.time()
    g.custom_data = {"flag": "before_request"}

    # ✅ 可以使用 request 对象
    print(f"  📍 请求路径: {request.path}")
    print(f"  📍 请求方法: {request.method}")
    print(f"  📍 请求参数: {dict(request.args)}")

    # ✅ 可以使用 current_app
    print(f"  📍 应用名称: {current_app.name}")

    # ✅ 可以使用 g 对象
    print(f"  📍 g.user: {g.user}")
    print(f"  📍 g.request_id: {g.request_id}")
    print(f"  📍 g对象ID: {id(g)}")
    print("=" * 70)


@context_demo_bp.route('/route1')
def route1():
    """
    路由1: 演示请求上下文的使用
    访问: http://127.0.0.1:5000/context/route1?user=Alice
    """
    print("\n" + "🔵 " * 35)
    print("【Route 1】在视图函数中")
    print("=" * 70)

    # ✅ 访问 g 对象
    print(f"  📌 g.user: {g.user}")
    print(f"  📌 g.request_id: {g.request_id}")
    print(f"  📌 g.custom_data: {g.custom_data}")
    print(f"  📌 g对象ID: {id(g)}")

    # ✅ 访问 request 对象
    print(f"  📌 request.path: {request.path}")
    print(f"  📌 request.endpoint: {request.endpoint}")

    # ✅ 访问 current_app
    print(f"  📌 current_app.name: {current_app.name}")

    # 在视图函数中修改g对象
    g.route_name = "route1"
    g.custom_data["route"] = "route1"

    print("=" * 70)

    return jsonify({
        'route': 'route1',
        'user': g.user,
        'request_id': g.request_id,
        'custom_data': g.custom_data,
        'message': '请求上下文可用'
    })


@context_demo_bp.route('/route2')
def route2():
    """
    路由2: 演示同一个请求中g对象的共享
    访问: http://127.0.0.1:5000/context/route2?user=Bob
    """
    print("\n" + "🟡 " * 35)
    print("【Route 2】另一个路由")
    print("=" * 70)

    # 可以访问在before_request中设置的g变量
    print(f"  📌 g.user (来自before_request): {g.user}")
    print(f"  📌 g.request_id (来自before_request): {g.request_id}")
    print(f"  📌 g对象ID: {id(g)}")

    # 检查route1中设置的变量是否存在
    # 注意: 不同的请求有不同的g对象!
    has_route_name = hasattr(g, 'route_name')
    print(f"  📌 是否有 g.route_name: {has_route_name}")

    # 设置route2特有的变量
    g.route_name = "route2"

    print("=" * 70)

    return jsonify({
        'route': 'route2',
        'user': g.user,
        'request_id': g.request_id,
        'has_route1_data': has_route_name,
        'message': '每个请求都有独立的g对象'
    })


@context_demo_bp.route('/multi-call')
def multi_call():
    """
    路由3: 演示在同一请求中多次访问g对象
    访问: http://127.0.0.1:5000/context/multi-call?user=Charlie
    """
    print("\n" + "🟣 " * 35)
    print("【Multi Call】多次调用辅助函数")
    print("=" * 70)

    # 调用辅助函数1
    result1 = helper_function_1()

    # 调用辅助函数2
    result2 = helper_function_2()

    # 调用辅助函数3
    result3 = helper_function_3()

    print("=" * 70)

    return jsonify({
        'route': 'multi-call',
        'user': g.user,
        'request_id': g.request_id,
        'helper1_result': result1,
        'helper2_result': result2,
        'helper3_result': result3,
        'message': '所有函数共享同一个g对象'
    })


def helper_function_1():
    """辅助函数1: 可以访问g对象"""
    print(f"  [Helper 1] 访问 g.user: {g.user}")
    print(f"  [Helper 1] g对象ID: {id(g)}")

    # 在辅助函数中也可以修改g对象
    g.helper1_called = True

    return f"Helper1 called by {g.user}"


def helper_function_2():
    """辅助函数2: 可以看到helper1设置的变量"""
    print(f"  [Helper 2] 访问 g.user: {g.user}")
    print(f"  [Helper 2] g对象ID: {id(g)}")
    print(f"  [Helper 2] helper1_called: {getattr(g, 'helper1_called', False)}")

    g.helper2_called = True

    return f"Helper2 sees helper1's data"


def helper_function_3():
    """辅助函数3: 可以看到所有之前设置的变量"""
    print(f"  [Helper 3] 访问 g.user: {g.user}")
    print(f"  [Helper 3] g对象ID: {id(g)}")
    print(f"  [Helper 3] helper1_called: {getattr(g, 'helper1_called', False)}")
    print(f"  [Helper 3] helper2_called: {getattr(g, 'helper2_called', False)}")

    # 查看g对象中的所有变量
    g_vars = {k: v for k, v in vars(g).items() if not k.startswith('_')}
    print(f"  [Helper 3] g对象所有变量: {g_vars}")

    return f"Helper3 sees all data"


@context_demo_bp.after_request
def after_request(response):
    """
    在每个请求之后执行
    这里仍然可以访问g对象
    """
    print("\n" + "🔴 " * 35)
    print("【After Request】请求即将结束")
    print("=" * 70)

    # ✅ 仍然可以访问g对象
    if hasattr(g, 'start_time'):
        elapsed = time.time() - g.start_time
        print(f"  📍 总耗时: {elapsed:.4f}s")
        print(f"  📍 用户: {g.user}")
        print(f"  📍 请求ID: {g.request_id}")

        # 添加响应头
        response.headers['X-Request-ID'] = g.request_id
        response.headers['X-User'] = g.user
        response.headers['X-Processing-Time'] = f'{elapsed:.4f}s'

    print(f"  📍 响应状态码: {response.status_code}")
    print(f"  📍 g对象ID: {id(g)}")
    print("=" * 70)

    return response


@context_demo_bp.teardown_request
def teardown_request(error):
    """
    请求结束时执行(即使出错也会执行)
    这里仍然可以访问g对象
    """
    print("\n" + "⚫ " * 35)
    print("【Teardown Request】清理请求上下文")
    print("=" * 70)

    # ✅ 仍然可以访问g对象
    print(f"  📍 清理用户: {getattr(g, 'user', 'Unknown')}")
    print(f"  📍 请求ID: {getattr(g, 'request_id', 'Unknown')}")

    # 清理资源
    db = g.pop('db', None)
    if db:
        print(f"  📍 关闭数据库连接")

    if error:
        print(f"  ❌ 请求出错: {error}")
    else:
        print(f"  ✅ 请求正常结束")

    print("=" * 70)
    print("🏁 请求上下文即将销毁\n")


# ==================== 对比: 应用上下文 ====================

@context_demo_bp.route('/app-context-demo')
def app_context_demo():
    """
    演示应用上下文
    访问: http://127.0.0.1:5000/context/app-context-demo
    """
    print("\n" + "🟠 " * 35)
    print("【App Context】应用上下文演示")
    print("=" * 70)

    # 在请求上下文中,应用上下文也是可用的
    print(f"  📌 应用名称: {current_app.name}")
    print(f"  📌 应用配置: DEBUG = {current_app.config.get('DEBUG')}")
    print(f"  📌 应用根路径: {current_app.root_path}")
    print(f"  📌 current_app对象ID: {id(current_app._get_current_object())}")

    # 请求上下文的变量
    print(f"  📌 g.user (请求上下文): {g.user}")
    print(f"  📌 request.path (请求上下文): {request.path}")

    print("=" * 70)

    return jsonify({
        'app_name': current_app.name,
        'debug': current_app.config.get('DEBUG'),
        'root_path': current_app.root_path,
        'user': g.user,
        'request_path': request.path,
        'message': '请求上下文包含应用上下文'
    })


# ==================== 比较不同请求的g对象 ====================

@context_demo_bp.route('/compare-requests')
def compare_requests():
    """
    演示不同请求有不同的g对象
    访问: http://127.0.0.1:5000/context/compare-requests?user=User1
    然后: http://127.0.0.1:5000/context/compare-requests?user=User2
    """
    print("\n" + "🔷 " * 35)
    print("【Compare】对比不同请求")
    print("=" * 70)

    # 每个请求的g对象是独立的
    print(f"  📌 当前请求的 g.user: {g.user}")
    print(f"  📌 当前请求的 g.request_id: {g.request_id}")
    print(f"  📌 当前请求的 g对象ID: {id(g)}")

    # 检查上一个请求的数据是否存在
    has_previous_data = hasattr(g, 'previous_request_data')
    print(f"  📌 是否有上一个请求的数据: {has_previous_data}")

    # 记录当前请求的数据
    g.current_request_data = {
        'user': g.user,
        'request_id': g.request_id,
        'timestamp': time.time()
    }

    # 查看g对象的所有属性
    g_attrs = {k: str(v)[:50] for k, v in vars(g).items() if not k.startswith('_')}
    print(f"  📌 g对象所有属性: {g_attrs}")

    print("=" * 70)

    return jsonify({
        'message': '每个请求都有独立的g对象',
        'current_user': g.user,
        'current_request_id': g.request_id,
        'g_object_id': id(g),
        'has_previous_data': has_previous_data,
        'g_attributes': g_attrs
    })


# ==================== 模拟并发请求 ====================

@context_demo_bp.route('/slow-request')
def slow_request():
    """
    慢请求: 模拟耗时操作,验证g对象的线程安全性
    访问: http://127.0.0.1:5000/context/slow-request?user=SlowUser

    可以同时发起多个请求,观察g对象是否隔离
    """
    print("\n" + "🐌 " * 35)
    print(f"【Slow Request】请求ID: {g.request_id}")
    print("=" * 70)

    print(f"  📌 开始时的 g.user: {g.user}")
    print(f"  📌 g对象ID: {id(g)}")

    # 模拟耗时操作
    print(f"  ⏳ 模拟耗时操作(2秒)...")
    time.sleep(2)

    print(f"  📌 结束时的 g.user: {g.user}")
    print(f"  📌 g.user 是否变化: {g.user == request.args.get('user', 'Guest')}")
    print(f"  📌 g对象ID: {id(g)}")

    print("=" * 70)

    return jsonify({
        'message': '慢请求完成',
        'user': g.user,
        'request_id': g.request_id,
        'processing_time': '2s',
        'g_object_id': id(g)
    })


# ==================== 查看上下文栈 ====================

@context_demo_bp.route('/context-stack')
def context_stack():
    """
    查看上下文栈信息
    访问: http://127.0.0.1:5000/context/context-stack
    """
    from flask.globals import request_ctx, app_ctx

    print("\n" + "📚 " * 35)
    print("【Context Stack】上下文栈信息")
    print("=" * 70)

    # 请求上下文信息
    if request_ctx:
        print(f"  📌 请求上下文存在: True")
        print(f"  📌 请求上下文对象: {request_ctx}")

    # 应用上下文信息
    if app_ctx:
        print(f"  📌 应用上下文存在: True")
        print(f"  📌 应用上下文对象: {app_ctx}")

    # g对象信息
    print(f"  📌 g对象ID: {id(g)}")
    print(f"  📌 g.user: {g.user}")

    # current_app信息
    print(f"  📌 current_app: {current_app}")
    print(f"  📌 current_app.name: {current_app.name}")

    # request信息
    print(f"  📌 request.path: {request.path}")
    print(f"  📌 request对象ID: {id(request)}")

    print("=" * 70)

    return jsonify({
        'message': '上下文栈信息',
        'request_context': str(request_ctx),
        'app_context': str(app_ctx),
        'g_object_id': id(g),
        'request_object_id': id(request),
        'current_app_name': current_app.name
    })


@context_demo_bp.after_request
def after_context_request(response):
    """
    蓝图级别的after_request
    """
    print("\n" + "🟢 " * 35)
    print("【After Request - Blueprint】蓝图级别的after_request")
    print("=" * 70)

    print(f"  📌 g.user: {g.user}")
    print(f"  📌 响应状态: {response.status_code}")

    # 添加蓝图特有的响应头
    response.headers['X-Blueprint'] = 'context_demo'

    print("=" * 70)

    return response


# ==================== 上下文对比总结路由 ====================

@context_demo_bp.route('/summary')
def summary():
    """
    总结: 请求上下文 vs 应用上下文
    访问: http://127.0.0.1:5000/context/summary
    """
    print("\n" + "📊 " * 35)
    print("【Summary】上下文对比总结")
    print("=" * 70)

    summary_data = {
        '请求上下文变量': {
            'g': {
                'user': g.user,
                'request_id': g.request_id,
                'object_id': id(g)
            },
            'request': {
                'path': request.path,
                'method': request.method,
                'endpoint': request.endpoint,
                'object_id': id(request)
            }
        },
        '应用上下文变量': {
            'current_app': {
                'name': current_app.name,
                'debug': current_app.config.get('DEBUG'),
                'object_id': id(current_app._get_current_object())
            }
        },
        '说明': {
            'g对象': '请求级别,每个请求独立,请求结束后清理',
            'request对象': '请求级别,包含请求的所有信息',
            'current_app': '应用级别,指向当前Flask应用实例'
        }
    }

    for category, data in summary_data.items():
        print(f"\n  【{category}】")
        print(f"  {data}")

    print("\n" + "=" * 70)

    return jsonify(summary_data)

