import { Router } from 'express';
import response0 from './responses/empty-response.fhir';
import response1 from './responses/exempt-vaccine.fhir';
import response2 from './responses/exempt-vaccine-and-testing.fhir';
import response3 from './responses/declined-vaccine.fhir';
import response4 from './responses/declined-vaccine-and-testing.fhir';
const responses = [
    response0,
    response1,
    response2,
    response3,
    response4
];

export default function(dependencies, config) {
    const router = new Router();
    
    router.get('/CovidMedicalExemption', (req, res, next) => {
        try {
            const [type, id] = req.query['patient.identifier'].split('|');
            const includes = req.query['_includes'] || 'Exemption:Patient';
            const ix = parseInt(id, 10) % responses.length;
            console.log(ix);
            const response = responses[ix](id, includes === 'Exemption:Patient');
            res.status(200).json(response);
        } catch(err) {
            next(err);
        }
    });

    return router;
};
