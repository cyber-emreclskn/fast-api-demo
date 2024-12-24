from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import os
from openai import OpenAI
from dotenv import load_dotenv
from enum import Enum
from typing import List, Optional

load_dotenv()

app = FastAPI(
    title="AI Assistant API",
    description="""
    # FastAPI ve OpenAI ile AI Agent API'si
    
    Bu API, FastAPI ve OpenAI'nin GPT-3.5 Turbo modelini kullanarak bir AI Agent oluşturur.
    
    ## FastAPI Nedir?
    FastAPI, modern ve hızlı bir Python web framework'üdür. Öne çıkan özellikleri:
    * Otomatik API dokümantasyonu
    * Yüksek performans
    * Pydantic ile veri validasyonu
    * Async/await desteği
    * Type hints ile güvenli kod
    
    ## AI Agent Nedir?
    AI Agent, yapay zeka modellerini kullanarak belirli görevleri yerine getiren yazılım bileşenidir.
    Bu API'de agent:
    * Metin anlama ve üretme
    * Soru yanıtlama
    * Bilgi dönüştürme
    işlevlerini yerine getirir.
    
    ## Kullanım Örnekleri:
    1. Soru-Cevap
    2. Metin Özetleme
    3. İçerik Üretme
    4. Analiz ve Değerlendirme
    
    ## API Özellikleri:
    * Çoklu mesaj desteği
    * Rol tabanlı mesajlaşma (user, system, assistant)
    * Ayarlanabilir yaratıcılık seviyesi (temperature)
    * Hata yönetimi
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

class Role(str, Enum):
    """
    Sohbet rollerini tanımlayan enum sınıfı
    """
    USER = "user"
    SYSTEM = "system"
    ASSISTANT = "assistant"

class Message(BaseModel):
    """
    Tekil mesaj modeli
    """
    role: Role = Field(
        default=Role.USER,
        description="Mesajı gönderen kişinin rolü (user, system, assistant)"
    )
    content: str = Field(
        ...,
        description="Mesaj içeriği",
        example="Python programlama dili nedir?"
    )

class ChatRequest(BaseModel):
    """
    Chat isteği modeli
    """
    messages: List[Message] = Field(
        default=[],
        description="Sohbet geçmişi mesajları"
    )
    temperature: float = Field(
        default=0.7,
        ge=0.0,
        le=2.0,
        description="Yanıt çeşitliliği ve yaratıcılık seviyesi (0.0: Tutarlı, 2.0: Yaratıcı)"
    )
    max_tokens: Optional[int] = Field(
        default=None,
        ge=1,
        le=4096,
        description="Maksimum yanıt uzunluğu"
    )

class ChatResponse(BaseModel):
    """
    Chat yanıt modeli
    """
    response: str = Field(
        ...,
        description="AI'dan gelen yanıt metni"
    )
    role: Role = Field(
        default=Role.ASSISTANT,
        description="Yanıtı veren asistanın rolü"
    )

@app.get("/", tags=["Genel"])
async def root():
    """
    API durumunu kontrol eder
    """
    return {"status": "active", "message": "AI Agent API çalışıyor"}

@app.post(
    "/chat",
    response_model=ChatResponse,
    description="""
    OpenAI GPT-3.5 Turbo ile sohbet endpoint'i.
    
    Bu endpoint üzerinden:
    * Soru sorabilir
    * Metin analizi isteyebilir
    * İçerik üretimi yapabilirsiniz
    
    Örnek kullanım:
    ```python
    response = requests.post(
        "http://localhost:8000/chat",
        json={
            "messages": [
                {
                    "role": "user",
                    "content": "Python nedir?"
                }
            ],
            "temperature": 0.7
        }
    )
    ```
    """,
    tags=["Sohbet"],
    response_description="AI asistandan gelen yanıt"
)
async def chat(request: ChatRequest):
    """
    OpenAI GPT-3.5 Turbo ile sohbet başlatır veya devam ettirir
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": m.role, "content": m.content} for m in request.messages],
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )
        return ChatResponse(
            response=response.choices[0].message.content,
            role=Role.ASSISTANT
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"error": str(e), "type": type(e).__name__}
        )