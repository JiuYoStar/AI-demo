# Python 内置函数与 JavaScript 对比

## 数学运算函数

| Python函数 | 功能说明 | 示例 | JavaScript对应 |
|-----------|---------|------|---------------|
| `abs(x)` | 返回数的绝对值 | `abs(-5)` → 5 | `Math.abs(-5)` |
| `divmod(a, b)` | 返回商和余数的元组 | `divmod(7, 3)` → (2, 1) | `[Math.floor(7/3), 7%3]` |
| `pow(x, y[, z])` | 返回x的y次幂，如果z存在则对z取模 | `pow(2, 3)` → 8 | `Math.pow(2, 3)` 或 `2**3` |
| `round(x[, n])` | 四舍五入到n位小数 | `round(3.14159, 2)` → 3.14 | `Number(3.14159).toFixed(2)` 或 `Math.round()` |
| `sum(iterable[, start])` | 对可迭代对象求和 | `sum([1,2,3])` → 6 | `[1,2,3].reduce((a,b)=>a+b, 0)` |
| `max(iterable)` | 返回最大值 | `max([1,2,3])` → 3 | `Math.max(...[1,2,3])` |
| `min(iterable)` | 返回最小值 | `min([1,2,3])` → 1 | `Math.min(...[1,2,3])` |

## 类型转换函数

| Python函数 | 功能说明 | 示例 | JavaScript对应 |
|-----------|---------|------|---------------|
| `int(x[, base])` | 转换为整数 | `int("10", 2)` → 2 | `parseInt("10", 2)` |
| `float(x)` | 转换为浮点数 | `float("3.14")` → 3.14 | `parseFloat("3.14")` 或 `Number()` |
| `str(obj)` | 转换为字符串 | `str(123)` → "123" | `String(123)` 或 `123.toString()` |
| `bool(x)` | 转换为布尔值 | `bool(0)` → False | `Boolean(0)` 或 `!!0` |
| `list(iterable)` | 转换为列表 | `list("abc")` → ['a','b','c'] | `Array.from("abc")` 或 `[..."abc"]` |
| `tuple(iterable)` | 转换为元组（不可变） | `tuple([1,2])` → (1,2) | 无直接对应，可用 `Object.freeze([1,2])` |
| `set(iterable)` | 转换为集合（去重） | `set([1,1,2])` → {1,2} | `new Set([1,1,2])` |
| `dict(...)` | 创建字典 | `dict(a=1, b=2)` → {'a':1,'b':2} | `{a:1, b:2}` 或 `new Map()` |
| `frozenset(iterable)` | 创建不可变集合 | `frozenset([1,2])` | 无直接对应 |
| `bytes(source)` | 转换为字节对象 | `bytes([65,66])` → b'AB' | `new Uint8Array([65,66])` |
| `bytearray(source)` | 转换为可变字节数组 | `bytearray([65])` | `new Uint8Array([65])` |
| `complex(real[, imag])` | 创建复数 | `complex(1, 2)` → (1+2j) | 无内置支持，需要库 |
| `memoryview(obj)` | 创建内存视图对象 | `memoryview(b"abc")` | `ArrayBuffer` 视图 |

## 进制转换函数

| Python函数 | 功能说明 | 示例 | JavaScript对应 |
|-----------|---------|------|---------------|
| `bin(x)` | 转换为二进制字符串 | `bin(10)` → '0b1010' | `(10).toString(2)` |
| `oct(x)` | 转换为八进制字符串 | `oct(8)` → '0o10' | `(8).toString(8)` |
| `hex(x)` | 转换为十六进制字符串 | `hex(255)` → '0xff' | `(255).toString(16)` |
| `ord(c)` | 返回字符的Unicode码点 | `ord('A')` → 65 | `'A'.charCodeAt(0)` |
| `chr(i)` | 返回Unicode码点对应的字符 | `chr(65)` → 'A' | `String.fromCharCode(65)` |

## 序列操作函数

| Python函数 | 功能说明 | 示例 | JavaScript对应 |
|-----------|---------|------|---------------|
| `len(s)` | 返回对象长度 | `len([1,2,3])` → 3 | `[1,2,3].length` 或 `Object.keys(obj).length` |
| `range(stop)` | 创建数字序列 | `range(3)` → 0,1,2 | `[...Array(3).keys()]` 或自定义函数 |
| `enumerate(iterable)` | 返回索引和值的枚举对象 | `enumerate(['a','b'])` | `arr.entries()` 或 `arr.map((v,i)=>[i,v])` |
| `zip(*iterables)` | 将多个可迭代对象打包成元组 | `zip([1,2],['a','b'])` | 需自定义或使用lodash的`_.zip()` |
| `reversed(seq)` | 返回反转的迭代器 | `reversed([1,2,3])` | `[1,2,3].reverse()` |
| `sorted(iterable)` | 返回排序后的列表 | `sorted([3,1,2])` → [1,2,3] | `[3,1,2].sort()` 或 `[...arr].sort()` |
| `slice(start, stop[, step])` | 创建切片对象 | `slice(1,3)` | `arr.slice(1,3)` |
| `filter(function, iterable)` | 过滤序列 | `filter(lambda x: x>0, [-1,1,2])` | `[-1,1,2].filter(x => x>0)` |
| `map(function, iterable)` | 映射函数到序列 | `map(str, [1,2,3])` | `[1,2,3].map(String)` |

## 逻辑判断函数

| Python函数 | 功能说明 | 示例 | JavaScript对应 |
|-----------|---------|------|---------------|
| `all(iterable)` | 所有元素为真时返回True | `all([True, 1, 'x'])` → True | `arr.every(x => x)` |
| `any(iterable)` | 任一元素为真时返回True | `any([False, 0, 1])` → True | `arr.some(x => x)` |
| `callable(obj)` | 判断对象是否可调用 | `callable(print)` → True | `typeof obj === 'function'` |
| `isinstance(obj, class)` | 判断对象是否是类的实例 | `isinstance(5, int)` → True | `obj instanceof Class` 或 `typeof` |
| `issubclass(class, classinfo)` | 判断是否是子类 | `issubclass(bool, int)` → True | `Child.prototype instanceof Parent` |

## 对象属性操作

| Python函数 | 功能说明 | 示例 | JavaScript对应 |
|-----------|---------|------|---------------|
| `getattr(obj, name[, default])` | 获取对象属性 | `getattr(obj, 'x', 0)` | `obj.x` 或 `obj['x']` 或 `obj?.x` |
| `setattr(obj, name, value)` | 设置对象属性 | `setattr(obj, 'x', 10)` | `obj.x = 10` 或 `obj['x'] = 10` |
| `delattr(obj, name)` | 删除对象属性 | `delattr(obj, 'x')` | `delete obj.x` |
| `hasattr(obj, name)` | 判断对象是否有某属性 | `hasattr(obj, 'x')` | `'x' in obj` 或 `obj.hasOwnProperty('x')` |
| `dir([obj])` | 返回对象的属性和方法列表 | `dir(obj)` | `Object.keys(obj)` 或 `Object.getOwnPropertyNames()` |
| `vars([obj])` | 返回对象的__dict__属性 | `vars(obj)` | `Object.entries(obj)` 或直接访问对象 |
| `id(obj)` | 返回对象的唯一标识符 | `id(obj)` | 无直接对应，对象引用本身 |
| `hash(obj)` | 返回对象的哈希值 | `hash("abc")` | 无内置，需自定义哈希函数 |

## 作用域和命名空间

| Python函数 | 功能说明 | 示例 | JavaScript对应 |
|-----------|---------|------|---------------|
| `globals()` | 返回全局命名空间字典 | `globals()` | `window`（浏览器）或 `global`（Node.js） |
| `locals()` | 返回局部命名空间字典 | `locals()` | 无直接对应 |
| `vars([obj])` | 返回对象的属性字典 | `vars()` 等同于 `locals()` | `Object.entries(obj)` |

## 输入输出

| Python函数 | 功能说明 | 示例 | JavaScript对应 |
|-----------|---------|------|---------------|
| `print(*objects)` | 打印输出 | `print("Hello", "World")` | `console.log("Hello", "World")` |
| `input([prompt])` | 从标准输入读取 | `input("输入:")` | `prompt()`（浏览器）或需要`readline`模块（Node.js） |
| `open(file, mode)` | 打开文件 | `open('file.txt', 'r')` | `fs.readFile()` 或 `fs.open()`（Node.js） |

## 代码执行和编译

| Python函数 | 功能说明 | 示例 | JavaScript对应 |
|-----------|---------|------|---------------|
| `eval(expression)` | 执行字符串表达式 | `eval("1+2")` → 3 | `eval("1+2")` |
| `exec(object)` | 执行Python代码 | `exec("print('hi')")` | `eval()` 或 `Function()` |
| `compile(source, filename, mode)` | 编译源代码为代码对象 | `compile("1+2", "", "eval")` | 无直接对应 |
| `__import__(name)` | 动态导入模块 | `__import__('os')` | `import()` 或 `require()` |

## 迭代器相关

| Python函数 | 功能说明 | 示例 | JavaScript对应 |
|-----------|---------|------|---------------|
| `iter(object)` | 返回迭代器对象 | `iter([1,2,3])` | `arr[Symbol.iterator]()` |
| `next(iterator[, default])` | 获取迭代器的下一个元素 | `next(it, 'end')` | `iterator.next().value` |

## 面向对象

| Python函数 | 功能说明 | 示例 | JavaScript对应 |
|-----------|---------|------|---------------|
| `type(obj)` | 返回对象类型 | `type(5)` → `<class 'int'>` | `typeof 5` 或 `obj.constructor` |
| `object()` | 返回新的无特征对象 | `object()` | `{}` 或 `new Object()` 或 `Object.create(null)` |
| `super([type[, obj]])` | 调用父类方法 | `super().__init__()` | `super.method()` |
| `classmethod(func)` | 类方法装饰器 | `@classmethod` | `static method()` |
| `staticmethod(func)` | 静态方法装饰器 | `@staticmethod` | `static method()` |
| `property(fget)` | 属性装饰器 | `@property` | `get property()` / `set property()` |

## 格式化和表示

| Python函数 | 功能说明 | 示例 | JavaScript对应 |
|-----------|---------|------|---------------|
| `repr(obj)` | 返回对象的官方字符串表示 | `repr("hi")` → "'hi'" | `JSON.stringify()` 或 `obj.toString()` |
| `ascii(obj)` | 返回ASCII字符串表示 | `ascii("你好")` | 需自定义转义 |
| `format(value[, format_spec])` | 格式化值 | `format(123, '05d')` → '00123' | 字符串模板或`padStart()/padEnd()` |

## 其他实用函数

| Python函数 | 功能说明 | 示例 | JavaScript对应 |
|-----------|---------|------|---------------|
| `help([obj])` | 显示帮助文档 | `help(print)` | `console.dir()` 或查看文档 |
| `breakpoint()` | 进入调试器 | `breakpoint()` | `debugger;` |

## 使用说明

### Python 特有的概念

1. **可迭代对象（iterable）**：在Python中，字符串、列表、元组、字典、集合等都是可迭代对象
2. **元组（tuple）**：不可变序列，JavaScript中没有直接对应
3. **集合（set）**：无序不重复元素集，JavaScript有`Set`类型
4. **字典（dict）**：键值对映射，JavaScript对应`Object`或`Map`

### JavaScript 的注意事项

1. 很多Python内置函数在JavaScript中需要使用对象方法（如`len(arr)` vs `arr.length`）
2. JavaScript的`Array`方法大多会修改原数组，而Python通常返回新对象
3. JavaScript没有元组的概念，通常使用数组或`Object.freeze()`
4. Python的`range()`需要在JavaScript中自己实现或使用展开运算符

### 常用函数对比示例

```python
# Python
numbers = [1, 2, 3, 4, 5]
print(len(numbers))              # 5
print(sum(numbers))              # 15
print(max(numbers))              # 5
filtered = list(filter(lambda x: x > 2, numbers))  # [3, 4, 5]
mapped = list(map(lambda x: x * 2, numbers))       # [2, 4, 6, 8, 10]
```

```javascript
// JavaScript
const numbers = [1, 2, 3, 4, 5];
console.log(numbers.length);                    // 5
console.log(numbers.reduce((a, b) => a + b));   // 15
console.log(Math.max(...numbers));              // 5
const filtered = numbers.filter(x => x > 2);    // [3, 4, 5]
const mapped = numbers.map(x => x * 2);         // [2, 4, 6, 8, 10]
```



### 关键对比总结

#### ✅ Python 返回新对象（推荐使用）
```python
# 序列
new_list = sorted(original_list)      # 不修改原列表
new_list = original_list.copy()       # 浅拷贝
new_list = original_list[:]           # 切片拷贝
new_list = list(map(func, data))      # 映射
new_list = list(filter(func, data))   # 过滤

# 集合
new_set = set1 | set2                 # 并集
new_set = set1 & set2                 # 交集
new_set = set1 - set2                 # 差集

# 字典 (Python 3.9+)
new_dict = dict1 | dict2              # 合并
new_dict = {**dict1, **dict2}         # 解包合并

# 字符串 (所有操作都返回新字符串)
new_str = old_str.upper()
new_str = old_str.replace('a', 'b')
```

#### ❌ Python 原地修改（需要注意）
```python
# 这些会修改原对象!
original_list.sort()          # 原地排序
original_list.reverse()       # 原地反转
original_list.append(x)       # 原地添加
original_list.extend(other)   # 原地扩展
original_set.add(x)           # 原地添加
original_dict.update(other)   # 原地更新
original_dict[key] = value    # 原地修改
```

#### JavaScript 对比
```javascript
// ✅ 返回新数组
const newArr = arr.map(x => x * 2);
const newArr = arr.filter(x => x > 0);
const newArr = arr.slice();
const newArr = [...arr];
const newArr = arr.concat(other);
const newArr = arr.toSorted();        // ES2023+
const newArr = arr.toReversed();      // ES2023+

// ❌ 原地修改
arr.sort();                           // 原地排序
arr.reverse();                        // 原地反转
arr.push(x);                          // 原地添加
```

### 最佳实践建议

1. **优先使用返回新对象的方法**，避免副作用
2. **需要性能优化时**才使用原地修改方法
3. **函数式编程**推荐使用 `map`、`filter`、推导式等
4. **记住规律**：
   - Python: 大部分**列表方法**原地修改，**内置函数**返回新对象
   - Python: **所有字符串操作**都返回新字符串（字符串不可变）
   - JavaScript: 大部分**数组方法**返回新数组（`sort`/`reverse`/`push` 等除外）

## 总结

Python的内置函数设计理念是提供丰富的功能函数，而JavaScript更倾向于将功能作为对象的方法。Python的函数式编程特性更强，而JavaScript在ES6+后也增强了函数式编程能力。



## 返回新对象的操作（非原地修改）

> 这些操作不会修改原始对象，而是返回新的对象/数组/集合

### 序列操作 - 返回新对象

| Python操作           | 返回类型 | 示例                                  | JavaScript对应                              | 是否返回新对象 |
| -------------------- | -------- | ------------------------------------- | ------------------------------------------- | -------------- |
| `sorted(list)`       | 新列表   | `sorted([3,1,2])` → `[1,2,3]`         | `[...arr].sort()` 或 `arr.toSorted()`       | ✅ 新数组       |
| `list.copy()`        | 新列表   | `[1,2].copy()` → `[1,2]`              | `arr.slice()` 或 `[...arr]`                 | ✅ 新数组       |
| `list[:]`            | 新列表   | `arr[:]`                              | `arr.slice()`                               | ✅ 新数组       |
| `list.sort()`        | None     | `arr.sort()` 原地排序                 | `arr.sort()`                                | ❌ 原地修改     |
| `list.reverse()`     | None     | `arr.reverse()` 原地反转              | `arr.reverse()`                             | ❌ 原地修改     |
| `reversed(list)`     | 迭代器   | `list(reversed([1,2,3]))` → `[3,2,1]` | `arr.toReversed()` 或 `[...arr].reverse()`  | ✅ 新数组       |
| `list + list`        | 新列表   | `[1,2] + [3,4]` → `[1,2,3,4]`         | `arr1.concat(arr2)` 或 `[...arr1, ...arr2]` | ✅ 新数组       |
| `list * n`           | 新列表   | `[1,2] * 3` → `[1,2,1,2,1,2]`         | `Array(3).fill([1,2]).flat()`               | ✅ 新数组       |
| `list.extend(other)` | None     | `arr.extend([3,4])` 原地扩展          | `arr.push(...other)`                        | ❌ 原地修改     |
| `list.append(x)`     | None     | `arr.append(5)` 原地添加              | `arr.push(5)`                               | ❌ 原地修改     |

### 迭代器/映射操作 - 返回新对象

| Python操作           | 返回类型  | 示例                                               | JavaScript对应           | 是否返回新对象 |
| -------------------- | --------- | -------------------------------------------------- | ------------------------ | -------------- |
| `map(func, iter)`    | 迭代器    | `list(map(str, [1,2]))` → `['1','2']`              | `arr.map(String)`        | ✅ 新数组       |
| `filter(func, iter)` | 迭代器    | `list(filter(lambda x:x>0, [-1,1]))` → `[1]`       | `arr.filter(x=>x>0)`     | ✅ 新数组       |
| `zip(*iters)`        | 迭代器    | `list(zip([1,2],['a','b']))` → `[(1,'a'),(2,'b')]` | 自定义或lodash `_.zip()` | ✅ 新数组       |
| `enumerate(iter)`    | 迭代器    | `list(enumerate(['a','b']))` → `[(0,'a'),(1,'b')]` | `arr.map((v,i)=>[i,v])`  | ✅ 新数组       |
| `range(n)`           | range对象 | `list(range(3))` → `[0,1,2]`                       | `[...Array(3).keys()]`   | ✅ 新数组       |

### 集合操作 - 返回新对象

| Python操作          | 返回类型   | 示例                         | JavaScript对应                               | 是否返回新对象 |
| ------------------- | ---------- | ---------------------------- | -------------------------------------------- | -------------- |
| `set(iter)`         | 新集合     | `set([1,1,2])` → `{1,2}`     | `new Set([1,1,2])`                           | ✅ 新Set        |
| `set1 \| set2`      | 新集合     | `{1,2} \| {2,3}` → `{1,2,3}` | `new Set([...set1, ...set2])`                | ✅ 新Set        |
| `set1 & set2`       | 新集合     | `{1,2} & {2,3}` → `{2}`      | `new Set([...set1].filter(x=>set2.has(x)))`  | ✅ 新Set        |
| `set1 - set2`       | 新集合     | `{1,2} - {2,3}` → `{1}`      | `new Set([...set1].filter(x=>!set2.has(x)))` | ✅ 新Set        |
| `set1 ^ set2`       | 新集合     | `{1,2} ^ {2,3}` → `{1,3}`    | 对称差集，需自定义                           | ✅ 新Set        |
| `frozenset(iter)`   | 不可变集合 | `frozenset([1,2])`           | 无直接对应                                   | ✅ 新对象       |
| `set.copy()`        | 新集合     | `{1,2}.copy()`               | `new Set(set)`                               | ✅ 新Set        |
| `set.add(x)`        | None       | `s.add(3)` 原地添加          | `set.add(3)`                                 | ❌ 原地修改     |
| `set.update(other)` | None       | `s.update({3,4})` 原地更新   | 循环 `add()`                                 | ❌ 原地修改     |

### 字典操作 - 返回新对象

| Python操作           | 返回类型      | 示例                                        | JavaScript对应                         | 是否返回新对象 |
| -------------------- | ------------- | ------------------------------------------- | -------------------------------------- | -------------- |
| `dict(other)`        | 新字典        | `dict(a=1, b=2)` → `{'a':1,'b':2}`          | `{a:1, b:2}`                           | ✅ 新对象       |
| `dict.copy()`        | 新字典        | `{'a':1}.copy()`                            | `{...obj}` 或 `Object.assign({}, obj)` | ✅ 新对象       |
| `dict1 \| dict2`     | 新字典 (3.9+) | `{'a':1} \| {'b':2}` → `{'a':1,'b':2}`      | `{...obj1, ...obj2}`                   | ✅ 新对象       |
| `{**dict1, **dict2}` | 新字典        | `{**{'a':1}, **{'b':2}}`                    | `{...obj1, ...obj2}`                   | ✅ 新对象       |
| `dict.keys()`        | 视图对象      | `{'a':1}.keys()` → `dict_keys(['a'])`       | `Object.keys(obj)`                     | ✅ 新数组       |
| `dict.values()`      | 视图对象      | `{'a':1}.values()` → `dict_values([1])`     | `Object.values(obj)`                   | ✅ 新数组       |
| `dict.items()`       | 视图对象      | `{'a':1}.items()` → `dict_items([('a',1)])` | `Object.entries(obj)`                  | ✅ 新数组       |
| `dict.update(other)` | None          | `d.update({'b':2})` 原地更新                | `Object.assign(obj, other)`            | ❌ 原地修改     |
| `dict[key] = value`  | None          | `d['a'] = 1` 原地修改                       | `obj.a = 1`                            | ❌ 原地修改     |

### 字符串操作 - 返回新对象

| Python操作              | 返回类型 | 示例                                   | JavaScript对应           | 是否返回新对象 |
| ----------------------- | -------- | -------------------------------------- | ------------------------ | -------------- |
| `str.upper()`           | 新字符串 | `'abc'.upper()` → `'ABC'`              | `'abc'.toUpperCase()`    | ✅ 新字符串     |
| `str.lower()`           | 新字符串 | `'ABC'.lower()` → `'abc'`              | `'ABC'.toLowerCase()`    | ✅ 新字符串     |
| `str.strip()`           | 新字符串 | `' abc '.strip()` → `'abc'`            | `' abc '.trim()`         | ✅ 新字符串     |
| `str.replace(old, new)` | 新字符串 | `'abc'.replace('a','x')` → `'xbc'`     | `'abc'.replace('a','x')` | ✅ 新字符串     |
| `str.split(sep)`        | 新列表   | `'a,b,c'.split(',')` → `['a','b','c']` | `'a,b,c'.split(',')`     | ✅ 新数组       |
| `str.join(iter)`        | 新字符串 | `','.join(['a','b'])` → `'a,b'`        | `['a','b'].join(',')`    | ✅ 新字符串     |
| `str + str`             | 新字符串 | `'a' + 'b'` → `'ab'`                   | `'a' + 'b'`              | ✅ 新字符串     |
| `str * n`               | 新字符串 | `'ab' * 3` → `'ababab'`                | `'ab'.repeat(3)`         | ✅ 新字符串     |
| `str[start:end]`        | 新字符串 | `'abcdef'[1:4]` → `'bcd'`              | `'abcdef'.slice(1,4)`    | ✅ 新字符串     |

### 类型转换 - 返回新对象

| Python操作        | 返回类型   | 示例                            | JavaScript对应                      | 是否返回新对象 |
| ----------------- | ---------- | ------------------------------- | ----------------------------------- | -------------- |
| `list(iter)`      | 新列表     | `list('abc')` → `['a','b','c']` | `Array.from('abc')` 或 `[...'abc']` | ✅ 新数组       |
| `tuple(iter)`     | 新元组     | `tuple([1,2])` → `(1,2)`        | `Object.freeze([1,2])`              | ✅ 新数组       |
| `set(iter)`       | 新集合     | `set([1,1,2])` → `{1,2}`        | `new Set([1,1,2])`                  | ✅ 新Set        |
| `dict(iter)`      | 新字典     | `dict([('a',1)])` → `{'a':1}`   | `Object.fromEntries([['a',1]])`     | ✅ 新对象       |
| `bytes(iter)`     | 新字节对象 | `bytes([65,66])` → `b'AB'`      | `new Uint8Array([65,66])`           | ✅ 新TypedArray |
| `bytearray(iter)` | 新字节数组 | `bytearray([65])`               | `new Uint8Array([65])`              | ✅ 新TypedArray |

### 推导式 - 返回新对象

| Python操作   | 返回类型 | 示例                                    | JavaScript对应                              | 是否返回新对象 |
| ------------ | -------- | --------------------------------------- | ------------------------------------------- | -------------- |
| 列表推导式   | 新列表   | `[x*2 for x in [1,2,3]]` → `[2,4,6]`    | `[1,2,3].map(x=>x*2)`                       | ✅ 新数组       |
| 集合推导式   | 新集合   | `{x*2 for x in [1,2,3]}` → `{2,4,6}`    | `new Set([1,2,3].map(x=>x*2))`              | ✅ 新Set        |
| 字典推导式   | 新字典   | `{x:x*2 for x in [1,2]}` → `{1:2, 2:4}` | `Object.fromEntries([1,2].map(x=>[x,x*2]))` | ✅ 新对象       |
| 生成器表达式 | 生成器   | `(x*2 for x in [1,2,3])`                | 自定义生成器函数                            | ✅ 新迭代器     |

### 其他操作 - 返回新对象

| Python操作           | 返回类型 | 示例                       | JavaScript对应                      | 是否返回新对象 |
| -------------------- | -------- | -------------------------- | ----------------------------------- | -------------- |
| `copy.copy(obj)`     | 浅拷贝   | `copy.copy([1,[2,3]])`     | `{...obj}` 或 `arr.slice()`         | ✅ 新对象       |
| `copy.deepcopy(obj)` | 深拷贝   | `copy.deepcopy([1,[2,3]])` | `structuredClone(obj)` (现代浏览器) | ✅ 新对象       |
| `slice(start, end)`  | 切片对象 | `arr[1:3]` → 新列表        | `arr.slice(1,3)`                    | ✅ 新数组       |
| `divmod(a, b)`       | 元组     | `divmod(7,3)` → `(2,1)`    | `[Math.floor(7/3), 7%3]`            | ✅ 新数组       |

### 
