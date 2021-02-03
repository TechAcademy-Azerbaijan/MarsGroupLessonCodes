FROM redis:4.0.11

ENV REDIS_PASSWORD 12345

CMD ["sh", "-c", "exec redis-server --requirepass \"$REDIS_PASSWORD\""]