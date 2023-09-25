# syntax=docker/dockerfile:1

FROM node:18-alpine
WORKDIR /app
COPY . .
RUN yarn install --production
# RUN pip install scrapy ||
    # pip install pymongo
CMD ["node", "src/index.js"]
EXPOSE 3000