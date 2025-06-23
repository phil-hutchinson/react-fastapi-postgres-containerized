# Dockerfile for FastAPI backend
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
# Install debugpy for remote debugging
RUN pip install debugpy
COPY . .
EXPOSE 8000 5678
# CMD for debugging: waits for debugger to attach before starting FastAPI
# CMD ["python", "-m", "debugpy", "--listen", "0.0.0.0:5678", "--wait-for-client", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# CMD for normal development: starts FastAPI immediately, debugger can attach any time
CMD ["python", "-m", "debugpy", "--listen", "0.0.0.0:5678", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
