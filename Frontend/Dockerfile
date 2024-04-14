# Use the official Node.js image as a base
FROM node:18-alpine 

# Set the working directory in the container
WORKDIR /matcch

# Copy the package.json and package-lock.json files into the container
COPY matcch/public/ /matcch/public
COPY matcch/src/ /matcch/src
COPY matcch/package.json /matcch/

# Install dependencies
RUN npm install

# Build the React app
CMD ["npm", "start"]

EXPOSE 3000

