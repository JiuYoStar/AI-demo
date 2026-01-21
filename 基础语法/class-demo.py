import abc

# 1. 抽象基类：定义接口契约
class Shape(abc.ABC):
    @abc.abstractmethod
    def area(self): ...

# 2. 现代元编程：使用 __init_subclass__ 替代简单元类
# 它可以拦截子类定义，比元类更轻量、易读
class BaseMeta:
    def __init_subclass__(cls, creator="System", **kwargs):
        super().__init_subclass__(**kwargs)
        cls.created_by = creator

# 3. 描述符：属性校验协议
class ValidatedName:
    def __set_name__(self, owner, name):
        self.storage_name = f"_{name}"

    def __get__(self, obj, objtype=None):
        return getattr(obj, self.storage_name) if obj else self

    def __set__(self, obj, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Name must be a non-empty string")
        setattr(obj, self.storage_name, value)

# 4. 多重继承与核心类定义
class Animal:
    def move(self): print("⚡ Moving fast...")

class Person(Animal, BaseMeta, creator="ModernMeta"):
    # 限制属性，优化内存性能
    __slots__ = ("_name", "_age", "__secret", "__dict__")

    name = ValidatedName()

    def __init__(self, name: str, age: int):
        self.name = name       # 触发描述符 __set__
        self._age = age        # 保护成员约定
        self.__secret = "TOP"  # 名称修饰 (Name Mangling)

    # --- 常用装饰器 ---
    @property
    def age(self): return self._age

    @classmethod
    def info(cls): return f"Class: {cls.__name__}, Created by: {cls.created_by}"

    @staticmethod
    def species(): return "Homo Sapiens"

    # --- 魔法方法 (Protocols) ---
    def __repr__(self): return f"Person(name={self.name!r})"
    def __call__(self): print(f"🚀 {self.name} is being called!")
    def __len__(self): return len(self.name)
    def __getitem__(self, i): return self.name[i]
    def __iter__(self): yield from self.name
    def __eq__(self, other):
        return isinstance(other, Person) and self.name == other.name

# --- 动态操作与自省 ---
if __name__ == "__main__":
    p = Person("Ada", 25)

    # 属性操作
    setattr(p, "tag", "AI")         # 动态增 (依赖 __dict__ 在 slots 中)
    val = getattr(p, "tag", None)   # 动态取
    exists = hasattr(p, "tag")      # 检查

    # 协议触发
    p()                             # __call__
    print(f"Index 0: {p[0]}")       # __getitem__
    print(f"Info: {Person.info()}") # @classmethod

    # 自省
    print(f"MRO: {Person.mro()}")   # 继承链
    print(f"Vars: {vars(p)}")       # 实例状态
