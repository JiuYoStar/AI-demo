#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Flask API 探索工具
用于查看Flask应用和蓝图的所有可用方法和属性
"""

from flask import Flask, Blueprint
import inspect

def print_section(title):
    """打印分节标题"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def print_methods(obj, obj_name):
    """打印对象的所有方法,并分类显示"""
    print_section(f"{obj_name} 的方法和属性")

    # 获取所有公共方法
    all_methods = [m for m in dir(obj) if not m.startswith('_')]

    # 分类
    categories = {
        '路由相关': lambda m: any(x in m.lower() for x in ['route', 'url', 'endpoint']),
        '蓝图相关': lambda m: 'blueprint' in m.lower(),
        '请求钩子': lambda m: any(x in m for x in ['before', 'after', 'teardown', 'context']),
        '错误处理': lambda m: 'error' in m.lower(),
        '配置相关': lambda m: 'config' in m.lower(),
        '模板相关': lambda m: any(x in m.lower() for x in ['template', 'jinja']),
        '静态文件': lambda m: 'static' in m.lower(),
        '测试相关': lambda m: 'test' in m.lower(),
    }

    # 显示分类方法
    for category, filter_func in categories.items():
        methods = [m for m in all_methods if filter_func(m)]
        if methods:
            print(f"\n【{category}】")
            for method in methods:
                # 获取方法签名
                try:
                    obj_method = getattr(obj, method)
                    if callable(obj_method):
                        sig = inspect.signature(obj_method)
                        print(f"  ✓ {obj_name}.{method}{sig}")
                    else:
                        print(f"  • {obj_name}.{method} (属性)")
                except:
                    print(f"  • {obj_name}.{method}")

    # 显示其他重要方法
    important = ['run', 'test_client', 'add_url_rule', 'make_response', 'logger',
                 'json', 'name', 'import_name', 'root_path']
    other_methods = [m for m in all_methods if m in important]

    if other_methods:
        print(f"\n【其他重要方法/属性】")
        for method in other_methods:
            try:
                obj_method = getattr(obj, method)
                if callable(obj_method):
                    sig = inspect.signature(obj_method)
                    print(f"  ✓ {obj_name}.{method}{sig}")
                else:
                    print(f"  • {obj_name}.{method} (属性)")
            except:
                print(f"  • {obj_name}.{method}")

def show_method_help(obj, method_name):
    """显示方法的详细帮助信息"""
    print_section(f"{method_name} 方法详解")

    try:
        method = getattr(obj, method_name)

        # 方法签名
        if callable(method):
            sig = inspect.signature(method)
            print(f"\n签名: {method_name}{sig}")

        # 文档字符串
        doc = inspect.getdoc(method)
        if doc:
            print(f"\n说明:\n{doc}")
        else:
            print("\n(无文档说明)")

        # 源代码位置
        try:
            source_file = inspect.getfile(method)
            print(f"\n源代码位置: {source_file}")
        except:
            pass

    except AttributeError:
        print(f"\n错误: 找不到方法 '{method_name}'")

def explore_flask_app():
    """探索Flask应用对象"""
    app = Flask(__name__)
    print_methods(app, "Flask应用(app)")

    # 显示一些常用方法的详细说明
    common_methods = ['route', 'register_blueprint', 'before_request', 'errorhandler', 'run']

    for method in common_methods:
        show_method_help(app, method)

def explore_blueprint():
    """探索Blueprint对象"""
    bp = Blueprint('example', __name__)
    print_methods(bp, "Blueprint(蓝图)")

    # 显示一些常用方法的详细说明
    common_methods = ['route', 'before_request', 'errorhandler']

    for method in common_methods:
        show_method_help(bp, method)

def show_usage_examples():
    """显示使用示例"""
    print_section("Flask 常用方法示例")

    examples = {
        "创建路由": """
@app.route('/path')
def view_function():
    return 'Hello'
        """,

        "注册蓝图": """
from flask import Blueprint
bp = Blueprint('name', __name__, url_prefix='/prefix')
app.register_blueprint(bp)
        """,

        "请求钩子": """
@app.before_request
def before():
    # 在每个请求之前执行
    pass

@app.after_request
def after(response):
    # 在每个请求之后执行
    return response
        """,

        "错误处理": """
@app.errorhandler(404)
def not_found(error):
    return {'error': 'Not found'}, 404
        """,

        "获取请求数据": """
from flask import request

@app.route('/data', methods=['POST'])
def handle_data():
    data = request.get_json()
    args = request.args
    form = request.form
    return {'received': data}
        """,

        "返回JSON": """
from flask import jsonify

@app.route('/api/data')
def get_data():
    return jsonify({'key': 'value'})
        """,

        "URL参数": """
@app.route('/user/<int:user_id>')
def user_profile(user_id):
    return f'User {user_id}'
        """,

        "多种HTTP方法": """
@app.route('/resource', methods=['GET', 'POST', 'PUT', 'DELETE'])
def resource():
    if request.method == 'GET':
        return 'Get'
    elif request.method == 'POST':
        return 'Post'
        """,
    }

    for title, code in examples.items():
        print(f"\n【{title}】")
        print(code)

def interactive_explore():
    """交互式探索"""
    print_section("Flask API 交互式探索工具")
    print("\n提示: 在Python交互式环境中使用以下命令:\n")

    commands = [
        ("查看所有方法", "dir(app)"),
        ("查看公共方法", "[m for m in dir(app) if not m.startswith('_')]"),
        ("查看方法帮助", "help(app.route)"),
        ("查看方法签名", "import inspect; inspect.signature(app.route)"),
        ("查看文档字符串", "print(app.route.__doc__)"),
        ("查看对象类型", "type(app)"),
        ("查看所有属性", "vars(app)"),
        ("查看类的MRO", "Flask.__mro__"),
    ]

    for desc, cmd in commands:
        print(f"  {desc:20s} → {cmd}")

    print("\n" + "="*70)
    print("示例: 在Python中运行")
    print("="*70)
    print("""
from app import app

# 查看所有路由
for rule in app.url_map.iter_rules():
    print(f"{rule.endpoint:30s} {rule.methods} {rule.rule}")

# 查看所有蓝图
for name, blueprint in app.blueprints.items():
    print(f"蓝图: {name}")

# 查看配置
print(app.config)

# 查看方法帮助
help(app.register_blueprint)
    """)

def main():
    """主函数"""
    print("\n" + "🔍 " * 30)
    print("Flask API 探索工具")
    print("🔍 " * 30)

    # 1. 探索Flask应用
    explore_flask_app()

    # 2. 探索Blueprint
    explore_blueprint()

    # 3. 显示使用示例
    show_usage_examples()

    # 4. 交互式探索提示
    interactive_explore()

    print("\n" + "="*70)
    print("提示: 运行 'python explore_api.py > flask_api_reference.txt' 保存到文件")
    print("="*70 + "\n")

if __name__ == '__main__':
    main()

