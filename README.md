# wl — Username-Targeted Password Wordlist Generator

Generate highly targeted password candidates for a given username by applying structural patterns derived from real-world breach data (RockYou, SecLists, etc.). Every generated password relates to the target username — no filler entries.

## Installation

```bash
pip install pslist   # once published
# or from source:
git clone https://github.com/5h4nnu-dev/wl.git
cd wl
pip install -e .
```

## Usage

```bash
wl <username> [options]
```

### Basic

```bash
wl john
```

Generates `john_wordlist.txt` with ~78k unique candidates using the common word pool and structural patterns.

### Options

| Flag | Description |
|------|-------------|
| `--keywords` | Custom keywords (pets, partners, etc.) |
| `--birth-year` | Birth year (e.g. 1990) |
| `--year-range` | Year range (default: 2020-2026) |
| `--leet` | Apply leet substitutions |
| `--output FILE` | Output file (default: `<username>_wordlist.txt`) |
| `--min-len` | Minimum password length (default: 4) |
| `--max-len` | Maximum password length (default: 32) |
| `--wordlist` | External wordlist file (adds to token pools) |
| `--refresh` | Re-download common passwords cache |

### Examples

```bash
wl john --leet --output john.txt
wl admin --birth-year 1990 --year-range 2020 2026 --keywords rocket star
wl alice --wordlist rockyou.txt --refresh
```

## How It Works

Token pools are built from the username (variants, truncations, reversals) and combined using structural patterns observed in real breaches:

```
{name}{digits}         →  john123
{name}{special}        →  john!
{name}{digits}{special} →  john123!
{Name}{digits}         →  John123
{name}{year}           →  john2024
{word}{digits}         →  password123
{name}{word}           →  johnpassword
{l33t}{digits}         →  j0hn123
```

### Token Sources

| Token | Source |
|-------|--------|
| `{name}` | username + case variants + truncations + reversed |
| `{Name}` | capitalized variants |
| `{digits}` | 0–99, common sequences, birth/year range |
| `{special}` | `! @ # $ % & *` |
| `{year}` | birth year + year range |
| `{word}` | top words from SecLists 10k-most-common |
| `{l33t}` | leet-speak variants |
| `{keyword}` | user-supplied custom keywords |

The common password pool is downloaded from [SecLists](https://github.com/danielmiessler/SecLists) on first run and cached at `~/.cache/wl/common_passwords.txt`.

## Use Cases

- **Offline hash cracking** — feed wordlist into Hashcat / John
- **Internal password spraying** — targeted low-and-slow attempts per user
- **Credential pattern analysis** — understand a target's password habits

## Dependencies

Python stdlib only — no third-party packages required.

## License

MIT
