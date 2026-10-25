# GRYFSMART — wersja oprogramowania 21

Find zwraca tekstowy model zamiast liczby: AT+Find=ID,WERSJA,MODEL. Nazwy: R0808, R0806T, S0804, ETH0606T. Format Search i zapis ID pozostają bez zmian. W R/S Find bez parametrów lub z ID=0 odczytuje moduł lokalny; Find=ID odczytuje moduł adresowany, bez zapisu EEPROM. Odbiorniki nadal przyjmują stare odpowiedzi liczbowe, lecz nowe odpowiedzi zawsze zawierają nazwę.

| Moduł | Wersja oprogramowania | Plik |
|---|---|---|
| R0806T | 21 | [R0806T-firmware.hex](R0806T-firmware.hex) |
| R0808 | 21 | [R0808-firmware.hex](R0808-firmware.hex) |
| S0804 | 21 | [S0804-firmware.hex](S0804-firmware.hex) |
| ETH0606T | 21 | [ETH0606T-firmware.hex](ETH0606T-firmware.hex) |

[Dokumentacja Search/Find](../docs/komendy-wspolne.md) · [Przykłady pięciu modułów](../docs/PRZYKLADY.md) · [Manifest](manifest.json) · [SHA-256](SHA256SUMS.txt).

Sprawdzenie w symulatorze AVR: R0806T rules (544), S0804 rules (269), R0808 skeleton (417), R0808 rules (240), S0804 IO (155), ETH firmware (2065), ETH gateway (13). Wszystkie zestawy zakończone bez błędów. Kompilacje produkcyjne z -Werror zakończyły się poprawnie.

Gotowe HEX-y sprawdzono w emulowanej linii R0808 → R0806T → R0806T → S0804 → S0804: Search nadaje i zapisuje pięć ID oraz zwraca właściwe nazwy modeli; wszystkie odczyty Find przechodzą do terminala bez zmian EEPROM. Dodatkowo przeszły testy produkcyjnego HEX ETH: UART, EEPROM, restart, W5500, TCP, HTTP, sondowanie RS-232, walidacja odpowiedzi i dotychczasowe reguły.

Zweryfikowano sumy rekordów HEX, EOF, granice bootloadera oraz SHA-256. Nie programowano fizycznego urządzenia. Paczka zawiera wyłącznie aplikacje modułów. Bootloadery i narzędzia Windows są udostępniane osobno. Kolejna aktualizacja otrzyma numer 22.