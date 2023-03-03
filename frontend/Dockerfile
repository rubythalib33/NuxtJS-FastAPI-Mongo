FROM node:lts as builder
WORKDIR /app
COPY . .

# install dependencies
RUN npm install

# build for production and launch server
RUN npm run build

# generate static project
RUN npm run generate

FROM node:lts
WORKDIR /app
COPY --from=builder /app  .
ENV HOST 0.0.0.0
CMD [ "npm", "start" ]
