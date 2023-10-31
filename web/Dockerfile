FROM node:18.16.0-slim as build

WORKDIR /app

COPY package*.json ./
RUN npm ci
COPY . ./

RUN npm run build

FROM nginx:1.23

# Generate a self-signed certificate
RUN apt-get update && \
    apt-get install -y openssl && \
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/nginx-selfsigned.key -out /etc/ssl/certs/nginx-selfsigned.crt -subj "/C=US/ST=Denial/L=Springfield/O=Dis/CN=localhost"

COPY ./nginx/nginx.conf /etc/nginx/nginx.conf

EXPOSE 443

COPY --from=build /app/build /usr/share/nginx/html