# 📘 pyenv 使用资料

## 1. 什么是 pyenv？
- **pyenv** 是一个 Python 版本管理工具，可以在同一台机器上安装和切换多个 Python 版本。
- 解决的问题：
  - 系统自带 Python 版本过旧/被占用。
  - 不同项目需要不同的 Python 版本。
  - 避免库冲突，每个版本配合独立的 `pip`。

> 简单理解：`pyenv` = Python 版本切换器。

---

## 2. 安装方法

### macOS
1. 安装 Homebrew（如果未安装）：
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
2. 安装 pyenv：
   ```bash
   brew update
   brew install pyenv
   ```
3. 配置环境变量（推荐写到 `~/.zshrc` 或 `~/.bashrc`）：
   ```bash
   export PYENV_ROOT="$HOME/.pyenv"
   export PATH="$PYENV_ROOT/bin:$PATH"
   eval "$(pyenv init --path)"
   eval "$(pyenv init -)"
   ```
4. 重新加载配置：
   ```bash
   source ~/.zshrc
   ```

---

### Linux (Ubuntu/Debian)
1. 安装依赖：
   ```bash
   sudo apt update
   sudo apt install -y build-essential curl git      libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev      wget llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev      libffi-dev liblzma-dev python3-openssl
   ```
2. 安装 pyenv：
   ```bash
   curl https://pyenv.run | bash
   ```
3. 配置环境变量（写入 `~/.bashrc` 或 `~/.zshrc`）：
   ```bash
   export PYENV_ROOT="$HOME/.pyenv"
   export PATH="$PYENV_ROOT/bin:$PATH"
   eval "$(pyenv init --path)"
   eval "$(pyenv init -)"
   ```
4. 重新加载配置：
   ```bash
   source ~/.bashrc
   ```

---

### Windows
在 Windows 上不直接用 pyenv，而是用 **pyenv-win**（移植版）。

1. 通过 PowerShell 安装（推荐）：
   ```powershell
   Invoke-WebRequest -UseBasicParsing -Uri "https://pyenv-win.github.io/pyenv-win/install-pyenv-win.ps1" -OutFile "./install-pyenv-win.ps1"
   &"./install-pyenv-win.ps1"
   ```
2. 配置环境变量（系统自动添加，一般不需要手动改）。
3. 之后就可以用 `pyenv` 指令。

---

## 3. 常用指令

### 查看版本
```bash
pyenv versions        # 查看已安装的 Python 版本
pyenv version         # 查看当前使用的版本
pyenv install --list  # 查看所有可安装的版本
```

### 安装版本
```bash
pyenv install 3.12.6     # 安装 Python 3.12.6
pyenv install -v 3.10.14 # 带日志安装
```

### 切换版本
```bash
pyenv global 3.12.6   # 设置全局默认版本
pyenv local 3.10.14   # 设置当前目录使用的版本（生成 .python-version）
pyenv shell 3.11.9    # 仅当前 shell 会话生效
```

### 卸载版本
```bash
pyenv uninstall 3.9.18
```

### 其他
```bash
cd ~/.pyenv && git pull  # 更新 pyenv 本体
which python             # 查看当前 python 路径
python --version         # 确认当前版本
```

---

## 4. 使用小贴士
- 每个 pyenv 安装的 Python 自带独立的 `pip`。
- 不同项目推荐配合 **pyenv-virtualenv** 使用，进一步隔离环境。
- macOS 安装新版本失败时，可考虑使用国内镜像：
  ```bash
  export PYTHON_BUILD_MIRROR_URL="https://mirrors.tuna.tsinghua.edu.cn/python"
  ```
