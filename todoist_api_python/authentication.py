import urllib
from typing import List, Optional

import requests
from requests import Session

from todoist_api_python.endpoints import (
    AUTHORIZE_ENDPOINT,
    TOKEN_ENDPOINT,
    get_auth_url,
)
from todoist_api_python.http_requests import post
from todoist_api_python.models import AuthResult
from todoist_api_python.utils import run_async


def get_auth_token(
    client_id: str, client_secret: str, code: str, session: Optional[Session] = None
) -> AuthResult:
    endpoint = get_auth_url(TOKEN_ENDPOINT)
    session = session or requests.Session()
    payload = {"client_id": client_id, "client_secret": client_secret, "code": code}
    response = post(session=session, url=endpoint, data=payload)

    return AuthResult.from_dict(response)


async def get_auth_token_async(
    client_id: str, client_secret: str, code: str
) -> AuthResult:
    return await run_async(lambda: get_auth_token(client_id, client_secret, code))


def get_authentication_url(client_id: str, scopes: List[str], state: str) -> str:
    if len(scopes) == 0:
        raise Exception("At least one authorization scope should be requested.")

    query = {"client_id": client_id, "scope": ",".join(scopes), "state": state}

    auth_url = get_auth_url(AUTHORIZE_ENDPOINT)

    return f"{auth_url}?{urllib.parse.urlencode(query)}"
