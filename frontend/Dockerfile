FROM node:lts-alpine

WORKDIR /frontend

COPY . /frontend

RUN npm install --legacy-peer-deps

EXPOSE 8080

CMD ["npm", "run", "serve"]
