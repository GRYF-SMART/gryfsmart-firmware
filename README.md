# GRYFSMART — publiczne oprogramowanie modułów

Pliki HEX dostępne bez logowania. Najnowsze stabilne wydanie:
https://github.com/GRYF-SMART/gryfsmart-firmware/releases/latest

| Moduł | Wersja | Procesor | Kwarc | Pobieranie |
|---|---|---|---|---|
| ETH0606T | 0007-TEMP5 | ATmega2560 | 16 MHz | [HEX](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/latest/download/ETH0606T-firmware.hex) |
| R0808 | 0008 | ATmega2560 | 18,432 MHz | [HEX](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/latest/download/R0808-firmware.hex) |
| R0806T | 0015 | ATmega1284P | 18,432 MHz | [HEX](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/latest/download/R0806T-firmware.hex) |
| S0804 | 0728 | ATmega1284P | 18,432 MHz | [HEX](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/latest/download/S0804-firmware.hex) |

[Rozpakuj i uruchom programator Windows](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/latest/download/GRYFSMART-Tools.zip).
[Suma SHA-256, wersja i parametry każdego pliku](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/latest/download/gryfsmart-update.json).

## Programator 1.1.2

GRYFSMART-Programator.exe ma logo, wybór modułu, Pobierz najnowszy HEX oraz Pobierz program z GitHub. Obecnie programuje wyłącznie ETH0606T, 16 MHz, przez RS-232 i zainstalowany bootloader v8. R0808, R0806 i S0804 są oznaczone jako w przygotowaniu. Udostępnienie ich wsadów nie włącza obsługi tych modułów w programatorze. R0806 w liście oznacza planowaną rodzinę; dostępny plik jest konkretnie dla R0806T.

ETH0606T: XS2 pin 1 GND, pin 2 TX modułu do RX adaptera, pin 3 RX modułu do TX adaptera. Użyj adaptera RS-232 do MAX232, 115200 8N1. Nie jest to UART TTL ani port CH340 na płytce.

Wybierz ETH0606T, COM i aktualny HEX (program domyślnie wybiera ETH0606T-firmware.hex). Program najpierw uzgadnia STK500v2, potwierdzając odpowiedź AVRISP_2, numer ramki i checksum. Jeśli bootloader działa już po komendzie z terminala, nie trzeba ponownie resetować modułu. AUTO jest domyślnie włączone i w razie potrzeby wysyła AT+BOOT=1 do aplikacji 0006+. Bez odpowiedzi program czeka do 20 sekund na S101 RESET. Log AVRDUDE pojawia się na bieżąco. Zamknij inne programy korzystające z COM. Samo pobieranie pliku nie programuje urządzenia. Pobraną nową paczkę programu rozpakuj po zamknięciu poprzedniej wersji.

Paczka publiczna zawiera programator aplikacji, a nie instalator ISP. Pierwsza instalacja bootloadera wymaga osobnego narzędzia USBasp.

## Zakres wydania

HEX-y zawierają aplikację Flash bez EEPROM i fusebitów. Używaj pliku dla dokładnego modelu, procesora i kwarcu. ETH0606T 0007-TEMP5 dodaje pięć czujników DS18B20 i podgląd WWW. R0808 0008 ma dwa DS18B20; wariant sterowania RS485 DE=PE2/PH3. R0806T 0015 i S0804 0728 obsługują przekazywanie ReadTemp/TempScan do R0808. S0804 migruje EEPROM v2 do v3, ale konfigurację reguł v1 trzeba odtworzyć.

Wydanie zawiera istniejące wsady sprawdzone sumami z metadanych kompilacji. Nie wykonano programowania ani testów na fizycznych modułach podczas publikacji. Dla ETH0606T zasilanie pasożytnicze i pomiary pięciu czujników wymagają potwierdzenia na płytce.

AVRDUDE 8.3: licencja GPL w avrdude-8.3/COPYING; wydanie i odpowiadające źródła: https://github.com/avrdudes/avrdude/releases/tag/v8.3 oraz https://github.com/avrdudes/avrdude/tree/v8.3.

Wersja 1.1.2: poprawiono wykrywanie aktywnego bootloadera i uzgadnianie protokołu przed przekazaniem COM do AVRDUDE. Sprawdzono binarne połączenie oraz odczyt sygnatury ATmega2560 na fizycznym COM2; nie wykonywano zapisu Flash. Testy parsera i aktualizacji: 119 sprawdzeń.
