from unittest.mock import patch

import decouple
from etria_logger import Gladsheim
from flask import Flask
from heimdall_client import HeimdallStatusResponses
from heimdall_client.bifrost import Heimdall
from pytest import mark
from werkzeug.test import Headers

with patch.object(decouple, "config", return_value="CONFIG"):
    from main import list_symbols
    from src.services.watch_list import WatchListService

decoded_jwt_ok = {
    "is_payload_decoded": True,
    "decoded_jwt": {"user": {"unique_id": "test"}},
    "message": "Jwt decoded",
}
decoded_jwt_invalid = {
    "is_payload_decoded": False,
    "decoded_jwt": {"user": {"unique_id": "test_error"}},
    "message": "Jwt decoded",
}

requests_with_invalid_parameters = [
    "?limit=&offset=12",
    "?limit1=&offset=",
    "?limit=-1&offset=-1",
]


@mark.asyncio
@patch.object(WatchListService, "list_symbols_in_watch_list")
@patch.object(Heimdall, "decode_payload")
async def test_list_symbols_when_request_is_ok(
    decode_payload_mock, list_symbols_in_watch_list_mock
):
    decode_payload_mock.return_value = (decoded_jwt_ok, HeimdallStatusResponses.SUCCESS)
    service_result = {
        "symbols": {"symbol": "symbol", "region": "region"},
        "pages": 1,
        "current_page": 1,
    }
    list_symbols_in_watch_list_mock.return_value = service_result

    app = Flask(__name__)
    with app.test_request_context(
        "?limit=3&offset=12",
        headers=Headers({"x-thebes-answer": "test"}),
    ).request as request:

        list_symbols_result = await list_symbols(request)

        assert (
            list_symbols_result.data
            == b'{"result": {"symbols": {"symbol": "symbol", "region": "region"}, "pages": 1, "current_page": 1}, "message": "Success", "success": true, "code": 0}'
        )
        assert list_symbols_in_watch_list_mock.called
        decode_payload_mock.assert_called_with(jwt="test")


@mark.asyncio
@patch.object(Gladsheim, "error")
@patch.object(WatchListService, "list_symbols_in_watch_list")
@patch.object(Heimdall, "decode_payload")
async def test_list_symbols_when_jwt_is_invalid(
    decode_payload_mock, list_symbols_in_watch_list_mock, etria_mock
):
    decode_payload_mock.return_value = (
        decoded_jwt_invalid,
        HeimdallStatusResponses.INVALID_TOKEN,
    )
    service_result = {
        "symbols": {"symbol": "symbol", "region": "region"},
        "pages": 1,
        "current_page": 1,
    }
    list_symbols_in_watch_list_mock.return_value = service_result

    app = Flask(__name__)
    with app.test_request_context(
        "?limit=3&offset=12",
        headers=Headers({"x-thebes-answer": "test_error"}),
    ).request as request:

        list_symbols_result = await list_symbols(request)

        assert (
            list_symbols_result.data
            == b'{"result": null, "message": "JWT invalid or not supplied", "success": false, "code": 30}'
        )
        assert not list_symbols_in_watch_list_mock.called
        decode_payload_mock.assert_called_with(jwt="test_error")
        etria_mock.assert_called()


@mark.asyncio
@mark.parametrize("query_values", requests_with_invalid_parameters)
@patch.object(Gladsheim, "error")
@patch.object(WatchListService, "list_symbols_in_watch_list")
@patch.object(Heimdall, "decode_payload")
async def test_list_symbols_when_params_are_invalid(
    decode_payload_mock, list_symbols_in_watch_list_mock, etria_mock, query_values
):
    decode_payload_mock.return_value = (
        decoded_jwt_ok,
        HeimdallStatusResponses.SUCCESS,
    )
    service_result = {
        "symbols": {"symbol": "symbol", "region": "region"},
        "pages": 1,
        "current_page": 1,
    }
    list_symbols_in_watch_list_mock.return_value = service_result

    app = Flask(__name__)
    with app.test_request_context(
        query_values,
        headers=Headers({"x-thebes-answer": "test"}),
    ).request as request:

        list_symbols_result = await list_symbols(request)

        assert (
            list_symbols_result.data
            == b'{"result": null, "message": "Invalid parameters", "success": false, "code": 10}'
        )
        assert not list_symbols_in_watch_list_mock.called
        decode_payload_mock.assert_called_with(jwt="test")
        etria_mock.assert_called()


@mark.asyncio
@patch.object(Gladsheim, "error")
@patch.object(WatchListService, "list_symbols_in_watch_list")
@patch.object(Heimdall, "decode_payload")
async def test_list_symbols_when_generic_exception_happens(
    decode_payload_mock, list_symbols_in_watch_list_mock, etria_mock
):
    decode_payload_mock.return_value = (decoded_jwt_ok, HeimdallStatusResponses.SUCCESS)
    list_symbols_in_watch_list_mock.side_effect = Exception("erro")

    app = Flask(__name__)
    with app.test_request_context(
        "?limit=3&offset=12",
        headers=Headers({"x-thebes-answer": "test"}),
    ).request as request:

        list_symbols_result = await list_symbols(request)

        assert (
            list_symbols_result.data
            == b'{"result": null, "message": "Unexpected error occurred", "success": false, "code": 100}'
        )
        assert list_symbols_in_watch_list_mock.called
        decode_payload_mock.assert_called_with(jwt="test")
        etria_mock.assert_called()
