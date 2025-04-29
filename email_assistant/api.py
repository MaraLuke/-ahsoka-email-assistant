from fastapi import FastAPI, Depends, HTTPException
from .client import EmailClient
from .settings import Settings
from .schemas import EmailOut, ReplyIn

app = FastAPI(title="Seznam Email Assistant")

def get_client(cfg: Settings = Depends(Settings)):
    return EmailClient(cfg)

@app.get("/emails", response_model=list[EmailOut])
def list_emails(days: int = 3, client: EmailClient = Depends(get_client)):
    return client.fetch(days)

@app.delete("/emails/{uid}")
def delete_email(uid: str, client: EmailClient = Depends(get_client)):
    return client.delete(uid)

@app.post("/emails/{uid}/star")
def star_email(uid: str, client: EmailClient = Depends(get_client)):
    return client.star(uid)

@app.post("/emails/{uid}/reply", response_model=dict)
def reply_email(uid: str, body: ReplyIn, client: EmailClient = Depends(get_client)):
    mails = client.fetch(days=30)
    msg = next((m for m in mails if m.get('uid') == uid), None)
    if not msg:
        raise HTTPException(404, "Email not found")
    return client.reply(msg.get('from_address'), msg.get('subject'), body.reply_text)
