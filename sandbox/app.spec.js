
const request = require("supertest");
const assert = require("chai").assert;
import App from './app';

describe("app handler tests", function () {
    const version_info = {
        build_label: "1233-shaacdef1",
        releaseId: "1234",
        commitId: "acdef12341ccc"
    };
    let server;
    let env;

    before(function () {
        let app = App({ }, process.env);
    });

    beforeEach(function () {

    });

    afterEach(function () {

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
                service: "covid-medical-exemption",
                version: version_info
            })
            .expect("Content-Type", /json/, done);
    });

    it("responds to /_status", (done) => {
        request(server)
            .get("/_status")
            .expect(200, {
                status: "pass",
                ping: "pong",
                service: "covid-medical-exemption",
                version: version_info
            })
            .expect("Content-Type", /json/, done);
    });

    it("responds to /hello", (done) => {
        request(server)
            .get("/hello")
            .expect(200, done);
    });
});

