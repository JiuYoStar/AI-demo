# Flask 基础教程

## 环境配置与管理

### 1. 创建虚拟环境

```bash
# python -m venv <虚拟环境名称>
# -m 参数: 以模块方式运行Python标准库中的venv模块
# venv: Python内置的虚拟环境模块
# 作用: 创建一个独立的Python环境,避免包冲突
python -m venv venv
```

**说明**:
- `python -m` : 以模块方式运行Python程序
- `venv` (第一个): Python标准库中的虚拟环境模块
- `venv` (第二个): 创建的虚拟环境目录名称(可自定义)

### 2. 激活虚拟环境

```bash
# macOS/Linux (bash/zsh)
# source: shell内置命令,用于在当前shell中执行脚本
# activate: 虚拟环境的激活脚本
# 作用: 修改PATH环境变量,使用虚拟环境中的Python和pip
source venv/bin/activate

# macOS/Linux (csh)
source venv/bin/activate.csh

# macOS/Linux (fish shell)
source venv/bin/activate.fish

# Windows (PowerShell)
venv\Scripts\Activate.ps1

# Windows (cmd)
venv\Scripts\activate.bat
```

**激活后的变化**:
- 命令行提示符前会显示 `(venv)`
- `which python` 指向虚拟环境中的Python
- `which pip` 指向虚拟环境中的pip

### 3. 安装依赖包

```bash
# pip install <包名>
# 作用: 在当前激活的虚拟环境中安装Python包
pip install flask

# 安装指定版本
pip install flask==3.1.2

# 从requirements.txt安装所有依赖
# -r: 从文件读取依赖列表
pip install -r requirements.txt

# 升级包
pip install --upgrade flask

# 卸载包
pip uninstall flask
```

### 4. 查看已安装的包

```bash
# 列出所有已安装的包
pip list

# 查看某个包的详细信息
# show: 显示包的元数据信息
pip show flask

# 导出当前环境的所有包到文件
# freeze: 以requirements格式输出所有包及版本
pip freeze > requirements.txt

# 查看包的依赖关系
pip show flask | grep Requires
```

### 5. 运行Flask应用

```bash
# 方式1: 分步执行
cd /path/to/project          # 进入项目目录
source venv/bin/activate     # 激活虚拟环境
python run.py                # 运行Flask应用

# 方式2: 一行命令执行
# &&: shell运算符,前一个命令成功后才执行下一个命令
cd /path/to/project && source venv/bin/activate && python run.py

# 方式3: 使用Flask命令行工具
export FLASK_APP=run.py      # 设置Flask应用入口
export FLASK_ENV=development # 设置开发环境
flask run                    # 运行应用

# 方式4: 指定主机和端口
python run.py --host=0.0.0.0 --port=8080
# 或在代码中: app.run(host='0.0.0.0', port=8080, debug=True)
```

### 6. 后台运行Flask应用

```bash
# 使用nohup在后台运行
# nohup: no hang up,忽略挂断信号
# &: 将进程放到后台运行
nohup python run.py > flask.log 2>&1 &

# 查看后台进程
ps aux | grep python

# 查看日志
tail -f flask.log

# 停止后台进程
# 先找到进程ID
ps aux | grep run.py
# 然后杀死进程
kill -9 <进程ID>

# 或者一行命令停止
pkill -f run.py
```

### 7. 停用虚拟环境

```bash
# deactivate: 虚拟环境提供的命令
# 作用: 恢复系统默认的Python环境
deactivate
```

### 8. 删除虚拟环境

```bash
# 直接删除虚拟环境目录即可
rm -rf venv/

# 或使用trash命令(更安全,可恢复)
trash venv/
```

### 9. 环境变量管理

```bash
# 查看当前Python路径
which python

# 查看Python版本
python --version

# 查看pip路径
which pip

# 查看环境变量
echo $PATH

# 临时设置环境变量(当前会话有效)
export FLASK_APP=run.py
export FLASK_ENV=development
export FLASK_DEBUG=1

# 使用.env文件管理环境变量
# 1. 安装python-dotenv
pip install python-dotenv

# 2. 创建.env文件
cat > .env << EOF
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key
EOF

# 3. 在代码中加载
# from dotenv import load_dotenv
# load_dotenv()
```

### 10. 常用组合命令

```bash
# 创建项目并初始化环境
mkdir myproject && cd myproject && python -m venv venv && source venv/bin/activate && pip install flask

# 克隆项目后快速启动
git clone <repo> && cd <project> && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt && python run.py

# 更新依赖并重启
source venv/bin/activate && pip install --upgrade -r requirements.txt && python run.py

# 清理并重建环境
deactivate && rm -rf venv && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt
```

### 11. 虚拟环境目录结构

```
venv/
├── bin/                    # 可执行文件(macOS/Linux)
│   ├── activate           # 激活脚本
│   ├── python            # Python解释器
│   ├── pip               # pip包管理器
│   └── flask             # Flask命令行工具
├── lib/                   # 库文件
│   └── python3.x/
│       └── site-packages/ # pip安装的所有包都在这里
├── include/               # C头文件
└── pyvenv.cfg            # 虚拟环境配置
```

### 12. 故障排查命令

```bash
# 检查是否在虚拟环境中
echo $VIRTUAL_ENV
# 如果输出路径,说明在虚拟环境中

# 检查Python路径
which python
# 应该指向venv/bin/python

# 检查模块是否安装
python -c "import flask; print(flask.__version__)"

# 重新安装损坏的包
pip uninstall flask && pip install flask

# 清理pip缓存
pip cache purge

# 检查端口占用
lsof -i :5000
# 或
netstat -an | grep 5000

# 杀死占用端口的进程
lsof -ti:5000 | xargs kill -9
```

---

## flask应用程序架构

-   路由
-   请求响应处理
-   模板
-   应用请求上下文
-   配置
-   蓝图
-   扩展

#### 应用对象

```py
from flask import Flask
app = Flask(__name__)

__name__ >> 在哪里找资源,模板文件静态资源在哪儿找
```

#### 路由

```py
@app.route('/')
def hello_world():
    return '<p>Hello, World!</p>'
```

#### 请求和响应处理

```python
# Flask将传入的HTTP请求和传出的响应封装在便捷的对象中
# 通过request和response对象访问
# 框架自动处理HTTP消息和Python对象之间的转换。

from flask import request

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username') # 从request中解析
    return f'Hello, {username}!' # 返回response
```

#### 模板

```py
from flask import render_template

@app.route('/hello/<name>')
def hello(name):
    return render_template('hello.html', name=name) # jinja2的模板语法
```

#### 上下文处理

Flask使用上下文对象使某些变量全局可访问，而无需显式传递：

-   **应用上下文**：提供对应用特定数据的访问
-   **请求上下文**：提供对请求特定数据的访问

```py
from flask import Flask, request, g, current_app

app = Flask(__name__)

@app.before_request
def before_request():
    # 在请求开始时设置一些全局变量
    g.user = request.args.get('user', 'Guest')
    print("Before request: g.user =", g.user)

@app.route('/')
def index():
    # 直接访问全局上下文对象 g 和 request
    return f"Hello, {g.user}! You are visiting {request.path}"

@app.teardown_request
def teardown_request(exception):
    # 请求结束时自动清理上下文
    print("Teardown: 清理上下文资源")

if __name__ == '__main__':
    app.run(debug=True)
```

