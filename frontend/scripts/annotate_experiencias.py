#!/usr/bin/env python3
"""Add data-i18n attributes to experiencias.astro."""

with open('src/pages/experiencias.astro', encoding='utf-8') as f:
    content = f.read()

replacements = [
    # Hero label
    (
        '<p class="font-body uppercase tracking-[0.3em] text-brand-gold text-sm font-medium">\n        EXPERIENCIAS\n      </p>',
        '<p class="font-body uppercase tracking-[0.3em] text-brand-gold text-sm font-medium" data-i18n="experiencias.hero_label">\n        EXPERIENCIAS\n      </p>',
    ),
    # Hero heading
    (
        '<h1 class="font-display italic text-4xl sm:text-5xl md:text-6xl lg:text-7xl text-white leading-tight">\n        Descubre la Costa del Azahar\n      </h1>',
        '<h1 class="font-display italic text-4xl sm:text-5xl md:text-6xl lg:text-7xl text-white leading-tight" data-i18n="experiencias.hero_heading">\n        Descubre la Costa del Azahar\n      </h1>',
    ),
    # Hero subtitle
    (
        '<p class="font-body text-white/80 text-lg leading-relaxed max-w-xl">\n        Excursiones, gastronomía y aventuras diseñadas para nuestros huéspedes\n      </p>',
        '<p class="font-body text-white/80 text-lg leading-relaxed max-w-xl" data-i18n="experiencias.hero_subtitle">\n        Excursiones, gastronomía y aventuras diseñadas para nuestros huéspedes\n      </p>',
    ),
    # Hero pills
    (
        'text-white font-body text-sm px-5 py-2 rounded-full">\n          Naturaleza\n        </span>',
        'text-white font-body text-sm px-5 py-2 rounded-full" data-i18n="experiencias.hero_pill_naturaleza">\n          Naturaleza\n        </span>',
    ),
    (
        'text-white font-body text-sm px-5 py-2 rounded-full">\n          Mar\n        </span>',
        'text-white font-body text-sm px-5 py-2 rounded-full" data-i18n="experiencias.hero_pill_mar">\n          Mar\n        </span>',
    ),
    (
        'text-white font-body text-sm px-5 py-2 rounded-full">\n          Cultura\n        </span>',
        'text-white font-body text-sm px-5 py-2 rounded-full" data-i18n="experiencias.hero_pill_cultura">\n          Cultura\n        </span>',
    ),
    (
        'text-white font-body text-sm px-5 py-2 rounded-full">\n          Gastronomía\n        </span>',
        'text-white font-body text-sm px-5 py-2 rounded-full" data-i18n="experiencias.hero_pill_gastronomia">\n          Gastronomía\n        </span>',
    ),
    # Hero CTA
    (
        'aria-label="Descubrir experiencias"\n      >\n        Descubrir experiencias',
        'aria-label="Descubrir experiencias"\n        data-i18n="experiencias.hero_cta"\n      >\n        Descubrir experiencias',
    ),
    # Intro label
    (
        '<p class="font-body uppercase tracking-[0.3em] text-brand-gold text-xs font-medium">\n            PARA NUESTROS HUÉSPEDES\n          </p>',
        '<p class="font-body uppercase tracking-[0.3em] text-brand-gold text-xs font-medium" data-i18n="experiencias.intro_label">\n            PARA NUESTROS HUÉSPEDES\n          </p>',
    ),
    # Intro heading
    (
        '<h2 class="font-display font-light text-3xl sm:text-4xl md:text-5xl text-brand-blue leading-tight">\n            Todo lo que Peñíscola tiene que ofrecerte\n          </h2>',
        '<h2 class="font-display font-light text-3xl sm:text-4xl md:text-5xl text-brand-blue leading-tight" data-i18n="experiencias.intro_heading">\n            Todo lo que Peñíscola tiene que ofrecerte\n          </h2>',
    ),
    # Packages section label
    (
        '<p class="font-body uppercase tracking-[0.3em] text-brand-gold text-xs font-medium">\n          RESERVA TU EXPERIENCIA\n        </p>',
        '<p class="font-body uppercase tracking-[0.3em] text-brand-gold text-xs font-medium" data-i18n="experiencias.packages_label">\n          RESERVA TU EXPERIENCIA\n        </p>',
    ),
    # Packages heading
    (
        '<h2 class="font-display font-light text-3xl sm:text-4xl md:text-5xl text-brand-blue leading-tight">\n          Nuestros Paquetes\n        </h2>',
        '<h2 class="font-display font-light text-3xl sm:text-4xl md:text-5xl text-brand-blue leading-tight" data-i18n="experiencias.packages_heading">\n          Nuestros Paquetes\n        </h2>',
    ),
    # Packages body
    (
        '<p class="font-body text-brand-stone text-lg leading-relaxed max-w-2xl">\n          Plazas limitadas. Reserva con antelación para garantizar tu experiencia.\n        </p>',
        '<p class="font-body text-brand-stone text-lg leading-relaxed max-w-2xl" data-i18n="experiencias.packages_body">\n          Plazas limitadas. Reserva con antelación para garantizar tu experiencia.\n        </p>',
    ),
    # Empty state
    (
        '<p class="font-display italic text-2xl text-brand-blue/60">\n            Próximamente nuevas experiencias\n          </p>',
        '<p class="font-display italic text-2xl text-brand-blue/60" data-i18n="experiencias.packages_empty">\n            Próximamente nuevas experiencias\n          </p>',
    ),
    # Sierra label
    (
        '<p class="font-body uppercase tracking-[0.3em] text-brand-gold text-xs font-medium">\n          NATURALEZA\n        </p>',
        '<p class="font-body uppercase tracking-[0.3em] text-brand-gold text-xs font-medium" data-i18n="experiencias.sierra_label">\n          NATURALEZA\n        </p>',
    ),
    # Sierra heading
    (
        '<h2 class="font-display italic text-4xl sm:text-5xl md:text-6xl text-white leading-tight">\n          Sierra de Irta\n        </h2>',
        '<h2 class="font-display italic text-4xl sm:text-5xl md:text-6xl text-white leading-tight" data-i18n="experiencias.sierra_heading">\n          Sierra de Irta\n        </h2>',
    ),
    # Sierra activities
    (
        '<span class="font-body text-white text-base">Senderismo guiado</span>',
        '<span class="font-body text-white text-base" data-i18n="experiencias.sierra_act1">Senderismo guiado</span>',
    ),
    (
        '<span class="font-body text-white text-base">Rutas en bicicleta</span>',
        '<span class="font-body text-white text-base" data-i18n="experiencias.sierra_act2">Rutas en bicicleta</span>',
    ),
    (
        '<span class="font-body text-white text-base">Observación de aves</span>',
        '<span class="font-body text-white text-base" data-i18n="experiencias.sierra_act3">Observación de aves</span>',
    ),
    (
        '<span class="font-body text-white text-base">Fotografía de naturaleza</span>',
        '<span class="font-body text-white text-base" data-i18n="experiencias.sierra_act4">Fotografía de naturaleza</span>',
    ),
    # Sierra CTA
    (
        'data-exp="sierra-irta"\n            class="exp-cta inline-flex items-center justify-center px-8 py-4 bg-brand-gold hover:bg-brand-stone text-brand-blue font-body text-sm uppercase tracking-widest font-medium rounded-lg transition-colors duration-300 shadow-lg"\n          >\n            Reservar Excursión',
        'data-exp="sierra-irta"\n            class="exp-cta inline-flex items-center justify-center px-8 py-4 bg-brand-gold hover:bg-brand-stone text-brand-blue font-body text-sm uppercase tracking-widest font-medium rounded-lg transition-colors duration-300 shadow-lg"\n            data-i18n="experiencias.sierra_cta"\n          >\n            Reservar Excursión',
    ),
    # Sea section label
    (
        '<p class="font-body uppercase tracking-[0.3em] text-brand-gold text-xs font-medium mb-4">\n          MAR &amp; PLAYA\n        </p>',
        '<p class="font-body uppercase tracking-[0.3em] text-brand-gold text-xs font-medium mb-4" data-i18n="experiencias.sea_label">\n          MAR &amp; PLAYA\n        </p>',
    ),
    # Sea heading
    (
        '<h2 class="font-display font-light text-3xl sm:text-4xl md:text-5xl text-brand-blue">\n          El Mediterráneo a tu puerta\n        </h2>',
        '<h2 class="font-display font-light text-3xl sm:text-4xl md:text-5xl text-brand-blue" data-i18n="experiencias.sea_heading">\n          El Mediterráneo a tu puerta\n        </h2>',
    ),
    # Cultura section label
    (
        '<p class="font-body uppercase tracking-[0.3em] text-brand-gold text-xs font-medium mb-4">\n          CULTURA &amp; GASTRONOMÍA\n        </p>',
        '<p class="font-body uppercase tracking-[0.3em] text-brand-gold text-xs font-medium mb-4" data-i18n="experiencias.cultura_label">\n          CULTURA &amp; GASTRONOMÍA\n        </p>',
    ),
    # Cultura heading
    (
        '<h2 class="font-display font-light italic text-3xl sm:text-4xl md:text-5xl text-white">\n          Peñíscola, historia y sabor\n        </h2>',
        '<h2 class="font-display font-light italic text-3xl sm:text-4xl md:text-5xl text-white" data-i18n="experiencias.cultura_heading">\n          Peñíscola, historia y sabor\n        </h2>',
    ),
    # Peñíscola Histórica card
    (
        '<h3 class="font-display text-3xl text-white font-light">Peñíscola Histórica</h3>',
        '<h3 class="font-display text-3xl text-white font-light" data-i18n="experiencias.cultura_peniscola_heading">Peñíscola Histórica</h3>',
    ),
    # Peñíscola CTA
    (
        'data-exp="cultura-historia"\n                class="exp-cta inline-flex items-center justify-center px-6 py-3 bg-brand-gold hover:bg-brand-stone text-brand-blue font-body text-sm uppercase tracking-widest font-medium rounded-lg transition-colors duration-300"\n              >\n                Explorar\n              </a>',
        'data-exp="cultura-historia"\n                class="exp-cta inline-flex items-center justify-center px-6 py-3 bg-brand-gold hover:bg-brand-stone text-brand-blue font-body text-sm uppercase tracking-widest font-medium rounded-lg transition-colors duration-300"\n                data-i18n="experiencias.cultura_peniscola_cta"\n              >\n                Explorar\n              </a>',
    ),
    # Vinos card
    (
        '<h3 class="font-display text-3xl text-white font-light">Cata de Vinos &amp; Gastronomía</h3>',
        '<h3 class="font-display text-3xl text-white font-light" data-i18n="experiencias.cultura_vinos_heading">Cata de Vinos &amp; Gastronomía</h3>',
    ),
    # Vinos CTA
    (
        'data-exp="gastronomia"\n                class="exp-cta inline-flex items-center justify-center px-6 py-3 bg-brand-gold hover:bg-brand-stone text-brand-blue font-body text-sm uppercase tracking-widest font-medium rounded-lg transition-colors duration-300"\n              >\n                Explorar\n              </a>',
        'data-exp="gastronomia"\n                class="exp-cta inline-flex items-center justify-center px-6 py-3 bg-brand-gold hover:bg-brand-stone text-brand-blue font-body text-sm uppercase tracking-widest font-medium rounded-lg transition-colors duration-300"\n                data-i18n="experiencias.cultura_vinos_cta"\n              >\n                Explorar\n              </a>',
    ),
    # Partners section label
    (
        '<p class="font-body uppercase tracking-[0.3em] text-brand-gold text-xs font-medium mb-4">\n          COLABORADORES\n        </p>',
        '<p class="font-body uppercase tracking-[0.3em] text-brand-gold text-xs font-medium mb-4" data-i18n="experiencias.partners_label">\n          COLABORADORES\n        </p>',
    ),
    # Partners heading
    (
        '<h2 class="font-display font-light text-3xl sm:text-4xl md:text-5xl text-brand-blue">\n          Nuestros colaboradores locales\n        </h2>',
        '<h2 class="font-display font-light text-3xl sm:text-4xl md:text-5xl text-brand-blue" data-i18n="experiencias.partners_heading">\n          Nuestros colaboradores locales\n        </h2>',
    ),
    # Partners subtitle
    (
        '<p class="font-body text-brand-stone text-base text-center leading-relaxed max-w-2xl mx-auto mb-16">\n        Trabajamos con los mejores proveedores de la zona para ofrecerte experiencias auténticas\n      </p>',
        '<p class="font-body text-brand-stone text-base text-center leading-relaxed max-w-2xl mx-auto mb-16" data-i18n="experiencias.partners_subtitle">\n        Trabajamos con los mejores proveedores de la zona para ofrecerte experiencias auténticas\n      </p>',
    ),
    # Form section label
    (
        '<p class="font-body uppercase tracking-[0.3em] text-brand-gold text-xs font-medium mb-4">\n          PLANIFICA TU ESTANCIA\n        </p>',
        '<p class="font-body uppercase tracking-[0.3em] text-brand-gold text-xs font-medium mb-4" data-i18n="experiencias.form_label">\n          PLANIFICA TU ESTANCIA\n        </p>',
    ),
    # Form heading
    (
        '<h2 class="font-display font-light italic text-3xl sm:text-4xl md:text-5xl text-white leading-tight">\n          Diseña tu experiencia perfecta\n        </h2>',
        '<h2 class="font-display font-light italic text-3xl sm:text-4xl md:text-5xl text-white leading-tight" data-i18n="experiencias.form_heading">\n          Diseña tu experiencia perfecta\n        </h2>',
    ),
    # Form body
    (
        '<p class="font-body text-white/60 text-base mt-4 leading-relaxed">\n          Cuéntanos qué te apetece y lo organizamos todo por ti\n        </p>',
        '<p class="font-body text-white/60 text-base mt-4 leading-relaxed" data-i18n="experiencias.form_body">\n          Cuéntanos qué te apetece y lo organizamos todo por ti\n        </p>',
    ),
    # Form labels
    (
        'for="nombre" class="font-body text-xs uppercase tracking-widest text-white/70 font-medium">\n                Nombre *\n              </label>',
        'for="nombre" class="font-body text-xs uppercase tracking-widest text-white/70 font-medium" data-i18n="experiencias.form_name_label">\n                Nombre *\n              </label>',
    ),
    (
        'for="email" class="font-body text-xs uppercase tracking-widest text-white/70 font-medium">\n                Email *\n              </label>',
        'for="email" class="font-body text-xs uppercase tracking-widest text-white/70 font-medium" data-i18n="experiencias.form_email_label">\n                Email *\n              </label>',
    ),
    (
        'for="telefono" class="font-body text-xs uppercase tracking-widest text-white/70 font-medium">\n                Teléfono\n              </label>',
        'for="telefono" class="font-body text-xs uppercase tracking-widest text-white/70 font-medium" data-i18n="experiencias.form_phone_label">\n                Teléfono\n              </label>',
    ),
    (
        'for="tipo-experiencia" class="font-body text-xs uppercase tracking-widest text-white/70 font-medium">\n                Tipo de experiencia *\n              </label>',
        'for="tipo-experiencia" class="font-body text-xs uppercase tracking-widest text-white/70 font-medium" data-i18n="experiencias.form_type_label">\n                Tipo de experiencia *\n              </label>',
    ),
    # Select options
    (
        '<option value="" disabled selected class="text-brand-blue">Selecciona una opción</option>',
        '<option value="" disabled selected class="text-brand-blue" data-i18n="experiencias.form_type_select">Selecciona una opción</option>',
    ),
    (
        '<option value="sierra-irta" class="text-brand-blue">Sierra de Irta</option>',
        '<option value="sierra-irta" class="text-brand-blue" data-i18n="experiencias.form_type_sierra">Sierra de Irta</option>',
    ),
    (
        '<option value="actividades-acuaticas" class="text-brand-blue">Actividades Acuáticas</option>',
        '<option value="actividades-acuaticas" class="text-brand-blue" data-i18n="experiencias.form_type_acuaticas">Actividades Acuáticas</option>',
    ),
    (
        '<option value="cultura-historia" class="text-brand-blue">Cultura &amp; Historia</option>',
        '<option value="cultura-historia" class="text-brand-blue" data-i18n="experiencias.form_type_cultura">Cultura &amp; Historia</option>',
    ),
    (
        '<option value="gastronomia" class="text-brand-blue">Gastronomía</option>',
        '<option value="gastronomia" class="text-brand-blue" data-i18n="experiencias.form_type_gastronomia">Gastronomía</option>',
    ),
    (
        '<option value="combinacion" class="text-brand-blue">Combinación personalizada</option>',
        '<option value="combinacion" class="text-brand-blue" data-i18n="experiencias.form_type_combinacion">Combinación personalizada</option>',
    ),
    # Date/guests labels
    (
        'for="fecha-llegada" class="font-body text-xs uppercase tracking-widest text-white/70 font-medium">\n                Fecha de llegada\n              </label>',
        'for="fecha-llegada" class="font-body text-xs uppercase tracking-widest text-white/70 font-medium" data-i18n="experiencias.form_date_label">\n                Fecha de llegada\n              </label>',
    ),
    (
        'for="personas" class="font-body text-xs uppercase tracking-widest text-white/70 font-medium">\n                Nº personas\n              </label>',
        'for="personas" class="font-body text-xs uppercase tracking-widest text-white/70 font-medium" data-i18n="experiencias.form_guests_label">\n                Nº personas\n              </label>',
    ),
    # Message label
    (
        'for="mensaje" class="font-body text-xs uppercase tracking-widest text-white/70 font-medium">\n              Mensaje especial\n            </label>',
        'for="mensaje" class="font-body text-xs uppercase tracking-widest text-white/70 font-medium" data-i18n="experiencias.form_message_label">\n              Mensaje especial\n            </label>',
    ),
    # Submit button
    (
        '              Planificar mi Experiencia\n            </button>',
        '              <span data-i18n="experiencias.form_submit">Planificar mi Experiencia</span>\n            </button>',
    ),
    # Response time
    (
        '<p class="font-body text-white/50 text-xs text-center">\n              Incluido en estancias de 3 noches o más &middot; Resto bajo reserva previa\n            </p>',
        '<p class="font-body text-white/50 text-xs text-center" data-i18n="experiencias.form_response_time">\n              Incluido en estancias de 3 noches o más &middot; Resto bajo reserva previa\n            </p>',
    ),
    # Crosssell label
    (
        '<p class="font-body text-center uppercase tracking-[0.3em] text-brand-stone text-xs font-medium mb-12">\n        DESCUBRE MÁS\n      </p>',
        '<p class="font-body text-center uppercase tracking-[0.3em] text-brand-stone text-xs font-medium mb-12" data-i18n="experiencias.crosssell_label">\n        DESCUBRE MÁS\n      </p>',
    ),
    # Crosssell links
    (
        'class="font-display text-2xl text-brand-blue font-light group-hover:text-brand-gold transition-colors duration-300">\n            El Hotel →',
        'class="font-display text-2xl text-brand-blue font-light group-hover:text-brand-gold transition-colors duration-300" data-i18n="experiencias.crosssell_hotel">\n            El Hotel →',
    ),
    (
        'class="font-display text-2xl text-brand-blue font-light group-hover:text-brand-gold transition-colors duration-300">\n            El Restaurante →',
        'class="font-display text-2xl text-brand-blue font-light group-hover:text-brand-gold transition-colors duration-300" data-i18n="experiencias.crosssell_restaurante">\n            El Restaurante →',
    ),
    (
        'class="font-display text-2xl text-brand-blue font-light group-hover:text-brand-gold transition-colors duration-300">\n            Eventos &amp; Celebraciones →',
        'class="font-display text-2xl text-brand-blue font-light group-hover:text-brand-gold transition-colors duration-300" data-i18n="experiencias.crosssell_eventos">\n            Eventos &amp; Celebraciones →',
    ),
]

for old, new in replacements:
    if old in content:
        content = content.replace(old, new, 1)
    else:
        print(f"WARNING: not found: {old[:80]!r}")

with open('src/pages/experiencias.astro', 'w', encoding='utf-8') as f:
    f.write(content)

print("experiencias.astro annotated.")
