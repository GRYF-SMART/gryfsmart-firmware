# 1. Aplikacja GRYFSMART

**[Pobierz najnowszą wersję 0.5.51](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/download/v2026.11.12-gryfexpert-0.5.51-rti-2.13/GRYFEXPERT-0.5.51-win-x64.zip)**

GRYFEXPERT 0.5.51 — bramka RTI (wymaga drivera GRYF 2.13). Nowy tryb połączenia Bramka RTI obok COM i Ethernet ETH. Nasłuch TCP, klucz parowania, identyfikator procesora i status. Konfiguracja i diagnostyka modułów przez RS232 procesora RTI, bez ETH. Heartbeat i rozłączenie sesji z przywróceniem pracy drivera. Wgrywanie HEX w tym trybie zablokowane.… [Pełny opis wydania](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/tag/v2026.11.12-gryfexpert-0.5.51-rti-2.13).

## Trzy ostatnie wersje

| Wersja | Data publikacji | Pobieranie | Zmiany |
|---|---|---|---|
| **0.5.51** | 2026-11-12 | [Pobierz](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/download/v2026.11.12-gryfexpert-0.5.51-rti-2.13/GRYFEXPERT-0.5.51-win-x64.zip) | GRYFEXPERT 0.5.51 — bramka RTI (wymaga drivera GRYF 2.13). Nowy tryb połączenia Bramka RTI obok COM i Ethernet ETH. Nasłuch TCP, klucz parowania, identyfikator procesora i status. Konfiguracja i diagnostyka modułów przez RS232 procesora RTI, bez ETH. Heartbeat i rozłączenie sesji z przywróceniem pracy drivera. Wgrywanie HEX w tym trybie zablokowane.… [Pełny opis](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/tag/v2026.11.12-gryfexpert-0.5.51-rti-2.13) |
| **0.5.50** | 2026-11-05 | [Pobierz](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/download/v2026.11.06-gryfexpert-0.5.50/GRYFEXPERT-0.5.50-win-x64.zip) | GRYFEXPERT 0.5.50 dodaje eksport nazw wejść, wyjść, PWM i flag do Integration Designera. Wybierz Plik → Eksportuj nazwy do RTI i wskaż plik .driverconfig wyeksportowany ze sterownika GRYF. [Pełny opis](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/tag/v2026.11.06-gryfexpert-0.5.50) |
| **0.5.49** | 2026-11-05 | [Pobierz](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/download/v2026.11.05-gryfexpert-0.5.49/GRYFEXPERT-0.5.49-win-x64.zip) | GRYFEXPERT 0.5.49 i ETH0606T FW34: AT+BootInfo, wersja bootloadera oraz źródło jej potwierdzenia w logach. Rozpoznana sygnatura lub jawne UNKNOWN przy braku odczytu. Weryfikacja TCP5001 i CHAIN1 przed zapisem Flash. Dokładny etap braku odpowiedzi ETH. Szczegóły: BOOTLOADER-WERSJA-INSTRUKCJA.txt. Pozostałe wsady bez zmian. [Pełny opis](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/tag/v2026.11.05-gryfexpert-0.5.49) |

## Do czego służy program

**GRYFSMART / GRYFEXPERT** to program Windows do konfiguracji sterowników GRYF: modułów, wejść, wyjść, flag, reguł, czasów, PWM i rolet. Nazwa pliku oraz aplikacji pozostaje GRYFEXPERT.

## Uruchomienie

1. Pobierz ZIP z linku na górze, rozpakuj cały katalog i uruchom GRYFEXPERT. Przed podmianą starszej instalacji zapisz projekt i zamknij program; zachowaj swoje projekty.
2. Wybierz **TCP/IP** i adres bramki ETH0606T lub ETH Mini. Dla aktualnego ETH0606T port 5002 służy konfiguratorowi; port 5000 może obsługiwać integrację. ETH Mini domyślnie używa `192.168.1.201:5002` i jednego klienta.
3. Przy połączeniu **RS-232** wybierz port COM, 115200 bit/s, 8N1, bez kontroli przepływu. Port nie może być otwarty w drugim programie.
4. Odczytaj moduły i ich konfigurację. Nadaj nazwy wejściom, wyjściom, roletom i flagom. Zapisz projekt na komputerze; zapis konfiguracji do modułów jest osobną czynnością.
5. Skonfiguruj funkcje odpowiednie dla modelu i wersji firmware, następnie zapisz ustawienia do modułów.

## Nazwy w RTI

W RTI wyeksportuj konfigurację instancji GRYF do `.driverconfig`. W GRYFEXPERT wybierz eksport nazw RTI w menu **Plik**, wskaż ten plik i zapisz wynik. Zaimportuj wynik do tej samej instancji w Integration Designer. ID i typy modułów w obu projektach muszą się zgadzać. [Dokładna instrukcja](../RTI/INSTRUKCJA.md#jak-przenieść-nazwy-z-gryfexpert-do-rti).

[Protokół i przykłady](../PROTOKOL) · [Najnowsze firmware modułów](../HEX)


[1. Aplikacja GRYFSMART](https://github.com/GRYF-SMART/gryfsmart-firmware/tree/main/GRYFSMART) · [2. GRYFSMART-Programator](https://github.com/GRYF-SMART/gryfsmart-firmware/tree/main/AKTUALIZATOR) · [3. Driver Home Assistant](https://github.com/GRYF-SMART/gryfsmart-firmware/tree/main/HOME-ASSISTANT) · [4. Driver RTI](https://github.com/GRYF-SMART/gryfsmart-firmware/tree/main/RTI) · [5. Instalator Bootloader](https://github.com/GRYF-SMART/gryfsmart-firmware/tree/main/BOOTLOADER) · [6. Protokół GRYFSMART](https://github.com/GRYF-SMART/gryfsmart-firmware/tree/main/PROTOKOL) · [7. System i moduły GRYFSMART](https://github.com/GRYF-SMART/gryfsmart-firmware/tree/main/SYSTEM)
