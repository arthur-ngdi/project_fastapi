import factory

from fast_zero.database import get_session
from fast_zero.models import User


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    email = factory.Faker('email')
    password = factory.Faker('password')


# Criar 10 usuários e salvá-los no banco de dados
with next(get_session()) as session:
    # Temporariamente defina a sessão no `Meta`
    UserFactory._meta.sqlalchemy_session = session
    for _ in range(10):
        UserFactory()
    # Remova a sessão após o uso (opcional)
    session.commit()
    UserFactory._meta.sqlalchemy_session = None
