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
