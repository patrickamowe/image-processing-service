FROM python:3.11-slim

# make app the working dir
WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN touch __init__.py

CMD ["fastapi", "run", "main.py", "--port", "8000"]
