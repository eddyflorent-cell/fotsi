-- ════════════════════════════════════════════════════════════════════════════
-- FGS CRM — Contenu du site (articles, photos, promos, témoignages)
-- À exécuter dans Supabase SQL Editor (après schema.sql)
--
-- Cette table existait déjà en usage (crm/contenu.html) mais n'avait jamais
-- été versionnée dans un fichier schema_*.sql — elle n'apparaissait qu'en
-- avertissement inline dans le JS si absente. Ce fichier la formalise.
-- ════════════════════════════════════════════════════════════════════════════

CREATE OR REPLACE FUNCTION is_admin()
RETURNS BOOLEAN AS $$
  SELECT EXISTS (SELECT 1 FROM profiles WHERE id = auth.uid() AND role = 'admin');
$$ LANGUAGE sql SECURITY DEFINER STABLE;

CREATE TABLE IF NOT EXISTS contenus_site (
  id         UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  type       TEXT NOT NULL CHECK (type IN ('article','photo','promo','temoignage')),
  titre      TEXT,
  resume     TEXT,
  contenu    TEXT,
  image_url  TEXT,
  statut     TEXT DEFAULT 'brouillon' CHECK (statut IN ('brouillon','publie','archive','en_attente','rejete')),
  meta       JSONB DEFAULT '{}'
);

ALTER TABLE contenus_site ENABLE ROW LEVEL SECURITY;
-- Toute personne connectée au CRM peut consulter le contenu (vue + suggestions
-- pour le rôle commercial), mais seul un admin publie/modifie/supprime.
CREATE POLICY "auth_read_contenu"   ON contenus_site FOR SELECT USING (auth.role() = 'authenticated');
CREATE POLICY "admin_write_contenu" ON contenus_site FOR INSERT WITH CHECK (is_admin());
CREATE POLICY "admin_update_contenu" ON contenus_site FOR UPDATE USING (is_admin()) WITH CHECK (is_admin());
CREATE POLICY "admin_delete_contenu" ON contenus_site FOR DELETE USING (is_admin());
