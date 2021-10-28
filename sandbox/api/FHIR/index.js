import { Router } from 'express';
import R4 from './R4';

export default function (dependencies, config) {
    const router = new Router();

    router.use('/R4', R4(dependencies, config));

    return router;
};