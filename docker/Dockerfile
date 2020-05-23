FROM python:3.7-buster

WORKDIR /opt/code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

ENV PORT 8080

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app
