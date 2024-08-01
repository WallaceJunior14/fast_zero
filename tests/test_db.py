from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):
    user = User(
        username='wallace', email='wall@gmail.com', password='12345689'
    )

    session.add(user)
    session.commit()

    result = session.scalar(select(User).where(User.email == 'wall@gmail.com'))

    assert result.username == 'wallace'
