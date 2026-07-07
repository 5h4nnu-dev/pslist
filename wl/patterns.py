import re
from itertools import product

TOKEN_RE = re.compile(r"\{(\w+)\}")

PATTERNS = [
    "{name}{digits}",
    "{name}{special}",
    "{name}{digits}{special}",
    "{Name}{digits}",
    "{Name}{special}",
    "{name}{year}",
    "{word}{digits}",
    "{digits}{name}",
    "{name}{special}{digits}",
    "{l33t}{digits}",
    "{name}{word}",
    "{word}{name}",
    "{Name}{year}",
    "{name}{special}{year}",
    "{name}{keyword}",
    "{keyword}{name}",
    "{Keyword}{digits}",
    "{name}{special}{keyword}",
    "{keyword}{special}{digits}",
]


def generate_for_pattern(pattern, pools, min_len, max_len):
    tokens = TOKEN_RE.findall(pattern)

    token_lists = []
    for t in tokens:
        vals = pools.get(t)
        if not vals:
            return
        token_lists.append(vals)

    for combo in product(*token_lists):
        pwd = pattern.format(**dict(zip(tokens, combo)))
        if min_len <= len(pwd) <= max_len:
            yield pwd


def generate_all(pools, min_len=4, max_len=32):
    seen = set()
    for pattern in PATTERNS:
        for pwd in generate_for_pattern(pattern, pools, min_len, max_len):
            if pwd not in seen:
                seen.add(pwd)
                yield pwd
