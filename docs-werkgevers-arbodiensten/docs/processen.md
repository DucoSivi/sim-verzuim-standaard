# Bedrijfsprocessen: Werkgevers ↔ Arbodiensten

Dit document beschrijft de functionele interacties tussen het HR-/salarissysteem van de werkgever en het operationele systeem van de arbodienst.

---

## 1. Initiële Verzuimmelding (Ziekmelding)
* **Trigger:** Werknemer meldt zich ziek bij de werkgever / leidinggevende.
* **Actie werkgever:** Het HR-systeem genereert een `Verzuimmelding` met meldingstype `01` (Eerste dag ziekte) en verstuurt dit bericht.
* **Actie arbodienst:** Het arbodienstsysteem valideert de werknemer, maakt een verzuimdossier aan en start het Poortwachter-termijnbewakingsprotocol.

## 2. Gedeeltelijk Herstel & Volledig Herstel
* **Trigger:** Werknemer hervat werkzaamheden voor een bepaald percentage of meldt zich 100% hersteld.
* **Actie:** Verzending van een `Verzuimmelding` met meldingstype `02` (Gedeeltelijk herstel) of `03` (Volledig herstel).

## 3. Stamgegevens Dienstverband
* **Trigger:** Nieuwe indiensttreding, wijziging van functie of beëindiging dienstverband.
* **Actie:** Periodieke of event-driven aanlevering via `WerknemerDienstverband`.
