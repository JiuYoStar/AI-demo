#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
滑动窗口切片策略 (Sliding Window Chunking)
特点: 固定长度切片，保留重叠区域，防止上下文丢失
"""

def sliding_window_chunk(text: str, chunk_size: int = 500, chunk_overlap: int = 50) -> list[str]:
    """
    使用滑动窗口对文本进行切片

    Args:
        text: 待切片的输入文本
        chunk_size: 每个切片的字符长度 (窗口大小)
        chunk_overlap: 切片之间的重叠字符数量

    Returns:
        包含切片文本的列表
    """
    if chunk_overlap >= chunk_size:
        raise ValueError("重叠长度必须小于切片长度")

    step_size = chunk_size - chunk_overlap
    chunks = []

    # 按步长滑动窗口
    for i in range(0, len(text), step_size):
        #截取并清理空白
        chunk = text[i : i + chunk_size].strip()
        if chunk:
            chunks.append(chunk)

    return chunks


# 语义化测试数据
knowledge_base_content = """
[RAG技术简介]
检索增强生成(RAG)是一种结合了检索系统和生成模型的技术架构。它通过从外部知识库中检索相关信息，作为上下文提供给大语言模型(LLM)，从而提高回答的准确性和时效性。

[核心优势]
1. 减少幻觉：基于事实数据的回答能显著降低模型编造信息的概率。
2. 数据实时性：无需重新训练模型，只需更新知识库即可掌握最新信息。
3. 数据隐私：企业私有数据可以在本地处理，无需上传至公有大模型训练。

[切片策略]
文档切片是RAG流程中的关键步骤。切片过大会导致检索噪音，切片过小则可能丢失上下文。滑动窗口策略通过在切片间保留重叠部分，有效解决了边界处的语义断连问题。
"""

if __name__ == "__main__":
    print("=== 滑动窗口切片测试 ===")

    # 设置切片参数
    CHUNK_SIZE = 100    # 切片长度
    OVERLAP = 20        # 重叠长度

    print(f"原始文本长度: {len(knowledge_base_content)} 字符")
    print(f"配置: 长度={CHUNK_SIZE}, 重叠={OVERLAP}\n")

    # 执行切片
    chunks = sliding_window_chunk(knowledge_base_content, CHUNK_SIZE, OVERLAP)

    # 展示结果
    for i, chunk in enumerate(chunks, 1):
        print(f"[{i:02d}] 长度: {len(chunk)}")
        print(f"内容: {chunk}")
        print("-" * 50)
