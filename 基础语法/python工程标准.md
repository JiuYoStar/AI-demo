```shell
Project_Name/
├── README.md                # 项目说明文档
├── pyproject.toml           # 构建配置（依赖、版本、入口等）
├── requirements.txt         # 依赖列表（可选）
├── .env                     # 环境变量（开发用，不提交）
├── .gitignore
├── data/                    # 原始数据、静态数据
│   ├── raw/                 # 原始数据
│   └── processed/           # 预处理后的数据
├── logs/                    # 自动生成的日志文件（运行时写入）
│   └── app.log
├── configs/                 # 配置文件目录
│   ├── config.py            # Python 配置（路径、常量、环境）
│   ├── settings_dev.py      # 开发环境配置
│   ├── settings_prod.py     # 生产环境配置
│   └── logging.conf         # logging 的高级配置
├── scripts/                 # 命令行脚本、任务脚本
│   ├── precompute_data.py   # 数据预处理程序
│   └── export_excel.py      # 导出 excel 脚本举例
├── app            			 # 主程序代码（包）
│   ├── __init__.py          # 包初始化，可放 create_app()
│   ├── app.py               # 应用程序入口
│   ├── api/                 # 路由/API 层
│   │   ├── __init__.py
│   │   ├── bed_api.py       # 示例：病床使用率接口
│   │   └── health_api.py    # 示例：健康检查接口
│   ├── services/            # Service 层（业务逻辑）
│   │   ├── __init__.py
│   │   ├── data_loader.py   # 加载数据逻辑
│   │   └── bed_service.py   # 病床业务逻辑
│   ├── models/              # 数据模型（ORM / Pydantic / Schema）
│   │   ├── __init__.py
│   │   └── bed_model.py
│   ├── utils/               # 工具函数、通用代码
│   │   ├── __init__.py
│   │   ├── logging_util.py  # 日志初始化
│   │   ├── file_util.py     # 文件处理
│   │   └── common.py        # 通用方法
│   ├── cache/               # 缓存文件读取/写入模块
│   │   ├── __init__.py
│   │   ├── cache_manager.py
│   │   └── data_cache.pkl   # 缓存文件（运行时生成，也可以放到 data/）
│   ├── static/              # 静态文件（HTML/CSS/JS）
│   │   └── style.css
│   └── templates/           # HTML 模板（Flask 用）
│       └── index.html
└── tests/                   # 单元测试
    ├── __init__.py
    ├── test_api.py
    └── test_service.py

```

