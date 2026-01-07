

# 📧 Email Analyzer – AI Calendar Automation

An AI-powered system that reads emails, understands deadlines and events, and automatically creates Google Calendar entries — so important things never get forgotten again.

This project was inspired by a simple real-life problem:
receiving important college emails (like expert lectures or deadlines), planning to attend… and then forgetting about them later.

---

## 🚀 What this project does

The system:

* Extracts **events, deadlines, and urgency** from emails using an LLM
* Resolves **relative dates** like:

  * *tomorrow*
  * *this Saturday*
  * *next Monday*
* Applies **safe default times** when time isn’t mentioned
* Handles **deadline logic** (start + end events)
* Detects **expired deadlines** before adding to calendar
* Automatically creates events in **Google Calendar**

---

## 🧠 System Architecture

```
Email Text
   ↓
LLM (understanding & extraction)
   ↓
Python Datetime Normalization
   ↓
Validation & Safety Checks
   ↓
Google Calendar API
   ↓
Event Created 🎉
```

---

## ✨ Key Features

* **Urgency Classification**
  Categorizes emails as *high / moderate / low* urgency.

* **Robust Time Handling**

  * Supports absolute and relative dates
  * Applies defaults when time is missing
  * Prevents invalid events

* **Deadline-Aware Logic**

  * Creates proper start & end events
  * Avoids duplicate or conflicting entries

* **Production-Safe Design**

  * Defensive validation
  * Clear separation of concerns
  * Ready for scaling

---

## 🛠️ Tech Stack

* **Python**
* **LangChain**
* **HuggingFace LLM APIs**
* **Pydantic**
* **Google Calendar API**
* **Datetime Normalization**
* **OAuth 2.0**

---

## 📂 Project Structure

```
Email_Analyzer/
├── main.py                  # Orchestrates the pipeline
├── llm.py                   # LLM extraction & urgency classification
├── datetime_normalizer.py   # Time normalization & defaults
├── google_auth.py           # OAuth handling
├── calendar_service.py      # Google Calendar service builder
├── calendar_events.py       # Event creation logic
├── calendar_utils.py        # Helper utilities
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository

```bash
git clone <your-repo-url>
cd Email_Analyzer
```

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Set up environment variables

Create a `.env` file:

```
HUGGINGFACE_API_KEY=your_api_key_here
```

### 4️⃣ Google Calendar API setup

1. Enable **Google Calendar API** in Google Cloud Console
2. Create **OAuth Client (Desktop App)**
3. Download `client_secret.json`
4. Place it in the project root
5. Run the app once to generate `token.json`

> ⚠️ Do not commit `client_secret.json` or `token.json` to GitHub.

---

## ▶️ Running the project

```bash
python main.py
```

The system will:

* Analyze the email
* Extract events
* Normalize dates & times
* Validate deadlines
* Add valid events to Google Calendar

---

## 🔮 Future Work

I’m currently learning **LangGraph** and extending this project into a **full-scale AI agent system**, including:

* 📥 Email Reader Agent
* 🧠 Understanding Agent
* 📅 Calendar Agent
* 📝 Summarizer Agent
* 🤖 Auto-Reply Agent
* 🛡️ Safety/Policy Agent
* 🎯 User Preference Agent

This project naturally fits a **multi-agent architecture** using:

* LangGraph
* AutoGen
* CrewAI
* Haystack Agents

---

## 🌱 What I learned

This project taught me that:

> The best ideas don’t come from big problems —
> they come from small everyday frustrations.

Turning a simple habit of forgetting important emails into an end-to-end AI automation system has been one of my most valuable learning experiences.

---

## 📬 Connect

If you’re interested in:

* AI agents
* LLM automation
* Calendar intelligence
* LangGraph workflows

Let’s connect and build smarter systems together 🚀



>>>>>>> 120d79b (Initial commit:Smart Email Scheduler)
