import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session

from fast_zero.app import app
from fast_zero.database import get_session
from fast_zero.models import User, table_registry
from fast_zero.security import get_password_hash


# Função para criar a sessão de teste.
# Sobrescrita da sessão de prod. para a seesão de dev. enquanto faz os testes
@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        # Troca a sessão principal (depends) para a de teste.
        app.dependency_overrides[get_session] = get_session_override

        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    # Cria um banco sqlite em memoria para poder usar em teste.
    # É descartado depois de utilizado.
    # Como o SQLAlchmy funciona em mult-threads, ele desabilita a verificação.
    # Assim não, as threads podem se comunicar, sem problema
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    # Cria todos os metadados 'Models' no banco fictício
    table_registry.metadata.create_all(engine)

    # 'with 'gerenciamento de contexto
    with Session(engine) as session:
        # 'yield' gerador
        yield session

    # Distroi o banco de dados fictício
    table_registry.metadata.drop_all(engine)


@pytest.fixture
def user(session):
    pwd = 'testest'

    user = User(
        username='wallace',
        email='wallace@gmail.com',
        password=get_password_hash(pwd),
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    # monkey patch
    user.clean_password = pwd

    return user


@pytest.fixture
def token(client, user):
    response = client.post(
        '/token',
        data={'username': user.email, 'password': user.clean_password},
    )

    return response.json()['access_token']
