FROM python:3.7-buster

WORKDIR /opt/code
COPY setup.py yamgal app.py ./
RUN pip install -e .

ENV PORT 8080

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app
