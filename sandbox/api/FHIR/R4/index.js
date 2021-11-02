import { Router } from 'express';
import empty from './responses/empty-response.fhir';
import exemptVaccination from './responses/1_exempt-vaccine.fhir';
import exemptVaccinationAndTest from './responses/2_exempt-vaccine-and-testing.fhir';
import declinedVaccination from './responses/3_declined-vaccine.fhir';
import declinedVaccinationAndTest from './responses/4_declined-vaccine-and-testing.fhir';
const responses = [
    empty,
    exemptVaccination,
    exemptVaccinationAndTest,
    declinedVaccination,
    declinedVaccinationAndTest
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
