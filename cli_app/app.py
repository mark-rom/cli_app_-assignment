from http import HTTPStatus
from typing import Dict, List

from requests import request

from validators import validate_url

HTTP_METHODS = [
    'GET', 'POST', 'PUT', 'PATCH', 'DELETE',
    'HEAD', 'OPTIONS', 'TRACE', 'CONNECT'
]


def read_cli_and_check_links() -> Dict[str, Dict[str, int]]:
    lines = _get_input()
    return _iterate_through_lines(lines)


def _get_input() -> List[str]:
    """Read strings from comand line."""

    lines = []

    while True:
        try:
            line = input()
        except EOFError:
            break
        lines.append(line)

    return lines


def _is_link(string: str) -> bool:

    try:
        validate_url(string)

    except Exception:
        return False

    return True


def _is_code_allowed(status_code: int) -> bool:

    return status_code != HTTPStatus.METHOD_NOT_ALLOWED


def _get_available_methods(
    link: str, methods_list: List[str] = HTTP_METHODS
) -> Dict[str, int]:

    avalable_methods = {}

    for method in methods_list:
        responce = request(method, link)
        status_code = responce.status_code

        if _is_code_allowed(status_code):
            avalable_methods[method] = status_code

    return avalable_methods


def _iterate_through_lines(lines: List[str]) -> Dict[str, Dict[str, int]]:
    links = {}

    for line in lines:

        if not _is_link(line):
            print(f'Строка "{line}" не является ссылкой')
            continue

        if links.get(line):
            continue

        methods = _get_available_methods(line)
        links[line] = methods

    return links


def main() -> None:
    print(read_cli_and_check_links())


if __name__ == '__main__':
    main()
