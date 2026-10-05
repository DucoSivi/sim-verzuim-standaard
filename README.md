# Verzuimstandaard: centrale ingang

> **Simulatie.** Zo zou de Verzuimstandaard op GitHub eruitzien in de voorgestelde inrichting.
> De inhoud bestaat uit de officiële publicaties van sivi.org (2019–2026), op 5 oktober 2026 geïmporteerd.

Deze repository is de ingang voor alles rond de Verzuimstandaard:
documentatie, vragen, wijzigingsverzoeken en discussies.
De releases zelf staan per koppelvlak in een eigen repository.

**Portaal:** <https://ducosivi.github.io/sim-verzuim-standaard/>

## De drie koppelvlakken

| Koppelvlak | Releases | Documentatie | Vragen en verzoeken |
|---|---|---|---|
| Werkgevers ↔ Arbodiensten | [sim-verzuim-werkgevers-arbodiensten](https://github.com/DucoSivi/sim-verzuim-werkgevers-arbodiensten/releases) | [portaal](https://ducosivi.github.io/sim-verzuim-standaard/werkgevers-arbodiensten/) | [label](https://github.com/DucoSivi/sim-verzuim-standaard/labels/Werkgevers%20%E2%86%94%20Arbodiensten) |
| Werkgevers ↔ Verzekeraars | [sim-verzuim-werkgevers-verzekeraars](https://github.com/DucoSivi/sim-verzuim-werkgevers-verzekeraars/releases) | [portaal](https://ducosivi.github.io/sim-verzuim-standaard/werkgevers-verzekeraars/) | [label](https://github.com/DucoSivi/sim-verzuim-standaard/labels/Werkgevers%20%E2%86%94%20Verzekeraars) |
| Arbodiensten ↔ Verzekeraars | [sim-verzuim-arbodiensten-verzekeraars](https://github.com/DucoSivi/sim-verzuim-arbodiensten-verzekeraars/releases) | [portaal](https://ducosivi.github.io/sim-verzuim-standaard/arbodiensten-verzekeraars/) | [label](https://github.com/DucoSivi/sim-verzuim-standaard/labels/Arbodiensten%20%E2%86%94%20Verzekeraars) |

## Meedoen

- [Stel een vraag](https://github.com/DucoSivi/sim-verzuim-standaard/issues/new?template=vraag.yml)
- [Dien een wijzigingsverzoek in](https://github.com/DucoSivi/sim-verzuim-standaard/issues/new?template=wijzigingsverzoek.yml)
- [Discussies](https://github.com/DucoSivi/sim-verzuim-standaard/discussions)

In het formulier kies je het koppelvlak. De vraag of het verzoek krijgt dan automatisch het label van dat koppelvlak.

## Wat staat waar

| Map | Inhoud |
|---|---|
| [`portaal/`](portaal) | De bron van het portaal. De berichtpagina's worden bij elke bouw uit de koppelvlakrepositories gehaald. |
| [`migratie/`](migratie) | De scripts waarmee de releases 2019–2026 van sivi.org naar GitHub zijn overgezet |
| [`.github/`](.github) | De formulieren voor vragen en wijzigingsverzoeken, het automatische label en de bouw van het portaal |

Het portaal wordt opnieuw gebouwd bij elke wijziging hier, elke ochtend, en op verzoek.
