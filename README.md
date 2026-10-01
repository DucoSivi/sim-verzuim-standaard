# SIVI Verzuimstandaard &mdash; Model A (Geïntegreerde Oplossing)

[![GitHub Pages](https://img.shields.io/badge/Docs-GitHub%20Pages-teal.svg)](https://ducosivi.github.io/sim-verzuim-standaard/)
[![Licentie](https://img.shields.io/badge/Licentie-SIVI%20Open-yellow.svg)](https://www.sivi.org)

Dit is de referentie-implementatie van **Model A** voor de SIVI Verzuimstandaard:
* **1 centrale repository** voor alle schema's, documentatie en issues.
* **3 afzonderlijke, doelgroepgerichte documentatiesites** (`docs.io`) op subpaden onder één gezamenlijk portaal!

---

## 📖 Live Documentatie Portalen

| Portaal / Koppelvlak | Doelgroep | Live GitHub Pages Link |
|:---|:---|:---|
| **Centraal Verzuim Portaal** | Alle ketenpartners | 👉 **[https://ducosivi.github.io/sim-verzuim-standaard/](https://ducosivi.github.io/sim-verzuim-standaard/)** |
| **Werkgevers ↔ Arbodiensten** | HR, Salarissoftware & Arbodiensten | 👉 **[https://ducosivi.github.io/sim-verzuim-standaard/werkgevers-arbodiensten/](https://ducosivi.github.io/sim-verzuim-standaard/werkgevers-arbodiensten/)** |
| **Werkgevers ↔ Verzekeraars** | HR, Salarissoftware & Inkomensverzekeraars | 👉 **[https://ducosivi.github.io/sim-verzuim-standaard/werkgevers-verzekeraars/](https://ducosivi.github.io/sim-verzuim-standaard/werkgevers-verzekeraars/)** |
| **Arbodiensten ↔ Verzekeraars** | Arbodiensten & Inkomensverzekeraars | 👉 **[https://ducosivi.github.io/sim-verzuim-standaard/arbodiensten-verzekeraars/](https://ducosivi.github.io/sim-verzuim-standaard/arbodiensten-verzekeraars/)** |

---

## 📁 Repository Structuur

```
sim-verzuim-standaard/
├── .github/workflows/deploy.yml         # CI/CD: bouwt portaal + 3 subdocs naar gh-pages
├── docs/                                 # Centrale portaal documentatie
│   ├── assets/sivi-logo.png
│   ├── stylesheets/sivi.css
│   ├── index.md                          # Overzicht & Koppelvlak-tegels
│   ├── koppelvlakken.md                  # Detailvergelijking
│   ├── datamodel.md                      # Gemeenschappelijk datamodel
│   └── releasebeheer.md                  # Versie- en wijzigingsbeleid
├── docs-werkgevers-arbodiensten/         # Deel 1: Dedicated doc Werkgevers <-> Arbodiensten
│   ├── mkdocs.yml
│   └── docs/ (index, processen, berichten, codelijsten, implementatie)
├── docs-werkgevers-verzekeraars/         # Deel 2: Dedicated doc Werkgevers <-> Verzekeraars
│   ├── mkdocs.yml
│   └── docs/ (index, processen, berichten, codelijsten, implementatie)
├── docs-arbodiensten-verzekeraars/       # Deel 3: Dedicated doc Arbodiensten <-> Verzekeraars
│   ├── mkdocs.yml
│   └── docs/ (index, processen, berichten, codelijsten, implementatie)
├── mkdocs.yml                            # Hoofdconfiguratie centraal portaal
└── schema/                               # Geïntegreerde XSD-schemas onder één dak
    ├── gemeenschappelijk/                # SIVIBasisTypes, Codelijsten
    ├── werkgevers-arbodiensten/          # Verzuimmeldingen, WerknemerDienstverband
    ├── werkgevers-verzekeraars/          # PolisdekkingAanmelding, VerzuimClaim
    └── arbodiensten-verzekeraars/        # InterventieAanvraag, ReintegratieStatus
```

---

&copy; SIVI &mdash; Kennis- en standaardisatie-instituut voor de financiële dienstverlening
