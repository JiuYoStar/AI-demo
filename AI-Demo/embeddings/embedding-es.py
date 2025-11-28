#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Elasticsearch + Embedding 语义搜索 Demo
✔ 生成向量
✔ 存入 Elasticsearch dense_vector 字段
✔ 执行 kNN 语义搜索
"""

from elasticsearch import Elasticsearch
from openai import OpenAI
import numpy as np


# ======================================================
# 1. 配置区域（请修改为你的环境信息）
# ======================================================

ES_HOST = "http://localhost:9200"             # 你的 ES 地址
ES_USER = "elastic"                            # 用户名
ES_PASSWORD = "Q7f8RBi=y4zgrlbCh029"           # 密码

OPENAI_KEY = "sk-7dea7af8f1824bedab1a176e92e42fe6"
OPENAI_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"

INDEX_NAME = "docs_vector_index"        # 索引名称
EMBED_DIM = 1024                        # 向量维度


# ======================================================
# 2. 初始化客户端
# ======================================================

# Elasticsearch 客户端
es = Elasticsearch(
    ES_HOST,
    basic_auth=(ES_USER, ES_PASSWORD)
)

# OpenAI Compatible 客户端（如 DashScope）
client = OpenAI(
    api_key=OPENAI_KEY,
    base_url=OPENAI_BASE_URL
)


# ======================================================
# 3. 创建索引（若不存在）
# ======================================================

def create_index():
    mapping = {
        "mappings": {
            "properties": {
                "text": {"type": "text"},
                "metadata": {"type": "object"},
                "embedding": {
                    "type": "dense_vector",
                    "dims": EMBED_DIM,
                    "index": True,
                    "similarity": "l2_norm"      # 支持 l2_norm / cosine / dot_product
                }
            }
        }
    }

    if not es.indices.exists(index=INDEX_NAME):
        es.indices.create(index=INDEX_NAME, body=mapping)
        print(f"索引创建成功: {INDEX_NAME}")
    else:
        print(f"索引已存在: {INDEX_NAME}")


# ======================================================
# 4. 函数：生成 embedding
# ======================================================

def embed_text(text: str):
    result = client.embeddings.create(
        model="text-embedding-v4",
        input=text,
        dimensions=EMBED_DIM,
        encoding_format="float"
    )
    return result.data[0].embedding


# ======================================================
# 5. 写入文档及向量到 ES
# ======================================================

documents = [
    {
        "id": "doc1",
        "text": "迪士尼门票不可退，但恶劣天气可以退款。",
        "metadata": {"category": "退票政策"}
    },
    {
        "id": "doc2",
        "text": "奇妙年卡一年内可多次入园，并享受餐饮折扣。",
        "metadata": {"category": "会员权益"}
    },
    {
        "id": "doc3",
        "text": "如果在线购买的门票需要退票，需提前48小时申请。",
        "metadata": {"category": "退票政策"}
    }
]


def index_documents():
    print("\n== 开始写入文档 ==")

    for doc in documents:
        emb = embed_text(doc["text"])

        es.index(
            index=INDEX_NAME,
            id=doc["id"],
            document={
                "text": doc["text"],
                "metadata": doc["metadata"],
                "embedding": emb
            }
        )
        print(f"已写入文档: {doc['id']}")

    print("全部文档写入完成\n")


# ======================================================
# 6. 使用 ES 进行 kNN 搜索
# ======================================================

def semantic_search(query_text: str, k: int = 3):
    print(f"\n== 查询文本: {query_text} ==")

    query_emb = embed_text(query_text)

    response = es.search(
        index=INDEX_NAME,
        knn={
            "field": "embedding",
            "query_vector": query_emb,
            "k": k,
            "num_candidates": 10
        },
        source=["text", "metadata"]
    )

    print("\n--- 搜索结果 ---")
    for hit in response["hits"]["hits"]:
        score = hit["_score"]
        source = hit["_source"]

        print(f"\n[相似度得分 score={score:.4f}]")
        print("文本:", source["text"])
        print("元数据:", source["metadata"])


# ======================================================
# 7. 主流程
# ======================================================

if __name__ == "__main__":
    create_index()
    index_documents()

    query = "我想了解迪士尼门票退款的规则"
    semantic_search(query)
