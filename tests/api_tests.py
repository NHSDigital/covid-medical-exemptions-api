import asyncio
from typing import List
from uuid import uuid4
from functools import partial

import pytest
from aiohttp import ClientResponse
from api_test_utils.api_session_client import APISessionClient
from api_test_utils.api_test_session_config import APITestSessionConfig
from api_test_utils import poll_until, env

from . import conftest


def dict_path(raw, path: List[str]):
    if not raw:
        return raw

    if not path:
        return raw

    res = raw.get(path[0])
    if not res or len(path) == 1 or type(res) != dict:
        return res

    return dict_path(res, path[1:])


def _base_valid_uri(nhs_number) -> str:
    return f"FHIR/R4/QuestionnaireResponse?patient.identifier=https://fhir.nhs.uk/Id/nhs-number%7C{nhs_number}"


# TO DO - Use valid version of URL once implemented on backend
def _valid_uri(nhs_number, questionnaire) -> str:
    return _base_valid_uri(nhs_number) + f"&questionnaire={questionnaire}"


# def _valid_uri(nhs_number, questionnaire) -> str:
#     return "FHIR/R4?patient.identifier=12345"


async def _is_deployed(resp: ClientResponse, api_test_config: APITestSessionConfig) -> bool:
    if resp.status != 200:
        return False
    body = await resp.json()

    return body.get("commitId") == api_test_config.commit_id


async def is_401(resp: ClientResponse) -> bool:
    return resp.status == 401


@pytest.mark.e2e
@pytest.mark.smoketest
def test_output_test_config(api_test_config: APITestSessionConfig):
    print(api_test_config)


@pytest.mark.e2e
@pytest.mark.smoketest
@pytest.mark.asyncio
async def test_wait_for_ping(api_client: APISessionClient, api_test_config: APITestSessionConfig):
    """
        test for _ping ..  this uses poll_until to wait until the correct SOURCE_COMMIT_ID ( from env var )
        is available
    """

    is_deployed = partial(_is_deployed, api_test_config=api_test_config)

    await poll_until(
        make_request=lambda: api_client.get('_ping'),
        until=is_deployed,
        timeout=120
    )


@pytest.mark.e2e
@pytest.mark.smoketest
@pytest.mark.asyncio
async def test_check_status_is_secured(api_client: APISessionClient):

    await poll_until(
        make_request=lambda: api_client.get('_status'),
        until=is_401,
        timeout=120
    )


@pytest.mark.e2e
@pytest.mark.smoketest
@pytest.mark.asyncio
async def test_wait_for_status(api_client: APISessionClient, api_test_config: APITestSessionConfig):

    """
        test for _status ..  this uses poll_until to wait until the correct SOURCE_COMMIT_ID ( from env var )
        is available
    """

    is_deployed = partial(_is_deployed, api_test_config=api_test_config)

    await poll_until(
        make_request=lambda: api_client.get('_status', headers={'apikey': env.status_endpoint_api_key()}),
        until=is_deployed,
        timeout=120
    )


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_check_cme_is_secured(api_client: APISessionClient):

    resp = await api_client.get(_base_valid_uri("2295442338"), allow_retries=True)
    assert resp.status == 401


@pytest.mark.e2e
@pytest.mark.asyncio
@pytest.mark.parametrize(
    'test_app',
    [
        {
            'suffixes': ['-application-restricted']
        },
        {
            'suffixes': ['-application-restricted', '-user-restricted']
        }
    ],
    indirect=True
)
async def test_client_credentials_happy_path(test_app, api_client: APISessionClient):
    authorised_headers = await conftest.get_authorised_headers(test_app)

    correlation_id = str(uuid4())
    authorised_headers["X-Correlation-ID"] = correlation_id

    async with api_client.get(
        _valid_uri("2295442338", "https://fhir.nhs.uk/Questionnaire/COVIDVaccinationMedicalExemption"),
        headers=authorised_headers,
        allow_retries=True
    ) as resp:
        assert resp.status == 200
        body = await resp.json()
        assert "x-correlation-id" in resp.headers, resp.headers
        assert resp.headers["x-correlation-id"] == correlation_id
        # TO DO - Use valid version of response body once implemented on backend
        assert body["test"] == "test", body


@pytest.mark.e2e
@pytest.mark.asyncio
@pytest.mark.parametrize(
    'test_app',
    [
        {
            'suffixes': ['-user-restricted']
        },
        {
            'suffixes': ['-application-restricted']
        }
    ],
    indirect=True
)
async def test_cme_no_auth_bearer_token_provided(test_app, api_client: APISessionClient):

    await asyncio.sleep(1)  # Add delay to tests to avoid 429 on service callout
    correlation_id = str(uuid4())
    headers = {
        "Authorization": "Bearer",
        "X-Correlation-ID": correlation_id
    }
    async with api_client.get(
        _valid_uri("2295442338", "https://fhir.nhs.uk/Questionnaire/COVIDVaccinationMedicalExemption"),
        headers=headers,
        allow_retries=True
    ) as resp:
        assert resp.status == 401, 'failed getting backend data'
        body = await resp.json()
        assert "x-correlation-id" in resp.headers, resp.headers
        assert resp.headers["x-correlation-id"] == correlation_id
        assert body["issue"] == [
            {'code': 'forbidden', 'diagnostics': 'Provided access token is invalid', 'severity': 'error'}
        ], body


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_correlation_id_mirrored_in_resp_when_error(
    api_client: APISessionClient
):
    access_token = "invalid_token"

    correlation_id = str(uuid4())

    async with api_client.get(
        _valid_uri("2295442338", "https://fhir.nhs.uk/Questionnaire/COVIDVaccinationMedicalExemption"),
        headers={"Authorization": f"Bearer {access_token}", "X-Correlation-ID": correlation_id},
        allow_retries=True
    ) as resp:
        assert resp.status == 401
        assert "x-correlation-id" in resp.headers, resp.headers
        assert resp.headers["x-correlation-id"] == correlation_id, resp.headers


@pytest.mark.e2e
@pytest.mark.asyncio
@pytest.mark.parametrize(
    'test_app',
    [
        {
            'suffixes': ['-user-restricted'],
            'requested_proofing_level': 'P9',
            'identity_proofing_level': 'P9'
        },
        {
            'suffixes': ['-user-restricted'],
            'requested_proofing_level': 'P5',
            'identity_proofing_level': 'P9'
        },
        {
            'suffixes': ['-user-restricted'],
            'requested_proofing_level': 'P5',
            'identity_proofing_level': 'P5'
        },
        {
            'suffixes': ['-application-restricted', '-user-restricted'],
            'requested_proofing_level': 'P9',
            'identity_proofing_level': 'P9'
        },
        {
            'suffixes': ['-application-restricted', '-user-restricted'],
            'requested_proofing_level': 'P5',
            'identity_proofing_level': 'P9'
        },
        {
            'suffixes': ['-application-restricted', '-user-restricted'],
            'requested_proofing_level': 'P5',
            'identity_proofing_level': 'P5'
        },
    ],
    indirect=True
)
async def test_token_exchange_happy_path(test_app, api_client: APISessionClient):
    subject_token_claims = {
        'identity_proofing_level': test_app.request_params['identity_proofing_level']
    }
    token_response = await conftest.get_token_nhs_login_token_exchange(
        test_app,
        subject_token_claims=subject_token_claims
    )
    token = token_response["access_token"]

    correlation_id = str(uuid4())
    headers = {
        "Authorization": f"Bearer {token}",
        "X-Correlation-ID": correlation_id
    }

    async with api_client.get(
        _valid_uri("2295442338", "https://fhir.nhs.uk/Questionnaire/COVIDVaccinationMedicalExemption"),
        headers=headers,
        allow_retries=True
    ) as resp:
        assert resp.status == 200, 'failed getting backend data'
        body = await resp.json()
        assert "x-correlation-id" in resp.headers, resp.headers
        assert resp.headers["x-correlation-id"] == correlation_id
        # TO DO - Use valid version of response body once implemented on backend
        assert body["test"] == "test", body


@pytest.mark.e2e
@pytest.mark.asyncio
@pytest.mark.parametrize(
    'test_app',
    [
        {
            'suffixes': ['-application-restricted'],
            'requested_proofing_level': 'P9',
            'identity_proofing_level': 'P9'
        },
        {
            'suffixes': ['-application-restricted'],
            'requested_proofing_level': 'P5',
            'identity_proofing_level': 'P9'
        },
        {
            'suffixes': ['-application-restricted'],
            'requested_proofing_level': 'P5',
            'identity_proofing_level': 'P5'
        },
    ],
    indirect=True
)
async def test_token_exchange_sad_path(test_app, api_client: APISessionClient):
    subject_token_claims = {
        'identity_proofing_level': test_app.request_params['identity_proofing_level']
    }
    await conftest.check_for_unauthorised_token_exchange(
        test_app,
        subject_token_claims=subject_token_claims
    )


@pytest.mark.e2e
@pytest.mark.asyncio
@pytest.mark.parametrize(
    'test_product_and_app',
    [
        {
            'scopes': ['urn:nhsd:apim:user-nhs-id:aal3:immunisation-history'],
            'requested_proofing_level': 'P9',
            'identity_proofing_level': 'P9'
        },
        {
            'scopes': ['urn:nhsd:apim:user-nhs-id:aal3:immunisation-history'],
            'requested_proofing_level': 'P5',
            'identity_proofing_level': 'P9'
        }
    ],
    indirect=True
)
async def test_user_restricted_access_not_permitted(api_client: APISessionClient, test_product_and_app):
    await asyncio.sleep(1)  # Add delay to tests to avoid 429 on service callout

    test_product, test_app = test_product_and_app

    token_response = await conftest.get_token(test_app)

    authorised_headers = {
        "Authorization": f"Bearer {token_response['access_token']}",
        "NHSD-User-Identity": conftest.nhs_login_id_token(
            test_app,
            allowed_proofing_level=test_app.request_params['identity_proofing_level']
        )
    }

    async with api_client.get(
        _valid_uri("2295442338", "https://fhir.nhs.uk/Questionnaire/COVIDVaccinationMedicalExemption"),
        headers=authorised_headers,
        allow_retries=True
    ) as resp:
        assert resp.status == 401
        body = await resp.json()
        assert body["resourceType"] == "OperationOutcome"
        assert body["issue"][0]["severity"] == "error"
        assert body["issue"][0]["diagnostics"] == "Provided access token is invalid"
        assert body["issue"][0]["code"] == "forbidden"


@pytest.mark.e2e
@pytest.mark.asyncio
@pytest.mark.parametrize(
    'test_product_and_app',
    [
        {
            'scopes': ['urn:nhsd:apim:user-nhs-login:P6:immunisation-history'],
            'requested_proofing_level': 'P9',
            'identity_proofing_level': 'P6'
        },
        {
            'scopes': ['urn:nhsd:apim:user-nhs-login:P6:immunisation-history'],
            'requested_proofing_level': 'P5',
            'identity_proofing_level': 'P6'
        }
    ],
    indirect=True
)
async def test_token_exchange_invalid_identity_proofing_level_scope(api_client: APISessionClient, test_product_and_app):

    test_product, test_app = test_product_and_app
    subject_token_claims = {
        "identity_proofing_level": test_app.request_params['identity_proofing_level']
    }
    token_response = await conftest.get_token_nhs_login_token_exchange(
        test_app, subject_token_claims=subject_token_claims
    )
    token = token_response["access_token"]

    correlation_id = str(uuid4())
    headers = {
        "Authorization": f"Bearer {token}",
        "X-Correlation-ID": correlation_id
    }

    async with api_client.get(
        _valid_uri("2295442338", "https://fhir.nhs.uk/Questionnaire/COVIDVaccinationMedicalExemption"),
        headers=headers,
        allow_retries=True
    ) as resp:
        assert resp.status == 401
        assert "x-correlation-id" in resp.headers, resp.headers
        assert resp.headers["x-correlation-id"] == correlation_id
