import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# ==============================
# LOAD API KEY
# ==============================
load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    st.error("Groq API key missing in .env file.")
    st.stop()

client = Groq(api_key=API_KEY)

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(
    page_title="DocuMind AI",
    page_icon="✨",
    layout="wide"
)

# ==============================
# SESSION MEMORY
# ==============================
if "messages" not in st.session_state:
    st.session_state.messages = []

# ==============================
# ULTRA PREMIUM CSS
# ==============================
st.markdown("""
<style>

body {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: white;
}

.block-container {
    padding-top: 2rem;
}

.hero {
    font-size: 48px;
    font-weight: 800;
    text-align: center;
    background: linear-gradient(90deg,#818cf8,#ec4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtitle {
    text-align:center;
    color:#cbd5e1;
    margin-bottom:30px;
    font-size:18px;
}

.glass-card {
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(18px);
    border-radius: 22px;
    padding: 25px;
    border: 1px solid rgba(255,255,255,0.1);
    box-shadow: 0 10px 40px rgba(0,0,0,0.4);
    margin-bottom:20px;
}

.user-bubble {
    background: linear-gradient(90deg,#6366f1,#8b5cf6);
    color:white;
    padding:14px 18px;
    border-radius:20px;
    max-width:80%;
    margin-left:auto;
    margin-bottom:10px;
}

.assistant-bubble {
    background: rgba(255,255,255,0.1);
    backdrop-filter: blur(10px);
    color:white;
    padding:14px 18px;
    border-radius:20px;
    max-width:80%;
    margin-bottom:10px;
}

.stTextInput>div>div>input {
    background: rgba(255,255,255,0.1);
    border-radius: 14px;
    padding: 12px;
    color: white;
}

footer {visibility:hidden;}

</style>

<script>
window.scrollTo(0, document.body.scrollHeight);
</script>
""", unsafe_allow_html=True)

# ==============================
# HEADER
# ==============================
st.markdown('<div class="hero">DocuMind AI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">AI-Powered Document Intelligence Platform</div>', unsafe_allow_html=True)

# ==============================
# LAYOUT (2 Columns)
# ==============================
col1, col2 = st.columns([2, 1])

# ==============================
# LEFT SIDE — MAIN APP
# ==============================
with col1:

    uploaded_file = st.file_uploader("Upload your PDF document", type="pdf")

    if uploaded_file:

        from langchain_community.document_loaders import PyPDFLoader
        from langchain_text_splitters import RecursiveCharacterTextSplitter
        from langchain_community.vectorstores import FAISS
        from langchain_community.embeddings import HuggingFaceEmbeddings

        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.read())

        loader = PyPDFLoader("temp.pdf")
        documents = loader.load()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=150
        )
        docs = splitter.split_documents(documents)

        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vectorstore = FAISS.from_documents(docs, embeddings)
        retriever = vectorstore.as_retriever()

        user_input = st.text_input("Ask something about your document...")

        if user_input:
            st.session_state.messages.append(("user", user_input))

            with st.spinner("Analyzing document..."):

                retrieved_docs = retriever.invoke(user_input)
                context = "\n\n".join(doc.page_content for doc in retrieved_docs)

                conversation_history = "\n".join(
                    [f"{role}: {msg}" for role, msg in st.session_state.messages]
                )

                prompt = f"""
You are a professional AI document assistant.

Conversation:
{conversation_history}

Context:
{context}

User Question:
{user_input}
"""

                stream = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0,
                    stream=True
                )

                placeholder = st.empty()
                full_response = ""

                for chunk in stream:
                    if chunk.choices[0].delta.content:
                        full_response += chunk.choices[0].delta.content
                        placeholder.markdown(
                            f'<div class="assistant-bubble">{full_response}▌</div>',
                            unsafe_allow_html=True
                        )

                placeholder.markdown(
                    f'<div class="assistant-bubble">{full_response}</div>',
                    unsafe_allow_html=True
                )

            st.session_state.messages.append(("assistant", full_response))

        st.markdown('<div class="glass-card">', unsafe_allow_html=True)

        for role, msg in st.session_state.messages:
            if role == "user":
                st.markdown(f'<div class="user-bubble">{msg}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="assistant-bubble">{msg}</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

# ==============================
# RIGHT SIDE — HOW IT WORKS
# ==============================
with col2:

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)

    st.markdown("## 🚀 How It Works")

    st.markdown("""
### 1️⃣ Document Processing  
Your PDF is loaded and split into intelligent text chunks.

### 2️⃣ Vector Embeddings  
Each chunk is converted into semantic vectors using HuggingFace embeddings.

### 3️⃣ Smart Retrieval (RAG)  
When you ask a question, the system retrieves the most relevant chunks using FAISS similarity search.

### 4️⃣ AI Reasoning  
The retrieved context is sent to Llama 3.1 via Groq for high-speed inference.

### 5️⃣ Streaming Response  
The answer is streamed live with typing animation for a premium experience.
""")

    st.markdown("### ⚡ Tech Stack")
    st.markdown("""
- Groq API (Llama 3.1)  
- LangChain  
- FAISS  
- HuggingFace Embeddings  
- Streamlit  
""")

    st.markdown('</div>', unsafe_allow_html=True)