# syntax=docker/dockerfile:1
FROM node:18-alpine AS build

WORKDIR /app
COPY package.json pnpm-lock.yaml ./

RUN npm install -g pnpm typescript
RUN pnpm install

COPY . .

RUN pnpm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html