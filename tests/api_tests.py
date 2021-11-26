import asyncio
from typing import List
from uuid import uuid4
from functools import partial

import pytest
from aiohttp import ClientResponse
from api_test_utils import env
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


def _valid_uri(nhs_number, questionnaire) -> str:
    return _base_valid_uri(nhs_number) + f"&questionnaire={questionnaire}"


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

    resp = await api_client.get(_base_valid_uri("9912003888"), allow_retries=True)
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
        _valid_uri("9912003888", "90640007"),
        headers=authorised_headers,
        allow_retries=True
    ) as resp:
        assert resp.status == 200
        body = await resp.json()
        assert "x-correlation-id" in resp.headers, resp.headers
        assert resp.headers["x-correlation-id"] == correlation_id
        assert body["resourceType"] == "Bundle", body
        assert len(body["entry"]) == 3, body
