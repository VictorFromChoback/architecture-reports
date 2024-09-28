from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from .dependencies import EmployeeRepository, get_employee_repo
from .jwt import create_token, verify_hashed_password
from .schemas import ResponseAuth, EmployeeData


router = APIRouter()


@router.post("", response_model=ResponseAuth)
async def auth(user: OAuth2PasswordRequestForm = Depends(),
               users_repo: EmployeeRepository = Depends(get_employee_repo)):
    user_data: EmployeeData | None = await users_repo.get_by_username(user.username)
    if user_data is None or not verify_hashed_password(user.password, user_data.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    return ResponseAuth(username=user.username,
                        role="admin",
                        access_token=create_token({"username": user.username}),
                        token_type="bearer")
