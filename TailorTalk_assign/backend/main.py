from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import process_input
import traceback

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserInput(BaseModel):
    text: str


@app.post("/message")
def message_endpoint(data: UserInput):
    try:
        reply = process_input(data.text)
        return {"reply": reply}
    except Exception as e:
        traceback.print_exc()
        return {"reply": f"⚠️ Internal Server Error: {str(e)}"}

