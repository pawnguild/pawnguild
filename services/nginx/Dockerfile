FROM nginx:1.21-alpine

RUN apk add inotify-tools certbot openssl bash certbot-nginx

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY command /opt/command
