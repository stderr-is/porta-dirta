#!/usr/bin/env python3
"""Add data-i18n attributes to eventos.astro."""

with open('src/pages/eventos.astro', encoding='utf-8') as f:
    content = f.read()

replacements = [
    # Hero label
    (
        '        EVENTOS &amp; CELEBRACIONES\n      </p>',
        '        EVENTOS &amp; CELEBRACIONES\n      </p>',
    ),
    # Hero label - add data-i18n
    (
        '<p class="font-body uppercase tracking-[0.3em] text-brand-gold text-sm font-medium">\n        EVENTOS &amp; CELEBRACIONES\n      </p>',
        '<p class="font-body uppercase tracking-[0.3em] text-brand-gold text-sm font-medium" data-i18n="eventos.hero_label">\n        EVENTOS &amp; CELEBRACIONES\n      </p>',
    ),
    # Hero heading
    (
        '<h1 class="font-display italic text-4xl sm:text-5xl md:text-6xl lg:text-7xl text-white leading-tight">\n        Momentos que duran para siempre\n      </h1>',
        '<h1 class="font-display italic text-4xl sm:text-5xl md:text-6xl lg:text-7xl text-white leading-tight" data-i18n="eventos.hero_heading">\n        Momentos que duran para siempre\n      </h1>',
    ),
    # Hero pills
    (
        'text-white font-body text-sm px-5 py-2 rounded-full">\n          Bodas\n        </span>',
        'text-white font-body text-sm px-5 py-2 rounded-full" data-i18n="eventos.hero_pill_bodas">\n          Bodas\n        </span>',
    ),
    (
        'text-white font-body text-sm px-5 py-2 rounded-full">\n          Comuniones\n        </span>',
        'text-white font-body text-sm px-5 py-2 rounded-full" data-i18n="eventos.hero_pill_comuniones">\n          Comuniones\n        </span>',
    ),
    (
        'text-white font-body text-sm px-5 py-2 rounded-full">\n          Cumpleaños\n        </span>',
        'text-white font-body text-sm px-5 py-2 rounded-full" data-i18n="eventos.hero_pill_cumpleanos">\n          Cumpleaños\n        </span>',
    ),
    # Hero CTA
    (
        'aria-label="Descubrir el espacio"\n      >\n        Descubrir el espacio',
        'aria-label="Descubrir el espacio"\n        data-i18n="eventos.hero_cta"\n      >\n        Descubrir el espacio',
    ),
    # Venue label
    (
        '<p class="font-body uppercase tracking-[0.3em] text-brand-gold text-xs font-medium">\n            EL ESPACIO\n          </p>',
        '<p class="font-body uppercase tracking-[0.3em] text-brand-gold text-xs font-medium" data-i18n="eventos.venue_label">\n            EL ESPACIO\n          </p>',
    ),
    # Venue heading
    (
        '<h2 class="font-display font-light text-3xl sm:text-4xl md:text-5xl text-brand-blue leading-tight">\n            Un entorno único\n          </h2>',
        '<h2 class="font-display font-light text-3xl sm:text-4xl md:text-5xl text-brand-blue leading-tight" data-i18n="eventos.venue_heading">\n            Un entorno único\n          </h2>',
    ),
    # Feature labels and values
    (
        '<p class="font-body text-xs uppercase tracking-widest text-brand-stone font-medium">Capacidad</p>',
        '<p class="font-body text-xs uppercase tracking-widest text-brand-stone font-medium" data-i18n="eventos.feature_capacity_label">Capacidad</p>',
    ),
    (
        '<p class="font-display text-2xl text-brand-blue font-light">Hasta 120 invitados</p>',
        '<p class="font-display text-2xl text-brand-blue font-light" data-i18n="eventos.feature_capacity_value">Hasta 120 invitados</p>',
    ),
    (
        '<p class="font-body text-xs uppercase tracking-widest text-brand-stone font-medium">Exterior</p>',
        '<p class="font-body text-xs uppercase tracking-widest text-brand-stone font-medium" data-i18n="eventos.feature_outdoor_label">Exterior</p>',
    ),
    (
        '<p class="font-display text-2xl text-brand-blue font-light">Jardín y terraza</p>',
        '<p class="font-display text-2xl text-brand-blue font-light" data-i18n="eventos.feature_outdoor_value">Jardín y terraza</p>',
    ),
    (
        '<p class="font-body text-xs uppercase tracking-widest text-brand-stone font-medium">Deportes</p>',
        '<p class="font-body text-xs uppercase tracking-widest text-brand-stone font-medium" data-i18n="eventos.feature_sports_label">Deportes</p>',
    ),
    (
        '<p class="font-display text-2xl text-brand-blue font-light">Pista de tenis</p>',
        '<p class="font-display text-2xl text-brand-blue font-light" data-i18n="eventos.feature_sports_value">Pista de tenis</p>',
    ),
    (
        '<p class="font-body text-xs uppercase tracking-widest text-brand-stone font-medium">Gastronomía</p>',
        '<p class="font-body text-xs uppercase tracking-widest text-brand-stone font-medium" data-i18n="eventos.feature_catering_label">Gastronomía</p>',
    ),
    (
        '<p class="font-display text-2xl text-brand-blue font-light">Restaurante propio</p>',
        '<p class="font-display text-2xl text-brand-blue font-light" data-i18n="eventos.feature_catering_value">Restaurante propio</p>',
    ),
    # Event types section label
    (
        '<p class="font-body uppercase tracking-[0.3em] text-brand-gold text-xs font-medium mb-4">\n          CELEBRACIONES\n        </p>',
        '<p class="font-body uppercase tracking-[0.3em] text-brand-gold text-xs font-medium mb-4" data-i18n="eventos.types_label">\n          CELEBRACIONES\n        </p>',
    ),
    # Event types heading
    (
        '<h2 class="font-display font-light italic text-3xl sm:text-4xl md:text-5xl text-white">\n          ¿Qué estás celebrando?\n        </h2>',
        '<h2 class="font-display font-light italic text-3xl sm:text-4xl md:text-5xl text-white" data-i18n="eventos.types_heading">\n          ¿Qué estás celebrando?\n        </h2>',
    ),
    # Bodas card
    (
        '<h3 class="font-display text-3xl text-white font-light">Bodas</h3>',
        '<h3 class="font-display text-3xl text-white font-light" data-i18n="eventos.type_bodas_heading">Bodas</h3>',
    ),
    # Comuniones card
    (
        '<h3 class="font-display text-3xl text-white font-light">Comuniones</h3>',
        '<h3 class="font-display text-3xl text-white font-light" data-i18n="eventos.type_comuniones_heading">Comuniones</h3>',
    ),
    # Eventos Privados card
    (
        '<h3 class="font-display text-3xl text-white font-light">Eventos Privados</h3>',
        '<h3 class="font-display text-3xl text-white font-light" data-i18n="eventos.type_private_heading">Eventos Privados</h3>',
    ),
    # Upcoming section label
    (
        '<p class="font-body uppercase tracking-[0.3em] text-brand-gold text-xs font-medium mb-4">\n            AGENDA\n          </p>',
        '<p class="font-body uppercase tracking-[0.3em] text-brand-gold text-xs font-medium mb-4" data-i18n="eventos.upcoming_label">\n            AGENDA\n          </p>',
    ),
    # Upcoming heading
    (
        '<h2 class="font-display font-light text-3xl sm:text-4xl md:text-5xl text-brand-blue">\n            Próximos Eventos en Porta D\'irta\n          </h2>',
        '<h2 class="font-display font-light text-3xl sm:text-4xl md:text-5xl text-brand-blue" data-i18n="eventos.upcoming_heading">\n            Próximos Eventos en Porta D\'irta\n          </h2>',
    ),
    # Upcoming free entry
    (
        '<span class="font-body text-sm text-brand-stone italic">Entrada libre</span>',
        '<span class="font-body text-sm text-brand-stone italic" data-i18n="eventos.upcoming_free">Entrada libre</span>',
    ),
    # Upcoming buy tickets
    (
        '              Comprar Entradas\n              <svg',
        '              <span data-i18n="eventos.upcoming_buy_tickets">Comprar Entradas</span>\n              <svg',
    ),
    # Upcoming more info
    (
        '              Más información\n              <svg xmlns="http://www.w3.org/2000/svg" width="14"',
        '              <span data-i18n="eventos.upcoming_more_info">Más información</span>\n              <svg xmlns="http://www.w3.org/2000/svg" width="14"',
    ),
    # Form section label
    (
        '<p class="font-body uppercase tracking-[0.3em] text-brand-gold text-xs font-medium mb-4">\n          CONTACTO\n        </p>',
        '<p class="font-body uppercase tracking-[0.3em] text-brand-gold text-xs font-medium mb-4" data-i18n="eventos.form_label">\n          CONTACTO\n        </p>',
    ),
    # Form heading
    (
        '<h2 class="font-display font-light italic text-3xl sm:text-4xl md:text-5xl text-white leading-tight">\n          Cuéntanos tu evento\n        </h2>',
        '<h2 class="font-display font-light italic text-3xl sm:text-4xl md:text-5xl text-white leading-tight" data-i18n="eventos.form_heading">\n          Cuéntanos tu evento\n        </h2>',
    ),
    # Form body
    (
        '<p class="font-body text-white/60 text-base mt-4 leading-relaxed">\n          Rellena el formulario y nuestro equipo te contactará para diseñar juntos la celebración perfecta.\n        </p>',
        '<p class="font-body text-white/60 text-base mt-4 leading-relaxed" data-i18n="eventos.form_body">\n          Rellena el formulario y nuestro equipo te contactará para diseñar juntos la celebración perfecta.\n        </p>',
    ),
    # Form labels
    (
        'for="nombre" class="font-body text-xs uppercase tracking-widest text-white/70 font-medium">\n                Nombre *\n              </label>',
        'for="nombre" class="font-body text-xs uppercase tracking-widest text-white/70 font-medium" data-i18n="eventos.form_name_label">\n                Nombre *\n              </label>',
    ),
    (
        'for="email" class="font-body text-xs uppercase tracking-widest text-white/70 font-medium">\n                Email *\n              </label>',
        'for="email" class="font-body text-xs uppercase tracking-widest text-white/70 font-medium" data-i18n="eventos.form_email_label">\n                Email *\n              </label>',
    ),
    (
        'for="telefono" class="font-body text-xs uppercase tracking-widest text-white/70 font-medium">\n                Teléfono\n              </label>',
        'for="telefono" class="font-body text-xs uppercase tracking-widest text-white/70 font-medium" data-i18n="eventos.form_phone_label">\n                Teléfono\n              </label>',
    ),
    (
        'for="tipo-evento" class="font-body text-xs uppercase tracking-widest text-white/70 font-medium">\n                Tipo de evento *\n              </label>',
        'for="tipo-evento" class="font-body text-xs uppercase tracking-widest text-white/70 font-medium" data-i18n="eventos.form_type_label">\n                Tipo de evento *\n              </label>',
    ),
    # Select options
    (
        '<option value="" disabled selected class="text-brand-blue">Selecciona una opción</option>',
        '<option value="" disabled selected class="text-brand-blue" data-i18n="eventos.form_type_select">Selecciona una opción</option>',
    ),
    (
        '<option value="boda" class="text-brand-blue">Boda</option>',
        '<option value="boda" class="text-brand-blue" data-i18n="eventos.form_type_boda">Boda</option>',
    ),
    (
        '<option value="comunion" class="text-brand-blue">Comunión</option>',
        '<option value="comunion" class="text-brand-blue" data-i18n="eventos.form_type_comunion">Comunión</option>',
    ),
    (
        '<option value="cumpleanos" class="text-brand-blue">Cumpleaños</option>',
        '<option value="cumpleanos" class="text-brand-blue" data-i18n="eventos.form_type_cumpleanos">Cumpleaños</option>',
    ),
    (
        '<option value="corporativo" class="text-brand-blue">Evento corporativo</option>',
        '<option value="corporativo" class="text-brand-blue" data-i18n="eventos.form_type_corporativo">Evento corporativo</option>',
    ),
    (
        '<option value="otro" class="text-brand-blue">Otro</option>\n              </select>',
        '<option value="otro" class="text-brand-blue" data-i18n="eventos.form_type_otro">Otro</option>\n              </select>',
    ),
    # Date and guests labels
    (
        'for="fecha" class="font-body text-xs uppercase tracking-widest text-white/70 font-medium">\n                Fecha aproximada\n              </label>',
        'for="fecha" class="font-body text-xs uppercase tracking-widest text-white/70 font-medium" data-i18n="eventos.form_date_label">\n                Fecha aproximada\n              </label>',
    ),
    (
        'for="invitados" class="font-body text-xs uppercase tracking-widest text-white/70 font-medium">\n                Número de invitados\n              </label>',
        'for="invitados" class="font-body text-xs uppercase tracking-widest text-white/70 font-medium" data-i18n="eventos.form_guests_label">\n                Número de invitados\n              </label>',
    ),
    # Message label
    (
        'for="mensaje" class="font-body text-xs uppercase tracking-widest text-white/70 font-medium">\n              Mensaje\n            </label>',
        'for="mensaje" class="font-body text-xs uppercase tracking-widest text-white/70 font-medium" data-i18n="eventos.form_message_label">\n              Mensaje\n            </label>',
    ),
    # Submit button
    (
        '              Enviar Consulta\n            </button>',
        '              <span data-i18n="eventos.form_submit">Enviar Consulta</span>\n            </button>',
    ),
    # Response time
    (
        '<p class="font-body text-white/50 text-xs text-center">\n              Respondemos en menos de 48 horas &middot; info@portadirta.com\n            </p>',
        '<p class="font-body text-white/50 text-xs text-center" data-i18n="eventos.form_response_time">\n              Respondemos en menos de 48 horas &middot; info@portadirta.com\n            </p>',
    ),
    # Crosssell label
    (
        '<p class="font-body text-center uppercase tracking-[0.3em] text-brand-stone text-xs font-medium mb-12">\n        DESCUBRE MÁS\n      </p>',
        '<p class="font-body text-center uppercase tracking-[0.3em] text-brand-stone text-xs font-medium mb-12" data-i18n="eventos.crosssell_label">\n        DESCUBRE MÁS\n      </p>',
    ),
    # Crosssell links (eventos.astro has Hotel, Restaurante, Experiencias)
    (
        'class="font-display text-2xl text-brand-blue font-light group-hover:text-brand-gold transition-colors duration-300">\n            El Hotel\n          </span>',
        'class="font-display text-2xl text-brand-blue font-light group-hover:text-brand-gold transition-colors duration-300" data-i18n="eventos.crosssell_hotel">\n            El Hotel\n          </span>',
    ),
    (
        'class="font-display text-2xl text-brand-blue font-light group-hover:text-brand-gold transition-colors duration-300">\n            El Restaurante\n          </span>',
        'class="font-display text-2xl text-brand-blue font-light group-hover:text-brand-gold transition-colors duration-300" data-i18n="eventos.crosssell_restaurante">\n            El Restaurante\n          </span>',
    ),
    (
        'class="font-display text-2xl text-brand-blue font-light group-hover:text-brand-gold transition-colors duration-300">\n            Experiencias\n          </span>',
        'class="font-display text-2xl text-brand-blue font-light group-hover:text-brand-gold transition-colors duration-300" data-i18n="eventos.crosssell_experiencias">\n            Experiencias\n          </span>',
    ),
]

for old, new in replacements:
    if old in content:
        content = content.replace(old, new, 1)
    else:
        print(f"WARNING: not found: {old[:80]!r}")

with open('src/pages/eventos.astro', 'w', encoding='utf-8') as f:
    f.write(content)

print("eventos.astro annotated.")
