# 🔐 AI-Based Semantic Search for Information Security Policies

## 📌 Overview

This project is an **AI-powered Semantic Search and Retrieval-Augmented Generation (RAG) system** designed to retrieve and explain information security policies in an intelligent and user-friendly manner.

Unlike traditional keyword-based search systems, this solution understands the **context and intent** of user queries and provides accurate, structured answers.

---

## 🚀 Key Features

* 🔍 **Semantic Search (FAISS)**
* 🤖 **AI Answer Generation (RAG)**
* 📄 **Section-based Retrieval (Purpose, Scope, Roles, etc.)**
* ⚡ **Fast Vector Search**
* 💬 **Chat-based UI**
* 🧠 **Context-aware responses**
* 📝 **Audit logging**

---

## 🏗️ System Architecture

User Query → Embedding → FAISS Search → Context Retrieval → LLM (RAG) → Response

---

## 🛠️ Technologies Used

* Python
* Flask
* Sentence Transformers
* FAISS (Vector Database)
* OpenAI GPT (LLM)
* HTML, CSS, JavaScript

---

## 📂 Project Structure

```
project/
│
├── policies.json
├── ingest.py
├── chatbot.py
├── app.py
├── vectordb.index
├── texts.pkl
├── meta.pkl
├── audit_log.json
```

---

## ⚙️ Installation & Setup

### 1️⃣ Install dependencies

```bash
pip install flask faiss-cpu sentence-transformers openai
```

---

### 2️⃣ Run ingestion

```bash
python ingest.py
```

---

### 3️⃣ Start application

```bash
python app.py
```

---

### 4️⃣ Open in browser

```
http://127.0.0.1:5000
```

---

## 🧪 Sample Queries

* What is the purpose of Risk Assessment Policy?
* What is the scope of Incident Management Policy?
* What are roles in Access Control Policy?
* Explain Encryption Policy

---

## 📊 Output Format

```
[Policy]: Risk Assessment Policy  
[Section]: Scope  
[Answer]: Applies to all employees and systems...  
[Source]: Based on policy content  
```

---

## ⚠️ Limitations

* Depends on quality of input data
* Requires internet for AI model
* Limited handling of ambiguous queries

---

## 🔮 Future Enhancements

* Multi-language support
* Voice-based interaction
* Role-based access control
* Enterprise dashboard

---

## 👨‍🎓 Academic Note

This project was developed as part of a **final year academic project** to demonstrate the application of AI, semantic search, and RAG in information security policy management.

---

## 📬 Contact

For any queries or improvements, feel free to reach out.

---

⭐ *If you found this project useful, consider giving it a star!*
