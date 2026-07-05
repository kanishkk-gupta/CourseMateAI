<div align="center">

# CourseMateAI

### Retrieval-Augmented Generation for Intelligent Document Conversations

An open-source Retrieval-Augmented Generation (RAG) application that enables users to upload PDF documents and interact with them through context-aware conversations powered by **LangChain**, **ChromaDB**, **HuggingFace Embeddings**, **Mistral AI**, and **Streamlit**.

<p align="center">

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-Framework-1C3C3C?style=for-the-badge)
![Mistral](https://img.shields.io/badge/Mistral-AI-orange?style=for-the-badge)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20Database-7B2CBF?style=for-the-badge)
![HuggingFace](https://img.shields.io/badge/HuggingFace-Embeddings-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-success?style=for-the-badge)
![Version](https://img.shields.io/badge/Version-v1.0.0-blue?style=for-the-badge)

</p>

</div>

---

## Overview

**CourseMateAI** is a Retrieval-Augmented Generation (RAG) application designed to answer questions directly from uploaded PDF documents.

Instead of relying solely on a Large Language Model's internal knowledge, the application retrieves the most relevant information from a document, supplies it as context to the LLM, and generates responses grounded in the uploaded content. This approach significantly reduces hallucinations while improving factual accuracy.

The current release (**v1.0.0**) establishes the core RAG pipeline by integrating document ingestion, recursive text chunking, semantic embeddings, vector search, and context-aware answer generation into a simple Streamlit interface.

---

## Live Demo

The application is deployed on Streamlit.

**Application:** **Coming Soon**

---

# Features

### Document Processing

- Upload PDF documents
- Automatic document parsing using **PyPDFLoader**
- Recursive document chunking
- Configurable chunk size and overlap

### Embedding & Indexing

- HuggingFace Embeddings
- `BAAI/bge-small-en-v1.5`
- Persistent Chroma Vector Database
- Local vector indexing

### Retrieval

- Maximum Marginal Relevance (MMR) Retrieval
- Semantic similarity search
- Context retrieval for user queries

### Answer Generation

- Powered by **Mistral AI**
- Prompt-based context grounding
- Hallucination reduction through retrieved context

### User Interface

- Interactive Streamlit application
- PDF Upload
- Question Answering
- Retrieved Context Viewer

---

# System Architecture

```text
                                    Upload PDF
                                         │
                                         ▼
                                PyPDFLoader
                                         │
                                         ▼
                     RecursiveCharacterTextSplitter
                                         │
                                         ▼
                              Document Chunks
                                         │
                                         ▼
                    HuggingFace Embeddings (BGE)
                                         │
                                         ▼
                           Chroma Vector Database
                                         │
────────────────────────────────────────────────────────────────────
                                         │
                                         ▼
                                 User Question
                                         │
                                         ▼
                              Query Embedding
                                         │
                                         ▼
                          MMR Vector Retriever
                                         │
                                         ▼
                          Relevant Document Chunks
                                         │
                                         ▼
                             Prompt Construction
                                         │
                                         ▼
                                Mistral AI LLM
                                         │
                                         ▼
                               Contextual Answer
```

---

# Project Highlights

- Built using the Retrieval-Augmented Generation (RAG) architecture
- Context-aware document question answering
- Semantic search using dense vector embeddings
- Persistent vector storage with ChromaDB
- Maximum Marginal Relevance (MMR) retrieval
- Streamlit-based user interface
- Modular indexing and retrieval workflow
- Foundation for future production-grade RAG enhancements

---

## Tech Stack

| Category | Technology |
|-----------|------------|
| Language | Python |
| Framework | LangChain |
| LLM | Mistral AI |
| Embedding Model | HuggingFace (BAAI/bge-small-en-v1.5) |
| Vector Database | ChromaDB |
| Document Loader | PyPDFLoader |
| Text Splitter | RecursiveCharacterTextSplitter |
| Frontend | Streamlit |
| Environment | Python Dotenv |

---
# Project Structure

```text
CourseMateAI/
│
├── app.py                     # Streamlit User Interface
├── main.py                    # RAG Inference Pipeline
├── create_database.py         # Document Indexing Pipeline
│
├── chroma_db/                 # Persistent Chroma Vector Database
│
├── document loaders/
│      └── deeplearning.pdf
│
├── requirements.txt
├── .env.example
├── .gitignore
├── LICENSE
└── README.md
```

---

# Installation

Clone the repository

```bash
git clone https://github.com/<your-username>/CourseMateAI.git
```

Move into the project

```bash
cd CourseMateAI
```

Install all dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file in the project root.

```env
# Required
MISTRAL_API_KEY=YOUR_MISTRAL_API_KEY

# Optional (Recommended)
HUGGINGFACEHUB_API_TOKEN=YOUR_HUGGINGFACE_TOKEN
```

> **Note**
>
> The Hugging Face access token is optional when using public embedding models such as `BAAI/bge-small-en-v1.5`. However, providing one enables faster downloads and higher API rate limits.

---

# Running the Application

Launch the Streamlit application.

```bash
streamlit run app.py
```

Once the application starts:

1. Upload a PDF document.
2. Click **Create Database**.
3. Wait for document indexing to finish.
4. Ask questions about the uploaded document.

---

# How the Project Works

CourseMateAI follows a two-stage Retrieval-Augmented Generation (RAG) workflow.

## Stage 1 — Document Indexing

This process is performed only once for a document (or whenever the document changes).

```
PDF
 │
 ▼
Load Document
 │
 ▼
Split into Chunks
 │
 ▼
Generate Embeddings
 │
 ▼
Store in ChromaDB
```

The entire indexing pipeline is implemented inside **`create_database.py`**.

---

## Stage 2 — Question Answering

Once the database has been created, the chatbot no longer reads the PDF directly.

Instead, every user query follows this workflow:

```
User Question
        │
        ▼
Generate Query Embedding
        │
        ▼
Search ChromaDB
        │
        ▼
Retrieve Relevant Chunks
        │
        ▼
Prompt Construction
        │
        ▼
Mistral AI
        │
        ▼
Final Answer
```

This entire workflow is implemented inside **`main.py`**.

---

# Why is `create_database.py` separate from `main.py`?

Document indexing is an expensive operation.

Every uploaded document must be:

- Loaded
- Split into chunks
- Embedded
- Indexed

These operations should only happen **once**.

If the indexing pipeline were placed inside `main.py`, the embeddings would be regenerated every time a user asked a question, making the application unnecessarily slow.

Separating the indexing pipeline from the inference pipeline follows the same design pattern used by modern production RAG systems.

---

# Retrieval Strategy

The current version uses **Maximum Marginal Relevance (MMR)** retrieval.

Current configuration:

```python
retriever = vector_store.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 4,
        "fetch_k": 10,
        "lambda_mult": 0.5
    }
)
```

MMR balances **semantic similarity** and **result diversity**, reducing redundant chunks while maintaining relevant context.

---

# Current Version

**Version:** `v1.0.0`

The initial release focuses on building a complete end-to-end RAG pipeline using LangChain and ChromaDB.

### Included Features

- PDF Upload
- Recursive Character Text Splitting
- HuggingFace Embeddings
- ChromaDB
- MMR Retrieval
- Mistral AI Integration
- Streamlit Interface
- Context-Based Responses

---

# Live Deployment

The application is deployed using **Streamlit**.

**Live Demo**

> https://your-streamlit-url.streamlit.app

---
# Future Versions

CourseMateAI is being developed incrementally using **Semantic Versioning**. Each release introduces new capabilities while improving the overall architecture and developer experience.

## v1.0.0 — Initial Release

The first stable release establishes the core Retrieval-Augmented Generation (RAG) pipeline.

### Features

- Single PDF Support
- Recursive Character Text Splitting
- HuggingFace Embeddings (`BAAI/bge-small-en-v1.5`)
- Chroma Vector Database
- Maximum Marginal Relevance (MMR) Retrieval
- Mistral AI Integration
- Streamlit Interface
- Context-Grounded Responses

---

## v1.1.0

### Planned Features

- Multi-PDF Support
- Dynamic Document Selection
- Improved File Management

---

## v1.2.0

### Planned Features

- Persistent Chat History
- Conversation Memory
- Better Session Management

---

## v1.3.0

### Planned Features

- MultiQuery Retriever
- Parent Document Retriever
- Improved Retrieval Quality
- Retrieval Optimization

---

## v2.0.0

### Planned Features

- Hybrid Search (BM25 + Vector Search)
- Cross Encoder Reranking
- Query Rewriting
- Source Citations
- Source Highlighting
- Streaming Responses
- Authentication
- Production-ready Architecture

---

# Planned Architectural Improvements

The current version intentionally prioritizes learning and understanding the fundamentals of Retrieval-Augmented Generation.

Future versions will progressively introduce production-grade software engineering practices.

### Architecture

- Configuration Management (`config.py`)
- Modular Project Structure
- Reusable Retriever Module
- Prompt Management (`prompts.py`)
- Dedicated RAG Chains
- LangChain Expression Language (LCEL)

### Retrieval

- MultiQuery Retriever
- Parent Document Retriever
- Contextual Compression Retriever
- Hybrid Search
- Query Rewriting
- Cross Encoder Reranking

### Engineering

- Logging
- Error Handling
- Configuration Files
- Modular Components
- Cleaner Codebase

### Product

- Persistent Conversations
- Multi-document Support
- Agentic RAG
- Evaluation Dashboard
- Source Attribution
- Better User Experience

---

# Why CourseMateAI?

Most introductory RAG projects demonstrate individual concepts such as document loading, chunking, embeddings, or vector databases in isolation.

CourseMateAI aims to combine these components into a complete end-to-end application while maintaining a clean, modular architecture that can evolve toward a production-ready Retrieval-Augmented Generation system.

The project is intentionally versioned so that every release introduces new capabilities while preserving a clear development history.

---

# Learning Objectives

This project was built to deepen practical understanding of modern Retrieval-Augmented Generation systems.

Core concepts explored include:

- Document Loaders
- Recursive Character Text Splitting
- Embedding Models
- Vector Databases
- Semantic Search
- Retrieval Strategies
- Prompt Engineering
- LangChain
- ChromaDB
- Mistral AI
- Streamlit

---

# Contributing

Contributions, suggestions, and discussions are always welcome.

If you would like to improve the project:

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Open a Pull Request.

Please ensure that any new feature includes clear documentation and follows the existing project structure.

---

# License

This project is licensed under the **MIT License**.

See the `LICENSE` file for additional information.

---

# Acknowledgements

This project builds upon the excellent open-source ecosystem provided by:

- LangChain
- ChromaDB
- Hugging Face
- Mistral AI
- Streamlit
- Python

Special thanks to the open-source community for making modern AI development more accessible.

---

# Author

**Kanishk Gupta**

Computer Science Engineering Undergraduate with a strong interest in Generative AI, Large Language Models, Retrieval-Augmented Generation (RAG), AI Engineering, and Full-Stack Development.

GitHub: **https://github.com/your-username**

LinkedIn: **https://linkedin.com/in/your-profile**

---

<div align="center">

### CourseMateAI

Retrieval-Augmented Generation for Intelligent Document Conversations

**Version 1.0.0**

Built using LangChain • ChromaDB • HuggingFace • Mistral AI • Streamlit

</div>