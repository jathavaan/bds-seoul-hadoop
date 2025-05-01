FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files (code, configs)
COPY . .

# Default command can be overridden by docker-compose
CMD ["python3", "src/main.py"]
