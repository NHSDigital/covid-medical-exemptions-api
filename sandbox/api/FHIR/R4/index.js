import { Router } from 'express';
import response0 from './responses/empty-response.fhir';
import response1 from './responses/1_exempt-vaccine.fhir';
import response2 from './responses/2_exempt-vaccine-and-testing.fhir';
import response3 from './responses/3_declined-vaccine.fhir';
import response4 from './responses/4_declined-vaccine-and-testing.fhir';
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
            const ix = parseInt(id, 10) % responses.length;
            console.log("Response:", ix);
            const response = responses[ix](id);
            res.status(200).json(response);
        } catch(err) {
            next(err);
        }
    });

    return router;
};
