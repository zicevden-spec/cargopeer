from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.deps import get_current_user
from app.models import Item, Request, User
from app.schemas import RequestAccept, RequestCreate, RequestOut, RequestReject


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


@router.post("/{request_id}/accept", response_model=RequestOut)
async def accept_request(
    item_id: int,
    request_id: int,
    data: RequestAccept,
    owner: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Принять заявку получателя (только владелец товара)"""
    # Проверяем товар
    result = await session.execute(select(Item).where(Item.id == item_id))
    item = result.scalar_one_or_none()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    # Только владелец может принять заявку
    if item.owner_id != owner.id:
        raise HTTPException(status_code=403, detail="Only item owner can accept requests")

    # Проверяем заявку
    result = await session.execute(select(Request).where(Request.id == request_id, Request.item_id == item_id))
    request = result.scalar_one_or_none()
    if request is None:
        raise HTTPException(status_code=404, detail="Request not found")

    # Обновляем статус заявки
    request.status = "accepted"
    
    # Отклоняем все остальные заявки для этого товара
    result = await session.execute(
        select(Request).where(Request.item_id == item_id, Request.id != request_id, Request.status == "pending")
    )
    for other_request in result.scalars().all():
        other_request.status = "rejected"

    # Обновляем статус товара
    item.status = "in_progress"

    await session.commit()
    await session.refresh(request)
    return request


@router.post("/{request_id}/reject", response_model=RequestOut)
async def reject_request(
    item_id: int,
    request_id: int,
    data: RequestReject,
    owner: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Отклонить заявку получателя (только владелец товара)"""
    # Проверяем товар
    result = await session.execute(select(Item).where(Item.id == item_id))
    item = result.scalar_one_or_none()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    # Только владелец может отклонить заявку
    if item.owner_id != owner.id:
        raise HTTPException(status_code=403, detail="Only item owner can reject requests")

    # Проверяем заявку
    result = await session.execute(select(Request).where(Request.id == request_id, Request.item_id == item_id))
    request = result.scalar_one_or_none()
    if request is None:
        raise HTTPException(status_code=404, detail="Request not found")

    # Обновляем статус заявки
    request.status = "rejected"

    await session.commit()
    await session.refresh(request)
    return request