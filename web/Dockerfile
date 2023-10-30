FROM node:18.16.0-slim as build

WORKDIR /app

COPY package*.json ./
RUN npm ci
COPY . ./

RUN npm run build

FROM nginx:1.23

COPY ./nginx/nginx.conf /etc/nginx/nginx.conf

EXPOSE 8080

COPY --from=build /app/build /usr/share/nginx/html