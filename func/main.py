from http import HTTPStatus

from etria_logger import Gladsheim
from flask import request, Request, Response

from func.src.domain.enums.response.code import InternalCode
from func.src.domain.exceptions.model import UnauthorizedError
from func.src.domain.response.model import ResponseModel
from func.src.services.jwt import JwtValidator
from func.src.services.watch_list import WatchListService


async def list_assets(request: Request = request) -> Response:
    x_thebes_answer = request.headers.get("x-thebes-answer")

    try:
        jwt_content = await JwtValidator.validate(x_thebes_answer)

        unique_id = jwt_content["decoded_jwt"]["user"]["unique_id"]
        result = await WatchListService.list_assets_in_watch_list(
            unique_id
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

    except Exception as ex:
        message = "Unexpected error occurred"
        Gladsheim.error(error=ex, message=message)
        response = ResponseModel(
            success=False, code=InternalCode.INTERNAL_SERVER_ERROR, message=message
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response
