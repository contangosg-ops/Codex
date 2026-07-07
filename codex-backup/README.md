# Codex Backup

This repository contains a portable backup of Codex skills and agent interface files
from this computer.

Included:

- `skills/`: Codex skill folders, including their `agents/openai.yaml` files.
- `plugins/installed-plugins.md`: A safe list of installed plugins.
- `restore-codex.ps1`: A Windows restore script for another computer.

Excluded on purpose:

- `auth.json`
- `.sandbox-secrets/`
- logs and SQLite databases
- runtime caches
- plugin executables
- session history
- machine-specific pipes and paths

## Restore On Another Windows Computer

Clone this repository, open PowerShell inside the repository folder, then run:

```powershell
powershell -ExecutionPolicy Bypass -File .\codex-backup\restore-codex.ps1
```

After restore, restart Codex.

Remote plugins such as Gmail and Data Analytics should be installed again from Codex
on the new computer so login and permissions are created safely for that machine.
