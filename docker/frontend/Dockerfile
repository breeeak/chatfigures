FROM node:16-alpine  as node-container
WORKDIR /cf-frontend-container
COPY ./cf-frontend/ .
RUN rm -rf node_modules
RUN yarn install
RUN yarn run build

FROM nginx:alpine
COPY ./docker/frontend/nginx/my.conf /etc/nginx/conf.d/default.conf
# COPY ./docker/frontend/nginx/my.conf /etc/nginx/nginx.conf
COPY --from=node-container /cf-frontend-container/dist /usr/share/nginx/html





