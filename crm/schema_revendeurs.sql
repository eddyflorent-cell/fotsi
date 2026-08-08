-- ════════════════════════════════════════════════════════════════════════════
-- FGS CRM — Extension revendeurs / apporteurs d'affaire
-- À exécuter dans Supabase SQL Editor (après schema.sql et schema_compta.sql)
-- ════════════════════════════════════════════════════════════════════════════

-- ── 1. REVENDEURS ─────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS revendeurs (
  id           UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  created_at   TIMESTAMPTZ DEFAULT NOW(),
  updated_at   TIMESTAMPTZ DEFAULT NOW(),
  nom          TEXT NOT NULL,
  prenom       TEXT,
  telephone    TEXT,
  om           TEXT,                          -- numéro Orange Money (paiement des ventes en gros)
  ville        TEXT,
  statut       TEXT DEFAULT 'actif' CHECK (statut IN ('actif','suspendu')),
  notes        TEXT
);

ALTER TABLE revendeurs ENABLE ROW LEVEL SECURITY;
-- Gestion des revendeurs ouverte à toute personne connectée au CRM (Wendy
-- gère l'opération Cameroun au quotidien, y compris l'onboarding des
-- revendeurs) — pas réservé à l'admin.
DROP POLICY IF EXISTS "auth_all_revendeurs" ON revendeurs;
CREATE POLICY "auth_all_revendeurs" ON revendeurs FOR ALL USING (auth.role() = 'authenticated');
DROP TRIGGER IF EXISTS revendeurs_updated_at ON revendeurs;
CREATE TRIGGER revendeurs_updated_at BEFORE UPDATE ON revendeurs
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- ── 2. TRAÇABILITÉ SUR LES COMMANDES ─────────────────────────────────────────
-- Permet de savoir qu'une commande a été apportée par un revendeur donné
ALTER TABLE commandes ADD COLUMN IF NOT EXISTS revendeur_id UUID REFERENCES revendeurs(id) ON DELETE SET NULL;

-- ── 3. TRAÇABILITÉ SUR LES DOCUMENTS (factures/reçus) ────────────────────────
-- emis_par : 'fgs' = document classique au nom de FGS (ex: facture de gros au revendeur)
--            'revendeur' = document émis au nom du revendeur pour son client final
--            (FGS n'apparaît pas comme vendeur sur ce document)
ALTER TABLE documents_generes ADD COLUMN IF NOT EXISTS revendeur_id UUID REFERENCES revendeurs(id) ON DELETE SET NULL;
ALTER TABLE documents_generes ADD COLUMN IF NOT EXISTS emis_par TEXT DEFAULT 'fgs' CHECK (emis_par IN ('fgs','revendeur'));
