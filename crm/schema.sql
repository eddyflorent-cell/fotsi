-- ── PROFILES (rôles utilisateurs) ───────────────────────────────────────────
CREATE TABLE profiles (
  id UUID REFERENCES auth.users PRIMARY KEY,
  nom TEXT NOT NULL,
  role TEXT NOT NULL CHECK (role IN ('admin', 'commercial')),
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ── CONTACTS / PROSPECTS ─────────────────────────────────────────────────────
CREATE TABLE contacts (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  nom TEXT NOT NULL,
  prenom TEXT,
  telephone TEXT,
  email TEXT,
  ville TEXT,
  pays TEXT DEFAULT 'CM',
  canal TEXT DEFAULT 'autre' CHECK (canal IN ('whatsapp','site','bouche_oreille','social','autre')),
  statut TEXT DEFAULT 'nouveau' CHECK (statut IN ('nouveau','contacte','devis','commande','livre','fidele','perdu')),
  produits_interesses TEXT[],
  notes TEXT,
  assigned_to UUID REFERENCES profiles(id)
);

-- ── COMMANDES ────────────────────────────────────────────────────────────────
CREATE TABLE commandes (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  contact_id UUID REFERENCES contacts(id) ON DELETE CASCADE,
  reference TEXT DEFAULT ('CMD-' || to_char(NOW(), 'YYYYMMDD-') || substr(gen_random_uuid()::text, 1, 6)),
  produits JSONB DEFAULT '[]',
  montant_total NUMERIC(12,0) DEFAULT 0,
  acompte_verse NUMERIC(12,0) DEFAULT 0,
  statut_paiement TEXT DEFAULT 'en_attente' CHECK (statut_paiement IN ('en_attente','acompte_recu','solde','annule')),
  statut_livraison TEXT DEFAULT 'en_attente' CHECK (statut_livraison IN ('en_attente','en_preparation','expedie','livre','annule')),
  mode_paiement TEXT DEFAULT 'orange_money' CHECK (mode_paiement IN ('orange_money','mtn_money','especes','paypal','autre')),
  notes TEXT
);

-- ── INTERACTIONS (historique) ─────────────────────────────────────────────────
CREATE TABLE interactions (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  contact_id UUID REFERENCES contacts(id) ON DELETE CASCADE,
  type TEXT CHECK (type IN ('note','appel','whatsapp','email','visite','commande')),
  contenu TEXT NOT NULL,
  created_by UUID REFERENCES profiles(id)
);

-- ── RELANCES ─────────────────────────────────────────────────────────────────
CREATE TABLE relances (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  contact_id UUID REFERENCES contacts(id) ON DELETE CASCADE,
  date_relance DATE NOT NULL,
  motif TEXT,
  fait BOOLEAN DEFAULT FALSE,
  created_by UUID REFERENCES profiles(id)
);

-- ── RLS (Row Level Security) ──────────────────────────────────────────────────
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE contacts ENABLE ROW LEVEL SECURITY;
ALTER TABLE commandes ENABLE ROW LEVEL SECURITY;
ALTER TABLE interactions ENABLE ROW LEVEL SECURITY;
ALTER TABLE relances ENABLE ROW LEVEL SECURITY;

-- Tout utilisateur connecté peut tout lire/écrire (contrôle rôle côté front)
CREATE POLICY "auth_read_profiles"    ON profiles    FOR ALL USING (auth.role() = 'authenticated');
CREATE POLICY "auth_all_contacts"     ON contacts    FOR ALL USING (auth.role() = 'authenticated');
CREATE POLICY "auth_all_commandes"    ON commandes   FOR ALL USING (auth.role() = 'authenticated');
CREATE POLICY "auth_all_interactions" ON interactions FOR ALL USING (auth.role() = 'authenticated');
CREATE POLICY "auth_all_relances"     ON relances    FOR ALL USING (auth.role() = 'authenticated');

-- ── TRIGGER updated_at ───────────────────────────────────────────────────────
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$ BEGIN NEW.updated_at = NOW(); RETURN NEW; END; $$ LANGUAGE plpgsql;

CREATE TRIGGER contacts_updated_at  BEFORE UPDATE ON contacts  FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER commandes_updated_at BEFORE UPDATE ON commandes FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- ── FONCTION auto-profile à l'inscription ────────────────────────────────────
CREATE OR REPLACE FUNCTION handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO profiles (id, nom, role)
  VALUES (NEW.id, COALESCE(NEW.raw_user_meta_data->>'nom', NEW.email), COALESCE(NEW.raw_user_meta_data->>'role', 'commercial'));
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION handle_new_user();
