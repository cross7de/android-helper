import argparse
from pathlib import Path
from textwrap import dedent

from .constants import init_ctx, VERSION
from .actions.debloat import cmd_debloat
from .actions.install_reinstall import cmd_install_reinstall
from .actions.install_apk import cmd_install_apk
from .actions.install_playstore import cmd_install_playstore
from .menu import menu, print_quickstart

def build_parser() -> argparse.ArgumentParser:
    epilog = dedent(f"""
    Beispiele:
      Interaktives Menü:           %(prog)s menu
      Debloat (Profil auto):       %(prog)s debloat -P auto
      Reinstall:                   %(prog)s install reinstall -s
      APKs installieren:           %(prog)s install apk -p ./apks/
      Play-Store öffnen:           %(prog)s install playstore -f ./config/<profil>/playstore.list

    Version: {VERSION}
    """).rstrip()

    parser = argparse.ArgumentParser(
        prog="android-helper.py",
        description="Android Debloat & Install Helper – Multi-Profil (Moto, Xiaomi/MIUI/HyperOS, generic).",
        epilog=epilog,
        formatter_class=argparse.RawTextHelpFormatter,
        add_help=False,
    )

    # Globale Optionen
    g = parser.add_argument_group("GLOBAL-OPTIONEN")
    g.add_argument("-n", "--dry-run", action="store_true",
                   help="Nur anzeigen, was passieren würde (keine Änderungen)")
    g.add_argument("-q", "--quiet", action="store_true",
                   help="Weniger Ausgaben (nur Warnungen/Fehler)")
    g.add_argument("-y", "--yes", "--assume-yes", dest="yes", action="store_true",
                   help='Bestätigungen automatisch mit "Ja" beantworten')
    g.add_argument("-P", "--profile", type=str, default="auto",
                   help="Profil: auto | moto | xiaomi_miui | xiaomi_hyperos | generic (Standard: auto)")
    g.add_argument("--adb-path", type=str, default="adb",
                   help="Pfad zu adb (Standard: in $PATH gefunden)")
    g.add_argument("--config-dir", type=str, default=str(Path.cwd() / "config"),
                   help="Konfigurationsverzeichnis (Standard: ./config)")
    g.add_argument("--apks-dir", type=str, default=str(Path.cwd() / "apks"),
                   help="APK-Verzeichnis (Standard: ./apks)")
    g.add_argument("--state-dir", type=str, default=str(Path.cwd() / "state"),
                   help="Zustand/Protokolle (Standard: ./state)")
    g.add_argument("-V", "--version", action="store_true",
                   help="Versionsinfo anzeigen")
    g.add_argument("-h", "--help", action="help",
                   help="Diese Hilfe anzeigen")

    sub = parser.add_subparsers(dest="command", metavar="BEFEHL")

    # menu
    p_menu = sub.add_parser("menu", help="Interaktives Menü starten", add_help=False)
    p_menu.add_argument("-h", "--help", action="help", help="Diese Hilfe anzeigen")

    # debloat
    p_debloat = sub.add_parser("debloat", help="Bloatware entfernen", add_help=False)
    p_debloat.add_argument("-f", "--list", dest="list_file", type=str,
                           help="Debloat-Liste (Format: paket|beschreibung) – überschreibt Profil-Liste")
    p_debloat.add_argument("-F", "--protect", dest="protect_file", type=str,
                           help="Zusätzliche Schutzliste – ergänzt Profil-Liste")
    p_debloat.add_argument("-h", "--help", action="help", help="Diese Hilfe anzeigen")

    # install root
    p_install = sub.add_parser("install", help="Installationsfunktionen", add_help=False)
    p_install.add_argument("-h", "--help", action="help", help="Diese Hilfe anzeigen")
    sub_install = p_install.add_subparsers(dest="install_cmd", metavar="UNTERBEFEHL")

    # install reinstall
    p_re = sub_install.add_parser("reinstall", help="System-Apps reaktivieren", add_help=False)
    p_re.add_argument("-s", "--scan-uninstalled", action="store_true",
                      help="Scan mit 'pm list packages -u' ergänzen")
    p_re.add_argument("--no-state", action="store_true",
                      help="Ignoriere ./state/removed*.json (nur Scan nutzen)")
    p_re.add_argument("-h", "--help", action="help", help="Diese Hilfe anzeigen")

    # install apk
    p_apk = sub_install.add_parser("apk", help="APK(s) installieren", add_help=False)
    p_apk.add_argument("-p", "--path", type=str,
                       help="Datei oder Ordner; ohne Angabe: scannt --apks-dir")
    rep_group = p_apk.add_mutually_exclusive_group()
    rep_group.add_argument("-r", "--replace", dest="replace", action="store_true",
                           help="Update erlauben (adb install -r) [Standard]")
    rep_group.add_argument("--no-replace", dest="replace", action="store_false",
                           help="Update nicht erzwingen")
    p_apk.set_defaults(replace=True)
    p_apk.add_argument("-d", "--downgrade", action="store_true",
                       help="Downgrade erlauben (adb -d) [vorsicht]")
    p_apk.add_argument("--fail-fast", action="store_true",
                       help="Beim ersten Fehler abbrechen (sonst nur Warnungen)")
    p_apk.add_argument("-h", "--help", action="help", help="Diese Hilfe anzeigen")

    # install playstore
    p_ps = sub_install.add_parser("playstore", help="Play-Store-Seiten öffnen", add_help=False)
    p_ps.add_argument("-f", "--from-list", dest="from_list", type=str,
                      help="Paketnamenliste (eine Zeile = com.example.app)")
    p_ps.add_argument("-p", "--pkg", action="append", default=[],
                      help="Paketname (mehrfach nutzbar)")
    p_ps.add_argument("-h", "--help", action="help", help="Diese Hilfe anzeigen")

    return parser

def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    init_ctx(args)

    if getattr(args, "version", False):
        print(VERSION)
        return 0

    if not args.command:
        print_quickstart()
        return menu() or 0

    if args.command == "menu":
        return menu() or 0

    if args.command == "debloat":
        list_file = Path(args.list_file) if getattr(args, "list_file", None) else None
        protect_file = Path(args.protect_file) if getattr(args, "protect_file", None) else None
        return cmd_debloat(list_file=list_file, protect_file=protect_file) or 0

    if args.command == "install":
        if args.install_cmd == "reinstall":
            scan = bool(getattr(args, "scan_uninstalled", False))
            use_state = not bool(getattr(args, "no_state", False))
            return cmd_install_reinstall(scan_uninstalled=scan, use_state=use_state) or 0

        if args.install_cmd == "apk":
            p = Path(args.path) if getattr(args, "path", None) else None
            replace = bool(getattr(args, "replace", True))
            downgrade = bool(getattr(args, "downgrade", False))
            fail_fast = bool(getattr(args, "fail_fast", False))
            return cmd_install_apk(path=p, replace=replace, downgrade=downgrade, fail_fast=fail_fast) or 0

        if args.install_cmd == "playstore":
            from_list = Path(args.from_list) if getattr(args, "from_list", None) else None
            pkgs = list(getattr(args, "pkg", []))
            return cmd_install_playstore(from_list=from_list, pkgs=pkgs) or 0

        from .utils.log import err_fatal
        err_fatal("Unbekannter Unterbefehl für 'install'. Nutze '--help'.", code=7)

    from .utils.log import err_fatal
    err_fatal("Unbekannter Befehl. Nutze '--help'.", code=8)
