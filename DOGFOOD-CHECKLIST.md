# Dogfood checklist — à dérouler avant chaque release

> À cocher **manuellement** avant de publier une nouvelle version.
> Prend ~10 minutes. Évite les régressions "works on my machine".

**Version testée** : ____________ · **Testeur** : ____________ · **Date** : ____________

---

## Prérequis — installer depuis un état vierge

Tester depuis MA machine de dev (avec son état accumulé) = **piège**. Il FAUT partir fresh.

```bash
# 1. Tuer toute instance V2 qui tourne
pkill -9 -f artemis-paysages-app

# 2. WIPE complet du dir V2 user (garde ~/meetings/ → patrimoine)
rm -rf ~/.artemis-paysages-v2 ~/.config/artemis-paysages-v2

# 3. Désinstaller l'app V2 courante
rm -rf "/Applications/Artemis Paysages Enregistreur V2.app"

# 4. Télécharger le DMG depuis la release GitHub (PAS le build local !)
# https://github.com/Matthieusabourin2/minutes/releases
# Glisser l'app dans /Applications

# 5. Dé-quarantaine + signature ad-hoc
sudo xattr -cr "/Applications/Artemis Paysages Enregistreur V2.app"
sudo codesign --force --deep --sign - "/Applications/Artemis Paysages Enregistreur V2.app"
open "/Applications/Artemis Paysages Enregistreur V2.app"
```

---

## Checklist — toutes les cases doivent passer

### 1. Onboarding
- [ ] L'écran "Bienvenue sur Artemis Paysages" s'affiche
- [ ] 4 boutons de modèle Whisper visibles (small, medium, **large-v3-turbo ⭐**, large-v3)
- [ ] Click sur **large-v3-turbo** → barre de progression s'affiche
- [ ] Le téléchargement se termine sans erreur (attendre 2-5 min)
- [ ] Le texte "Downloaded…" apparaît

### 2. Premier enregistrement
- [ ] Le bouton "Démarrer l'enregistrement" est cliquable
- [ ] Click → barre rouge apparaît, l'**audio viz rouge s'anime** quand on parle
- [ ] L'input "Prends une note timestampée" est visible (pas caché derrière un bouton)
- [ ] Taper "test note" + Enter → bordure verte flash 1s (note sauvegardée)
- [ ] Le bouton **⏸ Pause** est visible
- [ ] Click Pause → statut pill passe en ambre "en pause", bouton devient "▶ Reprendre"
- [ ] Click Reprendre → retour normal
- [ ] Parler pendant 30 secondes, puis Stop
- [ ] Traitement : les stages français s'affichent (Transcription… → Identification des intervenants… → Analyse ProcessCom…)
- [ ] Un RDV apparaît dans la liste de gauche

### 3. Détail RDV + brouillons
- [ ] Click sur la card du RDV → popup détail s'ouvre
- [ ] Titre complet visible (pas tronqué)
- [ ] Chips meta en français (date fr-FR, "rendez-vous", "X participants", etc.)
- [ ] Section "Résumé" + "Analyse ProcessCom" présentes
- [ ] Click "Créer un brouillon" → dialog templates s'ouvre
- [ ] Choisir "E-mail de relance" → brouillon généré en 5-10s
- [ ] Le brouillon s'ouvre dans le viewer markdown
- [ ] **Bouton ✉️ E-mail** en haut → Mail.app / client mail s'ouvre pré-rempli
- [ ] Click ← Retour (ou bouton back du viewer) → retour au RDV

### 4. Assistant chatbot
- [ ] Click "Échanger avec l'assistant" → panneau droit s'ouvre
- [ ] Taper "résume-moi ce RDV" → réponse en 5-10s
- [ ] La réponse est **rendue en markdown** (pas en texte brut avec des `##`)
- [ ] Fermer + rouvrir le panneau → la conversation est persistée
- [ ] Cliquer sur un autre RDV pendant que l'assistant est ouvert → switch de scope
- [ ] Bouton "Hebdo" dans Aide mémoire → résumé hebdomadaire affiché comme bulle assistant

### 5. Changement de modèle (régression V2.0-beta.1)
- [ ] Ouvrir Réglages (⌘,)
- [ ] Changer le dropdown "Modèle Whisper" vers un modèle NON téléchargé (ex: small si turbo est déjà pris)
- [ ] **Popup "Télécharger ce modèle maintenant ?"** s'affiche
- [ ] Click "Télécharger" → barre de progression
- [ ] Le download se termine
- [ ] Revenir à l'écran principal, démarrer un nouvel enregistrement → **ça marche** (pas d'erreur "ggml-XXX.bin not found")

### 6. Suppression + dialogs
- [ ] Clic "Supprimer" sur un RDV → **dialog de confirmation stylisé** (pas `confirm()` natif)
- [ ] Click "Annuler" → rien ne se passe
- [ ] Click "Supprimer définitivement" → le RDV disparaît de la liste + du disque

### 7. Raccourcis clavier (échantillon)
- [ ] ⌘R → démarre un record
- [ ] ⌘R à nouveau → stop
- [ ] ⌘K → focus la recherche
- [ ] ⌘, → ouvre Réglages
- [ ] Esc → ferme popup / viewer
- [ ] Cmd+Shift+N (pendant enregistrement) → focus l'input de note

### 8. Dark mode
- [ ] Système macOS → Apparence → Sombre
- [ ] L'app bascule en dark mode automatiquement
- [ ] Les bulles du chatbot sont lisibles (pas texte clair sur fond clair)
- [ ] Le champ de saisie de l'assistant est lisible (pas vert fluo sur blanc)
- [ ] La barre d'enregistrement rouge reste visible

### 9. Migration V1 → V2 (si applicable)
- [ ] Avant le wipe, avoir enregistré 1-2 RDV avec V1 et noté le nombre
- [ ] Après install fresh V2 → migration auto ? (voir les logs `~/.artemis-paysages-v2/MIGRATED-FROM-V1.txt`)
- [ ] Les RDV V1 apparaissent dans la liste V2 (via `~/meetings/` partagé)

---

## Si UNE case échoue

1. **Noter le numéro + le symptôme exact** dans le commit message du fix
2. **Ne pas publier la release** tant que la case n'est pas verte
3. Ajouter un test automatisé si possible pour que le bug ne revienne jamais

---

## Checklist CI (automatique, vérifie que c'est vert avant de dérouler le manuel)

- [ ] `cargo fmt --check` passe
- [ ] `cargo clippy` passe (warnings OK en beta)
- [ ] `cargo test -p minutes-core --no-default-features --lib` → 428+ verts
- [ ] Tests de cohérence UI ↔ validator passent (`all_ui_exposed_models_are_validator_accepted`, `artemis_template_default_model_is_validator_accepted`)
- [ ] Build macOS CI vert
- [ ] Build Windows CI vert
