"""
Extract Spotify cookies from browser and save to sessions.json

IMPORTANT COOKIES TO COPY:
- sp_dc (essential for authentication)
- sp_key (essential for authentication)
- wp_access_token (for API access)
- wp_refresh_token (for refreshing sessions)
- sp_t, sp_gaid (additional session data)

Methods to get cookies from your browser:

1. MANUAL COPY (Ctrl+C method):
   - Open https://open.spotify.com (make sure you're logged in)
   - Open DevTools (F12 or Right-click -> Inspect)
   - Go to Application/Storage -> Cookies -> https://open.spotify.com
   - Select all cookies (Ctrl+A), then copy (Ctrl+C)
   - Paste below - the script handles any format!
"""

import json
from pathlib import Path


def parseCookieString(cookieString: str) -> dict:
    """Parse cookie string into dictionary."""
    cookies = {}

    # Handle different cookie formats
    lines = cookieString.strip().split('\n')

    for line in lines:
        line = line.strip()

        if not line:
            continue

        # Try tab-separated format (Name\tValue\tDomain\tPath\t...)
        if '\t' in line:
            parts = line.split('\t')

            if len(parts) >= 2:
                name = parts[0].strip()
                value = parts[1].strip()

                if name and value != 'VALUE':  # Skip header
                    cookies[name] = value

        # Try semicolon-separated format
        elif ';' in line and '=' in line:
            for item in line.split(';'):
                item = item.strip()

                if '=' in item:
                    key, value = item.split('=', 1)
                    cookies[key.strip()] = value.strip()

        # Try single cookie format (name=value)
        elif '=' in line and not line.startswith('#'):
            key, value = line.split('=', 1)
            cookies[key.strip()] = value.strip()

    return cookies


def validateSpotifyCookies(cookies: dict) -> tuple[bool, list[str]]:
    """Check if we have the essential Spotify cookies."""

    essentialCookies = ['sp_dc', 'sp_key']
    importantCookies = [
        'wp_access_token',
        'wp_refresh_token',
        'sp_t',
        'sp_gaid'
    ]

    foundEssential = [
        cookie for cookie in essentialCookies
        if cookie in cookies
    ]

    foundImportant = [
        cookie for cookie in importantCookies
        if cookie in cookies
    ]

    hasEssential = len(foundEssential) > 0
    warnings = []

    if not hasEssential:
        warnings.append(
            "No essential Spotify cookies found (sp_dc, sp_key)"
        )

    if not foundImportant:
        warnings.append(
            "No authentication tokens found - session may expire quickly"
        )

    return hasEssential, warnings


def parseBrowserExport(data: str) -> dict:
    """Try to parse various browser export formats."""
    return parseCookieString(data)


def saveSession(
    cookies: dict,
    identifier: str,
    outputFile: str = "sessions.json"
) -> bool:
    """Save cookies to sessions.json file."""

    session = {
        "identifier": identifier,
        "cookies": cookies
    }

    # Create or append to sessions.json
    sessions = []
    outputPath = Path(outputFile)

    if outputPath.exists():
        try:
            with open(outputPath, 'r') as file:
                sessions = json.load(file)

        except Exception:
            sessions = []

    sessions = [
        sessionData
        for sessionData in sessions
        if sessionData.get("identifier") != identifier
    ]

    sessions.append(session)

    with open(outputPath, 'w') as file:
        json.dump(sessions, file, indent=2)

    return True


def interactiveMode(outputFile="session.json"):
    """Interactive cookie extraction."""

    print("=" * 70)
    print("Spotify Cookie Extractor from Browser")
    print("=" * 70)

    print("\n[*] How to get cookies from your browser:")
    print("    1. Open https://open.spotify.com (make sure you're logged in)")
    print("    2. Open DevTools (F12 or Right-click -> Inspect)")
    print("    3. Go to Application/Storage -> Cookies -> https://open.spotify.com")
    print("    4. Select all cookies (Ctrl+A), then copy (Ctrl+C)")
    print("       OR select individual important cookies:")
    print("          - sp_dc, sp_key, wp_access_token, wp_refresh_token")
    print("          - sp_t, sp_gaid, _ga, _gid")
    print("    5. Paste below (the script will parse any format)")
    print("    6. type END and press enter.")
    print("\n" + "-" * 70 + "\n")

    email = input("Enter Spotify email or username: ").strip()

    if not email:
        print("[-] Email is required")
        return False

    print("\nPaste your cookies (JSON format, cURL, or cookie string):")
    print("(You can paste multiple lines. When done, type 'END' on a new line)")
    print("Example formats:")
    print("  Tab-separated: sp_dc\\tABC123\\t.spotify.com\\t/")
    print("  Name=value: sp_dc=ABC123; sp_key=DEF456")
    print("  Individual lines:")
    print("    sp_dc=ABC123")
    print("    sp_key=DEF456")
    print("-" * 70)

    lines = []

    while True:
        line = input()

        if line.strip().upper() == 'END':
            break

        lines.append(line)

    cookieInput = "\n".join(lines)

    if not cookieInput.strip():
        print("[-] No cookies provided")
        return False

    print("\n[*] Parsing cookies...")

    try:
        cookies = parseBrowserExport(cookieInput)

    except Exception as error:
        print(f"[-] Error parsing cookies: {error}")
        return False

    if not cookies:
        print("[-] Could not extract any cookies")
        return False

    print(f"[+] Found {len(cookies)} cookies:")

    for key in sorted(cookies.keys())[:10]:
        print(f"    - {key}")

    if len(cookies) > 10:
        print(f"    ... and {len(cookies) - 10} more")

    # Validate cookies
    hasEssential, warnings = validateSpotifyCookies(cookies)

    if warnings:
        print("\n[!] Warnings:")

        for warning in warnings:
            print(f"    - {warning}")

    if not hasEssential:
        print("\n[-] No essential Spotify cookies detected!")
        print("    Make sure you're logged into https://open.spotify.com")
        print("    and copy cookies from the correct domain.")

        retry = input("\nTry again? (y/n): ").strip().lower()

        if retry == 'y':
            return interactiveMode()

        return False

    try:
        saveSession(cookies, email, outputFile)

        print(f"\n[+] Session saved to {Path(outputFile).absolute()}")

        return True

    except Exception as error:
        print(f"[-] Error saving session: {error}")
        return False


if __name__ == "__main__":
    success = interactiveMode()