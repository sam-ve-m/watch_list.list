from pydantic import BaseModel, validator


class WatchListParameters(BaseModel):
    limit: int
    offset: int

    @validator("limit")
    def limit_must_be_greather_than_zero(cls, limit):
        if limit < 0:
            raise ValueError("Limit must be greather than or equal to 0")
        return limit

    @validator("offset")
    def limit_must_be_greather_than_or_equal_to_zero(cls, offset):
        if offset < 0:
            raise ValueError("Offset must be greather than or equal to 0")
        return offset
