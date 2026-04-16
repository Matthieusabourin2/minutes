#!/usr/bin/env python3
"""Génère les icônes Artemis (.icns, .ico, PNGs de tray) depuis logo-paysages.png.

Idempotent — à relancer si le logo source évolue.

Dépendances :
    - Python 3 + Pillow (pip install Pillow)
    - iconutil (inclus macOS, pour .icns)

Source : tauri/src/assets/logo-paysages.png
Destinations : tauri/src-tauri/icons/*
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent.parent
SRC = REPO_ROOT / "tauri" / "src" / "assets" / "logo-paysages.png"
OUT = REPO_ROOT / "tauri" / "src-tauri" / "icons"

# Couleurs Artemis (brand system)
COLOR_RECORDING = (165, 31, 24, 255)   # #A51F18 rouge bordeaux
COLOR_LIVE = (12, 93, 64, 255)         # #0C5D40 vert forêt


def main() -> int:
    if not SRC.exists():
        print(f"[ERREUR] Logo source introuvable : {SRC}", file=sys.stderr)
        return 1

    OUT.mkdir(parents=True, exist_ok=True)
    src_img = Image.open(SRC).convert("RGBA")

    # 1. app-icon.png 512×512 (fallback)
    print("[1/5] Génération app-icon.png (512×512)…")
    src_img.resize((512, 512), Image.LANCZOS).save(OUT / "app-icon.png", format="PNG")

    # 2. icon.ico (Windows multi-tailles)
    print("[2/5] Génération icon.ico (Windows multi-tailles)…")
    ico_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    # Pillow prend la plus grande image et génère les multi-résolutions
    base_256 = src_img.resize((256, 256), Image.LANCZOS)
    base_256.save(OUT / "icon.ico", format="ICO", sizes=ico_sizes)

    # 3. icon.icns (macOS)
    print("[3/5] Génération icon.icns (macOS)…")
    with tempfile.TemporaryDirectory() as tmp:
        iconset = Path(tmp) / "icon.iconset"
        iconset.mkdir()
        for size in (16, 32, 64, 128, 256, 512):
            src_img.resize((size, size), Image.LANCZOS).save(
                iconset / f"icon_{size}x{size}.png", format="PNG"
            )
            retina = size * 2
            src_img.resize((retina, retina), Image.LANCZOS).save(
                iconset / f"icon_{size}x{size}@2x.png", format="PNG"
            )
        result = subprocess.run(
            ["iconutil", "--convert", "icns", str(iconset),
             "--output", str(OUT / "icon.icns")],
            check=False,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print(f"[ATTENTION] iconutil a échoué : {result.stderr}", file=sys.stderr)
            print("  → icon.icns non généré. (Un .icns obsolète peut rester en place.)")
        else:
            print(f"  → {OUT / 'icon.icns'} OK")

    # 4. icon.png (tray 44×44)
    print("[4/5] Génération icon.png (tray 44×44)…")
    tray_base = src_img.resize((44, 44), Image.LANCZOS)
    tray_base.save(OUT / "icon.png", format="PNG")

    # 5. icon-live.png + icon-recording.png (tray + pastille d'état)
    print("[5/5] Génération icon-live.png et icon-recording.png…")

    def with_dot(color: tuple[int, int, int, int]) -> Image.Image:
        img = tray_base.copy()
        draw = ImageDraw.Draw(img)
        # Pastille 14×14 en bas à droite, bordée de blanc pour contraste
        dot_radius = 7
        dot_center = (44 - dot_radius - 1, 44 - dot_radius - 1)
        # Halo blanc (bordure)
        draw.ellipse(
            [
                dot_center[0] - dot_radius - 1, dot_center[1] - dot_radius - 1,
                dot_center[0] + dot_radius + 1, dot_center[1] + dot_radius + 1,
            ],
            fill=(255, 255, 255, 230),
        )
        draw.ellipse(
            [
                dot_center[0] - dot_radius, dot_center[1] - dot_radius,
                dot_center[0] + dot_radius, dot_center[1] + dot_radius,
            ],
            fill=color,
        )
        return img

    with_dot(COLOR_LIVE).save(OUT / "icon-live.png", format="PNG")
    with_dot(COLOR_RECORDING).save(OUT / "icon-recording.png", format="PNG")

    # Summary
    print("\n[OK] Icônes Artemis générées :")
    for f in sorted(OUT.glob("*")):
        if f.is_file() and f.suffix.lower() in {".png", ".icns", ".ico"}:
            print(f"  {f.relative_to(REPO_ROOT)}  ({f.stat().st_size:,} octets)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
