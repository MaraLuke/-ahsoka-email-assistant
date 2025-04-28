import os
import imaplib, smtplib, email
from email.header import decode_header
from email.message import EmailMessage
import datetime

IMAP_SERVER = "imap.seznam.cz"
SMTP_SERVER = "smtp.seznam.cz"
USERNAME = os.getenv("EMAIL_USER")
PASSWORD = os.getenv("EMAIL_PASS")

def fetch_emails(days=3):
    messages = []
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(USERNAME, PASSWORD)
        mail.select("inbox")

        date = (datetime.date.today() - datetime.timedelta(days=days)).strftime("%d-%b-%Y")
        status, data = mail.search(None, f'(SINCE "{date}")')

        if status != "OK" or not data or not data[0]:
            print("📭 Žádné nové e-maily nenalezeny.")
            mail.logout()
            return []

        for num in data[0].split():
            status, msg_data = mail.fetch(num, "(RFC822)")
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)

            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding or "utf-8", errors="ignore")

            from_ = msg.get("From")
            date_ = msg.get("Date")

            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    if content_type == "text/plain":
                        body = part.get_payload(decode=True).decode(errors="ignore")
                        break
                else:
                    body = ""
            else:
                body = msg.get_payload(decode=True).decode(errors="ignore")

            messages.append({
                "uid": num.decode(),
                "from": from_,
                "subject": subject,
                "date": date_,
                "body": body[:1000]  # Omezit délku textu
            })

        mail.logout()
        return messages
    except Exception as e:
        return {"error": str(e)}

def delete_email(uid):
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(USERNAME, PASSWORD)
        mail.select("inbox")
        mail.store(uid, "+FLAGS", "\\Deleted")
        mail.expunge()
        mail.logout()
        return {"status": "deleted", "uid": uid}
    except Exception as e:
        return {"error": str(e)}

def star_email(uid):
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(USERNAME, PASSWORD)
        mail.select("inbox")
        mail.store(uid, "+FLAGS", "\\Flagged")
        mail.logout()
        return {"status": "starred", "uid": uid}
    except Exception as e:
        return {"error": str(e)}

def send_reply(uid, reply_text):
    try:
        msg = EmailMessage()
        msg.set_content(reply_text)
        msg["Subject"] = "Re: automatická odpověď"
        msg["From"] = USERNAME
        msg["To"] = "ZDE_ZADEJ_ADRESÁTA"  # POZOR: stále nutné dynamicky doplnit adresáta!

        with smtplib.SMTP_SSL(SMTP_SERVER, 465) as server:
            server.login(USERNAME, PASSWORD)
            server.send_message(msg)

        return {"status": "replied", "uid": uid}
    except Exception as e:
        return {"error": str(e)}
