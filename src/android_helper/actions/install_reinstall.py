from ..utils.adb import run, require_adb, device_info
from ..utils.io import load_state
from ..utils.log import log, warn
from ..constants import ctx
import shlex

def install_existing(pkg: str, desc: str = "") -> bool:
    out = run(f"{ctx.adb_path} shell cmd package install-existing --user 0 {shlex.quote(pkg)}").stdout
    if ("installed for user" in out) or ("Package" in out and "installed" in out):
        log(f"↩️  {desc or pkg:<32}  wiederhergestellt")
        return True
    warn(f"{desc or pkg:<32}  {out.strip() or 'Fehler beim Reinstall'}")
    return False

def cmd_install_reinstall(scan_uninstalled: bool, use_state: bool):
    require_adb()
    device_info()
    candidates = []
    if use_state:
        removed_state = load_state("removed", [])
        candidates.extend([it.get("pkg") for it in removed_state if it.get("pkg")])
    if scan_uninstalled or not candidates:
        out = run(f"{ctx.adb_path} shell pm list packages -u").stdout.splitlines()
        for line in out:
            line = line.strip()
            if line.startswith("package:"):
                pkg = line.split(":", 1)[1].split(" ", 1)[0]
                if pkg not in candidates:
                    candidates.append(pkg)
    if not candidates:
        warn("Keine Kandidaten gefunden.")
        return
    log("\n↩️  Reinstall startet…\n")
    for pkg in candidates:
        install_existing(pkg)
    log("\n✅ Reinstall abgeschlossen.")
