# 📚 PaperTutorAI

> An AI-powered research paper assistant that enables users to upload multiple scientific papers, generate detailed summaries, and interact with them through Retrieval-Augmented Generation (RAG).

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![FAISS](https://img.shields.io/badge/FAISS-Vector_Search-green)
![SentenceTransformers](https://img.shields.io/badge/SentenceTransformers-Embeddings-orange)
![OpenRouter](https://img.shields.io/badge/OpenRouter-LLM-purple)

---

## 🚀 Features

- 📄 Upload one or multiple research papers (PDF)
- 🔍 Hybrid Retrieval (FAISS + BM25)
- 💬 Chat with your research papers
- 📝 Generate structured paper summaries
- 🌐 Context-aware web search for background information
- 📏 Adjustable answer length
- 📚 Multi-paper knowledge base
- 📖 Source attribution with page numbers

---

## 📸 Screenshots

(Add screenshots here)

### Home Page

![Home](assets/home.png)

### Chat

![Chat](assets/chat.png)

### Summary

![Summary](assets/summary.png)

---

## 🏗️ Project Architecture

```text
PDF Upload
      │
      ▼
Text Extraction (PyMuPDF)
      │
      ▼
Chunking
      │
      ▼
SentenceTransformer Embeddings
      │
      ▼
FAISS + BM25 Hybrid Retrieval
      │
      ▼
Context Assembly
      │
      ▼
OpenRouter LLM
      │
      ▼
Answer / Summary
```

---

## 📂 Folder Structure

```text
PaperTutorAI/
│
├── app.py
├── parsers/
├── rag/
├── services/
├── utils/
├── assets/
├── uploads/
├── exports/
├── README.md
└── requirements.txt
```

---

## ⚙️ Installation

```bash
git clone https://github.com/oreomcflurryyy/PaperTutorAI.git

cd PaperTutorAI

python -m venv venv

source venv/bin/activate

pip install -r requirements.txt
```

Create a `.env` file:

```env
OPENROUTER_API_KEY=your_api_key
OPENROUTER_MODEL=nvidia/nemotron-3-super-120b-a12b:free
```

Run:

```bash
streamlit run app.py
```

---

## 💡 Usage

1. Upload one or more research papers.
2. Build the knowledge base.
3. Select a paper and generate a summary.
4. Ask questions about the uploaded papers.
5. Clear chat without removing the knowledge base.
6. Clear the knowledge base to start over.

---

## 🧠 Technologies

- Python
- Streamlit
- PyMuPDF
- SentenceTransformers
- FAISS
- BM25
- OpenRouter API
- NumPy

---

## 🔬 How It Works

1. Extract text from uploaded PDFs.
2. Split documents into semantic chunks.
3. Generate dense embeddings using SentenceTransformers.
4. Store embeddings in a FAISS index.
5. Combine semantic retrieval with BM25 keyword search.
6. Retrieve the most relevant chunks.
7. Augment prompts with retrieved context.
8. Generate answers and summaries using an LLM through OpenRouter.

---

## 🚧 Future Improvements

- Citation-aware responses
- Interactive paper comparison
- Figure and table understanding
- Export summaries to PDF/Markdown
- Conversation memory across sessions
- Support for additional document formats

---

## 📄 License

MIT License
