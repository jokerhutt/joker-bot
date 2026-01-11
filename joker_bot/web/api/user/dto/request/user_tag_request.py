from pydantic import BaseModel


class UserTagRequest(BaseModel):
    discord_id: int
    new_tag: str
