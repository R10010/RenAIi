from fastapi import FastAPI, HTTPException, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
import json
import os
import joblib
import pandas as pd

from .avatar_3d import Emotional3DAvatar

app = FastAPI(title="RenAI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize avatar
avatar = Emotional3DAvatar()

# Churn model variable
churn_model = None


# Load churn model when server starts
@app.on_event("startup")
async def load_churn_model():
    global churn_model
    model_path = "ml_pipeline/models/churn/model.pkl"

    if os.path.exists(model_path):
        churn_model = joblib.load(model_path)
        print("Churn model loaded successfully")
    else:
        print("Churn model not found")


# ---------------------------
# Request Schemas
# ---------------------------


class ChatRequest(BaseModel):
    text: str
    user_id: str = "guest"


class ChurnRequest(BaseModel):
    features: dict


# ---------------------------
# Chat Endpoint
# ---------------------------


@app.post("/api/chat")
async def chat_endpoint(req: ChatRequest):
    avatar_state = avatar.process_speech(req.text)

    return {"message": f"Echo: {req.text}", "avatar": avatar_state}


# ---------------------------
# Churn Prediction Endpoint
# ---------------------------


@app.post("/api/predict/churn")
async def predict_churn(req: ChurnRequest):

    if churn_model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")

    # Convert request features to dataframe
    df = pd.DataFrame([req.features])

    # Predict probability
    proba = churn_model.predict_proba(df)[0][1]

    return {"churn_probability": float(proba)}


# ---------------------------
# Avatar WebSocket
# ---------------------------


@app.websocket("/ws/avatar")
async def websocket_endpoint(websocket: WebSocket):

    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_json()
            text = data.get("text", "")

            avatar_state = avatar.process_speech(text)

            await websocket.send_json(avatar_state)

    except:
        pass


# ---------------------------
# Health Check
# ---------------------------


@app.get("/health")
async def health():
    return {"status": "ok"}
