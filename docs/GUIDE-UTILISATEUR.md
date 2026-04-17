# Artemis Paysages Enregistreur V2 — Guide utilisateur

**Version** : 0.2.0-beta · **Pour qui** : commerciaux Artemis Paysages

---

## En 60 secondes

1. **Avant le RDV** : lance l'app, clique ▶ "Démarrer l'enregistrement"
2. **Pendant le RDV** : parle normalement. Si besoin, tape une note éclair dans la
   barre rouge ("le client hésite sur le prix à 15k") — elle sera timestampée
   automatiquement dans le compte-rendu
3. **Après le RDV** : clique ■ "Arrêter". L'app transcrit, identifie les
   intervenants et génère un compte-rendu structuré avec analyse ProcessCom en
   ~60 secondes
4. **Exploitation** : dans la popup détail du RDV, bouton "Créer un brouillon"
   → choisis "E-mail de relance" → bouton ✉️ E-mail → Mail.app s'ouvre
   pré-rempli → tu relis, tu envoies

---

## Premier lancement (install)

### Mac — méthode Terminal (recommandée, 30 secondes)

L'app n'étant pas signée Apple Developer Program, macOS la met en
quarantaine au téléchargement. Il faut la dé-quarantaine et la signer
localement une seule fois. **Copie-colle ces 3 lignes dans ton Terminal
(Applications > Utilitaires > Terminal) :**

```bash
sudo xattr -cr "/Applications/Artemis Paysages Enregistreur V2.app"
sudo codesign --force --deep --sign - "/Applications/Artemis Paysages Enregistreur V2.app"
open "/Applications/Artemis Paysages Enregistreur V2.app"
```

**Pré-requis** : avoir d'abord glissé l'app depuis le DMG dans le dossier
`/Applications`. Résumé complet :

1. Double-clique `Minutes-Artemis-V2.dmg`
2. Glisse "Artemis Paysages Enregistreur V2" dans **Applications**
3. Ouvre Terminal → copie-colle les 3 lignes ci-dessus → appuie Entrée
4. Entre ton mot de passe admin (tu ne verras pas les caractères, c'est normal)
5. L'app se lance automatiquement. Tu n'auras plus jamais à refaire ça.

### Mac — alternative avec le script `.command` fourni

Le DMG contient aussi `Install-Artemis-V2.command` qui fait la même chose
en double-clic. Mais macOS Gatekeeper bloque aussi ce script. Pour
l'autoriser, dans Terminal :

```bash
xattr -c ~/Downloads/Install-Artemis-V2.command
```

Puis double-clic sur le `.command` dans Finder → il marche.

### Windows
1. Double-clique `Minutes-Artemis-V2-Setup.exe`
2. NSIS gère l'install, suis les étapes
3. Au premier lancement, Windows SmartScreen peut demander "Exécuter quand
   même" → clique "Informations complémentaires" puis "Exécuter quand même"
   (app non signée Microsoft, pas de risque)

### Premier démarrage (Mac + Windows)
L'écran d'accueil te propose 4 modèles Whisper (transcription locale) :
- **Small** (466 Mo) — rapide, précision moyenne, fallback PC/Mac ancien
- **Medium** (1,5 Go) — bon compromis
- **⭐ Large v3 Turbo** (1,6 Go) — **recommandé** sur Mac M1/M2/M3
- **Large v3** (3,1 Go) — qualité maximale, plus lent

Clique sur le modèle choisi. Téléchargement ~2-5 min selon ta connexion.

---

## Interface principale

```
┌──────────────────────┬──────────────────────┐
│  Liste de tes RDV    │  Assistant (chat)    │
│                      │                      │
│  🟢 Aide mémoire     │  Pose des questions  │
│  ────────            │  sur un RDV ou la    │
│  📄 RDV du jour      │  stratégie globale   │
│  📄 RDV d'hier       │                      │
│  ...                 │                      │
│                      │                      │
├──────────────────────┤                      │
│  🎤 Démarrer         │                      │
│  Note rapide │ Assist.│                     │
└──────────────────────┴──────────────────────┘
```

### Aide mémoire (en haut de la liste à gauche)
Récap des 7 derniers jours : RDV récents, mémos, engagements en attente, contacts
à relancer. **Cliquer "Hebdo"** → l'assistant génère un résumé hebdomadaire
consultable et discutable.

### Panneau assistant (à droite)
Deux modes :
- **Scopé** — quand tu cliques "Échanger avec l'assistant" depuis la popup d'un
  RDV, ou quand tu cliques sur une card de RDV pendant que l'assistant est
  ouvert. L'assistant ne parle que de CE RDV précis.
- **Général** — quand tu cliques sur le bouton "Assistant" du footer. Libre,
  pour poser des questions stratégie commerciale, préparer une relance type,
  demander des conseils ProcessCom.

L'historique est stocké par RDV — tu peux switcher entre RDV et retrouver
chaque conversation intacte.

---

## Raccourcis clavier

| Raccourci | Action |
|---|---|
| ⌘R | Démarrer / arrêter l'enregistrement |
| ⌘⇧N | Focus sur l'input de note (pendant enregistrement) |
| ⌘K | Recherche dans tes RDV |
| ⌘⇧A | Ouvrir / fermer l'assistant |
| ⌘W ou Esc | Fermer la popup courante |
| ⌘⌥[ | Retour dans la popup détail (si tu as navigué via "Source" / "Ouvrir") |
| ⌘, | Réglages |

---

## Brouillons (templates automatiques)

Depuis un RDV enregistré → popup détail → **"Créer un brouillon"** :

| Template | Quand l'utiliser |
|---|---|
| **E-mail de relance** | Le RDV est fini, tu veux envoyer un mail de suivi au prospect le lendemain. Le bouton ✉️ E-mail ouvre ton client mail avec tout pré-rempli. |
| **Brief de préparation** | Avant le prochain RDV avec le même prospect : rappel de ce qui s'est dit, objections à anticiper, température du lead. |
| **Mémo de débrief** | Pour la direction ou ton équipe : synthèse concise, leviers, blocages. |
| **Mémo de décision** | Le RDV a débouché sur une décision claire (signature imminente, prix acté, etc.). Archive ça. |

Tous les brouillons sont en **français plain-text** (pas de markdown qui fuit
dans Gmail) et copier-collables direct.

---

## Analyse ProcessCom

Dans chaque compte-rendu, une section "Analyse ProcessCom" identifie le profil
du prospect (Empathique, Travaillomane, Persévérant, Rêveur, Promoteur,
Rebelle) avec :
- **Indices détectés** : 2-3 verbatims qui orientent
- **Canal de communication recommandé** pour la prochaine fois
- **Points de vigilance** : drivers de stress potentiels

**Important** : c'est une **hypothèse de travail**, pas une certitude. Claude
écrit "Données insuffisantes" si la transcription est trop courte pour typer.

L'objectif n'est pas de manipuler — c'est d'adapter ta posture commerciale.

---

## Confidentialité

- **Audio stocké en local** sur ta machine, jamais envoyé ailleurs
- **Transcription faite en local** par Whisper (modèle téléchargé une fois)
- **Seul le texte du résumé est envoyé à Anthropic (Claude)** pour générer
  l'analyse. Aucun audio.
- **Aucune donnée de RDV stockée côté Anthropic au-delà de l'appel API** (voir
  https://www.anthropic.com/privacy pour le détail RGPD)
- **Tes fichiers** sont dans `~/meetings/` (Mac) ou `C:\Users\<toi>\meetings\`
  (Windows). Tu peux les ouvrir dans n'importe quel éditeur markdown.

---

## Problèmes fréquents

### Le bouton DIRECT ne lance rien / j'entends un bip
Modèle Whisper pas téléchargé ou mal configuré. Ouvre Réglages → Modèle
Whisper → télécharger.

### L'enregistrement démarre mais rien ne sort à la fin
Probablement un problème de permissions Microphone. Réglages macOS → Sécurité
et confidentialité → Microphone → autoriser l'app.

### Le compte-rendu est bizarre (anglais, titres manquants)
Si Claude API a échoué (panne réseau), l'app sauve quand même la transcription
brute. Tu peux relancer le traitement plus tard depuis la popup détail.

### L'app ne se lance pas (Mac) — dialogue "Apple could not verify…"
macOS bloque l'app parce qu'elle n'est pas signée par un développeur Apple
(l'abonnement Apple Developer Program à 99 €/an n'est pas encore pris
pour la V2 beta). Pour débloquer, ouvre Terminal et colle :

```bash
sudo xattr -cr "/Applications/Artemis Paysages Enregistreur V2.app"
sudo codesign --force --deep --sign - "/Applications/Artemis Paysages Enregistreur V2.app"
open "/Applications/Artemis Paysages Enregistreur V2.app"
```

Entre ton mot de passe admin. Tu n'auras plus jamais à refaire cette
opération sur cette machine.

### Le script `.command` est bloqué par "Apple could not verify…"
Même raison. Dans Terminal :

```bash
xattr -c ~/Downloads/Install-Artemis-V2.command
```

Puis double-clic sur le `.command`.

### Un brouillon ne s'affiche pas après création
Va dans la popup détail du RDV → section "Documents associés" → clique "Ouvrir"
sur le brouillon attendu.

---

## Contact support

**Catalia** (prestataire technique) — `matt@catalia.fr`
**Franck Martin** (Artemis Paysages) — `f.martin@artemis-paysages.fr`

En cas de bug critique (app qui crash, CR non sauvegardé), joins le fichier
`~/.artemis-paysages-v2/logs/minutes.log` à ton e-mail.
