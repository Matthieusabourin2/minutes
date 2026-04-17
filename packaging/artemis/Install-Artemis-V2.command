#!/bin/bash
# Installation Artemis Paysages Enregistreur V2 — script de dé-quarantaine
# + signature ad-hoc, pour contourner le fait que l'app n'est pas
# signée par un développeur Apple (Catalia n'a pas de certificat
# Apple Developer Program).
#
# Double-clic dans le Finder → tu entres ton mot de passe admin une
# fois, et c'est fini.

set -e

APP_PATH="/Applications/Artemis Paysages Enregistreur V2.app"

# ANSI colors
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo
echo -e "${BLUE}══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  Installation Artemis Paysages Enregistreur V2${NC}"
echo -e "${BLUE}══════════════════════════════════════════════════════════════${NC}"
echo

if [ ! -d "$APP_PATH" ]; then
    echo -e "${RED}✗ L'application n'est pas dans /Applications${NC}"
    echo
    echo "Avant de lancer ce script :"
    echo "  1. Ouvre le fichier .dmg (déjà fait si tu as cliqué dessus)"
    echo "  2. Glisse-dépose 'Artemis Paysages Enregistreur V2.app' dans le"
    echo "     dossier 'Applications' de ta machine"
    echo "  3. Relance ce script"
    echo
    read -p "Appuie sur Entrée pour fermer cette fenêtre..."
    exit 1
fi

echo -e "${YELLOW}L'application va être dé-quarantinée et signée localement.${NC}"
echo "Tu vas devoir entrer ton mot de passe administrateur."
echo

# 1. Retirer l'attribut quarantaine
echo -n "Étape 1/3 : retrait de la quarantaine macOS... "
if sudo xattr -cr "$APP_PATH" 2>/dev/null; then
    echo -e "${GREEN}OK${NC}"
else
    echo -e "${RED}échec${NC}"
    exit 1
fi

# 2. Re-signer ad-hoc
echo -n "Étape 2/3 : signature ad-hoc... "
if sudo codesign --force --deep --sign - "$APP_PATH" 2>/dev/null; then
    echo -e "${GREEN}OK${NC}"
else
    echo -e "${RED}échec${NC}"
    exit 1
fi

# 3. Lancer l'app
echo -n "Étape 3/3 : lancement de l'application... "
if open "$APP_PATH"; then
    echo -e "${GREEN}OK${NC}"
else
    echo -e "${RED}échec — tu peux la lancer manuellement depuis /Applications${NC}"
fi

echo
echo -e "${GREEN}✓ Installation terminée !${NC}"
echo
echo "Au premier lancement :"
echo "  • Tu choisiras un modèle de transcription (Large v3 Turbo recommandé)"
echo "  • Le modèle sera téléchargé une seule fois (~1,6 Go, 2-5 min)"
echo "  • Tu pourras commencer à enregistrer tes rendez-vous"
echo
echo "Tes comptes-rendus seront stockés dans ~/meetings/"
echo
read -p "Appuie sur Entrée pour fermer cette fenêtre..."
