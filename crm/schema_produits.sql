-- ════════════════════════════════════════════════════════════════════════════
-- FGS — Extension table produits_crm + import depuis produits.json
-- À exécuter dans Supabase SQL Editor
-- ════════════════════════════════════════════════════════════════════════════

-- ── 0. Créer la table si elle n'existe pas encore ────────────────────────────
CREATE TABLE IF NOT EXISTS produits_crm (
  id           UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  created_at   TIMESTAMPTZ DEFAULT NOW(),
  nom          TEXT NOT NULL,
  description  TEXT,
  prix_public  NUMERIC(12,0) DEFAULT 0,
  prix_revendeur NUMERIC(12,0) DEFAULT 0,
  stock        INTEGER DEFAULT 0,
  categorie    TEXT DEFAULT 'Autre',
  image_url    TEXT,
  actif        BOOLEAN DEFAULT TRUE
);

ALTER TABLE produits_crm ENABLE ROW LEVEL SECURITY;
DO $$ BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE tablename='produits_crm' AND policyname='auth_produits') THEN
    CREATE POLICY "auth_produits" ON produits_crm FOR ALL USING (auth.role() = 'authenticated');
  END IF;
END $$;
-- Lecture publique pour le site vitrine (sans auth)
DO $$ BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE tablename='produits_crm' AND policyname='public_read_produits') THEN
    CREATE POLICY "public_read_produits" ON produits_crm FOR SELECT USING (actif = true);
  END IF;
END $$;

-- ── 1. Colonnes supplémentaires ───────────────────────────────────────────────
ALTER TABLE produits_crm ADD COLUMN IF NOT EXISTS slug             TEXT UNIQUE;
ALTER TABLE produits_crm ADD COLUMN IF NOT EXISTS specs            TEXT[]  DEFAULT '{}';
ALTER TABLE produits_crm ADD COLUMN IF NOT EXISTS photos           TEXT[]  DEFAULT '{}';
ALTER TABLE produits_crm ADD COLUMN IF NOT EXISTS emoji            TEXT    DEFAULT '📦';
ALTER TABLE produits_crm ADD COLUMN IF NOT EXISTS badge            TEXT;
ALTER TABLE produits_crm ADD COLUMN IF NOT EXISTS badge_class      TEXT    DEFAULT 'pb-teal';
ALTER TABLE produits_crm ADD COLUMN IF NOT EXISTS min_qty_revendeur INTEGER DEFAULT 1;
ALTER TABLE produits_crm ADD COLUMN IF NOT EXISTS ordre            INTEGER DEFAULT 0;
ALTER TABLE produits_crm ADD COLUMN IF NOT EXISTS notes_internes   TEXT;

-- ── 2. Import des produits depuis produits.json ───────────────────────────────
INSERT INTO produits_crm (slug, categorie, badge, badge_class, nom, description, specs, prix_public, prix_revendeur, min_qty_revendeur, stock, photos, actif, emoji, ordre)
VALUES
(
  'shawarma-2-foyers', 'Restauration', '✓ Stock Douala', 'pb-teal',
  'Machine à Shawarma Gaz',
  'Brûleur gaz à plateau rotatif électrique — 2 foyers. Inox alimentaire, chauffe homogène, idéale pour snacks et fast-foods.',
  ARRAY['2 foyers gaz','Plateau rotatif électrique','Inox 304','Livraison Douala'],
  140000, 110000, 3, 99,
  ARRAY['images/produits/shawarma-1.jpg','images/produits/shawarma-2.jpg'],
  true, '🍖', 1
),
(
  'powerbank-20000', 'High-Tech FGS', '⚡ Charge rapide', 'pb-gold',
  'Power Bank 20 000 mAh — 66W',
  'Rechargez un Samsung S26 ou iPhone 17 jusqu''à 4 fois, un Tecno/Infinix 3 fois, vos écouteurs 30 fois — sans chercher une prise. La charge rapide 66W recharge votre téléphone en moins d''1h. Double sortie USB + Type-C : deux appareils simultanément. Affichage numérique précis, protection contre les courts-circuits, surcharge et basse tension.',
  ARRAY['20 000 mAh','66W charge rapide','USB-A + Type-C','Affichage numérique','Li-polymère'],
  12000, 9500, 3, 99,
  ARRAY['images/produits/powerbank-1.jpg','images/produits/powerbank-2.jpg','images/produits/powerbank-3.jpg'],
  true, '🔋', 2
),
(
  'ecouteurs-anc-tws', 'High-Tech FGS', '🎧 ANC Premium', 'pb-gold',
  'AirPods ANC Sans Fil',
  'Fini le bruit autour de vous — la suppression active ANC coupe les bruits de fond (rue, transport, bureau). Son riche et équilibré, autonomie longue durée supérieure. Connexion TWS instantanée. Sport ou bureau, ils restent en place. Recharge sans fil incluse.',
  ARRAY['ANC actif','Son premium','Autonomie longue durée','TWS sans fil','Recharge sans fil'],
  17500, 13000, 3, 99,
  ARRAY['images/produits/ecouteurs-3.jpg','images/produits/ecouteurs-1.jpg','images/produits/ecouteurs-2.jpg'],
  true, '🎧', 3
),
(
  'ecouteurs-jm19-anc', 'High-Tech FGS', '🎧 ANC', 'pb-gold',
  'AirPods A11 Pro ANC',
  'Suppression active du bruit ANC pour écouter sans distraction. Son HiFi stéréo, affichage LED de la batterie sur le boîtier. Connexion TWS instantanée, micro intégré pour les appels. Design sport noir et orange — robuste et accrocheur.',
  ARRAY['ANC actif','HiFi stéréo','Affichage LED','TWS sans fil','Micro intégré'],
  11000, 8500, 3, 99,
  ARRAY['images/produits/ecouteurs-jm19.avif'],
  true, '🎧', 4
),
(
  'ecouteurs-k4-entry', 'High-Tech FGS', '💸 Bon plan', 'pb-teal',
  'AirPods Bluetooth BT 5.4',
  'Son propre, connexion rapide et stable en Bluetooth 5.4, faible latence pour les vidéos et les jeux. Étanche, LED sur le boîtier, autonomie correcte. L''essentiel sans se ruiner.',
  ARRAY['Bluetooth 5.4','Faible latence','Waterproof','LED boîtier','TWS sans fil'],
  4000, 3000, 3, 99,
  ARRAY['images/produits/ecouteurs-k4.png'],
  true, '🎧', 5
)
ON CONFLICT (slug) DO UPDATE SET
  nom             = EXCLUDED.nom,
  description     = EXCLUDED.description,
  specs           = EXCLUDED.specs,
  photos          = EXCLUDED.photos,
  prix_public     = EXCLUDED.prix_public,
  prix_revendeur  = EXCLUDED.prix_revendeur,
  min_qty_revendeur = EXCLUDED.min_qty_revendeur,
  badge           = EXCLUDED.badge,
  badge_class     = EXCLUDED.badge_class,
  emoji           = EXCLUDED.emoji,
  ordre           = EXCLUDED.ordre;
