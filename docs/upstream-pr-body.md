## Summary

This PR introduces a configurable base directory (`BASE_DIR`) for all component
and extension installations in KIAUH.

Today every install path is hard-coded to `Path.home()`. This change replaces
those references with a single constant, `BASE_DIR`, that **defaults to
`Path.home()`** and can optionally be overridden via:

1. The `KIAUH_BASE_DIR` environment variable (highest priority), or
2. The `base_dir` option in `kiauh.cfg` (persisted)

When neither is set KIAUH behaves **identically to today** — every path
resolves to `~/component` exactly as before.

## Motivation

| Scenario | Why it's blocked today |
|---|---|
| Multi-printer farms | Separate stacks under `/srv/printer1/`, `/srv/printer2/` |
| System-wide installs | Shared box with Klipper under `/opt/klipper-stack/` |
| Container / chroot | `$HOME` doesn't exist or is ephemeral |
| CI/CD testing | Deterministic, non-home install paths |

## What changes

| File | Change |
|---|---|
| `core/constants.py` | Add `_resolve_base_dir()` → `BASE_DIR` |
| `default.kiauh.cfg` | Add commented `#base_dir:` option |
| `core/settings/kiauh_settings.py` | Add `base_dir` to `AppSettings` |
| `main.py` | Log non-default `BASE_DIR` at startup |
| 15× component/extension `__init__.py` | `Path.home()` → `BASE_DIR` |
| `utils/fs_utils.py` | `BASE_DIR` in `get_data_dir()` |
| `utils/sys_utils.py` | Check both `~` and `BASE_DIR` for NGINX perms |
| `core/services/backup_service.py` | Fallback-search both `~` and `BASE_DIR` |
| `components/moonraker/utils/utils.py` | Fallback-search both `~` and `BASE_DIR` |
| `components/webui_client/client_utils.py` | `tempfile.mkstemp()` for nginx tmp file |

## Backward compatibility

**Zero breaking change.** The default value of `BASE_DIR` is `Path.home()`, so
every path continues to resolve to `~/component` unless the user explicitly sets
the env var or config option.

## How to use

```bash
# Option A: per-session env var
export KIAUH_BASE_DIR=/opt/klipper-farm
./kiauh.sh

# Option B: persistent — add to kiauh.cfg under [kiauh]:
base_dir: /opt/klipper-farm
```

## Testing

```bash
# Default — no override, identical to upstream
PYTHONPATH=kiauh python3 -c "
from core.constants import BASE_DIR; from pathlib import Path
assert BASE_DIR == Path.home(); print('PASS: default')"

# Env var override
KIAUH_BASE_DIR=/opt/test PYTHONPATH=kiauh python3 -c "
from core.constants import BASE_DIR
assert str(BASE_DIR) == '/opt/test'; print('PASS: env var')"

# Invalid (relative / empty) falls back to home
KIAUH_BASE_DIR=relative PYTHONPATH=kiauh python3 -c "
from core.constants import BASE_DIR; from pathlib import Path
assert BASE_DIR == Path.home(); print('PASS: relative fallback')"
```
