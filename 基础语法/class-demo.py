import abc

# 28. 抽象基类
class Shape(abc.ABC):
    @abc.abstractmethod
    def area(self): pass

# 30. 元类 (定制类创建过程)
class Meta(type):
    def __new__(cls, name, bases, attrs):
        attrs["created_by"] = "Meta"
        return super().__new__(cls, name, bases, attrs)

# 29. 属性描述符 (拦截属性操作)
class ValidatedName:
    def __set_name__(self, owner, name): self.internal_name = "_" + name
    def __get__(self, obj, objtype=None): return getattr(obj, self.internal_name)
    def __set__(self, obj, value):
        if not value: raise ValueError("Name cannot be empty")
        setattr(obj, self.internal_name, value)

# 1. 类定义 & 27. 多重继承
class Animal:
    def move(self): print("Moving...")

class Person(Animal, metaclass=Meta):
    name = ValidatedName() # 使用描述符

    # 2. 构造函数
    def __init__(self, name, age):
        # 3. 实例属性
        self.name = name
        self._age = age # 18. 私有属性约定
        self.__secret = "shh!" # 18. 伪私有

    # 4. 实例方法 & 14. 调用父类
    def greet(self):
        super().move()
        return f"Hi, I'm {self.name}"

    # 12. 字符串表示
    def __repr__(self): return f"Person({self.name})"

    # 15. 静态方法
    @staticmethod
    def species(): return "Human"

    # 16. 类方法
    @classmethod
    def info(cls): return f"This is a {cls.__name__}"

    # 17. 属性装饰器
    @property
    def age(self): return self._age

    # 19-24. 魔法方法 (重载)
    def __len__(self): return len(self.name) # 19. 长度
    def __getitem__(self, i): return self.name[i] # 20. 索引
    def __call__(self): print("Called!") # 21. 实例调用
    def __eq__(self, other): return self.name == other.name # 22. 比较
    def __add__(self, other): return self.name + other.name # 23. 运算
    def __iter__(self): return iter(self.name) # 24. 迭代

# --- 动态操作 (6-11, 25-26) ---
p = Person("Ada", 25)
setattr(p, "job", "Dev")    # 6. 动态增
getattr(p, "job")           # 7. 获取
hasattr(p, "job")           # 8. 检查
delattr(p, "job")           # 9. 删除
isinstance(p, Person)       # 10. 类型检查
print(type(p))              # 11. 获取类型
print(dir(p))               # 25. 列出属性
print(vars(p))              # 26. 属性字典 (__dict__)
