FROM node:18-alpine

WORKDIR /app

ENV PATH /app/node_modules/.bin:$PATH

COPY ./frontend/package.json /app/
COPY ./frontend/package-lock.json /app/
RUN npm install

COPY ./frontend/ /app/