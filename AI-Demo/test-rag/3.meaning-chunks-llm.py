from openai import OpenAI
import json
import os
import re
from typing import Any, List

BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
MODEL_NAME = "qwen-turbo-latest"
SYSTEM_PROMPT = (
    "你是一个专业的文本切片助手。"
    "请严格按照JSON格式返回结果，不要添加任何额外的标记或注释。"
)


def build_prompt(text: str, max_chunk_size: int) -> str:
    """构造用户提示词，避免在逻辑里拼接散落的字符串。"""
    return f"""
        请将以下文本按照语义完整性进行切片，每个切片不超过{max_chunk_size}字符。
        要求：
        1. 保持语义完整性
        2. 在自然的分割点切分
        3. 严格返回JSON格式：
        {{
          "chunks": [
            "第一个切片内容",
            "第二个切片内容"
          ]
        }}

        文本内容：
        {text}

        仅返回JSON：
    """


def _load_json(candidate: str) -> Any:
    """尽量容忍轻微格式问题的 JSON 加载。"""
    try:
        return json.loads(candidate)
    except Exception:
        return None


def _normalize_chunks(chunks_data: Any) -> List[str]:
    """兼容多种返回结构，最终折叠为字符串列表。"""
    if isinstance(chunks_data, dict):
        if "chunks" in chunks_data and isinstance(chunks_data["chunks"], list):
            return [c for c in chunks_data["chunks"] if isinstance(c, str) and c.strip()]
        if "slice" in chunks_data:
            value = chunks_data["slice"]
            if isinstance(value, list):
                return [v for v in value if isinstance(v, str) and v.strip()]
            if isinstance(value, str) and value.strip():
                return [value]
    if isinstance(chunks_data, list):
        normalized = []
        for item in chunks_data:
            if isinstance(item, str) and item.strip():
                normalized.append(item)
            elif isinstance(item, dict):
                value = item.get("slice") or item.get("chunk") or item.get("text")
                if isinstance(value, str) and value.strip():
                    normalized.append(value)
        if normalized:
            return normalized
    return []


def parse_chunk_response(raw_result: str) -> List[str]:
    """清洗并解析 LLM 返回，容错处理常见 Markdown 包裹。"""
    cleaned = raw_result.strip()
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
    cleaned = re.sub(r"\s*```$", "", cleaned)

    # 先尝试直接解析
    direct = _load_json(cleaned)
    if direct:
        normalized = _normalize_chunks(direct)
        if normalized:
            return normalized

    # 再尝试抽取 JSON 片段
    json_match = re.search(r"(\{.*\}|\[.*\])", cleaned, re.DOTALL)
    if json_match:
        maybe_json = _load_json(json_match.group(1))
        if maybe_json:
            normalized = _normalize_chunks(maybe_json)
            if normalized:
                return normalized

    raise ValueError("无法解析LLM返回的切片结果")


def advanced_semantic_chunking_with_llm(text: str, max_chunk_size: int = 512) -> List[str]:
    """使用 LLM 进行高级语义切片，集中处理提示词构造与返回解析。"""
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        raise RuntimeError("缺少 DASHSCOPE_API_KEY 环境变量，无法调用模型。")

    client = OpenAI(api_key=api_key, base_url=BASE_URL)
    prompt = build_prompt(text, max_chunk_size)

    print("正在调用 LLM 进行语义切片...")
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
    )

    result = (response.choices[0].message.content or "").strip()
    print(f"LLM 返回结果预览: {result[:200]}...")

    return parse_chunk_response(result)


def test_chunking_methods():
    """测试 LLM 语义切片，使用更丰富的示例文本。"""
    text = """
上海迪士尼度假区旺季周末游客量接近承载上限，若计划一天内玩转热门项目，建议开园前30分钟到园并抢先领取虚拟排队。早上优先体验创极速光轮、飞跃地平线与雷鸣山漂流，中午避开人流去漫月轩或部落丰盛堂用餐。

官方购票渠道包括官网、App、小程序与微信服务号，第三方平台需确认“官方授权”标识。学生票、敬老票与儿童票均需绑定证件入园，现场抽检时需出示原件。生日当日登记可获得生日徽章并享部分餐厅甜品券。

演出与巡游需关注App上的当日时间表。城堡投影秀遇雨会切换精简版，花车巡游如遇大风会提前取消。下载官方App可以实时查看等待时间、提交移动点餐并导航到最近的洗手间或补给站。

度假区内有三大酒店：玩具总动员酒店适合亲子，迪士尼乐园酒店更靠近正门，会议团可预订玩具故事主题会议室。入住酒店的游客可享受提前入园和专属安检通道，退房后仍可凭房卡多次入园。

交通方面，地铁11号线直达“迪士尼”站，从出口到乐园步行约8分钟；自驾可停迪士尼停车场，平日小客车封顶200元，夜间18点后进入更优惠。天气多变，夏季防晒防暑，雨天自备雨衣以免影响室外项目。
"""

    print("\n=== LLM 高级语义切片测试 ===")
    try:
        chunks = advanced_semantic_chunking_with_llm(text, max_chunk_size=320)
        print(f"LLM 高级语义切片生成 {len(chunks)} 个切片:")
        for i, chunk in enumerate(chunks):
            print(f"LLM 语义块 {i + 1} (长度: {len(chunk)}): {chunk}")
    except Exception as e:
        print(f"LLM 切片测试失败: {e}")


if __name__ == "__main__":
    test_chunking_methods()

'''
    === LLM 高级语义切片测试 ===

    LLM 高级语义切片生成 5 个切片:
    LLM 语义块 1 (长度: 99): 上海迪士尼度假区旺季周末游客量接近承载上限，若计划一天内玩转热门项目，建议开园前30分钟到园并抢先领取虚拟排队。早上优先体验创极速光轮、飞跃地平线与雷鸣山漂流，中午避开人流去漫月轩或部落丰盛堂用餐。
    LLM 语义块 2 (长度: 96): 官方购票渠道包括官网、App、小程序与微信服务号，第三方平台需确认“官方授权”标识。学生票、敬老票与儿童票均需绑定证件入园，现场抽检时需出示原件。生日当日登记可获得生日徽章并享部分餐厅甜品券。
    LLM 语义块 3 (长度: 86): 演出与巡游需关注App上的当日时间表。城堡投影秀遇雨会切换精简版，花车巡游如遇大风会提前取消。下载官方App可以实时查看等待时间、提交移动点餐并导航到最近的洗手间或补给站。
    LLM 语义块 4 (长度: 86): 度假区内有三大酒店：玩具总动员酒店适合亲子，迪士尼乐园酒店更靠近正门，会议团可预订玩具故事主题会议室。入住酒店的游客可享受提前入园和专属安检通道，退房后仍可凭房卡多次入园。
    LLM 语义块 5 (长度: 95): 交通方面，地铁11号线直达“迪士尼”站，从出口到乐园步行约8分钟；自驾可停迪士尼停车场，平日小客车封顶200元，夜间18点后进入更优惠。天气多变，夏季防晒防暑，雨天自备雨衣以免影响室外项目。
'''
