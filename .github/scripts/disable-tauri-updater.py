#!/usr/bin/env python3
"""
Patch tauri/src-tauri/tauri.conf.json for the Artemis installer build:
set `bundle.createUpdaterArtifacts` to false so the build doesn't emit
`.app.tar.gz` / `.sig` updater artifacts and doesn't require a valid
`TAURI_SIGNING_PRIVATE_KEY` at signing time.

Artemis installers are one-shot: we don't ship a Sparkle-style auto
updater endpoint to the sales reps. If a new version is needed,
Catalia rebuilds and hands Franck a fresh .exe / .dmg by hand.

Cross-platform (stdlib only). Idempotent: running twice is a no-op.
Preserves the rest of the file byte-for-byte where possible via
json.dump with indent matching the upstream file (2 spaces).
"""

from __future__ import annotations

import json
import pathlib
import sys


CONF = pathlib.Path("tauri/src-tauri/tauri.conf.json")


def main() -> int:
    if not CONF.is_file():
        print(f"ERROR: {CONF} not found (run from repo root).", file=sys.stderr)
        return 1

    data = json.loads(CONF.read_text(encoding="utf-8"))
    bundle = data.setdefault("bundle", {})
    before = bundle.get("createUpdaterArtifacts")
    bundle["createUpdaterArtifacts"] = False

    CONF.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(
        f"Patched {CONF}: createUpdaterArtifacts {before!r} → False "
        "(no updater .tar.gz will be produced / signed)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
