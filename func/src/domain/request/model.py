from pydantic import BaseModel, conint


class WatchListParameters(BaseModel):
    limit: conint(ge=0)
    offset: conint(ge=0)
