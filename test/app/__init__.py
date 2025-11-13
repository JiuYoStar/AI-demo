# app/__init__.py - 创建Flask应用实例并注册路由
# 这个文件将app目录变成一个Python包,并创建唯一的Flask应用实例

from flask import Flask, g

# 创建Flask应用实例
# __name__ 参数帮助Flask确定应用的根路径
app = Flask(__name__)
# print(g, "g")
# g.user = "Guest"
# ⚠️ 重要: g对象不能在这里使用!
# g对象只能在"请求上下文"中使用,即:
#   - @app.before_request 函数中
#   - 视图函数中
#   - @app.after_request 函数中
#   - @app.teardown_request 函数中
# 在模块导入阶段使用g对象会报错: "Working outside of application context"

print(__name__, "app/__init__.py")

# 在创建app实例之后导入其他模块
# 这样可以避免循环导入的问题,同时确保路由被正确注册
from app import views, auth  # pyright: ignore[reportUnusedImport]

# ==================== 自动扫描并注册蓝图 ====================
import os
import importlib
from pathlib import Path
from flask import Blueprint

def auto_register_blueprints(app, blueprints_dir='app/blueprints'):
    """
    自动扫描并注册蓝图

    参数:
        app: Flask应用实例
        blueprints_dir: 蓝图目录路径

    工作原理:
        1. 扫描blueprints目录下的所有.py文件(排除__init__.py)
        2. 动态导入每个模块
        3. 查找模块中所有Blueprint实例
        4. 自动注册到Flask应用
    """
    print("\n" + "="*60)
    print("🔍 自动扫描并注册蓝图...")
    print("="*60)

    # 获取蓝图目录的绝对路径
    blueprints_path = Path(blueprints_dir)
    print(blueprints_path, "blueprints_path")

    if not blueprints_path.exists():
        print(f"⚠️  蓝图目录不存在: {blueprints_dir}")
        return

    # 扫描所有Python文件
    blueprint_files = [
        f for f in blueprints_path.glob('*.py')
        if f.name != '__init__.py' and not f.name.startswith('_')
    ]

    registered_count = 0

    for blueprint_file in blueprint_files:
        module_name = blueprint_file.stem  # 获取文件名(不含扩展名)

        try:
            # 动态导入模块
            # 例如: app.blueprints.user
            module_path = f'app.blueprints.{module_name}'
            module = importlib.import_module(module_path)

            print(f"\n📁 扫描模块: {module_path}")

            # 查找模块中的所有Blueprint实例
            blueprints_found = []
            for attr_name in dir(module):
                attr = getattr(module, attr_name)

                # 检查是否是Blueprint实例
                if isinstance(attr, Blueprint):
                    blueprints_found.append((attr_name, attr))

            # 注册找到的蓝图
            if blueprints_found:
                for bp_name, bp in blueprints_found:
                    app.register_blueprint(bp)
                    registered_count += 1

                    # 打印注册信息
                    url_prefix = bp.url_prefix or '/'
                    print(f"  ✅ 注册蓝图: {bp_name:30s} → URL前缀: {url_prefix}")
            else:
                print("  ⚠️  未找到Blueprint实例")

        except Exception as e:
            print(f"  ❌ 导入失败: {e}")

    print("\n" + "†"*60)
    print(f"✨✨✨ 蓝图注册完成! 共注册 {registered_count} 个蓝图")
    print("†"*60 + "\n")

# 调用自动注册函数
auto_register_blueprints(app)

# __all__ 定义了当使用 from app import * 时导出的内容
# 这是可选的,用于明确模块的公共API
__all__ = ['app']

def print_blueprints(app):
    print("\n" + "="*60)
    print("Flask应用对象 (app) 的常用方法:")
    print("="*60)

    # 过滤出公共方法(不以_开头的)
    public_methods = [method for method in dir(app) if not method.startswith('_')]

    # 分类显示
    print("\n【路由相关】")
    route_methods = [m for m in public_methods if 'route' in m.lower() or 'url' in m.lower()]
    for method in route_methods:
        print(f"  - app.{method}")

    print("\n【蓝图相关】")
    blueprint_methods = [m for m in public_methods if 'blueprint' in m.lower()]
    for method in blueprint_methods:
        print(f"  - app.{method}")

    print("\n【请求钩子】")
    hook_methods = [m for m in public_methods if any(x in m for x in ['before', 'after', 'teardown', 'context'])]
    for method in hook_methods:
        print(f"  - app.{method}")

    print("\n【错误处理】")
    error_methods = [m for m in public_methods if 'error' in m.lower()]
    for method in error_methods:
        print(f"  - app.{method}")

    print("\n【配置相关】")
    config_methods = [m for m in public_methods if 'config' in m.lower()]
    for method in config_methods:
        print(f"  - app.{method}")

    print("\n【其他常用方法】")
    other_methods = ['run', 'test_client', 'add_url_rule', 'make_response', 'logger']
    for method in other_methods:
        if method in public_methods:
            print(f"  - app.{method}")

    print("\n" + "="*60)
    print("提示: 使用 help(app.方法名) 查看详细文档")
    print("="*60 + "\n")

#
if __name__ != '__main__':
    print("开发调试: 查看Flask应用的所有方法和属性 -> 仅在引用时执行")
    # print_blueprints(app)


# 手动注册蓝图
# # 注册蓝图(Blueprints)
# # 蓝图是Flask用于组织大型应用的机制,可以将应用分成多个模块
# from app.blueprints.user import user_bp
# from app.blueprints.admin import admin_bp
# from app.blueprints.api import api_v1_bp, api_v2_bp

# print(app.__dict__)
# # 注册用户蓝图 - 所有路由以/user开头
# app.register_blueprint(user_bp)

# # 注册管理员蓝图 - 所有路由以/admin开头
# app.register_blueprint(admin_bp)

# # 注册API蓝图 - 支持版本控制
# app.register_blueprint(api_v1_bp)  # /api/v1/*
# app.register_blueprint(api_v2_bp)  # /api/v2/*

