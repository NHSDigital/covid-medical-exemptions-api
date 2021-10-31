export default (id, includePatient) => ({
    "resourceType": "Bundle",
    "type": "searchset",
    "entry": includePatient ? [{
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
    }] : [
        ]
});