from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.deps import get_current_user
from app.models import Item, Offer, User
from app.schemas import OfferAccept, OfferCreate, OfferOut, OfferReject


router = APIRouter(prefix="/items/{item_id}/offers", tags=["offers"])


@router.post("", response_model=OfferOut, status_code=status.HTTP_201_CREATED)
async def create_offer(
    item_id: int,
    data: OfferCreate,
    courier: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    # Проверяем, что товар существует
    result = await session.execute(select(Item).where(Item.id == item_id))
    item = result.scalar_one_or_none()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    # Нельзя делать предложение на свой товар
    if item.owner_id == courier.id:
        raise HTTPException(status_code=400, detail="Cannot offer on your own item")

    offer = Offer(
        item_id=item_id,
        courier_id=courier.id,
        price=data.price,
        comment=data.comment,
    )
    session.add(offer)
    await session.commit()
    await session.refresh(offer)
    return offer


@router.get("", response_model=list[OfferOut])
async def list_offers(item_id: int, session: AsyncSession = Depends(get_session)):
    # Проверяем, что товар существует
    result = await session.execute(select(Item).where(Item.id == item_id))
    item = result.scalar_one_or_none()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    result = await session.execute(
        select(Offer).where(Offer.item_id == item_id).order_by(Offer.created_at.desc())
    )
    return result.scalars().all()


@router.post("/{offer_id}/accept", response_model=OfferOut)
async def accept_offer(
    item_id: int,
    offer_id: int,
    data: OfferAccept,
    owner: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Принять предложение курьера (только владелец товара)"""
    # Проверяем товар
    result = await session.execute(select(Item).where(Item.id == item_id))
    item = result.scalar_one_or_none()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    # Только владелец может принять предложение
    if item.owner_id != owner.id:
        raise HTTPException(status_code=403, detail="Only item owner can accept offers")

    # Проверяем предложение
    result = await session.execute(select(Offer).where(Offer.id == offer_id, Offer.item_id == item_id))
    offer = result.scalar_one_or_none()
    if offer is None:
        raise HTTPException(status_code=404, detail="Offer not found")

    # Обновляем статус предложения
    offer.status = "accepted"
    
    # Отклоняем все остальные предложения для этого товара
    result = await session.execute(
        select(Offer).where(Offer.item_id == item_id, Offer.id != offer_id, Offer.status == "pending")
    )
    for other_offer in result.scalars().all():
        other_offer.status = "rejected"

    # Обновляем статус товара
    item.status = "in_progress"

    await session.commit()
    await session.refresh(offer)
    return offer


@router.post("/{offer_id}/reject", response_model=OfferOut)
async def reject_offer(
    item_id: int,
    offer_id: int,
    data: OfferReject,
    owner: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Отклонить предложение курьера (только владелец товара)"""
    # Проверяем товар
    result = await session.execute(select(Item).where(Item.id == item_id))
    item = result.scalar_one_or_none()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    # Только владелец может отклонить предложение
    if item.owner_id != owner.id:
        raise HTTPException(status_code=403, detail="Only item owner can reject offers")

    # Проверяем предложение
    result = await session.execute(select(Offer).where(Offer.id == offer_id, Offer.item_id == item_id))
    offer = result.scalar_one_or_none()
    if offer is None:
        raise HTTPException(status_code=404, detail="Offer not found")

    # Обновляем статус предложения
    offer.status = "rejected"

    await session.commit()
    await session.refresh(offer)
    return offer