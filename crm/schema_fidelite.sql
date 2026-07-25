-- ════════════════════════════════════════════════════════════════════════════
-- FGS CRM — Fidélité & Notation clients
-- À exécuter dans Supabase SQL Editor
-- ════════════════════════════════════════════════════════════════════════════

-- ── 1. COLONNES À AJOUTER SUR contacts ───────────────────────────────────────
ALTER TABLE contacts ADD COLUMN IF NOT EXISTS score       INTEGER DEFAULT 0;
ALTER TABLE contacts ADD COLUMN IF NOT EXISTS niveau      TEXT DEFAULT 'bronze'
  CHECK (niveau IN ('bronze','argent','or','platine'));
ALTER TABLE contacts ADD COLUMN IF NOT EXISTS parrain_id  UUID REFERENCES contacts(id) ON DELETE SET NULL;
ALTER TABLE contacts ADD COLUMN IF NOT EXISTS notes_privees TEXT;
-- notes_privees = commentaires internes (non partagés avec Wendy)
-- notes existant déjà = notes générales visibles

-- ── 2. FONCTION DE CALCUL DU SCORE ───────────────────────────────────────────
-- Score = CA facturé (÷1000 FCFA = 1pt) + filleuls×50pts + ancienneté×2pts/mois + bonus fidèle
CREATE OR REPLACE FUNCTION calc_score(p_contact_id UUID)
RETURNS INTEGER AS $$
DECLARE
  v_ca          NUMERIC  := 0;
  v_filleuls    INTEGER  := 0;
  v_mois        INTEGER  := 0;
  v_statut      TEXT;
  v_score       INTEGER  := 0;
BEGIN
  -- CA total des factures et reçus non annulés
  SELECT COALESCE(SUM(montant_ttc),0) INTO v_ca
  FROM documents_generes
  WHERE contact_id = p_contact_id AND type IN ('facture','recu') AND statut NOT IN ('annule','refuse');

  -- Nombre de clients apportés (filleuls directs)
  SELECT COUNT(*) INTO v_filleuls
  FROM contacts WHERE parrain_id = p_contact_id;

  -- Ancienneté en mois
  SELECT EXTRACT(MONTH FROM AGE(NOW(), created_at))::INTEGER INTO v_mois
  FROM contacts WHERE id = p_contact_id;

  -- Statut
  SELECT statut INTO v_statut FROM contacts WHERE id = p_contact_id;

  -- Calcul
  v_score := FLOOR(v_ca / 1000)          -- 1 pt par 1 000 FCFA de CA
           + (v_filleuls * 50)            -- 50 pts par filleul apporté
           + (v_mois * 2)                 -- 2 pts par mois d'ancienneté
           + CASE v_statut WHEN 'fidele' THEN 100 ELSE 0 END; -- bonus fidèle

  RETURN GREATEST(v_score, 0);
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- ── 3. FONCTION DE MISE À JOUR DU NIVEAU ─────────────────────────────────────
CREATE OR REPLACE FUNCTION update_contact_niveau(p_contact_id UUID)
RETURNS VOID AS $$
DECLARE
  v_score  INTEGER;
  v_niveau TEXT;
BEGIN
  v_score := calc_score(p_contact_id);

  v_niveau := CASE
    WHEN v_score >= 1000 THEN 'platine'
    WHEN v_score >= 300  THEN 'or'
    WHEN v_score >= 100  THEN 'argent'
    ELSE 'bronze'
  END;

  UPDATE contacts SET score = v_score, niveau = v_niveau WHERE id = p_contact_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- ── 4. RECALCUL EN MASSE (à lancer une fois puis après chaque facture) ────────
-- SELECT update_contact_niveau(id) FROM contacts;

-- ── 5. RPC APPELABLE DEPUIS LE FRONT ─────────────────────────────────────────
CREATE OR REPLACE FUNCTION recalc_score(p_contact_id UUID)
RETURNS JSONB AS $$
DECLARE
  v_score  INTEGER;
  v_niveau TEXT;
BEGIN
  PERFORM update_contact_niveau(p_contact_id);
  SELECT score, niveau INTO v_score, v_niveau FROM contacts WHERE id = p_contact_id;
  RETURN jsonb_build_object('score', v_score, 'niveau', v_niveau);
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
