# app/blueprints/__init__.py
# 蓝图包的初始化文件
# 用于组织和管理多个蓝图模块

# 这个文件可以为空,也可以导入所有蓝图方便统一注册
from app.blueprints.user import user_bp
from app.blueprints.admin import admin_bp

__all__ = ['user_bp', 'admin_bp']

