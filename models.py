from typing import Dict, List, NamedTuple
from uuid import uuid4

users: Dict[str, 'User'] = {}
clients: Dict[str, 'Client'] = {}


class Client(NamedTuple):
    id: str
    fio: str
    phone: str
    email: str
    user: 'User'
    photo_path: str


def create_client(fio: str, phone: str, email: str, user: 'User', photo_path=None) -> Client:
    client_id = uuid4().hex
    new_client = Client(client_id, fio, phone, email, user, photo_path)
    user.clients.append(new_client)
    clients[client_id] = new_client
    return new_client


class User(NamedTuple):
    username: str
    password: str
    clients: List[Client]


def create_user(username: str, password: str, user_clients=None) -> User:
    if not user_clients:
        user_clients = []
    new_user = User(username, password, user_clients)
    users[username] = new_user
    return new_user
