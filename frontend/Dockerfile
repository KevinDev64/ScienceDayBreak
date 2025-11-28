FROM node:current-alpine as build

WORKDIR /app

COPY package*.json .
RUN npm install

COPY . .
RUN npm run build

CMD ["HOST=0.0.0.0:3000", "npm", "run", "start"]
