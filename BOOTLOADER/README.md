# 5. Instalator Bootloader

**[Pobierz najnowszą wersję 2.0.21](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/download/v2026.11.05-installer-2.0.21/GRYFSMART-Instalator.zip)**

Instalator bootloaderów 2.0.21 pod stałą nazwą GRYFSMART-Instalator.exe. ZIP zawiera instalator, AVRDUDE i sześć wsadów bootloadera. Pozostałe pliki dystrybucyjne pochodzą z wydania v2026.11.05-gryfexpert-0.5.49. [Pełny opis wydania](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/tag/v2026.11.05-installer-2.0.21).

## Trzy ostatnie wersje

| Wersja | Data publikacji | Pobieranie | Zmiany |
|---|---|---|---|
| **2.0.21** | 2026-11-05 | [Pobierz](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/download/v2026.11.05-installer-2.0.21/GRYFSMART-Instalator.zip) | Instalator bootloaderów 2.0.21 pod stałą nazwą GRYFSMART-Instalator.exe. ZIP zawiera instalator, AVRDUDE i sześć wsadów bootloadera. Pozostałe pliki dystrybucyjne pochodzą z wydania v2026.11.05-gryfexpert-0.5.49. [Pełny opis](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/tag/v2026.11.05-installer-2.0.21) |
| **2.0.14** | 2026-10-29 | [Pobierz](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/download/v2026.10.29-restarts-all-0.5.15/GRYFSMART-Instalator.zip) | Pakiet instalatora z bootloaderem R0806T-OLD v13-old644p. Pozostałe bootloadery bez zmian. [Pełny opis](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/tag/v2026.10.29-restarts-all-0.5.15) |
| **2.0.13** | 2026-10-29 | [Pobierz](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/download/v2026.10.29-usb-fix-2.0.13/GRYFSMART-Instalator.zip) | Wydanie pakietu narzędzi 2.0.13. Poprawka USB dotyczy aktualizatora; wsady bootloaderów w tym wydaniu pozostały bez zmian. [Pełny opis](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/tag/v2026.10.29-usb-fix-2.0.13) |

## Pierwsza instalacja bootloadera — GRYFSMART-Instalator

**Bootloader wgrywa się tylko raz — przy pierwszym uruchomieniu modułu, który jeszcze go nie ma. Nowy moduł GRYFSMART ma już zainstalowany bootloader.**

Bootloader umożliwia późniejsze wgrywanie najnowszych wersji oprogramowania modułu przez **RS-232 lub Ethernet**, zależnie od modelu i dostępnego połączenia. Nie trzeba go ponownie instalować przy zwykłej aktualizacji oprogramowania. Ponowne wgranie jest potrzebne jedynie przy aktualizacji samego bootloadera.

**Po wgraniu bootloadera obie diody — RUN oraz RX/TX — świecą światłem ciągłym.** Jest to informacja, że bootloader został wgrany i moduł jest gotowy do wgrania aplikacji. Zaczekaj również na zakończenie weryfikacji w instalatorze.

Paczka ZIP z linku na górze zawiera instalator, AVRDUDE i wsady bootloaderów. Rozpakuj całą paczkę, zachowując strukturę katalogów. Sam plik EXE może nie zawierać potrzebnych plików towarzyszących.

1. Zapisz konfigurację instalacji. Zapewnij właściwe zasilanie płytki.
2. Podłącz **USBasp do złącza ISP/ICSP** wybranego modułu: MISO, MOSI, SCK, RESET, GND i właściwe napięcie odniesienia według dokumentacji płytki. RS-232 nie zastępuje ISP przy pierwszej instalacji.
3. Uruchom **GRYFSMART-Instalator.exe**, wybierz dokładny model modułu i sprawdź rozpoznany mikrokontroler.
4. Wybierz wgranie bootloadera. Operacja zmienia Flash i ustawienia startu mikrokontrolera; istniejąca aplikacja może zostać skasowana. Zaczekaj na odczyt, zapis i weryfikację.
5. Odłącz programator ISP i wgraj aplikację odpowiednią dla modelu [aktualizatorem GRYF](../AKTUALIZATOR).

| Model | Mikrokontroler | Zegar | Sekcja bootloadera |
|---|---|---|---|
| ETH0606T | ATmega2560 | 16 MHz | 8 KiB |
| R0808 | ATmega2560 | 18,432 MHz | 8 KiB |
| R0806T / S0804 | ATmega1284P | 18,432 MHz | 8 KiB |
| ETH Mini GATE | ATmega328P | 16 MHz | 4 KiB |

Dla Mini użyj ICSP J5 i zasilania płytki przez XS1; wyłącz zasilanie celu z USBasp i połącz masy. Inne płytki mają własny układ złączy — nie przenoś pinów Mini na inny model.

Kolejne aktualizacje aplikacji wykonuj przez istniejący bootloader. Nie trzeba ponownie instalować go przy każdym wydaniu firmware.


[1. Aplikacja GRYFSMART](https://github.com/GRYF-SMART/gryfsmart-firmware/tree/main/GRYFSMART) · [2. GRYFSMART-Programator](https://github.com/GRYF-SMART/gryfsmart-firmware/tree/main/AKTUALIZATOR) · [3. Driver Home Assistant](https://github.com/GRYF-SMART/gryfsmart-firmware/tree/main/HOME-ASSISTANT) · [4. Driver RTI](https://github.com/GRYF-SMART/gryfsmart-firmware/tree/main/RTI) · [5. Instalator Bootloader](https://github.com/GRYF-SMART/gryfsmart-firmware/tree/main/BOOTLOADER) · [6. Protokół GRYFSMART](https://github.com/GRYF-SMART/gryfsmart-firmware/tree/main/PROTOKOL)
