# ✨ DocuMind AI

> AI-Powered Document Intelligence Platform  
> Built with Groq Llama 3.1, FAISS, HuggingFace Embeddings & Streamlit

---

## 🚀 Live Demo

🌐 [View Live App](https://qfvmzkj6jud7f5buw3mutt.streamlit.app/)

---

## 📌 Overview

DocuMind AI is a production-ready Retrieval-Augmented Generation (RAG) based AI SaaS platform that allows users to upload PDF documents and interact with them using natural language.

It intelligently processes documents, performs semantic search, retrieves relevant context, and generates accurate AI-powered answers in real time.

Designed with a modern glassmorphism UI and streaming response experience, DocuMind AI delivers a premium, startup-grade product experience.

---

## 🧠 How It Works

1️⃣ **Document Processing**  
The uploaded PDF is parsed and split into intelligent text chunks.

2️⃣ **Vector Embeddings**  
Each chunk is converted into semantic vectors using HuggingFace sentence-transformer embeddings.

3️⃣ **Similarity Search (FAISS)**  
When a user asks a question, FAISS retrieves the most relevant chunks based on vector similarity.

4️⃣ **RAG (Retrieval-Augmented Generation)**  
The retrieved context is sent to Llama 3.1 (via Groq API) for high-speed inference.

5️⃣ **Streaming AI Response**  
Answers are streamed live with a typing animation for a premium ChatGPT-like experience.

---

## 🛠 Tech Stack

- Groq API (Llama 3.1-8B-Instant)
- LangChain
- FAISS Vector Database
- HuggingFace Embeddings
- Streamlit
- Python

---

## 💎 Key Features

- 📄 PDF Upload & Intelligent Parsing
- 🔎 Semantic Vector Search
- ⚡ High-Speed LLM Inference (Groq)
- 💬 Multi-Turn Chat Memory
- ✨ Streaming Typing Animation
- 🎨 Ultra-Premium Glassmorphism UI
- 🌙 Dark Mode
- 🌍 Public Deployment on Streamlit Cloud

---

## 📦 Installation (Local Setup)

```bash
git clone https://github.com/your-username/documind-ai.git
cd documind-ai
pip install -r requirements.txt
