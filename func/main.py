from http import HTTPStatus

from etria_logger import Gladsheim
from flask import request, Request, Response
from heimdall_client.bifrost import Heimdall
from heimdall_client.bifrost import HeimdallStatusResponses

from func.src.domain.enums.response.code import InternalCode
from func.src.domain.exceptions.model import UnauthorizedError
from func.src.domain.request.model import WatchListParameters
from func.src.domain.response.model import ResponseModel
from func.src.services.watch_list import WatchListService


async def list_symbols(request: Request = request) -> Response:
    x_thebes_answer = request.headers.get("x-thebes-answer")
    parameters_dict = request.args.to_dict()

    try:
        jwt_content, heimdall_status = await Heimdall.decode_payload(
            jwt=x_thebes_answer
        )
        parameters = WatchListParameters(**parameters_dict)

        if heimdall_status != HeimdallStatusResponses.SUCCESS:
            Gladsheim.error(status=heimdall_status)
            raise UnauthorizedError()

        unique_id = jwt_content["decoded_jwt"]["user"]["unique_id"]
        result = await WatchListService.list_symbols_in_watch_list(
            unique_id, parameters
        )

        response = ResponseModel(
            result=result,
            success=True,
            code=InternalCode.SUCCESS,
            message="Success",
        ).build_http_response(status=HTTPStatus.OK)
        return response

    except UnauthorizedError as ex:
        message = "JWT invalid or not supplied"
        Gladsheim.error(error=ex, message=message)
        response = ResponseModel(
            success=False, code=InternalCode.JWT_INVALID, message=message
        ).build_http_response(status=HTTPStatus.BAD_REQUEST)
        return response

    except ValueError as ex:
        message = "Invalid parameters"
        Gladsheim.error(error=ex, message=message)
        response = ResponseModel(
            success=False, code=InternalCode.INVALID_PARAMS, message=message
        ).build_http_response(status=HTTPStatus.BAD_REQUEST)
        return response

    except Exception as ex:
        message = "Unexpected error occurred"
        Gladsheim.error(error=ex, message=message)
        response = ResponseModel(
            success=False, code=InternalCode.INTERNAL_SERVER_ERROR, message=message
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response
