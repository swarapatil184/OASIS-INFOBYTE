"""
╔══════════════════════════════════════════════════╗
║     Random Password Generator  - Project 3      ║
║         Enhanced CLI Version (Beginner)          ║
╚══════════════════════════════════════════════════╝
"""

import random
import string
import time
import sys
import os

# ─── ANSI Color Codes ──────────────────────────────────────────────────────────
class C:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"

    # Text colors
    RED     = "\033[91m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    BLUE    = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN    = "\033[96m"
    WHITE   = "\033[97m"
    ORANGE  = "\033[38;5;208m"
    PURPLE  = "\033[38;5;135m"
    PINK    = "\033[38;5;213m"
    LIME    = "\033[38;5;118m"

    # Background colors
    BG_DARK   = "\033[48;5;234m"
    BG_BLUE   = "\033[48;5;17m"
    BG_GREEN  = "\033[48;5;22m"
    BG_RED    = "\033[48;5;52m"
    BG_YELLOW = "\033[48;5;58m"


# ─── Utility helpers ───────────────────────────────────────────────────────────
def clear():
    os.system("cls" if os.name == "nt" else "clear")


def slow_print(text: str, delay: float = 0.018):
    """Print text character by character for typing effect."""
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def loading_bar(label: str = "Generating", width: int = 30, delay: float = 0.03):
    """Animated loading bar."""
    print(f"\n  {C.CYAN}{label}  {C.RESET}", end="")
    sys.stdout.write(f"{C.DIM}[{C.RESET}")
    for i in range(width):
        time.sleep(delay)
        colors = [C.CYAN, C.BLUE, C.MAGENTA, C.PURPLE]
        color = colors[i % len(colors)]
        sys.stdout.write(f"{color}█{C.RESET}")
        sys.stdout.flush()
    sys.stdout.write(f"{C.DIM}]{C.RESET}")
    print(f"  {C.GREEN}{C.BOLD}DONE ✔{C.RESET}\n")


def spinner(label: str, duration: float = 0.8):
    """Spinning animation."""
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        sys.stdout.write(f"\r  {C.CYAN}{frames[i % len(frames)]}{C.RESET}  {C.WHITE}{label}{C.RESET}   ")
        sys.stdout.flush()
        time.sleep(0.08)
        i += 1
    sys.stdout.write(f"\r  {C.GREEN}✔{C.RESET}  {C.WHITE}{label}{C.RESET}   \n")
    sys.stdout.flush()


def print_banner():
    """Print the main banner."""
    banner = f"""
{C.CYAN}{C.BOLD}
  ██████╗  █████╗ ███████╗███████╗██╗    ██╗ ██████╗ ██████╗ ██████╗
  ██╔══██╗██╔══██╗██╔════╝██╔════╝██║    ██║██╔═══██╗██╔══██╗██╔══██╗
  ██████╔╝███████║███████╗███████╗██║ █╗ ██║██║   ██║██████╔╝██║  ██║
  ██╔═══╝ ██╔══██║╚════██║╚════██║██║███╗██║██║   ██║██╔══██╗██║  ██║
  ██║     ██║  ██║███████║███████║╚███╔███╔╝╚██████╔╝██║  ██║██████╔╝
  ╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝ ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═════╝
{C.RESET}"""

    subtitle = f"""
{C.PURPLE}  ╔══════════════════════════════════════════════════════════════════╗{C.RESET}
{C.PURPLE}  ║{C.RESET}  {C.YELLOW}🔐  G E N E R A T O R{C.RESET}    {C.DIM}│{C.RESET}    {C.CYAN}Python Project 3  ·  Beginner{C.RESET}  {C.PURPLE}║{C.RESET}
{C.PURPLE}  ╚══════════════════════════════════════════════════════════════════╝{C.RESET}
"""
    print(banner)
    print(subtitle)


def section_header(title: str, icon: str = ""):
    print(f"\n  {C.PURPLE}{'─'*52}{C.RESET}")
    print(f"  {C.BOLD}{C.YELLOW}{icon}  {title}{C.RESET}")
    print(f"  {C.PURPLE}{'─'*52}{C.RESET}\n")


def success_box(lines: list):
    """Print a colored success box."""
    width = max(len(l) for l in lines) + 6
    print(f"\n  {C.GREEN}╔{'═'*width}╗{C.RESET}")
    for line in lines:
        padding = width - len(line) - 2
        print(f"  {C.GREEN}║{C.RESET}  {C.WHITE}{line}{C.RESET}{' '*padding}  {C.GREEN}║{C.RESET}")
    print(f"  {C.GREEN}╚{'═'*width}╝{C.RESET}")


def error_msg(msg: str):
    print(f"\n  {C.RED}╔══ ERROR ══╗{C.RESET}")
    print(f"  {C.RED}║{C.RESET}  {C.YELLOW}✗  {msg}{C.RESET}")
    print(f"  {C.RED}╚═══════════╝{C.RESET}\n")


def info_msg(msg: str):
    print(f"  {C.CYAN}ℹ  {C.RESET}{C.WHITE}{msg}{C.RESET}")


# ─── Password Logic ────────────────────────────────────────────────────────────
LETTERS = string.ascii_letters
NUMBERS = string.digits
SYMBOLS = "!@#$%^&*()-_=+[]{}|;:,.<>?"


def generate_password(length, use_letters, use_numbers, use_symbols, exclude=""):
    pool = ""
    if use_letters: pool += LETTERS
    if use_numbers: pool += NUMBERS
    if use_symbols: pool += SYMBOLS

    for ch in exclude:
        pool = pool.replace(ch, "")

    if not pool:
        raise ValueError("No characters left! Select at least one type.")

    # Guarantee at least one of each selected type
    password_chars = []
    if use_letters:
        avail = [c for c in LETTERS if c in pool]
        if avail: password_chars.append(random.choice(avail))
    if use_numbers:
        avail = [c for c in NUMBERS if c in pool]
        if avail: password_chars.append(random.choice(avail))
    if use_symbols:
        avail = [c for c in SYMBOLS if c in pool]
        if avail: password_chars.append(random.choice(avail))

    password_chars += random.choices(pool, k=max(0, length - len(password_chars)))
    random.shuffle(password_chars)
    return "".join(password_chars)


def check_strength(password):
    score = 0
    if len(password) >= 8:  score += 1
    if len(password) >= 12: score += 1
    if len(password) >= 16: score += 1
    if any(c in string.ascii_lowercase for c in password): score += 1
    if any(c in string.ascii_uppercase for c in password): score += 1
    if any(c in NUMBERS for c in password):                score += 1
    if any(c in SYMBOLS for c in password):                score += 1

    if score <= 2:
        return "Weak",   C.RED,     "▓░░░░", "Very easy to crack ✗"
    elif score <= 4:
        return "Fair",   C.YELLOW,  "▓▓▓░░", "Moderate security"
    elif score <= 5:
        return "Good",   C.ORANGE,  "▓▓▓▓░", "Hard to crack ✔"
    else:
        return "Strong", C.GREEN,   "▓▓▓▓▓", "Excellent! Highly secure ✅"


def colorize_password(password):
    """Color each character type differently."""
    result = ""
    for ch in password:
        if ch in string.ascii_uppercase:
            result += f"{C.CYAN}{C.BOLD}{ch}{C.RESET}"
        elif ch in string.ascii_lowercase:
            result += f"{C.WHITE}{ch}{C.RESET}"
        elif ch in string.digits:
            result += f"{C.YELLOW}{C.BOLD}{ch}{C.RESET}"
        else:
            result += f"{C.PINK}{C.BOLD}{ch}{C.RESET}"
    return result


# ─── Input helpers ─────────────────────────────────────────────────────────────
def get_yes_no(prompt: str) -> bool:
    while True:
        ans = input(f"  {C.WHITE}{prompt}{C.RESET} {C.DIM}(y/n){C.RESET}  {C.CYAN}›{C.RESET} ").strip().lower()
        if ans in ('y', 'yes'): return True
        if ans in ('n', 'no'):  return False
        error_msg("Please type  y  or  n")


def get_int(prompt: str, min_v: int, max_v: int) -> int:
    while True:
        try:
            v = int(input(f"  {C.WHITE}{prompt}{C.RESET} {C.DIM}[{min_v}–{max_v}]{C.RESET}  {C.CYAN}›{C.RESET} "))
            if min_v <= v <= max_v:
                return v
            error_msg(f"Enter a number between {min_v} and {max_v}")
        except ValueError:
            error_msg("Please enter a whole number")


# ─── Main ──────────────────────────────────────────────────────────────────────
def main():
    clear()
    print_banner()
    slow_print(f"  {C.DIM}Welcome! Let's create some secure passwords for you...{C.RESET}", 0.025)
    time.sleep(0.3)

    while True:
        # ── Settings ──────────────────────────────────────────────────────────
        section_header("PASSWORD SETTINGS", "⚙")

        length      = get_int("Password length?", 6, 64)
        use_letters = get_yes_no("Include letters?   (a-z, A-Z)")
        use_numbers = get_yes_no("Include numbers?   (0-9)")
        use_symbols = get_yes_no("Include symbols?   (!@#$...)")

        if not (use_letters or use_numbers or use_symbols):
            error_msg("Select at least one character type!")
            continue

        exclude = input(
            f"\n  {C.WHITE}Exclude characters?{C.RESET} {C.DIM}(e.g. 0Ol1 — or press Enter to skip){C.RESET}  {C.CYAN}›{C.RESET} "
        ).strip()

        count = get_int("How many passwords?", 1, 10)

        # ── Animate ───────────────────────────────────────────────────────────
        loading_bar("Generating passwords", width=34, delay=0.025)

        # ── Results ───────────────────────────────────────────────────────────
        section_header("YOUR PASSWORDS", "🔑")

        generated = []
        col_w = length + 4

        # Table header
        print(f"  {C.PURPLE}  #  {C.RESET}"
              f"{C.PURPLE}{'PASSWORD':<{col_w}}{C.RESET}"
              f"{C.PURPLE}{'STRENGTH':<14}{C.RESET}"
              f"{C.PURPLE}BAR     {C.RESET}"
              f"{C.PURPLE}NOTE{C.RESET}")
        print(f"  {C.DIM}{'─'*70}{C.RESET}")

        for i in range(1, count + 1):
            try:
                pwd = generate_password(length, use_letters, use_numbers, use_symbols, exclude)
                label, color, bar, note = check_strength(pwd)
                colored_pwd = colorize_password(pwd)

                # The colored password has ANSI codes so we pad manually
                print(f"  {C.BOLD}{C.YELLOW} {i:<2} {C.RESET}"
                      f"{colored_pwd}{'':>{max(0, col_w - length)}} "
                      f"{color}{C.BOLD}{label:<10}{C.RESET}"
                      f"{color}{bar}{C.RESET}  "
                      f"{C.DIM}{note}{C.RESET}")
                generated.append(pwd)
            except ValueError as e:
                error_msg(str(e))
                break

        print(f"\n  {C.DIM}{'─'*70}{C.RESET}")
        print(f"  {C.DIM}Legend:  "
              f"{C.CYAN}UPPER{C.RESET}{C.DIM}  "
              f"{C.WHITE}lower{C.RESET}{C.DIM}  "
              f"{C.YELLOW}Digit{C.RESET}{C.DIM}  "
              f"{C.PINK}Symbol{C.RESET}")

        # ── Copy option ───────────────────────────────────────────────────────
        if generated:
            section_header("COPY A PASSWORD", "📋")
            choice_str = input(
                f"  {C.WHITE}Enter number to copy  {C.DIM}[1–{len(generated)}] or Enter to skip{C.RESET}  {C.CYAN}›{C.RESET} "
            ).strip()

            if choice_str.isdigit():
                idx = int(choice_str) - 1
                if 0 <= idx < len(generated):
                    selected = generated[idx]
                    copied = False
                    try:
                        import pyperclip
                        pyperclip.copy(selected)
                        copied = True
                    except ImportError:
                        pass

                    if copied:
                        spinner("Copying to clipboard", 0.6)
                        success_box([
                            f"Password #{int(choice_str)} copied to clipboard!",
                            f"Paste it anywhere with  Ctrl+V"
                        ])
                    else:
                        success_box([
                            f"Selected Password #{int(choice_str)}:",
                            f"  {selected}",
                            "Select the password above and copy manually."
                        ])

        # ── Security tips ─────────────────────────────────────────────────────
        section_header("SECURITY TIPS", "💡")
        tips = [
            "Never reuse the same password on multiple sites.",
            "Use a password manager to store passwords safely.",
            "Enable 2-Factor Authentication (2FA) wherever possible.",
            "Avoid using personal info (birthdays, names) in passwords.",
        ]
        for tip in tips:
            slow_print(f"  {C.CYAN}›{C.RESET}  {C.DIM}{tip}{C.RESET}", 0.008)
            time.sleep(0.05)

        # ── Continue? ─────────────────────────────────────────────────────────
        print()
        again = get_yes_no("Generate more passwords?")
        if not again:
            print(f"\n  {C.PURPLE}{'═'*52}{C.RESET}")
            slow_print(f"  {C.BOLD}{C.CYAN}  Stay safe and secure! Goodbye. 🔐{C.RESET}", 0.03)
            print(f"  {C.PURPLE}{'═'*52}{C.RESET}\n")
            break

        clear()
        print_banner()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n  {C.YELLOW}Interrupted. Goodbye! 🔐{C.RESET}\n")
