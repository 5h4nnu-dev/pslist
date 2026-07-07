import os
import sys
import urllib.request

COMMON_PASSWORDS_URL = (
    "https://raw.githubusercontent.com/danielmiessler/SecLists/"    # change 
    "master/Passwords/Common-Credentials/10k-most-common.txt"
)
CACHE_DIR = os.path.expanduser("~/.cache/wl")
CACHE_FILE = os.path.join(CACHE_DIR, "common_passwords.txt")


def _ensure_cache_dir():
    os.makedirs(CACHE_DIR, exist_ok=True)
    return CACHE_DIR


def fetch_common_passwords(refresh=False):
    _ensure_cache_dir()

    if not refresh and os.path.exists(CACHE_FILE):
        return CACHE_FILE

    print("[*] No cached word pool found — downloading common passwords...", file=sys.stderr)
    try:
        urllib.request.urlretrieve(COMMON_PASSWORDS_URL, CACHE_FILE)
        print(f"[*] Cached to {CACHE_FILE}", file=sys.stderr)
    except Exception as e:
        print(f"[!] Failed to download: {e}", file=sys.stderr)
        if os.path.exists(CACHE_FILE):
            return CACHE_FILE
        return None

    return CACHE_FILE


def extract_word_pool(wordlist_path=None, refresh=False):
    cache_file = fetch_common_passwords(refresh)
    words = set()

    sources = []
    if cache_file:
        sources.append(cache_file)
    if wordlist_path and os.path.exists(wordlist_path):
        sources.append(wordlist_path)

    for src in sources:
        try:
            with open(src, "r", errors="ignore") as f:
                for line in f:
                    word = line.strip()
                    if word and word.isalpha() and 3 <= len(word) <= 15:
                        words.add(word.lower())
        except Exception:
            pass

    return sorted(words)
