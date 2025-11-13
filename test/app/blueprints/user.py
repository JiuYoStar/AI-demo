# app/blueprints/user.py
# 用户相关的蓝图模块
# 蓝图(Blueprint)是Flask用于组织路由和视图的机制,类似于子应用

from flask import Blueprint, jsonify, request, render_template_string

# 创建蓝图对象
# 参数说明:
# - 'user': 蓝图名称(内部标识)
# - __name__: 模块名称,帮助Flask定位资源
# - url_prefix='/user': URL前缀,所有路由都会加上这个前缀
user_bp = Blueprint('user', __name__, url_prefix='/user')


@user_bp.route('/')
def user_index():
    """
    用户首页
    访问: http://127.0.0.1:5000/user/
    """
    return jsonify({
        'message': 'User Blueprint Index',
        'blueprint': 'user',
        'routes': [
            '/user/',
            '/user/profile',
            '/user/profile/<user_id>',
            '/user/settings'
        ]
    })


@user_bp.route('/profile')
def user_profile():
    """
    当前用户资料
    访问: http://127.0.0.1:5000/user/profile
    """
    return jsonify({
        'username': 'guest',
        'email': 'guest@example.com',
        'role': 'user'
    })


@user_bp.route('/profile/<int:user_id>')
def user_profile_by_id(user_id):
    """
    指定用户资料(带参数)
    访问: http://127.0.0.1:5000/user/profile/123

    参数:
        user_id: 用户ID(整数)
    """
    return jsonify({
        'user_id': user_id,
        'username': f'user_{user_id}',
        'email': f'user{user_id}@example.com'
    })


@user_bp.route('/settings', methods=['GET', 'POST'])
def user_settings():
    """
    用户设置(支持GET和POST)
    访问: http://127.0.0.1:5000/user/settings
    """
    if request.method == 'POST':
        # 处理POST请求
        data = request.get_json() or request.form.to_dict()
        return jsonify({
            'message': 'Settings updated',
            'data': data
        })
    else:
        # 处理GET请求
        return jsonify({
            'theme': 'dark',
            'language': 'zh-CN',
            'notifications': True
        })


# 蓝图级别的before_request钩子
# 只对当前蓝图的路由生效
@user_bp.before_request
def before_user_request():
    """
    在处理用户蓝图的每个请求之前执行
    可以用于权限检查、日志记录等
    """
    print(f"[User Blueprint] Processing request: {request.path}")


# 蓝图级别的错误处理
@user_bp.errorhandler(404)
def user_not_found(error):
    """
    处理用户蓝图中的404错误
    """
    return jsonify({
        'error': 'User resource not found',
        'path': request.path
    }), 404

