from itertools import product

LEET_MAP = {
    "a": ["4", "@"],
    "e": ["3"],
    "i": ["1", "!"],
    "o": ["0"],
    "s": ["5", "$"],
    "t": ["7"],
    "b": ["8"],
    "g": ["9"],
}


def apply_leet(text):
    if not text:
        return []

    text_lower = text.lower()
    positions = []
    for i, c in enumerate(text_lower):
        if c in LEET_MAP:
            positions.append((i, c))

    if not positions:
        return [text]

    if len(positions) > 6:
        positions = positions[:6]

    results = set()
    substitutions = []
    for _idx, char in positions:
        substitutions.append(LEET_MAP[char])

    for combo in product(*substitutions):
        chars = list(text)
        for (idx, _), sub in zip(positions, combo):
            chars[idx] = sub
        results.add("".join(chars))

    return list(results)
