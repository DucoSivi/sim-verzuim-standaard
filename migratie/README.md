# Migratie van sivi.org naar GitHub

Met deze scripts zijn de gepubliceerde releases van de Verzuimstandaard van sivi.org gehaald
en per koppelvlak als Git-geschiedenis met GitHub-releases opgezet.
Ze zijn bedoeld om bij de echte overgang opnieuw te gebruiken.

| Stap | Script | Wat het doet |
|---|---|---|
| 1 | `haal_sivi_bestanden.py <cache>` | Leest de drie downloadpagina's en haalt alle PDF-, XSD-, XLS- en ZIP-bestanden op, met een manifest |
| 2 | `bouw_koppelvlakrepos.py <cache> <werk>` | Zet per koppelvlak elk jaar als één versie in Git (`xsd/`, `berichten/`), met het jaartal als label, en zet de bijlagen per release klaar |
| 3 | `maak_releases.py <werk>` | Maakt de GitHub-releases aan met de officiële bestanden als bijlage. Kan veilig opnieuw draaien. |

`xsd_naar_markdown.py` maakt van een XSD een Markdown-pagina met de berichtstructuur.
De namen komen uit de functionele hiërarchie (FunHie-PDF).

## Keuzes

- **Een bestand hoort bij het jaar in zijn eigen adres**, niet bij het kopje op de pagina.
  Op sivi.org staan enkele links onder het verkeerde jaar; zie hieronder.
- **XSD's staan in Git zonder jaartal in de naam** (`Dienstverbanden.xsd`, niet `Dienstverbanden2026.xsd`).
  Alleen dan laat een vergelijking tussen twee jaren de wijzigingen per regel zien.
  De bijlagen bij de release houden hun officiële naam.
- **Regeleinden worden gelijkgetrokken (LF)**, zodat een vergelijking niet op regeleinden struikelt.
- **Elke XSD is zelfstandig.** Geen enkel schema gebruikt `xs:import` of `xs:include`;
  de koppelvlakken delen geen schema's.
- **Commitdatum = publicatiedatum**, zodat de geschiedenis de echte volgorde laat zien.

## Bevindingen op sivi.org (5 oktober 2026)

| Koppelvlak | Link | Staat onder | Hoort bij |
|---|---|---|---|
| Werkgevers ↔ Verzekeraars | Verzuimmelding (xsd) | 2022 | 2024 |
| Werkgevers ↔ Verzekeraars | Download alle bestanden (zip) | 2022 | 2024 |
| Werkgevers ↔ Verzekeraars | Verzuimmelding (xsd) | 2024 | 2022 |
| Werkgevers ↔ Verzekeraars | Download alle bestanden (zip) | 2024 | 2022 |
| Werkgevers ↔ Verzekeraars | Release notes 2022 (pdf) | 2022 | wijst naar Verzuimmelding 2021 met revisie |
| Arbodiensten ↔ Verzekeraars | alle PDF's | 2019 | 2020 |
| Arbodiensten ↔ Verzekeraars | Verzuimmelding Arbodiensten - Verzekeraars (pdf) | 2020 | 2019 |
| Arbodiensten ↔ Verzekeraars | Verzuimrapportage (xsd) | 2020 en 2021 | wijst naar de Verzuimmelding-XSD |
| Arbodiensten ↔ Verzekeraars | Retourmelding met revisie (pdf) | 2019 | wijst naar Rapportage met revisie |
| Werkgevers ↔ Arbodiensten | zip 2024 | 2024 | bevat ook een conflictkopie van OneDrive (`…met revisie-WS-5CG043BXLS.pdf`) |

Daarnaast heten enkele zips "XML schema's 2020" of "2024" terwijl ze bij een ander jaar horen.
Werkgevers ↔ Arbodiensten heeft op sivi.org geen releases van vóór 2022 meer staan.
