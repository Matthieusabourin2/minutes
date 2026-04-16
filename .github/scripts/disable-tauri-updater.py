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

    # 1. Disable updater artifact creation at build time. Without this,
    #    the macOS Tauri build tries to sign a .app.tar.gz at the end
    #    of bundling and fails when no TAURI_SIGNING_PRIVATE_KEY is set.
    bundle = data.setdefault("bundle", {})
    bundle_before = bundle.get("createUpdaterArtifacts")
    bundle["createUpdaterArtifacts"] = False

    # 2. REMOVE the runtime updater plugin config. Otherwise the shipped
    #    Artemis app periodically polls upstream silverstein/minutes
    #    `latest.json`, prompts the user to "upgrade", and on accept
    #    silently replaces our binary with the upstream signed bundle.
    #    The upstream bundle has no `artemis-default-config` feature
    #    flag, so the embedded config + French UI + ProcessCom prompt
    #    are all wiped. See the field report from the first Mac rollout.
    plugins = data.setdefault("plugins", {})
    had_updater = "updater" in plugins
    plugins.pop("updater", None)

    CONF.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    # ASCII-only output: Python on windows-latest opens stdout as cp1252
    # by default and chokes on Unicode arrows / em-dashes in print().
    print(
        f"Patched {CONF}:\n"
        f"  - createUpdaterArtifacts {bundle_before!r} -> False\n"
        f"  - removed updater plugin config (was present: {had_updater})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
