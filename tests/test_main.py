from unittest.mock import patch

from etria_logger import Gladsheim
from flask import Flask
from heimdall_client.bifrost import Heimdall
from pytest import mark
from werkzeug.test import Headers

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


@mark.asyncio
@patch.object(WatchListService, "list_symbols_in_watch_list")
@patch.object(Heimdall, "decode_payload")
async def test_list_symbols_when_request_is_ok(
    decode_payload_mock, list_symbols_in_watch_list_mock
):
    decode_payload_mock.return_value = (decoded_jwt_ok, "HeimdallStatus")
    list_symbols_in_watch_list_mock.return_value = [
        {"symbol": "symbol", "region": "region"}
    ]

    app = Flask(__name__)
    with app.test_request_context(
        headers=Headers({"x-thebes-answer": "test"}),
    ).request as request:

        list_symbols_result = await list_symbols(request)

        assert (
            list_symbols_result.data
            == b'{"result": [{"symbol": "symbol", "region": "region"}], "message": "Success", "success": true, "code": 0}'
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
    decode_payload_mock.return_value = (decoded_jwt_invalid, "HeimdallStatus")
    list_symbols_in_watch_list_mock.return_value = [
        {"symbol": "symbol", "region": "region"}
    ]

    app = Flask(__name__)
    with app.test_request_context(
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
@patch.object(Gladsheim, "error")
@patch.object(WatchListService, "list_symbols_in_watch_list")
@patch.object(Heimdall, "decode_payload")
async def test_list_symbols_when_generic_exception_happens(
    decode_payload_mock, list_symbols_in_watch_list_mock, etria_mock
):
    decode_payload_mock.return_value = (decoded_jwt_ok, "HeimdallStatus")
    list_symbols_in_watch_list_mock.side_effect = Exception("erro")

    app = Flask(__name__)
    with app.test_request_context(
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
