import argparse
import sys

from .generator import generate_wordlist


def main():
    parser = argparse.ArgumentParser(
        description="Generate a targeted password wordlist for a given username.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  wl john\n"
            "  wl john --leet --output john.txt\n"
            "  wl admin --birth-year 1990 --year-range 2020 2026 --keywords rocket star\n"
            "  wl alice --wordlist rockyou.txt --refresh\n"
        ),
    )
    parser.add_argument("username", help="Target username")
    parser.add_argument("--keywords", nargs="+", default=[], help="Additional keywords (pets, partners, etc.)")
    parser.add_argument("--birth-year", type=int, help="Birth year (e.g. 1990)")
    parser.add_argument("--year-range", nargs=2, type=int, default=[2020, 2026], metavar=("START", "END"), help="Year range (default: 2020 2026)")
    parser.add_argument("--leet", action="store_true", help="Apply leet speak substitutions")
    parser.add_argument("--output", help="Output file (default: <username>_wordlist.txt)")
    parser.add_argument("--min-len", type=int, default=4, help="Minimum password length (default: 4)")
    parser.add_argument("--max-len", type=int, default=32, help="Maximum password length (default: 32)")
    parser.add_argument("--wordlist", help="External wordlist file for additional tokens")
    parser.add_argument("--refresh", action="store_true", help="Re-download common passwords cache")

    args = parser.parse_args()

    output = args.output or f"{args.username}_wordlist.txt"

    passwords = generate_wordlist(
        username=args.username,
        keywords=args.keywords,
        birth_year=args.birth_year,
        year_range=tuple(args.year_range),
        leet=args.leet,
        min_len=args.min_len,
        max_len=args.max_len,
        wordlist_path=args.wordlist,
        refresh=args.refresh,
    )

    with open(output, "w") as f:
        for pwd in passwords:
            f.write(pwd + "\n")

    print(f"[*] Generated {len(passwords):,} unique candidates", file=sys.stderr)
    print(f"[*] Saved to {output}", file=sys.stderr)


if __name__ == "__main__":
    main()
