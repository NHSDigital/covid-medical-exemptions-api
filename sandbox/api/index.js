import { Router } from 'express';
import FHIR from './FHIR';

export default function(dependencies, config) {
    const router = new Router();

    router.use('/FHIR', FHIR(dependencies, config));

    return router;
};
