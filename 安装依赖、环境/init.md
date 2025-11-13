| 工具                   | 类型                  | 优点                                                 | 典型使用场景              |
| ---------------------- | --------------------- | ---------------------------------------------------- | ------------------------- |
| **conda**              | 包 + 环境管理器       | 管理系统级依赖（非纯 Python 也行），适合科学计算、AI | 数据科学、AI项目          |
| **pip + venv**         | Python 官方方案       | 轻量、原生                                           | Web / 通用项目            |
| **poetry**             | 现代项目管理工具      | 自动生成依赖锁定文件、打包方便                       | 应用、库开发              |
| **pipenv**             | pip + virtualenv 集成 | 自动虚拟环境、依赖锁定                               | 小型应用、学习            |
| **virtualenv**         | 环境隔离工具          | 创建独立 Python 环境                                 | 传统做法，轻量            |
| **pyenv**              | Python 版本管理       | 安装 / 切换多个 Python 版本                          | 系统层面控制              |
| **mamba / micromamba** | conda 的加速版        | 速度快很多                                           | 大项目 / CI 环境          |
| **uv / rye / hatch**   | 新一代管理器          | 超快 + 一体化（env + deps + build）                  | 前沿开发者 / 快速构建项目 |



| 对比点               | uv                          | pyenv                                   |
| -------------------- | --------------------------- | --------------------------------------- |
| 是否自带虚拟环境     | ✅ uv 会自动创建 `.venv/`    | ❌ 需要单独创建 venv 或 pyenv-virtualenv |
| 缓存目录             | `~/.local/share/uv/python/` | `~/.pyenv/versions/`                    |
| 多项目隔离           | ✅ 默认隔离依赖              | ⚠️ 依赖虚拟环境来隔离                    |
| 系统全局 Python 影响 | ❌ 几乎不影响                | ⚠️ 需要注意 PATH/shims                   |
| 安装和管理命令       | `uv python install`         | `pyenv install`                         |



# 1. 安装pyenv，管理py版本

* 如果有xcode，版本不兼容，需要先删除，否则会报错

```shell
sudo xcode-select --switch /Library/Developer/CommandLineTools
xcode-select -p
# /Library/Developer/CommandLineTools  输出这个是对的，然后就可以brew安装了
```

#### 安装pyenv

```shell
# 执行安装
brew install pyenv

#### 查看版本，确认是否安装成功
pyenv -v

#### 查看可安装的py版本
pyenv install -l
```

#### 安装python

```shell
#### 选择版本安装
pyenv install 3.12.2

#### 查看已安装的版本
ls -al ~/.pyenv/versions/
```

#### 设置 Python 版本

```shell
# 全局设置 （所有的项目都用这个版本）
pyenv global 3.12.2

# 项目本地版本（在项目目录下生效）
cd /xxx/
pyenv local 3.12.2
# 👉 会在目录下生成 .python-version 文件，进入这个目录就自动切换。

# 临时版本（仅在shell中生效）
pyenv shell 3.12.2
```

#### 查看python版本号

```shell
# 查看已安装的所有版本
pyenv versions

# 查看当前激活版本
pyenv version

# 查看python的实际地址
which python

# 确认版本号
python -version
```

#### 卸载版本
pyenv uninstall 3.10.13

#### 配置环境变量（保证全局生效）

```shell
# 在 ~/.zshrc 或 ~/.bashrc 加：
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv virtualenv-init -)"

source ~/.zshrc
```



# 📌 pyenv + 虚拟环境

```shell
# 安装插件
brew install pyenv-virtualenv

# 创建虚拟环境（基于 Python 3.12.2）
pyenv virtualenv 3.12.2 myproj-env

# 在项目里启用
pyenv local myproj-env
```



# pyenv virtualenv vs python -m venv

| 特性          | `python -m venv`            | `pyenv virtualenv`                |
| ----------- | --------------------------- | --------------------------------- |
| 依赖谁         | 使用系统/当前 Python 解释器          | 使用 **pyenv 管理的某个 Python 版本**      |
| 环境隔离        | ✅ 有独立 `.venv/`              | ✅ 有独立环境（存放在 `~/.pyenv/versions/`） |
| Python 版本管理 | ❌ 不能切换版本（只能用当前 Python）      | ✅ 可以绑定指定 Python 版本                |
| 多项目共享       | ❌ 每个项目必须建 `.venv/`          | ✅ 同一个虚拟环境可以跨项目复用                  |
| 激活方式        | `source .venv/bin/activate` | `pyenv local myproj-env`（自动切换）    |
| 配置文件        | 无                           | `.python-version`（记录环境名）          |
| 典型场景        | 小项目，轻量                      | 多版本并存，大型项目或团队开发                   |



# 2. 构建虚拟环境

#### 在当前目录下构建一个虚拟环境

```shell
python -m venv .venv
```

#### 1 激活

```bash
# macOS / Linux
source .venv/bin/activate

# Windows (cmd)
.venv\Scripts\activate

# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

#### 2 退出

`````
deactivate
`````

#### 3 安装依赖

```bash
pip install requests flask
```

---

#### 4 导出依赖

```bash
pip freeze > requirements.txt
```

示例文件：

```
flask==2.3.3
requests==2.31.0
```

---

#### 5 在新环境安装依赖

```bash
pip install -r requirements.txt
```

---

#### 6 Git 管理

在 `.gitignore` 里忽略 `.venv/`：

```
.venv/
```

👉 只提交 `requirements.txt`，保证依赖可复现。

---

#### 7  部署服务器（常见流程）

```bash
git clone https://xxx/myproject.git
cd myproject
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```
