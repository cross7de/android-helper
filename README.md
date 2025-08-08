# android-helper

Android Debloat & Install Helper – **Multi-Profil** (Moto, Xiaomi/MIUI/HyperOS, generic).

## Features
- Profile: `--profile auto|moto|xiaomi_miui|xiaomi_hyperos|generic` (Auto-Detect Standard)
- Debloat per Profil-Listen (config/<profil>/debloat.list, protect.list) oder Defaults
- Install: Reinstall (System-Apps), APK(s) (inkl. Split-APKs), Play-Store-Intent
- Interaktives Menü
- Saubere CLI: `-n/--dry-run`, `-q/--quiet`, `-y/--yes`, `-V/--version`, `-P/--profile`

## Quickstart
```bash
chmod +x android_helper.py
./android_helper.py --help
./android_helper.py            # Quickstart + Menü
./android_helper.py debloat -P auto
./android_helper.py install reinstall
./android_helper.py install apk -p ./apks/
./android_helper.py install playstore -f ./config/moto/playstore.list
```

## Profile & Konfig
```
config/
  moto/
    debloat.list
    protect.list
  xiaomi_miui/
    debloat.list
    protect.list
  xiaomi_hyperos/
    debloat.list
    protect.list
```
- Falls eine Datei nicht existiert, greifen **sinnvolle Defaults**.

## Installation als Tool (optional)
```bash
python3 -m pip install -e .
android-helper --help
```

## Lizenz
MIT
