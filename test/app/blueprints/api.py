# app/blueprints/api.py
# API蓝图 - 演示嵌套蓝图和版本控制

from flask import Blueprint, jsonify, request

# 创建API v1蓝图
api_v1_bp = Blueprint('api_v1', __name__, url_prefix='/api/v1')

# 创建API v2蓝图
api_v2_bp = Blueprint('api_v2', __name__, url_prefix='/api/v2')


# ==================== API v1 路由 ====================

@api_v1_bp.route('/')
def api_v1_index():
    """
    API v1 首页
    访问: http://127.0.0.1:5000/api/v1/
    """
    return jsonify({
        'version': '1.0',
        'status': 'deprecated',
        'message': 'Please use API v2',
        'endpoints': [
            '/api/v1/posts',
            '/api/v1/posts/<post_id>'
        ]
    })


@api_v1_bp.route('/posts')
def api_v1_posts():
    """
    获取文章列表 (v1)
    访问: http://127.0.0.1:5000/api/v1/posts
    """
    return jsonify({
        'version': 'v1',
        'posts': [
            {'id': 1, 'title': 'Post 1'},
            {'id': 2, 'title': 'Post 2'}
        ]
    })


@api_v1_bp.route('/posts/<int:post_id>')
def api_v1_post_detail(post_id):
    """
    获取文章详情 (v1)
    访问: http://127.0.0.1:5000/api/v1/posts/1
    """
    return jsonify({
        'version': 'v1',
        'id': post_id,
        'title': f'Post {post_id}',
        'content': 'This is post content from API v1'
    })


# ==================== API v2 路由 ====================

@api_v2_bp.route('/')
def api_v2_index():
    """
    API v2 首页
    访问: http://127.0.0.1:5000/api/v2/
    """
    return jsonify({
        'version': '2.0',
        'status': 'stable',
        'endpoints': [
            '/api/v2/posts',
            '/api/v2/posts/<post_id>',
            '/api/v2/comments'
        ]
    })


@api_v2_bp.route('/posts')
def api_v2_posts():
    """
    获取文章列表 (v2) - 增强版
    访问: http://127.0.0.1:5000/api/v2/posts
    """
    return jsonify({
        'version': 'v2',
        'posts': [
            {
                'id': 1,
                'title': 'Post 1',
                'author': 'Alice',
                'created_at': '2024-01-01',
                'tags': ['python', 'flask']
            },
            {
                'id': 2,
                'title': 'Post 2',
                'author': 'Bob',
                'created_at': '2024-01-02',
                'tags': ['javascript', 'react']
            }
        ]
    })


@api_v2_bp.route('/posts/<int:post_id>')
def api_v2_post_detail(post_id):
    """
    获取文章详情 (v2) - 增强版
    访问: http://127.0.0.1:5000/api/v2/posts/1
    """
    return jsonify({
        'version': 'v2',
        'id': post_id,
        'title': f'Post {post_id}',
        'content': 'This is enhanced post content from API v2',
        'author': 'Alice',
        'created_at': '2024-01-01',
        'updated_at': '2024-01-05',
        'tags': ['python', 'flask', 'api'],
        'views': 1250,
        'likes': 89
    })


@api_v2_bp.route('/comments')
def api_v2_comments():
    """
    获取评论列表 (v2新功能)
    访问: http://127.0.0.1:5000/api/v2/comments?post_id=1
    """
    post_id = request.args.get('post_id', type=int)

    if post_id:
        comments = [
            {
                'id': i,
                'post_id': post_id,
                'author': f'User{i}',
                'content': f'Comment {i} on post {post_id}'
            }
            for i in range(1, 4)
        ]
    else:
        comments = []

    return jsonify({
        'version': 'v2',
        'post_id': post_id,
        'comments': comments
    })


# API通用错误处理
@api_v1_bp.errorhandler(404)
@api_v2_bp.errorhandler(404)
def api_not_found(error):
    """
    API 404错误处理
    """
    return jsonify({
        'error': 'Not Found',
        'message': 'The requested resource does not exist'
    }), 404

