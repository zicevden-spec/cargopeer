from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.deps import get_current_user
from app.models import Item, User
from app.schemas import ItemCreate, ItemOut

router = APIRouter(prefix="/items", tags=["items"])


@router.post("", response_model=ItemOut, status_code=status.HTTP_201_CREATED)
async def create_item(
    data: ItemCreate,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    item = Item(
        owner_id=user.id,
        title=data.title,
        description=data.description,
        pickup_location=data.pickup_location,
        delivery_location=data.delivery_location,
        reward=data.reward,
    )
    session.add(item)
    await session.commit()
    await session.refresh(item)
    return item


@router.get("", response_model=list[ItemOut])
async def list_items(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Item).order_by(Item.created_at.desc()))
    return result.scalars().all()


@router.get("/{item_id}", response_model=ItemOut)
async def get_item(item_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Item).where(Item.id == item_id))
    item = result.scalar_one_or_none()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item