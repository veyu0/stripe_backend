FROM python:3.11

ENV PYTHONUNBUFFERED 1

RUN mkdir /app

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "localhost:8000"]
