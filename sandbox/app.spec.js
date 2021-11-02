const request = require("supertest");
const assert = require("chai").assert;
import App from './app';

describe("app handler tests", function () {
    const APP_NAME = 'covid-medical-exemption';
    const SWAGGER_FILE = '../specification/covid-medical-exemptions.yaml';
    const VERSION_INFO = {
        build_label: "1233-shaacdef1",
        releaseId: "1234",
        commitId: "acdef12341ccc"
    };
    let server;
    let env;

    before(function () {
        server = App({ 
        
        }, {
            APP_NAME,
            SWAGGER_FILE,
            VERSION_INFO,
        });
    });

    after(function () {
        process.env = env;
        server.close();
    });

    it("responds to /_ping", (done) => {
        request(server)
            .get("/_ping")
            .expect(200, {
                status: "pass",
                ping: "pong",
                service: APP_NAME,
                version: VERSION_INFO
            })
            .expect("Content-Type", /json/, done);
    });

    it("responds to /_status", (done) => {
        request(server)
            .get("/_status")
            .expect(200, {
                status: "pass",
                ping: "pong",
                service: APP_NAME,
                version: VERSION_INFO
            })
            .expect("Content-Type", /json/, done);
    });

    it("responds to /health", (done) => {
        request(server)
            .get("/health")
            .expect(200, {
                status: "pass",
                ping: "pong",
                service: APP_NAME,
                version: VERSION_INFO
            })
            .expect("Content-Type", /json/, done);
    });
});

