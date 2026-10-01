# Bedrijfsprocessen: Werkgevers ↔ Verzekeraars

Dit document beschrijft de interacties tussen werkgevers en inkomensverzekeraars voor dekking, premie en schadeclaims.

---

## 1. Polisdekking & Werknemersbestand
* **Trigger:** Aanvang verzekeringsjaar of mutaties in de werknemerspopulatie.
* **Actie werkgever:** Aanlevering van `PolisdekkingAanmelding` met actuele identificatienummers en loongegevens.

## 2. Verzuimclaim Loondoorbetaling
* **Trigger:** Een werknemer overschrijdt de overeengekomen eigenrisicoperiode / wachtdagen.
* **Actie werkgever:** Verzending van `VerzuimClaim` met historisch dagloon en verzuimpercentage.
