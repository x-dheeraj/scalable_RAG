# Scalable Async RAG Pipeline with LangChain & Docker

A fully containerized, asynchronous Retrieval-Augmented Generation (RAG) backend engineered for scale. Built with FastAPI, LangChain, Qdrant vector database, Valkey/Redis task queue (RQ), and local LLM inference via Ollama.

---

## 📌 Architecture Overview

```text
User / Client
      │
      ▼  POST /chat?query=...
┌───────────────────┐
│   FastAPI Server  │  ──► Enqueues job to Valkey & returns job_id immediately
└───────────────────┘
          │
          ▼  Push Task
┌───────────────────┐
│  Redis / Valkey   │  (Dockerized Message Broker & Task Queue)
└───────────────────┘
          │
          ▼  Pulls Job
┌───────────────────┐
│     RQ Worker     │  (Background Task Consumer)
└───────────────────┘
     │            ▲
     │ LangChain  │ 1. Similarity Search (Top-K Chunks)
     ▼            │
┌───────────────────┐
│     Qdrant DB     │  (Dockerized Vector Store on :6333)
└───────────────────┘
     │
     │ 2. Grounded Context + User Query
     ▼
┌───────────────────┐
│   Ollama (LLM)    │  (Local Models: Qwen2.5:7b/ bge-m3)
└───────────────────┘
     │
     ▼  Saves Output & Lifecycle Status
Client polls GET /job-status?job_id=... ──► Receives final response



## ✨ Features

- **Dockerized Infrastructure**: Run Qdrant vector database and Redis / Valkey queue services locally in lightweight Docker containers.
- **LangChain Orchestration**: Modular PDF parsing (`PyPDFLoader`), semantic text chunking, embedding generation, and contextual prompt construction.
- **Asynchronous Processing**: Long-running LLM generation runs in background worker processes via Python RQ, keeping FastAPI endpoints non-blocking.
- **Private & Local Inference**: Powered by local Ollama instances (`qwen2.5:7b`, `bge-m3`) with zero external API fees and total privacy.
- **Swagger Documentation**: Interactive OpenAPI / Swagger UI provided out-of-the-box by FastAPI.


## 📁 Project Structure

```text
├── client/
│   └── rq_client.py         # Valkey connection and RQ queue initialization
├── queues/
│   └── worker.py            # Background worker task (similarity search + LLM invocation)
├── cpumemory.pdf            # Sample document knowledge base
├── docker-compose.yml       # Container services (Qdrant, Redis/Valkey)
├── index.py                 # Offline indexing script (PDF chunking + Qdrant upload)
├── main.py                  # Application entry point
├── server.py                # FastAPI routes (/chat, /job-status)
└── requirements.txt         # Project dependencies


## 🛠️ Tech Stack

- **Framework**: FastAPI, Uvicorn
- **Orchestration**: LangChain, `langchain-community`, `langchain-ollama`
- **Vector Database**: Qdrant (Docker)
- **Task Queue & Broker**: Python RQ, Redis / Valkey (Docker)
- **LLM Engine**: Ollama (`qwen2.5:7b` / `bge-m3`)
- **Containerization**: Docker Compose
