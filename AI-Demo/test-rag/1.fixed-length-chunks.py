"""
固定长度切片策略
在句子边界进行切分，避免切断句子
"""

# 测试文本
text = """
患者入院前需在门诊完成初诊，医生根据检查结果决定是否具备住院指征。若需住院，患者在住院服务中心办理入院登记、病区分配及押金预缴。多数医院支持手机App自助办理，入住后护士会完成体征测量并建立护理计划。

医保报销方面，城镇职工医保住院起付线一般为1500元至2500元不等，根据医院等级不同报销比例在70%至92%之间。超过封顶线的部分由大病保险继续按照合同比例赔付。部分地区支持异地直接结算，但需提前进行备案，否则需回参保地手工报销。

住院期间若需加做特殊检查，如核磁或PET-CT，通常需要重新申请审批，部分医院对非急诊项目实行预约排队。出院当天由主管医生开具出院证明，费用清单打印后可通过自动结算机支付。若使用医保支付不足部分可选择电子支付或现金补齐。
"""


def improved_fixed_length_chunking(text, chunk_size=512, overlap=50):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size

        # 在句子边界优先截断
        if end < len(text):
            for i in range(end, max(start, end - 100), -1):
                if text[i] in ".!?。！？":
                    end = i + 1
                    break

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        start = end - overlap

    return chunks


def print_chunk_analysis(chunks, method_name):
    print(f"\n===== {method_name} =====")
    if not chunks:
        print("未生成任何切片")
        return

    total = sum(len(c) for c in chunks)
    print(f"切片数量: {len(chunks)}")
    print(f"平均长度: {total / len(chunks):.1f}")
    print(f"最短: {min(len(c) for c in chunks)}")
    print(f"最长: {max(len(c) for c in chunks)}")

    for i, c in enumerate(chunks, 1):
        print(f"\n--- Chunk {i} ({len(c)}) ---")
        print(c)


if __name__ == "__main__":
    print(f"文本长度: {len(text)}")
    chunks = improved_fixed_length_chunking(text, chunk_size=200, overlap=50)
    print_chunk_analysis(chunks, "固定长度切片")

