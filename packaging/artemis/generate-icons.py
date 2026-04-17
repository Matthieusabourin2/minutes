#!/usr/bin/env python3
"""Génère les icônes Artemis V2 (.icns, .ico, PNGs de tray) depuis logo-paysages.png.

V2 : ajoute un badge "V2" en coin inférieur droit pour distinguer visuellement
     la V2 de la V1 dans le Finder / Dock / Start Menu quand les deux apps
     coexistent sur la même machine.

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

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent.parent
SRC = REPO_ROOT / "tauri" / "src" / "assets" / "logo-paysages.png"
OUT = REPO_ROOT / "tauri" / "src-tauri" / "icons"

# Couleurs Artemis (brand system)
COLOR_RECORDING = (165, 31, 24, 255)   # #A51F18 rouge bordeaux
COLOR_LIVE = (12, 93, 64, 255)         # #0C5D40 vert forêt
COLOR_V2_BG = (123, 146, 55, 255)      # #7B9237 olive Artemis
COLOR_V2_FG = (255, 255, 255, 255)     # blanc


def resolve_font(size_px: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    """Trouve une police bold disponible sur la machine de build."""
    candidates = [
        # macOS
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/HelveticaNeue.ttc",
        # Linux (GitHub Actions ubuntu-latest)
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        # Windows
        "C:\\Windows\\Fonts\\arialbd.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size_px)
            except Exception:
                continue
    return ImageFont.load_default()


def add_v2_badge(img: Image.Image) -> Image.Image:
    """Ajoute un badge "V2" circulaire en coin inférieur droit."""
    side = img.size[0]
    # Badge occupe ~38% du côté de l'icône, ancré coin bas-droit.
    badge_diameter = int(side * 0.40)
    badge_margin = max(2, int(side * 0.03))

    out = img.copy().convert("RGBA")
    draw = ImageDraw.Draw(out)

    x0 = side - badge_diameter - badge_margin
    y0 = side - badge_diameter - badge_margin
    x1 = x0 + badge_diameter
    y1 = y0 + badge_diameter

    # Halo blanc pour contraste sur fonds sombres
    halo = max(1, int(side * 0.015))
    draw.ellipse(
        [x0 - halo, y0 - halo, x1 + halo, y1 + halo],
        fill=(255, 255, 255, 235),
    )
    # Fond olive Artemis
    draw.ellipse([x0, y0, x1, y1], fill=COLOR_V2_BG)

    # Texte "V2" centré
    font_size = max(10, int(badge_diameter * 0.55))
    font = resolve_font(font_size)
    text = "V2"
    try:
        # Pillow ≥ 8 : textbbox
        bbox = draw.textbbox((0, 0), text, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        text_x = x0 + (badge_diameter - text_w) / 2 - bbox[0]
        text_y = y0 + (badge_diameter - text_h) / 2 - bbox[1]
    except AttributeError:
        text_w, text_h = draw.textsize(text, font=font)
        text_x = x0 + (badge_diameter - text_w) / 2
        text_y = y0 + (badge_diameter - text_h) / 2

    draw.text((text_x, text_y), text, fill=COLOR_V2_FG, font=font)
    return out


def main() -> int:
    if not SRC.exists():
        print(f"[ERREUR] Logo source introuvable : {SRC}", file=sys.stderr)
        return 1

    OUT.mkdir(parents=True, exist_ok=True)
    src_img = Image.open(SRC).convert("RGBA")

    # 1. app-icon.png 512×512 (fallback) — avec badge V2
    print("[1/5] Génération app-icon.png (512×512) + badge V2…")
    app_icon = add_v2_badge(src_img.resize((512, 512), Image.LANCZOS))
    app_icon.save(OUT / "app-icon.png", format="PNG")

    # 2. icon.ico (Windows multi-tailles)
    print("[2/5] Génération icon.ico (Windows multi-tailles) + badge V2…")
    ico_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    base_256 = add_v2_badge(src_img.resize((256, 256), Image.LANCZOS))
    base_256.save(OUT / "icon.ico", format="ICO", sizes=ico_sizes)

    # 3. icon.icns (macOS) — badge appliqué à chaque taille
    print("[3/5] Génération icon.icns (macOS) + badge V2…")
    with tempfile.TemporaryDirectory() as tmp:
        iconset = Path(tmp) / "icon.iconset"
        iconset.mkdir()
        for size in (16, 32, 64, 128, 256, 512):
            add_v2_badge(src_img.resize((size, size), Image.LANCZOS)).save(
                iconset / f"icon_{size}x{size}.png", format="PNG"
            )
            retina = size * 2
            add_v2_badge(src_img.resize((retina, retina), Image.LANCZOS)).save(
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

    # 4. icon.png (tray 44×44) — PAS de badge V2 (trop petit pour être lisible)
    print("[4/5] Génération icon.png (tray 44×44, sans badge)…")
    tray_base = src_img.resize((44, 44), Image.LANCZOS)
    tray_base.save(OUT / "icon.png", format="PNG")

    # 5. icon-live.png + icon-recording.png (tray + pastille d'état)
    print("[5/5] Génération icon-live.png et icon-recording.png…")

    def with_dot(color: tuple[int, int, int, int]) -> Image.Image:
        img = tray_base.copy()
        draw = ImageDraw.Draw(img)
        dot_radius = 7
        dot_center = (44 - dot_radius - 1, 44 - dot_radius - 1)
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

    print("\n[OK] Icônes Artemis V2 générées :")
    for f in sorted(OUT.glob("*")):
        if f.is_file() and f.suffix.lower() in {".png", ".icns", ".ico"}:
            print(f"  {f.relative_to(REPO_ROOT)}  ({f.stat().st_size:,} octets)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
