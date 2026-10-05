# Werkwijze

## De inrichting

| Waar | Wat |
|---|---|
| **Centrale repository** [sim-verzuim-standaard](https://github.com/DucoSivi/sim-verzuim-standaard) | De ingang: dit portaal, vragen, wijzigingsverzoeken en discussies |
| **Repository per koppelvlak** | De releases van dat koppelvlak, met de XSD's en de berichtbeschrijvingen in Git |

De drie koppelvlakrepositories:

- [sim-verzuim-werkgevers-arbodiensten](https://github.com/DucoSivi/sim-verzuim-werkgevers-arbodiensten)
- [sim-verzuim-werkgevers-verzekeraars](https://github.com/DucoSivi/sim-verzuim-werkgevers-verzekeraars)
- [sim-verzuim-arbodiensten-verzekeraars](https://github.com/DucoSivi/sim-verzuim-arbodiensten-verzekeraars)

De berichtpagina's op dit portaal komen rechtstreeks uit die repositories.
Er is dus één bron: wat in de koppelvlakrepository staat, staat na de volgende bouw ook hier.

## Releases

- Per koppelvlak verschijnt elk jaar één GitHub-release, met het jaartal als label.
- Bij de release horen de officiële bestanden: toelichting en functionele beschrijvingen (PDF),
  XML-schema's (XSD), verzuimcontrolecodes (XLS) en de zips.
- De drie meest recente releases zijn **actueel**. Oudere releases blijven beschikbaar als **archief**.
- GitHub telt per bestand hoe vaak het is gedownload. Het portaal toont die tellingen per koppelvlak.

## Twee releases vergelijken

Omdat elke release een versie in Git is, kun je elke twee releases naast elkaar leggen:

```
https://github.com/DucoSivi/<koppelvlakrepository>/compare/<oud>...<nieuw>
```

Je ziet dan per bericht welke elementen erbij zijn gekomen, zijn vervallen of zijn gewijzigd
(voorkomen, formaat, toegestane waarden). Voorbeeld:
[Werkgevers ↔ Arbodiensten 2025 → 2026](https://github.com/DucoSivi/sim-verzuim-werkgevers-arbodiensten/compare/2025...2026).

Daarmee zijn de aparte revisiedocumenten (*met revisie*) niet meer nodig.

## Vragen en wijzigingsverzoeken

- Een vraag of wijzigingsverzoek dien je in via een formulier in de centrale repository.
  Je kiest daarin het koppelvlak; het verzoek krijgt automatisch het label van dat koppelvlak.
- Per koppelvlak is er zo een eigen, gefilterde lijst met vragen en verzoeken.
- Discussies die niet in een formulier passen, horen bij **Discussies**.

!!! tip "Alleen meldingen over je eigen koppelvlak"
    GitHub kan meldingen niet per label filteren. Wie alleen één koppelvlak volgt, kiest bij
    *Watch* voor **Custom → Releases** in die koppelvlakrepository en volgt de gefilterde lijst
    van vragen in de centrale repository.

## Hoe de geschiedenis is opgebouwd

De releases 2019–2026 zijn met een script van sivi.org gehaald en jaar voor jaar in Git gezet.
Het script staat in [`migratie/`](https://github.com/DucoSivi/sim-verzuim-standaard/tree/main/migratie)
en kan voor de echte overgang opnieuw gebruikt worden.
