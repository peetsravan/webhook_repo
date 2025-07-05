# webhook_# GitHub Webhook Listener (Flask + MongoDB)

A simple Flask application to receive GitHub webhook events (Push, Pull Request, Merge) and store them in MongoDB. It also serves a minimal UI and REST API to view recent events.

---

## Features

- Accepts GitHub Webhook events: `push`, `pull_request (opened + merged)`
- Stores data in MongoDB (`push`, `pull_request`, `merge`)
- Provides a `/events` endpoint to view the latest 25 events
- Includes signature verification with GitHub secret

---

## Technologies

- Python (Flask)
- MongoDB
- PyMongo
- GitHub Webhooks
- dotenv (.env support)

---

## Setup Instructions

git clone https://github.com/peetsravan/webhook_repo.git
cd webhook_repo

# Create virtual environment
python -m venv my_env

# Activate it
# For Windows:
my_env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env


# Start the Flask server
python app.py

# Documentation

When we make change in action-repo like push,merge and raising pull request to main branch the events gets listed in /events end points
This project uses ngrok to expose your locally running Flask app (webhook-repo) to the internet so GitHub can deliver webhook events.

ngrok http 5000

Copy the https://*.ngrok-free.app URL and paste it as the Payload URL in your GitHub Webhook settings (e.g., https://your-tunnel.ngrok-free.app/webhook).


