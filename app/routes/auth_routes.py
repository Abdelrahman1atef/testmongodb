# app/routes/auth_routes.py
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.models.user_model import User
from app.schemas.users_schema import UserCreate, UserLogin, Token, UserResponse
from app.utils.auth import hash_password, verify_password, create_access_token, decode_access_token, oauth2_scheme
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate):
    """Register a new user"""
    # Check if user already exists
    existing_user = await User.find_one(User.email == user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    # Hash the password
    hashed_password = hash_password(user_data.password)
    print("Hashed password:", hashed_password)
    # Create new user
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        password=hashed_password
    )
    # call the class-level insert function and pass the instance explicitly
    await User.insert(new_user)
    # await new_user.insert()
    
    # Return user response (excluding password)
    return UserResponse(
        id=str(new_user.id),
        name=new_user.name,
        email=new_user.email,
        is_active=new_user.is_active,
        is_verified=new_user.is_verified,
        created_at=new_user.created_at
    )


@router.post("/login", response_model=Token)
async def login(user_credentials: UserLogin):
    """Login user and return JWT token"""
    # Find user by email
    user = await User.find_one(User.email == user_credentials.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verify password
    if not verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive"
        )
    
    # Create access token
    access_token = create_access_token(
        data={"sub": user.email, "user_id": str(user.id)}
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/token", response_model=Token)
async def login_form(form_data: OAuth2PasswordRequestForm = Depends()):
    """OAuth2 compatible login (for Swagger UI)"""
    user = await User.find_one(User.email == form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(
        data={"sub": user.email, "user_id": str(user.id)}
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """Dependency to get current authenticated user"""
    payload = decode_access_token(token)
    email = payload.get("sub")
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = await User.find_one(User.email == email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current authenticated user information"""
    return UserResponse(
        id=str(current_user.id),
        name=current_user.name,
        email=current_user.email,
        is_active=current_user.is_active,
        is_verified=current_user.is_verified,
        created_at=current_user.created_at
    )