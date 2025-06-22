# AI-Powered Food Ordering Chatbot

Welcome to the **AI-Powered Food Ordering Chatbot** repository! This project leverages Dialogflow, FastAPI, and MySQL (hosted on Aiven) to create a seamless conversational food ordering experience. The backend is deployed on Render, and the chatbot is integrated into a static website.

---


> Visit Live Chatbot Website : (https://foodbot-frontend-ujcj.onrender.com/)

## Table of Contents

* [Features](#features)
* [Architecture](#architecture)
* [Technologies Used](#technologies-used)
* [Getting Started](#getting-started)

  * [Prerequisites](#prerequisites)
  * [Clone the Repository](#clone-the-repository)
  * [Install Dependencies](#install-dependencies)
  * [Environment Variables](#environment-variables)
  * [Local Development](#local-development)
* [Testing](#testing)
* [Deployment](#deployment)

  * [Database Migration](#database-migration)
  * [Deploy Backend to Render](#deploy-backend-to-render)
  * [Deploy Frontend to Render](#deploy-frontend-to-render)
* [Usage](#usage)
* [Troubleshooting](#troubleshooting)
* [Contributing](#contributing)
* [License](#license)

---

## Features

* Natural language conversation via Dialogflow
* Place, track, and cancel orders through chat
* Persistent order data in Aiven-hosted MySQL
* FastAPI webhook handles business logic
* Integration with Dialogflow Messenger on the frontend
* Secure deployment on Render with SSL

---

## Architecture

```text
[User]
   ⇩ interacts via Dialogflow Messenger (web widget)
[Dialogflow]
   ⇩ sends webhook requests to FastAPI
[FastAPI]
   ⇩ processes intents & parameters
   ⇩ calls db_helper (MySQL connector)
[Aiven MySQL]
   ⇩ stores orders and tracking states
[FastAPI]
   ⇩ responds with fulfillmentText
[Dialogflow]
   ⇩ displays response to user
```

---

## Technologies Used

* **Dialogflow**: Intent detection, slot filling, fulfillment
* **FastAPI**: Webhook service
* **MySQL** (via `mysql-connector-python`): Persistent storage
* **Aiven**: Managed MySQL database
* **Render**: Hosting for backend and frontend
* **Cloudflare Tunnel**: Local development testing
* **HTML/CSS/JavaScript**: Frontend static site with embedded chatbot
* **python-dotenv**: Environment variable management

---

## Getting Started

### Prerequisites

* Python 3.10+
* Git
* Aiven MySQL account (free tier)
* Render account (free tier)

### Clone the Repository

```bash
git clone https://github.com/S1nen/Food-Chatbot.git
cd Food-Chatbot/backend
```

### Install Dependencies

```bash
python -m venv venv
source venv/bin/activate    # Linux/macOS
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in `backend/`:

```env
MYSQLHOST=<Aiven host>
MYSQLUSER=<Aiven user>
MYSQLPASSWORD=<Aiven password>
MYSQLDATABASE=pandeyji_eatery
MYSQLPORT=<Aiven port>
# If using bundled certs folder:
# SSL certificate path inside container
MYSQLSSLCA=certs/ca.pem
```

Ensure `.env` is in `.gitignore`.

### Local Development

1. **Run MySQL locally** (optional) or use Aiven credentials.
2. **Start FastAPI**:

   ```bash
   cd backend
   uvicorn main:app --reload
   ```
3. **Expose via Cloudflare Tunnel** (for Dialogflow testing):

   ```bash
   cloudflared tunnel --url http://localhost:8000
   ```
4. **Configure Dialogflow webhook** to the tunnel URL.
5. **Interact** with your chatbot in Dialogflow test console.

---

## Testing

### End-to-End with curl

```bash
curl -X POST http://localhost:8000/ \
     -H "Content-Type: application/json" \
     --data '{"queryResult":{"intent":{"displayName":"Track Order-context:ongoing-order"},"parameters":{"number":123},"outputContexts":[{"name":".../contexts/ongoing-order"}]}}'
```

### Unit Testing Handlers

You can write pytest tests for individual functions in `main.py`:

```python
from backend.main import track_order

def test_track_order_missing():
    resp = track_order({"number":None}, "session1")
    assert b"valid order-id" in resp.body
```

---

## Deployment

### Database Migration

1. **Export local DB** (Workbench or `mysqldump --routines`).
2. **Create schema** `pandeyji_eatery` in Aiven (Workbench).
3. **Import dump.sql** into Aiven via Workbench or CLI with `ssl-ca`.

### Deploy Backend to Render

1. Push `main.py`, `db_helper.py`, `requirements.txt`, `certs/ca.pem` to GitHub.
2. In Render → **New Web Service**:

   * GitHub repo: `Food-Chatbot`
   * Start Command: `uvicorn backend.main:app --host 0.0.0.0 --port 10000`
   * Environment Variables: match your `.env`
3. Deploy and verify logs (`✅ Connected to Aiven MySQL`).

### Deploy Frontend to Render

1. Push `frontend/` folder containing `index.html` and `style.css`.
2. In Render → **New Static Site**:

   * Root Directory: `frontend`
   * Publish Directory: `./`
3. Deploy and get the static URL.

---

## Usage

1. Open frontend URL.
2. Click chatbot icon and converse naturally:

   * "I want two pizzas and one mango lassi"
   * "Track order 123"
3. Observe real-time fulfillment responses.

---

## Troubleshooting

* **500 Errors**: Check Render logs, ensure env vars are correct.
* **SSL Issues**: Verify `ssl_ca` path and certificate.
* **Cloudflare Tunnel**: Ensure tunnel is running and webhook URL is updated.

---

## Contributing

1. Fork this repo.
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m "Add feature..."`
4. Push to branch: `git push origin feature/my-feature`
5. Open a Pull Request.

---

## License

© 2025 Sinan Ak. All rights reserved.

This project is strictly for educational and personal portfolio use only.
Unauthorized use, copying, or redistribution of any part of this codebase
or design without explicit permission is strictly prohibited.

