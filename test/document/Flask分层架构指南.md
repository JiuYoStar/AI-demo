# 🧱 Flask 分层架构指南

> 当 Flask 项目代码越来越多、模块越来越复杂时，需要通过“分层架构”来优化结构，提高可维护性与扩展性。

---

## 📖 一、为什么要分层

当一个模块文件（例如 `user.py`）变得上千行时，容易出现以下问题：

- 文件太长，查找和阅读困难；
- 路由、逻辑、数据混杂在一起；
- 改一处影响全局；
- 单元测试和协作困难。

解决方式：将项目按功能职责拆分为多层结构。

---

## 🧩 二、分层思路（MVC 扩展）

Flask 虽然轻量，但仍可借鉴 MVC 思想：

| 层级                   | 职责                     | 示例文件      |
| ---------------------- | ------------------------ | ------------- |
| 路由层（Routes）       | 定义 URL 与 HTTP 入口    | `routes.py`   |
| 业务层（Services）     | 处理业务逻辑             | `services.py` |
| 数据层（Models / DAO） | 操作数据库、定义数据结构 | `models.py`   |
| 工具层（Utils）        | 通用工具函数、装饰器     | `utils/`      |

> 流程：  
> **HTTP 请求 → 路由层 → 业务层 → 数据层 → 返回响应**

---

## 🏗️ 三、推荐项目结构

```python
app/
├── **init**.py
│
├── extensions/               # 第三方库与扩展初始化
│   ├── **init**.py
│   ├── db.py
│   ├── cache.py
│   └── login_manager.py
│
├── blueprints/
│   ├── **init**.py
│   ├── user/
│   │   ├── **init**.py       # 创建 user 蓝图
│   │   ├── routes.py         # 路由层：处理 HTTP 请求
│   │   ├── services.py       # 业务层：登录注册逻辑
│   │   ├── models.py         # 数据层：ORM 模型
│   │   └── validators.py     # 参数校验
│   │
│   ├── admin/
│   │   ├── **init**.py
│   │   ├── routes.py
│   │   ├── services.py
│   │   └── models.py
│   │
│   └── order/
│       ├── **init**.py
│       ├── routes.py
│       ├── services.py
│       └── models.py
│
├── config/
│   ├── **init**.py
│   ├── dev.py
│   ├── prod.py
│   └── test.py
│
└── utils/
├── **init**.py
├── common.py
├── jwt_util.py
├── email_util.py
└── decorators.py
```



## 💡 四、模块示例：User 模块

### 1️⃣ `app/blueprints/user/__init__.py`

````python
from flask import Blueprint

bp_user = Blueprint('user', __name__)

from . import routes  # 注册路由, 从当前的包导入
````

---

### 2️⃣ `app/blueprints/user/routes.py`

```python
from flask import request, jsonify
from . import bp_user
from .services import register_user, login_user

@bp_user.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    result = register_user(data)
    return jsonify(result)

@bp_user.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    result = login_user(data)
    return jsonify(result)
```

---

### 3️⃣ `app/blueprints/user/services.py`

```python
from .models import User
from app.extensions.db import db

def register_user(data):
    user = User(username=data['username'])
    db.session.add(user)
    db.session.commit()
    return {"message": "user created"}

def login_user(data):
    user = User.query.filter_by(username=data['username']).first()
    if not user:
        return {"error": "user not found"}
    return {"message": "login success"}
```

---

### 4️⃣ `app/blueprints/user/models.py`

```python
from app.extensions.db import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
```

---

## ⚙️ 五、自动注册蓝图

当蓝图很多时，可自动扫描注册：

```python
# app/__init__.py
from flask import Flask
import pkgutil, importlib

def create_app():
    app = Flask(__name__)

    package = 'app.blueprints'
    for _, name, _ in pkgutil.iter_modules([package.replace('.', '/')]):
        module = importlib.import_module(f"{package}.{name}")
        if hasattr(module, 'bp'):
            app.register_blueprint(module.bp)
    return app
```

---

## 🧠 六、进一步优化方向

| 模块       | 说明                                   |
| ---------- | -------------------------------------- |
| `schemas/` | 使用 Pydantic / Marshmallow 做数据验证 |
| `dao/`     | 数据访问层，封装复杂查询               |
| `tasks/`   | 异步任务模块（Celery、RQ）             |
| `tests/`   | 单元测试目录                           |

---

## ✅ 七、总结

> 当项目代码量变大时，不应堆代码，而应拆分层次。
>
> * **Routes**：HTTP 请求入口
> * **Services**：业务逻辑聚合
> * **Models/DAO**：数据存取
> * **Utils**：通用工具
>
> Flask 的灵活性使你能自由组合这些模块，
> 从轻量脚本平滑扩展到大型工程架构。



