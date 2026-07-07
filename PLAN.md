# WL — Username-Targeted Password Wordlist Generator

## Concept
Generate highly targeted password candidates for a given username by applying
structural patterns derived from real-world breach data (RockYou, SecLists, etc.).
Every generated password relates to the target username — no filler entries.

## Use Cases
1. **Offline hash cracking** — feed wordlist into Hashcat/John after dumping hashes
2. **Internal password spraying** — targeted low-and-slow attempts per user
3. **Credential pattern analysis** — understand target's password habits

## CLI
```
pip install -e .     # one-time install
wl <username> [options]

Options:
  --keywords     Custom keywords (pets, partners, etc.)
  --birth-year   Birth year (e.g. 1990)
  --year-range   Year range (default: 2020-2026)
  --leet         Apply leet substitutions
  --output FILE  Output file (default: <username>_wordlist.txt)
  --min-len      Minimum password length (default: 4)
  --max-len      Maximum password length (default: 32)
  --wordlist     External wordlist file (adds to token pools)
  --refresh      Re-download common passwords cache
```

## Architecture

### Token Pools
| Token | Source |
|---|---|
| `{name}` | username + case variants + truncations + reversed |
| `{Name}` | capitalized variants |
| `{digits}` | 0-9, 00-99, common sequences (007, 69, 123, 420), birth year, year range |
| `{special}` | `! @ # $ % & *` |
| `{year}` | birth year + year range |
| `{word}` | top alphabetic words from downloaded common passwords |
| `{l33t}` | leet-speak variants of username |
| `{keyword}` | user-supplied custom keywords |

### Pattern Templates (from breach analysis)
```
{name}{digits}         →  john123
{name}{special}        →  john!
{name}{digits}{special} →  john123!
{Name}{digits}         →  John123
{name}{year}           →  john2024
{word}{digits}         →  password123
{digits}{name}         →  123john
{name}{special}{digits} →  john!123
{l33t}{digits}         →  j0hn123
{name}{word}           →  johnpassword
{word}{name}           →  passwordjohn
{Name}{year}           →  John2024
{name}{special}{year}  →  john!2024
{name}{name}           →  johnjohn
```

### Word Pool Fetching
- Downloads SecLists 10k-most-common.txt on first run
- Extracts alphabetic words for `{word}` token pool
- Caches in `~/.cache/wl/common_passwords.txt`

## Project Structure
```
wl/
├── wl/
│   ├── __init__.py
│   ├── __main__.py        # python -m wl support
│   ├── cli.py             # argparse entry point
│   ├── generator.py       # Orchestrates pattern-based generation
│   ├── patterns.py        # Pattern templates
│   ├── tokens.py          # Token pool builders
│   ├── leet.py            # Leet substitution maps
│   └── fetcher.py         # Download + cache word pool
├── pyproject.toml         # Build config + console_scripts
├── PLAN.md
└── README.md
```

## Dependencies
Python stdlib only — `argparse`, `itertools`, `pathlib`, `urllib.request`, `re`, `hashlib`, `json`
