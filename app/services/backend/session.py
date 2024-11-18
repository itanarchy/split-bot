from typing import Any, cast

from stollen import Stollen
from stollen.requests import StollenRequest, StollenResponse
from stollen.session.aiohttp import AiohttpSession


def search_error_message(body: dict[str, Any]) -> str:
    if "detail" in body:
        if isinstance(body["detail"], str):
            return cast(str, body.pop("detail"))
        body = body.pop("detail")
    return cast(str, body["error_message"])


class BackendSession(AiohttpSession):
    @classmethod
    def prepare_response(
        cls,
        client: Stollen,
        request: StollenRequest,
        response: StollenResponse,
    ) -> Any:
        if response.body is not None:
            response.body["error_message"] = search_error_message(response.body)
        return super().prepare_response(client, request, response)
