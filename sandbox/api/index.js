import { Router } from 'express';
import FHIR from './FHIR';

export default function(dependencies, config) {
    const router = new Router();

    const status = (req, res) => {
        res.status(200).json({
            status: "pass",
            ping: "pong",
            service: req.app.locals.app_name,
            version: req.app.locals.version_info
        });
    }

    router.get('/_status', status);
    router.get('/ping', status);
    router.get('/health', status);

    router.get('/hello', (req, res) => {
        res.status(200).json({ message: 'Hello World' });
    });

    router.use('/FHIR', FHIR(dependencies, config));

    return router;
};
