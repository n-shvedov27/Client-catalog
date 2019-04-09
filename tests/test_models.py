from models import create_client, create_user, users, clients


def test_create_user():
    user = create_user('Username', '1234')
    assert len(users) == 1
    assert user.username == 'Username'
    assert user.password == '1234'


def test_create_client():
    user = create_user('Username', '1234')
    client = create_client('Name', '899920068885', 'n.shvedov27@gmail.com', user)
    assert len(clients) == 1
    assert len(users) == 1
    assert client.fio == 'Name'
    assert client.phone == '899920068885'
    assert client.email == 'n.shvedov27@gmail.com'
    assert client.user == user

