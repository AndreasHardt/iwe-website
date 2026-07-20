# Persönliche Website von Dipl.-Ing. Andreas Hardt – CMS-Version

Diese Version erzeugt die Website automatisch aus editierbaren JSON-Inhaltsdateien und veröffentlicht sie über GitHub Actions auf GitHub Pages.

## Inhalt

- `content/de/` – alle deutschen Texte der Website
- `cms/config.template.yml` – Felder des Redaktionssystems
- `build.py` – erzeugt die fertige Website im Ordner `_site`
- `.github/workflows/pages.yml` – automatische Veröffentlichung
- `static/` – Gestaltung, JavaScript und Bilder
- `OAUTH-EINRICHTUNG.md` – Einrichtung der Schaltfläche „Mit GitHub anmelden“

## Lokal testen

```bash
python build.py
python -m http.server 8000 --directory _site
```

Anschließend `http://localhost:8000` öffnen. Ohne die Variable `SVELTIA_AUTH_URL` zeigt `/admin/` zunächst eine Einrichtungsseite.

## GitHub Pages

Im Repository unter `Settings > Pages` bei `Build and deployment` als Quelle **GitHub Actions** auswählen. Jeder Commit auf `main` erstellt und veröffentlicht die Website neu.

## Inhalte bearbeiten

Nach Einrichtung von OAuth:

1. `/admin/` öffnen.
2. „Mit GitHub anmelden“ auswählen.
3. Gewünschten Bereich öffnen.
4. Texte ändern und speichern.
5. GitHub Actions veröffentlicht die Änderung automatisch.

## Mehrsprachigkeit

Die Verzeichnisse `content/en/` und `content/fr/` sind bereits vorbereitet. Die englische und französische Ausgabe kann später ergänzt werden, ohne die deutsche Inhaltsstruktur neu zu entwerfen.

## Rechtlicher Hinweis

Impressum und Datenschutzerklärung sind technische Arbeitsfassungen und keine Rechtsberatung. Vor der Veröffentlichung rechtlich prüfen lassen.
