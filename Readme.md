# FastAPI OpenAI Agent

Modern web framework FastAPI ile geliştirilmiş, OpenAI GPT-3.5 Turbo destekli AI Agent.

## 🚀 Özellikler

- RESTful API (FastAPI)
- OpenAI GPT-3.5 Turbo
- Docker & Docker Compose
- Swagger UI & ReDoc
- Ayarlanabilir yanıt parametreleri

## 📋 Gereksinimler

- Python 3.11+
- Docker & Docker Compose
- OpenAI API key

## 🛠 Kurulum

```bash
# Repo klonlama
git clone <repo-url>
cd fastapi-openai-agent

# Environment ayarları
cp .env.sample .env
# .env dosyasına OPENAI_API_KEY ekleyin

# Docker ile çalıştırma
docker-compose up --build
```

## 🔌 API Kullanımı

### Chat Endpoint

`POST /chat`

**Request:**
```json
{
  "messages": [
    {
      "role": "user",
      "content": "Python nedir?"
    }
  ],
  "temperature": 0.7
}
```

**Response:**
```json
{
  "response": "Python, yüksek seviyeli...",
  "role": "assistant"
}
```

### cURL Örneği
```bash
curl -X POST "http://localhost:8000/chat" \
-H "Content-Type: application/json" \
-d '{
  "messages": [{"role": "user", "content": "Python nedir?"}],
  "temperature": 0.7
}'
```

### Python Örneği
```python
import requests

response = requests.post(
    "http://localhost:8000/chat",
    json={
        "messages": [
            {"role": "user", "content": "Python nedir?"}
        ],
        "temperature": 0.7
    }
)
print(response.json())
```

## 📁 Proje Yapısı

```
.
├── main.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.sample
└── README.md
```

## ⚙️ Parametreler

| Parametre | Açıklama | Varsayılan |
|-----------|----------|------------|
| messages | Sohbet mesajları | - |
| temperature | Yanıt çeşitliliği | 0.7 |
| max_tokens | Maksimum token | None |

## 🔑 Environment Değişkenleri

| Değişken | Açıklama |
|----------|-----------|
| OPENAI_API_KEY | OpenAI API anahtarı |

## 💻 Geliştirme

```bash
# Virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows

# Bağımlılıklar
pip install -r requirements.txt

# Çalıştırma
uvicorn main:app --reload
```

## 🔍 Endpoint'ler

- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## ⚠️ Sorun Giderme

**API Key Hatası:**
```
Error: OpenAI API key not found
```
➡️ `.env` dosyasını kontrol edin

**Docker Hatası:**
```
Error: Connection refused
```
➡️ Docker servisini kontrol edin

## 🔒 Güvenlik Önerileri

- API key'i güvenli saklayın
- Production'da CORS ayarlarını düzenleyin
- Rate limiting ekleyin

## 📝 License

MIT

## 📧 İletişim

GitHub Issues üzerinden iletişime geçebilirsiniz.