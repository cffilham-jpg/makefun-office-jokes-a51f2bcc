"""Write and validate one UTF-8 office joke without a trailing newline.
The CC detail gives blame one specific twist, ending on forwarding address.
"""

import hashlib
import os
import tempfile
from pathlib import Path

LINE = "I CC'd my boss so the blame has a forwarding address."
CHAR_LIMIT = 199


def _resolve_output_dir() -> Path:
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        path = Path(env_dir)
        path.mkdir(parents=True, exist_ok=True)
        return path
    try:
        out = Path("out")
        out.mkdir(parents=True, exist_ok=True)
        return out
    except OSError:
        return Path(tempfile.mkdtemp(prefix="makefun-office-jokes-a51f2bcc-"))


def validate(path: Path) -> None:
    data = path.read_bytes()
    text = data.decode("utf-8")
    if text != LINE:
        raise ValueError("entry.txt content differs from LINE")
    if not 1 <= len(text) <= CHAR_LIMIT:
        raise ValueError("entry.txt length must be between 1 and 199 characters")
    if "\n" in text or "\r" in text:
        raise ValueError("entry.txt must contain a single line without line breaks")
    if text.endswith("\n"):
        raise ValueError("entry.txt must not end with a newline")
    if text != text.strip():
        raise ValueError("entry.txt must not have leading or trailing whitespace")


def main() -> None:
    out_dir = _resolve_output_dir()
    entry = out_dir / "entry.txt"
    entry.write_bytes(LINE.encode("utf-8"))
    validate(entry)
    print(hashlib.sha256(LINE.encode("utf-8")).hexdigest())


if __name__ == "__main__":
    main()
