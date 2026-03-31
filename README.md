# 📄 PDF RAG Production App

A production-ready Retrieval-Augmented Generation (RAG) application built to ingest, chunk, embed, and query PDF documents.

This project uses **FastAPI** for the web server, **Inngest** for durable, event-driven background workflows (handling rate limits and retries), **Qdrant** for vector storage, and **OpenAI (GPT-4o-mini)** for embeddings and intelligent question answering.

---

## 🚀 Features

- **Event-Driven PDF Ingestion:** Upload and process large PDFs in the background without blocking the main API thread.
- **Durable Workflows:** Built-in step tracking, throttling, and rate-limiting powered by Inngest.
- **Semantic Search:** Fast and accurate context retrieval using Qdrant Vector Database.
- **LLM Integration:** AI-powered answers grounded _strictly_ in the provided document context using the Inngest Experimental AI adapter and OpenAI.
- **Source Tracking:** Every answer returns the exact source documents and text chunks used to generate the response.

---

## 🛠️ Architecture & Tech Stack

- **Framework:** [FastAPI](https://fastapi.tiangolo.com/) (Python)
- **Workflow Engine:** [Inngest](https://www.inngest.com/) (Serverless event-driven queues)
- **Vector Database:** [Qdrant](https://qdrant.tech/) (Local or Cloud)
- **LLM / Embeddings:** [OpenAI API](https://openai.com/) (GPT-4o-mini)
- **Environment:** `python-dotenv` for configuration

---

## 📂 Project Structure

```text
pdfrag_ragproductionapp/
├── main.py             # FastAPI entry point & Inngest function definitions
├── vector_db.py        # Qdrant client wrapper (QdrantStorage)
├── data_loader.py      # PDF parsing, chunking, and embedding logic
├── custom_types.py     # Pydantic data models for structured type hinting
├── .env                # Environment variables (Not committed to version control) .env.sample change it to .env and put your OPENAi api key
└── requirements.txt    # Python dependencies
```

---

## ⚙️ Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.9+**
- **Qdrant Server:** Running locally via Docker (`http://localhost:6333`) or Qdrant Cloud.
- **Inngest Dev Server:** For local testing (`npx inngest-cli@latest dev`).

---

## 💻 Installation

**1. Clone the repository:**

```bash
git clone [https://github.com/mesailesh7/pdfrag_ragproductionapp.git](https://github.com/mesailesh7/pdfrag_ragproductionapp.git)
cd pdfrag_ragproductionapp
```

**2. Create and activate a virtual environment:**

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

**3. Install dependencies:**

```bash
pip install -r requirements.txt
```

---

## 🔑 Configuration

Create a `.env` file in the root directory and add your necessary API keys and configuration variables:

```env
# OpenAI API
OPENAI_API_KEY=your_openai_api_key_here

# Environment
NODE_ENV=development # Set to 'production' when deploying

# Optional: Qdrant Cloud URL (defaults to localhost:6333 in code if not set)
# QDRANT_URL=your_qdrant_cloud_url
# QDRANT_API_KEY=your_qdrant_api_key
```

---

## 🚀 Usage & Running Locally

To run the application locally, you need three terminals open to run the Vector DB, the FastAPI server, and the Inngest Dev Server.

### Step 1: Start Qdrant (via Docker)

If you are running Qdrant locally, spin it up using Docker:

```bash
docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant
```

### Step 2: Start the FastAPI App

Run your web server using Uvicorn:

```bash
uvicorn main:app --reload --port 8000
```

_Your app is now running at `http://localhost:8000`. The Inngest API endpoint is mounted at `/api/inngest`._

### Step 3: Start the Inngest Dev Server

Start the local Inngest dashboard to trigger and monitor events:

```bash
npx inngest-cli@latest dev -u http://localhost:8000/api/inngest
```

_Open `http://localhost:8288` in your browser to view the Inngest Dashboard._

---

## 📡 Triggering Events

Because this app is event-driven, you execute workflows by sending events to Inngest. You can do this via the Inngest local dashboard or by adding a FastAPI route that sends the event.

### 1. Ingesting a PDF

Send the `rag/ingest_pdf` event with the following JSON payload:

```json
{
  "name": "rag/ingest_pdf",
  "data": {
    "pdf_path": "/path/to/your/document.pdf",
    "source_id": "unique-doc-id-123"
  }
}
```

_This triggers the background worker to load, chunk, embed, and upsert the PDF to Qdrant._

### 2. Querying the AI

Send the `rag/query_pdf_ai` event to ask a question based on your uploaded docs:

```json
{
  "name": "rag/query_pdf_ai",
  "data": {
    "question": "What is the main topic of the document?",
    "top_k": 5
  }
}
```

_The worker will embed your question, search Qdrant for the top 5 most relevant chunks, and use GPT-4o-mini to return a concise answer along with the sources._

---

## ⚠️ Troubleshooting

- **`AttributeError: 'QdrantClient' object has no attribute 'search'`**: This means you are using a newer version of the `qdrant-client`. Ensure your `vector_db.py` is updated to use the `.query_points()` API instead of the deprecated `.search()` method.
- **Inngest Connection Issues**: Ensure the Inngest CLI is pointing to the correct local port (default is usually `8000` for FastAPI). Check that `is_production=False` is set in your `inngest.Inngest` client initialization during local development.

---

_Built with FastAPI, Qdrant, and Inngest._
