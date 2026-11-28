# 3. Driver Home Assistant

**[Pobierz najnowszą wersję 0.3.16](https://github.com/GRYF-SMART/ha-gryfsmart/releases/download/v0.3.16/GRYFSMART-HomeAssistant-0.3.16.zip)**

Naprawiono zapis RulePulse (bez nieobsługiwanej sumy), odczyt termostatu z histerezą 0 i walidację tras przez mieszaną magistralę. Dodano modele R0808-STM, S0804-OLD i ETH-Mini-GATE, poprawiono możliwości modeli OLD oraz akcje rolet. Flagi mają osobne encje; edytor reguł zachowuje warunki flag i harmonogramy STM. Akcja administratora… [Pełny opis wydania](https://github.com/GRYF-SMART/ha-gryfsmart/releases/tag/v0.3.16).

## Trzy ostatnie wersje

| Wersja | Data publikacji | Pobieranie | Zmiany |
|---|---|---|---|
| **0.3.16** | 2026-11-28 | [Pobierz](https://github.com/GRYF-SMART/ha-gryfsmart/releases/download/v0.3.16/GRYFSMART-HomeAssistant-0.3.16.zip) | Naprawiono zapis RulePulse (bez nieobsługiwanej sumy), odczyt termostatu z histerezą 0 i walidację tras przez mieszaną magistralę. Dodano modele R0808-STM, S0804-OLD i ETH-Mini-GATE, poprawiono możliwości modeli OLD oraz akcje rolet. Flagi mają osobne encje; edytor reguł zachowuje warunki flag i harmonogramy STM. Akcja administratora… [Pełny opis](https://github.com/GRYF-SMART/ha-gryfsmart/releases/tag/v0.3.16) |
| **0.3.15** | 2026-11-13 | [Pobierz](https://github.com/GRYF-SMART/ha-gryfsmart/releases/download/v0.3.15/GRYFSMART-HomeAssistant-0.3.15.zip) | GRYFSMART Home Assistant 0.3.15 Komplet dziewięciu akcji rolet: OTWÓRZ, STOP, ZAMKNIJ, oba kierunkowe STEP, STEP cykliczny, otwieranie i zamykanie na czas oraz pozycja procentowa. Usługa gryfsmart.shutter_action przyjmuje czas w sekundach dla obu akcji czasowych. Parametry walidowane są przed wysłaniem. Zgodne z protokołem modułów GRYF i GRYFEXPERT 0.5.60.… [Pełny opis](https://github.com/GRYF-SMART/ha-gryfsmart/releases/tag/v0.3.15) |
| **0.3.14** | 2026-11-05 | [Pobierz](https://github.com/GRYF-SMART/ha-gryfsmart/releases/download/v0.3.14/GRYFSMART-HomeAssistant-0.3.14.zip) | R0806T FW35: nowa akcja Włącz po czasie i pozostaw włączone. Stan wyjścia zachowany podczas opóźnienia, po terminie ON. Zdalna akcja wymaga R0806T FW35 na całej drodze. Pozostałe modele bez zmian. Po zakończeniu aktualizacji sprzętu zaktualizuj integrację, zrestartuj HA i odśwież przeglądarkę. [Pełny opis](https://github.com/GRYF-SMART/ha-gryfsmart/releases/tag/v0.3.14) |

## Instalacja przez HACS

Repozytorium integracji: **[GRYF-SMART/ha-gryfsmart](https://github.com/GRYF-SMART/ha-gryfsmart)**.

1. W HACS otwórz menu ⋮ → **Custom repositories / Repozytoria niestandardowe**.
2. Dodaj `https://github.com/GRYF-SMART/ha-gryfsmart`, kategoria **Integration**.
3. Znajdź **GRYFSMART**, pobierz i uruchom ponownie Home Assistant.
4. Otwórz **Ustawienia → Urządzenia i usługi → Dodaj integrację → GRYFSMART**.
5. Wybierz Ethernet lub RS-232 i podaj parametry połączenia. Integracja wymaga HA 2025.6 lub nowszego.

Instalacja ręczna: rozpakuj ZIP z linku na górze i skopiuj katalog `custom_components/gryfsmart` do katalogu `config/custom_components/gryfsmart` w Home Assistant. Następnie uruchom HA ponownie i dodaj integrację.

## Połączenie i obsługa

ETH0606T: adres IP modułu, TCP **5000**. Aktualny firmware umożliwia równoległe połączenie konfiguratora przez 5002. RS-232: **115200, 8N1**, bez kontroli przepływu; użyj stałej ścieżki `/dev/serial/by-id/...` i udostępnij adapter maszynie/ kontenerowi HA.

Po wykryciu modułów integracja tworzy urządzenia i encje wejść, wyjść, rolet oraz dostępnych temperatur i regulatorów. Nazwy oraz grupy można zaimportować z projektu GRYFEXPERT. Flagi są zmiennymi wirtualnymi, oddzielnymi od przekaźników.

S0804: góra, dół, STOP, pozycja procentowa. **0% to zamknięcie, 100% otwarcie.** Po restarcie lub zmianie czasów pozycja może być nieznana; wykonaj pełny przejazd. Pozycja wynika z czasu ruchu, nie z czujnika położenia.

## Panel GRYFSMART

Karta `custom:gryfsmart-home-card` prezentuje urządzenia i pokoje; zasób JavaScript rejestrowany jest przez integrację. Zaimportuj nazwy/grupy z projektu, wybierz układ i dodaj kartę do pulpitu. Edytor reguł i akcji czasowych wymaga firmware obsługującego daną funkcję. Najpierw odczytaj konfigurację, a po zmianach zapisz ją do właściwego modułu.

[Protokół oraz znaczenie raportów](https://github.com/GRYF-SMART/gryfsmart-firmware/tree/main/PROTOKOL) · [Najnowsze HEX-y](https://github.com/GRYF-SMART/gryfsmart-firmware/tree/main/HEX)


## Zgodność integracji — 2026-11-28

RTI 2.23, HA 0.3.16 i GRYFEXPERT 0.5.87 obsługują osiem modeli i adresy 1–35. Poprawiono RulePulse w HA, odczyt histerezy 0 i walidację mieszanej magistrali. Firmware pozostaje bez zmian. [Pełna tabela komend, ograniczenia i instrukcja aktualizacji](https://github.com/GRYF-SMART/gryfsmart-firmware/blob/main/PROTOKOL/COMPATIBILITY.md).


[1. Aplikacja GRYFSMART](https://github.com/GRYF-SMART/gryfsmart-firmware/tree/main/GRYFSMART) · [2. GRYFSMART-Programator](https://github.com/GRYF-SMART/gryfsmart-firmware/tree/main/AKTUALIZATOR) · [3. Driver Home Assistant](https://github.com/GRYF-SMART/gryfsmart-firmware/tree/main/HOME-ASSISTANT) · [4. Driver RTI](https://github.com/GRYF-SMART/gryfsmart-firmware/tree/main/RTI) · [5. Instalator Bootloader](https://github.com/GRYF-SMART/gryfsmart-firmware/tree/main/BOOTLOADER) · [6. Protokół GRYFSMART](https://github.com/GRYF-SMART/gryfsmart-firmware/tree/main/PROTOKOL) · [7. System i moduły GRYFSMART](https://github.com/GRYF-SMART/gryfsmart-firmware/tree/main/SYSTEM)
