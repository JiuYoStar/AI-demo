# run.py - Flask应用的启动入口
# 从app包中导入Flask应用实例
from app import app

# 添加标记,验证run.py是否被执行
print("🔥 run.py 文件被执行了!")

if __name__ == '__main__':
    # 以调试模式运行Flask应用
    # debug=True 会启用自动重载和详细的错误信息
    print("🚀 通过 python run.py 启动")
    app.run(debug=True)

