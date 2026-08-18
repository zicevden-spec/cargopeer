from pydantic import BaseModel, ConfigDict, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    full_name: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ItemCreate(BaseModel):
    title: str
    description: str = ""
    pickup_location: str
    delivery_location: str
    reward: int = 0


class ItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    owner_id: int
    title: str
    description: str
    pickup_location: str
    delivery_location: str
    reward: int
    status: str


class OfferCreate(BaseModel):
    price: int
    comment: str = ""


class OfferOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    item_id: int
    courier_id: int
    price: int
    comment: str