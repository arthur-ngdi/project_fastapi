from datetime import datetime, timedelta
from http import HTTPStatus

import bcrypt
import pytz

# from zoneinfo import ZoneInfo
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError, decode, encode
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.settings import Settings

from .models import User

pwd_context = bcrypt.gensalt()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


def get_password_hash(password: str):
    return bcrypt.hashpw(password.encode('utf-8'),
                                      pwd_context).decode('utf-8')


def verify_password(plain_password: str, hashed_password: str):
    return bcrypt.checkpw(plain_password.encode('utf-8'),
                          hashed_password.encode('utf-8'))


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(tz=pytz.UTC) + timedelta(
        minutes=Settings().ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({'exp': expire})
    encode_jwt = encode(to_encode, Settings().SECRET_KEY,
                        algorithm=Settings().ALGORITHM)

    return encode_jwt


def get_current_user(
    session: Session = Depends(get_session),
    token: User = Depends(oauth2_scheme),
):

    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'}
    )
    try:
        payload = decode(token,
                         Settings().SECRET_KEY,
                         algorithms=Settings().ALGORITHM,
                    )
        username = payload.get('sub')
        if not username:
            raise credentials_exception
    except PyJWTError:
        raise credentials_exception

    user_db = session.scalar(select(User).where(User.email == username))

    if not user_db:
        raise credentials_exception

    return user_db
