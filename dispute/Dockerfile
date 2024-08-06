# Use the official Python image from the Docker Hub
FROM python:3.10-slim-bullseye

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    libopenblas-dev \
    python3-dev \
    cmake \
    git \
    curl \
    && apt-get clean

RUN pip install --upgrade pip

WORKDIR /usr/src/app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Specify the command to run on container start

# Set the environment variable
ARG LLM_API_KEY
ENV LLM_API_KEY=${LLM_API_KEY}
# print
RUN echo "----------"
RUN echo $LLM_API_KEY
RUN if [ "$LLM_API_KEY" = "ollama" ]; then python3 verify_ollama.py; fi

CMD ["python", "main.py"]