from PyPDF2 import PdfReader
from langchain.chains.question_answering import load_qa_chain
from langchain_community.callbacks.manager import get_openai_callback
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.chat_models import ChatTongyi
from typing import List, Tuple
import os
import pickle

# DASHSCOPE_API_KEY = os.getenv('DASHSCOPE_API_KEY')
DASHSCOPE_API_KEY = "sk-7dea7af8f1824bedab1a176e92e42fe6"
# if not DASHSCOPE_API_KEY:
#     raise ValueError("请设置环境变量 DASHSCOPE_API_KEY")


def extract_text_with_page_numbers(pdf) -> Tuple[str, List[int]]:
    """
    从PDF中提取文本并记录每行文本对应的页码

    参数:
        pdf: PDF文件对象

    返回:
        text: 提取的文本内容
        page_numbers: 每行文本对应的页码列表
    """
    text = ""
    page_numbers = []

    for page_number, page in enumerate(pdf.pages, start=1):
        extracted_text = page.extract_text()
        if extracted_text:
            text += extracted_text
            page_numbers.extend([page_number] * len(extracted_text.split("\n")))

    return text, page_numbers


def process_text_with_splitter(
    text: str, page_numbers: List[int], save_path: str = None
) -> FAISS:
    """
    处理文本并创建向量存储

    参数:
        text: 提取的文本内容
        page_numbers: 每行文本对应的页码列表
        save_path: 可选，保存向量数据库的路径

    返回:
        knowledgeBase: 基于FAISS的向量存储对象
    """
    # 创建文本分割器，用于将长文本分割成小块
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", ".", " ", ""],
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )

    # 分割文本
    chunks = text_splitter.split_text(text)
    print(f"文本被分割成 {len(chunks)} 个块。")

    # 创建嵌入模型
    embeddings = DashScopeEmbeddings(
        model="text-embedding-v1",
        dashscope_api_key=DASHSCOPE_API_KEY,
    )

    # 从文本块创建知识库
    knowledgeBase = FAISS.from_texts(chunks, embeddings)
    print("已从文本块创建知识库。")

    # 改进：存储每个文本块对应的页码信息
    # 创建原始文本的行列表和对应的页码列表
    lines = text.split("\n")

    # 为每个chunk找到最匹配的页码
    page_info = {}
    for chunk in chunks:
        # 查找chunk在原始文本中的开始位置
        start_idx = text.find(chunk[:100])  # 使用chunk的前100个字符作为定位点
        if start_idx == -1:
            # 如果找不到精确匹配，则使用模糊匹配
            for i, line in enumerate(lines):
                if chunk.startswith(line[: min(50, len(line))]):
                    start_idx = i
                    break

            # 如果仍然找不到，尝试另一种匹配方式
            if start_idx == -1:
                for i, line in enumerate(lines):
                    if line and line in chunk:
                        start_idx = text.find(line)
                        break

        # 如果找到了起始位置，确定对应的页码
        if start_idx != -1:
            # 计算这个位置对应原文中的哪一行
            line_count = text[:start_idx].count("\n")
            # 确保不超出页码列表长度
            if line_count < len(page_numbers):
                page_info[chunk] = page_numbers[line_count]
            else:
                # 如果超出范围，使用最后一个页码
                page_info[chunk] = page_numbers[-1] if page_numbers else 1
        else:
            # 如果无法匹配，使用默认页码-1（这里应该根据实际情况设置一个合理的默认值）
            page_info[chunk] = -1

    knowledgeBase.page_info = page_info

    # 如果提供了保存路径，则保存向量数据库和页码信息
    if save_path:
        # 确保目录存在
        os.makedirs(save_path, exist_ok=True)

        # 保存FAISS向量数据库
        knowledgeBase.save_local(save_path)
        print(f"向量数据库已保存到: {save_path}")

        # 保存页码信息到同一目录
        with open(os.path.join(save_path, "page_info.pkl"), "wb") as f:
            pickle.dump(page_info, f)
        print(f"页码信息已保存到: {os.path.join(save_path, 'page_info.pkl')}")

    return knowledgeBase


def load_knowledge_base(load_path: str, embeddings=None) -> FAISS:
    """
    从磁盘加载向量数据库和页码信息

    参数:
        load_path: 向量数据库的保存路径
        embeddings: 可选，嵌入模型。如果为None，将创建一个新的DashScopeEmbeddings实例

    返回:
        knowledgeBase: 加载的FAISS向量数据库对象
    """
    # 如果没有提供嵌入模型，则创建一个新的
    if embeddings is None:
        embeddings = DashScopeEmbeddings(
            model="text-embedding-v1",
            dashscope_api_key=DASHSCOPE_API_KEY,
        )

    # 加载FAISS向量数据库，添加allow_dangerous_deserialization=True参数以允许反序列化
    knowledgeBase = FAISS.load_local(
        load_path, embeddings, allow_dangerous_deserialization=True
    )
    print(f"向量数据库已从 {load_path} 加载。")

    # 加载页码信息
    page_info_path = os.path.join(load_path, "page_info.pkl")
    if os.path.exists(page_info_path):
        with open(page_info_path, "rb") as f:
            page_info = pickle.load(f)
        knowledgeBase.page_info = page_info
        print("页码信息已加载。")
    else:
        print("警告: 未找到页码信息文件。")

    return knowledgeBase


# 读取PDF文件
base_dir = os.path.dirname(os.path.abspath(__file__))
pdf_path = os.path.join(base_dir, "demo.pdf")
pdf_reader = PdfReader(pdf_path)
# 提取文本和页码信息
text, page_numbers = extract_text_with_page_numbers(pdf_reader)
text

print(f"提取的文本长度: {len(text)} 个字符。")

# 处理文本并创建知识库，同时保存到磁盘
save_dir = "./vector_db"
knowledgeBase = process_text_with_splitter(text, page_numbers, save_path=save_dir)

# 示例：如何加载已保存的向量数据库
# 注释掉以下代码以避免在当前运行中重复加载
"""
# 创建嵌入模型
embeddings = DashScopeEmbeddings(
    model="text-embedding-v1",
    dashscope_api_key=DASHSCOPE_API_KEY,
)
# 从磁盘加载向量数据库
loaded_knowledgeBase = load_knowledge_base("./vector_db", embeddings)
# 使用加载的知识库进行查询
docs = loaded_knowledgeBase.similarity_search("客户经理每年评聘申报时间是怎样的？")

# 直接使用FAISS.load_local方法加载（替代方法）
# loaded_knowledgeBase = FAISS.load_local("./vector_db", embeddings, allow_dangerous_deserialization=True)
# 注意：使用这种方法加载时，需要手动加载页码信息
"""

# llm = Tongyi(model_name="deepseek-v3", dashscope_api_key=DASHSCOPE_API_KEY) # qwen-turbo
# 使用 qwen-turbo 或其他通义千问模型，或者使用 ChatTongyi
llm = ChatTongyi(model="qwen-turbo", dashscope_api_key=DASHSCOPE_API_KEY)

# 设置查询问题
query = "客户经理被投诉了，投诉一次扣多少分"
# query = "客户经理每年评聘申报时间是怎样的？"
if query:
    # 执行相似度搜索，找到与查询相关的文档
    docs = knowledgeBase.similarity_search(query, k=2) # ← 语义检索召回块

    # 加载问答链
    chain = load_qa_chain(llm, chain_type="stuff")

    # 查看docs内容
    print(f"{docs} <<< docs")

    # 准备输入数据
    input_data = {"input_documents": docs, "question": query}

    # 使用回调函数跟踪API调用成本
    with get_openai_callback() as cost:
        # 执行问答链
        response = chain.invoke(input=input_data)
        print(f"查询已处理。成本: {cost}")
        print(response["output_text"])
        print("来源:")

    # 记录唯一的页码
    unique_pages = set()

    # 显示每个文档块的来源页码
    for doc in docs:
        text_content = getattr(doc, "page_content", "")
        source_page = knowledgeBase.page_info.get(text_content.strip(), "未知")

        if source_page not in unique_pages:
            unique_pages.add(source_page)
            print(f"文本块页码: {source_page}")

'''

这两个系统的核心原理（RAG：检索增强生成）是一致的，但在**技术选型**和**工程复杂度**上有显著区别。您的直觉非常敏锐，`FAISS` 和 `Elasticsearch (ES)` 的选择确实与数据规模、检索方式以及系统架构有关。

### 对比分析：ChatPDF-Faiss vs Ragflow (基于 ES)

| 特性 | 本 Demo (FAISS 方案) | Ragflow / 企业级 RAG (ES 方案) |
| :--- | :--- | :--- |
| **检索核心** | **纯向量检索** (Vector Search) | **混合检索** (Hybrid Search = 关键词 + 向量) |
| **存储引擎** | **FAISS** (Facebook AI Similarity Search) | **Elasticsearch** / OpenSearch / Milvus |
| **数据规模** | **轻量级** (内存级)。适合几千到几百万个向量。 | **海量级** (分布式)。适合亿级数据，支持水平扩展。 |
| **持久化** | 通常存为本地文件 (`.index`, `.pkl`)，加载需全量入内存。 | 存入磁盘索引，支持实时增删改查，无需全量加载。 |
| **检索能力** | 擅长语义相似度匹配 (Dense Retrieval)。 | 擅长关键词精确匹配 (BM25) + 语义匹配，综合召回率更高。 |
| **元数据过滤** | 较弱 (FAISS 主要做向量计算，元数据通常需外挂)。 | **极强**。ES 天生支持复杂的字段过滤、范围查询等。 |

### 1. 为什么 Ragflow 用 ES？
Ragflow 等成熟的 RAG 系统倾向于使用 ES（或类似组件），原因如下：
*   **混合检索 (Hybrid Search)**：这是 RAG 效果提升的关键。纯向量检索有时候会“失效”（例如搜索专有名词、精确数字时，Embedding 可能匹配不准）。ES 可以同时做 **BM25（关键词匹配）** 和 **kNN（向量匹配）**，然后用 RRF（倒排融合）算法合并结果，效果远好于单一检索。
*   **数据量与扩展性**：ES 是分布式的，数据量大了可以加节点，而 FAISS 如果不配合其他数据库，单机内存很容易爆。
*   **多租户与权限**：企业级应用需要隔离不同用户的数据，ES 的过滤查询非常成熟，而 FAISS 实现起来比较麻烦。

### 2. 为什么 Demo 用 FAISS？
*   **极致轻量与速度**：FAISS 是为向量计算优化的 C++ 库，在纯向量搜索速度上非常快，且不需要部署额外的服务（不用像 ES 那样启动一个 Java 进程）。
*   **极简部署**：就是一个 Python 库，装好就能用，非常适合 Demo、个人知识库或嵌入式场景。

### 总结
*   **FAISS** 像是“瑞士军刀”里的**小刀**：专注于**向量计算**这一件事，快、准、轻，适合单机、小规模、纯语义检索场景。
*   **Elasticsearch (Ragflow)** 像是**重型工程车**：是**全功能的搜索引擎**，不仅能算向量，还能做关键词匹配、复杂过滤、分布式存储，适合构建大规模、高质量的企业级知识库。

**结论**： Ragflow 选用 ES 是为了应对大规模数据和更复杂的混合检索需求，而 Demo 选用 FAISS 是为了轻量化和快速演示。
'''
