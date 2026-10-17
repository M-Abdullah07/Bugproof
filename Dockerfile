FROM python:3.13-slim
WORKDIR /app
COPY requirements.lock pyproject.toml README.md ./
COPY src ./src
COPY scripts/container-entrypoint.py /app/container-entrypoint.py
RUN pip install --no-cache-dir -r requirements.lock && pip install --no-cache-dir --no-deps .
RUN useradd --uid 10001 --create-home bugproof && mkdir /data && chown bugproof:bugproof /data
ENV BUGPROOF_DATABASE_PATH=/data/bugproof.sqlite3 BUGPROOF_FASTN_OAUTH_PATH=/data/fastn-oauth.json BUGPROOF_ENV=production
EXPOSE 8000
CMD ["python", "/app/container-entrypoint.py"]
