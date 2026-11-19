# Build z katalogu głównego projektu:
#   docker build -f altium_odbc/Dockerfile -t altium-odbc .
FROM python:3.12-slim

WORKDIR /app
ENV PYTHONUNBUFFERED=1

COPY odbc/requirements.txt /app/odbc/requirements.txt
RUN pip install --no-cache-dir -r /app/odbc/requirements.txt

COPY backend /app/backend
COPY odbc /app/odbc

EXPOSE 5433
CMD ["python", "odbc/main.py"]