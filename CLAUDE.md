# Project: Porta D'irta (Peñíscola)

## 🧠 Memory Access & Maintenance
**On every startup, immediately read ALL of the following files before doing anything else:**
- `_memory/00_Master_Architecture.md` — system architecture, data flow, Beds24/TastyIgniter/Hi.Events relationships
- `_memory/01_Implementation_Roadmap.md` — current phase, completed/pending tasks
- `_memory/02_Risk_Management.md` — known risks and mitigations
- `_memory/04_Hospitality_Design_System.md` — visual language, conversion architecture, UX philosophy

**After every significant coding session, you are REQUIRED to update the relevant memory files:**
- Mark completed roadmap items with `[x]` in `01_Implementation_Roadmap.md`
- Add new architectural decisions to `00_Master_Architecture.md`
- Add new design decisions/components to `04_Hospitality_Design_System.md`
- Add new risks discovered to `02_Risk_Management.md`

## 🎨 Design Directive (Imitation Phase)
- Reference the "Ideal" images in `frontend/public/assets/placeholders/`.
- Imitate the CSS, shadows, and glassmorphism of those images using Tailwind.
- Use placeholders for images that will later be replaced with real assets.

## 🛠️ Tech Stack
- **Frontend:** Astro (SSG), Tailwind CSS
- **Booking:** Beds24 API V2 (master source of truth)
- **Restaurant:** TastyIgniter API
- **Events/Ticketing:** Hi.Events
- **Automation:** n8n
- **Hosting:** Coolify/Railway (Docker)
