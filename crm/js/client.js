import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

export const sb = createClient(
  "https://krffbvfbmztwgmdmwkgi.supabase.co",
  "sb_publishable_6TQI0kPaNDgsx_N9mfd2GQ_Q2pbUjOb",
);

export async function requireAuth() {
  const {
    data: { session },
  } = await sb.auth.getSession();
  if (!session) {
    window.location.href = "/crm/login.html";
    return null;
  }
  return session;
}

export async function getProfile(userId) {
  const { data } = await sb
    .from("profiles")
    .select("*")
    .eq("id", userId)
    .single();
  return data;
}

export const STATUTS = {
  nouveau: { label: "Nouveau", color: "#6366f1" },
  contacte: { label: "Contacté", color: "#8b5cf6" },
  devis: { label: "Devis", color: "#f59e0b" },
  commande: { label: "Commande", color: "#1a7a6e" },
  livre: { label: "Livré", color: "#10b981" },
  fidele: { label: "Fidèle", color: "#b08a3e" },
  perdu: { label: "Perdu", color: "#6b7280" },
};

export const CANAUX = {
  whatsapp: "WhatsApp",
  site: "Site web",
  bouche_oreille: "Bouche à oreille",
  social: "Réseaux sociaux",
  autre: "Autre",
};

export const STATUTS_PAIEMENT = {
  en_attente: { label: "En attente", color: "#f59e0b" },
  acompte_recu: { label: "Acompte reçu", color: "#6366f1" },
  solde: { label: "Soldé", color: "#10b981" },
  annule: { label: "Annulé", color: "#6b7280" },
};

export const STATUTS_LIVRAISON = {
  en_attente: { label: "En attente", color: "#f59e0b" },
  en_preparation: { label: "En préparation", color: "#8b5cf6" },
  expedie: { label: "Expédié", color: "#6366f1" },
  livre: { label: "Livré", color: "#10b981" },
  annule: { label: "Annulé", color: "#6b7280" },
};

export function formatDate(iso) {
  if (!iso) return "—";
  return new Date(iso).toLocaleDateString("fr-FR", {
    day: "2-digit",
    month: "short",
    year: "numeric",
  });
}

export function formatMoney(n) {
  if (!n) return "0 FCFA";
  return Number(n).toLocaleString("fr-FR") + " FCFA";
}

export function initials(nom, prenom) {
  return ((prenom?.[0] || "") + (nom?.[0] || "")).toUpperCase() || "?";
}

export function avatarColor(statut) {
  return STATUTS[statut]?.color || "#6b7280";
}

export function badge(statut, map = STATUTS) {
  const s = map[statut] || { label: statut, color: "#6b7280" };
  return `<span style="background:${s.color}20;color:${s.color};border:1px solid ${s.color}40;padding:2px 10px;border-radius:99px;font-size:12px;font-weight:600">${s.label}</span>`;
}

export function bottomNav(active) {
  const pages = [
    { id: "index", icon: "⊞", label: "Dashboard", href: "/crm/index.html" },
    {
      id: "contacts",
      icon: "👥",
      label: "Contacts",
      href: "/crm/contacts.html",
    },
    {
      id: "commandes",
      icon: "📦",
      label: "Commandes",
      href: "/crm/commandes.html",
    },
    {
      id: "catalogue",
      icon: "🛒",
      label: "Catalogue",
      href: "/crm/catalogue.html",
      adminOnly: true,
    },
  ];
  return pages;
}
