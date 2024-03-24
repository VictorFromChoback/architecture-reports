import typing as tp

from fastapi import Depends, HTTPException, status

from ...database import get_session
from .jwt import decode_token, oath_scheme
from .repository import EmployeeRepository
from .schemas import EmployeeData, Roles


def get_employee_repo(session=Depends(get_session)) -> EmployeeRepository:
    repo = EmployeeRepository(async_session=session)
    yield repo


async def get_current_user(users_repo: EmployeeRepository = Depends(get_employee_repo),
                           token: str = Depends(oath_scheme)) -> EmployeeData:
    try:
        payload = decode_token(token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    user = await users_repo.get_by_username(payload["username"])
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


async def get_current_admin(current_user: EmployeeData = Depends(get_current_user)):
    if current_user.role != Roles.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Method for admin")
    return current_user


CurrentUser = tp.Annotated[EmployeeData, Depends(get_current_user)]
CurrentAdmin = tp.Annotated[EmployeeData, Depends(get_current_admin)]
EmployeeRepo = tp.Annotated[EmployeeRepository, Depends(get_employee_repo)]
