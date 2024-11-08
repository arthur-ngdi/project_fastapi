from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schemas import Message, UserList, UserPublic, UserSchema

app = FastAPI()

database = []


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Hello World!'}


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session=Depends(get_session)):
    db_user = session.scalar(
            select(User).where(User.username == user.username)
        )

    if db_user:
        match db_user:
            case user.username:
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail='Username already exists',
                )
            case user.email:
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail='Email already exists',
                )
    else:
        db_user = User(
                    username=user.username,
                    email=user.email,
                    password=user.password
                )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get('/users/', response_model=UserList)
def read_user(session=Depends(get_session)):

    user = session.scalars(
            select(User)
        )

    return {'users': user}


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user: UserSchema):
        db_user = session.scalar(
            select(User).where(User.id == user_id)
        )


@app.delete('/users/{user_id}', response_model=UserPublic)
def delete_user(user_id: int):
    if user_id < 1 or user_id >= len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User Not Found'
        )

    del database[user_id - 1]

    return {'users': database}
