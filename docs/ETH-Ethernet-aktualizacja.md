# ETH0606T — firmware 25 i bootloader v12 Ethernet

## Instalacja i późniejsze aktualizacje

1. Pierwszy raz zainstaluj `ETH0606T-bootloader.hex` **v12-ethernet** przez USBasp/ISP, wybierając ETH0606T. Instalacja bootloadera kasuje obecną aplikację i zachowuje EEPROM.
2. Odłącz USBasp. Wgraj `ETH0606T-firmware.hex` **25** przez Ethernet albo przez USB/RS-232.
3. Kolejne aktualizacje aplikacji wykonuj z GRYFEXPERT **0.5.8**: połącz z ETH przez TCP i użyj panelu firmware. Programator i instalator **2.0.12** mają również przycisk aktualizacji ETH przez Ethernet, z wyborem lokalnego HEX lub najnowszego pliku GitHub.

Aplikacja używa TCP **5000**, bootloader TCP **5001**. Podaj faktyczny adres IP ETH. Bootloader odczytuje zapisane ustawienia MAC/IP/maski/bramy z dwóch rekordów EEPROM i sprawdza ich CRC. Bez poprawnego zapisu używa `192.168.1.200/24`. Zmiany IP nieutrwalone w EEPROM nie są ustawieniem bootloadera.

Program najpierw sprawdza tożsamość ETH, aplikację 25+ i `AT+NetBoot=1`. Instalator ustawia lock bits `0x0F`, które chronią bootloader przed zapisem i odczytem przez aplikację. Dlatego aplikacja 25 może zwrócić `NETBOOT=1,UNSUPPORTED` mimo poprawnie zainstalowanego v12. To nie dowodzi braku bootloadera. Narzędzia 2.0.11 i GRYFEXPERT 0.5.7 obsługują tę sytuację: `AT+BOOT=1` wyłącza wyjścia i przechodzi do bootloadera, a następnie program sprawdza jego własną sygnaturę protokołu i MCU ATmega2560 przez TCP 5001. Dopiero poprawna identyfikacja pozwala wysłać nagłówek obrazu i rozpocząć zapis. Zabezpieczenia Flash pozostają bez zmian; poprawnie zainstalowanego v12 nie trzeba wgrywać ponownie przez USBasp.

Narzędzia 2.0.10 błędnie przerywają aktualizację przy `UNSUPPORTED`. Otwarta strona HTTP (port 80) nie jest przyczyną tego błędu. Inny klient sterujący przez TCP 5000, np. Home Assistant lub GRYFEXPERT, może natomiast zajmować jedyne połączenie aplikacji — rozłącz go przed aktualizacją.

Jeśli urządzenie jest już w bootloaderze lub trybie odzyskiwania, program łączy się bezpośrednio z TCP 5001; działająca aplikacja nie jest wtedy potrzebna. Bootloader zachowuje też protokół STK500v2 na USB i RS-232.

Przez Ethernet aktualizowana jest **aplikacja**, nie obszar samego bootloadera. Zmiana bootloadera wymaga ISP. Obszar aplikacji kończy się na `0x3E000`; bootloader mieści się w ostatnich 8 KiB Flash.

## Aktualizacja wszystkich modułów za ETH przez Ethernet

Narzędzia **2.0.12** i GRYFEXPERT **0.5.8** obsługują układ:

```text
PC / HA -- Ethernet TCP 5000 --> ETH0606T ID 1
                                  |
                               RS-232
                                  |
                         port 0 modułu ID 2
                                  |
                         port 1 -> port 0 ID 3 -> kolejne ID 4..35
```

ETH musi mieć aplikację 25 lub nowszą. R0808, R0806T i S0804 wymagają już zainstalowanego zgodnego bootloadera `v11-chain1`, a OLD własnego `v12-old644p`. Do przesyłania aktualizacji dalszych modułów ETH wystarczy rola bramki; bootloader Ethernet v12 ETH jest potrzebny do aktualizacji samego ETH. Pierwsza instalacja bootloaderów nadal wymaga ISP/USBasp.

W GRYFSMART Programator wybierz **Sieć → Ethernet / ETH**, wpisz IP i port 5000, następnie **Wykryj CHAIN1**. Zaznacz **Aktualizuj wszystkie moduły do najnowszej wersji z GitHub**, użyj **Sprawdź całą sieć**, przejrzyj listę wersji i uruchom aktualizację. Z okna aktualizacji pojedynczego ETH możesz przejść przyciskiem **Moduły za ETH — aktualizacja sieci**. W GRYFEXPERT wybierz TCP/IP, połącz z ETH i użyj zakładki zbiorczej **Aktualizacja firmware** albo przycisku aktualizacji pojedynczego modułu.

Pozycja 1 oznacza ETH; pozycja 2 oznacza pierwszy moduł RS232. Zapytanie CHAIN1 do pozycji 2 ma HOPS=0, do pozycji 3 HOPS=1. ETH przekazuje ramkę bez zmiany HOPS i CRC, sam nie jest węzłem CHAIN1. Program rozróżnia pozycję od zapisanego ID i przed zapisem potwierdza model, ID, MCU oraz bootloader wybranego modułu.

Skan nie zmienia adresów ani EEPROM. Do aktualizacji zbiorczej przez ETH ustaw kolejno ID 1,2,3,4…; niezgodność pozycji/ID lub powtórzony adres blokuje serię. W razie potrzeby adresuj moduły oddzielnie przed przygotowaniem planu, np. poleceniami `AT+Search=0,2`, `AT+Search=0,3`, `AT+Search=0,4`, wysyłanymi do ETH i potwierdzanymi odpowiedzią Find po każdej komendzie. Search nadaje adres wskazanej pozycji; nie używaj go jako odczytu diagnostycznego.

Aktualizacja zbiorcza pobiera wsady wszystkich modeli z jednego wydania GitHub i sprawdza SHA-256. Zapisuje tylko wymagające aktualizacji, **od końca linii, ETH na końcu**, a potem sprawdza wszystkie wykryte moduły. Nie odczytuje starego Flash ani nie wykonuje jego kopii. EEPROM konfiguracji jest zachowany; Flash jest sprawdzany CRC i ponownym odczytem tożsamości aplikacji. Brak odpowiedzi na kolejnej pozycji kończy skan po 2 s; moduły za przerwą nie są uznawane za sprawdzone. Brak znanego modułu lub błąd zapisu zatrzymuje serię.

Podczas aktualizacji zwolnij TCP 5000 w HA i pozostałych programach. Każde narzędzie używa własnego połączenia, a ETH przyjmuje jednego klienta sterującego. Strona HTTP na porcie 80 może pozostać otwarta. Aktualizacja wyłącza wyjścia aktualizowanego modułu; ETH jest aktualizowany na końcu, aby wcześniej przekazywał ruch do całej linii.

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
