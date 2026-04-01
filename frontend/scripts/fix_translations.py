#!/usr/bin/env python3
import sys

with open('src/i18n/translations.ts', encoding='utf-8') as f:
    content = f.read()

original = content

# ── 1a. Contacto form option keys ──────────────────────────────

# ES
old = '      form_submit_button: "Enviar Mensaje",\n    },\n    footer: {'
new = ('      form_submit_button: "Enviar Mensaje",\n'
       '      form_option_mesa: "Reserva de mesa",\n'
       '      form_option_alergenos: "Alérgenos e intolerancias",\n'
       '      form_option_eventos: "Eventos y celebraciones",\n'
       '      form_option_grupos: "Grupos y catering",\n'
       '      form_option_otro: "Otro",\n'
       '      form_success_heading: "¡Mensaje enviado!",\n'
       '      form_success_body: "Gracias por ponerte en contacto con nosotros. Te responderemos en menos de 48 horas.",\n'
       '    },\n    footer: {')
assert content.count(old) == 1, f"ES contacto: found {content.count(old)} occurrences"
content = content.replace(old, new, 1)

# EN
old = '      form_submit_button: "Send Message",\n    },\n    footer: {'
new = ('      form_submit_button: "Send Message",\n'
       '      form_option_mesa: "Table reservation",\n'
       '      form_option_alergenos: "Allergens and intolerances",\n'
       '      form_option_eventos: "Events and celebrations",\n'
       '      form_option_grupos: "Groups and catering",\n'
       '      form_option_otro: "Other",\n'
       '      form_success_heading: "Message sent!",\n'
       '      form_success_body: "Thank you for contacting us. We will respond within 48 hours.",\n'
       '    },\n    footer: {')
assert content.count(old) == 1, f"EN contacto: found {content.count(old)} occurrences"
content = content.replace(old, new, 1)

# FR
old = '      form_submit_button: "Envoyer le Message",\n    },\n    footer: {'
new = ('      form_submit_button: "Envoyer le Message",\n'
       '      form_option_mesa: "Réservation de table",\n'
       '      form_option_alergenos: "Allergènes et intolérances",\n'
       '      form_option_eventos: "Événements et célébrations",\n'
       '      form_option_grupos: "Groupes et traiteur",\n'
       '      form_option_otro: "Autre",\n'
       '      form_success_heading: "Message envoyé !",\n'
       '      form_success_body: "Merci de nous avoir contactés. Nous répondrons dans les 48 heures.",\n'
       '    },\n    footer: {')
assert content.count(old) == 1, f"FR contacto: found {content.count(old)} occurrences"
content = content.replace(old, new, 1)

# DE
old = '      form_submit_button: "Nachricht senden",\n    },\n    footer: {'
new = ('      form_submit_button: "Nachricht senden",\n'
       '      form_option_mesa: "Tischreservierung",\n'
       '      form_option_alergenos: "Allergene und Unverträglichkeiten",\n'
       '      form_option_eventos: "Veranstaltungen und Feiern",\n'
       '      form_option_grupos: "Gruppen und Catering",\n'
       '      form_option_otro: "Sonstiges",\n'
       '      form_success_heading: "Nachricht gesendet!",\n'
       '      form_success_body: "Danke für Ihre Kontaktaufnahme. Wir antworten innerhalb von 48 Stunden.",\n'
       '    },\n    footer: {')
assert content.count(old) == 1, f"DE contacto: found {content.count(old)} occurrences"
content = content.replace(old, new, 1)

# ── 1b. loading_text in reservar ────────────────────────────────

# ES
old = '      modify_button: "Modificar",\n      loading_availability: "Cargando disponibilidad...",'
new = ('      modify_button: "Modificar",\n'
       '      loading_text: "Cargando disponibilidad…",\n'
       '      loading_availability: "Cargando disponibilidad...",')
assert content.count(old) == 1, f"ES reservar loading: found {content.count(old)} occurrences"
content = content.replace(old, new, 1)

# EN
old = '      modify_button: "Modify",\n      loading_availability: "Loading availability...",'
new = ('      modify_button: "Modify",\n'
       '      loading_text: "Loading availability…",\n'
       '      loading_availability: "Loading availability...",')
assert content.count(old) == 1, f"EN reservar loading: found {content.count(old)} occurrences"
content = content.replace(old, new, 1)

# FR
old = '      modify_button: "Modifier",\n      loading_availability: "Chargement de la disponibilité...",'
new = ('      modify_button: "Modifier",\n'
       '      loading_text: "Chargement de la disponibilité…",\n'
       '      loading_availability: "Chargement de la disponibilité...",')
assert content.count(old) == 1, f"FR reservar loading: found {content.count(old)} occurrences"
content = content.replace(old, new, 1)

# DE
old = '      modify_button: "Ändern",\n      loading_availability: "Verfügbarkeit wird geladen...",'
new = ('      modify_button: "Ändern",\n'
       '      loading_text: "Verfügbarkeit wird geladen…",\n'
       '      loading_availability: "Verfügbarkeit wird geladen...",')
assert content.count(old) == 1, f"DE reservar loading: found {content.count(old)} occurrences"
content = content.replace(old, new, 1)

# ── 1c. Allergen keys in restaurante ────────────────────────────

allergen_es = ('      allergen_gluten: "Gluten",\n'
               '      allergen_lacteos: "Lácteos",\n'
               '      allergen_sulfitos: "Sulfitos",\n'
               '      allergen_moluscos: "Moluscos",\n'
               '      allergen_crustaceos: "Crustáceos",\n'
               '      allergen_pescado: "Pescado",\n')
allergen_en = ('      allergen_gluten: "Gluten",\n'
               '      allergen_lacteos: "Dairy",\n'
               '      allergen_sulfitos: "Sulphites",\n'
               '      allergen_moluscos: "Molluscs",\n'
               '      allergen_crustaceos: "Crustaceans",\n'
               '      allergen_pescado: "Fish",\n')
allergen_fr = ('      allergen_gluten: "Gluten",\n'
               '      allergen_lacteos: "Produits laitiers",\n'
               '      allergen_sulfitos: "Sulfites",\n'
               '      allergen_moluscos: "Mollusques",\n'
               '      allergen_crustaceos: "Crustacés",\n'
               '      allergen_pescado: "Poisson",\n')
allergen_de = ('      allergen_gluten: "Gluten",\n'
               '      allergen_lacteos: "Milchprodukte",\n'
               '      allergen_sulfitos: "Sulfite",\n'
               '      allergen_moluscos: "Weichtiere",\n'
               '      allergen_crustaceos: "Krustentiere",\n'
               '      allergen_pescado: "Fisch",\n')

# ES: og_image -> reservar (meta_title: "Reservar")
old = ('      og_image: "/assets/images/food-paella-wine.jpg",\n'
       '    },\n'
       '    reservar: {\n'
       '      meta_title: "Reservar — Habitación o Mesa",')
new = ('      og_image: "/assets/images/food-paella-wine.jpg",\n'
       + allergen_es +
       '    },\n'
       '    reservar: {\n'
       '      meta_title: "Reservar — Habitación o Mesa",')
assert content.count(old) == 1, f"ES restaurante allergen: found {content.count(old)} occurrences"
content = content.replace(old, new, 1)

# EN: og_image -> reservar (meta_title: "Book")
old = ('      og_image: "/assets/images/food-paella-wine.jpg",\n'
       '    },\n'
       '    reservar: {\n'
       '      meta_title: "Book — Room or Table",')
new = ('      og_image: "/assets/images/food-paella-wine.jpg",\n'
       + allergen_en +
       '    },\n'
       '    reservar: {\n'
       '      meta_title: "Book — Room or Table",')
assert content.count(old) == 1, f"EN restaurante allergen: found {content.count(old)} occurrences"
content = content.replace(old, new, 1)

# FR: og_image -> reservar (meta_title: "Réserver")
old = ('      og_image: "/assets/images/food-paella-wine.jpg",\n'
       '    },\n'
       '    reservar: {\n'
       '      meta_title: "Réserver — Chambre ou Table",')
new = ('      og_image: "/assets/images/food-paella-wine.jpg",\n'
       + allergen_fr +
       '    },\n'
       '    reservar: {\n'
       '      meta_title: "Réserver — Chambre ou Table",')
assert content.count(old) == 1, f"FR restaurante allergen: found {content.count(old)} occurrences"
content = content.replace(old, new, 1)

# DE: og_image -> reservar (meta_title: "Buchen")
old = ('      og_image: "/assets/images/food-paella-wine.jpg",\n'
       '    },\n'
       '    reservar: {\n'
       '      meta_title: "Buchen — Zimmer oder Tisch",')
new = ('      og_image: "/assets/images/food-paella-wine.jpg",\n'
       + allergen_de +
       '    },\n'
       '    reservar: {\n'
       '      meta_title: "Buchen — Zimmer oder Tisch",')
assert content.count(old) == 1, f"DE restaurante allergen: found {content.count(old)} occurrences"
content = content.replace(old, new, 1)

with open('src/i18n/translations.ts', 'w', encoding='utf-8') as f:
    f.write(content)

print("All replacements applied successfully.")
