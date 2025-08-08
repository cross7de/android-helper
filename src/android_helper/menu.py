from textwrap import dedent
from pathlib import Path
from .actions.debloat import cmd_debloat
from .actions.install_reinstall import cmd_install_reinstall
from .actions.install_apk import cmd_install_apk
from .actions.install_playstore import cmd_install_playstore
from .utils.log import log
from .constants import VERSION, ctx

def print_quickstart():
    qs = dedent(f"""
    Quickstart:
      1) USB-Debugging am Gerät aktivieren (RSA-Dialog „Diesem Computer vertrauen“).
      2) Hilfe/Usage ansehen:   android-helper.py --help
      3) Geführt starten:       android-helper.py menu
         Häufig:
           Debloat:             android-helper.py debloat
           System-Apps zurück:  android-helper.py install reinstall
           APK(s) installieren: android-helper.py install apk -p ./apks/
           Play-Store öffnen:   android-helper.py install playstore -f ./config/<profil>/playstore.list
    Hinweis: Dry-Run mit -n, z. B. 'android-helper.py -n debloat'

    Version: {VERSION}
    Aktives Profil: {ctx.profile}
    """).strip("\n")
    print(qs)

def menu():
    while True:
        print(dedent("""
        === HAUPTMENÜ ===
        1) Debloat                      (= android-helper.py debloat)
        2) Install → Reinstall          (= android-helper.py install reinstall)
        3) Install → APK(s)             (= android-helper.py install apk)
        4) Install → Play-Store         (= android-helper.py install playstore)
        5) Profil wechseln
        h) Hilfe/Usage                  (= android-helper.py --help)
        q) Beenden
        """).rstrip())
        choice = input("> ").strip().lower()
        if choice == "1":
            log("\n→ Befehl: android-helper.py debloat\n", force=True)
            cmd_debloat(list_file=None, protect_file=None)
        elif choice == "2":
            log("\n→ Befehl: android-helper.py install reinstall\n", force=True)
            cmd_install_reinstall(scan_uninstalled=False, use_state=True)
        elif choice == "3":
            p = input("Pfad zu APK oder Ordner (Leer = Standard ./apks): ").strip()
            arg = Path(p) if p else None
            shown = f" -p {p}" if p else ""
            log(f"\n→ Befehl: android-helper.py install apk{shown}\n", force=True)
            cmd_install_apk(path=arg, replace=True, downgrade=False, fail_fast=False)
        elif choice == "4":
            src = input("Liste (-f) oder einzelne Pakete (-p, komma-getrennt)? Datei/Pakete: ").strip()
            if src and Path(src).exists():
                log(f"\n→ Befehl: android-helper.py install playstore -f {src}\n", force=True)
                cmd_install_playstore(from_list=Path(src), pkgs=[])
            else:
                pkgs = [s.strip() for s in src.split(",") if s.strip()]
                shown = " ".join(f"-p {p}" for p in pkgs) if pkgs else ""
                log(f"\n→ Befehl: android-helper.py install playstore {shown}\n", force=True)
                cmd_install_playstore(from_list=None, pkgs=pkgs)
        elif choice == "5":
            newp = input("Profil (auto/moto/xiaomi_miui/xiaomi_hyperos/generic): ").strip()
            if newp:
                ctx.profile = newp
                print(f"Aktives Profil: {ctx.profile}")
        elif choice == "h":
            from .cli import build_parser
            print(build_parser().format_help())
        elif choice == "q":
            print("Bye.")
            break
        else:
            print("Ungültige Eingabe.")
