# Entwickler-Notizen für android-helper

Diese Datei ist für Entwickler und dich selbst als „Langzeit-Gedächtnis“ gedacht.

---

## Lokale Einrichtung

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

**Wichtig:** immer vor Arbeit am Code venv aktivieren:
```bash
source .venv/bin/activate
```

---

## Wichtige Befehle

- CLI starten (installiert):  
  ```bash
  android-helper --help
  ```

- CLI starten (ohne Installation, Wrapper):  
  ```bash
  ./android_helper_local.py --help
  ```

- Linter prüfen:  
  ```bash
  ruff check src android_helper_local.py
  ```

- Auto-Fixes mit Ruff:  
  ```bash
  ruff check src android_helper_local.py --fix
  ```

- Smoke-Test lokal:  
  ```bash
  python -m android_helper.cli --help
  ```

---

## Branch-Strategie

- `main` → stabiler, getesteter Stand
- `feature/*` → neue Funktionen
- `fix/*` → Bugfixes
- PRs werden per GitHub Actions (Lint + Smoke-Test) geprüft

---

## Dateien und Verzeichnisse

- `src/android_helper/` → Python-Paket
- `config/<profil>/` → Debloat- und Protect-Listen pro Profil
- `apks/` → APK-Dateien für Installationen
- `state/` → Laufzeit-/Cache-Daten
- `.github/workflows/ci.yml` → CI-Definition (Python 3.10, Ruff, Smoke-Test)

---

## Tipps

- `run`-Script im Repo nutzen, um CLI schnell aufzurufen:
  ```bash
  ./run --help
  ```
- Bei längerer Pause immer zuerst README/DEV.md anschauen  
  (hier steht alles für einen schnellen Wiedereinstieg).

