# Python vs JavaScript 类对比表格

## 类（Class）完整对比

| 功能分类 | Python 伪代码 | JavaScript 伪代码 | 说明 |
|---------|--------------|------------------|------|
| **1. 基本类定义** | `class Person:` | `class Person {}` | Python用冒号，JS用花括号 |
| **2. 构造函数** | `def __init__(self, name):` | `constructor(name) {}` | Python用魔法方法，JS用关键字 |
| **3. 实例属性** | `self.name = name` | `this.name = name` | 都使用this/self引用 |
| **4. 实例方法** | `def greet(self):` | `greet() {}` | Python需要显式self参数 |
| **5. 创建实例** | `p = Person("Ada")` | `p = new Person("Ada")` | JS需要new关键字 |
| **6. 动态添加属性** | `setattr(obj, "key", value)` | `obj.key = value` | Python用函数，JS直接赋值 |
| **7. 获取属性** | `getattr(obj, "key")` | `obj.key` 或 `obj["key"]` | Python用函数，JS直接访问 |
| **8. 检查属性存在** | `hasattr(obj, "key")` | `"key" in obj` | Python用函数，JS用in操作符 |
| **9. 删除属性** | `delattr(obj, "key")` | `delete obj.key` | Python用函数，JS用delete |
| **10. 类型检查** | `isinstance(obj, Class)` | `obj instanceof Class` | 判断实例类型 |
| **11. 获取类型** | `type(obj)` | `obj.constructor` 或 `typeof obj` | type返回类，typeof返回字符串 |
| **12. 字符串表示** | `def __repr__(self):` 或 `__str__` | `toString() {}` | Python有两种，JS只有toString |
| **13. 继承** | `class Dog(Animal):` | `class Dog extends Animal {}` | 单继承语法 |
| **14. 调用父类方法** | `super().__init__()` | `super.method()` | 访问父类 |
| **15. 静态方法** | `@staticmethod` <br> `def add():` | `static add() {}` | 类级别方法，不需实例 |
| **16. 类方法** | `@classmethod` <br> `def info(cls):` | `static info() {}` | Python有cls参数，JS无直接对应 |
| **17. 属性装饰器** | `@property` <br> `def name(self):` | `get name() {}` <br> `set name(v) {}` | Python用装饰器，JS用get/set |
| **18. 私有属性** | `self._private` (约定) | `#private` (真私有) | Python只是约定，JS真正私有 |
| **19. 魔法方法-长度** | `def __len__(self):` | 无，使用 `obj.length` 属性 | Python可重载len() |
| **20. 魔法方法-索引** | `def __getitem__(self, i):` | 无，使用 `obj[i]` 直接访问数组 | Python可重载[] |
| **21. 魔法方法-调用** | `def __call__(self):` | 无，只有函数可调用 | Python可让实例像函数调用 |
| **22. 魔法方法-比较** | `def __eq__(self, other):` | 无，需手动实现equals() | Python可重载== |
| **23. 魔法方法-运算** | `def __add__(self, other):` | 无，需手动实现add() | Python可重载+ |
| **24. 魔法方法-迭代** | `def __iter__(self):` | `[Symbol.iterator]() {}` | 两者都支持迭代器 |
| **25. 列举属性** | `dir(obj)` | `Object.keys(obj)` | 获取所有属性名 |
| **26. 获取属性字典** | `vars(obj)` 或 `obj.__dict__` | `Object.entries(obj)` | Python有内置属性字典 |
| **27. 多重继承** | `class C(A, B):` | 不支持，需混入（mixin）模式 | Python原生支持 |
| **28. 抽象基类** | `from abc import ABC` <br> `class A(ABC):` | 无，需手动实现 | Python有ABC模块 |
| **29. 属性描述符** | `def __get__(self, obj, type):` | 使用Proxy或defineProperty | Python描述符协议 |
| **30. 元类** | `class Meta(type):` <br> `class C(metaclass=Meta):` | 无，原型链机制不同 | Python可定制类创建 |

## 核心差异总结

| 特性 | Python | JavaScript | 备注 |
|-----|--------|-----------|------|
| **设计哲学** | 显式优于隐式 | 简洁灵活 | Python self显式，JS this隐式 |
| **魔法方法** | ✅ 丰富的魔法方法系统 | ❌ 不支持运算符重载 | Python可深度定制对象行为 |
| **私有性** | 约定式（_name） | 真私有（#name） | JS的#是语法级别的私有 |
| **多重继承** | ✅ 原生支持 | ❌ 只支持单继承 | Python用MRO解决菱形继承 |
| **类方法** | 有@classmethod和@staticmethod | 只有static | Python区分类方法和静态方法 |
| **属性访问** | 函数式（getattr/setattr） | 直接访问（obj.key） | Python更函数式，JS更直观 |
| **类型系统** | 鸭子类型 + 类型提示 | 鸭子类型 + TypeScript | 都支持动态类型 |
| **原型链** | 基于类（新式类） | 基于原型链 | 底层机制不同 |

## 常用伪代码模式对比

### 创建和使用类

```python
# Python 伪代码
class Person:
    def __init__(name): self.name = name
    def greet(): return f"Hi {self.name}"

p = Person("Ada")
p.greet()
// JavaScript 伪代码
class Person {
    constructor(name) { this.name = name }
    greet() { return `Hi ${this.name}` }
}

p = new Person("Ada")
p.greet()
```

### 继承和多态

```python
# Python 伪代码
class Animal:
    def speak(): pass

class Dog(Animal):
    def speak(): return "Woof"

class Cat(Animal):
    def speak(): return "Meow"

animals = [Dog(), Cat()]
for a in animals: a.speak()  # 多态
// JavaScript 伪代码
class Animal {
    speak() {}
}

class Dog extends Animal {
    speak() { return "Woof" }
}

class Cat extends Animal {
    speak() { return "Meow" }
}

animals = [new Dog(), new Cat()]
animals.forEach(a => a.speak())  // 多态
```

### 属性操作

```python
# Python 伪代码
obj = MyClass()
setattr(obj, "key", "value")  # 设置
getattr(obj, "key")           # 获取
hasattr(obj, "key")           # 检查
delattr(obj, "key")           # 删除
// JavaScript 伪代码
obj = new MyClass()
obj.key = "value"      // 设置
obj.key                // 获取
"key" in obj           // 检查
delete obj.key         // 删除
```

## 魔法方法详细对比

| Python 魔法方法 | 用途 | JavaScript 对应 |
|----------------|------|----------------|
| `__init__(self)` | 构造函数 | `constructor()` |
| `__str__(self)` | 字符串表示（用户友好） | `toString()` |
| `__repr__(self)` | 字符串表示（开发者） | `toString()` |
| `__len__(self)` | len()调用 | `.length`属性 |
| `__getitem__(self, key)` | obj[key]访问 | 直接用[]访问 |
| `__setitem__(self, key, val)` | obj[key]=val设置 | 直接用[]=设置 |
| `__delitem__(self, key)` | del obj[key] | `delete obj[key]` |
| `__iter__(self)` | 迭代器 | `[Symbol.iterator]()` |
| `__next__(self)` | 下一个元素 | `.next()` |
| `__call__(self)` | 实例可调用 | 无（只有函数可调用） |
| `__eq__(self, other)` | == 运算符 | `===` 或自定义equals() |
| `__lt__(self, other)` | < 运算符 | `<` 或自定义compare() |
| `__add__(self, other)` | + 运算符 | 无，需自定义add() |
| `__sub__(self, other)` | - 运算符 | 无，需自定义sub() |
| `__mul__(self, other)` | * 运算符 | 无，需自定义mul() |
| `__contains__(self, item)` | in 运算符 | `.includes()` |
| `__enter__(self)` | with语句进入 | 无（无上下文管理器） |
| `__exit__(self)` | with语句退出 | 无（无上下文管理器） |
| `__getattr__(self, name)` | 获取不存在的属性 | `Proxy` handler.get |
| `__setattr__(self, name, val)` | 设置属性 | `Proxy` handler.set |

## 总结

Python的类系统更加强大和灵活，特别是魔法方法提供了深度定制能力；JavaScript的类系统更简洁直观，但功能相对有限。选择哪个取决于具体需求和使用场景。
