# Setup Technique — FGS Studio
> Checklist interne FGS. À compléter AVANT d'écrire la première ligne de code.  
> Le client n'a pas besoin de faire quoi que ce soit à cette étape.

---

## Infos projet

| | |
|---|---|
| Nom court du projet | `nomprojet` _(minuscules, sans espaces)_ |
| Client | |
| Date de démarrage | |
| Chargé(e) de projet | |

---

## Étape 1 — Email projet dédié

> Un email unique par projet. C'est la clé de voûte : tous les comptes en dépendent.

- [ ] Créer `nomprojet.fgs@gmail.com`
- [ ] Mot de passe noté dans **Bitwarden FGS** (vault "Projets clients")
- [ ] Compte de récupération : `contact@fotsiglobalservices.com`
- [ ] Numéro de récupération : `+33 6 29 85 02 14`
- [ ] 2FA activé (code noté dans Bitwarden)

**Email créé :** `_________________________@gmail.com`

---

## Étape 2 — Dépôt GitHub

- [ ] Créer repo `fgs-nomprojet` sur GitHub (compte `eddyflorent-cell`)
- [ ] Visibilité : **Privé** par défaut
- [ ] Branching initial : `main` (prod) + `dev`
- [ ] Ajouter `.gitignore` adapté à la stack
- [ ] Ajouter `README.md` minimal (nom projet + stack)
- [ ] Créer fichier `.env.example` avec les clés à renseigner (sans valeurs)

**URL repo :** `https://github.com/eddyflorent-cell/fgs-_______`

---

## Étape 3 — Nom de domaine

- [ ] Acheter le domaine avec **l'email projet** (IONOS / OVH / Namecheap)
- [ ] Domaine acheté : `_________________________`
- [ ] DNS configuré vers hébergement
- [ ] Renouvellement auto activé

> Préférer IONOS si stack PHP (pipeline CI/CD déjà en place chez FGS).  
> Préférer Namecheap si stack JS/Vercel (moins cher, DNS simple).

---

## Étape 4 — Hébergement

**Selon la stack :**

| Stack | Hébergement recommandé |
|---|---|
| HTML/JS + PHP + MySQL | IONOS (même compte FGS) |
| HTML/JS + Supabase | Vercel (compte créé avec email projet) |
| React / Next.js | Vercel |
| PWA standalone | Vercel ou GitHub Pages |

- [ ] Hébergement configuré : _______________
- [ ] Déploiement automatique (CI/CD) en place
- [ ] HTTPS actif

---

## Étape 5 — Base de données (si applicable)

**Supabase :**
- [ ] Créer projet Supabase avec **l'email projet**
- [ ] Nom du projet : `fgs-nomprojet`
- [ ] URL + clé anon notées dans `.env` local + Bitwarden
- [ ] RLS (Row Level Security) configuré avant le premier déploiement

**MySQL / IONOS :**
- [ ] Base créée dans le panel IONOS
- [ ] User dédié créé (pas de root)
- [ ] Credentials dans `.env` local + Bitwarden

---

## Étape 6 — Paiement (si applicable)

- [ ] Créer compte Stripe avec **l'email projet**
- [ ] Mode test activé en premier
- [ ] Clés `STRIPE_PUBLIC_KEY` et `STRIPE_SECRET_KEY` dans `.env` + Bitwarden
- [ ] Webhook configuré
- [ ] Mode live activé uniquement à la recette finale

---

## Étape 7 — Variables d'environnement

- [ ] Fichier `.env` créé en local
- [ ] `.env` ajouté au `.gitignore` (ne JAMAIS commiter)
- [ ] `.env.example` committé avec les noms de clés (sans valeurs)
- [ ] Toutes les clés sensibles dans Bitwarden vault "Projets clients"

**Template `.env.example` minimal :**
```env
# Base de données
DB_HOST=
DB_NAME=
DB_USER=
DB_PASS=

# Supabase (si applicable)
SUPABASE_URL=
SUPABASE_ANON_KEY=

# Stripe (si applicable)
STRIPE_PUBLIC_KEY=
STRIPE_SECRET_KEY=
STRIPE_WEBHOOK_SECRET=

# Auth Google (si applicable)
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=

# App
APP_URL=
APP_ENV=development
```

---

## Étape 8 — Espace de partage client

- [ ] Dossier Google Drive créé : `FGS — NomProjet`
- [ ] Partagé avec le client (lecture seule sur les livrables)
- [ ] Structure :
  - `📁 Brief` — brief signé
  - `📁 Maquettes` — wireframes / designs
  - `📁 Livrables` — versions livrées
  - `📁 Factures` — devis + factures

---

## Récapitulatif credentials _(à remplir et stocker dans Bitwarden)_

| Service | Login | Mot de passe | Notes |
|---|---|---|---|
| Gmail projet | | | Récupération : contact@fotsiglobalservices.com |
| GitHub | | | Repo : fgs-nomprojet |
| Hébergement | | | |
| Domaine | | | Exp. : |
| Supabase | | | |
| Stripe | | | Mode test → live à la recette |
| Google Drive | | | Partagé client : oui/non |

---

## Checklist finale avant livraison

- [ ] `.env` jamais dans le repo (vérifier git log)
- [ ] HTTPS actif sur le domaine
- [ ] Tests fonctionnels réalisés sur mobile
- [ ] Documentation utilisateur basique fournie au client
- [ ] Credentials remis au client (si demandé) dans un document sécurisé
- [ ] Facturation émise et archivée dans Google Drive
