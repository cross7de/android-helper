# android-helper

Ein universeller ADB-Helfer für Android-Geräte (z. B. Motorola, Xiaomi, HyperOS, MIUI).  
Unterstützt Debloat, Reinstall und APK-Installationen – alles per Profil steuerbar.

---

## Quickstart (lokal)

```bash
# 1. Virtuelle Umgebung anlegen und aktivieren
python3 -m venv .venv
source .venv/bin/activate

# 2. Im Entwicklermodus installieren
pip install -e .

# 3. CLI starten
android-helper --help

# ... oder lokal ohne Installation (Wrapper)
./android_helper.py --help
```

---

## Features

- Mehrere Geräte-Profile (`moto`, `xiaomi_miui`, `xiaomi_hyperos`, …)
- Debloat-Listen (`config/<profil>/debloat.list`)
- Schutz-Listen (`config/<profil>/protect.list`)
- Installations- und Reinstall-Optionen
- Saubere CLI mit Kurz- und Langoptionen
- CI-Checks (ruff, Smoke-Test)

---

## Lizenz
[MIT](LICENSE)

