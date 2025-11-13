# Python types 模块 - 动态类型创建和内置类型名称

## 一、动态类型创建函数

| 函数名 | 功能说明 | 参数 | 返回值 | 示例代码 |
|--------|----------|------|--------|----------|
| `new_class()` | 动态创建类对象 | name, bases=(), kwds=None, exec_body=None | 新类对象 | 见下方代码1 |
| `prepare_class()` | 计算元类并创建类命名空间 | name, bases=(), kwds=None | (metaclass, namespace, kwds) | 见下方代码2 |
| `resolve_bases()` | 动态解析MRO条目 | bases | 解析后的基类元组 | 见下方代码3 |

### 代码示例 1: new_class() 动态创建类

```python
from types import new_class

# 方式1: 简单创建类
MyClass = new_class('MyClass')  # 等价于: class MyClass: pass

# 方式2: 指定基类
MyClass = new_class('MyClass', (dict,))  # 等价于: class MyClass(dict): pass

# 方式3: 使用 exec_body 填充类内容
def init_class_namespace(ns):
    ns['x'] = 10
    ns['greet'] = lambda self: f"Hello, {self.name}"

MyClass = new_class('MyClass', exec_body=init_class_namespace)
# 等价于:
# class MyClass:
#     x = 10
#     greet = lambda self: f"Hello, {self.name}"

# 方式4: 指定元类
def init_meta_class(ns):
    ns['version'] = '1.0'

MyClass = new_class('MyClass', kwds={'metaclass': type}, exec_body=init_meta_class)
```

### 代码示例 2: prepare_class() 准备类命名空间

```python
from types import prepare_class

# 准备类的元类和命名空间
name = 'MyClass'
bases = (dict,)
kwds = {'metaclass': type}

metaclass, namespace, kwds = prepare_class(name, bases, kwds)
# metaclass: 计算得到的元类
# namespace: 预备好的类命名空间(字典)
# kwds: 更新后的关键字参数

# 然后可以手动填充命名空间
namespace['x'] = 100
namespace['greet'] = lambda self: "Hello"

# 最后创建类
MyClass = metaclass(name, bases, namespace, **kwds)
```

### 代码示例 3: resolve_bases() 解析基类

```python
from types import resolve_bases

# 假设有一个特殊基类
class SpecialBase:
    def __mro_entries__(self, bases):
        # 返回真正的基类
        return (dict,)

# 解析基类
original_bases = (SpecialBase(),)
resolved_bases = resolve_bases(original_bases)
# resolved_bases 将是 (dict,)
```

---

## 二、标准解释器类型

| 类型名称 | 说明 | 用途示例 | 示例代码 |
|---------|------|----------|----------|
| `FunctionType` / `LambdaType` | 用户自定义函数和lambda函数的类型 | 类型检查 | 见代码4 |
| `GeneratorType` | 生成器迭代器对象的类型 | 判断是否为生成器 | 见代码5 |
| `CoroutineType` | 协程对象的类型(async def) | 判断是否为协程 | 见代码6 |
| `AsyncGeneratorType` | 异步生成器迭代器的类型 | 判断是否为异步生成器 | 见代码7 |
| `CodeType` | 代码对象的类型 | 代码对象操作 | 见代码8 |
| `CellType` | 单元对象(闭包变量容器) | 闭包变量管理 | 见代码9 |
| `MethodType` | 实例方法的类型 | 方法类型检查 | 见代码10 |
| `BuiltinFunctionType` / `BuiltinMethodType` | 内置函数和方法的类型 | 类型检查 | 见代码11 |
| `ModuleType` | 模块的类型 | 动态创建模块 | 见代码12 |
| `TracebackType` | 回溯对象的类型 | 异常处理 | 见代码13 |
| `FrameType` | 帧对象的类型 | 调试、性能分析 | 见代码14 |
| `GetSetDescriptorType` | C扩展中定义的属性描述器 | 类型检查 | 见代码15 |
| `MemberDescriptorType` | C扩展中定义的成员描述器 | 类型检查 | 见代码16 |

### 代码示例 4: FunctionType / LambdaType

```python
from types import FunctionType, LambdaType

def my_func():
    pass

my_lambda = lambda x: x * 2

print(isinstance(my_func, FunctionType))     # True
print(isinstance(my_lambda, LambdaType))     # True
print(FunctionType is LambdaType)            # True (它们是同一个类型)

# 实际应用: 动态创建函数
def create_adder(n):
    code = compile(f'lambda x: x + {n}', '<string>', 'eval')
    return FunctionType(code.co_consts[0], {})

add_5 = create_adder(5)
```

### 代码示例 5: GeneratorType

```python
from types import GeneratorType

def my_generator():
    yield 1
    yield 2

gen = my_generator()
print(isinstance(gen, GeneratorType))  # True

# 实际应用: 判断是否为生成器
def process_data(data):
    if isinstance(data, GeneratorType):
        return list(data)  # 将生成器转为列表
    return data
```

### 代码示例 6: CoroutineType

```python
from types import CoroutineType
import asyncio

async def my_coroutine():
    await asyncio.sleep(1)
    return "done"

coro = my_coroutine()
print(isinstance(coro, CoroutineType))  # True

# 记得关闭协程避免警告
coro.close()
```

### 代码示例 7: AsyncGeneratorType

```python
from types import AsyncGeneratorType

async def my_async_generator():
    for i in range(3):
        yield i

async_gen = my_async_generator()
print(isinstance(async_gen, AsyncGeneratorType))  # True
await async_gen.aclose()  # 关闭异步生成器
```

### 代码示例 8: CodeType

```python
from types import CodeType

def example():
    x = 10
    return x * 2

code = example.__code__
print(isinstance(code, CodeType))  # True
print(code.co_name)                # 'example'
print(code.co_varnames)            # ('x',)

# 使用 replace() 修改代码对象 (Python 3.8+)
new_code = code.replace(co_name='new_example')
print(new_code.co_name)            # 'new_example'
```

### 代码示例 9: CellType

```python
from types import CellType

def outer():
    x = 10  # 这是一个自由变量
    def inner():
        return x
    return inner

func = outer()
print(func.__closure__)                      # (<cell at 0x...: int object at 0x...>,)
print(isinstance(func.__closure__[0], CellType))  # True
print(func.__closure__[0].cell_contents)     # 10
```

### 代码示例 10: MethodType

```python
from types import MethodType

class MyClass:
    def my_method(self):
        pass

obj = MyClass()
print(isinstance(obj.my_method, MethodType))  # True

# 动态绑定方法
def new_method(self):
    return "dynamically added"

obj.new_method = MethodType(new_method, obj)
print(obj.new_method())  # "dynamically added"
```

### 代码示例 11: BuiltinFunctionType

```python
from types import BuiltinFunctionType, BuiltinMethodType

print(isinstance(len, BuiltinFunctionType))          # True
print(isinstance([].append, BuiltinMethodType))      # True
print(BuiltinFunctionType is BuiltinMethodType)      # True
```

### 代码示例 12: ModuleType

```python
from types import ModuleType

# 动态创建模块
my_module = ModuleType('my_module', 'This is my module')
my_module.x = 100
my_module.greet = lambda: "Hello"

print(my_module.__name__)    # 'my_module'
print(my_module.__doc__)     # 'This is my module'
print(my_module.x)           # 100
print(my_module.greet())     # 'Hello'

# 更推荐的方式
import importlib.util
spec = importlib.util.spec_from_loader('my_module', loader=None)
my_module = importlib.util.module_from_spec(spec)
```

### 代码示例 13: TracebackType

```python
from types import TracebackType
import sys

try:
    1 / 0
except:
    tb = sys.exc_info()[2]
    print(isinstance(tb, TracebackType))  # True
    print(tb.tb_lineno)                   # 错误发生的行号
    print(tb.tb_frame.f_code.co_name)     # 函数名
```

### 代码示例 14: FrameType

```python
from types import FrameType
import sys

def my_function():
    frame = sys._getframe()
    print(isinstance(frame, FrameType))  # True
    print(frame.f_code.co_name)          # 'my_function'
    print(frame.f_locals)                # 局部变量字典

my_function()
```

### 代码示例 15-16: Descriptor Types

```python
from types import GetSetDescriptorType, MemberDescriptorType
import datetime

# GetSetDescriptorType 示例
frame_locals = type(sys._getframe().f_locals)
print(isinstance(type(sys._getframe()).f_locals, GetSetDescriptorType))  # True

# MemberDescriptorType 示例
print(isinstance(datetime.timedelta.days, MemberDescriptorType))  # True
```

---

## 三、附加工具类和函数

| 类型/函数 | 功能说明 | 主要用途 | 示例代码 |
|----------|----------|----------|----------|
| `SimpleNamespace` | 简单的命名空间对象 | 替代空类,存储属性 | 见代码17 |
| `MappingProxyType` | 只读映射代理 | 创建字典的只读视图 | 见代码18 |
| `DynamicClassAttribute` | 动态类属性 | 实例和类访问不同行为 | 见代码19 |

### 代码示例 17: SimpleNamespace

```python
from types import SimpleNamespace

# 创建简单命名空间
person = SimpleNamespace(name='Alice', age=30, city='Beijing')

print(person.name)      # 'Alice'
print(person.age)       # 30

# 可以动态添加/修改属性
person.email = 'alice@example.com'
person.age = 31

print(person)  # SimpleNamespace(name='Alice', age=31, city='Beijing', email='alice@example.com')

# 替代方案对比:
# 旧方式: class NS: pass
#        obj = NS()
#        obj.name = 'Alice'
# 新方式: obj = SimpleNamespace(name='Alice')

# 实际应用: 配置对象
config = SimpleNamespace(
    debug=True,
    host='localhost',
    port=8000
)
```

### 代码示例 18: MappingProxyType

```python
from types import MappingProxyType

# 创建只读字典
original = {'a': 1, 'b': 2}
readonly = MappingProxyType(original)

print(readonly['a'])    # 1
print('b' in readonly)  # True

# 不能修改
# readonly['c'] = 3     # TypeError: 'mappingproxy' object does not support item assignment

# 但会反映原字典的变化
original['c'] = 3
print(readonly['c'])    # 3

# 实际应用: 保护类属性
class MyClass:
    _data = {'secret': 'value'}

    @property
    def data(self):
        return MappingProxyType(self._data)

obj = MyClass()
# obj.data['secret'] = 'new'  # TypeError: 不能修改
```

### 代码示例 19: DynamicClassAttribute

```python
from types import DynamicClassAttribute

class MyClass:
    def __init__(self, value):
        self._value = value

    @DynamicClassAttribute
    def special(self):
        """实例访问时返回实例的值"""
        return f"Instance value: {self._value}"

    def __getattr__(self, name):
        """类访问时触发"""
        if name == 'special':
            return "Class level access"
        raise AttributeError(name)

# 实例访问
obj = MyClass(42)
print(obj.special)        # "Instance value: 42"

# 类访问
# print(MyClass.special)  # "Class level access"

# 实际应用场景: enum.Enum
# 在枚举中,实例访问返回枚举值,类访问返回枚举成员
```

---

## 四、协程工具函数

| 函数名 | 功能说明 | 参数 | 返回值 | 示例代码 |
|--------|----------|------|--------|----------|
| `coroutine()` | 将生成器函数转换为协程函数 | gen_func | 协程函数 | 见代码20 |

### 代码示例 20: coroutine()

```python
from types import coroutine
import asyncio

# 将生成器装饰为协程
@coroutine
def my_coroutine():
    yield from asyncio.sleep(1)
    return "done"

# 现在可以像协程一样使用
async def main():
    result = await my_coroutine()
    print(result)  # "done"

# asyncio.run(main())

# 对比现代写法:
# async def my_coroutine():
#     await asyncio.sleep(1)
#     return "done"
```

---

## 五、常用场景总结

### 场景1: 类型检查

```python
from types import FunctionType, GeneratorType, CoroutineType

def check_callable_type(obj):
    if isinstance(obj, FunctionType):
        return "普通函数"
    elif isinstance(obj, GeneratorType):
        return "生成器"
    elif isinstance(obj, CoroutineType):
        return "协程"
    else:
        return "其他类型"
```

### 场景2: 动态创建类

```python
from types import new_class

# 插件系统中动态创建类
def create_plugin_class(name, methods):
    def init_namespace(ns):
        for method_name, method_func in methods.items():
            ns[method_name] = method_func

    return new_class(name, bases=(object,), exec_body=init_namespace)

# 使用
plugin_methods = {
    'run': lambda self: print("Plugin running"),
    'stop': lambda self: print("Plugin stopped")
}
PluginClass = create_plugin_class('MyPlugin', plugin_methods)
```

### 场景3: 配置管理

```python
from types import SimpleNamespace, MappingProxyType

# 应用配置
config = SimpleNamespace(
    database=SimpleNamespace(
        host='localhost',
        port=5432,
        name='mydb'
    ),
    api=SimpleNamespace(
        url='https://api.example.com',
        timeout=30
    )
)

# 只读配置
readonly_config = MappingProxyType({
    'version': '1.0',
    'app_name': 'MyApp'
})
```

### 场景4: 模块热重载

```python
from types import ModuleType
import sys

def create_dynamic_module(name, code_str):
    """动态创建并执行模块"""
    module = ModuleType(name)
    exec(code_str, module.__dict__)
    sys.modules[name] = module
    return module

# 使用
code = """
def greet(name):
    return f'Hello, {name}!'

VERSION = '1.0'
"""
my_module = create_dynamic_module('dynamic_module', code)
print(my_module.greet('World'))  # Hello, World!
```

---

## 六、快速参考表

| 需求 | 使用的类型/函数 |
|------|----------------|
| 动态创建类 | `new_class()` |
| 判断是否为函数 | `isinstance(obj, FunctionType)` |
| 判断是否为生成器 | `isinstance(obj, GeneratorType)` |
| 判断是否为协程 | `isinstance(obj, CoroutineType)` |
| 创建简单的数据容器 | `SimpleNamespace()` |
| 创建只读字典 | `MappingProxyType()` |
| 动态创建模块 | `ModuleType()` |
| 获取函数的代码对象 | `func.__code__` (CodeType) |
| 获取异常的回溯信息 | `sys.exc_info()[2]` (TracebackType) |
| 将生成器转为协程 | `@coroutine` 装饰器 |

---

## 参考文档

- [Python 官方文档 - types 模块](https://docs.python.org/zh-cn/3.9/library/types.html)
- PEP 3115 - Python 3000 中的元类
- PEP 560 - 对 typing 模块和泛型类型的核心支持
