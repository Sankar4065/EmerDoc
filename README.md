# 🏥 EmerDoc: Privacy-First Emergency AI
---

## 📌 Overview

**EmerDoc** is a privacy-preserving AI system designed to provide **safe, non-diagnostic emergency first-aid guidance** using **text, image, and audio inputs**.  
The system ensures **no raw user data is stored or sent externally** — only extracted intents and safe action points are processed.
A RAG system which uses **vectored memory (qdrant)semantic search and retrieval**
EmerDoc is built for **hackathons, research prototypes, and real-world emergency assistance scenarios** where privacy and safety are critical.

---

## 🎯 Key Objectives

- Provide **general first-aid guidance** without diagnosis or medication
- Ensure **strict privacy boundaries** (no raw data retention)
- Support **multimodal inputs** (text, image, audio)
- Avoid repetitive advice using memory-aware reasoning
- Use **local processing wherever possible**
- **RAG** system which uses **qdrant semantic search with meta data filtering**
- Relay on semantic search for ensured knowledge generation 
---

## 🧠 System Architecture (High Level)

 User Input (Text / Image / Audio)
↓
Modality Router
(Text normalization only)
↓
Intent Extractor (Privacy Boundary)
↓
LLM Knowledge Generator (Internal)
↓
Safety Filters + Knowledge Limiter
↓
Temporary Memory (Qdrant + TTL)
↓
Long-Term Memory (Qdrant)
↓
Context Builder
↓
Reasoning Engine
↓
Final Safe First-Aid Output



---

## 🔒 Privacy-First Design

- Raw **images and audio are deleted immediately** after processing
- Only **normalized text and intent keywords** flow into the system
- No personal identifiers are stored
- Temporary memory auto-expires using TTL
- Long-term memory stores **validated advice and queries**

---

## 🧩 Features

- ✅ Text-based first-aid queries
- ✅ Image understanding using BLIP (local vision model)
- ✅ Audio transcription using Whisper (local)
- ✅ Vector memory using Qdrant
- ✅ Re-ranking using past memory
- ✅ Repetition avoidance
- ✅ Strict medical safety filtering
- ❌ No diagnosis
- ❌ No medication advice

---

## 🛠️ Technology Stack

### Backend
- **Python 3.14**
- **FastAPI**
- **Uvicorn**

### AI / ML
- **Groq LLM API** (text knowledge generation)
- **Whisper (local)** – audio to text
- **BLIP Image Captioning (local)** – image to text
- **Sentence Transformers** – embeddings

### Vector Database
- **Qdrant (Docker)**

### Utilities
- FFmpeg (audio processing)
- Pillow (image handling)
- Torch (model inference)

---

## 📂 Project Structure

privacy_agent/
│
├── agent/
│ ├── agent.py
│ ├── context_builder.py
│ ├── reasoning.py
│ └── reasoning_utils.py
│
├── intent/
│ ├── intent_extractor.py
│ └── embedder.py
│
├── knowledge/
│ ├── llm_generator.py
│ ├── point_parser.py
│ ├── knowledge_limiter.py
│ └── safety.py
│
├── memory/
│ ├── qdrant_client.py
│ ├── temp_memory.py
│ └── long_term_memory.py
│
├── modality/
│ ├── image_processor.py
│ ├── audio_processor.py
│ └── modality_router.py
│
├── app.py
├── requirements.txt
└── README.md  



---

## 🚀 Installation & Setup

---

### 1️⃣ Clone the repository

git clone https://github.com/<Sankar4065>/EmerDoc.git
cd EmerDoc

---

### 2️⃣ Install dependencies

pip install -r requirements.txt


###  3️⃣ Run Qdrant (Docker)


docker run -p 6333:6333 qdrant/qdrant


### 4️⃣ Set Groq API Key


 $env:GROQ_API_KEY="gsk_your_real_api_key_here"


### 5️⃣ Run the application


python -m uvicorn app:app --reload



### API Usage




Health Check
GET /

Ask Endpoint (Multimodal)
POST /ask


Form Parameters

query (optional) – text input

image (optional) – image file

audio (optional) – audio file

user_id (optional)




### ⚠️ Safety Constraints

EmerDoc WILL NOT:

Diagnose medical conditions

Suggest medicines or dosages

Replace professional medical help

EmerDoc WILL:

Provide general first-aid actions

Encourage rest, hydration, safety

Avoid unsafe or repetitive 



#### 🌍 Impact

Enables emergency guidance in low-resource settings

Protects user privacy in sensitive health scenarios

Reduces misinformation during emergencies

Demonstrates ethical AI deployment



##### 🔮 Future Scope

Offline-only LLM integration

Multilingual support

Wearable device integration

Edge deployment (mobile / Raspberry Pi)

Emergency escalation logic

system can be used to develop ai based mobile software

######  📜 License

This project is developed for educational and hackathon purposes.
Use responsibly and ethically.



###### 🙌 Author

YALLA SATYA SIVA SANKAR 
JNTUGV CEV VIZIANAGARAM 
ROLL 22VV1A0459
EmerDoc – Privacy-First Emergency AI


