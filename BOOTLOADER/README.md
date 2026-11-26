# 5. Instalator Bootloader

**[Pobierz najnowszą wersję 2.0.32](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/download/v2026.11.26-r0808-stm-rtc-2/GRYFSMART-Instalator.zip)**

Programator / aktualizator modułów GRYFSMART 2.0.32. Po poprawnym zapisie i weryfikacji firmware komunikat głosowy „Moduł R0806T został zaprogramowany”, z nazwą rzeczywistego modelu. Wszystkie osiem obsługiwanych modeli: ETH0606T, ETH Mini GATE, R0808, R0806T, S0804, R0806T-OLD, S0804-OLD i R0808 STM. Pole „Komunikaty głosowe” wyłącza mowę i przerywa… [Pełny opis wydania](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/tag/v2026.11.26-programator-2.0.32).

## Trzy ostatnie wersje

| Wersja | Data publikacji | Pobieranie | Zmiany |
|---|---|---|---|
| **2.0.32** | 2026-11-26 | [Pobierz](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/download/v2026.11.26-r0808-stm-rtc-2/GRYFSMART-Instalator.zip) | Programator / aktualizator modułów GRYFSMART 2.0.32. Po poprawnym zapisie i weryfikacji firmware komunikat głosowy „Moduł R0806T został zaprogramowany”, z nazwą rzeczywistego modelu. Wszystkie osiem obsługiwanych modeli: ETH0606T, ETH Mini GATE, R0808, R0806T, S0804, R0806T-OLD, S0804-OLD i R0808 STM. Pole „Komunikaty głosowe” wyłącza mowę i przerywa… [Pełny opis](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/tag/v2026.11.26-programator-2.0.32) |
| **2.0.31** | 2026-11-26 | [Pobierz](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/download/v2026.11.26-r0808-stm-1/GRYFSMART-Instalator.zip) | R0808 STM — pierwszy firmware dla STM32F103RET6, kwarc 12 MHz, CPU 72 MHz. Takie same funkcje i obsługa w GRYFEXPERT jak R0808: 8 wejść, 8 przekaźników, 16 reguł, 4 SLOT-y na regułę, timery, flagi, nazwy, 2 czujniki DS18B20, 4 regulatory i Online. Komendy AT zachowują format R0808; osobna identyfikacja sprzętu chroni przed pomyleniem wsadów AVR/STM. Kod… [Pełny opis](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/tag/v2026.11.26-r0808-stm-1) |
| **2.0.30** | 2026-11-24 | [Pobierz](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/download/v2026.11.24-gryfexpert-0.5.79/GRYFSMART-Instalator.zip) | Nowy moduł GRYF S0804 OLD: ATmega644PA, kwarc 11,0592 MHz. Firmware 1: lokalnie tylko OTWÓRZ, STOP, ZAMKNIJ, ZAMKNIJ/STOP i OTWÓRZ/STOP. 16 reguł; jedna zdalna akcja SLOT na regułę. Bez STEP, zadawania procentu, ruchu czasowego i flag lokalnych. Cztery pary przekaźników zasilanie/kierunek: PC0/PC1, PC2/PC3, PC4/PC5, PC6/PC7. Bezpieczny start, wyłączenie… [Pełny opis](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/tag/v2026.11.24-s0804-old-1) |

## Pierwsza instalacja bootloadera — GRYFSMART-Instalator

**Bootloader wgrywa się tylko raz — przy pierwszym uruchomieniu modułu, który jeszcze go nie ma. Nowy moduł GRYFSMART ma już zainstalowany bootloader.**

Bootloader umożliwia późniejsze wgrywanie najnowszych wersji oprogramowania modułu przez **RS-232 lub Ethernet**, zależnie od modelu i dostępnego połączenia. Nie trzeba go ponownie instalować przy zwykłej aktualizacji oprogramowania. Ponowne wgranie jest potrzebne jedynie przy aktualizacji samego bootloadera.

**Po wgraniu bootloadera obie diody — RUN oraz RX/TX — świecą światłem ciągłym.** Jest to informacja, że bootloader został wgrany i moduł jest gotowy do wgrania aplikacji. Zaczekaj również na zakończenie weryfikacji w instalatorze.

Paczka ZIP z linku na górze zawiera instalator, AVRDUDE i wsady bootloaderów. Rozpakuj całą paczkę, zachowując strukturę katalogów. Sam plik EXE może nie zawierać potrzebnych plików towarzyszących.

### R0808 STM — w tym samym instalatorze

Wybierz **R0808 STM**. Pierwsze wgranie wymaga **ST-LINK / SWD** oraz zainstalowanego STM32CubeProgrammer; AVR nadal używa USBasp / ISP. Instalator kontroluje STM32F103RE i 512 KiB Flash, zapisuje kopię pamięci i weryfikuje bootloader. Późniejsze aplikacje wgrywa ten sam GRYFSMART-Programator lub GRYFEXPERT przez RS232 J5. [Instrukcja STM](R0808-STM-v1-INSTRUKCJA.txt).

### Podłączenie programatora — przykład R0806T

![Podłączenie USBasp do dolnego złącza ISP modułu GRYF R0806T](../docs/assets/GRYF-R0806T-podlaczenie-USBasp.png)

Strzałka wskazuje złącze ISP na dole modułu, pomiędzy zaciskami **12V DC** i **INPUT 12–24 VDC**. Podłącz tam wtyk 6-pin programatora, zgodnie z oznaczeniami sygnałów na module. Ilustracja pokazuje miejsce podłączenia w R0806T; położenie złącza w pozostałych modelach może być inne.

### Kolejność instalacji

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
| R0808 STM | STM32F103RET6 | HSE 12 MHz / CPU 72 MHz | 32 KiB, SWD |
| ETH Mini GATE | ATmega328P | 16 MHz | 4 KiB |

Dla Mini użyj ICSP J5 i zasilania płytki przez XS1; wyłącz zasilanie celu z USBasp i połącz masy. Inne płytki mają własny układ złączy — nie przenoś pinów Mini na inny model.

Kolejne aktualizacje aplikacji wykonuj przez istniejący bootloader. Nie trzeba ponownie instalować go przy każdym wydaniu firmware.


[1. Aplikacja GRYFSMART](https://github.com/GRYF-SMART/gryfsmart-firmware/tree/main/GRYFSMART) · [2. GRYFSMART-Programator](https://github.com/GRYF-SMART/gryfsmart-firmware/tree/main/AKTUALIZATOR) · [3. Driver Home Assistant](https://github.com/GRYF-SMART/gryfsmart-firmware/tree/main/HOME-ASSISTANT) · [4. Driver RTI](https://github.com/GRYF-SMART/gryfsmart-firmware/tree/main/RTI) · [5. Instalator Bootloader](https://github.com/GRYF-SMART/gryfsmart-firmware/tree/main/BOOTLOADER) · [6. Protokół GRYFSMART](https://github.com/GRYF-SMART/gryfsmart-firmware/tree/main/PROTOKOL) · [7. System i moduły GRYFSMART](https://github.com/GRYF-SMART/gryfsmart-firmware/tree/main/SYSTEM)
