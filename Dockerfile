FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY email_assistant/ ./email_assistant/
CMD ["uvicorn", "email_assistant.api:app", "--host", "0.0.0.0", "--port", "80"]
