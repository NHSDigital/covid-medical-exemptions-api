const developerAppName = context.getVariable('developer.app.name');
const developerAppId = context.getVariable('developer.app.id');
const clientIP = context.getVariable('client.ip');
const allowedProofingLevel = context.getVariable('nhs-login-allowed-proofing-level');

const clientRpDetailsHeader = {
    "developer.app.name": developerAppName,
    "developer.app.id": developerAppId,
    "developer.app.nhs-login-minimum-proofing-level": allowedProofingLevel,
    "client.ip": clientIP
};

context.targetRequest.headers['NHSD-Client-RP-Details'] = clientRpDetailsHeader;
