FROM python:3.11.1-slim-buster

COPY . /app

WORKDIR /app

RUN pip install --upgrade pip && pip install -r requirements.txt


CMD ["python", "database/setup.py"]

CMD ["python", "app.py"]