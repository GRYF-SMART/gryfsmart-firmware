# ETH0606T — firmware 25 i bootloader v12 Ethernet

## Instalacja i późniejsze aktualizacje

1. Pierwszy raz zainstaluj `ETH0606T-bootloader.hex` **v12-ethernet** przez USBasp/ISP, wybierając ETH0606T. Instalacja bootloadera kasuje obecną aplikację i zachowuje EEPROM.
2. Odłącz USBasp. Wgraj `ETH0606T-firmware.hex` **25** przez Ethernet albo przez USB/RS-232.
3. Kolejne aktualizacje aplikacji wykonuj z GRYFEXPERT **0.5.6**: połącz z ETH przez TCP i użyj panelu firmware. Programator i instalator **2.0.10** mają również przycisk aktualizacji ETH przez Ethernet, z wyborem lokalnego HEX lub najnowszego pliku GitHub.

Aplikacja używa TCP **5000**, bootloader TCP **5001**. Podaj faktyczny adres IP ETH. Bootloader odczytuje zapisane ustawienia MAC/IP/maski/bramy z dwóch rekordów EEPROM i sprawdza ich CRC. Bez poprawnego zapisu używa `192.168.1.200/24`. Zmiany IP nieutrwalone w EEPROM nie są ustawieniem bootloadera.

Program najpierw sprawdza tożsamość ETH i `AT+NetBoot=1`. Odpowiedź `NETBOOT=1,VERSION=12,PORT=5001` potwierdza obecność sygnatury nowego bootloadera. Następnie `AT+BOOT=1` wyłącza wyjścia i przechodzi do bootloadera. Po połączeniu TCP 5001 sprawdzane są sygnatura protokołu oraz MCU ATmega2560, a dopiero potem rozpoczyna się zapis.

Jeśli urządzenie jest już w bootloaderze lub trybie odzyskiwania, program łączy się bezpośrednio z TCP 5001; działająca aplikacja nie jest wtedy potrzebna. Bootloader zachowuje też protokół STK500v2 na USB i RS-232.

Przez Ethernet aktualizowana jest **aplikacja**, nie obszar samego bootloadera. Zmiana bootloadera wymaga ISP. Obszar aplikacji kończy się na `0x3E000`; bootloader mieści się w ostatnich 8 KiB Flash.

## Kontrola i odzyskiwanie

Zapis nie odczytuje starego Flash ani nie wykonuje jego kopii. Każda strona 256 B ma numer i CRC32, jest zapisywana i porównywana z Flash. Po 992 stronach sprawdzane jest CRC32 całego obrazu. Dopiero poprawny wynik pozwala uruchomić aplikację. Program ponownie odczytuje model i wersję po restarcie.

EEPROM `0xFF0` jest zarezerwowany na znacznik przerwanego zapisu. Nie kopiuj do niego własnych danych. Błąd, zerwanie połączenia lub restart po częściowym zapisie pozostawia ETH w bootloaderze zamiast uruchamiać niekompletny program. Ponów zapis w oknie Ethernet; obraz jest przesyłany od początku. Konfiguracja aplikacji i zapisane parametry sieciowe pozostają oddzielone od tego znacznika.

Nowy bootloader korzysta z nowego protokołu TCP; nie jest to STK500v2 przeniesiony na port TCP. Do aktualizacji sieciowej używaj wskazanych wersji programu. Instalator USBasp dołącza właściwy plik bootloadera i sprawdza jego SHA-256.

## Przekazywanie komend i R0806T-OLD

ETH 25 przekazuje z TCP i USB na RS-232 polecenia `AT+...=ID,...` dla ID **2–35**, również polecenia nieznane samemu ETH. ID **1** i lokalne zapytania ID **0** pozostają adresem ETH. Do modułu OLD nie można kierować komend przez ETH pod ID 1.

`Discovery`, `ModuleInfo` i ramki `AT+Chain=...` są przekazywane bez zmiany HOPS, SEQ, danych i CRC. ETH działa jako bramka, a nie kolejny moduł liczony przez HOPS. Search zachowuje osobne zachowanie: ETH zajmuje ID 1, a do linii przekazuje zwiększony licznik.

Odpowiedzi z RS-232, w tym `AT+Find=ID,4,R0806T-OLD`, `Chain=...`, PS/PL/I/o, potwierdzenia zapisu i nieznane przyszłe raporty, trafiają do TCP i USB bez echa na RS-232. Limit linii to 199 znaków bez CR/LF. Przekazanie polecenia nie dodaje OLD funkcji, których nie obsługuje lokalnie, np. GetOut, Info czy lokalnego PWM.

## Walidacja wydania

- 100 kontroli bramki: USB/TCP, komendy przekaźników, reguł, PWM, temperatur, rolet, OLD, CHAIN1, przyszłe ramki, limit linii, brak echa i adres lokalny ETH.
- 2235 kontroli firmware ETH i 29 kontroli przekazywania protokołu roletowego.
- Rzeczywisty kod HEX w modelu AVR/W5500: TCP/USB/RS-232, EEPROM, restart, HTTP, OLD i CHAIN1.
- Nowy bootloader: pełne 992 strony, dzielone pakiety TCP, CRC strony i obrazu, odrzucenie zapisu do bootloadera, uszkodzona strona oraz reset po pierwszej stronie i ponowienie odzyskiwania.
- Klient programu: pełny transfer przez lokalny TCP, zgodność CRC i potwierdzeń, sprawdzenie wersji, odrzucenie HEX innego modelu i HEX bootloadera.
- Regresja obu UART-ów nowego bootloadera: STK500v2, odczyt i zapis, blokada wybranego portu oraz ochrona granicy Flash. GRYFEXPERT przechodzi własny zestaw testów.

Testy wykonano programowo i w modelach sprzętu. Nie programowano fizycznych urządzeń podczas przygotowania wydania.
