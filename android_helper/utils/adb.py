import subprocess
import shlex
from shutil import which as _which
from .log import log, err_fatal
from ..constants import ctx

def run(cmd: str) -> subprocess.CompletedProcess:
    if ctx.dry_run:
        log(f"🧪 {cmd}")
        return subprocess.CompletedProcess(cmd, 0, "", "")
    return subprocess.run(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

def require_adb():
    if not _which(ctx.adb_path):
        err_fatal("adb nicht gefunden. Bitte Android Platform Tools installieren und PATH prüfen.")
    r = run(f"{ctx.adb_path} get-state")
    if r.returncode != 0 or "device" not in r.stdout:
        err_fatal("Kein Gerät verbunden oder USB-Debugging aus. 'adb devices' prüfen.", code=3)

def device_info():
    oem = run(f"{ctx.adb_path} shell getprop ro.product.manufacturer").stdout.strip().lower()
    model = run(f"{ctx.adb_path} shell getprop ro.product.model").stdout.strip()
    android = run(f"{ctx.adb_path} shell getprop ro.build.version.release").stdout.strip()
    log(f"📱 Gerät: {model or '?'} | Hersteller: {oem or '?'} | Android: {android or '?'}")
    return oem, model, android

def detect_profile() -> str:
    oem = run(f"{ctx.adb_path} shell getprop ro.product.manufacturer").stdout.strip().lower()
    build = run(f"{ctx.adb_path} shell getprop ro.build.display.id").stdout.strip().lower()
    if "motorola" in oem:
        return "moto"
    if "xiaomi" in oem or "redmi" in oem or "poco" in oem:
        if "hyperos" in build:
            return "xiaomi_hyperos"
        if "miui" in build:
            return "xiaomi_miui"
        return "xiaomi_miui"
    return "generic"
