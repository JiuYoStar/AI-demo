#### 使用 Black 自动格式化为 4 空格

```shell
# PEP 8（官方）建议4个空格, 区别js/ts, 需要适应一下
pip install black
black main_refactored.py
```

#### 去重

```shell
# 使用set
arr = [1, 2, 2, 3, 1, 4]
unique = list(set(arr))
print(unique)   # [1, 2, 3, 4]  （顺序可能乱）

# 使用dict.fromkeys
arr = [1, 2, 2, 3, 1, 4]
unique = list(dict.fromkeys(arr))
print(unique)   # [1, 2, 3, 4]

# 使用循环逻辑
arr = [1, 2, 2, 3, 1, 4]
unique = []
for x in arr:
    if x not in unique:
        unique.append(x)

print(unique)  # [1, 2, 3, 4]

# 使用列表推导式
arr = [1, 2, 2, 3, 1, 4]
seen = set()
unique = [x for x in arr if not (x in seen or seen.add(x))]
print(unique)   # [1, 2, 3, 4]

# demo >>> 香港agent项目
arr = [1, 2, 3, 4, "Subject", "Feedback", "PdfContent"]
preferred = ["Subject", "Feedback", "PdfContent", "Subject"]

seen = set()
defaults_columns = [x if x in arr else arr[0] for x in preferred if not (x in seen or seen.add(x))]
print(defaults_columns)
```

#### 判断某个值是否在数组中

```shell
# in → 直接判断
print(x in arr)

# count → 统计数量
arr.count(x) > 0
```

#### AI-Agent 香港

`````shell
# 集合推导式
  defaults_columns = {
      x if x in available_columns else available_columns[0] for x in preferred
  }
  ## {表达式 for 变量 in 可迭代对象}
  ## {条件表达式 for 变量 in 可迭代对象}

# 列表推导式
  columns = [col.strip() for col in column.split(",")]
  ## 带条件过滤
  parts = [c.strip() for c in re.split(r"[，,、;]\s*", sel) if c.strip()]
  ## 嵌套推导式
  [label for batch in ordered_results for label in batch]
  ## 等价于
  result = []
  for batch in ordered_results:
      for label in batch:
          result.append(label)
        
# 字典推导式
  ratios = {
      str(r["Category"]): float(r["Ratio%"]) 
      for _, r in stats.iterrows()
  }
  ## 基本用法
  {k: v for k, v in items}
  ## 带条件
  {k: v for k, v in items if condition}
  ## 键值转换
  {v: k for k, v in original_dict.items()}

# 三元表达式
值1 if 条件 else 值2
  ## 等价于
  if 条件:
      result = 值1
  else:
      result = 值2
      
# lambda表达式
  # 第 234 行 - pandas assign 中使用
  .assign(**{"Ratio%": lambda x: x["Count"] / total * 100})
  # 第 60 行 - apply 中使用
  .apply(lambda x: x[:max_chars_per_text])
  # 排序中使用
  .sort_values(key=lambda x: custom_logic(x))
  
# 切片操作
  # 第 42 行 - 字符串切片
  clean_text = text.replace("\n", " ").strip()[:1000]
  # 第 132 行 - 列表切片
  df["建議分類"] = classifications[: len(df)]
  # 第 56 行 - DataFrame 切片
  batch_df = df.iloc[i : i + batch_size]
  # 步长切片
  overview_pts = points[:7]
  appendix_pts = points[7:14]
 
# 生成器表达式
	# 与列表推导式类似，但更节省内存
  (x for x in items)  # 生成器
  [x for x in items]  # 列表
  # 用于 any/all
  any(condition for item in items)
  all(condition for item in items)
  
# *表达式(解构)
  # 第 68 行 - keyword-only 参数
  def func(a, b, *, c, d):
      # c 和 d 必须用关键字传参
      pass
  # 解包
  first, *middle, last = [1, 2, 3, 4, 5]
  # first=1, middle=[2,3,4], last=5
  
# 海象运算符
  # Python 3.8+ 在条件表达式中赋值
  if (n := len(data)) > 10:
      print(f"数据有 {n} 条")
`````



🎯 学习建议

**初级（必须掌握）**列表/字典推导式三元表达式F-strings上下文管理器切片操作

**中级（应该掌握）**Lambda 表达式类型注解解包操作链式调用装饰器基础

**高级（进阶学习）**异步编程 (async/await)高级装饰器元类描述符生成器和协程

这个项目充分展示了现代 Python 的编程特性，是学习 Python 高级特性的绝佳示例！🚀



#### 确认需要引用的依赖包

|    任务类型    | 常用库举例                                   |
| :------------: | :------------------------------------------- |
|    数据处理    | pandas, numpy, polars                        |
| 网络请求 / API | requests, httpx, aiohttp                     |
|    Web开发     | Flask, FastAPI, Django                       |
|      爬虫      | requests + BeautifulSoup, scrapy, playwright |
|    机器学习    | scikit-learn, xgboost, lightgbm              |
|    深度学习    | pytorch, tensorflow                          |
|     可视化     | matplotlib, plotly, seaborn                  |
|     自动化     | pyautogui, selenium, openpyxl                |
|   并发/异步    | threading, multiprocessing, asyncio          |

##### 从网上检索有效的信息

````py
```
在github/google/chatgpt询问相关的信息, 查看推荐的依赖
```
python [任务描述] library
python [想实现的功能] package
best python library for [你的任务]
````



#### 查询

| 类型    | 有序 | 可变 | 支持 index | 支持 find | 典型查找方式                    |
| ------- | ---- | ---- | ---------- | --------- | ------------------------------- |
| `str`   | ✅    | ❌    | ✅          | ✅         | `find()`, `index()`, `'x' in s` |
| `list`  | ✅    | ✅    | ✅          | ❌         | `index()`, `'x' in lst`         |
| `tuple` | ✅    | ❌    | ✅          | ❌         | `index()`, `'x' in tup`         |
| `set`   | ❌    | ✅    | ❌          | ❌         | `'x' in s`                      |
| `dict`  | ❌    | ✅    | ❌          | ❌         | `'key' in d`, `d.get()`         |

-   有序才有index → str list tuple
-   set/dict 无序 → 可变
-   list 有序 → 可变

