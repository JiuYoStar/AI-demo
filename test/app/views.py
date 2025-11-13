# app/views.py - 主要的视图路由模块
# 从app包中导入Flask应用实例
from app import app
# 导入Flask的request对象(用于获取请求数据)和g对象(用于存储请求期间的全局数据)
from flask import request, g

@app.before_request
def before_request():
    """
    请求预处理函数
    在每个请求处理之前自动执行
    这里从URL参数中获取user,如果没有则默认为'Guest'
    并将其存储在g对象中,供本次请求的其他函数使用
    """
    g.user = request.args.get('user', 'Guest')

@app.route('/')
def index():
    """
    首页路由
    返回欢迎信息,包含当前用户名
    访问方式: http://127.0.0.1:5000/ 或 http://127.0.0.1:5000/?user=YourName
    """
    return f"Hello, {g.user}!"

