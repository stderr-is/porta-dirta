---
name: Claude memory setup — Google Drive sync
description: How Claude memory is structured, where it lives, and how to replicate on a new machine
type: reference
---

## Architecture

```
/home/stderr/google-drive/_memory/        ← Google Drive (syncs to all devices)
  ├── 00_Master_Architecture.md           ← Project docs (in Obsidian + git)
  ├── ...
  └── memory/                             ← Claude auto-memory (NOT in git)
      ├── MEMORY.md                       ← Index (loaded every session)
      ├── reference_credentials.md        ← Passwords (gitignored)
      └── feedback_*.md / project_*.md

~/.claude/projects/-home-stderr/memory   → symlink → google-drive/_memory/memory/
```

## Setting up on a new machine

1. Install Google Drive and wait for `_memory/` to sync
2. Create the symlink:
```bash
mkdir -p ~/.claude/projects/-home-stderr
ln -s ~/google-drive/_memory/memory ~/.claude/projects/-home-stderr/memory
```
3. Done — Claude Code will load all memories automatically on next session.

## Git backup

- All `_memory/` files EXCEPT `memory/reference_credentials.md` are in git
- `memory/.gitignore` excludes credentials
- To push changes from VPS: `gitpush "message"` (runs from `/opt/portadirta-repo/`)
- Local git root: `/home/stderr` (not `/home/stderr/hospitality-project/`)

## Obsidian

Open `/home/stderr/google-drive/_memory/` as an Obsidian vault — all project docs + memory files visible and editable there.
