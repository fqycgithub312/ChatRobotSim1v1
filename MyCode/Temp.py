##sim0614>>仿真知识库的建立
"""
本地知识库问答系统
使用阿里 DashScope（兼容 OpenAI SDK）实现：
1. 向量化 demo.txt 构建知识库
2. 基于知识库回答用户提问
"""

from openai import OpenAI
import numpy as np
import os
# ------------------- 配置 -------------------
from dotenv import load_dotenv
load_dotenv()
# base_url = os.getenv("base_url1")
key = os.getenv("key1")
DASHSCOPE_API_KEY = key    # 替换为你的阿里云 DashScope API Key
BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
EMBEDDING_MODEL = "text-embedding-v1"             # 嵌入模型（生成向量）
CHAT_MODEL = "qwen3.6-plus"                           # 问答模型（可替换为 qwen-max-latest 等）
KB_FILE = "knowledge_base.npy"                    # 知识库持久化文件
# --------------------------------------------

client = OpenAI(api_key=DASHSCOPE_API_KEY, base_url=BASE_URL)


def read_file(path: str) -> str:
    """读取本地文本文件"""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def split_text(text: str, chunk_size: int = 200, overlap: int = 50) -> list[str]:
    """将长文本按句子/段落切分为小块，支持重叠"""
    import re
    sentences = re.split(r'(?<=[。！？.!?])\s*', text)
    chunks, current = [], ""
    for s in sentences:
        if len(current) + len(s) <= chunk_size:
            current += s
        else:
            if current:
                chunks.append(current.strip())
            current = s[max(0, len(s) - overlap):] + s
    if current.strip():
        chunks.append(current.strip())
    result = []
    for chk in chunks:
        if chk:
            result.append(chk)
    return result


def get_embedding(text: str) -> np.ndarray:
    """调用嵌入模型获取文本向量"""
    resp = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text)
    return np.array(resp.data[0].embedding, dtype=np.float32)


def cosine_sim(a: np.ndarray, b: np.ndarray) -> float:
    """计算余弦相似度"""
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-8))


def build_knowledge_base(file_path: str):
    """读取文件、切分、向量化，持久化保存"""
    print(f"正在读取文件: {file_path}")
    text = read_file(file_path)

    print(f"正在切分文本，共 {len(text)} 字符...")
    chunks = split_text(text)
    print(f"切分为 {len(chunks)} 个文本块")

    print(f"正在向量化（使用模型: {EMBEDDING_MODEL}）...")
    vectors = [get_embedding(chunk) for chunk in chunks]

    kb = {"chunks": chunks,
          "vectors": np.array(vectors, dtype=np.float32)
          }
    np.save(KB_FILE, kb, allow_pickle=True)
    print(f"知识库已保存至: {KB_FILE}")
    return kb


def load_knowledge_base() -> dict:
    """加载已有知识库"""
    return np.load(KB_FILE, allow_pickle=True).item()


def search(query: str, kb: dict, top_k: int = 3) -> list[tuple[str, float]]:
    """基于向量相似度从知识库检索相关内容"""
    query_vec = get_embedding(query)
    scores = [cosine_sim(query_vec, v) for v in kb["vectors"]]
    top_idx = np.argsort(scores)[-top_k:][::-1]
    return [(kb["chunks"][i], scores[i]) for i in top_idx]


def answer(question: str, kb: dict) -> str:
    """从知识库检索相关片段，拼入 prompt，让大模型生成回答"""
    results = search(question, kb, top_k=3)

    # 把检索到的相关文档拼成参考资料
    doc_parts = []
    for i, (text, score) in enumerate(results):
        doc_index = f"[相关文档 {i + 1}]"
        score_info = f"(相似度 {score:.2f}):"
        part = f"{doc_index}{score_info}\n{text}"
        doc_parts.append(part)

    context = "\n---\n".join(doc_parts)

    prompt = f"""你是一个基于本地知识库的问答助手。请仅根据以下提供的参考资料回答用户问题。
如果参考资料中没有相关信息，请如实回答"我没有找到相关信息"。

【参考资料】
{context}

【用户问题】
{question}
"""
    resp = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )
    text_all=[]
    for chunk in resp:
        if(chunk.choices):
            text=chunk.choices[0].delta.content
            if text is not None:
                print(f"{text}",end='',flush=False)
                text_all.append(text)
    return text_all
# ------------------- 主程序 -------------------
# 首次运行：构建知识库（如文件已存在则跳过）
if not os.path.exists(KB_FILE):
    print("当前没有知识库！马上建立知识库！")
    kb = build_knowledge_base("demo.txt")
else:
    print("检测到已有知识库，直接加载...")
    kb = load_knowledge_base()
# 交互式问答
print("=" * 30)
question="张角是谁？有什么本领？太平妖术是什么"
print(f"用户提问>>{question}\n")
print("正在检索知识库并生成回答...")
answer(question, kb)
