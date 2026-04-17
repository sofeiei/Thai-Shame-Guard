from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import os
import uvicorn
from preprocess import preprocess_text
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# อนุญาตให้เว็บบน Vercel เข้าใช้งาน API นี้ได้
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# โหลดโมเดล
# ตรวจสอบว่ามีไฟล์ model.pkl และ vectorizer.pkl อยู่ในโฟลเดอร์เดียวกัน
model = joblib.load('model.pkl')
vectorizer = joblib.load('vectorizer.pkl')

class Item(BaseModel):
    text: str

@app.get("/")
def read_root():
    return {"status": "Thai Shame Guard API is Running!"}

@app.post("/predict")
def predict(item: Item):
    try:
        # 1. ทำความสะอาดข้อความด้วย preprocess_text ที่คุณมี
        cleaned = preprocess_text(item.text)
        # 2. แปลงเป็น Vector
        vec = vectorizer.transform([cleaned])
        # 3. ทำนายผล
        pred = model.predict(vec)[0]
        return {"result": pred.upper()}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # ใช้ Port ที่ระบบ Render กำหนดให้
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
