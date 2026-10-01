# SIVI Verzuimstandaard (Model A)

Welkom bij het centrale documentatieportaal van de **SIVI Verzuimstandaard (Release 2026)**.

In **Model A** worden alle onderdelen van de verzuimketen beheerd vanuit **één centrale repository**, terwijl softwareleveranciers en ketenpartners via gerichte deel-documentaties precies die informatie vinden die voor hún domein relevant is.

---

## 🧭 Direct naar de Koppelvlak-documentaties

Kies hieronder het gewenste domein voor de specifieke processen, XML-berichten en XSD-schema's:

<div class="grid cards" markdown>

-   ### 🏢 ↔ 🩺 Werkgevers & Arbodiensten
    ---
    Gegevensuitwisseling voor ziek- en herstelmeldingen, werknemer- en dienstverbandgegevens, Plan van Aanpak en Poortwachter-termijnbewaking.
    
    👉 **[Naar Koppelvlak Werkgevers ↔ Arbodiensten](werkgevers-arbodiensten/)**

-   ### 🏢 ↔ 🛡️ Werkgevers & Verzekeraars
    ---
    Gegevensuitwisseling voor polisadministratie, premiestelling, wachtdagen en schadeclaims bij loondoorbetaling en ZW/WGA-eigenrisicodragerschap.
    
    👉 **[Naar Koppelvlak Werkgevers ↔ Verzekeraars](werkgevers-verzekeraars/)**

-   ### 🩺 ↔ 🛡️ Arbodiensten & Verzekeraars
    ---
    Gegevensuitwisseling voor re-integratiemonitoring, aanvraag en toekenning van interventiebudgetten en WIA-trajecten met strikte medische privacy.
    
    👉 **[Naar Koppelvlak Arbodiensten ↔ Verzekeraars](arbodiensten-verzekeraars/)**

</div>

---

## Waarom Model A? (Voordelen van de geïntegreerde opzet)

```
                       ┌─────────────────────────────────────────┐
                       │     SIVI Verzuimstandaard (1 repo)     │
                       └────────────────────┬────────────────────┘
                                            │
               ┌────────────────────────────┼────────────────────────────┐
               ▼                            ▼                            ▼
  ┌─────────────────────────┐  ┌─────────────────────────┐  ┌─────────────────────────┐
  │  Werkgevers ↔ Arbo docs │  │  Werkgevers ↔ Verz docs │  │  Arbo ↔ Verzekeraars doc│
  │  (HR / Salaris / Arbo)  │  │  (HR / Inkomensverzek.) │  │  (Arbodienst / Volmacht)│
  └─────────────────────────┘  └─────────────────────────┘  └─────────────────────────┘
```

1. **Eén Waarheid voor Bouwstenen:** Werknemer, Werkgever, Dienstverband en Codelijsten zijn identiek over alle drie de koppelvlakken. Een wijziging wordt in één commit integraal doorgevoerd.
2. **Eigen Documentatiedomein per Community:** Softwarebouwers hoeven niet door specificaties van andere koppelvlakken te bladeren. De documentatie is modulair opgebouwd en heeft eigen zoekfuncties.
3. **Eén Gezamenlijke Issue Tracker:** Ketenproblemen of vragen die meerdere partijen raken (zoals een onduidelijkheid in de verzuimcodelijst) worden op één centrale plek behandeld met labels per koppelvlak (`label:wg-arbo`, `label:wg-verz`, `label:arbo-verz`).
