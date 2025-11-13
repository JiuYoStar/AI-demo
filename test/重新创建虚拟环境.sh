#!/bin/bash
# 重新创建虚拟环境脚本

echo "🔧 重新创建虚拟环境"
echo "================================"

cd /Users/lingk/work/py/demo/test

# 1. 停用当前环境
echo "1. 停用当前虚拟环境..."
deactivate 2>/dev/null || true

# 2. 备份requirements.txt
echo "2. 备份依赖列表..."
cp requirements.txt requirements.txt.bak

# 3. 删除旧的虚拟环境
echo "3. 删除旧的虚拟环境..."
rm -rf venv

# 4. 创建新的虚拟环境
echo "4. 创建新的虚拟环境..."
python -m venv venv

# 5. 激活新环境
echo "5. 激活新环境..."
source venv/bin/activate

# 6. 升级pip
echo "6. 升级pip..."
pip install --upgrade pip -q

# 7. 安装依赖
echo "7. 安装依赖..."
pip install -r requirements.txt -q

# 8. 验证
echo ""
echo "================================"
echo "✅ 虚拟环境重新创建完成!"
echo "================================"
echo "VIRTUAL_ENV: $VIRTUAL_ENV"
echo "Python: $(which python)"
echo "Flask: $(which flask)"
echo ""
echo "Flask版本:"
flask --version
echo ""
echo "🚀 现在可以运行: flask run"

