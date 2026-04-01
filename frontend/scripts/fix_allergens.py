#!/usr/bin/env python3

with open('src/pages/restaurante.astro', encoding='utf-8') as f:
    content = f.read()

class_attr = 'class="text-[7px] uppercase tracking-wider text-brand-stone/40 border border-brand-stone/10 px-1 py-0.5 rounded-sm"'
class_attr2 = 'class="text-[7px] uppercase tracking-wider text-brand-stone/40 border border-brand-stone/10 px-1.5 py-0.5 rounded-sm"'

allergens = {
    'Gluten': 'restaurante.allergen_gluten',
    'Lácteos': 'restaurante.allergen_lacteos',
    'Sulfitos': 'restaurante.allergen_sulfitos',
    'Moluscos': 'restaurante.allergen_moluscos',
    'Crustáceos': 'restaurante.allergen_crustaceos',
    'Pescado': 'restaurante.allergen_pescado',
}

for text, key in allergens.items():
    for cls in [class_attr, class_attr2]:
        old = f'<span {cls}>{text}</span>'
        new = f'<span {cls} data-i18n="{key}">{text}</span>'
        content = content.replace(old, new)

with open('src/pages/restaurante.astro', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done")
