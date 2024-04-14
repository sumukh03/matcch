FROM node:18-alpine 

WORKDIR /matcch

COPY matcch/public/ /matcch/public
COPY matcch/src/ /matcch/src
COPY matcch/package.json /matcch/


RUN npm install

CMD ["npm", "start"]

EXPOSE 3000

