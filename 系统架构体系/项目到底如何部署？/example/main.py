"""最小后端示例：无状态 + 连云数据库 + 调 AI 云 API + 配置 CORS。

配套章节：15（Docker 部署）、16（云数据库）、17（AI API）、18（无状态）、21（CORS）。
重点演示"敏感信息全部走环境变量，不写死进代码"。
"""
import os

import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# 跨域：只允许你自己的前端域名，生产环境不要用 "*"（第 21 章）
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.environ.get("FRONTEND_ORIGIN", "http://localhost:5173")],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 无状态：连接串 / 密钥从环境变量注入，不写死（第 16、17、18 章）
DATABASE_URL = os.environ.get("DATABASE_URL", "")
AI_API_KEY = os.environ.get("AI_API_KEY", "")
AI_API_URL = os.environ.get("AI_API_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions")
AI_MODEL = os.environ.get("AI_MODEL", "qwen-plus")


class ChatRequest(BaseModel):
    question: str


def ask_ai(question: str) -> str:
    """调用云端大模型 API（第 17 章）。多数国内模型兼容 OpenAI 格式。"""
    resp = requests.post(
        AI_API_URL,
        headers={"Authorization": f"Bearer {AI_API_KEY}"},
        json={"model": AI_MODEL, "messages": [{"role": "user", "content": question}]},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]


def save_to_db(question: str, answer: str) -> None:
    """把对话存进云数据库（第 16 章）。此处仅示意，实际用 SQLAlchemy 等。"""
    # 例如：INSERT INTO chats (question, answer) VALUES (...)
    pass


@app.get("/api/hello")
def hello():
    return {"message": "Hello from Serverless!"}


@app.post("/api/chat")
def chat(req: ChatRequest):
    answer = ask_ai(req.question)
    save_to_db(req.question, answer)
    return {"answer": answer}
