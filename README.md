# CFB 27 Defensive Playbook Lab

**Version:** 4.60

A standalone browser tool for exploring CFB 27 defensive formations and plays, visualizing player assignments, building custom play maps, and saving defensive macro packages.

## Files

- `index.html` — the complete application and GitHub Pages entry file
- `README.md` — setup, sharing, and release information
- `FINAL_QA_REPORT.md` — final coverage and validation record
- `example-backup.json` — empty example of the backup/import format

## Run locally

1. Download or extract the package.
2. Open `index.html` in Google Chrome.
3. No installation or internet connection is required after the file is downloaded.

Your macros, mapped plays, and My Playbook selections are stored in that browser on that device. Use **Export Backup** inside the application to preserve or transfer them.

## Publish with GitHub Pages

1. Upload the release files to the repository root.
2. Open **Settings → Pages**.
3. Under **Build and deployment**, choose **Deploy from a branch**.
4. Select the `main` branch and `/ (root)`, then save.
5. GitHub will provide the public website address after deployment.

Do not rename `index.html`; GitHub Pages uses that filename as the home page.

## Included features

- 72 defensive formations and 1,245 formation-specific play entries
- 1,243 built-in mapped entries
- 1,204 source-reviewed mapped entries
- 39 legacy-source-confirmed mapped entries
- Formation, play-type, and map-status filters
- Global formation/play search
- My Playbook favorites
- Team Playbook view for all 138 teams across all 31 defensive books, with exact formation/play membership referencing the existing master play database
- Searchable Team Playbook Navigator with favorite teams, recently viewed teams, scheme browsing, local persistence, and backup support
- Weekly Gameplan Builder with opponent selection, situation-based calls, current-play and macro capture, reordering, reload, local persistence, backup support, and a print-friendly Call-Sheet View
- Player-by-player zone, spy, contain, and rush assignments
- Draft and verified play maps
- Ten saved macro slots
- Undo, backup export/import, help, release notes, and protected reset
- Clear distinction between source-reviewed, source-asset-confirmed, built-in, and local verified mappings

## Accuracy note

Two source assets remain intentionally unmapped rather than fabricated:

- `3-3-5 Mint — Cover 9`
- `3-4 Grizzly — Cover 9`

All other built-in mapped entries have completed the final source reconciliation process documented in `FINAL_QA_REPORT.md`.

## Sharing and backups

The application is self-contained, so `index.html` can be sent directly to another Chrome user. Each user receives separate local browser storage.

Importing a backup replaces the current macros, play maps, and My Playbook selections. Export the current data before importing when it needs to be retained.

## Release

**CFB 27 Defensive Playbook Lab v4.60**
