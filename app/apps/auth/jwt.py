from fastapi import HTTPException, Request, status
from fastapi.security import HTTPBearer, OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from ...configs import app_settings


crypto_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    return crypto_context.hash(password)


def verify_hashed_password(password: str, hashed_password: str) -> bool:
    return crypto_context.verify(password, hashed_password)


def create_token(values) -> str:
    values_ = values.copy()
    return jwt.encode(values_, app_settings.token.secret, algorithm=app_settings.token.jwt_algo)


def decode_token(token: str):
    try:
        encoded = jwt.decode(token, app_settings.token.secret, algorithms=[app_settings.token.jwt_algo])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid auth token")
    return encoded


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials = await super().__call__(request)
        if credentials:
            return decode_token(credentials.credentials)
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Missed auth token")


oath_scheme = OAuth2PasswordBearer(tokenUrl="login")
