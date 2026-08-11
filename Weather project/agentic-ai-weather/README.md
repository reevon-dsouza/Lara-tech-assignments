# 🌤️ Agentic AI Weather

A simple Python agent that fetches **real-time weather data** from the [Open-Meteo API](https://open-meteo.com/) and makes a basic decision based on the current temperature.

> No API key required — Open-Meteo is free and open-source!

---

## 📁 Project Structure

```
agentic-ai-weather/
│
├── src/
│   └── agent.py          # Main agent script
│
├── logs/
│   └── agent.log         # Auto-generated log file
│
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/agentic-ai-weather.git
cd agentic-ai-weather
```

### 2. Create a virtual environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the agent

```bash
python src/agent.py
```

---

## 📋 Sample Output

```
2026-08-07 13:30:00 | INFO     | Agent started.
2026-08-07 13:30:00 | INFO     | Fetching weather data from Open-Meteo API...
2026-08-07 13:30:01 | INFO     | Weather fetched successfully!
2026-08-07 13:30:01 | INFO     | Decision: It's hot outside.
2026-08-07 13:30:01 | INFO     | Agent stopped.

🌡️  Temperature : 32.5 °C
💨  Wind Speed  : 12.3 km/h

🤖  Agent says  : It's hot outside.
```

---

## ⚙️ Configuration

By default the agent fetches weather for **New Delhi, India** (`28.6139°N, 77.2090°E`).

To change the location, edit the coordinates in `src/agent.py`:

```python
DEFAULT_LATITUDE = 28.6139
DEFAULT_LONGITUDE = 77.2090
```

---

## 🧠 Decision Logic

| Temperature       | Agent Response          |
| ------------------ | ----------------------- |
| Below 10 °C       | It's cold outside.      |
| 10 °C – 25 °C     | Weather is pleasant.    |
| Above 25 °C       | It's hot outside.       |

---

## 📝 Logging

All activity is logged to **both** the console and `logs/agent.log`. Events recorded include:

- Agent started / stopped
- Weather fetch attempts
- Successful data retrieval
- Decisions made
- Errors (network failures, invalid responses, etc.)

---

## 📦 Dependencies

- [requests](https://pypi.org/project/requests/) — HTTP library for API calls

---

## 📄 License

This project is open-source and available under the [MIT License](https://opensource.org/licenses/MIT).
