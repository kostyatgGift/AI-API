import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai

app = FastAPI(title="Free AI Proxy API")

# Код автоматически возьмет ключ из настроек хостинга (переменных окружения)
GEMINI_API_KEY = os.getenv("AQ.Ab8RN6K_kRasxTeRTBW3HUKiZ0MdwuK6y0CihYGb1YgbWiYW8g")

if not GEMINI_API_KEY:
    print("ВНИМАНИЕ: Переменная GEMINI_API_KEY не установлена!")
else:
    genai.configure(api_key=GEMINI_API_KEY)

class ChatRequest(BaseModel):
    prompt: str

@app.get("/")
def read_root():
    return {"status": "online", "message": "Мой ИИ API работает бесплатно!"}

@app.post("/v1/chat")
async def ask_ai(request: ChatRequest):
    if not GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="Критическая ошибка: API ключ не настроен на сервере.")
    
    if not request.prompt:
        raise HTTPException(status_code=400, detail="Промпт не может быть пустым")
    
    try:
        # Используем бесплатную и быструю модель gemini-1.5-flash
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(request.prompt)
        return {
            "success": True,
            "response": response.text
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка ИИ: {str(e)}")
      
