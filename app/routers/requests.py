from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.deps import get_current_user
from app.models import Item, Request, User
from app.schemas import RequestCreate, RequestOut

router = APIRouter(prefix="/items/{item_id}/requests", tags=["requests"])


@router.post("", response_model=RequestOut, status_code=status.HTTP_201_CREATED)
async def create_request(
    item_id: int,
    data: RequestCreate,
    requester: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    # Проверяем, что товар существует
    result = await session.execute(select(Item).where(Item.id == item_id))
    item = result.scalar_one_or_none()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    # Нельзя делать заявку на свой товар
    if item.owner_id == requester.id:
        raise HTTPException(status_code=400, detail="Cannot request your own item")

    request = Request(
        item_id=item_id,
        requester_id=requester.id,
        price=data.price,
        comment=data.comment,
    )
    session.add(request)
    await session.commit()
    await session.refresh(request)
    return request


@router.get("", response_model=list[RequestOut])
async def list_requests(item_id: int, session: AsyncSession = Depends(get_session)):
    # Проверяем, что товар существует
    result = await session.execute(select(Item).where(Item.id == item_id))
    item = result.scalar_one_or_none()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    result = await session.execute(
        select(Request).where(Request.item_id == item_id).order_by(Request.created_at.desc())
    )
    return result.scalars().all()