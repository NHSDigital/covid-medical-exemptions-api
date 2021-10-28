import createMiddleware from 'swagger-express-middleware';
import { serve, setup } from "swagger-ui-express";
import yaml from 'js-yaml';
import fs from 'fs';
import express from 'express';
import bodyParser from 'body-parser';
import api from './api';
import { logging, errorHandler, notFound } from './middleware';

export default function(dependencies, config) {
    const app = express();
    app.use(bodyParser.urlencoded({ extended: false }));
    app.use(bodyParser.json());

    app.locals.app_name = config.APP_NAME;
    app.locals.version_info = config.VERSION_INFO;

    console.log('Loading', config.SWAGGER_FILE);
    const swaggerRaw = fs.readFileSync(config.SWAGGER_FILE, 'utf-8');
    const swagger = yaml.load(swaggerRaw);
    swagger.host = `${config.HOST}:${config.PORT}`;

    app.use(logging);
    app.use('/swagger', serve, setup(swagger));
    createMiddleware(config.SWAGGER_FILE, app, (_err, middleware) => {
        app.use(
            middleware.metadata(),
            middleware.CORS(),
            middleware.files(),
            middleware.parseRequest(),
            middleware.validateRequest(),
            // middleware.mock(),
        );
        app.use('/', api(dependencies, config));
        app.use(notFound);
        app.use(errorHandler);      
    });

    return app;
}
