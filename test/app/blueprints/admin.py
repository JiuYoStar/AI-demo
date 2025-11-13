# app/blueprints/admin.py
# 管理员相关的蓝图模块
# 演示如何创建独立的管理后台模块

from flask import Blueprint, jsonify, request, g

# 创建管理员蓝图
# url_prefix='/admin': 所有路由都以/admin开头
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/')
def admin_index():
    """
    管理后台首页
    访问: http://127.0.0.1:5000/admin/
    """
    return jsonify({
        'message': 'Admin Blueprint Index',
        'blueprint': 'admin',
        'routes': [
            '/admin/',
            '/admin/dashboard',
            '/admin/users',
            '/admin/users/<user_id>',
            '/admin/stats'
        ]
    })


@admin_bp.route('/dashboard')
def admin_dashboard():
    """
    管理员仪表盘
    访问: http://127.0.0.1:5000/admin/dashboard
    """
    return jsonify({
        'total_users': 1250,
        'active_users': 856,
        'total_posts': 3420,
        'server_status': 'healthy'
    })


@admin_bp.route('/users')
def admin_users_list():
    """
    用户列表(支持分页)
    访问: http://127.0.0.1:5000/admin/users?page=1&limit=10
    """
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)

    # 模拟用户数据
    users = [
        {'id': i, 'username': f'user_{i}', 'email': f'user{i}@example.com'}
        for i in range((page-1)*limit + 1, page*limit + 1)
    ]

    return jsonify({
        'page': page,
        'limit': limit,
        'total': 1250,
        'users': users
    })


@admin_bp.route('/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def admin_user_detail(user_id):
    """
    用户详情管理(支持查看、更新、删除)
    访问: http://127.0.0.1:5000/admin/users/123

    方法:
        GET: 查看用户详情
        PUT: 更新用户信息
        DELETE: 删除用户
    """
    if request.method == 'GET':
        return jsonify({
            'id': user_id,
            'username': f'user_{user_id}',
            'email': f'user{user_id}@example.com',
            'role': 'user',
            'created_at': '2024-01-01'
        })

    elif request.method == 'PUT':
        data = request.get_json()
        return jsonify({
            'message': f'User {user_id} updated',
            'data': data
        })

    elif request.method == 'DELETE':
        return jsonify({
            'message': f'User {user_id} deleted'
        })


@admin_bp.route('/stats')
def admin_stats():
    """
    系统统计信息
    访问: http://127.0.0.1:5000/admin/stats
    """
    return jsonify({
        'daily_active_users': 523,
        'new_registrations': 45,
        'total_revenue': 12500.50,
        'server_uptime': '15 days 3 hours'
    })


# 管理员蓝图的before_request钩子
@admin_bp.before_request
def check_admin_permission():
    """
    在处理管理员请求之前检查权限
    实际项目中应该检查用户是否有管理员权限
    """
    print(f"[Admin Blueprint] Checking permission for: {request.path}")

    # 模拟权限检查
    # 实际项目中应该检查session或token
    # if not is_admin():
    #     return jsonify({'error': 'Unauthorized'}), 403

    # 将管理员信息存储到g对象中
    g.admin_user = 'admin@example.com'


# 管理员蓝图的after_request钩子
@admin_bp.after_request
def after_admin_request(response):
    """
    在管理员请求处理完成后执行
    可以用于添加响应头、日志记录等
    """
    response.headers['X-Admin-Request'] = 'true'
    print(f"[Admin Blueprint] Request completed: {request.path}")
    return response


# 管理员蓝图的错误处理
@admin_bp.errorhandler(403)
def admin_forbidden(error):
    """
    处理403权限错误
    """
    return jsonify({
        'error': 'Forbidden',
        'message': 'You do not have permission to access this resource'
    }), 403

