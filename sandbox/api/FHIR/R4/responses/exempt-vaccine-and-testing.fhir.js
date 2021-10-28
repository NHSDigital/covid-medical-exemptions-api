export default (id, includePatient) => ({
    "resourceType": "Bundle",
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
                    "display": "Ivor Fritagelse"
                },
                "authored": "2021-08-13T17:15:00+00:00",
                "item": [
                    {
                        "linkId": "exemptionStatus",
                        "answer": [
                            {
                                "valueCoding": {
                                    "code": "2",
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
        },
        ...(includePatient ? [{
            "resource": {
                "resourceType": "Patient",
                "identifier": [
                    {
                        "system": "https://fhir.nhs.uk/Id/nhs-number",
                        "value": id
                    }
                ],
                "name": [
                    {
                        "use": "official",
                        "given": ["John", "Jonah"],
                        "family": "Jameson"
                    }
                ],
                "birthDate": "1960-01-01"
            }
        }] : [])
    ]
});