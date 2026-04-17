from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import os
import uvicorn
from preprocess import preprocess_text
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# อนุญาตให้ Next.js ส่งข้อมูลข้ามมาได้ (ป้องกัน Error CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# โหลดโมเดล
model = joblib.load('model.pkl')
vectorizer = joblib.load('vectorizer.pkl')

class Item(BaseModel):
    text: str

@app.get("/")
def read_root():
    return {"status": "Server is Running!"}

@app.post("/predict")
def predict(item: Item):
    try:
        cleaned = preprocess_text(item.text)
        vec = vectorizer.transform([cleaned])
        pred = model.predict(vec)[0]
        return {"result": pred.upper()}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
