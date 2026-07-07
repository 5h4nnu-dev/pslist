import sys

from .tokens import build_token_pools
from .patterns import generate_all
from .fetcher import extract_word_pool


def generate_wordlist(
    username, keywords=None, birth_year=None, year_range=None,
    leet=False, min_len=4, max_len=32, wordlist_path=None, refresh=False,
):
    word_pool = extract_word_pool(wordlist_path, refresh)
    if word_pool:
        print(f"[*] Extracted {len(word_pool):,} common words as pattern tokens", file=sys.stderr)

    pools = build_token_pools(
        username=username,
        leet=leet,
        keywords=keywords,
        word_pool=word_pool,
        birth_year=birth_year,
        year_range=year_range,
    )

    for key, values in pools.items():
        if values:
            print(f"[*] {key}: {len(values)} tokens", file=sys.stderr)

    passwords = list(generate_all(pools, min_len, max_len))
    passwords.sort()

    return passwords
