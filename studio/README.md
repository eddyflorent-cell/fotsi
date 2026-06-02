# FGS Studio

**Des outils clés en main pour les entrepreneurs qui n'ont pas encore les moyens d'une grande agence.**

FGS Studio conçoit et livre des SaaS et webapps sur mesure — code propre, zéro maintenance côté client, scalable quand le business grandit.

---

## Principe

1. **On collecte tout en une fois** — brief client complet dès le départ, plus d'allers-retours pour récupérer des infos
2. **FGS gère tout le technique** — email dédié, repo, domaine, hébergement, base de données, paiement
3. **Le client reçoit un outil qui tourne** — sans se soucier de l'infrastructure
4. **Le code est propre** — quand le client peut se payer un dev, il reprend sans friction

---

## Templates disponibles

| Fichier | Usage | Moment |
|---|---|---|
| [`templates/01-brief-client.md`](templates/01-brief-client.md) | À remplir avec le client (15–20 min, aucune tech) | Premier échange |
| [`templates/02-setup-technique-fgs.md`](templates/02-setup-technique-fgs.md) | Checklist interne FGS avant de coder | Après acompte reçu |
| [`templates/03-devis-type.md`](templates/03-devis-type.md) | Trame de devis — 5 postes, modalités 50/50 | Après brief validé |

---

## Workflow type

```
1. Appel / WhatsApp client  →  remplir 01-brief-client.md
2. Devis envoyé             →  adapter 03-devis-type.md + envoyer en PDF
3. Devis signé + acompte    →  remplir 02-setup-technique-fgs.md
4. Développement            →  stack selon brief
5. Recette                  →  tests mobile + HTTPS + .env check
6. Livraison                →  doc utilisateur + solde + facture
```

---

## Stack par défaut FGS Studio

| Type de projet | Stack |
|---|---|
| Site vitrine | HTML / CSS / JS vanilla |
| App de gestion | HTML/JS + PHP + MySQL (IONOS) |
| App avec auth / temps réel | HTML/JS + Supabase |
| App avec paiement | Stack ci-dessus + Stripe |
| PWA mobile | HTML/JS + Service Worker + Manifest |

> Pas de frameworks lourds, pas de bundler, pas de TypeScript sur les projets clients — priorité à la maintenabilité et à la vitesse de livraison.
