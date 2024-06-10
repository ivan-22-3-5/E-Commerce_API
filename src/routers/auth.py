from datetime import timedelta, datetime, UTC
from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response
from fastapi.security import OAuth2PasswordRequestForm

from src.custom_exceptions import InvalidCredentialsError, InvalidTokenError
from src.schemas.token import Token
from src.schemas.message import Message
from src.crud import users, refresh_tokens
from src.config import settings
from src.deps import token_dependency, db_dependency
from src.utils import create_jwt_token, get_user_id_from_jwt, verify_password

router = APIRouter(
    prefix='/auth',
    tags=["Authentication"]
)


@router.post('/token', response_model=Token)
async def login(user_credentials: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency,
                response: Response):
    user = await users.get_by_email(user_credentials.username, db)
    if not (user and verify_password(user_credentials.password, user.password)):
        raise InvalidCredentialsError("No account with the given email exists or the password is wrong")
    access_token = create_jwt_token(data={"sub": str(user.id)},
                                    expires_in=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh_token = create_jwt_token(data={"sub": str(user.id)},
                                     expires_in=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS))
    if await refresh_tokens.get_by_user_id(user.id, db=db):
        await refresh_tokens.update(user_id=user.id, new_token=refresh_token, db=db)
    else:
        await refresh_tokens.add(user_id=user.id, token=refresh_token, db=db)
    response.set_cookie(key="refresh_token",
                        value=refresh_token,
                        httponly=True,
                        secure=False,
                        expires=datetime.now(UTC) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
                        samesite=settings.SAME_SITE_COOKIE)
    return {'access_token': access_token, "token_type": "bearer"}


@router.get('/refresh', response_model=Token)
async def refresh(req: Request, res: Response, db: db_dependency):
    token = req.cookies.get('refresh_token')
    if not token:
        raise InvalidTokenError("No token found")
    user_id = get_user_id_from_jwt(token)
    db_token = await refresh_tokens.get_by_user_id(user_id, db)
    if not (db_token and db_token == token):
        raise InvalidTokenError("Invalid refresh token")
    access_token = create_jwt_token(data={"sub": str(user_id)},
                                    expires_in=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh_token = create_jwt_token(data={"sub": str(user_id)},
                                     expires_in=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS))
    await refresh_tokens.update(user_id=user_id, new_token=refresh_token, db=db)
    res.set_cookie(key="refresh_token",
                   value=refresh_token,
                   httponly=True,
                   secure=False,
                   expires=datetime.now(UTC) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
                   samesite=settings.SAME_SITE_COOKIE)
    return {'access_token': access_token, "token_type": "bearer"}


@router.delete('/logout', response_model=Message)
async def refresh(token: token_dependency, res: Response, db: db_dependency):
    user_id = get_user_id_from_jwt(token)
    await refresh_tokens.delete(user_id=user_id, db=db)
    res.delete_cookie('refresh_token')
    return Message(message='logged out')
