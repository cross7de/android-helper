import shlex, time
from ..utils.adb import run, require_adb, device_info, detect_profile
from ..utils.io import read_list_file, load_state, save_state
from ..utils.log import log, warn
from ..constants import DEFAULT_DEBLOAT_GENERIC, DEFAULT_DEBLOAT_MOTO, DEFAULT_DEBLOAT_XIAOMI, DEFAULT_PROTECT, ctx

def _defaults_for(profile: str):
    if profile == "moto":
        return DEFAULT_DEBLOAT_MOTO
    if profile in ("xiaomi_miui", "xiaomi_hyperos"):
        return DEFAULT_DEBLOAT_XIAOMI
    return DEFAULT_DEBLOAT_GENERIC

def _resolve_profile():
    if ctx.profile and ctx.profile != "auto":
        return ctx.profile
    try:
        p = detect_profile()
        log(f"🔎 Profil-Erkennung: {p}")
        return p
    except Exception:
        warn("Profil-Erkennung fehlgeschlagen. Nutze 'generic'.")
        return "generic"

def _load_profile_list(fname: str, profile: str):
    p1 = ctx.config_dir / profile / fname
    items = read_list_file(p1)
    if items:
        return items
    p2 = ctx.config_dir / fname
    items = read_list_file(p2)
    if items:
        return items
    if fname.startswith("debloat"):
        return _defaults_for(profile)
    return []

def _uninstall_pkg(pkg: str, desc: str, removed: list, extra_protect: set[str]):
    if pkg in DEFAULT_PROTECT or pkg in extra_protect:
        log(f"🛡️  {desc:<32}  (geschützt, übersprungen)")
        return
    out = run(f"{ctx.adb_path} shell pm uninstall --user 0 {shlex.quote(pkg)}").stdout
    if "Success" in out:
        log(f"✅ {desc:<32}  ({pkg})")
        removed.append({"pkg": pkg, "desc": desc, "ts": int(time.time())})
    elif "not installed for 0" in out or "NOT_INSTALLED" in out:
        warn(f"{desc:<32}  bereits nicht installiert")
    elif "-1000" in out or "Permission" in out or "delete failed for" in out:
        warn(f"{desc:<32}  system/geschützt")
    elif "Unknown package" in out:
        warn(f"{desc:<32}  nicht vorhanden")
    else:
        warn(f"{desc:<32}  {out.strip() or 'Unbekannter Fehler'}")

def cmd_debloat(list_file=None, protect_file=None):
    require_adb()
    profile = _resolve_profile()
    oem, model, android = device_info()
    log(f"🧩 Aktives Profil: {profile}")
    entries = read_list_file(list_file) if list_file else _load_profile_list("debloat.list", profile)
    protect_extra = set(read_list_file(protect_file) if protect_file else _load_profile_list("protect.list", profile))
    removed = load_state("removed", [])
    log("\n🔧 Debloat startet…\n")
    for line in entries:
        if "|" in line:
            pkg, desc = [s.strip() for s in line.split("|", 1)]
        else:
            pkg, desc = line.strip(), line.strip()
        _uninstall_pkg(pkg, desc, removed, protect_extra)
    save_state("removed", removed)
    log("\n✅ Debloat abgeschlossen.")
