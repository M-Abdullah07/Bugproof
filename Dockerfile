FROM python:3.13-slim
WORKDIR /app
COPY requirements.lock pyproject.toml README.md ./
COPY src ./src
RUN pip install --no-cache-dir -r requirements.lock && pip install --no-cache-dir --no-deps .
RUN useradd --uid 10001 --create-home bugproof && mkdir /data && chown bugproof:bugproof /data
USER bugproof
ENV BUGPROOF_DATABASE_PATH=/data/bugproof.sqlite3 BUGPROOF_ENV=production
EXPOSE 8000
CMD ["python", "-m", "bugproof"]
