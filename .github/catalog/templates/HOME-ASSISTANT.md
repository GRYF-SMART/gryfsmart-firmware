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
