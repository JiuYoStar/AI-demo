"""
层次切片策略（优化版）
- 先识别文档结构
- 再根据层级 + 长度策略切片
- 适合 RAG / 文档索引 / 长文拆分
"""

from enum import Enum
from dataclasses import dataclass
from typing import List


# =========================
# 1. 层级定义
# =========================


class Level(Enum):
    TITLE1 = 1
    TITLE2 = 2
    TITLE3 = 3
    PARAGRAPH = 4


LEVEL_MARKERS = {
    Level.TITLE1: ("# ", "一、", "1. ", "标题1："),
    Level.TITLE2: ("## ", "二、", "2. ", "标题2："),
    Level.TITLE3: ("### ", "三、", "3. ", "标题3："),
}


# =========================
# 2. 行结构单元
# =========================


@dataclass
class LineUnit:
    text: str
    level: Level


def detect_level(line: str) -> Level:
    """
    根据当前文档的"开头标记", 来识别当前行的层级
    """
    for level, markers in LEVEL_MARKERS.items():
        if any(line.startswith(m) for m in markers):
            return level
    return Level.PARAGRAPH # 如果找不到, 则返回段落级别


# =========================
# 3. 切片判定逻辑
# =========================


def should_split(
    current_chunk: str,
    new_line: LineUnit,
    target_size: int,
    preserve_hierarchy: bool,
) -> bool:
    """
    判断是否需要开启新的 chunk
    """
    print("~" * 80)
    print(f"current_chunk -> {current_chunk}") # 打印当前chunk
    print(f"new_line -> {new_line}") # 打印新行
    print(f"target_size -> {target_size}") # 打印目标长度
    print(f"preserve_hierarchy -> {preserve_hierarchy}") # 打印是否保留层次结构
    print(f"Level.PARAGRAPH -> {Level.PARAGRAPH}")
    print("~" * 80)

    if not current_chunk:
        return False

    # 1. 高层级标题优先切片
    if preserve_hierarchy and new_line.level in (Level.TITLE1, Level.TITLE2):
        return True

    # 2. 超过目标长度
    if len(current_chunk) + len(new_line.text) > target_size:
        return True

    # 3. 段落自然切分
    if new_line.level == Level.PARAGRAPH and len(current_chunk) >= target_size * 0.8:
        return True

    return False


# =========================
# 4. 主切片函数
# =========================


def hierarchical_chunking(
    text: str,
    target_size: int = 512,
    preserve_hierarchy: bool = True,
) -> List[str]:
    """
    基于文档层次结构的切片算法
    """
    chunks: List[str] = []
    current_chunk: List[str] = []

    lines = [l.strip() for l in text.splitlines() if l.strip()]  # noqa: E741
    # print(f"lines -> {lines}") # 将每一行切成独立单元
    for raw_line in lines:
        unit = LineUnit(
            text=raw_line,
            level=detect_level(raw_line),
        )
        # print(f"unit -> {unit}") # 打印每个单元, 定义了text和level

        if should_split(
            current_chunk="\n".join(current_chunk),
            new_line=unit,
            target_size=target_size,
            preserve_hierarchy=preserve_hierarchy,
        ):
            chunks.append("\n".join(current_chunk))
            current_chunk = []

        current_chunk.append(unit.text)

    if current_chunk:
        chunks.append("\n".join(current_chunk))

    return chunks


# =========================
# 5. 结果分析打印
# =========================


def print_chunk_analysis(chunks: List[str], title: str):
    print("=" * 80)
    print(f"{title}")
    print("=" * 80)

    if not chunks:
        print("❌ 未生成切片")
        return

    lengths = [len(c) for c in chunks]

    print(f"切片数量: {len(chunks)}")
    print(f"平均长度: {sum(lengths) / len(lengths):.1f}")
    print(f"最短长度: {min(lengths)}")
    print(f"最长长度: {max(lengths)}")
    print("-" * 80)

    for i, chunk in enumerate(chunks, 1):
        print(f"[Chunk {i}] ({len(chunk)} chars)")
        print(chunk)
        print("-" * 80)


# =========================
# 6. 测试样本数据
# =========================

SAMPLE_TEXT_STANDARD = """
# 1 迪士尼乐园门票指南

## 1.1 门票类型

### 1.1.1 基础门票
迪士尼乐园提供一日票与两日票两种基础门票。
一日票需指定日期使用，价格随季节浮动。
两日票需连续使用，整体价格较单日票更优惠。

### 1.1.2特殊门票
年票适合高频游客，享受多项专属权益。
VIP 门票包含快速通道服务。
团体票适用于 10 人以上团队。

## 1.2 购票方式

### 1.2.1 官方渠道
推荐通过官网、官方 App、微信公众号购票，
可确保票源可靠且信息及时更新。

### 1.2.2 第三方平台
携程、飞猪等平台支持购票，
需认准官方授权标识。

## 1.3 入园须知

### 1.3.1 入园时间
乐园通常在 8:00 开园，20:00 闭园，
具体时间以官方公告为准。

### 1.3.2 安全检查
禁止携带危险物品及玻璃制品，
建议提前到达以减少排队时间。
"""


SAMPLE_TEXT_MIXED = """
# 1 上海迪士尼门票说明

## 1.1 门票说明
迪士尼门票分为单日票、多日票与特殊票种。
购票时需绑定实名信息。

## 1.2 特殊票种说明
1. 年卡说明
年卡适合多次入园游客，部分日期不可使用。

2. VIP 服务
VIP 门票包含快速通道权益，可显著减少排队时间。

## 1.3 入园规则

### 1.3.1 证件要求
所有游客需携带有效身份证件。
儿童票需提供出生证明或户口本。

### 1.3.2 特殊人群
现役及退役军人可享受优惠政策，
需提前通过官方渠道审核。
"""


# =========================
# 7. 主入口
# =========================

if __name__ == "__main__":
    print("▶ 标准 Markdown 结构测试")
    chunks = hierarchical_chunking(
        SAMPLE_TEXT_STANDARD,
        target_size=300,
        preserve_hierarchy=True,
    )
    print_chunk_analysis(chunks, "标准结构切片结果")

    print("\n\n▶ 混合真实风格测试")
    chunks = hierarchical_chunking(
        SAMPLE_TEXT_MIXED,
        target_size=300,
        preserve_hierarchy=True,
    )
    print_chunk_analysis(chunks, "混合结构切片结果")


"""
开发思路:

## 一、先定性：这是一个什么问题？

这个需求本质是：

> **把“长、无序或半结构化的文档”，转换为“适合下游理解与检索的结构化文本块”**

它不是简单的字符串处理，而是**信息工程 / RAG 上游预处理问题**。

---

## 二、高层整体思路（一条主线）

可以用一句话概括整个方案：

> **以文档结构为主线、以长度约束为边界、以语义完整性为目标，构建一个可控的切片流水线**

---

## 三、任务拆分

### 1️⃣ 明确切片的“设计目标”

在动代码前，先统一三点：

* **为什么要切？**
  → 给 embedding / LLM 用
* **切多大？**
  → 有上限、有下限
* **切在哪里？**
  → 尽量在“结构边界”或“语义边界”

这是所有后续设计的**约束条件**。

---

### 2️⃣ 建立文档的“结构认知”

不管输入是 Markdown、Word 还是纯文本，都要回答：

* 什么是标题？
* 什么是段落？
* 哪些是主题边界？

解决方案层面就是：

> **先识别文档结构，而不是直接切字符串**

---

### 3️⃣ 把“文本”转成“结构化单元”

在工程上，需要一个**中间表示**：

* 不再直接处理字符串
* 而是处理“带结构标签的文本单元”

这是为了：

* 解耦逻辑
* 提升可扩展性
* 支撑后续策略升级

---

### 4️⃣ 设计切片策略（规则层）

从策略角度，只需要回答三类问题：

* **结构上是否该切？**（标题）
* **长度上是否必须切？**（上限）
* **语义上是否更优切？**（段落）

本质是：

> **结构规则优先，长度规则兜底，语义规则优化**

---

### 5️⃣ 组装成一个可替换的流水线

最终得到的不是“一个函数”，而是：

* 一条清晰的处理管线
* 各环节可替换、可调参
* 可以横向对比不同策略效果

这一步是为了：

* 接入 RAG
* 接入评测
* 接入不同文档源

---

> **先定义切片目标 → 再建立文档结构 → 再设计切片策略 → 最后流水线化实现**
> 而不是一上来写字符串处理代码。

---

## 五、如果把它当成一个模块来看

> **Document Chunking Engine（文档切片引擎）**

天然属于：

* RAG 上游
* 搜索索引构建
* 文档理解基础设施

---

"""
