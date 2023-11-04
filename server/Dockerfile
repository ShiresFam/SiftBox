FROM python:3.10-slim-buster

COPY ./app ./app

COPY ./requirements.txt .

ARG CLIENT_ID
ARG CLIENT_SECRET

ENV CLIENT_ID $CLIENT_ID
ENV CLIENT_SECRET $CLIENT_SECRET

RUN mkdir ./token

RUN pip install -r requirements.txt

ENV PORT=8000
EXPOSE 8000

COPY wait-for-cert-gen.sh /wait-for-cert-gen.sh
RUN chmod +x /wait-for-cert-gen.sh

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--ssl-keyfile", "/etc/ssl/private/nginx-selfsigned.key", "--ssl-certfile", "/etc/ssl/certs/nginx-selfsigned.crt"]