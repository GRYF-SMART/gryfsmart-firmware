# 5. Instalator Bootloader

**[Pobierz najnowszą wersję 2.0.27](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/download/v2026.11.17-jtag-unified/GRYFSMART-Instalator.zip)**

R0806T i R0808: ochrona przed JTAG ujednolicona z S0804. Instalator 2.0.27 wyłącza JTAGEN także dla R0806T i R0808: HIGH 98/99 → D8, albo D0 przy zaprogramowanym EESAVE. Zachowuje EESAVE i EXTENDED; sprawdza zapis ponownym odczytem. Polityka ETH0606T/OLD bez zmian. R0806T: JTAG PC2–PC5 współdzieli wyjścia WY6–WY3. R0808: JTAG PF4–PF7 współdzieli wejścia… [Pełny opis wydania](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/tag/v2026.11.17-jtag-unified).

## Trzy ostatnie wersje

| Wersja | Data publikacji | Pobieranie | Zmiany |
|---|---|---|---|
| **2.0.27** | 2026-11-17 | [Pobierz](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/download/v2026.11.17-jtag-unified/GRYFSMART-Instalator.zip) | R0806T i R0808: ochrona przed JTAG ujednolicona z S0804. Instalator 2.0.27 wyłącza JTAGEN także dla R0806T i R0808: HIGH 98/99 → D8, albo D0 przy zaprogramowanym EESAVE. Zachowuje EESAVE i EXTENDED; sprawdza zapis ponownym odczytem. Polityka ETH0606T/OLD bez zmian. R0806T: JTAG PC2–PC5 współdzieli wyjścia WY6–WY3. R0808: JTAG PF4–PF7 współdzieli wejścia… [Pełny opis](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/tag/v2026.11.17-jtag-unified) |
| **2.0.26** | 2026-11-17 | [Pobierz](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/download/v2026.11.17-s0804-jtag/GRYFSMART-Instalator.zip) | S0804 39 — zwolnienie pinów rolet 2 i 3 zajmowanych przez JTAG. Poprzedni instalator zachowywał JTAGEN; fabryczne HIGH=99 przechodziło na 98, co pozostawiało JTAG na PC2–PC5. To piny zasilania i kierunku rolet 2/3. Raporty czasu mogły działać bez sterowania fizycznymi przekaźnikami. Aplikacja S0804 39 i bootloader v13-chain1-jtag-off zerują przekaźniki i… [Pełny opis](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/tag/v2026.11.17-s0804-jtag) |
| **2.0.25** | 2026-11-13 | [Pobierz](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/download/v2026.11.13-rti-2.17/GRYFSMART-Instalator.zip) | Programator 2.0.25 i GRYFEXPERT 0.5.53 — zgodność z bootloaderem S0804 v12-chain1-led-on. Usunięto błędne odrzucanie aktualnego bootloadera S0804 z komunikatem wymagającym v11-chain1. Zapis przez RS-232 i aktualizacja CHAIN1 akceptują dla S0804 zarówno v11-chain1, jak i v12-chain1-led-on. Lista wersji dla innych modeli i kontrola modelu, MCU oraz protokołu… [Pełny opis](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/tag/v2026.11.13-s0804-compatible) |

## Pierwsza instalacja bootloadera — GRYFSMART-Instalator

**Bootloader wgrywa się tylko raz — przy pierwszym uruchomieniu modułu, który jeszcze go nie ma. Nowy moduł GRYFSMART ma już zainstalowany bootloader.**

Bootloader umożliwia późniejsze wgrywanie najnowszych wersji oprogramowania modułu przez **RS-232 lub Ethernet**, zależnie od modelu i dostępnego połączenia. Nie trzeba go ponownie instalować przy zwykłej aktualizacji oprogramowania. Ponowne wgranie jest potrzebne jedynie przy aktualizacji samego bootloadera.

**Po wgraniu bootloadera obie diody — RUN oraz RX/TX — świecą światłem ciągłym.** Jest to informacja, że bootloader został wgrany i moduł jest gotowy do wgrania aplikacji. Zaczekaj również na zakończenie weryfikacji w instalatorze.

Paczka ZIP z linku na górze zawiera instalator, AVRDUDE i wsady bootloaderów. Rozpakuj całą paczkę, zachowując strukturę katalogów. Sam plik EXE może nie zawierać potrzebnych plików towarzyszących.

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
| ETH Mini GATE | ATmega328P | 16 MHz | 4 KiB |

Dla Mini użyj ICSP J5 i zasilania płytki przez XS1; wyłącz zasilanie celu z USBasp i połącz masy. Inne płytki mają własny układ złączy — nie przenoś pinów Mini na inny model.

Kolejne aktualizacje aplikacji wykonuj przez istniejący bootloader. Nie trzeba ponownie instalować go przy każdym wydaniu firmware.


[1. Aplikacja GRYFSMART](https://github.com/GRYF-SMART/gryfsmart-firmware/tree/main/GRYFSMART) · [2. GRYFSMART-Programator](https://github.com/GRYF-SMART/gryfsmart-firmware/tree/main/AKTUALIZATOR) · [3. Driver Home Assistant](https://github.com/GRYF-SMART/gryfsmart-firmware/tree/main/HOME-ASSISTANT) · [4. Driver RTI](https://github.com/GRYF-SMART/gryfsmart-firmware/tree/main/RTI) · [5. Instalator Bootloader](https://github.com/GRYF-SMART/gryfsmart-firmware/tree/main/BOOTLOADER) · [6. Protokół GRYFSMART](https://github.com/GRYF-SMART/gryfsmart-firmware/tree/main/PROTOKOL) · [7. System i moduły GRYFSMART](https://github.com/GRYF-SMART/gryfsmart-firmware/tree/main/SYSTEM)
