import re

def semantic_chunking(text, max_chunk_size=512):
    """按句子边界进行语义切片"""
    sentences = re.split(r'[。！？.!?]+', text)
    chunks = []
    current = ""

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue

        if len(current) + len(sentence) > max_chunk_size and current:
            chunks.append(current.strip())
            current = sentence
        else:
            current = f"{current} {sentence}".strip() if current else sentence

    if current:
        chunks.append(current.strip())

    return chunks


def print_chunk_analysis(chunks, method_name):
    print(f"\n===== {method_name} =====")
    if not chunks:
        print("未生成切片")
        return

    lengths = [len(c) for c in chunks]
    print(f"切片数量: {len(chunks)}")
    print(f"平均长度: {sum(lengths)/len(lengths):.1f}")
    print(f"最短长度: {min(lengths)}")
    print(f"最长长度: {max(lengths)}")

    for i, c in enumerate(chunks, 1):
        print(f"\n--- Chunk {i} ({len(c)}) ---")
        print(c)


# 更真实的测试文本（医疗业务）
text = """
患者入院需要由门诊医生根据检查结果出具住院指征，随后到住院服务中心办理手续，包括押金预缴、病区分配以及医保信息确认。多数医院已支持手机App自助办理，减少窗口排队时间。

医保报销比例与参保城市、医院等级及科室类型有关。一般情况下，城镇职工医保住院的起付线在1500至2500元之间，超过起付线的部分按照70%至92%比例进行报销。超过封顶线的费用由大病保险继续赔付。异地就医需提前备案，否则无法进行直接结算。

住院期间的治疗方案由主管医生根据病情变化动态调整。若需申请高值耗材或特殊检查（如核磁共振、PET-CT），部分医院要求主管医生审核并向科室主任报批。出院时由医生开具出院证明，费用清单打印后可在自助结算机缴费，医保结算后不足部分可通过电子支付方式补齐。
"""

if __name__ == "__main__":
    print(f"文本长度: {len(text)}")
    chunks = semantic_chunking(text, max_chunk_size=300)
    print_chunk_analysis(chunks, "语义切片")
