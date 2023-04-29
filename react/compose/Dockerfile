FROM node:18-alpine

WORKDIR /app

ENV PATH /app/node_modules/.bin:$PATH

COPY frontend/package.json ./
COPY frontend/package-lock.json ./
RUN npm install

COPY ./frontend/ ./