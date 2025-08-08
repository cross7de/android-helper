from pathlib import Path
from ..utils.adb import run, require_adb, device_info
from ..utils.io import read_list_file
from ..utils.log import log, err_fatal
from ..constants import ctx

def cmd_install_playstore(from_list: Path | None, pkgs: list[str]):
    require_adb()
    device_info()
    all_pkgs: list[str] = []
    if from_list:
        all_pkgs += read_list_file(from_list)
    all_pkgs += pkgs
    all_pkgs = [p.strip() for p in all_pkgs if p.strip() and not p.strip().startswith("#")]
    if not all_pkgs:
        err_fatal("Keine Pakete angegeben. Nutze -f/--from-list oder -p/--pkg.", code=6)
    for pkg in all_pkgs:
        url = f"market://details?id={pkg}"
        out = run(f'{ctx.adb_path} shell am start -a android.intent.action.VIEW -d "{url}"').stdout
        log(f"🛒 {pkg}: {out.strip() or 'Intent gestartet'}")
    log("\nℹ️  Bitte am Gerät auf „Installieren“ tippen (silent aus Play Store ohne DO/MDM nicht möglich).")
