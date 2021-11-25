import { Router } from 'express';
import declinedVaccination from './responses/3_declined-vaccine.fhir';
import declinedVaccinationAndTest from './responses/4_declined-vaccine-and-testing.fhir';
import empty from './responses/empty-response.fhir';
import exemptVaccination from './responses/1_exempt-vaccine.fhir';
import exemptVaccinationAndTest from './responses/2_exempt-vaccine-and-testing.fhir';
const responses = [
    empty,
    exemptVaccination,
    exemptVaccinationAndTest,
    declinedVaccination,
    declinedVaccinationAndTest
];

export default function(dependencies, config) {
    const router = new Router();
    
    router.get('/QuestionnaireResponse', (req, res, next) => {
        try {
            const questionnaire = req.query['questionnaire'];
            if (questionnaire !== 'https://fhir.nhs.uk/Questionnaire/COVIDVaccinationMedicalExemption')
                return res.status(400).json({ message: 'Bad Request' });
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
