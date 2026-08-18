from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.deps import get_current_user
from app.models import Item, Offer, User
from app.schemas import OfferCreate, OfferOut

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