FROM node:12

ENV SWAGGER_FILE 'specification/covid-medical-exemptions.yaml'

WORKDIR /sandbox

EXPOSE 9000

COPY . /sandbox

RUN npm install

CMD ["npm", "start"]
