FROM python:3.12-slim


WORKDIR /app

# зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# код приложения
COPY app ./app

# по умолчанию запускаем main
CMD ["python", "-m", "app.main"]
