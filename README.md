# CFB 27 Defensive Playbook Lab

**Version:** 4.4 Beta

A standalone browser tool for exploring CFB 27 defensive formations and plays, visualizing player assignments, building custom play maps, and saving defensive macro packages.

## Files

- `index.html` — the complete application and GitHub Pages entry file
- `README.md` — setup, sharing, and release information
- `example-backup.json` — empty example of the backup/import format

## Run locally

1. Download or extract the package.
2. Open `index.html` in Google Chrome.
3. No installation or internet connection is required after the file is downloaded.

Your macros, mapped plays, and My Playbook selections are stored in that browser on that device. Use **Export Backup** inside the application to preserve or transfer them.

## Publish with GitHub Pages

1. Create a new GitHub repository.
2. Upload the three files in this package to the repository root.
3. Open **Settings → Pages**.
4. Under **Build and deployment**, choose **Deploy from a branch**.
5. Select the `main` branch and `/ (root)`, then save.
6. GitHub will provide the public website address after deployment.

Do not rename `index.html`; GitHub Pages uses that filename as the home page.

## Included features

- 72 defensive formations and 1,245 formation-specific play entries
- Formation, play-type, and map-status filters
- Global formation/play search
- My Playbook favorites
- Player-by-player zone, spy, contain, and rush assignments
- Draft and verified play maps
- Ten saved macro slots
- Undo, backup export/import, help, release notes, and protected reset
- Clear distinction between inferred base assignments and manual overrides

## Accuracy note

Formation and play names were compiled from public CFB 27 playbook databases. Initial play art is an inferred shell unless a play map has been verified against the game.

Position assignment menus are conservatively filtered by player role, but formation-specific in-game exceptions may still exist. Treat **Verified** as a status reserved for assignments checked directly in CFB 27.

## Sharing and backups

The application is self-contained, so `index.html` can be sent directly to another Chrome user. Each user receives separate local browser storage.

Importing a backup replaces the current macros, play maps, and My Playbook selections. Export the current data before importing when it needs to be retained.

## Release

**CFB 27 Defensive Playbook Lab v4.4 Beta**
