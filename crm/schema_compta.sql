-- ════════════════════════════════════════════════════════════════════════════
-- FGS CRM — Extension comptable
-- À exécuter dans Supabase SQL Editor (après schema.sql)
-- ════════════════════════════════════════════════════════════════════════════

-- ── 1. SÉQUENCES DE NUMÉROTATION ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS doc_sequences (
  type    TEXT    NOT NULL,
  annee   INTEGER NOT NULL,
  dernier_num INTEGER DEFAULT 0,
  PRIMARY KEY (type, annee)
);

ALTER TABLE doc_sequences ENABLE ROW LEVEL SECURITY;
CREATE POLICY "auth_sequences" ON doc_sequences FOR ALL USING (auth.role() = 'authenticated');

-- Fonction atomique (pas de doublon même en concurrence)
CREATE OR REPLACE FUNCTION next_doc_number(p_type TEXT)
RETURNS TEXT AS $$
DECLARE
  v_annee  INTEGER := EXTRACT(YEAR FROM NOW())::INTEGER;
  v_num    INTEGER;
  v_prefix TEXT;
BEGIN
  INSERT INTO doc_sequences(type, annee, dernier_num)
  VALUES (p_type, v_annee, 1)
  ON CONFLICT (type, annee)
  DO UPDATE SET dernier_num = doc_sequences.dernier_num + 1
  RETURNING dernier_num INTO v_num;

  v_prefix := CASE p_type
    WHEN 'facture'      THEN 'FA'
    WHEN 'devis'        THEN 'DV'
    WHEN 'bon_commande' THEN 'BC'
    WHEN 'recu'         THEN 'RC'
    ELSE 'DOC'
  END;

  RETURN v_prefix || '-' || v_annee || '-' || LPAD(v_num::TEXT, 4, '0');
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- ── 2. JOURNAL DES DOCUMENTS GÉNÉRÉS ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS documents_generes (
  id           UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  created_at   TIMESTAMPTZ DEFAULT NOW(),
  updated_at   TIMESTAMPTZ DEFAULT NOW(),
  type         TEXT NOT NULL CHECK (type IN ('facture','devis','bon_commande','recu','courrier','bon_reduction')),
  numero       TEXT NOT NULL UNIQUE,          -- FA-2026-0001
  contact_id   UUID REFERENCES contacts(id) ON DELETE SET NULL,
  commande_id  UUID REFERENCES commandes(id) ON DELETE SET NULL,
  objet        TEXT,                          -- description libre
  montant_ht   NUMERIC(14,2) DEFAULT 0,
  tva_pct      NUMERIC(5,2)  DEFAULT 0,      -- 0 au Cameroun (non assujetti TVA)
  montant_ttc  NUMERIC(14,2) DEFAULT 0,
  montant_regle NUMERIC(14,2) DEFAULT 0,     -- ce qui a été encaissé
  statut       TEXT DEFAULT 'brouillon'
                CHECK (statut IN ('brouillon','emis','accepte','paye','partiellement_paye','annule','refuse')),
  date_emission DATE DEFAULT CURRENT_DATE,
  date_echeance DATE,
  mode_paiement TEXT,
  data         JSONB DEFAULT '{}',           -- snapshot complet du document
  notes        TEXT,
  created_by   UUID REFERENCES auth.users(id)
);

ALTER TABLE documents_generes ENABLE ROW LEVEL SECURITY;
CREATE POLICY "auth_documents" ON documents_generes FOR ALL USING (auth.role() = 'authenticated');
CREATE TRIGGER documents_updated_at BEFORE UPDATE ON documents_generes
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- ── 3. ENTRÉES DE TRÉSORERIE (recettes & dépenses) ───────────────────────────
-- Pour un bilan simplifié sans logiciel comptable externe
CREATE TABLE IF NOT EXISTS tresorerie (
  id           UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  created_at   TIMESTAMPTZ DEFAULT NOW(),
  date_op      DATE NOT NULL DEFAULT CURRENT_DATE,
  type         TEXT NOT NULL CHECK (type IN ('recette','depense')),
  categorie    TEXT NOT NULL DEFAULT 'autre',
  -- Catégories recettes : vente_produit, vente_service, acompte, remboursement, autre
  -- Catégories dépenses : achat_stock, transport, loyer, salaire, marketing, telecom, autre
  libelle      TEXT NOT NULL,
  montant      NUMERIC(14,2) NOT NULL CHECK (montant > 0),
  mode_paiement TEXT,
  document_id  UUID REFERENCES documents_generes(id) ON DELETE SET NULL,
  contact_id   UUID REFERENCES contacts(id) ON DELETE SET NULL,
  created_by   UUID REFERENCES auth.users(id)
);

ALTER TABLE tresorerie ENABLE ROW LEVEL SECURITY;
CREATE POLICY "auth_tresorerie" ON tresorerie FOR ALL USING (auth.role() = 'authenticated');

-- ── 4. VUE : RÉSUMÉ MENSUEL (CA + encaissé) ──────────────────────────────────
CREATE OR REPLACE VIEW v_ca_mensuel AS
SELECT
  DATE_TRUNC('month', date_emission)::DATE AS mois,
  COUNT(*) FILTER (WHERE type IN ('facture','recu')) AS nb_factures,
  COALESCE(SUM(montant_ttc) FILTER (WHERE type IN ('facture','recu') AND statut NOT IN ('annule','refuse')), 0) AS ca_facture,
  COALESCE(SUM(montant_regle) FILTER (WHERE type IN ('facture','recu')), 0) AS ca_encaisse
FROM documents_generes
GROUP BY 1
ORDER BY 1 DESC;

-- Vue dépenses mensuelles
CREATE OR REPLACE VIEW v_depenses_mensuelles AS
SELECT
  DATE_TRUNC('month', date_op)::DATE AS mois,
  categorie,
  COUNT(*) AS nb_ops,
  SUM(montant) AS total
FROM tresorerie
WHERE type = 'depense'
GROUP BY 1, 2
ORDER BY 1 DESC, 4 DESC;
