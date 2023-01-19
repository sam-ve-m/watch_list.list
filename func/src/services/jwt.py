from etria_logger import Gladsheim
from heimdall_client import Heimdall, HeimdallStatusResponses

from func.src.domain.exceptions.model import UnauthorizedError


class JwtValidator:

    @staticmethod
    async def validate(jwt: str) -> dict:
        jwt_content, heimdall_status = await Heimdall.decode_payload(
            jwt=jwt
        )
        if heimdall_status != HeimdallStatusResponses.SUCCESS:
            Gladsheim.error(status=heimdall_status)
            raise UnauthorizedError()
        return jwt_content
