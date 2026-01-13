# 🎓 UChicago MSADS RAG Assistant

**RAG-Based Interactive AI Assistant for the MS in Applied Data Science Program**

An interactive Retrieval-Augmented Generation (RAG) chatbot designed to help prospective students, current students, and alumni easily navigate and understand the **MS in Applied Data Science (MSADS)** program at the **University of Chicago**.


## 🔍 Project Motivation

The MSADS program website contains rich information spread across **14+ subpages** (admissions, curriculum, capstone, course progression, etc.).
While comprehensive, this structure makes it difficult for users to quickly find answers to natural language questions.

**Goal:**
Build a conversational AI assistant that:

* Understands natural language queries
* Retrieves the most relevant program information
* Delivers clear, grounded, and contextual answers


## ✨ Key Features

* 💬 **Natural language Q&A** over MSADS program content
* 📚 **Retrieval-Augmented Generation (RAG)** for factual grounding
* 🔎 **Vector search + external context** via dual-source retrieval
* 🖥 **Interactive web UI** (Streamlit-based)
* 🧠 Designed for **students, applicants, and alumni**


## 🧠 System Architecture

### 1. Data Collection & Preparation

* **Web scraping** of 14 MSADS subpages

  * Admissions
  * Course Progressions
  * Capstone Projects
  * Program Overview, etc.
* Tools: `requests`, `BeautifulSoup`
* Cleaning & normalization:

  * Removed navigation/sidebars
  * Standardized headers and course names
  * Extracted structured/tabular content

### 2. RAG Pipeline Design

* **Embedding Store:** ChromaDB

  * Chunk size: ~1000 tokens (larger context retention)
* **Retrieval:** Top-3 most relevant chunks
* **LLM Integration:**

  * Vector DB context (internal knowledge)
  * Perplexity API for **external web grounding**


## 🧩 Tech Stack

| Layer           | Tools                                   |
| --------------- | --------------------------------------- |
| Data Collection | Python, BeautifulSoup                   |
| Vector Store    | ChromaDB                                |
| RAG Pipeline    | Custom retrieval + prompt orchestration |
| LLM             | Perplexity API                          |
| Frontend        | Streamlit                               |
| Evaluation      | Manual human review                     |


## 💡 Example Use Cases

* “What are the core courses in the MSADS program?”
* “How does the capstone project work?”
* “What is the recommended course progression for part-time students?”
* “What background is expected for admission?”


## 📊 Evaluation

**Evaluation Goal:**
Assess answer quality in terms of:

* Relevance
* Grounding
* Clarity
* Completeness

**Methodology:**

* Tested **10 representative student queries**
* Manual human review chosen over automated metrics

  * Open-ended answers lack gold references
  * Human evaluation better captures grounding & usefulness
* Evaluation approach aligned with best practices from
  *The LLM Engineers’ Handbook* (Madaan & Ramamurthy, 2024) 

**Findings:**

* Responses were generally fluent and relevant
* Occasional grounding gaps when source coverage was incomplete


## 🚀 Future Work

* Add retrieval metrics (e.g., Precision@K)
* Expand query set for broader student scenarios
* Incorporate user feedback loop
* Improve grounding consistency across subpages
* Potential deployment for official program support


## 👥 Team

**Team 6 – Generative AI Midterm Project**

* Amy Kim
* Cassandra
* Jazil
* Karim
* Maxine

