FROM python:3
RUN  pip install aiosmtpd
COPY server.py client.py /
COPY server.pem server.key /
WORKDIR /
# Ensure logging is displayed in docker logs
ENV PYTHONUNBUFFERED=1
ENTRYPOINT ["/server.py"]
