FROM node:current-alpine as build

WORKDIR /app

COPY package*.json .
RUN npm install

COPY . .
RUN npm run build

ENV HOST "0.0.0.0:3000"

CMD ["npm", "run", "start"]
