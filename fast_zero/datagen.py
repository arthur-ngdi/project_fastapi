import factory  # pragma: no cover

from fast_zero.database import get_session  # pragma: no cover
from fast_zero.models import User  # pragma: no cover


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):  # pragma: no cover
    class Meta:  # pragma: no cover
        model = User

    username = factory.Faker('user_name')
    email = factory.Faker('email')
    password = factory.Faker('password')


# Criar 10 usuários e salvá-los no banco de dados
with next(get_session()) as session:  # pragma: no cover
    # Temporariamente defina a sessão no `Meta`
    UserFactory._meta.sqlalchemy_session = session
    for _ in range(10):  # pragma: no cover
        UserFactory()

    session.commit()
    UserFactory._meta.sqlalchemy_session = None
