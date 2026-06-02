"""
FGS Studio — Générateur de PDFs fillables
Produit : brief-client.pdf et devis-type.pdf
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white, black
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.enums import TA_LEFT, TA_CENTER

W, H = A4

# Couleurs FGS
NAVY    = HexColor('#0f2d52')
NAVY_MID= HexColor('#1a4070')
TEAL    = HexColor('#1a7a6e')
TEAL_LT = HexColor('#e8f5f3')
GOLD    = HexColor('#b08a3e')
GOLD_BG = HexColor('#fdf6e8')
SURFACE = HexColor('#f0f2f5')
BORDER  = HexColor('#dde4ec')
TEXT    = HexColor('#0f1e2e')
TEXT_MID= HexColor('#3a5068')
TEXT_SOFT=HexColor('#6a8399')
PAGE_BG = HexColor('#f7f8fa')

def draw_header(c, title, subtitle):
    c.setFillColor(NAVY)
    c.rect(0, H - 28*mm, W, 28*mm, fill=1, stroke=0)
    c.setFillColor(TEAL)
    c.rect(0, H - 29.5*mm, W, 1.5*mm, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 15)
    c.drawString(14*mm, H - 13*mm, title)
    c.setFont("Helvetica", 8)
    c.setFillColor(HexColor('#a0b4c4'))
    c.drawString(14*mm, H - 19*mm, subtitle)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 7)
    c.drawRightString(W - 14*mm, H - 14*mm, "Fotsi Global Services")
    c.setFont("Helvetica", 7)
    c.drawRightString(W - 14*mm, H - 19*mm, "contact@fotsiglobalservices.com")

def draw_footer(c, page_num, total):
    c.setFillColor(NAVY)
    c.rect(0, 0, W, 10*mm, fill=1, stroke=0)
    c.setFillColor(HexColor('#a0b4c4'))
    c.setFont("Helvetica", 7)
    c.drawString(14*mm, 3.5*mm, "FGS Studio — Document confidentiel")
    c.drawRightString(W - 14*mm, 3.5*mm, f"Page {page_num}/{total}")

def section_title(c, y, num, label, color=TEAL):
    c.setFillColor(color)
    c.roundRect(12*mm, y - 5*mm, W - 24*mm, 8*mm, 2*mm, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(16*mm, y - 2*mm, f"{num}. {label.upper()}")
    return y - 12*mm

def field_label(c, x, y, label, required=False):
    c.setFillColor(TEXT_MID)
    c.setFont("Helvetica-Bold", 7.5)
    c.drawString(x, y, label)
    if required:
        c.setFillColor(HexColor('#c0392b'))
        c.drawString(x + c.stringWidth(label, "Helvetica-Bold", 7.5) + 1, y, " *")
    return y - 4*mm

def text_field(c, name, x, y, w, h=6*mm, font_size=8):
    c.setFillColor(white)
    c.setStrokeColor(BORDER)
    c.roundRect(x, y - h, w, h, 1.5*mm, fill=1, stroke=1)
    c.acroForm.textfield(
        name=name,
        x=x + 1.5*mm, y=y - h + 1*mm,
        width=w - 3*mm, height=h - 2*mm,
        fontSize=font_size,
        fontName="Helvetica",
        fillColor=white,
        borderColor=None,
        textColor=black,
    )
    return y - h - 2*mm

def textarea_field(c, name, x, y, w, h=14*mm, font_size=8):
    c.setFillColor(white)
    c.setStrokeColor(BORDER)
    c.roundRect(x, y - h, w, h, 1.5*mm, fill=1, stroke=1)
    c.acroForm.textfield(
        name=name,
        x=x + 1.5*mm, y=y - h + 1*mm,
        width=w - 3*mm, height=h - 2*mm,
        fontSize=font_size,
        fontName="Helvetica",
        fillColor=white,
        borderColor=None,
        textColor=black,
        fieldFlags="multiline",
    )
    return y - h - 2*mm

def checkbox_row(c, name, x, y, label, size=3.5*mm):
    c.acroForm.checkbox(
        name=name,
        x=x, y=y - size,
        size=size,
        fillColor=white,
        borderColor=BORDER,
        forceBorder=True,
    )
    c.setFillColor(TEXT)
    c.setFont("Helvetica", 8)
    c.drawString(x + size + 2*mm, y - size + 0.8*mm, label)
    return y - size - 2*mm

def two_col(W):
    col_w = (W - 24*mm - 4*mm) / 2
    x1 = 14*mm
    x2 = 14*mm + col_w + 4*mm
    return x1, x2, col_w


# ─────────────────────────────────────────────
# PDF 1 — BRIEF CLIENT
# ─────────────────────────────────────────────

def generate_brief():
    path = "brief-client.pdf"
    c = canvas.Canvas(path, pagesize=A4)
    c.setTitle("FGS Studio — Brief Client")
    c.setAuthor("Fotsi Global Services")

    # ── PAGE 1 ──
    c.setFillColor(PAGE_BG)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    draw_header(c, "Brief Client — FGS Studio",
                "À remplir lors de notre premier échange · 15–20 min · Aucune connaissance technique requise")
    draw_footer(c, 1, 2)

    y = H - 35*mm

    # Section 1 — Projet
    y = section_title(c, y, 1, "Votre projet en quelques mots")

    x1, x2, cw = two_col(W)

    field_label(c, x1, y, "Nom du projet / de l'entreprise", required=True)
    y = text_field(c, "nom_projet", x1, y - 4*mm, cw)

    y2_start = y + 6*mm + 4*mm
    field_label(c, x2, y2_start, "Secteur d'activité", required=True)
    text_field(c, "secteur", x2, y2_start - 4*mm, cw)

    field_label(c, x1, y, "Décris ce que tu fais / vends", required=True)
    y = textarea_field(c, "description", x1, y - 4*mm, W - 28*mm, 12*mm)

    field_label(c, x1, y, "Qui sont tes clients ? (âge, lieu, profil)")
    y2b = y
    y = text_field(c, "clients_cibles", x1, y - 4*mm, cw)

    field_label(c, x2, y2b, "Ville / pays principal d'activité")
    text_field(c, "ville_pays", x2, y2b - 4*mm, cw)

    y -= 2*mm

    # Section 2 — Ce que tu veux
    y = section_title(c, y, 2, "Ce que tu veux construire")

    c.setFillColor(TEXT_MID)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x1, y, "Quel type d'outil ?")
    y -= 5*mm

    types = [
        ("type_vitrine",  "Site vitrine — être trouvé en ligne"),
        ("type_ecom",     "E-commerce — vendre en ligne"),
        ("type_gestion",  "Application de gestion"),
        ("type_mobile",   "Application mobile (iOS / Android)"),
    ]
    col_break = len(types) // 2
    y_cb = y
    for i, (name, label) in enumerate(types):
        if i == col_break:
            y = y_cb
            x1_cb = x2
        else:
            x1_cb = x1
        y_tmp = checkbox_row(c, name, x1_cb, y, label)
        if i < col_break:
            y = y_tmp

    y -= 2*mm
    field_label(c, x1, y, "Autre type d'outil :")
    y = text_field(c, "type_autre", x1, y - 4*mm, W - 28*mm)

    c.setFillColor(TEXT_MID)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x1, y, "Fonctionnalités souhaitées (en langage simple) :")
    y -= 4*mm

    for i in range(1, 4):
        field_label(c, x1, y, f"{i}.")
        y = text_field(c, f"fonc_{i}", x1 + 6*mm, y - 4*mm, W - 34*mm)

    y -= 1*mm
    c.setFillColor(TEXT_SOFT)
    c.setFont("Helvetica-Oblique", 7)
    c.drawString(x1, y, 'Exemples : "les clients peuvent réserver", "je vois mes commandes du jour", "envoi automatique de factures"')
    y -= 4*mm

    field_label(c, x1, y, "Tu as déjà un site / outil en place ?")
    y = text_field(c, "existant", x1, y - 4*mm, W - 28*mm)

    field_label(c, x1, y, "Des sites ou apps qui te plaisent ? (pour le style)")
    y = text_field(c, "inspirations", x1, y - 4*mm, W - 28*mm)

    c.showPage()

    # ── PAGE 2 ──
    c.setFillColor(PAGE_BG)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    draw_header(c, "Brief Client — FGS Studio (suite)",
                "Page 2 / 2")
    draw_footer(c, 2, 2)

    y = H - 35*mm
    x1, x2, cw = two_col(W)

    # Section 3 — Présence en ligne
    y = section_title(c, y, 3, "Présence en ligne existante")

    c.setFillColor(TEXT_MID)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x1, y, "Réseaux sociaux actifs :")
    y -= 5*mm

    socials = [
        ("rs_instagram", "Instagram →"), ("rs_facebook", "Facebook →"),
        ("rs_tiktok",    "TikTok →"),    ("rs_linkedin",  "LinkedIn →"),
    ]
    y_rs = y
    for i, (name, label) in enumerate(socials):
        col = x1 if i % 2 == 0 else x2
        if i % 2 == 0 and i > 0:
            y_rs = y
        c.acroForm.checkbox(name=name, x=col, y=y_rs - 3.5*mm,
                            size=3.5*mm, fillColor=white, borderColor=BORDER, forceBorder=True)
        c.setFillColor(TEXT)
        c.setFont("Helvetica", 8)
        c.drawString(col + 5*mm, y_rs - 2.5*mm, label)
        tf_x = col + 5*mm + c.stringWidth(label, "Helvetica", 8) + 2*mm
        tf_w = cw - 5*mm - c.stringWidth(label, "Helvetica", 8) - 4*mm
        c.acroForm.textfield(name=f"{name}_handle",
                             x=tf_x, y=y_rs - 3.5*mm,
                             width=tf_w, height=3.5*mm,
                             fontSize=7, fontName="Helvetica",
                             fillColor=white, borderColor=None)
        c.setStrokeColor(BORDER)
        c.line(tf_x, y_rs - 3.5*mm, tf_x + tf_w, y_rs - 3.5*mm)
        if i % 2 == 1:
            y_rs -= 6*mm
    y = y_rs - 4*mm

    c.setFillColor(TEXT_MID)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x1, y, "Langue(s) du site :")
    y -= 5*mm

    langs = [("lang_fr", "Français"), ("lang_en", "Anglais"), ("lang_both", "Français + Anglais")]
    for name, label in langs:
        y = checkbox_row(c, name, x1, y, label)
    field_label(c, x1, y, "Autre langue :")
    y = text_field(c, "lang_autre", x1, y - 4*mm, cw)

    c.setFillColor(TEXT_MID)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x2, y + 6*mm + 4*mm + 5*mm, "Référencement Google important ?")
    y_seo = y + 6*mm + 4*mm
    for name, label in [("seo_oui","Oui, prioritaire"),("seo_maybe","Oui, mais pas urgent"),("seo_non","Non / Je ne sais pas")]:
        y_seo = checkbox_row(c, name, x2, y_seo, label)

    y -= 2*mm

    # Section 4 — Contenu
    y = section_title(c, y, 4, "Contenu disponible")

    items = [
        ("cont_logo",    "Logo"),
        ("cont_photos",  "Photos produits / équipe"),
        ("cont_textes",  "Textes de présentation"),
        ("cont_videos",  "Vidéos"),
        ("cont_domaine", "Nom de domaine déjà acheté"),
        ("cont_hebergement", "Hébergement existant"),
        ("cont_email",   "Email professionnel"),
    ]
    col_break = 4
    y_ct = y
    y_ct2 = y
    for i, (name, label) in enumerate(items):
        if i < col_break:
            y_ct = checkbox_row(c, name, x1, y_ct, label)
        else:
            y_ct2 = checkbox_row(c, name, x2, y_ct2, label)
    y = min(y_ct, y_ct2) - 2*mm

    c.setFillColor(TEAL_LT)
    c.roundRect(x1, y - 6*mm, W - 28*mm, 6*mm, 1.5*mm, fill=1, stroke=0)
    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 7.5)
    c.drawString(x1 + 3*mm, y - 4*mm, "Si Non sur tout → FGS s'occupe de créer et centraliser. Aucun souci.")
    y -= 9*mm

    # Section 5 — Budget
    y = section_title(c, y, 5, "Budget & délai")

    field_label(c, x1, y, "Budget approximatif")
    y2_b = y
    y = text_field(c, "budget", x1, y - 4*mm, cw)

    field_label(c, x2, y2_b, "Délai souhaité pour la mise en ligne")
    text_field(c, "delai", x2, y2_b - 4*mm, cw)

    field_label(c, x1, y, "Délai impératif (événement, lancement...)")
    y = text_field(c, "delai_imperatif", x1, y - 4*mm, W - 28*mm)

    # Section 6 — Contact
    y = section_title(c, y, 6, "Contact & disponibilité")

    field_label(c, x1, y, "Prénom / Nom", required=True)
    y2_c = y
    y = text_field(c, "contact_nom", x1, y - 4*mm, cw)

    field_label(c, x2, y2_c, "WhatsApp", required=True)
    text_field(c, "contact_wa", x2, y2_c - 4*mm, cw)

    field_label(c, x1, y, "Email")
    y2_d = y
    y = text_field(c, "contact_email", x1, y - 4*mm, cw)

    field_label(c, x2, y2_d, "Meilleur moment pour un appel")
    text_field(c, "contact_dispo", x2, y2_d - 4*mm, cw)

    c.save()
    print(f"OK: {path}")


# ─────────────────────────────────────────────
# PDF 2 — DEVIS
# ─────────────────────────────────────────────

def generate_devis():
    path = "devis-type.pdf"
    c = canvas.Canvas(path, pagesize=A4)
    c.setTitle("FGS Studio — Devis")
    c.setAuthor("Fotsi Global Services")

    def page_bg():
        c.setFillColor(PAGE_BG)
        c.rect(0, 0, W, H, fill=1, stroke=0)

    def divider(y, color=BORDER):
        c.setStrokeColor(color)
        c.setLineWidth(0.4)
        c.line(14*mm, y, W - 14*mm, y)

    def label_val(c, x, y, label, name, w, required=False):
        field_label(c, x, y, label, required)
        return text_field(c, name, x, y - 4*mm, w)

    # ── PAGE 1 ──
    page_bg()
    draw_header(c, "Devis — FGS Studio", "Trame à adapter avant envoi · Valable 30 jours")
    draw_footer(c, 1, 3)

    y = H - 35*mm
    x1, x2, cw = two_col(W)

    # En-tête devis
    c.setFillColor(SURFACE)
    c.roundRect(12*mm, y - 22*mm, W - 24*mm, 22*mm, 2*mm, fill=1, stroke=0)

    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x1, y - 4*mm, "NUMÉRO DE DEVIS")
    c.acroForm.textfield("num_devis", x=x1, y=y - 10*mm, width=cw,
                         height=5*mm, fontSize=9, fontName="Helvetica-Bold",
                         fillColor=HexColor('#f0f2f5'), borderColor=None)

    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x2, y - 4*mm, "DATE")
    c.acroForm.textfield("date_devis", x=x2, y=y - 10*mm, width=cw/2,
                         height=5*mm, fontSize=9, fontName="Helvetica",
                         fillColor=HexColor('#f0f2f5'), borderColor=None)

    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x1, y - 14*mm, "CLIENT")
    c.acroForm.textfield("client_nom", x=x1, y=y - 20*mm, width=cw,
                         height=5*mm, fontSize=9, fontName="Helvetica",
                         fillColor=HexColor('#f0f2f5'), borderColor=None)

    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x2, y - 14*mm, "WHATSAPP CLIENT")
    c.acroForm.textfield("client_wa", x=x2, y=y - 20*mm, width=cw,
                         height=5*mm, fontSize=9, fontName="Helvetica",
                         fillColor=HexColor('#f0f2f5'), borderColor=None)

    y -= 26*mm

    # Récap projet
    y = section_title(c, y, "·", "Récapitulatif du projet", color=NAVY_MID)

    y = label_val(c, x1, y, "Nom du projet", "projet_nom", cw)
    y2 = y + 6*mm + 4*mm
    label_val(c, x2, y2, "Type d'outil", "projet_type", cw)

    y = label_val(c, x1, y, "Délai estimé", "projet_delai", cw)
    y2b = y + 6*mm + 4*mm
    label_val(c, x2, y2b, "Hébergement", "projet_hebergement", cw)

    y -= 2*mm
    divider(y)
    y -= 6*mm

    # Poste 1 — Setup
    c.setFillColor(TEAL)
    c.roundRect(x1, y - 5*mm, W - 24*mm, 6*mm, 1.5*mm, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(x1 + 3*mm, y - 2.5*mm, "POSTE 1 — SETUP & INFRASTRUCTURE")
    c.setFont("Helvetica", 7)
    c.setFillColor(HexColor('#a0d8d3'))
    c.drawRightString(W - 16*mm, y - 2.5*mm, "Email · GitHub · Domaine · Hébergement · CI/CD")
    y -= 9*mm

    c.setFillColor(SURFACE)
    c.roundRect(x1, y - 7*mm, W - 28*mm, 7*mm, 1.5*mm, fill=1, stroke=0)
    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x1 + 3*mm, y - 4.5*mm, "Sous-total Setup")
    c.acroForm.textfield("setup_total", x=W - 50*mm, y=y - 6.5*mm,
                         width=34*mm, height=5*mm,
                         fontSize=9, fontName="Helvetica-Bold",
                         fillColor=white, borderColor=BORDER)
    y -= 11*mm

    # Poste 2 — Développement
    c.setFillColor(NAVY)
    c.roundRect(x1, y - 5*mm, W - 24*mm, 6*mm, 1.5*mm, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(x1 + 3*mm, y - 2.5*mm, "POSTE 2 — DÉVELOPPEMENT")
    y -= 9*mm

    dev_items = [
        ("dev_design",    "Design & maquette"),
        ("dev_frontend",  "Développement frontend"),
        ("dev_backend",   "Développement backend / BDD"),
        ("dev_stripe",    "Intégration paiement Stripe"),
        ("dev_auth",      "Authentification utilisateurs"),
        ("dev_f1",        "Fonctionnalité : _______________"),
        ("dev_f2",        "Fonctionnalité : _______________"),
    ]
    for name, label in dev_items:
        c.setFillColor(TEXT_SOFT)
        c.setFont("Helvetica", 7.5)
        c.drawString(x1 + 2*mm, y - 2*mm, label)
        c.acroForm.textfield(name, x=W - 50*mm, y=y - 4.5*mm,
                             width=34*mm, height=4.5*mm,
                             fontSize=8, fontName="Helvetica",
                             fillColor=white, borderColor=BORDER)
        c.setStrokeColor(BORDER)
        c.setLineWidth(0.3)
        c.line(x1, y - 5.5*mm, W - 14*mm, y - 5.5*mm)
        y -= 6.5*mm

    c.setFillColor(SURFACE)
    c.roundRect(x1, y - 7*mm, W - 28*mm, 7*mm, 1.5*mm, fill=1, stroke=0)
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x1 + 3*mm, y - 4.5*mm, "Sous-total Développement")
    c.acroForm.textfield("dev_total", x=W - 50*mm, y=y - 6.5*mm,
                         width=34*mm, height=5*mm,
                         fontSize=9, fontName="Helvetica-Bold",
                         fillColor=white, borderColor=BORDER)
    y -= 11*mm

    c.showPage()

    # ── PAGE 2 ──
    page_bg()
    draw_header(c, "Devis — FGS Studio (suite)", "Page 2 / 3")
    draw_footer(c, 2, 3)

    y = H - 35*mm
    x1, x2, cw = two_col(W)

    # Poste 3 — Recette (inclus)
    c.setFillColor(TEAL)
    c.roundRect(x1, y - 5*mm, W - 24*mm, 6*mm, 1.5*mm, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(x1 + 3*mm, y - 2.5*mm, "POSTE 3 — RECETTE & LIVRAISON")
    c.setFont("Helvetica", 7)
    c.setFillColor(HexColor('#a0d8d3'))
    c.drawRightString(W - 16*mm, y - 2.5*mm, "Inclus dans tous les projets")
    y -= 9*mm

    recette = [
        "Tests fonctionnels (mobile + desktop)",
        "Corrections issues recette (1 cycle inclus)",
        "Documentation utilisateur (1 page PDF)",
        "Vidéo de démonstration",
        "Remise des accès (credentials sécurisés)",
    ]
    for item in recette:
        c.setFillColor(TEAL)
        c.circle(x1 + 2*mm, y - 2*mm, 1*mm, fill=1, stroke=0)
        c.setFillColor(TEXT_SOFT)
        c.setFont("Helvetica", 7.5)
        c.drawString(x1 + 5*mm, y - 3*mm, item)
        c.setFillColor(TEXT_SOFT)
        c.setFont("Helvetica-Bold", 7.5)
        c.drawRightString(W - 16*mm, y - 3*mm, "✓ Inclus")
        y -= 5.5*mm

    y -= 3*mm
    divider(y)
    y -= 8*mm

    # Poste 4 — Maintenance
    c.setFillColor(GOLD)
    c.roundRect(x1, y - 5*mm, W - 24*mm, 6*mm, 1.5*mm, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(x1 + 3*mm, y - 2.5*mm, "POSTE 4 — MAINTENANCE  (optionnel · sans engagement)")
    y -= 9*mm

    maint = [
        ("maint_essentielle", "Formule Essentielle — sécurité + backup + 1h support / mois"),
        ("maint_active",      "Formule Active — Essentielle + jusqu'à 3h modifs / mois"),
    ]
    for name, label in maint:
        c.setFillColor(TEXT_SOFT)
        c.setFont("Helvetica", 7.5)
        c.drawString(x1 + 2*mm, y - 2*mm, label)
        c.acroForm.textfield(name, x=W - 50*mm, y=y - 4.5*mm,
                             width=34*mm, height=4.5*mm,
                             fontSize=8, fontName="Helvetica",
                             fillColor=GOLD_BG, borderColor=BORDER)
        c.setStrokeColor(BORDER)
        c.setLineWidth(0.3)
        c.line(x1, y - 5.5*mm, W - 14*mm, y - 5.5*mm)
        y -= 6.5*mm

    y -= 4*mm

    # Poste 5 — Formation
    c.setFillColor(NAVY_MID)
    c.roundRect(x1, y - 5*mm, W - 24*mm, 6*mm, 1.5*mm, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(x1 + 3*mm, y - 2.5*mm, "POSTE 5 — FORMATION  (optionnel)")
    y -= 9*mm

    form_items = [
        ("form_prise_main", "Session prise en main — 1h (visio ou présentiel)"),
        ("form_avancee",    "Session avancée — 2h (gestion, paramétrage)"),
    ]
    for name, label in form_items:
        c.setFillColor(TEXT_SOFT)
        c.setFont("Helvetica", 7.5)
        c.drawString(x1 + 2*mm, y - 2*mm, label)
        c.acroForm.textfield(name, x=W - 50*mm, y=y - 4.5*mm,
                             width=34*mm, height=4.5*mm,
                             fontSize=8, fontName="Helvetica",
                             fillColor=white, borderColor=BORDER)
        c.setStrokeColor(BORDER)
        c.setLineWidth(0.3)
        c.line(x1, y - 5.5*mm, W - 14*mm, y - 5.5*mm)
        y -= 6.5*mm

    y -= 4*mm
    divider(y, NAVY)
    y -= 8*mm

    # Récap financier
    c.setFillColor(NAVY)
    c.roundRect(x1, y - 5*mm, W - 24*mm, 6*mm, 2*mm, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(x1 + 3*mm, y - 2.5*mm, "RÉCAPITULATIF FINANCIER")
    y -= 9*mm

    recap = [
        ("recap_setup",  "Setup & infrastructure"),
        ("recap_dev",    "Développement"),
        ("recap_maint",  "Maintenance / mois (si retenue)"),
        ("recap_form",   "Formation (si retenue)"),
    ]
    for name, label in recap:
        c.setFillColor(TEXT)
        c.setFont("Helvetica", 8)
        c.drawString(x1 + 2*mm, y - 2.5*mm, label)
        c.acroForm.textfield(name, x=W - 50*mm, y=y - 5*mm,
                             width=34*mm, height=5*mm,
                             fontSize=8, fontName="Helvetica",
                             fillColor=white, borderColor=BORDER)
        c.setStrokeColor(BORDER)
        c.setLineWidth(0.3)
        c.line(x1, y - 5.5*mm, W - 14*mm, y - 5.5*mm)
        y -= 7*mm

    # TOTAL
    c.setFillColor(NAVY)
    c.roundRect(x1, y - 9*mm, W - 28*mm, 9*mm, 1.5*mm, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(x1 + 3*mm, y - 5.5*mm, "TOTAL")
    c.acroForm.textfield("total", x=W - 54*mm, y=y - 8*mm,
                         width=38*mm, height=7*mm,
                         fontSize=11, fontName="Helvetica-Bold",
                         fillColor=NAVY, borderColor=None, textColor=white)
    y -= 14*mm

    # Modalités paiement
    c.setFillColor(TEAL_LT)
    c.roundRect(x1, y - 18*mm, W - 28*mm, 18*mm, 2*mm, fill=1, stroke=0)
    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x1 + 3*mm, y - 5*mm, "MODALITÉS DE PAIEMENT — 50 % / 50 %")

    c.setFillColor(TEXT_MID)
    c.setFont("Helvetica", 7.5)
    c.drawString(x1 + 3*mm, y - 9.5*mm, "Acompte 50 % à la signature → démarrage immédiat du projet")
    c.acroForm.textfield("acompte", x=W - 52*mm, y=y - 12*mm,
                         width=36*mm, height=5*mm,
                         fontSize=9, fontName="Helvetica-Bold",
                         fillColor=white, borderColor=BORDER)

    c.drawString(x1 + 3*mm, y - 15*mm, "Solde 50 % à la livraison → avant remise des accès")
    c.acroForm.textfield("solde", x=W - 52*mm, y=y - 18*mm,
                         width=36*mm, height=5*mm,
                         fontSize=9, fontName="Helvetica-Bold",
                         fillColor=white, borderColor=BORDER)
    y -= 22*mm

    c.showPage()

    # ── PAGE 3 — Conditions & Signature ──
    page_bg()
    draw_header(c, "Devis — FGS Studio (conditions)", "Page 3 / 3")
    draw_footer(c, 3, 3)

    y = H - 35*mm
    x1, x2, cw = two_col(W)

    # Révisions
    y = section_title(c, y, "·", "Révisions incluses", color=TEAL)

    revisions = [
        ("Maquettes / design",        "2 cycles inclus — au-delà : taux horaire"),
        ("Bugs / corrections de code","Illimitées — un bug est un défaut du code, pas un changement"),
        ("Modifications fonctionnelles","1 cycle post-recette — au-delà : avenant chiffré"),
    ]
    for label, detail in revisions:
        c.setFillColor(TEAL)
        c.circle(x1 + 2*mm, y - 2.5*mm, 1*mm, fill=1, stroke=0)
        c.setFillColor(TEXT)
        c.setFont("Helvetica-Bold", 8)
        c.drawString(x1 + 5*mm, y - 3*mm, label)
        c.setFillColor(TEXT_SOFT)
        c.setFont("Helvetica", 7.5)
        c.drawString(x1 + 5*mm, y - 7*mm, detail)
        y -= 10*mm

    y -= 2*mm

    # Engagements
    y = section_title(c, y, "·", "Engagements mutuels", color=NAVY_MID)

    c.setFillColor(TEXT_MID)
    c.setFont("Helvetica-Bold", 7.5)
    c.drawString(x1, y, "FGS s'engage à :")
    y -= 5*mm
    fgs_eng = [
        "Livrer un outil fonctionnel conforme au brief validé",
        "Remettre un code propre, documenté, sans dépendance cachée",
        "Répondre aux messages WhatsApp sous 24h (jours ouvrés)",
        "Ne jamais sous-traiter sans accord préalable du client",
    ]
    for item in fgs_eng:
        c.setFillColor(NAVY)
        c.circle(x1 + 2*mm, y - 1.5*mm, 0.8*mm, fill=1, stroke=0)
        c.setFillColor(TEXT_SOFT)
        c.setFont("Helvetica", 7.5)
        c.drawString(x1 + 5*mm, y - 3*mm, item)
        y -= 5.5*mm

    y -= 2*mm
    c.setFillColor(TEXT_MID)
    c.setFont("Helvetica-Bold", 7.5)
    c.drawString(x1, y, "Le client s'engage à :")
    y -= 5*mm
    client_eng = [
        "Fournir les contenus (logos, photos, textes) dans les délais convenus",
        "Valider les maquettes avant le démarrage du développement",
        "Désigner une seule personne référente pour les retours",
        "Régler chaque échéance dans les délais prévus",
    ]
    for item in client_eng:
        c.setFillColor(TEAL)
        c.circle(x1 + 2*mm, y - 1.5*mm, 0.8*mm, fill=1, stroke=0)
        c.setFillColor(TEXT_SOFT)
        c.setFont("Helvetica", 7.5)
        c.drawString(x1 + 5*mm, y - 3*mm, item)
        y -= 5.5*mm

    y -= 4*mm

    # Conditions générales
    y = section_title(c, y, "·", "Conditions générales", color=NAVY)

    cg = [
        "Devis valable 30 jours à compter de la date d'émission.",
        "Le démarrage est conditionné à la réception de l'acompte de 50 %.",
        "Toute demande hors périmètre initial fait l'objet d'un avenant chiffré.",
        "Propriété intellectuelle : le code appartient intégralement au client après paiement du solde.",
        "Confidentialité : FGS s'engage à ne pas divulguer les données du projet à des tiers.",
        "FGS peut mentionner le projet dans son portfolio sauf refus explicite ci-dessous.",
    ]
    for item in cg:
        c.setFillColor(NAVY)
        c.circle(x1 + 2*mm, y - 1.5*mm, 0.8*mm, fill=1, stroke=0)
        c.setFillColor(TEXT_SOFT)
        c.setFont("Helvetica", 7.5)
        c.drawString(x1 + 5*mm, y - 3*mm, item)
        y -= 5.5*mm

    y -= 1*mm
    c.acroForm.checkbox("refus_portfolio", x=x1 + 5*mm, y=y - 4*mm,
                        size=3.5*mm, fillColor=white, borderColor=BORDER, forceBorder=True)
    c.setFillColor(TEXT_MID)
    c.setFont("Helvetica-Oblique", 7.5)
    c.drawString(x1 + 10*mm, y - 3*mm, "Je refuse que FGS mentionne ce projet dans son portfolio.")
    y -= 8*mm

    divider(y, NAVY)
    y -= 8*mm

    # Signature
    c.setFillColor(NAVY)
    c.roundRect(x1, y - 5*mm, W - 24*mm, 6*mm, 2*mm, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(x1 + 3*mm, y - 2.5*mm, "SIGNATURE — BON POUR ACCORD")
    y -= 10*mm

    sign_w = (W - 28*mm - 8*mm) / 2

    for col, label, name_date, name_sign in [
        (x1, "FGS — Eddy Takougang", "sign_fgs_date", "sign_fgs"),
        (x2, "Client", "sign_client_date", "sign_client"),
    ]:
        c.setFillColor(SURFACE)
        c.roundRect(col, y - 28*mm, sign_w, 28*mm, 2*mm, fill=1, stroke=0)
        c.setFillColor(NAVY)
        c.setFont("Helvetica-Bold", 8)
        c.drawString(col + 3*mm, y - 5*mm, label)
        c.setFillColor(TEXT_SOFT)
        c.setFont("Helvetica", 7)
        c.drawString(col + 3*mm, y - 9*mm, "Date :")
        c.acroForm.textfield(name_date, x=col + 14*mm, y=y - 12*mm,
                             width=sign_w - 16*mm, height=5*mm,
                             fontSize=8, fontName="Helvetica",
                             fillColor=white, borderColor=BORDER)
        c.setFillColor(TEXT_SOFT)
        c.setFont("Helvetica", 7)
        c.drawString(col + 3*mm, y - 16*mm, "Signature :")
        c.setFillColor(white)
        c.setStrokeColor(BORDER)
        c.roundRect(col + 3*mm, y - 28*mm, sign_w - 6*mm, 10*mm, 1.5*mm, fill=1, stroke=1)
        c.setFillColor(TEXT_SOFT)
        c.setFont("Helvetica-Oblique", 6.5)
        c.drawString(col + 3*mm + 2*mm, y - 25*mm, '"Bon pour accord"')

    c.save()
    print(f"OK: {path}")


if __name__ == "__main__":
    import os
    os.chdir(r"C:/Users/Utilisateur/Documents/_Fotsi/fotsi/studio/pdf")
    generate_brief()
    generate_devis()
    print("\nPDFs generes dans studio/pdf/")
