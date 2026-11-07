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
