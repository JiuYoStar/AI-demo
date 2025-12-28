"""
智能文档分段 (Smart Document Splitting)
使用最简单的逻辑：读取每一行 -> 判断是不是标题 -> 根据长度决定要不要切断
"""

from enum import Enum
from dataclasses import dataclass


# ==========================================
# 1. 定义部分
# ==========================================

class LineType(Enum):
    """ 定义一行的类型 (枚举) """
    H1 = 1           # 一级标题 (例如: # 引言, 一、介绍)
    H2 = 2           # 二级标题 (例如: ## 背景, 二、目的)
    H3 = 3           # 三级标题 (例如: ### 细节)
    NORMAL_TEXT = 4  # 普通正文 (普通段落)


@dataclass
class LineInfo:
    """ 这里存放每一行的信息 """
    text: str       # 行的具体内容
    type: LineType  # 行的类型(是标题还是正文)


# 这里定义了如何识别标题
# 比如: 以 "# " 开头的就是 H1 一级标题
TITLE_MARKERS = {
    LineType.H1: ("# ", "一、", "1. ", "标题1："),
    LineType.H2: ("## ", "二、", "2. ", "标题2："),
    LineType.H3: ("### ", "三、", "3. ", "标题3："),
}


def parse_line_type(text: str) -> LineType:
    """
    判断一行文字是什么类型?
    原理: 检查这行文字是不是以特定的符号开头
    这里的逻辑不太晚上, 如果遇到换行等情况就会识别错误, 最好的方式是分步解析, 参考混乱的md解析
    """
    for type, markers in TITLE_MARKERS.items():
        # 只要这行文字以 markers 里的任意一个开头
        if any(text.startswith(m) for m in markers):
            return type

    # 都不匹配，那就是普通正文
    return LineType.NORMAL_TEXT


# ==========================================
# 2. 核心逻辑: 什么时候切分?
# ==========================================

def need_split(
    current_chunk: str,  # 当前积累的文本片段
    next_line: LineInfo, # 接下来要加入的一行
    max_size: int,       # 允许的最大长度
) -> bool:
    """
    做决定: 是否应该在这里切一刀, 把当前积累的文本存下来?
    返回 True 表示要切分, False 表示继续积累
    """

    # 如果当前还没积累任何内容, 肯定不切
    if not current_chunk:
        return False

    # 规则1: 遇到大标题 (一级或二级标题), 强制切分
    # 这样可以保证每个大章节是独立的
    if next_line.type in (LineType.H1, LineType.H2):
        print(f"  [切分原因] 遇到大标题: {next_line.text[:10]}...")
        return True

    # 规则2: 如果加上新的一行, 长度就会爆掉, 那就切分
    current_length = len(current_chunk)
    new_line_length = len(next_line.text)

    if current_length + new_line_length > max_size:
        print(f"  [切分原因] 长度超标: {current_length} + {new_line_length} > {max_size}")
        return True

    # 规则3: 如果是普通段落, 且当前长度已经比较长了(比如超过80%), 可以从这里自然断开
    # 这样避免把两个无关的长段落硬塞在一起
    if next_line.type == LineType.NORMAL_TEXT and current_length >= max_size * 0.8:
        print(f"  [切分原因] 长度合适且遇到新段落, 自然切分")
        return True

    # 其他情况, 继续积累
    return False


# ==========================================
# 3. 主函数: 开始干活
# ==========================================

def split_text_smartly(
    text: str,       # 要处理的完整大文本
    max_size: int = 512, # 期望的每个片段最大长度
) -> list[str]:

    # 存放最终结果的盒子
    final_chunks: list[str] = []

    # 临时存放当前正在通过积累的行
    current_lines: list[str] = []

    # 1. 把大文本拆成一行一行, 并去掉两头空白
    raw_lines = [line.strip() for line in text.splitlines() if line.strip()]

    print(f"开始处理... 总行数: {len(raw_lines)}")

    # 2. 逐行处理
    for raw_line in raw_lines:

        # 把这一行文字, 包装成 LineInfo 对象, 标记它的类型
        line_info = LineInfo(
            text=raw_line,
            type=parse_line_type(raw_line)
        )

        # 把当前积累的行拼成一个大字符串, 用来做判断
        chunk_so_far = "\n".join(current_lines)

        # 3. 询问裁判: 要不要切分?
        if need_split(chunk_so_far, line_info, max_size):
            # 要切分! 把当前积累的放入最终结果
            final_chunks.append(chunk_so_far)
            # 清空临时列表, 准备积累下一个片段
            current_lines = []

        # 4. 把这一行加入临时列表
        current_lines.append(line_info.text)

    # 5. 循环结束, 别忘了把最后剩下的一点点也存进去
    if current_lines:
        final_chunks.append("\n".join(current_lines))

    return final_chunks


# ==========================================
# 4. 测试与展示
# ==========================================

def show_results(chunks: list[str]):
    """ 漂亮地打印结果 """
    print("\n" + "=" * 50)
    print(f"处理完成! 共生成 {len(chunks)} 个片段")
    print("=" * 50)

    for i, chunk in enumerate(chunks, 1):
        print(f"\n>> 片段 {i} (长度: {len(chunk)})")
        print("-" * 30)
        print(chunk)
        print("-" * 30)


# 测试数据
SAMPLE_TEXT = """
# 苏轼诗词选辑

## 1.1 宋词巅峰
《定风波·莫听穿林打叶声》
三月七日，沙湖道中遇雨。雨具先去，同行皆狼狈，余独不觉。

## 1.2 名篇精选
1. 水调歌头
明月几时有？把酒问青天。
不知天上宫阙，今夕是何年。

2. 念奴娇·赤壁怀古
大江东去，浪淘尽，千古风流人物。
故垒西边，人道是，三国周郎赤壁。

## 1.3 诗歌鉴赏

### 1.3.1 豪放派风格
苏轼作为豪放派代表，其作品气势磅礴，
打破了晚唐以来唯婉约是从的格局。

### 1.3.2 意境分析
即便在遭受贬谪之时，他的诗作依然充满豁达之情，
如“此心安处是吾乡”等千古名句。
"""

if __name__ == "__main__":
    # 运行测试
    results = split_text_smartly(SAMPLE_TEXT, max_size=300)
    show_results(results)
