FROM node:18-alpine 

WORKDIR /react-app

COPY react-app/public/ /react-app/public
COPY react-app/src/ /react-app/src
COPY react-app/package.json /react-app/


RUN npm install

CMD ["npm", "start"]

EXPOSE 3000

