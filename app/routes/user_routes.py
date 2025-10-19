from fastapi import APIRouter, HTTPException
from app.models.user_model import User
from app.schemas.users_schema import UserCreate, UserUpdate
from beanie import PydanticObjectId

router = APIRouter(prefix="/users", tags=["Users"])

# READ (all)
@router.get("/", response_model=list[User])
async def get_all_users():
    users = await User.find_all().to_list()
    return users


# READ (single)
@router.get("/{user_id}", response_model=User)
async def get_user(user_id: PydanticObjectId):
    user = await User.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# CREATE
@router.post("/", response_model=User)
async def create_user(user_data: UserCreate):
    user = await User.find_one(User.email == user_data.email)
    if user:
        raise HTTPException(status_code=400, detail="Email already exists")
    new_user = User(**user_data.model_dump())
    await new_user.insert()
    return new_user

# UPDATE
@router.put("/{user_id}", response_model=User)
async def update_user(user_id: PydanticObjectId, update_data: UserUpdate):
    user = await User.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    update_dict = update_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(user, key, value)

    await user.save()
    return user


# DELETE
@router.delete("/{user_id}")
async def delete_user(user_id: PydanticObjectId):
    user = await User.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await user.delete()
    return {"detail": "User deleted successfully"}