# Jormungandr
from src.domain.enums.response.code import InternalCode
from src.domain.exceptions.model import UnauthorizedError
from src.services.watch_list import WatchListService
from src.domain.response.model import ResponseModel
from heimdall_client.bifrost import Heimdall

# Standards
from http import HTTPStatus

# Third party
from flask import request, Request, Response
from etria_logger import Gladsheim


async def list_symbols(request: Request = request) -> Response:
    x_thebes_answer = request.headers.get('x-thebes-answer')

    try:
        jwt_content, heimdall_status = await Heimdall.decode_payload(jwt=x_thebes_answer)
        if not jwt_content["is_payload_decoded"]:
            raise UnauthorizedError()

        unique_id = jwt_content["decoded_jwt"]["user"]["unique_id"]
        result = await WatchListService.list_symbols(unique_id)

        response = ResponseModel(
            result=result,
            success=True,
            code=InternalCode.SUCCESS,
            message="Success.",
        ).build_http_response(status=HTTPStatus.OK)
        return response

    except UnauthorizedError:
        response = ResponseModel(
            success=False, code=InternalCode.JWT_INVALID, message="JWT invalid or not supplied."
        ).build_http_response(status=HTTPStatus.BAD_REQUEST)
        return response

    except Exception as ex:
        message = "Unexpected error occurred"
        Gladsheim.error(error=ex, message=message)
        response = ResponseModel(
            success=False, code=InternalCode.INTERNAL_SERVER_ERROR, message=message
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response
