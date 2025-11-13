# 将 flask-demo1 重命名为 test 的完整指南

## 步骤 1: 重命名目录

在终端中执行:

```bash
cd /Users/lingk/work/py/demo
mv flask-demo1 test
```

## 步骤 2: 更新文件中的路径引用

重命名完成后,需要更新以下文件中的路径:

### 2.1 启动命令.md

将所有 `/Users/lingk/work/py/demo/flask-demo1` 替换为 `/Users/lingk/work/py/demo/test`
将所有 `flask-demo1` 替换为 `test`

### 2.2 环境变量配置说明.md

将所有 `flask-demo1/` 替换为 `test/`
将所有 `/Users/lingk/work/py/demo/flask-demo1` 替换为 `/Users/lingk/work/py/demo/test`

### 2.3 document/README.md

- 第 1 行: `# flask-demo1 - Flask Blueprint 示例项目` → `# test - Flask Blueprint 示例项目`
- 第 18 行: `cd /Users/lingk/work/py/demo/flask-demo1` → `cd /Users/lingk/work/py/demo/test`
- 第 35 行: `source /Users/lingk/work/py/demo/flask-demo1/venv/bin/activate` → `source /Users/lingk/work/py/demo/test/venv/bin/activate`
- 第 42 行: `/Users/lingk/work/py/demo/flask-demo1/venv/bin/flask` → `/Users/lingk/work/py/demo/test/venv/bin/flask`
- 所有 `flask-demo1/` → `test/`

### 2.4 重新创建虚拟环境.sh

将所有 `/Users/lingk/work/py/demo/flask-demo1` 替换为 `/Users/lingk/work/py/demo/test`

### 2.5 test_context.sh

将所有路径中的 `flask-demo1` 替换为 `test`

### 2.6 其他文档文件

在 `document/` 目录下的所有 .md 文件中,将 `flask-demo1` 替换为 `test`

## 步骤 3: 验证虚拟环境

重命名后,虚拟环境的路径引用可能需要更新:

```bash
cd /Users/lingk/work/py/demo/test

# 检查虚拟环境
source venv/bin/activate

# 验证 Python 路径
which python
# 应该输出: /Users/lingk/work/py/demo/test/venv/bin/python

# 如果路径不对,需要重新创建虚拟环境
deactivate
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 步骤 4: 测试启动

```bash
cd /Users/lingk/work/py/demo/test
source venv/bin/activate
python run.py
```

## 快速执行脚本

我已经为你准备了自动化脚本,在终端中执行:

```bash
cd /Users/lingk/work/py/demo
python3 update_project_name.py
```

这个脚本会自动完成所有的重命名和更新工作。

