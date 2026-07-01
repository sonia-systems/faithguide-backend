# FaithGuide AI 🌟 - Virtual Youth Mentor

**FaithGuide AI** is a virtual mentorship assistant tailored for teenagers and young adults within a Salesian Oratory. It adopts a youthful, dynamic, and empathetic tone to provide guidance rooted in human and Christian values, offering support without judgment while fostering hope and motivation.

This full-stack project features a lightweight **Flask Backend** that orchestrates real-time conversational memory via sessions, connected natively to the **Google Gemini 2.5 Flash API**, paired with a modern, responsive **Web Frontend** fully optimized for mobile devices.

---

## 🚀 Key Features

- **Empathetic AI with Session Memory:** Leverages native history tracking mapped to unique `session_id` tokens, allowing the assistant to recall crucial user context (name, age, shared challenges) across messages.
- **Enhanced Reading UX:** Implementation of a silent text-rendering container, freezing the view so users can scroll and read long responses at their own pace without annoying screen jumps.
- **Secure & Dependency-Free Architecture:** Uses pure HTTP calls instead of heavy vendor SDKs, bypassing binary execution restrictions on secure enterprise environments.

---

## 🛠️ Tech Stack

- **Backend:** Python 3.x, Flask, Requests.
- **AI Engine:** Google Gemini 2.5 Flash API.
- **Frontend:** HTML5, CSS3 (Google Fonts), Asynchronous JavaScript (Fetch API).
- **Version Control:** Git & GitHub.

---

## 📦 Installation & Local Setup

Follow these steps to run the project locally:

### 1. Clone the repository
```bash
git clone [https://github.com/sonia-systems/faithguide-backend.git](https://github.com/sonia-systems/faithguide-backend.git)
cd faithguide-backend

2. Create and activate a Virtual Environment
On Windows (PowerShell):
python -m venv venv
.\venv\Scripts\Activate.ps1

3. Install dependencies
pip install flask requests

4. Configure Environment Variables (API Key)
For security compliance, the Gemini API key is never hardcoded. You must load it into your current terminal session prior to booting the server:
$env:GEMINI_API_KEY="YOUR_GEMINI_API_KEY_HERE"

5. Launch the application
python main.py
The web server will spin up at: http://localhost:8000/

📂 Project Structure
faithguide-backend/
├── main.py            # Flask server & native integration with Gemini API
├── static/
│   ├── app.js         # Frontend handling, chat session tracking & async Fetch API
│   └── style.css      # Chat interface layout and custom responsive styling
└── templates/
    └── index.html     # User Interface (UI) structure

🛡️ Security Architecture Note (WDAC/AppLocker)
This project was intentionally engineered to use direct HTTP requests via Python's standard requests library. This design choice completely bypasses software restriction policies—such as Windows Defender Application Control (WDAC)—which frequently flag or block pre-compiled C-binary files (_pydantic_core) standard in most third-party AI frameworks.