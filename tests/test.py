from io import StringIO
from http import HTTPStatus
from random import randint
import sys

import pytest
import requests


class MockResponce:
    __attrs__ = [
        "status_code"
    ]

    def __init__(self):
        self.status_code = None


def test__get_input():
    # подумать, как сделать mock или monkeypatch
    sys.stdin = StringIO('https://google.com\nabc\nmos.ru')
    from cli_app import app
    func_name = '_get_input'
    strings = app._get_input()

    assert isinstance(strings, list), (
        f'Проверьте, что функция {func_name} возвращает список из строк'
    )
    assert strings == ['https://google.com', 'abc', 'mos.ru'], (
        f'Проверьте, что функция {func_name}'
        'принимает все аргументы, переданные пользователем'
    )


@pytest.mark.parametrize(
    'input_data, expected', [
        ('abc', False),
        ('https://vk', False),
        ('https://vk.', False),
        ('https:/vk.', False),
        ('vk.com', False),
        ('https://google.com', True),
        ('http://facebook.com', True),
        ('https://ya.ru/', True),
        ('https://www.google.com/search?q=http+options&oq=http+o&aqs=chrome.1.69i57j0i512l2j69i60l3j69i65l2.5949j0j7&sourceid=chrome&ie=UTF-8', True),
        ('http://localhost:8000', True),
        ('http://127.0.0.1:8000', True),
        ('http://82.146.29.191:4000/', True),
    ]
)
def test__is_link(input_data, expected):
    from cli_app import app
    link = app._is_link(input_data)
    func_name = '_is_link'
    assert link == expected, (
        f'Проверьте, что функция {func_name}'
        f'Корректно обрабатывает запросы вида "{link}"'
    )


@pytest.mark.parametrize(
    'input_data, expected', [
        (randint(100, 103), True),
        (randint(200, 208), True),
        (208, True),
        (randint(300, 308), True),
        (randint(400, 404), True),
        (randint(406, 418), True),
        (randint(421, 426), True),
        (randint(428, 429), True),
        (431, True),
        (451, True),
        (randint(500, 508), True),
        (randint(510, 511), True),
        (405, False)
    ]
)
def test__is_code_allowed(input_data, expected):
    from cli_app import app

    code_allowed = app._is_code_allowed(input_data)
    assert code_allowed == expected, (
        'Проверьте, что программа считает доступным метод'
        'с любым кодом кроме 405'
    )


@pytest.mark.parametrize(
    'input_data, expected', (
        ('GET', 200),
        ('POST', 200),
        ('PUT', 200),
        ('PATCH', 200),
        ('DELETE', 200),
        ('HEAD', 200),
        ('OPTIONS', 200),
        ('TRACE', 200),
        ('CONNECT', 200)
    )
)
def test__get_available_methods_allowed(monkeypatch, input_data, expected):

    def mock_request(*args, **kwargs):
        responce = MockResponce()
        responce.status_code = HTTPStatus.OK
        return responce

    monkeypatch.setattr(requests, 'request', mock_request)
    func_name = '_get_available_methods'
    from cli_app import app
    try:
        methods = app._get_available_methods("https://fakeurl")
    except:
        pass
    else:
        assert len(methods) == 9, (
            'Проверьте, что программа считает доступным метод'
            'с любым кодом кроме 405'
        )
        assert methods.get(input_data) == expected, (
            f'Проверьте, что функция {func_name}'
            'корректно забирает status_code ответа'
        )


def test__get_available_methods_some_methods_not_allowed(monkeypatch):

    def mock_responce_with_not_allowed_methods(*args, **kwargs):
        responce = MockResponce()
        if args[0] in ['GET', 'HEAD', 'OPTIONS', 'CONNECT']:
            responce.status_code = HTTPStatus.METHOD_NOT_ALLOWED
        else:
            responce.status_code = HTTPStatus.OK
        return responce

    monkeypatch.setattr(requests, 'request', mock_responce_with_not_allowed_methods)

    from cli_app import app
    try:
        methods = app._get_available_methods("https://fakeurl")
    except:
        pass
    else:
        assert len(methods) == 5, (
            'Проверьте, что программа считает доступным метод'
            'с любым кодом кроме 405'
        )
        assert methods.values() == ['POST', 'PUT', 'PATCH', 'DELETE', 'TRACE'], (
            'Проверьте, что программа считает доступным метод'
            'с любым кодом кроме 405'
        )


def test__iterate_through_lines_prints_strings(capsys):

    from cli_app import app
    try:
        links_dict = app._iterate_through_lines(['mos.ru'])
        captured = capsys.readouterr()
    except:
        pass
    else:
        assert captured.out == 'Строка "mos.ru" не является ссылкой\n', (
            'Проверьте, что программа выводит в терминал сообщение'
            '"Строка "mos.ru" не является ссылкой"'
        )
        assert links_dict == {}, (
            'Проверьте, что программа возвращает пустой словарь,'
            'если в запросе нет ссылок'
        )


def test__iterate_through_lines_returns_valid_dict(monkeypatch, capsys):

    def mock_get_available_methods(*args, **kwargs):
        return {'GET': 300, 'PUT': 100}

    def mock__is_link(*args, **kwargs):
        return True

    from cli_app import app

    monkeypatch.setattr(app, '_get_available_methods', mock_get_available_methods)
    monkeypatch.setattr(app, '_is_link', mock__is_link)

    try:
        links_dict = app._iterate_through_lines(["https://fakeurl", "https://fakeurl"])
    except:
        pass
    else:
        assert len(links_dict) == 1, (
            'Проверьте, что программа не дублирует ссылки'
        )
        assert links_dict.get("https://fakeurl") == {'GET': 300, 'PUT': 100}, (
            'Проверьте, что программа сохраняет данные в словарь'
        )
