# GRYFSMART — programator i instalator 2.0.1

## Dokumentacja komend modułów

- [Wszystkie instrukcje i zasady wspólne](docs/README.md)
- [R0808 — 8 wyjść, 8 wejść, 16 reguł, 1 temperatura, 2 porty RS485](docs/R0808.md)
- [R0806T — 6 wyjść, 8 wejść, 1 PWM, 16 reguł, 1 temperatura](docs/R0806T.md)
- [S0804 — 4 rolety, 8 wejść](docs/S0804.md)
- [ETH0606T — 6 wyjść, 6 wejść,  USB/RS-232 i 5 temperatur](docs/ETH0606T.md)

[Pobierz oba programy i wsady](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/latest/download/GRYFSMART-Tools.zip). Rozpakuj cały ZIP.

- [Instalator bootloadera / USBasp](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/latest/download/GRYFSMART-Instalator.zip)
- [Programator aplikacji / USB, RS-232 i sieć do 35 modułów](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/latest/download/GRYFSMART-Programator.zip)
- [Najnowsze wydanie](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/latest) — dostęp bez logowania, również osobne EXE.
- [Manifest wersji i SHA-256](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/latest/download/gryfsmart-update.json)

| Model | Aplikacja | Procesor / zegar | Port logiczny 0 | Bootloader |
|---|---|---|---|---|
| R0808 | [0010](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/latest/download/R0808-firmware.hex) | ATmega2560 / 18,432 MHz | RS-232 USART3 | [v11-chain1](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/latest/download/R0808-bootloader.hex) |
| R0806T | [0017](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/latest/download/R0806T-firmware.hex) | ATmega1284P / 18,432 MHz | USART0 | [v11-chain1](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/latest/download/R0806T-bootloader.hex) |
| S0804 | [0730](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/latest/download/S0804-firmware.hex) | ATmega1284P / 18,432 MHz | USART0 | [v11-chain1](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/latest/download/S0804-bootloader.hex) |
| ETH0606T | [0008-USB-TEMP5](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/latest/download/ETH0606T-firmware.hex) | ATmega2560 / 16 MHz | USB USART0; RS-232 USART1 | [v11-dual-faststart](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/latest/download/ETH0606T-bootloader.hex) |

## Sieć do 35 modułów

Połącz PC z portem 0 pierwszego modułu, port 1 pierwszego z portem 0 drugiego itd. Używaj połączeń i poziomów elektrycznych właściwych dla płytek. Komunikacja: 115200, 8N1, bez kontroli przepływu. 

W programatorze wybierz „Sieć — do 35 modułów”, COM i „Wykryj moduły”. Tabela pokazuje pozycję, model, ID, wersję aplikacji, APP/BOOT, wersję bootloadera w trybie BOOT oraz maski wejść i wyjść. W aplikacji wersja bootloadera jest oznaczona UNKNOWN, ponieważ nie jest potwierdzana odczytem. „Porównaj z GitHub” pobiera wersje najnowszego stabilnego wydania.

Zaznacz wiersz i wybierz „Zgraj wsad + EEPROM” albo „Aktualizuj wybrany”. Źródłem HEX może być komputer lub GitHub. GitHub dobiera plik do wykrytego modelu i sprawdza SHA-256. Przed aktualizacją sieciową program sprawdza topologię i zapisuje kopię aplikacji HEX, EEPROM BIN oraz opis w Dokumenty/GRYFSMART/Kopie. Logi operacji: Dokumenty/GRYFSMART/Siec. Kopia EEPROM wykonana podczas pracy może zawierać zmiany bieżących liczników; nie jest atomowym zdjęciem całego urządzenia. Odczyt nie obejmuje chronionego obszaru bootloadera.

Adresowanie odbywa się po pozycji, a nie ID; powtarzające się ID są dozwolone. Nie przepinaj urządzeń w trakcie operacji. Wyjścia aktualizowanego modułu są wyłączane. Pozostałe moduły wykonują lokalne sterowanie i przekazują ramki serwisowe; ich zwykłe raporty szeregowe są wyciszane na czas obsługi. Sieć nie gwarantuje w tym czasie przekazania zwykłych zdarzeń między urządzeniami.

Każda ramka ma CRC16, numer żądania i potwierdzenie. Program zapisuje kompletne strony Flash, weryfikuje zapis i CRC32 całego obszaru aplikacji przed uruchomieniem. Zapis nie zmienia konfiguracji EEPROM; ostatnie 16 bajtów EEPROM (4080–4095) są zarezerwowane dla stanu aktualizacji.

W terminalu `AT+Discovery` lub `AT+ModuleInfo`, zakończone CR, zwracają informacje lokalnego modułu bez zmiany ID i bez zapisu EEPROM. Program skanuje dalsze pozycje parametryzowaną wersją tych komend. Odczyt pełnego wsadu i aktualizacja odległych pozycji mogą trwać długo: ramki przechodzą kolejno przez każde urządzenie.

## Reset, wejście do bootloadera i odzyskiwanie

Poprawna aplikacja uruchamia się po resecie bez okna oczekiwania bootloadera. Do bootloadera przechodzi się komendą `AT+BOOT=1` zakończoną CR lub poleceniem programu. Pusty wsad albo aktualizacja CHAIN1 przerwana przed potwierdzeniem CRC pozostają w trybie odzyskiwania. RESET nie służy już do wejścia w bootloader przy poprawnej aplikacji.

Po przerwaniu aktualizacji wykonaj skanowanie, wybierz moduł BOOT i ponów aktualizację od początku. Najpierw napraw pierwsze urządzenie BOOT w linii: jego bootloader nie przekazuje ramek do dalszych urządzeń. Kopie nie są automatycznie przywracane, a EEPROM nie jest nadpisywany podczas aktualizacji aplikacji. Bootloader aktualizuje się lokalnie przez ISP, nie przez sieć.

Nowy programator dla R0808/R0806T/S0804 używa CHAIN1 także przy bezpośrednim podłączeniu jednego modułu. Zachowane binarne STK500v2 służy kompatybilności, ale sam zapis zewnętrznym AVRDUDE nie wykonuje transakcji CHAIN1 i nie potwierdza jej znacznika odzyskiwania. Do normalnej aktualizacji i odzyskiwania używaj programu 2.0.1.

RUN i RXTX w bootloaderach R0808/R0806T/S0804: zmiana stanu co 0,3 s podczas oczekiwania oraz co 0,1 s podczas zapisu/weryfikacji. Po sekundzie bez operacji Flash wraca wolne miganie. ETH zachowuje animację oraz STK500v2 na USB USART0 i RS-232 USART1; `AT+BOOT=1` przez USB wymaga aplikacji 0008. Firmware ETH nie został zmieniony w wydaniu 2.0.1.

## Walidacja i źródła

Wydanie jest sprawdzane testami klienta Windows oraz wykonywaniem skompilowanych HEX-ów w emulatorze AVR, w tym łańcuchem 35 modułów, ochroną obszaru bootloadera, CRC, przerwaniem aktualizacji i startem po resecie. Nie wykonano testu na fizycznych modułach ani fizycznej linii 35 urządzeń. Emulator operacji pamięci nie zastępuje próby na sprzęcie.

Paczka zawiera oba programy Windows, AVRDUDE, aplikacje i bootloadery. [Odpowiadające źródła bootloaderów na licencji GPL](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/latest/download/GRYFSMART-Bootloader-source.zip) zawierają instrukcję kompilacji. Prywatne źródła aplikacji modułów nie są publikowane.
