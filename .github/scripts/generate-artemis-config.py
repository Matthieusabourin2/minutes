#!/usr/bin/env python3
"""
Generate crates/core/src/artemis-default-config.toml from the committed
template at packaging/artemis/config.toml.template, substituting the
__CLE_API_CLAUDE__ placeholder with the ANTHROPIC_API_KEY secret.

Called from .github/workflows/build-artemis.yml on both windows-latest
and macos-latest runners. Cross-platform (stdlib only, no deps).

The output file is gitignored — never commit it. It is picked up by the
`artemis-default-config` Cargo feature via include_str! in
crates/core/src/config.rs.
"""

from __future__ import annotations

import os
import pathlib
import sys


PLACEHOLDER = "__CLE_API_CLAUDE__"
TEMPLATE_PATH = pathlib.Path("packaging/artemis/config.toml.template")
OUTPUT_PATH = pathlib.Path("crates/core/src/artemis-default-config.toml")


def main() -> int:
    api_key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if not api_key:
        print(
            "ERROR: ANTHROPIC_API_KEY is empty or unset.\n"
            "Set it at: repo Settings → Secrets and variables → Actions → "
            "New repository secret (name: ANTHROPIC_API_KEY).",
            file=sys.stderr,
        )
        return 1

    if not TEMPLATE_PATH.is_file():
        print(f"ERROR: template not found at {TEMPLATE_PATH}", file=sys.stderr)
        return 1

    template = TEMPLATE_PATH.read_text(encoding="utf-8")

    if PLACEHOLDER not in template:
        print(
            f"ERROR: placeholder {PLACEHOLDER!r} missing from {TEMPLATE_PATH}. "
            "The template has drifted from the generator.",
            file=sys.stderr,
        )
        return 1

    rendered = template.replace(PLACEHOLDER, api_key)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(rendered, encoding="utf-8")

    # Deliberately do NOT echo size/bytes of the rendered file — GitHub
    # auto-masks registered secrets but we avoid any signal that could
    # help infer the key length.
    print(f"Wrote {OUTPUT_PATH} (placeholder substituted).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
