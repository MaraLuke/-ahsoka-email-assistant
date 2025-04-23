from fastapi import FastAPI
from app.mail import fetch_emails, delete_email, star_email, send_reply
from pydantic import BaseModel

app = FastAPI()

class ReplyInput(BaseModel):
    reply_text: str

@app.get("/emails")
def get_emails(days: int = 3):
    return fetch_emails(days)

@app.post("/email/{uid}/reply")
def reply_email(uid: str, body: ReplyInput):
    return send_reply(uid, body.reply_text)

@app.post("/email/{uid}/star")
def star(uid: str):
    return star_email(uid)

@app.delete("/email/{uid}")
def delete(uid: str):
    return delete_email(uid)