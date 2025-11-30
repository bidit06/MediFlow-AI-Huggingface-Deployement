
---

# MediFlow AI — Hugging Face Spaces Deployment Documentation

MediFlow AI is a **context-aware medical triage assistant** built using **Google ADK Agents**, deployed on **Hugging Face Spaces** using **Gradio** as the frontend interface.

The system uses **LLM-powered agents**, **tool-calling**, **session management**, and **Google Search integration** to assist users with symptom intake, context enrichment, condition estimation, and doctor lookup.

This documentation explains:

* The directory structure of the deployed project
* What each file does
* How the deployment architecture works
* How Gradio, sessions, and agents interact
* How to reproduce the deployment from scratch

### MediFlow AI is deployed at: https://huggingface.co/spaces/bidit06/mediflow_ai
Go and Use it

---

## 🗂 1. Project Structure

```
mediflow_ai/
│
├── .gitattributes           # Git LFS configuration (if needed)
├── README.md                # everything about project
├── __init__.py              # Package initializer
├── agent.py                 # Core agent setup (Tara + Search Agent)
├── app.py                   # Gradio interface & session handling
├── requirements.txt         # Python dependencies
```

### 📌 Overview

Your project contains two key modules:

1. **`agent.py`** → *Defines all ADK Agents:*

   * Triage Agent (“Tara”)
   * Google Search Agent (“Silent Librarian”)
   * Runner factory
   * SessionService setup

2. **`app.py`** → *Hugging Face Entrypoint:*

   * Launches Gradio chat UI
   * Handles per-visitor sessions
   * Sends user messages to agents
   * Receives final LLM output

---

## 🤖 2. Explanation of Each File

### 🧩 `agent.py` — Core Agent Architecture

This file defines:

### ✔️ Two LLM Agents

#### 1. `triage_doctor_finder_agent` (Tara)

* Main conversational agent
* Performs symptom interview and iterative intake
* Enriches context using Google Search
* Generates triage reasoning and condition estimation
* Produces final medical triage report

#### 2. `google_search_agent` (Silent Librarian)

* Performs only factual lookup
* Never diagnoses
* Fetches:

  * Weather
  * AQI
  * Local outbreaks
  * Symptom medical causes
  * Home remedies
  * Nearby doctors

### ✔️ Custom Tools Used

* **Google Search Tool** → For real-time facts
* **preload_memory** → Used in ADK sandbox/local, not used on Hugging Face

### ✔️ Session Service

* **InMemorySessionService** → For per-session context
* Used on Hugging Face (no SQLite storage here)

### ✔️ Runner Factory

`make_runner_for()` creates async runners for any agent.

---

## 🖥 `app.py` — Hugging Face Runtime

This file contains the entire runtime logic.

### ✔️ Per-Visitor Session Management

Each new user gets a unique:

```
session-<UUID>
```

Stored as a **hidden marker** in Gradio chat history.

This allows:

* User-specific context
* Independent triage flows
* No database required

### ✔️ Async Agent Execution

`_send_and_get_final_response_async()`:

* Sends the message
* Iterates event stream
* Returns only the *final* response

### ✔️ Gradio Chat Interface

```python
gr.ChatInterface(fn=chat_fn, title="MediFlow Agent")
```

### ✔️ Supported Interaction Modes

* 🌐 Hugging Face Web UI
* 💻 CLI Mode (local only)
* 🧪 Local notebook testing
* 🛠 ADK Web Sandbox

> **Note:** On Hugging Face, **no SQLite storage** is used.

---

## 📦 `requirements.txt`

Contains required dependencies, including:

* `gradio>=5`
* Google ADK / Generative AI dependencies
* `asyncio`

Ensures identical environment across local and HF deployments.

---

## 🧱 3. Deployment Architecture (HF → Agents → Tools)

### 📡 End-to-End Data Flow

1. User sends a message via Gradio UI
2. `app.py` receives text
3. Session ID is created or restored
4. Message passed to triage agent runner
5. Triage agent may call Google Search agent
6. Search agent calls the Google Search tool
7. Factual results are returned
8. Triage agent processes everything
9. Final answer displayed in UI

---

## 🔁 4. How to Reproduce This Deployment on Hugging Face Spaces

A clear step-by-step guide for anyone replicating your deployment.

### STEP 1 — Create a New Space

Go to:
👉 **[https://huggingface.co/new-space](https://huggingface.co/new-space)**

Choose:

* SDK: **Python**
* Hardware: **CPU Basic**
* Visibility: Public/Private
* Name: `mediflow_ai` # you can name it anything

---

### STEP 2 — Upload All Files

Upload:

✔ `agent.py`
✔ `app.py`
✔ `__init__.py`
✔ `requirements.txt`
✔ `.gitattributes`
✔ `README.md` (optional)

Maintain folder structure exactly.

---

### STEP 3 — Add Environment Variables

Go to:

**Settings → Variables & Secrets**

Add:

```
GOOGLE_API_KEY = <your-key>
GOOGLE_GENAI_MODEL = gemini-2.0-flash-lite
```

---

### STEP 4 — Space Will Auto-Build

Hugging Face will:

1. Install dependencies
2. Create environment
3. Run `app.py`
4. Deploy app publicly

---

### STEP 5 — Test the Deployment

Test that:

* Agents respond correctly
* Google Search tool works
* Session IDs persist
* Multiple users do not mix conversations

---
## 🌟 A Final Word by Bidit: Bridging the Gap

MediFlow AI was born from a simple belief: **Healthcare guidance should be accessible to everyone, everywhere.**

In a world where millions lack immediate access to medical advice, AI has the potential to be a bridge—not to replace doctors, but to guide patients safely until they can reach professional help. 

This project is a step towards that future: transparent, empathetic, and safe.

### 🙏 Acknowledgments
This project stands on the shoulders of giants. A heartfelt thank you to:
* **Google ADK:** For the powerful Gemini models and the Agent Development Kit (ADK) that serve as the brain of this system.
* **Hugging Face:** For democratizing AI deployment and making it easy to share ideas with the world.
* **Me:** For taking the time to explore this code. If this project inspired you, please consider giving it a ⭐ Star!

Don't Forget to Explore my Github Profile!



