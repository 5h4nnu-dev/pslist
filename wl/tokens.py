from .leet import apply_leet

COMMON_DIGITS = [
    "00", "000", "0000", "007", "069", "123", "234", "345",
    "456", "567", "678", "789", "69", "88", "420", "666",
    "777", "999", "111", "222", "333",
]


def build_name_variants(username):
    variants = set()
    u = username

    variants.add(u)
    variants.add(u.lower())
    variants.add(u.upper())
    variants.add(u.capitalize())

    rev = u[::-1]
    if len(rev) >= 3:
        variants.add(rev)
        variants.add(rev.capitalize())

    max_trunc = min(5, len(u))
    for i in range(3, max_trunc + 1):
        variants.add(u[:i].lower())
        variants.add(u[-i:].lower())

    if len(u) >= 3:
        variants.add(u.lower() * 2)

    return [v for v in variants if v]


def build_token_pools(
    username, leet=False, keywords=None,
    word_pool=None, birth_year=None, year_range=None,
):
    name_variants = build_name_variants(username)

    pools = {}

    pools["name"] = sorted(set(v.lower() for v in name_variants if v))

    pools["Name"] = sorted(set(
        v[0].upper() + v[1:].lower() if len(v) > 1 else v.upper()
        for v in name_variants if v
    ))

    pools["NAME"] = sorted(set(v.upper() for v in name_variants if v))

    if leet:
        l33t_set = set()
        for v in name_variants:
            l33t_set.update(apply_leet(v))
        pools["l33t"] = sorted(l33t_set)
    else:
        pools["l33t"] = []

    digits = set()
    for d in range(10):
        digits.add(str(d))
    for d in range(10, 100):
        digits.add(str(d))
    for seq in COMMON_DIGITS:
        digits.add(seq)

    if birth_year is not None:
        digits.add(str(birth_year))
    if year_range:
        for y in range(year_range[0], year_range[1] + 1):
            digits.add(str(y))

    pools["digits"] = sorted(digits, key=lambda x: (len(x), x))

    pools["special"] = ["!", "@", "#", "$", "%", "&", "*"]

    years = set()
    if birth_year is not None:
        years.add(str(birth_year))
    if year_range:
        for y in range(year_range[0], year_range[1] + 1):
            years.add(str(y))
    pools["year"] = sorted(years, key=lambda x: int(x))

    if word_pool:
        pools["word"] = word_pool[:500]
    else:
        pools["word"] = []

    kw = [k.lower() for k in (keywords or []) if k]
    pools["keyword"] = sorted(set(kw))
    pools["Keyword"] = sorted(set(k.capitalize() for k in kw))
    pools["KEYWORD"] = sorted(set(k.upper() for k in kw))

    return pools
