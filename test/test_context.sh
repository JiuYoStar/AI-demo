#!/bin/bash
# Flask 上下文测试脚本

echo "🧪 Flask 上下文测试"
echo "================================"
echo ""

BASE_URL="http://127.0.0.1:5000"

echo "1️⃣ 测试 route1 (基本使用)"
echo "--------------------------------"
curl -s "$BASE_URL/context/route1?user=Alice" | jq .
echo ""

echo "2️⃣ 测试 route2 (不同请求)"
echo "--------------------------------"
curl -s "$BASE_URL/context/route2?user=Bob" | jq .
echo ""

echo "3️⃣ 测试 multi-call (多次调用)"
echo "--------------------------------"
curl -s "$BASE_URL/context/multi-call?user=Charlie" | jq .
echo ""

echo "4️⃣ 测试 context-stack (上下文栈)"
echo "--------------------------------"
curl -s "$BASE_URL/context/context-stack?user=David" | jq .
echo ""

echo "5️⃣ 测试 summary (总结)"
echo "--------------------------------"
curl -s "$BASE_URL/context/summary?user=Eve" | jq .
echo ""

echo "6️⃣ 测试并发请求 (slow-request)"
echo "--------------------------------"
echo "同时发起3个请求,观察g对象隔离性..."
curl -s "$BASE_URL/context/slow-request?user=Concurrent1" &
curl -s "$BASE_URL/context/slow-request?user=Concurrent2" &
curl -s "$BASE_URL/context/slow-request?user=Concurrent3" &
wait
echo ""

echo "================================"
echo "✅ 测试完成!"
echo "💡 查看终端输出,观察g对象的变化"
echo "================================"

