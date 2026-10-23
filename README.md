# GRYFSMART — oprogramowanie i bootloadery

[Pobierz programator i instalator Windows 1.2.0](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/latest/download/GRYFSMART-Tools.zip). Rozpakuj cały ZIP.

| Moduł | Aplikacja | Procesor / zegar | Port bootloadera | Bootloader |
|---|---|---|---|---|
| ETH0606T | [0007-TEMP5](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/latest/download/ETH0606T-firmware.hex) | ATmega2560 / 16 MHz | USB USART0 lub RS-232 USART1 | [v9 dual](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/latest/download/ETH0606T-bootloader.hex) |
| R0808 | [0008](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/latest/download/R0808-firmware.hex) | ATmega2560 / 18,432 MHz | USART0 | [v8](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/latest/download/R0808-bootloader.hex) |
| R0806T | [0015](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/latest/download/R0806T-firmware.hex) | ATmega1284P / 18,432 MHz | USART0 | [v8](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/latest/download/R0806T-bootloader.hex) |
| S0804 | [0728](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/latest/download/S0804-firmware.hex) | ATmega1284P / 18,432 MHz | USART0 | [v8](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/latest/download/S0804-bootloader.hex) |

[Wydanie](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/latest) · [Parametry i SHA-256](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/latest/download/gryfsmart-update.json). Dostęp bez logowania.

## Instalacja bootloadera przez USBasp / ISP

Uruchom GRYFSMART-Instalator.exe, wybierz dokładny model i podłącz USBasp do ISP zgodnie ze schematem płytki. Używaj jednego źródła zasilania. Program dobiera procesor i bootloader, sprawdza SHA-256 oraz odczytuje EEPROM i fusebity do Dokumenty/GRYFSMART/Kopie-bootloadera.

Kliknięcie „Wgraj bootloader” kasuje dotychczasową aplikację Flash, bez jej kopii. Instalator przywraca EEPROM, ustawia BOOTRST i obszar bootloadera 8 KiB oraz weryfikuje zapis. LOW i EXTENDED pozostają bez zmian; płytka musi mieć właściwy kwarc i konfigurację zegara. Po instalacji odłącz USBasp, zresetuj moduł i wgraj aplikację programatorem.

## Wgrywanie aplikacji przez USB / RS-232

Uruchom GRYFSMART-Programator.exe, wybierz moduł i COM. Wszystkie bootloadery używają STK500v2, 115200, 8N1.

- ETH0606T: jeden bootloader v9 obsługuje USB na USART0 i RS-232 na USART1. Pierwszy odebrany bajt wybiera port do resetu lub uruchomienia aplikacji. Programuj przez jeden port naraz. Na USB wyłącz AUTO i naciśnij RESET podczas oczekiwania. Na RS-232 aplikacja 0006+ obsługuje AUTO / AT+BOOT=1. Stary v8 obsługiwał tylko USART1; instalator USBasp dodaje obsługę USB.
- R0808, R0806T, S0804: użyj portu 0 / USART0. Kliknij „Sprawdź bootloader” lub „Wgraj aplikację”, następnie naciśnij RESET podczas oczekiwania. AUTO jest wyłączone dla tych modułów.

ETH RS-232: XS2 pin 1 GND, pin 2 TX modułu do RX adaptera, pin 3 RX modułu do TX adaptera. Przy MAX232 użyj adaptera RS-232. USB korzysta z wbudowanego konwertera. Pinout i poziomy elektryczne innych modułów sprawdź na ich schemacie.

Źródło „Plik z komputera” pozwala wskazać HEX. „GitHub — najnowszy HEX” automatycznie pobiera aplikację wybranego modułu, także po zmianie modelu. Program sprawdza model, zegar, SHA-256, format i granicę bootloadera. Pobieranie nie uruchamia zapisu. Zamknij inne programy korzystające z COM. Log: Dokumenty/GRYFSMART/RS232.

## Testy i zawartość

Sprawdzono kompilacje, protokół, sygnatury, adresowanie Flash, ochronę bootloadera i wybór UART w emulatorze oraz pobieranie i wybór modułu w testach Windows. Model operacji SPM nie zastępuje testu fizycznej pamięci. Nowych bootloaderów nie testowano na fizycznych modułach.

Animacja LED występuje tylko w ETH0606T. Pozostałe bootloadery nie przełączają portu wyjść przekaźnikowych. Aplikacje zachowują dotychczasowe wersje i sumy. ETH TEMP5 wymaga potwierdzenia pomiarów pięciu czujników na płytce.

Paczka zawiera oba programy Windows, cztery aplikacje, cztery bootloadery, AVRDUDE i odpowiadające źródła bootloadera GPL. Prywatne źródła aplikacji nie są publikowane.

[Źródła bootloadera i licencja](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/latest/download/GRYFSMART-Bootloader-source.zip). AVRDUDE 8.3: GPL w avrdude-8.3/COPYING; [wydanie i źródła](https://github.com/avrdudes/avrdude/releases/tag/v8.3).
