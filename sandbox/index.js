import path from 'path';
import App from './app';

const {
    HOST = 'localhost',
    PORT = 9000,
    APP_NAME = 'covid-medical-exemptions',
    VERSION_INFO = '{}',
    SWAGGER_FILE = null
} = process.env;

const dependencies = { };

const swaggerFile = path.join(__dirname, SWAGGER_FILE || '../specification/covid-medical-exemptions.yaml');
const config = {
    HOST,
    PORT,
    APP_NAME,
    VERSION_INFO: JSON.parse(VERSION_INFO),
    SWAGGER_FILE: swaggerFile
};

const app = App(dependencies, config);

const server = app.listen(PORT, function() {
    console.log(`listening http://localhost:${PORT}/`);
});
