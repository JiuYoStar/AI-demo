// 28. 抽象基类 (JS 无原生 ABC，需手动抛错)
class Shape {
  constructor() {
    if (this.constructor === Shape) throw new Error("Abstract class");
  }
  area() {
    throw new Error("Method must be implemented");
  }
}

// 29. 属性描述符/拦截 (JS 通常使用 Proxy 或 defineProperty)
// 30. 元类 (JS 无元类，通常使用 Class Decorators 或 Proxy 代理构造函数)

// 1. 类定义 & 13. 继承 (JS 不支持 27. 多重继承)
class Animal {
  move() {
    console.log("Moving...");
  }
}

class Person extends Animal {
  // 18. 私有属性 (真私有)
  #secret = "shh!";

  // 2. 构造函数
  constructor(name, age) {
    super(); // 14. 必须先调用 super()
    // 3. 实例属性
    this.name = name;
    this._age = age; // 18. 约定私有
  }

  // 4. 实例方法
  greet() {
    super.move();
    return `Hi, I'm ${this.name}`;
  }

  // 12. 字符串表示
  toString() {
    return `Person(${this.name})`;
  }

  // 15. 静态方法 & 16. 类方法 (JS 中 static 即类方法)
  static species() {
    return "Human";
  }
  static info() {
    return `This is a ${this.name}`;
  }

  // 17. 属性装饰器 (Getter/Setter)
  get age() {
    return this._age;
  }
  set age(v) {
    this._age = v;
  }

  // 24. 迭代器 (唯一对应的魔法方法)
  *[Symbol.iterator]() {
    for (let char of this.name) yield char;
  }

  // 19-23. JS 不支持运算符重载 (__len__, __add__, __eq__ 等无对应)
  // 21. 实例调用：JS 实例不可作为函数调用，除非实例本身是 Function
}

// --- 动态操作 (6-11, 25-26) ---
const p = new Person("Ada", 25); // 5. new 关键字
p.job = "Dev"; // 6. 动态增
const job = p.job; // 7. 获取
const hasJob = "job" in p; // 8. 检查
delete p.job; // 9. 删除
console.log(p instanceof Person); // 10. 类型检查
console.log(typeof p); // 11. 获取类型 (返回 'object')
console.log(Object.keys(p)); // 25. 列出属性
console.log(Object.entries(p)); // 26. 属性字典对应项
