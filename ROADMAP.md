# Roadmap — Artemis Paysages Enregistreur

> **Document vivant.** Ouvre une [Issue](https://github.com/Matthieusabourin2/minutes/issues)
> ou une [Discussion](https://github.com/Matthieusabourin2/minutes/discussions)
> pour proposer une feature, prioriser, ou remonter un bug.

**Mise à jour** : 17 avril 2026

---

## Légende

- ✅ **Livré** — disponible dans la version courante
- 🚧 **En cours** — en dev actif, prochain release
- 📋 **Planifié** — prévu, pas commencé
- 💡 **Idée** — à valider / discuter avec les utilisateurs
- ⏸ **Parking** — dépriorisé, revient si demande

---

## V2.0-beta — Actuellement en test (pilote Franck)

Tag : [`v0.2.0-beta.1-artemis-v2`](https://github.com/Matthieusabourin2/minutes/releases/tag/v0.2.0-beta.1-artemis-v2)

### ✅ Bugs résolus
- Audio viz rouge visible pendant enregistrement
- Modèle Whisper téléchargé = modèle utilisé (plus de mismatch)
- Dead code auto-updater supprimé
- Migration auto des données V1 → V2 au premier lancement
- Calendar polling désactivé par défaut
- Note inline toujours visible pendant enregistrement
- Script `.command` macOS pour éviter la procédure Terminal

### ✅ UX polish
- Rendu markdown dans les bulles chatbot
- 8 raccourcis clavier (⌘R, ⌘K, ⌘W, ⌘⇧A, ⌘⌥[, Esc, ⌘⇧N, ⌘,)
- Dialog de confirmation stylisé (plus de `confirm()` natif)
- Bouton "↻ Réessayer" sur les erreurs Claude API
- Progress states français pendant traitement
- Bouton "✉️ E-mail" dans le viewer de brouillon → mailto pré-rempli
- **Pause / reprise** enregistrement (ajouté en V2-beta.2)
- **Popup confirmation + download auto** au changement de modèle dans les settings (V2-beta.2)

---

## V2.0 stable — Dans les 4 semaines après la beta

Objectif : sortir V2.0 stable quand Franck + 2 commerciaux ont utilisé V2-beta pendant 2 semaines sans régression majeure.

### 🚧 En cours
- Feedback Franck beta sur 5-10 RDV réels
- Correction des régressions éventuelles
- Vidéo Loom officielle de 3 min ([script déjà écrit](docs/LOOM-SCRIPT.md))

### 📋 Inclus dans V2.0 stable si temps permet
- Apple Developer Program (99 €/an) + notarisation du DMG → fini les commandes Terminal pour les users Mac
- Windows code signing (~250 €/an) → fini SmartScreen

---

## V2.1 — Fonctionnalités utilisateur (priorisation à faire)

Les items ci-dessous sont prévus mais non encore priorisés entre eux.
**C'est là que ton feedback compte le plus.**

### 📋 Organisation
- **Tags / catégories sur les RDV** — prospect / client / interne · chaud / tiède / froid — pour que la liste reste lisible au-delà de 30 RDV
- **Dashboard KPI** — vue agrégée hebdomadaire : nb de RDV, leads chauds, engagements en retard, prestations top, temps d'enregistrement total
- **Search étendu** — la barre de recherche actuelle ne scanne que les CR. L'étendre aux brouillons et aux conversations chatbot.

### 📋 Productivité commercial
- **Enrôlement vocal** — Franck + chaque commercial enregistre 30s de sa voix. Les transcriptions affichent "Franck : …", "Client : …" au lieu de "SPEAKER_00".
- **Calendar integration** — lecture Google / Apple Calendar → RDV à venir pré-remplit le prospect
- **Digest hebdomadaire e-mail** — chaque dimanche soir, Claude génère un résumé de la semaine + plan lundi, envoyé par mail
- **Auto-suggest relances** — à partir des `action_items` extraits, créer des events Calendar ("Relancer Pierre mardi 10h")
- **Renommage speakers** depuis le viewer markdown — bouton "Attribuer à…" avec liste des participants (workaround tant que l'enrôlement vocal n'est pas fait)
- **Exports PDF / Word** des comptes-rendus

### 📋 Techniques
- **Auto-updater propre** — infra `releases.artemis-paysages.fr` ou CDN, Franck peut pousser une update à son équipe sans redistribuer
- **Tests E2E** Playwright sur 3 flows critiques (onboarding, enregistrement, création brouillon)
- **Telemetry opt-in** (Sentry OSS) — crash reports auto, pas de data RDV envoyée

---

## V3.0 — Vision long terme (6-12 mois)

### 💡 Stratégique
- **App mobile iOS companion** — enregistrement depuis iPhone, sync vers Mac/Windows
- **CRM integration** — sync HubSpot / Pipedrive / feuille Excel
- **Mode coaching live** — pour les RDV visio, Claude suggère des relances au fil du discours
- **Devis template generator** — à partir des "Prestations identifiées" → devis HTML/PDF structuré
- **Offline fallback Ollama** — LLM local pour pas dépendre du réseau ni d'Anthropic

### 💡 Avancé
- Analytics émotionnelles (température émotionnelle pendant le RDV)
- Competitor intelligence (mentions de concurrents dans les transcripts)
- Collaboration équipe (Franck voit les CR de ses commerciaux en temps réel)
- Multi-langue (EN / ES / DE)

---

## ⏸ Parking (reviendra si demande)

- Support Linux desktop (seuls Mac + Windows aujourd'hui)
- Plugin Obsidian direct (aujourd'hui les MD sont stockés dans `~/meetings/`, on peut les ouvrir dans Obsidian manuellement)
- Streaming live vers Slack / Teams pendant le RDV

---

## Comment contribuer à cette roadmap ?

**Tu es commercial Artemis ou utilisateur pilote :**
1. [Ouvre une Discussion](https://github.com/Matthieusabourin2/minutes/discussions) décrivant ton use case et le problème concret
2. Si c'est déjà dans la roadmap, vote / commente pour faire remonter la priorité
3. Si c'est nouveau, Catalia évalue effort/valeur et propose un slot V2.1 ou V3.0

**Tu es développeur :**
1. [Ouvre une Issue](https://github.com/Matthieusabourin2/minutes/issues) avec reproduction claire (OS, version, steps)
2. Les PRs sur `artemis-v2` branche sont bienvenues (fork l'upstream `silverstein/minutes` n'est pas compatible — fork spécifique Artemis)

---

## Politique de MAJ — engagement Catalia

- **Rien n'est jamais supprimé** lors d'une mise à jour
- **Les données utilisateur** (`~/meetings/`, voices.db, graph.db, conversations chatbot) sont **migrées automatiquement** à chaque montée de version majeure
- **Les anciennes versions** restent téléchargeables sur [GitHub Releases](https://github.com/Matthieusabourin2/minutes/releases) pour un rollback si besoin
- **Les versions majeures** (V1 → V2, V2 → V3) utilisent un bundle ID distinct → coexistence possible sur la même machine le temps de valider la nouvelle

---

Contact : `matt@catalia.fr` (Catalia / développement)
