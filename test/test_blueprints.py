#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
蓝图功能测试脚本
用于验证所有蓝图路由是否正常工作
"""

import requests
import json
from colorama import init, Fore, Style

# 初始化colorama(用于彩色输出)
# 如果colorama未安装或初始化失败,则跳过彩色输出功能
try:
    init(autoreset=True)
except Exception:
    # 捕获所有异常,但不影响程序继续运行
    pass

BASE_URL = 'http://127.0.0.1:5000'

def print_success(message):
    """打印成功信息"""
    print(f"{Fore.GREEN}✅ {message}{Style.RESET_ALL}")

def print_error(message):
    """打印错误信息"""
    print(f"{Fore.RED}❌ {message}{Style.RESET_ALL}")

def print_info(message):
    """打印提示信息"""
    print(f"{Fore.CYAN}ℹ️  {message}{Style.RESET_ALL}")

def test_route(method, path, expected_status=200, description=""):
    """
    测试单个路由

    参数:
        method: HTTP方法(GET, POST等)
        path: 路由路径
        expected_status: 期望的HTTP状态码
        description: 测试描述
    """
    url = f"{BASE_URL}{path}"
    print_info(f"测试: {description}")
    print(f"      {method} {path}")

    try:
        if method == 'GET':
            response = requests.get(url, timeout=2)
        elif method == 'POST':
            response = requests.post(url, json={'test': 'data'}, timeout=2)
        elif method == 'PUT':
            response = requests.put(url, json={'test': 'data'}, timeout=2)
        elif method == 'DELETE':
            response = requests.delete(url, timeout=2)
        else:
            print_error(f"不支持的HTTP方法: {method}")
            return False

        if response.status_code == expected_status:
            print_success(f"状态码: {response.status_code}")
            try:
                data = response.json()
                print(f"      响应: {json.dumps(data, ensure_ascii=False, indent=2)[:200]}...")
            except:
                print(f"      响应: {response.text[:100]}...")
            print()
            return True
        else:
            print_error(f"状态码错误: 期望 {expected_status}, 实际 {response.status_code}")
            print()
            return False

    except requests.exceptions.ConnectionError:
        print_error("连接失败! 请确保Flask应用正在运行")
        print_info("启动命令: python run.py")
        print()
        return False
    except Exception as e:
        print_error(f"测试失败: {str(e)}")
        print()
        return False

def main():
    """主测试函数"""
    print("\n" + "="*60)
    print("Flask Blueprint 测试脚本")
    print("="*60 + "\n")

    results = []

    # 测试主应用路由
    print(f"{Fore.YELLOW}{'='*60}")
    print("测试主应用路由")
    print(f"{'='*60}{Style.RESET_ALL}\n")

    results.append(test_route('GET', '/', description="主页"))
    results.append(test_route('GET', '/login', description="登录页"))
    results.append(test_route('GET', '/?user=Alice', description="主页(带用户参数)"))

    # 测试用户蓝图
    print(f"{Fore.YELLOW}{'='*60}")
    print("测试用户蓝图 (user_bp)")
    print(f"{'='*60}{Style.RESET_ALL}\n")

    results.append(test_route('GET', '/user/', description="用户首页"))
    results.append(test_route('GET', '/user/profile', description="用户资料"))
    results.append(test_route('GET', '/user/profile/123', description="指定用户资料"))
    results.append(test_route('GET', '/user/settings', description="用户设置(GET)"))
    results.append(test_route('POST', '/user/settings', description="用户设置(POST)"))

    # 测试管理员蓝图
    print(f"{Fore.YELLOW}{'='*60}")
    print("测试管理员蓝图 (admin_bp)")
    print(f"{'='*60}{Style.RESET_ALL}\n")

    results.append(test_route('GET', '/admin/', description="管理后台首页"))
    results.append(test_route('GET', '/admin/dashboard', description="管理仪表盘"))
    results.append(test_route('GET', '/admin/users', description="用户列表"))
    results.append(test_route('GET', '/admin/users?page=2&limit=5', description="用户列表(分页)"))
    results.append(test_route('GET', '/admin/users/123', description="用户详情"))
    results.append(test_route('PUT', '/admin/users/123', description="更新用户"))
    results.append(test_route('DELETE', '/admin/users/123', description="删除用户"))
    results.append(test_route('GET', '/admin/stats', description="系统统计"))

    # 测试API v1蓝图
    print(f"{Fore.YELLOW}{'='*60}")
    print("测试API v1蓝图 (api_v1_bp)")
    print(f"{'='*60}{Style.RESET_ALL}\n")

    results.append(test_route('GET', '/api/v1/', description="API v1 首页"))
    results.append(test_route('GET', '/api/v1/posts', description="文章列表(v1)"))
    results.append(test_route('GET', '/api/v1/posts/1', description="文章详情(v1)"))

    # 测试API v2蓝图
    print(f"{Fore.YELLOW}{'='*60}")
    print("测试API v2蓝图 (api_v2_bp)")
    print(f"{'='*60}{Style.RESET_ALL}\n")

    results.append(test_route('GET', '/api/v2/', description="API v2 首页"))
    results.append(test_route('GET', '/api/v2/posts', description="文章列表(v2)"))
    results.append(test_route('GET', '/api/v2/posts/1', description="文章详情(v2)"))
    results.append(test_route('GET', '/api/v2/comments?post_id=1', description="评论列表"))

    # 测试总结
    print(f"{Fore.YELLOW}{'='*60}")
    print("测试总结")
    print(f"{'='*60}{Style.RESET_ALL}\n")

    total = len(results)
    passed = sum(results)
    failed = total - passed

    print(f"总测试数: {total}")
    print_success(f"通过: {passed}")
    if failed > 0:
        print_error(f"失败: {failed}")

    success_rate = (passed / total * 100) if total > 0 else 0
    print(f"\n成功率: {success_rate:.1f}%\n")

    if failed == 0:
        print_success("🎉 所有测试通过!")
    else:
        print_error("⚠️  部分测试失败,请检查应用是否正常运行")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n测试被用户中断")
    except Exception as e:
        print_error(f"测试脚本出错: {str(e)}")

