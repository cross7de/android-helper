from pathlib import Path
from ..utils.adb import run, require_adb, device_info
from ..utils.log import log, warn, err_fatal
from ..constants import ctx

def is_split_dir(p: Path) -> bool:
    return p.is_dir() and any(x.suffix == ".apk" for x in p.iterdir())

def adb_install_apk(path: Path, *, replace: bool, downgrade: bool) -> bool:
    flags = []
    if replace:
        flags.append("-r")
    if downgrade:
        flags.append("-d")
    if path.is_file():
        cmd = f"{ctx.adb_path} install {' '.join(flags)} {str(path)!s}".strip()
        out = run(cmd).stdout
    elif is_split_dir(path):
        apks = " ".join(str(x) for x in sorted(path.glob('*.apk')))
        cmd = f"{ctx.adb_path} install-multiple {' '.join(flags)} {apks}".strip()
        out = run(cmd).stdout
    else:
        warn(f"Ungültiger Pfad: {path}")
        return False
    if "Success" in out:
        log(f"✅ Installiert: {path.name}")
        return True
    if "INSTALL_FAILED_UPDATE_INCOMPATIBLE" in out:
        warn(f"{path.name}: Signatur-Konflikt (Store-Version ≠ Sideload). Erwäge '--downgrade' oder vorheriges Uninstall.")
    else:
        warn(f"{path.name}: Install-Fehler: {out.strip() or 'Unbekannter Fehler'}")
    return False

def cmd_install_apk(path: Path | None, replace: bool, downgrade: bool, fail_fast: bool):
    require_adb()
    device_info()
    base = path or ctx.apks_dir
    targets = []
    if base.is_file() or is_split_dir(base):
        targets = [base]
    elif base.is_dir():
        for p in sorted(base.iterdir()):
            if p.is_file() and p.suffix == ".apk":
                targets.append(p)
            elif is_split_dir(p):
                targets.append(p)
    else:
        err_fatal(f"Pfad nicht gefunden: {base}", code=4)

    if not targets:
        warn("Keine APKs gefunden.")
        return

    log("\n🔧 Installation …\n")
    errors = 0
    for t in targets:
        ok = adb_install_apk(t, replace=replace, downgrade=downgrade)
        if not ok:
            errors += 1
            if fail_fast:
                err_fatal("Abbruch wegen '--fail-fast'.", code=5)
    if errors:
        warn(f"Fertig mit {errors} Fehler(n).")
    else:
        log("✅ APK-Install abgeschlossen.")
