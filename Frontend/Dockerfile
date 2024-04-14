FROM node:18-alpine 

WORKDIR /front-app

COPY front-app/public/ /front-app/public
COPY front-app/src/ /front-app/src
COPY front-app/package.json /front-app/


RUN npm install

CMD ["npm", "start"]

EXPOSE 3000

