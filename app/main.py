from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Message(BaseModel):
    user_id: str
    text: str

@app.post("/message")
async def send_message(msg: Message):
    # Placeholder response - echo message
    return {"reply": f"You said: {msg.text}"}
