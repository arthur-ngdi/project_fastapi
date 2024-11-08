from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):
    user = User(username='arthur', email='ar@thur.com', password='senha123')

    session.add(user)
    session.commit()

    result = session.scalar(select(User).where(User.email == 'ar@thur.com'))

    assert result.username == 'arthur'
