import itertools
from pathlib import Path

def get_log_lines(log_dir: str):
    """工序 1: 扫描目录并逐行读取 (惰性)"""
    paths = Path(log_dir).glob("*.log") # 拿到了一个文件路径的生成器
    print(f'paths: {paths}') # 输出paths对象<迭代器>
    # 返回的chain对象, 并没有打开文件, 是一个itertools.chain对象
    return itertools.chain.from_iterable(open(p) for p in paths)

def clean_pipeline(log_dir: str):
    raw_stream = get_log_lines(log_dir) # 创建raw_stream, 输出 chain object, 非日志内容
    stripped_stream = itertools.islice(raw_stream, 10, None)
    error_stream = filter(lambda line: "ERROR" in line, stripped_stream)
    code_stream = map(lambda line: line.split('[')[1].split(']')[0], error_stream)
    final_stream = itertools.islice(code_stream, 1000)
    # 创建的每一个对象, 都是一个迭代器, 是上一个对象的"包装", 并没有真正执行
    print(f'final_stream: {final_stream}') # >>> 输出 islice object
    return final_stream # 到此为止,声明的阶段, 没有执行一行数据, 内存占用极低
    # ↑ 以上都是铺设管道的过程

# 启动管道
if __name__ == "__main__":
    # 直到这一步，内存中依然没有加载任何日志内容
    print(f'catch-log >>>> start')
    for error_code in clean_pipeline("./logs"): # 这里开始索取数据, 触发执行 "拧开水龙头"
        print(f"处理错误码: {error_code}")
    print('----------------')
    py_counter = clean_pipeline("./logs")
    print(f"py_counter: {next(py_counter, 'EOF')}")
    print(f"py_counter: {next(py_counter, 'EOF')}")
    print(f"py_counter: {next(py_counter, 'EOF')}")
    print(f"py_counter: {next(py_counter, 'EOF')}")
    print(f"py_counter: {next(py_counter, 'EOF')}")
    print(f"py_counter: {next(py_counter, 'EOF')}")
    print(f"py_counter: {next(py_counter, 'EOF')}")
    print(f'catch-log >>>> end')



'''
铺设管道的过程:
  1. Path(log_dir).glob("*.log") -> 拿到一个文件路径的生成器
  2. open(p) for p in paths -> 拿到一个文件句柄的生成器
  3. itertools.chain.from_iterable(...) -> 拿到一个chain对象
  4. itertools.islice(raw_stream, 10, None) -> 拿到一个islice对象
  5. filter(lambda line: "ERROR" in line, stripped_stream) -> 拿到一个filter对象
  6. map(lambda line: line.split('[')[1].split(']')[0], error_stream) -> 拿到一个map对象
  7. itertools.islice(code_stream, 1000) -> 拿到一个islice对象(final_stream)

数据获取流程:
  1. for error_code in clean_pipeline("./logs"): 开始索要数据, 触发执行
  2. for循环, 向 final_stream 索要一个值
  3. final_stream 向上游 islice 索要一个值
  4. islice 向 map 索要一个值
  5. map 向 filter 索要一个值
  6. filter 向上游 islice 索要一个值
  7. islice 向 chain 索要一个值
  8. chain 向 open 索要一个值
  9. open 读取文件, 返回一行数据
  ------------------------------------
  10. chain 返回一行数据
  11. islice 返回一行数据
  12. filter 判断是否包含 "ERROR"
  13. 如果包含, 返回该行数据
  14. map 处理该行数据, 返回错误码
  15. islice 返回错误码
  16. for 循环打印错误码
  ------------------------------------
  17. for 循环向 final_stream 索要下一个值
  18. ...重复以上过程
'''
