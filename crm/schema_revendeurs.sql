-- ════════════════════════════════════════════════════════════════════════════
-- FGS CRM — Extension revendeurs / apporteurs d'affaire
-- À exécuter dans Supabase SQL Editor (après schema.sql et schema_compta.sql)
-- ════════════════════════════════════════════════════════════════════════════

-- ── 0. HELPER : l'utilisateur connecté est-il admin ? ────────────────────────
-- SECURITY DEFINER pour pouvoir lire profiles sans se heurter à ses propres
-- policies RLS (évite toute récursion). Réutilisé par les policies ci-dessous.
CREATE OR REPLACE FUNCTION is_admin()
RETURNS BOOLEAN AS $$
  SELECT EXISTS (SELECT 1 FROM profiles WHERE id = auth.uid() AND role = 'admin');
$$ LANGUAGE sql SECURITY DEFINER STABLE;

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
-- Toute personne connectée au CRM peut consulter les revendeurs (nécessaire
-- pour facturer en leur nom depuis Documents), mais seul un admin peut en
-- créer/modifier/supprimer — c'est justement le point de ce module : éviter
-- que n'importe qui negocie des accords revendeur sans validation d'Eddy.
CREATE POLICY "auth_read_revendeurs" ON revendeurs FOR SELECT USING (auth.role() = 'authenticated');
CREATE POLICY "admin_write_revendeurs" ON revendeurs FOR INSERT WITH CHECK (is_admin());
CREATE POLICY "admin_update_revendeurs" ON revendeurs FOR UPDATE USING (is_admin()) WITH CHECK (is_admin());
CREATE POLICY "admin_delete_revendeurs" ON revendeurs FOR DELETE USING (is_admin());
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
