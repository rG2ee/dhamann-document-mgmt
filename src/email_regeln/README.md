# email_regeln

Sortiert Mails per IMAP über die lokale Protonmail Bridge in Ordner unter
`Folders/filter-andwendungen/`.

## Ausführung

Alle Skripte werden aus dem Projekt-Root gestartet:

```bash
uv run python src/email_regeln/<skript>.py
```

Die Zugangsdaten kommen aus der `.env` im Projekt-Root (`IMAP_Address`,
`IMAP_port`, `IMAP_Username`, `IMAP_Password`).

## Skripte

| Skript | Zweck | Verändert Mails? |
| --- | --- | --- |
| `run.py` | Hauptlauf: verschiebt Mails anhand der Absender-Zuordnungen | ja |
| `move_to_delete.py` | Verschiebe-Logik inklusive Schutzmechanismen, plus `undo()` für `Folders/to-be-deleted` | ja |
| `move_old_mails.py` | Mails von 2022 und älter aus der INBOX ins Archiv | ja |
| `restore_sent.py` | Holt fälschlich verschobene eigene Mails zurück nach `Sent` | ja |
| `copy_mailbox.py` | `export_all_folders()` schreibt `.eml`-Dateien auf die Platte; `copy_mailbox()` verschiebt serverseitig (siehe Warnung im Docstring) | teils |
| `imap_connection.py` | Verbindung, Ordnerliste, Ordner anlegen | nein |
| `folder_tree.py` | Ordnerstruktur mit Anzahl Nachrichten als `email-state/folder_tree.json` | nein |
| `find_lost_sent.py` | Diagnose: findet, wohin Mails verschoben wurden | nein |
| `absender_statistik.py` | Absender-Häufigkeiten als Grundlage für neue Zuordnungen | nein |
| `search_mail_content.py` | Volltextsuche in der INBOX | nein |

Die Absender-Zuordnungen liegen in
`bereits_ausgefuerht_und_spaeter_als_regel_hinterlegen.py` als
`ZUORDNUNGEN1` … `ZUORDNUNGENn`. `run.py` importiert am Dateiende genau eine
davon; für einen neuen Lauf wird diese Zeile angepasst.

## Vorfall 05.08.2026: Sent-Ordner geleert

**Symptom:** Nach einem Lauf war `Sent` von 753 auf 47 Nachrichten gefallen,
`Drafts` von 83 auf 2.

**Ursache:** Drei Dinge kamen zusammen.

1. Der Lauf lief mit `folder="All Mail"`. Dieser virtuelle Ordner der Bridge
   enthält jede Nachricht des Accounts, also auch `Sent`, `Drafts`, `Archive`
   und `Trash`.
2. In `ZUORDNUNGEN9` stand die eigene Adresse `dennis.hamann@protonmail.com`
   als Suchbegriff für `Folders/filter-andwendungen/persoenliche-kontakte`.
   Jede gesendete Mail trägt die eigene Adresse im `From`-Header, also matchte
   der Filter den kompletten Sent-Ordner.
3. Protonmail-Ordner sind exklusiv: Eine Nachricht liegt in genau einem Ordner.
   Ein `COPY` nach `Folders/…` nimmt sie damit automatisch aus ihrem bisherigen
   Ordner heraus, auch aus `Sent`.

Ein Nebeneffekt von `IMAP SEARCH FROM`: Das ist eine Teilstring-Suche über den
gesamten `From`-Header, inklusive Anzeigename. `"protonmail.com"` als
Suchbegriff hätte 986 Nachrichten getroffen, davon 944 eigene.

**Fund:** Die Mails lagen in `Folders/filter-andwendungen/persoenliche-kontakte`
(168 → 1049 Nachrichten), davon 897 mit eigener Absenderadresse: 845 an fremde
Empfänger, 52 Notizen an sich selbst, verteilt über 2020 bis 2026.

**Behoben am 05.08.2026.** Alle 897 Mails wurden über den Zwischenordner
`Folders/sent-wiederhergestellt` nach `Sent` zurückgeschoben. Danach:
`Sent` 852 Nachrichten (vor dem Vorfall 753), `Drafts` 88 (vorher 83),
`persoenliche-kontakte` 152 (vorher 168). Der Trash blieb unverändert, es ging
also nichts verloren. Dass `Sent` und `Drafts` etwas voller sind als vorher,
liegt daran, dass der Filter auch gesendete Mails erfasst hatte, die vorher in
anderen Ordnern lagen (`Folders/t-online`, `Labels/Imported …`, `Archive`).

## Schutzmechanismen

In `move_to_delete.py` verhindern vier Mechanismen eine Wiederholung:

- **Ausschluss eigener Mails.** Jede Suche wird um `NOT FROM <eigene Adresse>`
  erweitert (`protect_own=True`, Standard). Gesendete Mails, Entwürfe und
  Selbstnotizen können damit gar nicht mehr erfasst werden. Geschützt sind
  nicht nur `IMAP_Username`, sondern auch die Protonmail-Aliasse mit gleichem
  lokalen Teil auf `protonmail.com`, `protonmail.ch`, `pm.me` und `proton.me` –
  im `Sent`-Ordner kommen tatsächlich zwei Adressen vor. Weitere eigene
  Adressen lassen sich in der `.env` unter `OWN_ALIASES` kommagetrennt
  ergänzen, etwa `dennis.hamann.mgmt@proton.me`.

  Eigene Adressen auf Fremd-Domains (`dennis.hamann@external.kadewe.com`,
  `dennis.hamann@deltakonnect.de`) sind bewusst **nicht** geschützt, weil sie in
  den Zuordnungen als legitime Filter dienen.
- **Gesperrte Quellordner.** `Sent` und `Drafts` als `folder` lösen einen
  `ValueError` aus (`PROTECTED_SOURCE_FOLDERS`).
- **Validierung der Suchbegriffe.** `validate_absender()` bricht ab, wenn ein
  Begriff auf die eigene Adresse passt, und warnt bei Begriffen ohne `@` unter
  sechs Zeichen, weil diese als Teilstring viel zu breit treffen. `run.py`
  prüft alle Zuordnungen, bevor die Verbindung aufgebaut wird.
- **Kein Löschen ohne erfolgreiches Kopieren.** `_move_messages()` prüft den
  Status von `COPY` und `STORE` und bricht ab, bevor `\Deleted` gesetzt wird.
  Zusätzlich arbeitet die Funktion mit UIDs statt Sequenznummern und in
  Batches von 200.

`run.py`, `move_to_delete.py` und `move_old_mails.py` starten per `__main__`
bewusst im Dry-Run. Für einen echten Lauf wird `dry_run=False` gesetzt.

Der Ausschluss eigener Mails gilt auch für `move_old_mails.py`
(`protect_own=True`). Das ist nach der Wiederherstellung wichtig: In der INBOX
liegen die Notizen an die eigene Adresse, die Protonmail dort als
Empfangskopie anlegt. Ohne Schutz würde ein Lauf 33 davon direkt wieder ins
Archiv `2022_and_older` verschieben.

`copy_mailbox()` in `copy_mailbox.py` bricht ohne `accept_move=True` ab. Ein
IMAP-`COPY` in einen Ordner unter `Folders/` ist bei Protonmail nämlich ein
Verschieben – mit `All Mail` als Quelle würde es die komplette Mailbox in den
Backup-Ordner umziehen und INBOX, `Sent` und alle Filter-Ordner leeren. Für
Backups ist `export_all_folders()` gedacht, das nur liest und `.eml`-Dateien
schreibt.

### Was der Schutz messbar bewirkt

| Prüfung | ohne Schutz | mit Schutz |
| --- | --- | --- |
| Suchbegriff `protonmail.com` in `All Mail` | 986 Treffer | 42 Treffer |
| Suchbegriff `protonmail.com` in `Sent` | 850 Treffer | 0 Treffer |
| Suchbegriff `pm.me` in `Sent` (Alias) | 2 Treffer | 0 Treffer |
| 386 Suchbegriffe aus `ZUORDNUNGEN13`–`19` gegen `Sent` | 0 Treffer | 0 Treffer |
| `move_old_mails.py` gegen die INBOX | 33 Mails | 0 Mails |

Die mittlere Zeile zeigt, dass die regulären Zuordnungen den `Sent`-Ordner
ohnehin nicht berühren: Sie enthalten fremde Absenderadressen, und in `Sent`
steht immer die eigene Adresse im `From`. Gefährlich war ausschließlich der
eine Eintrag mit der eigenen Adresse.

## Bekannte Einschränkung

Suchbegriffe mit Umlauten liefern über die Bridge keine Treffer, obwohl die
Suche mit `OK` antwortet. Getestet mit `orthopädikum`, `grüne` und `für`,
jeweils 0 Treffer. Grund ist die MIME-Kodierung der Header. Solche Einträge in
den Zuordnungen wirken also nur scheinbar; besser die Mailadresse verwenden.

## Wiederherstellung

`restore_sent.py` verschiebt Mails mit der eigenen Adresse im `From`-Header aus
einem Quellordner zurück nach `Sent`. Standard ist ein Dry-Run mit
Aufschlüsselung nach Empfängertyp und Jahr.

```bash
uv run python src/email_regeln/restore_sent.py
```

Für den echten Lauf `restore(dry_run=False)` aufrufen, optional mit
`only_to_others=True`, um die Selbstnotizen im Quellordner zu lassen.

`COPY` nach `Sent` funktioniert über die Bridge, entgegen der ursprünglichen
Annahme. Zwei Eigenheiten sind dabei zu erwarten:

- Die Bridge sortiert selbst nach Charakter der Nachricht. Von 896
  zurückgeschobenen Mails landeten 86 in `Drafts` (Entwürfe) und die Notizen an
  die eigene Adresse zusätzlich in der `INBOX`.
- Ein `COPY` nach `Sent` legt die Nachricht dort ab, ohne sie aus dem
  Quellordner zu entfernen – anders als bei `Folders/…`, die exklusiv sind.
  Das anschließende `\Deleted` plus `EXPUNGE` im Quellordner ist deshalb nötig
  und lässt die Kopie in `Sent` unangetastet.

Der Weg über einen Zwischenordner ist trotzdem der sichere: Erst dorthin
sammeln, das Ergebnis prüfen, dann nach `Sent` weiterschieben.

`find_lost_sent.py` ist das Diagnose-Gegenstück. Es sichert
`email-state/folder_tree.json` als Backup, vergleicht den alten Snapshot mit dem
Live-Zustand, sucht in allen Ordnern nach Mails mit eigener Absenderadresse und
zeigt Stichproben. Alle `SELECT`s laufen mit `readonly=True`.

Wichtig: Der Vergleich taugt nur, solange der Snapshot älter als der
fragliche Lauf ist. Vor jedem größeren Sortierlauf daher `folder_tree.py`
aktualisieren.
