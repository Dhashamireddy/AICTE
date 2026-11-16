# AICTE Assistive Portal
An AI-based system for simplifying the approval process for technical institutions.

> Academic assistance prototype. Not an official AICTE approval system.

## Run the backend
    cd backend
    python -m venv venv
    venv\Scripts\activate          # Windows   (Mac/Linux: source venv/bin/activate)
    pip install -r requirements.txt
    uvicorn app.main:app --reload --port 8000
API docs: http://localhost:8000/docs

## Run the frontend
    cd frontend
    npm install
    npm run dev
App: http://localhost:5173

## Run tests
    cd backend
    pytest
