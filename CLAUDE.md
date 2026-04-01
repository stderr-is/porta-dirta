# Project: Porta D'irta (Peñíscola)

## 🧠 Strategic Memory Access (Lazy-Loading)
**DO NOT read all memory files on startup. Follow this strict hierarchy to conserve context limits:**
1. **Startup:** Read ONLY `_memory/01_Implementation_Roadmap.md` to identify the current active task.
2. **Architecture / Data Flow:** Read `_memory/00_Master_Architecture.md` ONLY if the current task involves Beds24, TastyIgniter, or Hi.Events integration.
3. **Design:** Read `_memory/04_Hospitality_Design_System.md` ONLY if building or modifying UI components.
4. **Risk:** Read `_memory/02_Risk_Management.md` ONLY when refactoring core logic or payment flows.

## 🔍 Context & Tool Rules (Strict Efficiency)
- **Search First:** Never read a file over 100 lines without searching it first. Always use `ls` and `grep` (or `ast-grep`) to find the specific function, component, or line number.
- **Large Files:** If a file is over 300 lines, use `sed`, `head`, or `tail` to read specific blocks rather than loading the entire file into context.
- **n8n & Backends:** DO NOT read `.json` workflow files or massive backend logs directly. Refer to architecture docs or ask for specific node logic.
- **Media:** DO NOT attempt to read image files in `frontend/public/assets/`. Rely on descriptions.

## ✍️ Maintenance Protocol
**End-of-Session updates must be lean and targeted:**
- Always mark completed tasks with `[x]` in `01_Implementation_Roadmap.md`.
- ONLY update `00_Master_Architecture.md`, `04_Hospitality_Design_System.md`, or `02_Risk_Management.md` if a **major** structural or design shift occurred during the session. Do not append minor tweaks.
- Run `/compact` before executing final memory saves to reduce prompt payload.

## 🎨 Design Directive (Imitation Phase)
- **Framework:** Astro (SSG) with Tailwind CSS. Maintain component isolation; do not modify global styles unless explicitly requested.
- **Style:** Imitate placeholder images using Tailwind utility classes (e.g., `backdrop-blur`, `bg-white/10` for glassmorphism, specific shadows).
- **Assets:** Use placeholders for images pending real photography.

## 🌐 Translation & Localisation Tasks
- **Always use `gemini-cli`** with model `gemini-2.5-flash-lite` for generating or updating translation strings.
- Example: `gemini-cli --model gemini-2.5-flash-lite` — then paste the string dictionary task.
- Never manually write translation strings for EN/FR/DE when gemini-cli can do it faster.

## 🛠️ Tech Stack
- Frontend: Astro, Tailwind CSS
- Booking: Beds24 API V2 (Master source of truth)
- Restaurant: TastyIgniter API
- Events/Ticketing: Hi.Events
- Automation: n8n
- Hosting: Coolify/Railway (Docker)