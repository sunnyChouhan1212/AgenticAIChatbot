# 🤖 Agentic AI Chatbot

An end-to-end **Agentic AI application** built using LangGraph that supports multiple intelligent workflows including chatbot interactions, tool-based reasoning, and automated AI news summarization.

---

## 🚀 Features

* 💬 **Basic Chatbot** – Conversational AI powered by LLM
* 🌐 **Chatbot with Web Access** – Tool-enabled agent using Tavily Search
* 📰 **AI News Pipeline** – Fetch → Summarize → Save as Markdown
* ⚡ **Fast LLM Inference** using Groq
* 🧠 **State-driven workflow orchestration** using LangGraph
* 🎯 **Modular Node Architecture** (chatbot, tools, pipelines)
* 🖥️ **Interactive UI** built with Streamlit

---

## 🛠️ Tech Stack

* **Python**
* **LangGraph**
* **LangChain**
* **Groq LLM**
* **Tavily Search API**
* **Streamlit**

---

## 📂 Project Structure

```
src/
 ├── langgraphagenticai/
 │   ├── graph/        # Graph builder and workflow orchestration
 │   ├── nodes/        # Chatbot, tools, and AI pipeline nodes
 │   ├── tools/        # External tool integrations (Tavily)
 │   ├── state/        # Shared graph state definition
 │   └── ui/           # Streamlit UI components
app.py
requirements.txt
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone Repository

```bash
git clone <repo-url>
cd AgenticAIChatbot
```

---

### 2️⃣ Create Virtual Environment

#### 🪟 Windows (PowerShell)

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

#### 🍎 macOS / 🐧 Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Configure API Keys

You can either:

* Enter API keys directly in the UI (recommended)
* OR set environment variables:

#### macOS / Linux

```bash
export GROQ_API_KEY=your_groq_key
export TAVILY_API_KEY=your_tavily_key
```

#### Windows (PowerShell)

```powershell
setx GROQ_API_KEY "your_groq_key"
setx TAVILY_API_KEY "your_tavily_key"
```

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

---

## 🧠 Use Cases

### 💬 Basic Chatbot

* Simple conversational AI using LLM
* Maintains chat flow using message state

---

### 🌐 Chatbot With Web

* Tool-enabled agent
* Uses Tavily Search for real-time data
* Supports dynamic tool calling via LangGraph

---

### 📰 AI News Pipeline

* Fetch latest AI news articles
* Summarize using LLM
* Save output as Markdown file (`/AINews/`)

---

## 📌 Future Enhancements

* 🔹 Add RAG (Vector Database: FAISS / Chroma)
* 🔹 Conversation Memory
* 🔹 Streaming responses for better UX
* 🔹 Multi-LLM support (OpenAI, Ollama)
* 🔹 Docker + Cloud Deployment (AWS / Render)

---

## 👨‍💻 Author

**Sunny Chouhan**

---

## ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub!
