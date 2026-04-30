# 2 Fensterung und Faltung

Materialien der zweiten Vorlesung zu Fensterung, Fensterspektren, Faltung und Anwendungen auf IR-Messungen.

## Inhalt dieses Ordners

- `00_konzept_fensterung_und_faltung.md`
  Vollständiges Vorlesungskonzept und Abgleich mit dem aktuellen Storyboard-Stand.
- `export_block_01_...` bis `export_block_08_...`
  Exportskripte für die einzelnen Vorlesungsblöcke.
- `data/`
  Messdaten für den IR-Block, aktuell:
  - `FF_HT.wav`
  - `FF_TT.wav`
- `png_storyboards/`
  Alle exportierten Bildserien.

## Aktuelle Blockstruktur

- `01_uebergang_ft_zu_fensterung`
- `02_rechteckfenster_als_beobachtung`
- `03_rechteck_zu_sinc`
- `04_faltung_als_fensterkopien`
- `05_herleitung_und_dualitaet`
- `06_fenstervergleich`
- `07_fensterlaenge_und_auflosung`
- `08_ir_messung_und_fensterung`

## Interne Unterstruktur wichtiger Blöcke

### Block 4

- `04A_formelkarte_und_zutaten`
- `04B_faltung_als_ueberlappung`
- `04C1_rampe_und_dirac`
- `04C2_spektrum_und_spektrallinie`
- `04D_cosinus_mit_zwei_linien`
- `04E_mehrere_harmonische`

### Block 5

- `05A_zeitbereichsanalyse`
- `05B_rueckweg_zur_faltung`

### Block 6

- `06A_fenstervergleich`
- `06B_tradeoff_hauptkeule_und_nebenkeulen`

### Block 8

- `08_hochtoener`
- `08_tieftöner`

Jeder dieser beiden Datensätze enthält:

- `08A_ir_ueberblick`
- `08B` bis `08F` Rechteckfenster `40 / 20 / 10 / 5 / 2 ms`
- `08G` bis `08K` Hammingfenster `40 / 20 / 10 / 5 / 2 ms`

## Ordnungsprinzip

- Skripte liegen direkt im Themenordner.
- Storyboards liegen ausschliesslich unter `png_storyboards/`.
- Daten liegen ausschliesslich unter `data/`.
- Temporäre Python-Caches gehören nicht zur Projektstruktur und können gelöscht werden.

## Gestaltungsreferenz

Für neue Exportskripte nicht neu anfangen, sondern die bestehende Stilreferenz verwenden:

- Root-Datei: `../00_vorlesungs_plot_stilguide.md`

Sie fasst Farben, Figure-Grössen, Schriftgrössen und die didaktische Rollenlogik der aktuellen Vorlesungsplots zusammen.
