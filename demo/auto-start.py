def auto_start(func):
    """自动启动生成器的装饰器"""
    def wrapper(*args, **kwargs):
        gen = func(*args, **kwargs)
        next(gen)  # 自动执行第一次 next()
        return gen
    return wrapper


@auto_start
def simple_monitor_forever():
    print("📢 监控已自动激活！")
    while True:
        val = yield "等待数据..."
        print(f"📥 收到数据: {val}")
    print("监控结束")

@auto_start
def simple_monitor_once():
    print("📢 监控已自动激活！")
    val = yield "等待数据..."
    print(f"📥 收到数据: {val}")
    print("监控结束")

# 现在我们可以直接 send 了，不需要手动 next()
m = simple_monitor_forever() # 在声明的时候, 已经触发了一次next()
m.send("Hello!")
m.send("World!")


