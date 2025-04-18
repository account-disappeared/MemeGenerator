FROM python:3.13-slim
WORKDIR /app
COPY . .
RUN apt-get update && apt-get install -y \
    fonts-noto-cjk \
    && rm -rf /var/lib/apt/lists/*
RUN pip install -r requirements.txt
EXPOSE 8501
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health
ENTRYPOINT ["streamlit", "run", "meme.py", "--server.port=8501", "--server.address=0.0.0.0"]
