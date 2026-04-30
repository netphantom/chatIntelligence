# 💬 Self-Hosted Chat Intelligence

A modern self-hosted and open source analytics platform that transforms any chat export into behavioral, temporal, and content-based insights.

No platform dependency. Works with any structured chat JSON export.
![img.png](img.png)
---

## 🚀 Features

- 📊 Behavioral analysis (dominance, engagement)
- ⏱️ Temporal patterns (weekly/monthly trends)
- 🔥 Anomaly detection
- 🧠 Word & content frequency analysis
- 📈 Moving averages & periodicity detection
- 🎯 Interactive visual analytics

---

## 🧱 Architecture

- Streamlit frontend (single-page flow)
- Strategy-based analytics engine
- Modular chart system
- Lazy-loaded data pipeline
- Cached parsing layer

---

## 📦 Installation (local)

### 1. Install uv
```bash
curl -Ls https://astral.sh/uv/install.sh | sh
```
### 2. Install dependencies
```bash
uv sync
```
### 3. Run app
```bash
uv run streamlit run app.py
```

## 🐳 Docker
```bash
docker build -t conversation-intelligence .
```
```bash
docker run -p 8501:8501 conversation-intelligence
```

## 📁 Project structure
```
.
├── app.py
├── controller/
│   └── TelegramParser.py
├── view/
│   ├── DashboardApp.py
│   └── charts/
│       ├── strategies...
├── pyproject.toml
├── Dockerfile
└── .github/workflows/
```
## ⚙️ Configuration

No environment variables required by default.

Optional:

* logging level
* cache tuning (future)

## 🧠 Design principles
* Strategy pattern for analytics modules
* Separation between UI and computation
* Stateless execution model
* Cached dataset parsing

## 📌 Future improvements
* AI-generated summaries per section
* Export to PDF report
* Streaming analysis (real-time ingestion)
* Multi-chat comparison mode

## 📜 License

MIT