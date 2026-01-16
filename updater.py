import base64
import os
import re
import subprocess
from urllib.request import Request, urlopen

from trustifi import __version__

API_URL = "https://chromium.googlesource.com/chromium/src/+/refs/heads/main/{path}?format=TEXT"
TEXTPROTO_PATH = "net/data/ssl/chrome_root_store/root_store.textproto"
CERTS_PATH = "net/data/ssl/chrome_root_store/root_store.certs"

VERSION_RE = re.compile(r"version_major\s*:\s*(\d+)")
PEM_RE = re.compile(r"-----BEGIN CERTIFICATE-----[\s\S]*?-----END CERTIFICATE-----")


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True, timeout=30)


def get_file(path: str) -> str:
    path = path.lstrip("/")
    req = Request(API_URL.format(path=path))
    with urlopen(req, timeout=30) as r:
        return base64.b64decode(r.read()).decode("utf-8")


def extract_version(text: str) -> str:
    match = VERSION_RE.search(text)
    if not match:
        raise ValueError("Could not find version_major")

    return match.group(1)


def extract_pems(text: str) -> list[str]:
    pems = PEM_RE.findall(text)
    if not pems:
        raise ValueError("No certificates found")

    return pems


def write_certs(pems: list[str], path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(pems))

    print(f"Wrote {len(pems)} certificates to {path}")


def update_version_file(path: str, new_version: str) -> None:
    with open(path, "r+", encoding="utf-8") as f:
        content = f.read()
        content = re.sub(
            r'__version__\s*=\s*["\']\d+["\']',
            f'__version__ = "{new_version}"',
            content,
        )
        f.seek(0)
        f.truncate()
        f.write(content)

    print(f"Updated trustifi version to {new_version}")


def git_commit_and_tag(version: str) -> None:
    run(["git", "config", "user.name", "github-actions[bot]"])
    run(
        [
            "git",
            "config",
            "user.email",
            "41898282+github-actions[bot]@users.noreply.github.com",
        ]
    )

    run(["git", "add", "trustifi/cacert.pem", "trustifi/__init__.py"])
    run(
        [
            "git",
            "commit",
            "--author=AYMENJD <53928879+AYMENJD@users.noreply.github.com>",
            "-m",
            f"Update version to {version}.",
        ]
    )
    run(["git", "push"])
    run(["git", "tag", f"v{version}"])
    run(["git", "push", "--tags"])


def test_cacert() -> None:
    print("Testing cacert.pem...\n")

    from trustifi import where, contents
    import ssl
    import socket

    assert "-----BEGIN CERTIFICATE-----" in contents(), "cacert.pem seems invalid"

    cafile = where()
    ctx = ssl.create_default_context(cafile=cafile)

    tests = [
        # (host, should_pass)
        ("expired.badssl.com", False),
        ("self-signed.badssl.com", False),
        ("wrong.host.badssl.com", False),
        ("untrusted-root.badssl.com", False),
        ("google.com", True),
        ("cloudflare.com", True),
        ("github.com", True),
    ]

    failures = 0

    for host, should_pass in tests:
        try:
            with socket.create_connection((host, 443), timeout=10) as sock:
                with ctx.wrap_socket(sock, server_hostname=host):
                    if not should_pass:
                        print(f"FAIL: {host} (unexpected PASS)")
                        failures += 1
                    else:
                        print(f"PASS: {host}")

        except ssl.SSLError:
            if should_pass:
                print(f"FAIL: {host} (unexpected FAIL)")
                failures += 1
            else:
                print(f"FAIL: {host} (expected)")

        except OSError as exc:
            print(f"SKIP: {host} (network error: {exc})")

    if failures:
        print(f"\nCA test finished with {failures} failure(s)\n")
        return

    print("All CA tests passed.\n")


def main() -> None:
    textproto = get_file(TEXTPROTO_PATH)
    remote_version = extract_version(textproto)

    if remote_version == __version__:
        print("Already up to date.")
        return

    certs_content = get_file(CERTS_PATH)
    pems = extract_pems(certs_content)

    write_certs(pems, "trustifi/cacert.pem")

    test_cacert()

    update_version_file("trustifi/__init__.py", remote_version)
    git_commit_and_tag(remote_version)

    if "GITHUB_ENV" in os.environ:
        with open(os.environ["GITHUB_ENV"], "a", encoding="utf-8") as env_file:
            print("TRUSTIFI_UPDATED=1", file=env_file)


if __name__ == "__main__":
    main()
