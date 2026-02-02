# AquaMind: Water Cleaning Robot Dashboard & Vision Service

This repository contains the full stack for the AquaMind project, including the AI-powered vision service and the real-time monitoring dashboard.

## Project Structure
- **/backend**: Python-based vision service using YOLO and Ollama.
- **/dashboard**: React+Vite frontend for monitoring and AI advice.

## Getting Started on a New Device

### 1. Prerequisites
- [Python 3.10+](https://www.python.org/downloads/)
- [Node.js](https://nodejs.org/)
- [Ollama](https://ollama.com/) (for AI Advisor)

### 2. Backend Setup
```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### 3. Frontend Setup
```powershell
cd dashboard
npm install
npm run dev
```

### 4. AI Advisor Setup
Ensure Ollama is running and you have the model downloaded:
```powershell
ollama pull llama3
```

## Features
- AI-driven object detection in water.
- Real-time statistics and alerts.
- Scientific AI Advisor powered by Llama 3.
