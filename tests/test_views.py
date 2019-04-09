from http import HTTPStatus

import pytest
from flask import url_for
from werkzeug.datastructures import FileStorage
import os
from mock import Mock
from views import file_is_allowed, get_file_path_from_request


def test_get_index_routing(client):
    response = client.get(url_for('index'))
    assert response.status_code == HTTPStatus.OK


def test_file_is_allowed():
    assert file_is_allowed('img.png')
    assert not file_is_allowed('img.pdf')


def test_get_file_from_request():
    request = Mock()
    request.files = {}
    request.files['photo'] = FileStorage(filename=os.path.join('../tests', 'test_img.png'))
    filepath = get_file_path_from_request(request)
    assert filepath.startswith('static/images/')
