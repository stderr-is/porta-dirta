import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const colaboradores = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/colaboradores' }),
  schema: z.object({
    nombre: z.string(),
    categoria: z.string(),
    descripcion: z.string(),
    orden: z.number().default(0),
    website: z.string().url().optional(),
  }),
});

const eventosLocales = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/eventos-locales' }),
  schema: z.object({
    titulo: z.string(),
    fecha: z.coerce.date(),
    fechaFin: z.coerce.date().optional(),
    categoria: z.enum(['gastronomia', 'cultura', 'musica', 'naturaleza', 'otro']),
    descripcion: z.string(),
    imagen: z.string().optional(),
    precio: z.number().optional(),
    aforo: z.number().optional(),
    ticketsUrl: z.string().url().optional(),
  }),
});

export const collections = {
  colaboradores,
  'eventos-locales': eventosLocales,
};
