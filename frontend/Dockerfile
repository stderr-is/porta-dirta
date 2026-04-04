# Porta D'irta — Astro SSR container (Hostinger VPS)
# Build: docker build -t portadirta-frontend .
# Run:   docker run -p 4321:4321 --env-file .env portadirta-frontend

FROM node:22-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .

# SSR build for Node.js standalone server
RUN BUILD_TARGET=node npm run build

# ── Runtime stage ──────────────────────────────────────────────────────────────
FROM node:22-alpine AS runtime

WORKDIR /app

# Only copy the built output — no dev dependencies
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json

ENV HOST=0.0.0.0
ENV PORT=4321
ENV NODE_ENV=production

EXPOSE 4321

USER node

CMD ["node", "./dist/server/entry.mjs"]
