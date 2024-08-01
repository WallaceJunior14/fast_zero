import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from fast_zero.app import app
from fast_zero.models import table_registry


@pytest.fixture
def client():
    # Arrange (organização)
    return TestClient(app)


@pytest.fixture
def session():
    # Cria um banco sqlite em memoria para poder usar em teste.
    # É descado depois de utilizado.
    engine = create_engine('sqlite:///:memory:')
    # Cria todos os metadados 'Models' no banco fictício
    table_registry.metadata.create_all(engine)

    # 'with 'gerenciamento de contexto
    with Session(engine) as session:
        # 'yield' gerador
        yield session

    # Distroi o banco de dados fictício
    table_registry.metadata.drop_all(engine)
