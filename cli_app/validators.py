import re
from urllib.parse import urlparse

# source https://stackoverflow.com/a/55827638
DOMAIN_FORMAT = re.compile(
    r"(?:^(\w{1,255}):(.{1,255})@|^)"
    r"(?:(?:(?=\S{0,253}(?:$|:))"
    r"((?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+"
    r"(?:[a-z0-9]{1,63})))"
    r"|localhost)"
    r"(:\d{1,5})?",
    re.IGNORECASE
)
SCHEME_FORMAT = re.compile(
    r"^(http|hxxp|ftp|fxp)s?$",
    re.IGNORECASE
)


def validate_url(url: str):
    url = url.strip()

    if not url:
        raise Exception("No URL specified")

    if len(url) > 2048:
        raise Exception("URL exceeds its maximum length of 2048 characters (given length={})".format(len(url)))

    result = urlparse(url)
    scheme = result.scheme
    domain = result.netloc

    if not scheme:
        raise Exception("No URL scheme specified")

    if not re.fullmatch(SCHEME_FORMAT, scheme):
        raise Exception("URL scheme must either be http(s) or ftp(s) (given scheme={})".format(scheme))

    if not domain:
        raise Exception("No URL domain specified")

    if not re.fullmatch(DOMAIN_FORMAT, domain):
        raise Exception("URL domain malformed (domain={})".format(domain))

    return url


if __name__ == '__main__':
    # validate_url('google.com')
    print(validate_url('https://www.google.com/'))