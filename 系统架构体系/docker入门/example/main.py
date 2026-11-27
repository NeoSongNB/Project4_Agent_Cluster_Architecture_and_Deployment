from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="My AI App", description="一个用来体验 Docker 的最简 AI 服务")


@app.get("/")
def home():
    return {"message": "Hello Docker! 这个 AI 服务正在容器里运行。"}


class PredictRequest(BaseModel):
    text: str


@app.post("/predict")
def predict(req: PredictRequest):
    # 这里假装做了一次 AI 推理。真实场景里，这里会调用模型。
    text = req.text
    sentiment = "正面" if any(w in text for w in ["好", "棒", "喜欢", "赞"]) else "中性/负面"
    return {
        "input": text,
        "length": len(text),
        "fake_sentiment": sentiment,
        "note": "这是模拟的推理结果，重点是体验 Docker 打包部署。",
    }
