# app/routes/user_routes.py
from fastapi import APIRouter, HTTPException, Depends, status
from app.models.user_model import User
from app.schemas.users_schema import UserUpdate, UserResponse
from app.routes.auth_routes import get_current_user
from app.utils.auth import hash_password
from beanie import PydanticObjectId

router = APIRouter(prefix="/users", tags=["Users"])

# READ (all) - Protected
@router.get("/", response_model=list[UserResponse])
async def get_all_users(current_user: User = Depends(get_current_user)):
    """Get all users (requires authentication)"""
    users = await User.find_all().to_list()
    return [
        UserResponse(
            id=str(user.id),
            name=user.name,
            email=user.email,
            is_active=user.is_active,
            is_verified=user.is_verified,
            created_at=user.created_at
        ) for user in users
    ]


# READ (single) - Protected
@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: PydanticObjectId,
    current_user: User = Depends(get_current_user)
):
    """Get a specific user by ID (requires authentication)"""
    user = await User.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserResponse(
        id=str(user.id),
        name=user.name,
        email=user.email,
        is_active=user.is_active,
        is_verified=user.is_verified,
        created_at=user.created_at
    )


# UPDATE - Protected (users can only update themselves)
@router.put("/me", response_model=UserResponse)
async def update_current_user(
    update_data: UserUpdate,
    current_user: User = Depends(get_current_user)
):
    """Update current user's information"""
    update_dict = update_data.model_dump(exclude_unset=True)
    
    # Hash password if it's being updated
    if "password" in update_dict and update_dict["password"]:
        update_dict["password"] = hash_password(update_dict["password"])
    
    for key, value in update_dict.items():
        setattr(current_user, key, value)

    await User.update(current_user)
    # await current_user.save()
    
    return UserResponse(
        id=str(current_user.id),
        name=current_user.name,
        email=current_user.email,
        is_active=current_user.is_active,
        is_verified=current_user.is_verified,
        created_at=current_user.created_at
    )


# DELETE - Protected (users can only delete themselves)
@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_current_user(current_user: User = Depends(get_current_user)):
    """Delete current user's account"""
    await User.delete(current_user)
    # await current_user.delete()
    return None