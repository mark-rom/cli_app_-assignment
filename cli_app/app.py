import re
from http import HTTPStatus
from typing import Dict, List

from requests import request

from validators import validate_url

HTTP_METHODS = [
    'get', 'post', 'put', 'patch', 'delete',
    'head', 'options', 'trace', 'connect'
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

    # if re.match(
    # source https://daringfireball.net/2010/07/improved_regex_for_matching_urls
    # есть еще кириллические урлы, этот зверь их не ест, да и они мало распространены
    #     r"""(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))""",
    #     string
    # ):
    #     return True
    # return False

    try:
        validate_url(string)

    except Exception:
        return False

    return True


def _get_available_methods(
    link: str, methods_list: List[str] = HTTP_METHODS
) -> Dict[str, int]:

    avalable_methods = {}

    for method in methods_list:
        # request не принимает урлы типа www.vk.com. Только со схемой
        responce = request(method, link)

        if responce.status_code != HTTPStatus.METHOD_NOT_ALLOWED:
            avalable_methods[responce.request.method] = responce.status_code

    return avalable_methods


def _iterate_through_lines(lines: List[str]) -> Dict[str, Dict[str, int]]:
    links = {}

    for line in lines:

        if not _is_link(line):
            print(f'Строка "{line}" не является ссылкой')
            continue

        if links.get(line):
            # проверка на наличие ссылки в ответе
            continue

        methods = _get_available_methods(line)
        links[line] = methods

    return links


def main() -> None:
    print(read_cli_and_check_links())


if __name__ == '__main__':
    main()
