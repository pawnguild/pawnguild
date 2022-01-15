FROM nginx:1.21-alpine

RUN apk add inotify-tools certbot openssl bash certbot-nginx
WORKDIR /opt
COPY nginx.conf /etc/nginx/conf.d/web.conf
COPY command ./
CMD ["./command"]
