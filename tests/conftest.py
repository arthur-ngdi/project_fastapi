import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from fast_zero.app import app
from fast_zero.database import get_session
from fast_zero.models import table_registry
from fast_zero.settings import Settings


@pytest.fixture
def client(session):

    def get_session_test():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_test()

        yield client
    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine(
        Settings().DATABASE_URL_TEST,
        connect_args={'check_same_thread': False},
        poolclass=StaticPool
    )

    table_registry.metadata.create_all(engine)

    # Gerenciamento de contexto
    with Session(engine) as session:
        yield session
    table_registry.metadata.drop_all(engine)