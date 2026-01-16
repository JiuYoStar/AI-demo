import os
from pathlib import Path

# 🧱 工序 1: 水源 (读取文件行)
def get_log_lines_yield(log_dir: str):
    paths = Path(log_dir).glob("*.log")
    for p in paths:
        with open(p, 'r', encoding='utf-8') as f:
            # yield from 会把文件 f 里的每一行依次“吐”出去
            yield from f

# ✂️ 工序 2: 节流 (跳过前 10 行)
def skip_header(stream, n=10):
    for i, item in enumerate(stream):
        if i >= n:
            yield item

# 🔍 工序 3: 滤芯 (只留 ERROR)
def filter_errors(stream):
    for line in stream:
        if "ERROR" in line:
            yield line

# 🧪 工序 4: 加工 (提取错误码)
def extract_code(stream):
    for line in stream:
        # 假设格式: "ERROR: [Code404] ..."
        code = line.split('[')[1].split(']')[0]
        yield code

# 🏁 工序 5: 限量 (只取前 1000 个)
def limit_results(stream, count=1000):
    for i, item in enumerate(stream):
        if i < count:
            yield item
        else:
            break  # 达到数量，直接停止下游的需求

# 🏗️ 组装流水线
def manual_pipeline(log_dir):
    s1 = get_log_lines_yield(log_dir)  # 获取原始流
    s2 = skip_header(s1)               # 加上跳过头部的逻辑
    s3 = filter_errors(s2)             # 加上过滤逻辑
    s4 = extract_code(s3)              # 加上解析逻辑
    s5 = limit_results(s4)             # 加上限额逻辑
    return s5

# 🚰 运行：拧开水龙头
if __name__ == "__main__":
    print("Manual Pipeline >>>> Start")
    # 只有在这里循环时，上面的 yield 才会一个接一个地被触发
    for error_code in manual_pipeline("./logs"):
        print(f"处理错误码: {error_code}")
    print("Manual Pipeline >>>> End")
