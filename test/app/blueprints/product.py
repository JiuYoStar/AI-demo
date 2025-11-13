# app/blueprints/product.py
# 产品管理蓝图 - 演示自动注册功能

from flask import Blueprint, jsonify, request

# 创建产品蓝图
product_bp = Blueprint('product', __name__, url_prefix='/product')


@product_bp.route('/')
def product_index():
    """
    产品首页
    访问: http://127.0.0.1:5000/product/
    """
    return jsonify({
        'message': 'Product Blueprint Index',
        'blueprint': 'product',
        'routes': [
            '/product/',
            '/product/list',
            '/product/<product_id>',
            '/product/search'
        ]
    })


@product_bp.route('/list')
def product_list():
    """
    产品列表
    访问: http://127.0.0.1:5000/product/list?page=1&limit=10
    """
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)

    # 模拟产品数据
    products = [
        {
            'id': i,
            'name': f'Product {i}',
            'price': 99.99 + i,
            'stock': 100 - i
        }
        for i in range((page-1)*limit + 1, page*limit + 1)
    ]

    return jsonify({
        'page': page,
        'limit': limit,
        'total': 100,
        'products': products
    })


@product_bp.route('/<int:product_id>')
def product_detail(product_id):
    """
    产品详情
    访问: http://127.0.0.1:5000/product/123
    """
    return jsonify({
        'id': product_id,
        'name': f'Product {product_id}',
        'description': f'This is product {product_id}',
        'price': 99.99,
        'stock': 50,
        'category': 'Electronics',
        'rating': 4.5
    })


@product_bp.route('/search')
def product_search():
    """
    产品搜索
    访问: http://127.0.0.1:5000/product/search?q=laptop
    """
    query = request.args.get('q', '')

    if not query:
        return jsonify({
            'error': 'Search query is required',
            'example': '/product/search?q=laptop'
        }), 400

    # 模拟搜索结果
    results = [
        {
            'id': i,
            'name': f'{query.title()} Model {i}',
            'price': 999.99 + i * 100
        }
        for i in range(1, 4)
    ]

    return jsonify({
        'query': query,
        'count': len(results),
        'results': results
    })


# 产品蓝图的请求钩子
@product_bp.before_request
def before_product_request():
    """在处理产品请求之前执行"""
    print(f"[Product Blueprint] Processing: {request.path}")


# 产品蓝图的错误处理
@product_bp.errorhandler(404)
def product_not_found(error):
    """处理产品蓝图中的404错误"""
    return jsonify({
        'error': 'Product not found',
        'path': request.path
    }), 404

