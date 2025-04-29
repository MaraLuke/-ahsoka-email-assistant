from pydantic import BaseModel

class EmailOut(BaseModel):
    uid: str
    from_address: str
    subject: str
    date: str
    body: str

class ReplyIn(BaseModel):
    reply_text: str
