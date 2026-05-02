---
name: Local Testing Machine Setup
description: Configuration of the Windows testing environment synced with VPS and Git
type: reference
---

## Status
- **Host:** Windows 10/11 (Local machine)
- **Path:** `C:\Users\Administrator\Desktop\Puerto de Irta\hospitality-project`
- **SSH Access:** Configured via `id_ed25519` (Root access to 72.62.180.39)
- **GitHub Access:** Configured via local `github_vps` key.

## Sync Strategy
1. **Source of Truth:** VPS (`/opt/portadirta/`).
2. **Local Sync:** Repository pulled from VPS via tarball/scp and tracked via Git.
3. **Private Files:** Restored manually from handover folder (`.env` files and `reference_credentials.md`).

## Tools Installed
- **Git:** 2.54.0
- **SSH/SCP/Tar:** OpenSSH for Windows / bsdtar.
