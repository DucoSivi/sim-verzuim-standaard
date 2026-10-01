# Berichtspecificatie: SIVI Verzuim: Arbodiensten ↔ Verzekeraars

De XML-berichten in dit koppelvlak zijn gedefinieerd met XML Schema Definition (XSD).

---

## Schema-overzicht in Repository

In de centrale repository zijn de schema's geplaatst onder [`schema/arbodiensten-verzekeraars/`](https://github.com/DucoSivi/sim-verzuim-standaard/tree/main/schema/arbodiensten-verzekeraars):

| Schemabestand | Doel |
|:---|:---|
| [`InterventieAanvraag2026.xsd`](https://github.com/DucoSivi/sim-verzuim-standaard/blob/main/schema/arbodiensten-verzekeraars/InterventieAanvraag2026.xsd) | Primaire transactie |
| [`ReintegratieStatus2026.xsd`](https://github.com/DucoSivi/sim-verzuim-standaard/blob/main/schema/arbodiensten-verzekeraars/ReintegratieStatus2026.xsd) | Ondersteunende transactie |

### Voorbeeld XML

```xml
<?xml version="1.0" encoding="UTF-8"?>
<SIVIVerzuimBericht xmlns="http://www.sivi.org/verzuim/2026/arbodiensten-verzekeraars"
                   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                   versie="2026.1">
    <Kop>
        <BerichtID>MSG-20261001-0001</BerichtID>
        <Aanmaakdatum>2026-10-01T12:00:00</Aanmaakdatum>
        <Domein>arbodiensten-verzekeraars</Domein>
    </Kop>
    <Inhoud>
        <WerkgeverID>NL-KVK-12345678</WerkgeverID>
        <WerknemerID>EMP-987654</WerknemerID>
        <Transactiedatum>2026-10-01</Transactiedatum>
        <Status>Actief</Status>
    </Inhoud>
</SIVIVerzuimBericht>
```
