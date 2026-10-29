# R0806T-OLD — starsza płytka i różnice względem R0806T

R0806T-OLD to **osobny profil sprzętowy**, a nie nazwa starego pliku HEX nowego R0806T. Aktualny firmware OLD ma wersję **4**, a aktualny R0806T ma wersję **27**. Tych numerów nie porównuje się między modelami. Firmware i bootloadery tych płytek nie są zamienne.

| Cecha | R0806T-OLD, firmware 4 | R0806T, firmware 27 |
|---|---|---|
| Procesor i zegar | ATmega644P, 11,0592 MHz | ATmega1284P, 18,432 MHz |
| Obszar aplikacji | do 60 KiB | do 120 KiB |
| Bootloader | osobny `v12-old644p`, ostatnie 4 KiB | profil ATmega1284P, ostatnie 8 KiB |
| EEPROM | 2 KiB, własny format konfiguracji LITE | 4 KiB, format pełnej aplikacji |
| Wejścia i przekaźniki | 8 wejść, 6 wyjść | 8 wejść, 6 wyjść |
| Reguły i timery | 16 reguł, akcje lokalne i zdalne, timery | 16 reguł, akcje lokalne i zdalne, timery |
| Lokalny PWM i rampy | brak | dostępne |
| Zdalny PWM przez SLOT typu 4 | dostępny od OLD 4; steruje innym modułem z PWM | dostępny |
| Temperatura i lokalne termostaty | brak | dostępne |
| Odczyt konfiguracji i stanów na żądanie | brak lokalnego API Get/Info/Factory/Loop/ResetStats | dostępne odczyty konfiguracji, wejść, wyjść i diagnostyki |
| Powiadomienia zmian | PS/PL, I=, o= | PS/PL, I=, o= i raporty funkcji pełnego profilu |
| Identyfikacja | Find oraz Discovery/CHAIN1 | Find, Discovery/CHAIN1 i Info |
| Aktualizacja przez łańcuch | tak, z właściwym bootloaderem OLD | tak, z właściwym bootloaderem R0806T |

## Podłączenie i identyfikacja

Port logiczny 0 to USART0, port 1 to USART1; komunikacja 115200, 8N1. Łańcuch prowadzi od portu 0 do portu 1 następnego modułu. `AT+Find` zwraca nazwę `R0806T-OLD` i wersję 4. Discovery/CHAIN1 identyfikuje procesor jako `ATmega644P`.

W odpowiedzi CHAIN1 aplikacji OLD pola masek wejść i wyjść są w obecnej implementacji stałymi `0`; nie stanowią pomiaru rzeczywistych stanów. Do obserwacji zmian służą raporty I=/o=. Brak odpowiedzi na lokalne Get/Info nie oznacza uszkodzenia połączenia — ten profil nie udostępnia tych odczytów.

## Co działa w OLD

Sterowanie przekaźnikami, ustawienie progów wejść, konfiguracja 16 reguł, zdalne akcje i timery pozostają dostępne. Zapis należy potwierdzać przez RuleOK/SaveOK, bez oczekiwania na lokalny odczyt kontrolny GetRule/GetOut. Domyślne progi przycisków to 0,5 s i 1,5 s.

Od wersji 3 przywrócono raporty PS/PL/I/o; wersja 4 dodaje **zdalną** akcję PWM w SLOT typu 4: akcje 0–4, poziom 0–100%, rampa 0–50 w jednostkach 0,1 s. Nie tworzy to lokalnego wyjścia PWM w OLD. Nieobsługiwane polecenia adresowane do innych modułów i odpowiedzi są przekazywane przez OLD; pełne możliwości zależą od urządzenia docelowego.

Zdalne polecenia roletowe są wykonywane przez S0804. Odwrócenie kierunków w S0804 27 obowiązuje także wtedy, gdy polecenie wysyła reguła OLD, R0806T, R0808, ETH0606T albo program komputerowy.

## Właściwe pliki

- `R0806T-OLD-firmware.hex` — aplikacja OLD 4, do aktualizacji przez programator.
- `R0806T-OLD-bootloader.hex` — bootloader wyłącznie dla ATmega644P 11,0592 MHz; pierwsza instalacja przez ISP/USBasp.
- `R0806T-firmware.hex` — aplikacja nowego R0806T; **nie wgrywać do OLD**.

Wybierz dokładnie profil R0806T-OLD. Nie kopiuj pełnego EEPROM nowego R0806T do OLD: różnią się pojemnością i formatem. `ISP-combined.hex` jest obrazem instalacyjnym ISP, nie aplikacją do aktualizacji RS-232. Nie zmieniaj fuse na wartości nowej płytki.

Programator/Instalator 2.0.9 i GRYFEXPERT 0.5.5 mają profil OLD. Profil pozostaje eksperymentalny; dotychczasowe testy protokołu i kolejek wykonano w symulatorze, co nie potwierdza ustawień fuse ani zachowania każdej fizycznej płytki.

[Pełny R0806T](R0806T.md) · [Sterowanie roletami S0804](rolety-komendy.md) · [Najnowsze pliki i manifest SHA-256](https://github.com/GRYF-SMART/gryfsmart-firmware/releases/latest)
