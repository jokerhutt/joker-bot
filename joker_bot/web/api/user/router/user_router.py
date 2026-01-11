from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from joker_bot.web.api.user.dto.request.user_tag_request import UserTagRequest
from joker_bot.web.db.session import get_session
from joker_bot.web.service.user_service import UserService


router = APIRouter(prefix="/user")


@router.post("/tag")
async def update_user_tag(
    body: UserTagRequest, session: AsyncSession = Depends(get_session)
) -> str:
    response = await UserService().set_tag(
        session=session, discord_id=body.discord_id, new_tag=body.new_tag
    )
    await session.commit()
    return response


@router.get("/tag/{discord_id}")
async def get_user_Tag(
    discord_id: int, session: AsyncSession = Depends(get_session)
) -> str:
    user_tag = await UserService().get_tag(session=session, discord_id=discord_id)
    await session.commit()
    return user_tag
