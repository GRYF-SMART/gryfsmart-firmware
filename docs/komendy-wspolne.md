# Wspólne komendy GRYFSMART — sieć, stan i identyfikacja

Dokumentacja dotyczy firmware **20** wszystkich modułów. Przykładowe odpowiedzi nie są odczytem fizycznych urządzeń.


## Zasady komunikacji i struktura sieci

Podstawą działania sieci GRYFSMART jest **liniowe przekazywanie rozkazów konfiguracyjnych, sterujących i statusowych**. Moduły R0808, R0806T i S0804 mają po dwa porty RS-232 używane do głównej linii: port logiczny 0 od strony sterownika i port logiczny 1 do następnego modułu.

```text
Sterownik / komputer
        │
        ▼
 [port 0 — Moduł 1 — port 1]
                         │
                         ▼
                  [port 0 — Moduł 2 — port 1]
                                          │
                                          ▼
                                   [port 0 — Moduł 3 — port 1] ── …
```

**Maksymalna liczba modułów w jednej linii wynosi 35.** Adresy ID są liczbami 1–35. Nie są adresami IP. Do sterowania adresowanego nadaj modułom indywidualne ID.

Po odebraniu polecenia moduł sprawdza, czy jest ono przeznaczone dla niego. Polecenie lokalne wykonuje i odsyła odpowiedź. Poprawne polecenie do innego ID przekazuje dalej; odpowiedzi i raporty statusowe są przekazywane wzdłuż linii. Nie każde polecenie wybiera odbiorcę przez ID: Discovery wybiera pozycję przez liczbę przejść, a Search używa licznika i nadaje ID — szczegóły poniżej. Discovery/CHAIN1 ma określony kierunek port 0 → port 1.

Domyślne parametry głównej linii RS-232:

**115200 bit/s, 8 bitów danych, bez parzystości, 1 bit stopu (8N1), bez kontroli przepływu. Zamknij inne programy korzystające z danego portu COM.**

Jeżeli moduł udostępnia dodatkowe porty, inne interfejsy lub konfigurowalną prędkość, szczegóły i wyjątki są podane w dokumentacji tego modułu. Numer portu logicznego nie musi odpowiadać numerowi sprzętowego USART.

**ETH0606T ma jeden port RS-232 i może pracować jako bramka Ethernet/TCP ↔ RS-232.** Ma również interfejs USB/USART0. Nie jest kolejnym symetrycznym modułem o dwóch portach RS-232. Obsługę USB, Ethernetu i kierunki przekazywania opisuje [instrukcja ETH0606T](ETH0606T.md).

Komendy są **ciągami znaków ASCII zakończonymi znakiem CR** (`\r`, bajt `0x0D`), zwykle wysyłanym po naciśnięciu Enter w odpowiednio ustawionym terminalu. Zapis `<CR>` w przykładach oznacza znak końca polecenia; nie wpisuj dosłownie tych czterech znaków.

```text
AT+GetOut=1<CR>
```

Odpowiedzi i powiadomienia również są ciągami ASCII. Zakończenie odpowiedzi jest opisane przy danej komendzie: zwykle CRLF (`\r\n`), a niektóre raporty R0806T mają samo CR. Terminal odbiorczy powinien obsługiwać oba warianty. Enter wysyłający CRLF również może być używany w obsługiwanym terminalu.

`TX` oznacza wysyłanie, `RX` odbiór. Odpowiedzi na zapytania i samoczynne raporty mogą się przeplatać. Sprawdzaj prefiks, ID i sumę, jeśli występuje; nie zakładaj, że kolejna odebrana linia jest odpowiedzią na ostatnio wysłany rozkaz.

## Sieć i stan

```text
AT+Loop=0<CR>
AT+LoopReset=0<CR>
AT+ResetStats=0<CR>
AT+Discovery<CR>
AT+Discovery=4,05<CR>
AT+ModuleInfo<CR>
AT+Search=1,5<CR>
```

`Loop` pokazuje liczbę obiegów oraz minimum, średnią i maksimum czasu pętli w mikrosekundach, a także licznik nasycenia: `LOOP=ID,N=...,MIN_US=...,AVG_US=...,MAX_US=...,SAT=0`. `LoopReset` zeruje pomiar i odpowiada `LoopOK=ID`. ID=0 oznacza moduł lokalny. `ResetStats` odczytuje liczbę startów, przyczyny resetów i stan zapisu diagnostyki; nie zeruje tych liczników.

`Discovery` i `ModuleInfo` odczytują informacje bez zapisu EEPROM w R0808, R0806T i S0804. Format parametryzowany to `HOPS_HEX,SEKWENCJA_HEX`: pozycja 5 wymaga hops=4; przykład `4,05` używa sekwencji 05. Odpowiedź `Chain=SEKWENCJA,OK,MODEL;FW;ID;APP;MCU;UNKNOWN;WEJŚCIA;WYJŚCIA;CHAIN1` zawiera model, wersję, ID, MCU i maski IO. **ETH0606T nie implementuje Discovery/ModuleInfo/CHAIN1**; używa Info i osobnych zasad bramkowania opisanych poniżej.

**Search nadaje ID jednej wskazanej pozycji i zapisuje je do EEPROM.** W zapisie `AT+Search=LICZNIK,ILE` drugie pole jest docelową pozycją i nowym ID, a nie liczbą modułów numerowanych jednym wywołaniem. Z początku linii wysyłaj `AT+Search=0,N`. W ramce `AT+Search=1,5` licznik uwzględnia już jedną pozycję; taka ramka występuje przy przekazywaniu wewnątrz linii. Aby nadać ID całej linii, wykonaj osobne wywołanie dla każdej pozycji. Search służy wyłącznie do celowego nadawania ID, nie do skanowania.

`AT+RST=ID` resetuje wskazany moduł. `AT+BOOT=1` wyłącza sterowanie i uruchamia bootloader. W R/S komendę podaje się na porcie logicznym 0: R0808 USART3, R0806T i S0804 USART0. ETH obsługuje ją przez USB/USART0 i RS-232/USART1. Zwykły reset poprawnej aplikacji uruchamia ją bez oczekiwania w bootloaderze.

## 1. Zestawienie identyfikacji i adresowania

Liczby Search i Info są dziesiętne, a HOPS i SEQ w Discovery — szesnastkowe. Te komendy nie mają dodatkowego pola SUMA.

| Komenda | Cel | Wybór modułu | Zapis EEPROM |
|---|---|---|---|
| `AT+Search=LICZNIK,DOCELOWE_ID` | Nadanie ID i identyfikacja | Pozycja liczona od strony nadawcy | Tak, ID wybranego modułu |
| `AT+Discovery` | Identyfikacja modułu lokalnego | Moduł przy terminalu, port logiczny 0 | Nie |
| `AT+Discovery=HOPS,SEQ` | Identyfikacja modułu w linii | Liczba przejść do kolejnych modułów | Nie |
| `AT+Info=ID` | Szczegółowa identyfikacja | Zapisane ID; 0 oznacza moduł lokalny | Nie |

Discovery opisane tutaj obsługują aplikacje R0808, R0806T i S0804 z włączonym `CHAIN_SERVICE`. Aktualna aplikacja ETH0606T nie implementuje tego protokołu. Info jest dostępne również w ETH0606T; jego bramka ma osobne zasady przekazywania, opisane na końcu.

## 2. AT+Search — wyszukanie pozycji i trwałe nadanie ID

### 2.1. Co wysyła sterownik

```text
AT+Search=LICZNIK,DOCELOWE_ID<CR>
```

Spotykany zapis `AT+Search=ID,ILOSC_MODULOW` wymaga doprecyzowania: **pierwsze pole nie jest dotychczasowym ID odbiorcy, a drugie nie oznacza automatycznego ponumerowania wszystkich modułów jedną komendą**.

| Pole | Znaczenie w aktualnej implementacji |
|---|---|
| `LICZNIK` | Liczba pozycji już uwzględnionych przed bieżącym modułem; przy wysyłaniu od początku linii użyj 0 |
| `DOCELOWE_ID` | Docelowa pozycja i jednocześnie nowe ID; zakres 1–35 |

Musi zachodzić `0 <= LICZNIK < DOCELOWE_ID <= 35`. Aby ponumerować N urządzeń od początku linii, sterownik kolejno wysyła `AT+Search=0,1`, `AT+Search=0,2`, ..., `AT+Search=0,N`, oczekując na odpowiedź po każdym wywołaniu.

### 2.2. Co odbiera i wysyła moduł

Każdy moduł liniowy R0808/R0806T/S0804:

1. Odbiera ramkę i zwiększa LICZNIK o 1.
2. Jeżeli wynik jest mniejszy od DOCELOWE_ID, wysyła drugim portem Search ze zwiększonym licznikiem. Nie zmienia własnego ID i nie zapisuje EEPROM.
3. Jeżeli wynik jest równy DOCELOWE_ID, przyjmuje tę wartość jako nowe ID i zapisuje ją do EEPROM. Nie przekazuje Search dalej.
4. Po poprawnym zapisie/weryfikacji odsyła odpowiedź portem, którym przyszła komenda:

```text
AT+Find=ID,WERSJA_FW,TYP<CR><LF>
```

Moduły pośrednie przekazują odpowiedź Find w stronę sterownika. Zapis adresu nie zapisuje całej konfiguracji reguł i czasów; nie wymaga dodatkowego SaveConfig do utrwalenia samego ID.

### 2.3. Parametry odpowiedzi AT+Find

| Pole | Znaczenie | Przykład |
|---|---|---|
| `ID` | Nadany adres logiczny | `3` |
| `WERSJA_FW` | Wersja oprogramowania, z zachowaniem zer na początku | `20` |
| `TYP` | Numeryczny typ modułu | `3` dla S0804 |

| Typ | Model |
|---|---|
| 3 | S0804 |
| 4 | R0806T |
| 5 | R0808 |
| 6 | ETH0606T |

Nazwa pola `MAC` w strukturze modułu przechowuje tutaj wersję firmware, a nie ethernetowy adres MAC. Odpowiedź ma znak `=`: `AT+Find=...`, nie `AT+Find-...`.

### 2.4. Przykład: trzy moduły w linii

```text
Terminal ── M1: R0808 ── M2: R0806T ── M3: S0804
              ID=1          ID=2          ID=3
```

Powyższe ID są wynikiem procedury. Przed jej wykonaniem mogą być inne lub powtarzać się. Wersje w przykładzie: R0808 20, R0806T 20, S0804 20.

**Krok 1 — adresowanie pierwszego modułu:**

```text
Terminal TX → M1:  AT+Search=0,1<CR>
M1: licznik 0 → 1; zapis ID=1 do EEPROM
Terminal RX ← M1:  AT+Find=1,20,5<CR><LF>
```

M2 i M3 nie otrzymują tej komendy.

**Krok 2 — adresowanie drugiego modułu:**

```text
Terminal TX → M1:  AT+Search=0,2<CR>
M1 TX → M2:       AT+Search=1,2<CR><LF>
M2: licznik 1 → 2; zapis ID=2 do EEPROM
M2 TX → M1:       AT+Find=2,20,4<CR><LF>
Terminal RX ← M1:  AT+Find=2,20,4<CR><LF>
```

M1 tylko przekazuje ramki, nie zapisuje ponownie swojego ID. M3 nie otrzymuje Search.

**Krok 3 — adresowanie trzeciego modułu:**

```text
Terminal TX → M1:  AT+Search=0,3<CR>
M1 TX → M2:       AT+Search=1,3<CR><LF>
M2 TX → M3:       AT+Search=2,3<CR><LF>
M3: licznik 2 → 3; zapis ID=3 do EEPROM
M3 TX → M2:       AT+Find=3,20,3<CR><LF>
M2 TX → M1:       AT+Find=3,20,3<CR><LF>
Terminal RX ← M1:  AT+Find=3,20,3<CR><LF>
```

Samo `AT+Search=0,3` adresuje tylko trzeci moduł, a nie wszystkie trzy. Liczenie zależy od strony podłączenia terminala, nie od dotychczasowych ID.

### 2.5. Odrzucenie i brak odpowiedzi

Niepoprawny format/zakres albo niedozwolony stan, np. wykonywanie reguł lub zajęty zapis konfiguracji, może dać `RuleERROR=ID<CR><LF>`. ID w błędzie identyfikuje moduł odrzucający komendę. Nie traktuj braku odpowiedzi jako potwierdzenia zapisu: nieistniejąca pozycja, zerwana linia lub utracona ramka mogą nie wygenerować żadnego błędu zwrotnego. Sterownik powinien stosować timeout i sprawdzić wynik przed następnym krokiem.

## 3. AT+Discovery — rozpoznanie bez zmiany adresów

### 3.1. Zapytanie lokalne

Sterownik wysyła na port logiczny 0:

```text
AT+Discovery<CR>
```

Moduł przy terminalu odpowiada własną identyfikacją. Komenda bez parametrów **nie rozsyła zapytania do wszystkich urządzeń**. `AT+ModuleInfo` jest aliasem tej operacji w protokole CHAIN1.

Przykład dla lokalnego S0804 o zapisanym ID=3, wejściach i wyjściach równych 0:

```text
TX: AT+Discovery<CR>
RX: Chain=0,OK,S0804;20;3;APP;ATmega1284P;UNKNOWN;0;0;CHAIN1*03A2<CR><LF>
```

### 3.2. Zapytanie do pozycji w linii

```text
AT+Discovery=HOPS,SEQ<CR>
```

| Pole | Znaczenie |
|---|---|
| `HOPS` | Liczba przejść dalej, w HEX; 0 = pierwszy moduł, 1 = drugi, 2 = trzeci; maksymalnie `22` HEX = 34 przejścia |
| `SEQ` | Numer zapytania nadany przez sterownik w HEX, 0–FFFF; odpowiedź zachowuje jego zapis |

Discovery nie wymaga znajomości aktualnego ID. Nie zmienia ID ani typu i nie zapisuje EEPROM. Zwraca model, wersję oraz zapisany adres. Typ rozpoznaje się po nazwie modelu, a nie po polu numerycznym TYP z Find.

Na tej samej linii trzech modułów:

```text
Terminal TX → M1:  AT+Discovery=2,03<CR>
M1 TX → M2:       AT+Discovery=1,03<CR><LF>
M2 TX → M3:       AT+Discovery=0,03<CR><LF>
M3 TX → M2:       Chain=03,OK,S0804;20;3;APP;ATmega1284P;UNKNOWN;0;0;CHAIN1*4DFB<CR><LF>
M2 TX → M1:       ta sama odpowiedź Chain
Terminal RX ← M1:  ta sama odpowiedź Chain
```

HOPS maleje na każdym przejściu. SEQ pozostaje bez zmian. Moduły przyjmują zapytania Discovery od strony portu logicznego 0, przekazują je portem 1, a odpowiedzi wracają z portu 1 na port 0. Nie jest to symetryczne adresowanie od dowolnego końca linii, jak w Search.

### 3.3. Format odpowiedzi

```text
Chain=SEQ,OK,MODEL;FW;ID;TRYB;MCU;UNKNOWN;WEJSCIA;WYJSCIA;CHAIN1*CRC16<CR><LF>
```

| Pole | Znaczenie |
|---|---|
| `SEQ` | Numer zapytania; przy komendzie bez parametrów 0 |
| `OK` | Zapytanie obsłużone |
| `MODEL` | R0808, R0806T albo S0804 |
| `FW` | Wersja firmware |
| `ID` | Aktualny adres logiczny, dziesiętnie |
| `TRYB` | `APP` w odpowiedzi działającej aplikacji; bootloader ma osobną implementację |
| `MCU` | Typ mikrokontrolera |
| `UNKNOWN` | Stałe pole tej implementacji; nie jest odczytem numeru seryjnego |
| `WEJSCIA` | Dziesiętna maska stanów wejść, nie liczba wejść |
| `WYJSCIA` | Dziesiętny odczyt PORTC w aktualnych adapterach; interpretacja bitów zależy od modelu, nie jest to liczba wyjść |
| `CHAIN1` | Znacznik obsługi protokołu |
| `CRC16` | Cztery cyfry HEX CRC-16/CCITT; inicjalizacja FFFF, wielomian 1021, zakres od SEQ do CHAIN1, bez `Chain=`, `*` i CRLF |

CRC w przykładach jest policzone dla dokładnie podanych danych. Zmiana ID, wersji lub stanu wejść/wyjść zmieni CRC. Błędne parametry lub brak modułu mogą skutkować ciszą; wymagany jest timeout w sterowniku.

### 3.4. Skanowanie całej linii

Sterownik pyta kolejno `AT+Discovery=0,01`, `AT+Discovery=1,02`, `AT+Discovery=2,03`, itd., za każdym razem czekając na odpowiedź. Wynik daje pozycję, model i dotychczasowe ID bez ich zmiany. Brak odpowiedzi może oznaczać koniec linii, ale też przerwę albo urządzenie bez CHAIN1.

Discovery nie modyfikuje konfiguracji ani wyjść, lecz aktywuje czasowe wyciszanie zwykłych ramek nadawczych przez mechanizm serwisowy `chain_quiet()`. Nie używaj go jako częstego odpytywania podczas sterowania: „bez zapisu EEPROM” nie oznacza braku wpływu na bieżącą komunikację.

## 4. AT+Info — szczegółowe informacje bez zmiany konfiguracji

### 4.1. Co wysyła sterownik

```text
AT+Info=ID<CR>
```

`ID=1..35` wybiera moduł po zapisanym adresie. `ID=0` pyta urządzenie bezpośrednio przy terminalu, nie oznacza broadcastu. Info nie zmienia ID, konfiguracji, stanu wyjść ani zawartości EEPROM.

Moduł liniowy o innym ID przekazuje komendę bez zmiany parametrów drugim portem. Moduł zgodny z ID odpowiada portem wejściowym i nie przekazuje zapytania dalej. Dlatego przy powielonych ID odpowiedź może pochodzić tylko od pierwszego pasującego urządzenia; do rozpoznania pozycji użyj Discovery.

### 4.2. Co odsyła moduł

Odpowiedź jest pojedynczą linią zaczynającą się od `ID=`, a nie `AT+Info=`:

```text
ID=ID,FW=WERSJA,MODEL=MODEL,MCU=MIKROKONTROLER,PCB=REWIZJA,GIT=COMMIT,DIRTY=STAN,UTC=BUILD,SIG=SYGNATURA,CAL=KALIBRACJA,SERIAL=DANE,STATUS=STATUS<CR><LF>
```

ETH0606T dodatkowo wstawia `F_CPU=16000000` po polu MCU.

| Pole | Znaczenie |
|---|---|
| `ID`, `FW`, `MODEL`, `MCU` | Adres, wersja aplikacji, model modułu i mikrokontroler |
| `PCB` | Zadeklarowana przy kompilacji rewizja PCB; nie jest automatycznym rozpoznaniem płytki |
| `GIT`, `DIRTY`, `UTC` | Metadane kompilacji: rewizja źródeł, stan zmian i data/czas kompilacji |
| `SIG` | Sygnatura mikrokontrolera, HEX |
| `CAL` | Odczyt fabrycznego bajtu kalibracji, HEX |
| `SERIAL` | Dziewięć odczytanych bajtów fabrycznych, 18 cyfr HEX; nie traktować jako potwierdzonego unikalnego numeru |
| `STATUS` | `EMPTY` dla samych zer lub FF w SERIAL, w pozostałych przypadkach `UNVERIFIED` |

### 4.3. Przykład odczytu trzeciego modułu

```text
Terminal TX → M1:  AT+Info=3<CR>
M1 TX → M2:       AT+Info=3<CR><LF>
M2 TX → M3:       AT+Info=3<CR><LF>
M3 TX → M2:       ID=3,FW=20,MODEL=S0804,MCU=ATmega1284P,PCB=UNKNOWN,GIT=unknown,DIRTY=unknown,UTC=unknown,SIG=1E9705,CAL=80,SERIAL=000000000000000000,STATUS=EMPTY<CR><LF>
M2 TX → M1:       ta sama odpowiedź ID=...
Terminal RX ← M1:  ta sama odpowiedź ID=...
```

Pola fabryczne i metadane są przykładowe; rzeczywiste wartości zależą od urządzenia i sposobu kompilacji. Zapytanie lokalne `AT+Info=0` zakończyłoby się odpowiedzią M1, nawet gdy jego zapisane ID byłoby inne niż 1.

Przy błędnej komendzie S0804/R0806T mogą odpowiedzieć `RuleERROR=ID`, a R0808/ETH0606T `InfoERROR=ID`. Poprawne Info nie wymaga dodatkowego potwierdzenia RuleOK.

## 5. ETH0606T i rozróżnienie sposobów podłączenia

Przykłady linii M1–M3 dotyczą bezpośredniego podłączenia do R0808/R0806T/S0804. ETH0606T jest bramką/urządzeniem końcowym i nie należy zakładać identycznego przekazywania obu portami.

- Lokalny parser ETH przyjmuje Search i zapisuje ID tylko wtedy, gdy LICZNIK+1 jest równy DOCELOWE_ID; nie realizuje przekazywania Search jak moduł liniowy.
- W ścieżce bramki TCP ETH jest pozycją/ID 1. `AT+Search=0,1` wykonuje odczyt Find urządzenia ETH. Dla kolejnych pozycji bramka przekazuje przez RS-232 np. `AT+Search=1,3` po odebraniu z TCP `AT+Search=0,3`.
- Bramka TCP kieruje adresowane zapytania `AT+Info=2..35` do RS-232. Odczyt lokalny Info dotyczy ETH.
- Aktualne ETH nie obsługuje Discovery/CHAIN1. Nie przenoś przykładu Discovery przez tę bramkę bez osobnego potwierdzenia obsługi w danym firmware.

## 6. Podstawa opisu

- Search i Info: `S0804/src/komendy_at.c`, `R0806T/src/komendy_at.c`, `R0808/src/komendy_at.c`, `R0808/src/diagnostics.c`.
- Discovery: `BOOTLOADER/source/chain/app.inc`, `protocol.h` oraz adaptery `*/src/chain_service.c`.
- ETH: `ETH-0606T/src/komendy_at.c`, `diagnostics.c`, `network/gateway.c`.
- Typy i wersje: `*/src/ustawienia.h`.
