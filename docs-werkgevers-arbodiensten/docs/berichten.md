# Berichtspecificatie: SIVI Verzuim: Werkgevers ↔ Arbodiensten

De XML-berichten in dit koppelvlak zijn gedefinieerd met XML Schema Definition (XSD).

---

## Schema-overzicht in Repository

In de centrale repository zijn de schema's geplaatst onder [`schema/werkgevers-arbodiensten/`](https://github.com/DucoSivi/sim-verzuim-standaard/tree/main/schema/werkgevers-arbodiensten):

| Schemabestand | Doel |
|:---|:---|
| [`Verzuimmeldingen2026.xsd`](https://github.com/DucoSivi/sim-verzuim-standaard/blob/main/schema/werkgevers-arbodiensten/Verzuimmeldingen2026.xsd) | Primaire transactie |
| [`WerknemerDienstverband2026.xsd`](https://github.com/DucoSivi/sim-verzuim-standaard/blob/main/schema/werkgevers-arbodiensten/WerknemerDienstverband2026.xsd) | Ondersteunende transactie |

### Voorbeeld XML

```xml
<?xml version="1.0" encoding="UTF-8"?>
<SIVIVerzuimBericht xmlns="http://www.sivi.org/verzuim/2026/werkgevers-arbodiensten"
                   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                   versie="2026.1">
    <Kop>
        <BerichtID>MSG-20261001-0001</BerichtID>
        <Aanmaakdatum>2026-10-01T12:00:00</Aanmaakdatum>
        <Domein>werkgevers-arbodiensten</Domein>
    </Kop>
    <Inhoud>
        <WerkgeverID>NL-KVK-12345678</WerkgeverID>
        <WerknemerID>EMP-987654</WerknemerID>
        <Transactiedatum>2026-10-01</Transactiedatum>
        <Status>Actief</Status>
    </Inhoud>
</SIVIVerzuimBericht>
```
