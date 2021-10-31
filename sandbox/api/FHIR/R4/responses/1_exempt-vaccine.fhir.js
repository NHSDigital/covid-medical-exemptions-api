export default (id, includePatient) => ({
    "resourceType": "Bundle",
    "type": "searchset",
    "entry": [
        {
            "resource": {
                "resourceType": "QuestionnaireResponse",
                "id": "2fa8f1b8-caea-4f3d-9978-c0839da568b2",
                "questionnaire": "https://fhir.nhs.uk/Questionnaire/COVIDVaccinationMedicalExemption",
                "status": "completed",
                "subject": {
                    "identifier": [
                        {
                            "system": "https://fhir.nhs.uk/Id/nhs-number",
                            "value": id
                        }
                    ],
                    "display": "John Jonah Jameson"
                },
                "contained": [
                    {
                        "id": "p1",
                        "resourceType": "Patient",
                        "birthDate": "1960-01-01"
                    }
                ],
                "authored": "2021-08-13T17:15:00+00:00",
                "item": [
                    {
                        "linkId": "exemptionStatus",
                        "answer": [
                            {
                                "valueCoding": {
                                    "code": "1",
                                    "display": "Approved: Exemption from COVID vaccination"
                                }
                            }
                        ]
                    },
                    {
                        "linkId": "exemptionPeriodStart",
                        "answer": [
                            {
                                "valueDateTime": "2021-08-13T17:15:00+00:00"
                            }
                        ]
                    },
                    {
                        "linkId": "exemptionPeriodEnd",
                        "answer": [
                            {
                                "valueDateTime": "2022-08-13T17:15:00+00:00"
                            }
                        ]
                    }
                ]
            }
        }
    ]
});