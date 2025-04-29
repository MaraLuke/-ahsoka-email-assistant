import imaplib, smtplib, email
from email.message import EmailMessage
from .settings import Settings

class EmailClient:
    def __init__(self, cfg: Settings):
        self.cfg = cfg

    def _imap_connect(self):
        conn = imaplib.IMAP4_SSL(self.cfg.imap_server)
        conn.login(self.cfg.email_user, self.cfg.email_pass)
        return conn

    def fetch(self, days: int = 3):
        mail = self._imap_connect()
        mail.select("inbox")
        # (přidejte logiku pro stahování a dekódování podobně jako dříve)
        mail.logout()
        return []

    def delete(self, uid: str):
        mail = self._imap_connect()
        mail.select("inbox")
        mail.store(uid, "+FLAGS", "\Deleted")
        mail.expunge()
        mail.logout()
        return {"status": "deleted", "uid": uid}

    def star(self, uid: str):
        mail = self._imap_connect()
        mail.select("inbox")
        mail.store(uid, "+FLAGS", "\Flagged")
        mail.logout()
        return {"status": "starred", "uid": uid}

    def reply(self, to_addr: str, subject: str, body: str):
        msg = EmailMessage()
        msg["From"] = self.cfg.email_user
        msg["To"] = to_addr
        msg["Subject"] = f"Re: {subject}"
        msg.set_content(body)
        with smtplib.SMTP_SSL(self.cfg.smtp_server, self.cfg.smtp_port) as s:
            s.login(self.cfg.email_user, self.cfg.email_pass)
            s.send_message(msg)
        return {"status": "sent"}
