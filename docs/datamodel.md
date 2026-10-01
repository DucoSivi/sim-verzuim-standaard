# Gemeenschappelijk Datamodel & Kernbouwstenen

De kracht van de SIVI Verzuimstandaard is de modulaire opbouw. Hoewel de drie koppelvlakken verschillende transacties ondersteunen, delen zij dezelfde kernbouwstenen.

---

## Gedeelde Entiteiten

| Bouwsteen | Beschrijving | Toegepast in |
|:---|:---|:---|
| **Werkgever** | Identificatie via KVK, Sub-administratienummer en NAW-gegevens. | Alle 3 de koppelvlakken |
| **Werknemer** | BSN, WerknemerID, Geboortedatum, Geslacht en Adres. | Alle 3 de koppelvlakken |
| **Dienstverband** | Arbeidsomvang (uren per week), Functie, Soort contract (vast/bepaald) en CAO-code. | Koppelvlak 1 & 2 |
| **Verzuimperiode** | Eerste ziektedag, Hersteldatum, Percentage arbeidsongeschiktheid. | Alle 3 de koppelvlakken |
| **Codelijsten** | Uniforme coderingen voor Verzuimoorzaken (Vangnet), Verzuimstatussen en Interventietypes. | Alle 3 de koppelvlakken |

---

## Waarom modulaire XSD's?

Door het scheiden van basisdefinities (`SIVIBasisTypes2026.xsd`) van specifieke berichtdefinities (`Verzuimmeldingen2026.xsd`, `VerzuimClaim2026.xsd`) ontstaat maximale herbruikbaarheid zonder redundantie.
