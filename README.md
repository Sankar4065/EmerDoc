# 🏥 EmerDoc  
### Privacy-First Multimodal Emergency Intelligence System

---

## 📌 Abstract

**EmerDoc** is a **privacy-preserving, multimodal medical intelligence system** designed to assist users with **non-diagnostic, safe emergency first-aid guidance** while maintaining **strict data isolation and memory control**.

Unlike conventional medical chatbots, EmerDoc introduces **episodic reasoning**, **controlled semantic memory**, and **escalation-aware decision logic**, ensuring that:
- advice is **contextually consistent across time**,  
- **unsafe medical escalation is blocked**, and  
- **no raw personal data is permanently retained**.

EmerDoc is engineered as both:
1. a **consumer-facing emergency assistant**, and  
2. a **foundation layer for future clinical pattern-analysis tools**.

---

## 🎯 Problem Statement

### ❓ What problem does EmerDoc address?

- Emergency situations require **immediate guidance**, but:
  - doctors are unavailable,
  - internet access may be limited,
  - and existing AI tools over-diagnose or hallucinate.

- Medical AI systems often:
  - store raw personal data,
  - escalate incorrectly,
  - or give unsafe medical advice.

### ❗ Why does it matter?

- For every **1000 people**, there is **<1 doctor** in many regions.
- Incorrect medical advice can cause **panic, harm, or legal risk**.
- Privacy breaches in health data are **irreversible**.

EmerDoc solves this by enforcing **engineering-level safety and privacy guarantees**.

---

## 🧠 Core Innovation

EmerDoc introduces **three novel design principles**:

### 1️⃣ Episodic Medical Reasoning  
User interactions are grouped into **time-bounded episodes**, allowing:
- symptom accumulation across turns,
- stable issue inference,
- prevention of contradictory advice.

### 2️⃣ Escalation-Aware Issue Control  
A severity-ranked escalation guard ensures:
- issues only escalate when **symptom evidence supports it**,
- dangerous jumps (e.g., *cold → pneumonia*) are blocked.

### 3️⃣ Memory-Safe RAG Architecture  
Retrieval-Augmented Generation is implemented with:
- **TTL-based temporary memory** (auto-expires),
- **episodic long-term memory** (validated only),
- **personal memory overwrite rules** (no silent accumulation).

---

## 🧩 System Architecture

User Input (Text / Image / Audio)
↓
Modality Router
(Text normalization only)
↓
Intent & Symptom Extraction
↓
Issue Refinement + Escalation Guard
↓
LLM Knowledge Generator (Internal)
↓
Safety & Action Filters
↓
Temporary Memory (Qdrant + TTL)
↓
Episodic Memory (Qdrant)
↓
Reasoning Agent
↓
Safe First-Aid Output



---

## 🔒 Privacy-First Design

EmerDoc enforces **hard privacy boundaries**:

- ❌ No raw images stored  
- ❌ No raw audio stored  
- ❌ No diagnosis or medication  
- ❌ No irreversible personal data accumulation  

✅ Only **normalized text** enters reasoning  
✅ Temporary memory auto-expires  
✅ Personal memory is **episode-scoped and replaceable**  

> Privacy is enforced **by architecture**, not policy.

---

## 🧠 Multi-Agent Pipeline

| Agent | Responsibility |
|-----|---------------|
| PlannerAgent | Controls execution stages |
| KnowledgeAgent | Generates educational first-aid actions |
| CriticAgent | Filters unsafe or non-actionable content |
| MemoryAgent | Manages episodic & TTL memory |
| ReasoningAgent | Finalizes stable episode output |

---

## 🧪 Multimodal Strategy

| Modality | Technology | Scope |
|--------|-----------|------|
| Text | Intent + LLM | Primary reasoning |
| Image | BLIP (local) | Caption → text |
| Audio | Whisper (local) | Transcription |

> Multimodal inputs are **converted to text**, then discarded.

---

## 🧠 Memory Architecture

### 🔹 Temporary Memory (TTL)
- Stores validated actions
- Auto-expires
- Prevents repetition

### 🔹 Episodic Memory
- Groups interactions within time windows
- Maintains symptom continuity

### 🔹 Personal Memory
- Overwritten per episode
- Used only for **probabilistic priors**
- Never directly exposed

---

## 🛠️ Technology Stack

### Backend
- Python 3.14
- FastAPI
- Uvicorn

### AI / ML
- Groq LLM API (text reasoning)
- Whisper (local speech-to-text)
- BLIP (local image captioning)
- Sentence-Transformers (embeddings)

### Vector Store
- Qdrant (Docker, local)

---

## 🚀 Installation & Setup

### 1️⃣ Clone
```bash
git clone https://github.com/Sankar4065/EmerDoc.git
cd EmerDoc



2️⃣ Install dependencies
pip install -r requirements.txt

3️⃣ Run Qdrant
docker run -p 6333:6333 qdrant/qdrant

4️⃣ Set API key
$env:GROQ_API_KEY="your_api_key_here"

5️⃣ Run server
python -m uvicorn app:app --reload

📡 API Usage
Health Check
GET /

Main Endpoint
POST /ask


Form Inputs

query (optional)

image (optional)

audio (optional)

user_id (optional)

⚠️ Safety Guarantees

EmerDoc WILL NOT:

Diagnose conditions

Prescribe medication

Replace doctors

EmerDoc WILL:

Provide safe first-aid actions

Encourage rest, hydration, monitoring

Block unsafe escalation

🌍 Impact

Emergency guidance in low-resource regions

Ethical AI in healthcare

Strong privacy guarantees

Scalable clinical intelligence foundation

🔮 Future Directions

Offline LLM deployment

Multilingual reasoning

Doctor-facing diagnostic pattern analysis

Edge & mobile deployment

Federated medical embeddings

📜 License

Educational & hackathon use only.
Medical use requires regulatory compliance.

🙌 Author

Yalla Satya Siva Sankar
JNTUGV CEV, Vizianagaram
EmerDoc — Privacy-First Medical Intelligence

