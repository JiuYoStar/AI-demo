# app/auth.py - 认证相关的路由模块
# 从app包中导入Flask应用实例
from app import app

@app.route('/login')
def login():
    """
    登录页面路由
    访问方式: http://127.0.0.1:5000/login
    """
    return "This is login page."

